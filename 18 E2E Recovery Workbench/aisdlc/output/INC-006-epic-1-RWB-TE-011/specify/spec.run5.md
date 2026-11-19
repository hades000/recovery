---
run_id: INC-006-epic-1-RWB-TE-011
story: RWB-TE-011
title: PDPA lint for code, tests and logs
stage: specify
spec_ids: SPEC-TE011-001..SPEC-TE011-017
change_type: NEW_STORY
ui_in_scope: NO
api_impact: NO_API_CHANGE
prepared: 2026-11-17
revised: 2026-11-18 (remediation after spec gate round 4)
author: Technical Specifier (agent run)
---

# Technical Specification — RWB-TE-011 PDPA lint for code, tests and logs

| Field | Value |
|---|---|
| Story | RWB-TE-011, E1, module P2 Integration, story type Enabler, priority Must (SRC-01 header) |
| RUN_ID | `INC-006-epic-1-RWB-TE-011` |
| Increment card | `aisdlc/docs/increments/INC-006-epic-1-RWB-TE-011.md` (build order 6 of 72, Build Sequence v6) |
| Upstream IDs | `REQ-RDF-010` (Business Requirements Program v4 §6.7), `REQ-ACA-005` (v4 §6.9), `NFR-054` and `NFR-045` (Non-Functional Specification v3), `CTL-11` (Controls Catalog v3); matrix grouping `BR-RWB-013` / `FR-RWB-013` |
| Depends on | RWB-TE-001 (implemented, Traceability Matrix v2.0 row 002). See SPEC-TE011-014 for the code-owner dependency on RWB-TE-002. Later stories that must meet this lint (RWB-E1-001) or own a seam next to it (RWB-E1-043) are in SPEC-TE011-017; this story depends on neither (D-RUN-08). |
| SPEC ID scheme | `SPEC-TE011-nnn`, story-scoped so that IDs do not collide with other runs' `SPEC-nnn` |
| Status | Revised after spec gate round 4 (`review/spec-gate-review-4.md`: FAIL, 0 Critical, 0 High, 3 Medium, 1 Low; SG4-01..SG4-04 and DG4-01/DG4-02), following the orchestrator's triage of 2026-11-18T00:04 (`AI-SDLC-BUILD-LOG.md`). Earlier rounds: 1 (FAIL, 2 Medium, 5 Low), 2 (FAIL, 1 Medium, 1 Low), 3 (FAIL, 2 Low; the round-3 fixes were reviewed in round 4 and found resolved in substance). Every change is mapped in `specify/gate-response.md`. Next: spec gate round 5 (`review/spec-gate-review-5.md`) |

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
| SRC-18 | Decision register: D-RCV-16, D-RCV-50, L-RCV-03, L-RCV-12, L-RCV-13 | `aisdlc/docs/decisions/decision-register.md` |
| SRC-19 | Phase 0 standards audit, findings A-07, A-09, A-10 | `aisdlc/evidence/phase0-standards-audit.md` |
| SRC-20 | Backend context v2.0 §6–§7; backend standards v2.0 BS-1.5, BS-4.6, BS-7.2; testing standards v2.0 §1–§6 | `aisdlc/.github/contexts/` |
| SRC-21 | `AGENTS.md` §3.9, §4.4, §4.7, §6 (acceptance of a story with no business ACs, generalising D-RCV-16), §9; `README.md` "Decisions taken while setting this up" | repository root |
| SRC-22 | Decision Log v10, DL26 (retention and masking; owner Compliance) and D-RCV-29 (line 78: "Later dictionary changes are reference loads through RWB-E1-043") | `legacy/01-decisions-and-governance/recovery-workbench-decision-log-v10-xlsx.md` |
| SRC-23 | RWB-TE-002 specification (run `INC-004-epic-1-RWB-TE-002`, 17 Nov 2026): SPEC-RWB-TE-002-001 (`.gitlab/CODEOWNERS`, GitLab sections), -009 (owner register), validator rules V4, V7, V9 | `aisdlc/output/INC-004-epic-1-RWB-TE-002/specify/spec.md` |
| SRC-24 | RWB-E1-001 specification under revision (run `INC-009-epic-1-RWB-E1-001`, 18 Nov 2026): SPEC-RWB-E1-001-004, -006 (seeds), `ASM-E1001-14` (protective union, 526 fields; Blocker = Yes gap `GAP-E1001-18` awaiting a human ruling); evidence `is_personal_union_v4.tsv` | `aisdlc/output/INC-009-epic-1-RWB-E1-001/specify/` |
| SRC-25 | RWB-E1-043 specification under revision (run `INC-008-epic-1-RWB-E1-043`, 18 Nov 2026): SPEC-RWB-E1-043-031 (dictionary loads and the `is_personal` mark), GAP-38 | `aisdlc/output/INC-008-epic-1-RWB-E1-043/specify/spec.md` |
| SRC-26 | Run decisions D-RUN-07 (migration numbers at merge), D-RUN-08 (dependencies and seams), D-RUN-13 (SQL identifiers versus string literals); orchestrator triage of RWB-TE-011, 2026-11-18T00:04 | `AI-SDLC-BUILD-LOG.md` §1 and the event log |
| SRC-27 | Round-4 evidence of this stage: INSERT count and pattern scan of the Physical Schema v6 copy, statements that write `sys_fields`, name ambiguity of the protective union, today's log calls | `specify/evidence/te011_round4_check.py` and `-output.txt` (run 18 Nov 2026, `python -I`) |

## Change Scope Declaration

| Item | Value | Evidence |
|---|---|---|
| Change Type | `NEW_STORY` | No prior trace chain: Traceability Matrix v2.0 row 006 reads "No current spec/plan"; no `output/INC-006-*` folder existed; no `tools/` folder exists in the repository. The story adds a new build-time flow (SRC-01 §4). |
| UI In Scope | NO | SRC-01 §15: "No screen in this story." |
| Logic In Scope | YES | Six lint rules, allow-list logic and rule generation (SRC-01 §4, §8, §12). |
| API In Scope | NO | No endpoint; SRC-01 §10 "No Workbench capability area applies"; TC-TE-011-11 "This story has no Workbench endpoint". |
| API Impact Type | `NO_API_CHANGE` | As above. API Specification v4 is read as an input file only (SRC-01 §12). |
| Impacted Existing Nodes | `.gitlab-ci.yml` (new job); `.gitlab/CODEOWNERS` delivered by RWB-TE-002 (one new entry in section `[Recovery module]`; RWB-TE-002 spec SPEC-RWB-TE-002-001, L-RCV-12); `scripts/dev.ps1` (local run, recommended) | SRC-01 §13 build step 6; SRC-19 A-09; SPEC-TE011-013, -014 |
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
| A-07 (a): `ApiExceptionHandler` logs raw exception text (`log.error("Unhandled recovery API error", ex)`) | Out of scope | SRC-01 specifies a static, file-reading build check: §13 "Database. None", "Feature flag. None. A build check has no runtime path to switch off", §12 Input lists files only. No AC, BR or flow step changes runtime logging. The lint rules key on personal field names and personal entities (BR2); a raw `Throwable` argument carries neither, so the lint cannot flag it without a rule the story does not contain. The concern is real under Audit and Logging Design v2 §6 and BS-4.6; it needs an owning story (candidate RWB-TE-003, which changes the same class under A-08) or an `AISDLC-HARDENING` change; proposed as a release-readiness open item and an A-07 owner change in `shared-updates.md`. |
| A-07 (b): no correlation ID in the MDC; `X-Correlation-Id` not read or echoed | Out of scope | Not in SRC-01 or SRC-08. `X-Correlation-Id` occurs 0 times in API Specification v4 and in the converted document set. Audit and Logging Design v2 §3 requires a trace ID end to end, and `ProblemFactory` already returns `traceId`. Proposed as an open item for an owner (`shared-updates.md`). |
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
`develop-recovery`; L-RCV-13 protected branches `main`, `develop-recovery`, `develop`).

## Personal data classification used

The lint's field list is the union of (SRC-01 §12, BR1):

1. Every `sys_fields` row with `is_personal = true` in the dictionary as seeded and changed by
   migrations (SRC-06; SPEC-TE011-001), each kept as an (object, field) pair, and
2. Every schema property with `x-personal-data: true` in the API specification (SRC-07), mapped to its
   snake-case field name, with the snake case of its schema name as the object.

**What the lint covers, stated narrowly.** The lint covers the dictionary as seeded and changed by
migrations: the Physical Schema v6 copy (the stand-in for the RWB-E1-001 seed) and the `sys_fields`
statements in the recovery migration folder. Decision Log v10 D-RCV-29 sends "later dictionary changes"
through reference loads of RWB-E1-043 (SRC-22). Such a load changes the database and no repository
file, and this lint reads files only (story §13, §17). A mark added by reference load is therefore not
visible to the lint. That route is a seam owned by RWB-E1-043, a later story (Build Sequence v6 order
8; D-RUN-08). The orchestrator has told the RWB-E1-043 remediation to guard `is_personal` changes on
load (triage 2026-11-18T00:04; SRC-25 SPEC-RWB-E1-043-031). This conflict is recorded as DGL-13.

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
| RWB-E1-001 seeds PS v6 as written (the human ruling on `GAP-E1001-18` goes the other way) | Items (a) and (b) stay open. They close only when a later migration adds the marks with a statement the reader recognises (SPEC-TE011-001). A mark added by reference load does not close them (DGL-13) |

A green lint therefore proves that the fields in the dictionary as seeded and changed by migrations
stay out of code, fixtures and logs: today the 18 marked fields. The story's ACs use a test dictionary
that marks the Background fields (SPEC-TE011-016).

## Functional specification

### SPEC-TE011-001 Personal field reader (BR1; flow step 1; AC5)

**Sources and order** (configuration, SPEC-TE011-015; ASM-TE011-02):

1. The baseline: `infra/postgres/schema/03-recovery-physical-schema-v6.sql`. It is the Physical Schema
   v6 copy that stands in for the dictionary seed RWB-E1-001 delivers (`README.md`;
   `infra/postgres/init/10-load-ace-database.sh`).
2. Then every `*.sql` file in `backend/src/main/resources/db/modulemigration/recovery/`, in Flyway
   version order.
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
| Ignored (cannot change the field list) | `UPDATE sys_fields SET …` whose SET list names none of `is_personal`, `field_id`, `object_name`, `field_name`, `source_field`. `CREATE TABLE sys_fields`. `CREATE [UNIQUE] INDEX … ON sys_fields`. `COMMENT ON TABLE\|COLUMN sys_fields…`. `ALTER TABLE sys_fields ADD CONSTRAINT …`. `GRANT`/`REVOKE … ON sys_fields`. Any statement that only reads `sys_fields` (`SELECT`, a view or an `INSERT INTO <other table> … SELECT … FROM sys_fields`). | None |
| **Fail closed** | Every other statement that writes `sys_fields`. Examples: `DELETE`, `TRUNCATE`, `COPY` (and psql `\copy`), `MERGE`, `INSERT … SELECT`, `INSERT … ON CONFLICT`, a non-literal value in a key column or in `is_personal`, an `UPDATE` of `is_personal` or a key column in any form not listed under R2 (for example `WHERE object_name = …`, a subquery, an expression), any other `ALTER TABLE sys_fields` action, `DROP TABLE sys_fields`, and a `DO` block, function or procedure body that names `sys_fields`. | Exit 2 with `dictionary statement not supported: {file}:{line}`; never the statement text (BR7) |

Physical Schema v6 contains only R1 and ignored statements on `sys_fields`. These are 1,379
single-row INSERTs, 1 `CREATE TABLE`, 1 view that reads it, 1 `ALTER TABLE … ADD CONSTRAINT` and 18
`COMMENT ON`, so the baseline reads without failing (SRC-27).

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
  that reaches only the database, such as a D-RCV-29 reference load, is outside the lint (DGL-13;
  SPEC-TE011-017).
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
- Output is deterministic: entries sorted by field name and rule; no timestamp in the file body (contract
  "Idempotency").

### SPEC-TE011-003 Scan scope (flow steps 3–4; §13 Package)

Scan roots and exclusions are configuration, not code (SRC-01 §6 "Negotiable"; §17). Defaults
(ASM-TE011-05), all relative to the repository root:

| Class | Default roots | Rules applied |
|---|---|---|
| Production source | `backend/src/main/java/th/co/scb/ace/demo/recovery/**/*.java`; `frontend/src/modules/recovery/**/*.{ts,tsx}` excluding `__tests__/**` and `*.test.*` | LOG-FIELD, LOG-ENTITY, EXCEPTION, TOSTRING, FIXTURE-ID |
| Seeds and migrations | `backend/src/main/resources/db/modulemigration/recovery/**/*.sql` | FIXTURE-FIELD, matched by (object, field) against the dictionary at that migration (SPEC-TE011-008); FIXTURE-ID. Never excused by the allow list (SPEC-TE011-011) |
| Tests and fixtures | `backend/src/test/**/*.{java,sql,json}` and `backend/src/test/resources/**`; `frontend/src/modules/recovery/__tests__/**`, `frontend/src/**/*.test.{ts,tsx}`, `frontend/src/test/**`; `frontend/e2e/**/*.{ts,json}` | FIXTURE-FIELD, FIXTURE-ID |
| Local infrastructure | `infra/**` except `infra/postgres/schema/**` (init scripts, mock identity provider, Temporal set-up; repo-authored and a likely place for future SQL seeds, story §4 step 4) | FIXTURE-FIELD, FIXTURE-ID |
| The lint itself | `tools/pdpa-lint/**` | FIXTURE-ID only (self-scan; enforces story §17 "generated at run time and never stored") |

Not scanned: `infra/postgres/schema/**` (three read-only copies: `01-ace-schema-v1.sql`, header "Schema only: no
data rows"; `02-ace-tier2-probe.sql`, DDL only; `03-recovery-physical-schema-v6.sql`, the byte-identical
copy of Physical Schema v6, which holds reference and dictionary seed INSERTs, including the `sys_fields`
seed that is the lint's input. None is a test fixture, and none may be edited in this repository. The
third file holds 2,584 INSERT statements: 1,379 into `sys_fields`, 1 multi-row into `data_product` and
421 `INSERT … SELECT` into `permission`. The pattern scan of 18 Nov 2026 found 0 13-digit runs, 0 dashed
IDs, 0 Thai mobile numbers and 0 e-mail addresses (SRC-27), so the exclusion hides no FIXTURE-ID
match); FIXTURE-FIELD and the log rules on `tools/pdpa-lint/**` (its
fixtures name personal fields by design); `frontend/src/api/schema.d.ts` (generated types; read only to
recognise personal entity types); `node_modules`, `build`, `dist`, `coverage`.

On 17 Nov 2026 the repo-authored `infra/` files hold no personal-field literal, no 13-digit number and
only e-mail addresses in the reserved domain `local.test` (grep), so the added roots keep the zero-finding
baseline (SPEC-TE011-016).

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
on one object and not on another: `status` is personal on `recovery_case` and not on `listing`. A
position is personal when its resolved (object, field) equals a key of a personal field
(SPEC-TE011-001).

| File type | Position and object | Object resolution |
|---|---|---|
| SQL (`.sql` files) | `INSERT INTO <t> (<cols>) VALUES (<row>)[, (<row>)]…`: the value in a column `<c>`. `INSERT INTO <t> (<cols>) SELECT <list> …`: a literal in the select list at column `<c>`. `UPDATE <t> SET <c> = <literal>`. | `<t>`, with any schema qualifier removed (`${recoverySchema}.`, `recovery.`, `public.`, quoted). The key is (`<t>`, `<c>`). It also matches a source-field key, so `public.customer (surname)` matches DF-ACE-058. |
| Java / TypeScript test source | `setXxx(<literal>)` or builder `.xxx(<literal>)` on a receiver; `<receiver>.xxx = <literal>`; object-literal property `xxx: <literal>`. | The declared type of the receiver, builder or object literal, resolved in the same file: (1) a generated entity type name (SPEC-TE011-002: `CustomerEntity` → `v_ace_customer`); (2) a JPA `@Table(name = "<t>")` on a type declared in a scanned file; (3) an API schema type from `frontend/src/api/schema.d.ts` (`components["schemas"]["DocumentField"]` → `document_field`). |
| JSON | The value of a key at any depth. | A `fixtureObjects` entry in configuration, mapping a path glob to an object (SPEC-TE011-015). |

**When no object can be resolved** (a JSON file with no `fixtureObjects` entry, a bare
`xxx = <literal>`, an untyped object literal), the lint applies the (object, field) test across the
whole dictionary:

- If the name is **unambiguous** (every dictionary row with that name is personal; SPEC-TE011-002), the
  position is a finding. No non-personal (object, field) pair has that name, so the result cannot be a
  match against the wrong object. This keeps every PS v6 field and every Restricted field checked in
  JSON and test source (SRC-27).
- If the name is **ambiguous**, the position is not a finding. The run prints
  `PDPA-NOTICE: {file}:{line} object not resolved for {field}; add a fixtureObjects entry or a typed
  receiver` (field name only, no value). A notice does not change the exit code. This is the remaining
  gap of object scoping, and it is reported on every run, not hidden (ASM-TE011-20).

**Migrations use the dictionary at that point.** A file in the recovery migration folder is checked
against the dictionary as it stands after that file has been read (SPEC-TE011-001). Two consequences:

- The migration's own `sys_fields` rows count. RWB-E1-001's seed is checked against the classification
  it seeds.
- A mark added by a later migration does not turn a merged migration red. A merged migration is never
  edited (`AGENTS.md` §4.6), and the allow list never excuses a migration (SPEC-TE011-011). Instead the
  run prints `PDPA-NOTICE: {file}:{line} seeds {field}, marked personal by a later migration` (no value),
  so code owners can decide on a corrective migration (ASM-TE011-21).

Every other scanned file is checked against the full dictionary (baseline, every migration, API).

**Dictionary and reference seed tables.** These rules alone keep `sys_fields`, `sys_objects`,
`data_product`, `lov_value`, `role` and `permission` seed rows clean. Their columns `field_name`,
`description`, `source_system` and `owner_role` share names with personal fields on other objects, but
the (object, field) pairs differ. Under the protective union, the only personal pair on those six tables
is `data_product.owner_user_id` (SRC-27). RWB-E1-001 seeds it `NULL` (SRC-24 SPEC-RWB-E1-001-006), and
`NULL` is never a finding. No table is exempted by name, so a personal column added to one of these
tables later is still checked. A system test proves this (TS-TE011-01).

**Other rules.**

- `NULL`, an empty string and SQL `DEFAULT` are never a finding.
- Non-text personal fields (`date_of_birth` DATE; `capture_latitude`, `capture_longitude` numeric) cannot
  carry the prefix. Any non-null literal in such a position is a finding. Outside the migration folder
  it can be allow-listed (BR3 read as written; DGL-08).
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
  recovery migration folder (`backend/src/main/resources/db/modulemigration/recovery/`) is invalid: exit
  2, naming the entry index. Every entry must expire, and a merged migration can never be edited
  (`AGENTS.md` §4.6). An entry for a migration would therefore expire and fail every later pipeline
  with no fix available. A finding in an unmerged migration is fixed in the file before merge. A later
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
  the same way, then a count of each kind. They are three: an unmarking, an object that could not be
  resolved for an ambiguous name, and a merged migration that touches a later mark. A notice carries a
  field ID or field name, a file and a line, never a value. It does not change the exit code. Notices
  are kept in the CI artifact with the console output.
- Exit code: 0 no unexcused finding; 1 at least one; 2 configuration or input error, including an
  unsupported dictionary statement (SPEC-TE011-001) and an allow entry on a migration (SPEC-TE011-011)
  (ASM-TE011-14).
- The lint holds no state between runs; a failed run is repeated by rerunning the pipeline.

### SPEC-TE011-013 Pipeline job (flow step 7; §13 build step 6; A-09 PDPA part)

- New job `pdpa-lint` in `.gitlab-ci.yml`, stage `verify`, no `rules:` filter, so it runs in every
  pipeline, as the existing `backend-unit` and `frontend-check` do (merge requests and every branch
  build, which covers `main`, `develop-recovery`, `develop`; D-RCV-50, L-RCV-13).
- The job runs the tool's unit tests with coverage verification, then the lint over the repository; any
  non-zero exit fails the job. `pdpa-rules.yaml` and the console output are kept as artifacts
  (`when: always`).
- In ACE the same check runs in the ACE pipeline on the `develop-recovery` merge request (D-RCV-50; header
  comment of `.gitlab-ci.yml`).
- Recommended for the plan: a local entry point in `scripts/dev.ps1` so that a developer can run the lint
  before pushing (SRC-01 §10 "RW-TRIBE … Run the lint").

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
anywhere: they need no exemption (SPEC-TE011-008).
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
| (1) This story's merge | Baseline: PS v6 copy, 18 fields; the migration folder holds no `sys_fields` statement. API v4: 5 properties | 0 findings. The only e-mail literals are in `local.test`, a reserved `.test` domain (ASM-TE011-08). No 13-digit number, no Thai mobile number, no personal-field literal (grep, 17 Nov 2026). The implementation stage records the run. |
| (2) RWB-E1-001's merge, if it seeds the protective union | RWB-E1-001's migration replaces the baseline rows: 526 fields | 0 findings is RWB-E1-001's merge condition (SPEC-TE011-017). On the files that exist on 18 Nov 2026, 0 findings are expected; files merged between orders 6 and 9 were each checked by this lint when they merged, but against the smaller baseline dictionary, so RWB-E1-001's merge request is where any new finding on them first shows. The four back-end log calls use no union name. The keys in `infra/mock-oidc/config.json` (`name`, `sub`, `preferred_username`, `roles`, `aud`) are not personal on any object. The SQL in `RecoveryDatabaseIT.java` sits in Java strings, which are not a SQL position (SPEC-TE011-008). On RWB-E1-001's own migration, the six dictionary and reference seed tables raise 0 FIXTURE-FIELD findings under (object, field) matching. The only personal pair among them is `data_product.owner_user_id`, which RWB-E1-001 seeds `NULL` (SRC-24, SRC-27). The 4,274 name-only findings that review SG4-01 counted do not arise. No allow entry may be used for it (SPEC-TE011-011). |
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
meet, or the seams they own. The orchestrator has already passed each one to the owning remediation run.

| Story (order) | Obligation or seam | Why |
|---|---|---|
| RWB-E1-001 (9) | **Seed the protective classification as parseable `INSERT` values.** The `sys_fields` seed in its baseline migration uses form R1 of SPEC-TE011-001: single-row or multi-row `INSERT … VALUES` with literal `field_id`, `object_name`, `field_name` and `is_personal`. It sets `is_personal` in the row itself. It does not use a bulk `UPDATE`, `ON CONFLICT`, `INSERT … SELECT` or `COPY`; any of those fails this lint closed. | Without this, the 526-field union never reaches the lint (review SG4-03). |
| RWB-E1-001 (9) | **Pass this lint with zero findings** on its merge request, with no allow-list entry for its migration (SPEC-TE011-011). Its seed values for personal (object, field) pairs are `NULL` or start with `SYN-`. | The `pdpa-lint` job runs on every pipeline (SPEC-TE011-013). |
| RWB-E1-043 (8) | **Seam: dictionary changes by reference load (D-RCV-29).** This lint does not see them. RWB-E1-043 owns guarding `is_personal` changes on load; the orchestrator has told its remediation to do so. RWB-E1-043's spec asks this story to read loaded dictionary versions (SRC-25, GAP-38). This story does not: it is earlier in the build sequence (D-RUN-08), and story §13 and §17 forbid a database read. A later story may commit a dictionary export in form R1; SPEC-TE011-001 item 3 then reads it with no code change. | Decision Log v10 D-RCV-29 (SRC-22); DGL-13. |

Until RWB-E1-001 merges, the lint's dictionary is the PS v6 baseline (state 1 of SPEC-TE011-016). The
residual risk and its two outcomes are in "Personal data classification used".

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
| Lint running | Dictionary or API file missing or unparsable, unsupported statement writing `sys_fields`, duplicate seed row across migrations, `UPDATE` of an unknown `field_id`, empty field list, invalid allow-list entry (including any entry on a migration) or configuration | Fail (exit 2) |
| Lint running | Only notices (unmarking, unresolved object for an ambiguous name, later mark on a merged migration) | Pass (exit 0); notices printed and kept |

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
| T3 | Source file the lint cannot parse | Fail | exit 2, file and line, no source text | -012 |
| T4 | Statement writing `sys_fields` that the reader cannot interpret (for example `DELETE`, `COPY`, `INSERT … SELECT`, `ON CONFLICT`, bulk `UPDATE`), a duplicate seed row across migrations, or an `UPDATE` of an unknown `field_id` | Fail closed | exit 2, `dictionary statement not supported: {file}:{line}` or the duplicate/unknown ID message, no SQL text | -001 |
| T5 | A later source turns a mark from `true` to `false` | Applied; build result unchanged | `PDPA-NOTICE: {field_id} unmarked at {file}:{line}` | -001 |
| T6 | Fixture position with an ambiguous personal name and no resolvable object | Not a finding | `PDPA-NOTICE: … object not resolved for {field} …` | -008 |
| T7 | Merged migration seeds a field that a later migration marks personal | Not a finding | `PDPA-NOTICE: … marked personal by a later migration` | -008 |
| T8 | Dictionary mark added by D-RCV-29 reference load | Not visible to the lint (files only) | none; seam owned by RWB-E1-043 | -001, -017 |

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
  allow-list handling (-011) and PdpaLintStep (-012, -013). The splitter is the tool's own code; it does
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
    unambiguousName: true      # every dictionary row named last_name is personal
    dataType: TEXT
    variants: [last_name, lastName, getLastName]
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
| Backend | YES (build tooling `tools/pdpa-lint/`; application code unchanged) | REQUIRED | ≥ 80% for lines, branches, methods and instructions (JaCoCo LINE, BRANCH, METHOD, INSTRUCTION) on `tools/pdpa-lint` production classes, enforced by a coverage verification task that fails the job below threshold | SPEC-TE011-001..-017; BR1–BR7; AC1–AC10 | New code with logic (SRC-01 §13). BS-7.2 and testing standards §6 set 80%. Results and native reports per `.github/rules/implementation-execution-gates.md` under `output/<RUN_ID>/implement/unit-tests/`. | Per rule: positive (finding), negative (no finding), boundary and error path, listed in "Test requirements". Every test asserts that no fixture value appears in the output (BR7). |

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

Additional system tests (the full lint against synthetic fixture trees; added after spec gate round 4):

| ID | SPEC | Fixture and assertion |
|---|---|---|
| TS-TE011-01 | -001, -008, -011, -016, -017 | **Dictionary seed tables raise no finding.** It uses a synthetic migration shaped like RWB-E1-001's baseline. It holds a multi-row and a single-row `INSERT INTO ${recoverySchema}.sys_fields (field_id, object_name, field_name, …, source_system, source_field, is_personal, description, owner_role)`. Those rows mark `description`, `owner_role`, `field_name` and `source_system` personal on synthetic business objects (for example `case_note.description`, `team_assignment.owner_role`). It also holds `INSERT INTO ${recoverySchema}.sys_objects (…, description)` and `INSERT INTO ${recoverySchema}.data_product (…, owner_role, owner_user_id)` with `owner_role = 'RW-DATASTEW'` and `owner_user_id` `NULL`. All values are non-`SYN-` text. **Assert:** 0 FIXTURE-FIELD findings on every `sys_fields`, `sys_objects` and `data_product` row. **Assert:** exactly 1 finding on a business-table row in the same file (`INSERT INTO case_note (description) VALUES ('<free text>')`). **Assert:** an allow entry whose path matches the file gives exit 2. |
| TS-TE011-02 | -001, -008 | **Point in time.** Migration A seeds `x.col` with a literal. Migration B marks (`x`, `col`) personal. **Assert:** no finding on A and one notice naming A's file and line. **Assert:** a test SQL fixture outside the migration folder that writes `x.col` with a literal gives a finding. |
| TS-TE011-03 | -001, -008 | **Source-field key.** A test SQL fixture `INSERT INTO public.customer (surname) VALUES ('<text>')`, with the test dictionary row `v_ace_customer.last_name` and source field `public.customer.surname`, gives PDPA-FIXTURE-FIELD for `last_name (surname)`. |

Additional unit-level scenarios (testing standards §3 "Engineering enabler: one test per business rule
and test case"; positive, negative, boundary, error):

| Area | Scenarios |
|---|---|
| Reader (-001), read forms | **R1** single-row INSERT by column name, with columns reordered. **R1** multi-row INSERT (3 rows, mixed `true`/`false`). Qualifiers `${recoverySchema}.`, `recovery.` and `"sys_fields"`. `is_personal` column omitted → `false`. `source_field` key kept. **R2** `UPDATE … WHERE field_id = '<id>'`. **R2** `UPDATE … WHERE field_id IN (…)`. `is_active = false` row still listed. API `x-personal-data` camel → snake with the schema object. |
| Reader (-001), ignored forms | `UPDATE sys_fields SET description = … WHERE object_name = …` leaves the list unchanged. `CREATE TABLE`, `CREATE INDEX`, `COMMENT ON`, `ALTER TABLE … ADD CONSTRAINT` and a view reading `sys_fields` are ignored. `sys_fields` inside a string literal, a `--` comment, a `/* */` comment or a dollar-quoted string is not a statement target. The PS v6 copy reads without exit 2 and yields 18 fields. |
| Reader (-001), fail closed, one scenario each, each exit 2 with file and line and no SQL text in the output | `UPDATE … SET is_personal = true WHERE object_name = '…'`. `UPDATE … SET is_personal = (SELECT …)`. `UPDATE … SET field_name = …`. `DELETE FROM sys_fields …`. `TRUNCATE sys_fields`. `COPY sys_fields FROM …` and `\copy`. `INSERT INTO sys_fields … SELECT …`. `INSERT … ON CONFLICT … DO UPDATE SET is_personal = …`. `MERGE INTO sys_fields`. `ALTER TABLE sys_fields ALTER COLUMN is_personal …`. `DROP TABLE sys_fields`. A `DO $$ … sys_fields … $$` block. An INSERT whose `is_personal` is a function call. An `UPDATE` naming an unknown `field_id`. A duplicate `field_id` INSERT in two migrations. |
| Reader (-001), order and notices | A migration row replaces a baseline row. A baseline row not replaced stays. A `true` → `false` change by replacement or by R2 is applied with one `PDPA-NOTICE` naming the field ID only, and the exit code is unchanged. Missing file → exit 2. Empty union → exit 2. |
| Generator (-002) | Variants for `id_no_last4` (digits), `extracted_fields`; entity names with suffixes; byte-identical output on two runs |
| Check digit (-009) | Valid and invalid check digit; dashed form; 12 and 14 digits; digit-adjacent match rejected |
| Mobile / e-mail (-009) | Every failing value assembled at run time (never stored): national 3-3-4 form, `+66` 2-3-4 separated form, bare `66` form; `example.com`, `sub.example.org`, `x.test` pass; an address in another domain, built at run time, fails |
| Self-scan (-003, -009) | A stored FIXTURE-ID match under `tools/pdpa-lint/**` fails the build; FIXTURE-FIELD is not applied there |
| Log rules (-004..-006) | Field name inside a string literal → no finding; concatenation, `String.format`, template literal → finding; non-logger method → no finding |
| TOSTRING (-007) | Record with explicit `toString()` excluding the field → no finding; class without personal member → no finding |
| Fixture field (-008) | `NULL`, empty string and `DEFAULT` → no finding. DATE literal → finding. JSON nested key. Builder call. **Object scoping:** `INSERT INTO listing (status)` with only `recovery_case.status` personal → no finding; `INSERT INTO recovery_case (status)` → finding; multi-row VALUES checked row by row; a literal in `INSERT … SELECT` at a personal column → finding. **Resolution:** a `CustomerEntity` setter → `v_ace_customer`; `@Table(name = …)`; a schema.d.ts type; a `fixtureObjects` glob for JSON. **Unresolved:** an unambiguous name (`lastName`) → finding; an ambiguous name (`status`) → notice and no finding. SQL in a Java string → no FIXTURE-FIELD. |
| Allow list (-011) | Missing `owner`, `reason` or `expires` → exit 2. Both `line` and `pattern` → exit 2. `line` match. `pattern` match. Unused expired entry → exit 0. A `path` glob matching a file in the migration folder (exact path, and a broad `**/*.sql`) → exit 2. |
| Output (-012) | Sort order. Exit codes. A parse error prints no source text. Notices follow the findings, carry no value and leave the exit code unchanged. |

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
| DL v10 D-RCV-29 | Later dictionary changes are reference loads through RWB-E1-043 | SPEC-TE011-001, -017 | DIRECT | The lint states the limit: reference-load marks are not visible (files only, story §13/§17); the guard on load is a seam owned by RWB-E1-043 (D-RUN-08); DGL-13 | COVERED |

## Out of scope

- Secret scanning and dependency approval in the pipeline (NFR-052, NFR-054): ACE pipeline (SRC-01 §19).
- Masking rules by role at run time: RWB-E1-037 (SRC-01 §19).
- Masked data in SIT and UAT: RWB-TE-004 (SRC-01 §19).
- Which fields are personal and how long they are kept: DL26, Compliance (SRC-01 §19; SRC-22).
- A-07: raw exception text in `ApiExceptionHandler` and correlation-ID propagation (see "Scope decisions").
- A-09: contract, dependency scan, ZAP, Playwright/axe and coverage-verification jobs (see "Scope decisions").
- Publishing the masking helper: common module (OPEN-024).
- Writing the CODEOWNERS file and branch rule: RWB-TE-002.
- Guarding `is_personal` changes made by D-RCV-29 reference loads, and any dictionary load handler: RWB-E1-043 and RWB-E1-001 (seam, SPEC-TE011-017; DGL-13).
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
| CLAR-004 | BR3 | `SYN-` cannot apply to DATE and NUMBER personal fields | Fixtures for `date_of_birth`, GPS fields | Strict: any literal is a finding unless allow-listed (DGL-08) | RESOLVED (ASM) | SPEC-TE011-008 |
| CLAR-005 | SRC-04 step 2 | Entity class names in flow vs §13 RuleGenerator | AC2 | Generate them; suffixes `Entity`, `View` (ASM-TE011-04) | RESOLVED (story flow + AC2) | SPEC-TE011-002, -005 |
| CLAR-006 | SRC-04 step 4 | AC3 value generated at run time vs literal scan | AC3 | Test writes the generated value to a temp file the lint scans | RESOLVED (story §17) | SPEC-TE011-009 |
| CLAR-007 | §10, X11 | Code owners come from RWB-TE-002, which is not built; host unconfirmed | TC-TE-011-11 | Add entry to section `[Recovery module]` of `.gitlab/CODEOWNERS` (SRC-23); TC-11 `BLOCKED` locally (OPEN-038) | RESOLVED (ASM) | SPEC-TE011-014 |
| CLAR-008 | AC1 vs AC7 | Output names `first_name` (AC1) but `lastName` (AC7) | Output format | Dictionary name plus matched token in parentheses (ASM-TE011-14) | RESOLVED (ASM) | SPEC-TE011-012 |
| CLAR-009 | BR3, §13 RuleGenerator; DGL-14 (review DG4-02) | The same field name is personal on one object and not on another; name-only fixture matching flags dictionary and reference seeds | FIXTURE-FIELD positions; RWB-E1-001 merge | Orchestrator triage 2026-11-18: match SQL and fixtures by (object, field), never by name alone; no allow entry for a migration. Unresolved objects: unambiguous names only, ambiguous names reported as notices (ASM-TE011-20) | RESOLVED (orchestrator triage; `sys_fields.object_name`) | SPEC-TE011-001, -002, -008, -011, -016 |
| CLAR-010 | BR1; DL v10 D-RCV-29; DGL-13 (review DG4-01) | Later dictionary changes are reference loads, which a files-only lint cannot see | Production coverage claim | Precedence: Decision Log v10 over story files v7 for the route. The lint stays files-only (story §13/§17). Claim narrowed to the dictionary as seeded and changed by migrations; the guard on load is a seam owned by RWB-E1-043 (D-RUN-08; orchestrator triage 2026-11-18) | RESOLVED (precedence + D-RUN-08) | SPEC-TE011-001, -016, -017 |

`CLARIFICATION_STATUS: RESOLVED [OPEN_ITEMS: 0]` — every item is settled by story text, precedence or a
labelled assumption; the assumptions and the proposed open items are carried to the plan gate.

## Status reporting

```text
MCP_STATUS_SUMMARY: No Jira, Confluence, GitLab or Figma MCP is connected (RUN-BRIEF rule 5); the story file was read from the document set.
MCP_API_RESULT: NOT_APPLICABLE [API: n/a] [HTTP: n/a] [ERROR: n/a] [RETRY_AFTER: n/a] [NODE_TYPE: n/a] [CHILD_COUNT: n/a]
CHANGE_CLASSIFICATION_SUMMARY: New build-time PDPA lint in tools/pdpa-lint plus a CI job; no UI, no API, no application code change.
CHANGE_CLASSIFICATION_RESULT: NEW_STORY [UI_IN_SCOPE: NO] [LOGIC_IN_SCOPE: YES] [API_IN_SCOPE: NO] [API_IMPACT: NO_API_CHANGE] [REASON: build tooling only; no prior trace chain]
REQUIREMENT_COVERAGE_SUMMARY: All 7 flow steps, 7 business rules, 11 exception paths, 10 ACs, §11 data, contract items, guardrails and 5 upstream requirements map to SPEC-TE011-001..017, plus Decision Log v10 D-RCV-29.
REQUIREMENT_COVERAGE_RESULT: SUCCESS [TOTAL_RULES: 31] [COVERED_RULES: 31] [MISSING_RULES: 0] [AMBIGUOUS_RULES: 0] [CONTRADICTIONS: 0]
DESIGN_EVIDENCE_STATUS: NOT_REQUIRED [SOURCE: NONE] [SCREENS: 0] [UNBLOCK_ACTION: n/a]
CLARIFICATION_STATUS: RESOLVED [OPEN_ITEMS: 0]
```

Contradictions between sources are recorded in `document-gaps.md` (DGL-01..DGL-14); each is settled by
precedence or a labelled assumption, so none is left open in the coverage table.

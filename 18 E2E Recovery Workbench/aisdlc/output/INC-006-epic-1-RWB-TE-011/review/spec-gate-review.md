# Spec gate review: RWB-TE-011 PDPA lint for code, tests and logs

| Field | Value |
|---|---|
| RUN_ID | `INC-006-epic-1-RWB-TE-011` |
| Gate | Spec gate (Compliance Reviewer, independent of the author) |
| Reviewed | `specify/spec.md` (SPEC-TE011-001..016), `compliance-validation.md`, `assumptions.md`, `document-gaps.md`, `shared-updates.md`, `contracts/backend-apis.json`, `contracts/frontend-integrations.json`, `figma/figma_report.md` |
| Reviewed against | Increment card INC-006; RWB-TE-011 story file v1 (Epic 1 Story Files v7, 28 Oct 2026); Technical Enabler Stories v7 §RWB-TE-011; Build Notes Technical Enablers v2; Story Defects v4; Test Cases v7 TC-TE-011-01..11; Physical Schema v6 `sys_fields` seed; API Specification v4; Personal Data Protection Design v2; Data Classification and Personal Data Inventory v4; Logical Data Model and Data Dictionary v8; Audit and Logging Design v2; NFR Specification v3; Controls Catalog v3; Business Requirements Program v4; D-RCV-35; decision register; Phase 0 standards audit (A-07, A-09, A-10); `aisdlc/.github/contexts/*`; `aisdlc/.github/rules/specification-execution-gates.md`, `pdlc.md`, `traceability-standards.md`; RWB-TE-002 spec (`output/INC-004-epic-1-RWB-TE-002/specify/spec.md`); repository code (`.gitlab-ci.yml`, `ApiExceptionHandler.java`, `frontend/`, `infra/`) |
| Date | 2026-11-17 |
| Reviewer | Compliance Reviewer (agent) |

## 1. Result

**Overall status: FAIL**

| Severity | Count |
|---|---|
| Critical | 0 |
| High | 0 |
| Medium | 2 |
| Low | 5 |

The two Medium findings block the handoff to the Implementation Planner until they are fixed and this
gate is run again (`spec-gate-review-2.md`), or until a person records that they accept them
(`pdlc.md`, "Human Checkpoints").

## 2. Answers to the points the orchestrator asked about

| Point | Verdict | Basis |
|---|---|---|
| Every statement traced to a cited source (name and version) or a labelled assumption | **Mostly yes.** 22 sources are listed with document name, version and path. 19 assumptions are labelled. I checked the key factual claims against the sources and the repository, and they hold: 18 `is_personal = true` rows in the Physical Schema v6 seed; 5 `x-personal-data: true` properties in API Specification v4; LDM v8 marks 9 fields; Inventory v4 marks 523 "Yes"; the repository copies of the schema and the API are byte-identical to the document set; `.gitlab-ci.yml` has 3 jobs; there is no `tools/` folder and no `X-Correlation-Id` in the document set; the `ApiExceptionHandler` log calls are on lines 35 and 52. **Exceptions:** one behaviour is not traced (REVIEW-TE011-SG-03), one citation goes beyond the cited decision (REVIEW-TE011-SG-05), and one repository path conflicts with the current RWB-TE-002 spec (REVIEW-TE011-SG-02). | Section 3 |
| Has the spec invented any requirement? | **No material invention.** The six rules, the trigger, the output text, the allow-list fields, the configuration items and the "done when" criterion are all in story file v1 §4, §8, §12–§14 and §17. The detail added (patterns, exit codes, scan roots, the time zone, the entity-name suffixes) is labelled ASM-TE011-01..19 and kept in configuration. The one unlabelled behaviour, "rows with `is_active = false` are ignored", is REVIEW-TE011-SG-03 (Low). | SPEC-TE011-001..016; `assumptions.md` |
| A-07 out of scope, A-09 (PDPA part) in scope | **Sound.** A-09 (PDPA part): the story file v1 §4 step 7 and §13 build step 6 ("Add PdpaLintStep to the pull request pipeline") and testing standards §1 ("PDPA lint … Pass on every MR") require the job; SPEC-TE011-013 specifies it. A-07: the story is a static check that reads files (§12 Input, §13 "Database. None", "Feature flag. None. A build check has no runtime path"). No AC, BR or flow step changes runtime logging or correlation IDs. A rule for "a `Throwable` passed to a log call" is not one of the six rules in §12, so adding it would be an invented requirement. The audit's Owner column assigns A-07 to RWB-TE-011, though, and the hand-off of the deferred item to an owner is not complete (REVIEW-TE011-SG-07, Low). | `phase0-standards-audit.md` rows A-07 and A-09; `ApiExceptionHandler.java` lines 35 and 52 |
| Classification source correct, version cited | **The source is correct and its version is cited; the record of the conflict and the residual risk is incomplete.** Using the `sys_fields.is_personal` seed (Physical Schema v6) together with `x-personal-data` (API Specification v4) follows story file v1 §3 and §12 and Technical Enabler Stories v7 BR1/§12. This is the story's contract, and classification is DL26 (Compliance) and out of scope (§19). However, Personal Data Protection Design v2 §1 names the Inventory workbook as "the field-level inventory", and backend context §6 says "field-level classification in the Personal Data Inventory v4". Neither designation is recorded. The list of Restricted fields that the production lint will not cover is understated (REVIEW-TE011-SG-01, Medium). | Section 3 |
| Personal data in the artefacts | **None found.** No real names, national IDs, account or contract numbers, mobile numbers, addresses or personal e-mail addresses appear in any reviewed file. The only handle is the team handle `@scb-ace/techx-recovery-tech-leads` (L-RCV-12). The values are synthetic (`SYN-LAST-0001`, `TESTNAME` from AC4). Values that would match a FIXTURE-ID pattern are specified as generated at run time. No secrets. (Observation, not a finding: the increment card, a shared file outside this review's scope, names staff approvers. That is governance metadata, not data subjects.) | grep of the `specify/` folder for e-mail, digit-run, phone and name patterns |

## 3. Findings

### REVIEW-TE011-SG-01: Classification conflict and residual coverage risk are understated (Medium)

- **Affects:** "Personal data classification used", "Entry trigger and preconditions" (precondition 2),
  SPEC-TE011-001, SPEC-TE011-016, Requirement-to-SPEC Logic Coverage (no row for story §11), DGL-01,
  OPEN-NEW-TE011-1, CTL-11, REQ-RDF-010, BS-4.6.
- **Evidence:**
  1. Personal Data Protection Design v2 §1 (document table reads "Version 1") ends its category table
     by naming the Inventory as the authoritative list: "The field-level inventory is the data
     classification and personal data inventory workbook". Backend context v2.0 §6 says "field-level classification in the
     Personal Data Inventory v4". Project context, row "PDPA", cites Personal Data Inventory v4. The
     spec cites PDPA Design v2 §1 and backend context §6 as sources (SRC-08, SRC-20), but DGL-01 records
     neither designation, and does not record the precedence reasoning that sets them aside.
  2. Inventory v4 classes 17 fields as **Restricted**. Nine of them are **not** `is_personal = true`
     in the Physical Schema v6 seed, so the production lint will not flag them:
     DF-ACE-003 `v_ace_account.account_name` (direct identifier), DF-ACE-041
     `v_ace_account.special_memo` (direct identifier), DF-ACE-053 `v_ace_payment.comments` (direct
     identifier), DF-ACE-116 `v_ace_efs_action.comments` (direct identifier), DF-ACE-060
     `deceased_date`, DF-ACE-061 `deceased_flag`, DF-EXT-002 `vulnerable`, DF-EXT-003
     `deceased_override`, DF-EXT-004 `bankruptcy` (sensitive). The spec's "Consequence" paragraph
     (spec.md lines 152–155) and DGL-01 name only `cif_no`, `contract_no`, `case_no` and three of the
     sensitive flags. They omit the four Restricted direct identifiers (a party or account name and
     three free-text fields) and two of the five sensitive fields.
  3. Story file v1 §11 "Data" lists as fields the lint reads "(definition)": DF-ACE-055 `cif_no`,
     DF-EXT-002 `vulnerable`, DF-ACE-061 `deceased_flag` and DF-EXT-004 `bankruptcy`. None of these is
     in the production list. §11 has no row in Requirement-to-SPEC Logic Coverage, and DGL-01 does not
     cite §11.
  4. "Entry trigger and preconditions" marks precondition 2 ("the data dictionary marks each personal
     field") as **Met**. Against Inventory v4 and PDPA Design v2 §1 it is only partly met.
- **Why it matters:** the decision to follow the seed is correct, because it is the story contract and
  does not invent a requirement. But the gate output is what Compliance (RW-COMPLY, DL26) will act on.
  An incomplete list of Restricted fields, and a "Met" precondition, give false assurance. A green lint
  ("zero findings on main", SPEC-TE011-016) would not show that names in `account_name` or free text
  in `comments` can still reach logs and fixtures (CTL-11; Audit and Logging Design v2 §6;
  BS-4.6).
- **Required fix (spec, `document-gaps.md`, `shared-updates.md`; no change to the classification
  source):**
  1. DGL-01: add PDPA Design v2 §1 (Inventory named as the field-level inventory) and backend context
     §6 as conflicting sources. State the precedence used: story files v7 (§12; Technical Enabler
     Stories v7 BR1/§12) over context summaries and design documents outside the RUN-BRIEF chain, with
     DL26 as the owner of the decision.
  2. Replace the "Consequence" paragraph with the full list of Inventory v4 Restricted fields that the
     seed does not mark (the nine above). Also say that the 523 "Yes" fields minus the 18 seed fields
     are not covered. Copy the explicit list into OPEN-NEW-TE011-1.
  3. Set precondition 2 to "Partly met (DGL-01)".
  4. Add a Requirement-to-SPEC row for story §11 Data. Map it to SPEC-TE011-001 and -016, and say
     that four §11 fields are covered only once Compliance marks them, because the test dictionary
     marks them for the ACs.
  5. In SPEC-TE011-016, state that "zero findings" is measured against the dictionary as it is, and
     that it does not cover the fields listed in point 2 until OPEN-NEW-TE011-1 closes.

### REVIEW-TE011-SG-02: Code-owner file path and format conflict with the RWB-TE-002 spec (Medium)

- **Affects:** Change Scope Declaration "Impacted Existing Nodes"; SPEC-TE011-014; X11; TC-TE-011-11;
  story §10 (authority control); OPEN-NEW-TE011-5; DGL-12.
- **Evidence:** spec.md line 65 names "`.github/CODEOWNERS` created by RWB-TE-002" as an impacted
  node. The current RWB-TE-002 spec (`output/INC-004-epic-1-RWB-TE-002/specify/spec.md`, 17 Nov 2026,
  matrix row 004 "Planned") delivers `.gitlab/CODEOWNERS` in GitLab section format (SPEC-RWB-TE-002-001).
  That spec also delivers an owner register `.gitlab/codeowners-register.yaml` as "the only local
  source of valid owners" (SPEC-RWB-TE-002-009), and a validator with rules V1–V11 (V4 anchored, no
  wildcard; V7 owner must be in the register; V9 every non-reserved pattern must match a file). L-RCV-12 provides
  for the `.gitlab/` equivalent. SPEC-TE011-014 does not say which section the `/tools/pdpa-lint/`
  entry goes in, or that it must pass the TE-002 validator.
- **Why it matters:** a planner who follows the spec would add the entry to a `.github/CODEOWNERS` file
  that TE-002 does not create and that a GitLab host does not read. The tech-lead approval on
  allow-list and rule changes (story §10, X11, BR6 change control) would then have no effect, and
  TC-TE-011-11 could never pass.
- **Required fix:** in the scope declaration, SPEC-TE011-014, DGL-12 and OPEN-NEW-TE011-5, name the
  code-owner file that RWB-TE-002 delivers (`.gitlab/CODEOWNERS` per SPEC-RWB-TE-002-001 and L-RCV-12,
  or "the file RWB-TE-002 delivers" with that reference). Name the section for the
  `/tools/pdpa-lint/` entry. State that the owner must be in `.gitlab/codeowners-register.yaml`, and
  that the entry must pass the TE-002 validator: anchored with no wildcard (V4), and matching a file
  (V9), so the entry lands in the same merge as `tools/pdpa-lint/` or after it.

### REVIEW-TE011-SG-03: Unlabelled behaviour, inactive dictionary rows ignored (Low)

- **Affects:** SPEC-TE011-001.
- **Evidence:** spec.md line 166: "Rows with `is_active = false` are ignored." No source and no
  `ASM-TE011-nn` supports it. The story says nothing on `is_active`. The Physical Schema v6 seed INSERTs
  do not set the column (it defaults to `true`). The specification gates' "No-Assumption Policy"
  requires every inferred behaviour to be evidenced or recorded.
- **Why it matters:** the inference weakens coverage. A field can be deactivated in the dictionary
  while code, fixtures or logs still use it.
- **Required fix:** remove the rule, so that inactive personal fields stay in the list (fail-safe).
  Or keep it, label it as a new assumption with its rationale and risk, and list it for confirmation by
  RW-COMPLY.

### REVIEW-TE011-SG-04: Scan exclusions leave the lint's own guardrail and some repo-authored files unenforced (Low)

- **Affects:** SPEC-TE011-003, SPEC-TE011-009, Test requirements (row "Mobile / e-mail"), ASM-TE011-05,
  story §17 guardrail 2.
- **Evidence:**
  1. `tools/pdpa-lint/**` is excluded from every rule (spec.md line 201). Story §17 requires that the
     lint's "own check digit fixtures are generated at run time and never stored". With the exclusion,
     nothing enforces this. The e-mail negative case ("other domain fails", spec.md line 510) is not
     specified as built at run time, but the mobile case is.
  2. The `infra/**` exclusion is justified as "verbatim copies of the read-only document set and local
     mock identities". That is true for `infra/postgres/schema/`. But `infra/postgres/init/` and
     `infra/mock-oidc/config.json` are repo-authored, and the init folder is the natural place for
     future SQL seed files (story §4 step 4 "SQL seed files").
- **Required fix:** keep PDPA-FIXTURE-ID active on `tools/pdpa-lint/**`, or add a self-scan test over
  the tool's test tree. State that every failing ID, mobile and e-mail value in the tool's tests is
  built at run time. Narrow the default exclusion to `infra/postgres/schema/**`, or record evidence
  for the wider exclusion in ASM-TE011-05.

### REVIEW-TE011-SG-05: D-RCV-16 cited beyond its scope (Low)

- **Affects:** Preflight evidence, SPEC-TE011-016 heading, DGL-02.
- **Evidence:** the decision register defines D-RCV-16 as acceptance "for RWB-E1-044 and RWB-TE-001,
  whose acceptance criteria BA removed on 4 Nov 2026". The spec cites it as a general rule for
  RWB-TE-011. `AGENTS.md` §6 generalises it ("A story with no business ACs is accepted on its business
  rules and test cases (D-RCV-16)").
- **Required fix:** cite `AGENTS.md` §6 as the general rule, with D-RCV-16 as its origin, or say that
  D-RCV-16 is applied by analogy.

### REVIEW-TE011-SG-06: Thai mobile pattern grouping does not fit the international form (Low)

- **Affects:** SPEC-TE011-009, ASM-TE011-09.
- **Evidence:** spec.md line 285 allows separators "between the 3-3-4 groups". With the `+66` or `66`
  prefix, the national number is 9 digits, grouped 1-3-4 or 2-3-4 after the country code, not 3-3-4.
  A separated international number could therefore be missed. Bare `66` + 9 digits also widens the
  false-positive surface.
- **Required fix:** define the separator grouping for each prefix form (`0` + 9 digits; `+66`/`66` +
  9 digits). Add a unit scenario for a separated `+66` value built at run time. Record the false-positive
  trade-off of the bare `66` prefix in ASM-TE011-09 (it stays configuration).

### REVIEW-TE011-SG-07: A-07 deferral is sound but its hand-off has no owner (Low)

- **Affects:** "Scope decisions on the orchestrator notes", OPEN-NEW-TE011-2, OPEN-NEW-TE011-3.
- **Evidence:** the Phase 0 audit row A-07 names RWB-TE-011 as the owner. The spec places A-07 out of
  scope, with valid reasons (see section 2). The proposed open items say "Assign an owning story or an
  `AISDLC-HARDENING` change" and "Blocks: Nothing". `ApiExceptionHandler` line 52 logs the whole
  exception, and line 35 logs the cause. Exception text from the persistence layer can carry column
  values, which Audit and Logging Design v2 §6 and BS-4.6 forbid in application logs. Audit row A-08
  already gives RWB-TE-003 (INC-005) changes to the same `ApiExceptionHandler` class.
- **Required fix:** in `shared-updates.md`, ask the orchestrator to change the A-07 owner in the audit
  (or record the reassignment in the run's README). Name a candidate owner, for example RWB-TE-003,
  which already changes `ApiExceptionHandler` under A-08, or an `AISDLC-HARDENING` change. Mark
  OPEN-NEW-TE011-2 as a release-readiness item, not "Blocks: Nothing".

## 4. Checks that passed

| Check (compliance-reviewer "Required Checks"; spec gate checklist) | Result |
|---|---|
| Change Scope Declaration present and consistent with the footprint | Pass: `NEW_STORY`; UI NO; API `NO_API_CHANGE`; backend YES (build tooling only); frontend NO |
| Required spec sections (intent, trigger and preconditions, field matrix, status matrix, exceptions, API assessment, Unit Test Applicability, Requirement-to-SPEC) | Pass |
| Unit Test Applicability | Pass: frontend `NOT_APPLICABLE` with evidence (no file under `frontend/` changes; front-end source is scan input only); backend `REQUIRED`, 80% JaCoCo LINE/BRANCH/METHOD/INSTRUCTION on `tools/pdpa-lint`, positive/negative/boundary/error scenarios listed, reference to `implementation-execution-gates.md`; no invented measured results |
| Authentication and authorization | Not applicable at run time (story §10). Change control by code owners is specified, but the path is wrong (SG-02) |
| Customer and account data protection | Specified as a blocking pipeline job (BR2–BR5, BR7); coverage caveat SG-01 |
| Audit logging for sensitive financial actions | Not applicable: no case, decision or financial action (story §9) |
| KYC, AML, suitability, consent | Not in scope |
| Frontend integration versioning and error contract | Not applicable; `contracts/frontend-integrations.json` `NOT_APPLICABLE` with reason |
| API contract | `contracts/backend-apis.json` parses; `NO_API_CHANGE`; file and CLI contract consistent with SPEC-TE011-002, -011, -012, -013 |
| Secrets and environment configuration | None in the artefacts; no runtime configuration change |
| The lint never prints values (BR7) | Specified in SPEC-TE011-012 and asserted in every TC |
| Allow list time-boxed and owned (BR6) | Specified; an invalid entry fails closed (exit 2) |
| Fail closed on missing or empty dictionary | Specified (ASM-TE011-03) |
| Design evidence | `NOT_REQUIRED`, with reason (story §15) |
| Document gaps recorded with two citations, none blocking | Pass. DGL-01..12 checked; the precedence application is correct for DGL-02, -03, -04, -05, -11, -12 |
| Traceability | Matrix row 006 proposed in `shared-updates.md` (shared file not edited, as RUN-BRIEF rule 3 requires); SPEC IDs unique; TC-TE-011-11 honestly `BLOCKED` until RWB-TE-002 and OPEN-038 |
| TC-TE-011-01..10 mapped to ACs and BRs; synthetic data only | Pass |

## 5. Gate output

```text
REVIEW_STATUS: FAIL
REVIEW_COUNTS: [CRITICAL: 0] [HIGH: 0] [MEDIUM: 2] [LOW: 5]
BLOCKING: YES (REVIEW-TE011-SG-01, REVIEW-TE011-SG-02)
NEXT_STEP: Technical Specifier fixes SG-01 and SG-02 (and the Low findings or records them as accepted); Compliance Reviewer reruns the spec gate as review/spec-gate-review-2.md before the Implementation Planner starts.
```

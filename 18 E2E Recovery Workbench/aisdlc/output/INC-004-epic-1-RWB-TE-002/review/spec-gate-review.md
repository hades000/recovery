# Spec gate review: RWB-TE-002 Code owners for the recovery module

| Field | Value |
|---|---|
| Review ID | `REVIEW-RWB-TE-002-SG-2026111701` |
| RUN_ID | `INC-004-epic-1-RWB-TE-002` |
| Gate | Specification gate, fresh review under D-RUN-05 (`AI-SDLC-BUILD-LOG.md:28`) |
| Artefacts reviewed | `_v2-baseline/specify/spec.md`, `_v2-baseline/specify/compliance-validation.md`, `_v2-baseline/specify/assumptions.md` (written in the 17 v2 workspace for the real ACE monorepo) |
| Baseline | Increment card `aisdlc/docs/increments/INC-004-epic-1-RWB-TE-002.md`; Story Files v7 `rwb-te-002-code-owners-for-the-recovery-module-v1.md`; Architecture Decision Records v3; Decision Log v10; D-RCV-35/36; `aisdlc/docs/open-items.md` OPEN-038, OPEN-041 |
| Implementability baseline | `<repo>/AGENTS.md` §5, §8; `aisdlc/evidence/phase0-standards-audit.md` A-05, A-10; this repository at `c22ee73` |
| Reviewer | Compliance Reviewer (agent run) |
| Date | 2026-11-17 |

## Status

**`FAIL`**

| Severity | Count | IDs |
|---|---|---|
| Critical | 0 | none |
| High | 2 | SG-001, SG-002 |
| Medium | 6 | SG-003 to SG-008 |
| Low | 3 | SG-009 to SG-011 |

The High and Medium findings block the handoff to the Implementation Planner until a human records a
fix and this gate runs again, or explicitly accepts the finding (`aisdlc/.github/rules/pdlc.md`, Human
Checkpoints). The v2 gate result `REVIEW-RWB-TE-002-SPEC-001` (`PASS`, 5 Low) applied to the real ACE
monorepo. It does not carry over to this repository.

### What is right in the spec

- It covers story v7 completely. BR1–BR7, AC1–AC7, X1–X7, flow steps 1–7, §12 contract, §17 guardrails
  and §19 out of scope each have a row in the coverage table (`spec.md:47-67`).
- It replaces the story's placeholder `ace-service/...` and `ace-web/...` paths with paths that exist
  here (`spec.md:165-178`): D-RCV-37 for the module map, D-RCV-10 for the front end, and RUN-BRIEF
  "Local stack facts" for the migration folder. The recovery main, test, migration and front-end
  folders exist in this repository (`git ls-files`).
- It resolves BR4 against story §10 (`ASM-TE002-07`, L-RCV-13, OPEN-041) and the `main`-only branch
  rule against D-RCV-50 (`ASM-TE002-04`, L-RCV-13). Both rulings follow the decision register.
- **Owners.** The spec names no person. The two team handles come from story v7 §3, where the story
  itself marks them as assumed until DL37 and DL36 are answered. The spec calls them "values pending
  DL37/DL36" (`ASM-TE002-03`), and OPEN-038 records them for confirmation. D-RCV-21 names a person,
  but the spec only uses D-RCV-21 as the basis for team membership and does not copy the name. This
  check passes. SG-005 and SG-009 add the rule for any new owner entry.
- No personal data, no credential and no production data. The token is held by the host and never
  printed (`spec.md:217-219`, `spec.md:230-232`).
- The change classification is correct: `NEW_STORY`, UI NO, API NO, `NO_API_CHANGE`.

## Findings

### REVIEW-RWB-TE-002-SG-001: no local implementation boundary for the host-only controls

| Field | Value |
|---|---|
| Severity | **High** |
| Affects | AC1 (second clause), AC3, AC5, AC6; X1, X3, X4, X5, X7; BR6; TC-TE-002-01, -03, -05, -06, -08; flow steps 3, 5 and 7 |
| Evidence | `spec.md:147-148` says the system tests "are executed in the ACE repository with test pull requests". `spec.md:191-204` sets branch rules on `main`, `develop-recovery` and `develop`. `spec.md:267-268` says the test PRs run "in a test branch protected by the same rules". In this repository: `git branch -a` shows only `develop-recovery`, so `main` and `develop` do not exist. No GitLab, GitHub or MR host is connected (RUN-BRIEF hard rule 5). `.gitlab-ci.yml:1-2` says that in ACE the same gates run "in the ACE pipeline". The rule in `pdlc.md` (line 31) is that acceptance checks outside automation "must remain visible as human-verification gaps, not fabricated QA results". AGENTS.md §8 requires a "named reviewer" on every merge. |
| Problem | Requesting reviewers, counting approvals, ignoring an author's own approval, dismissing stale approvals and blocking a merge are all done by the repository host. None of them can run or be tested here. The spec does not say which parts it builds and tests in this repository, which parts it only documents as host configuration, or which acceptance criteria stay as human-verification gaps until the ACE host exists. Without that split the planner can only invent test PRs, or mark the criteria as passed. |
| Required fix | Add a section, "Local implementation boundary (D-RUN-05)", that does three things. (1) **Built and tested here:** the code owners file; a validation step that runs as a `.gitlab-ci.yml` job and from `scripts/dev.ps1 test`; and an ownership resolver that computes the required owners for a set of changed paths using the last-match rule. That resolver covers AC1 first clause, AC2, AC3 (both teams required), AC4 and BR5 as automated tests. (2) **Documented as host configuration only:** the protected-branch and approval settings (code-owner approval required, 1 approval, author approval ignored, approvals removed on a new commit), recorded as a settings file that the ACE administrator applies. (3) **`NOT_APPLICABLE` here, carried as human-verification gaps** with a named document-set role (ACE team repository administrator) and OPEN-038 as the unblock: AC1 second clause, AC3 merge-blocked clause, AC5, AC6, X1, X4, X5, X7, TC-TE-002-08. Update the coverage table and the Unit Test Applicability table to match. Do not claim these criteria as COVERED by local evidence. |

### REVIEW-RWB-TE-002-SG-002: the common-module pattern matches no file, so the spec's own check fails and AC2/AC3 cannot run

| Field | Value |
|---|---|
| Severity | **High** |
| Affects | BR3, AC2, AC3, X2, X3, TC-TE-002-02, -03; validation rule 4 (`spec.md:214`); contract §12 "every pattern matches at least one file" |
| Evidence | `spec.md:167` sets `/backend/src/main/java/th/co/scb/ace/demo/common/ @scb-ace/ace-team`. `git ls-files` in this repository shows no `th/co/scb/ace/demo/common` path: the only packages are `recovery/**`, plus `e2e` in tests. `spec.md:214` fails the job "when no file matches". Story Files v7, RWB-TE-001 (DL05 note), says the common published packages are "assumed; DL05" until the ACE team names them. Decision Log v10 DL05 applies option B, under which the ACE team applies the common boundaries later. AGENTS.md §3.1 allows the common module to change only "where the story file names it". The TE-001 v2 spec SPEC-RWB-TE-001-006 uses `allowEmptyShould(true)` because the common module can stay empty. `spec.md:186-188` already uses the no-match argument to leave out the common test folder, but does not apply it to the common main folder. |
| Problem | Built as written, the first pipeline run fails on the spec's own BR3 entry. AC2 and AC3 need a file under the common module, and none exists here. Creating one would change the common module, which story v7 does not authorise. |
| Required fix | Choose and state one disposition, and record it as an assumption. Option (a): the validation step accepts a pattern only when it is listed in a reviewed "declared external module" list taken from the module map `external[]` (`common`, `collection`). It warns rather than fails on an empty match for those patterns, and still fails on an empty match for every other pattern. Option (b): leave the common entry out until the ACE team names the package, and record the gap. With either option, AC2 and AC3 are tested here through the ownership resolver (SG-001), using a synthetic changed-path list. No file is created under `common/`. Record the dependency on DL05 and OPEN-038. |

### REVIEW-RWB-TE-002-SG-003: the host format is GitHub; this repository stands in for GitLab

| Field | Value |
|---|---|
| Severity | Medium |
| Affects | Components (`spec.md:156-159`), the BR4 entry (`spec.md:177`), branch-rule vocabulary (`spec.md:191-200`), validation step 3 (`spec.md:212-213`), `ASM-TE002-01`, CLAR-001 |
| Evidence | `ASM-TE002-01` (`spec.md:20`) and CLAR-001 (`spec.md:290`) choose `.github/CODEOWNERS` and GitHub branch protection. This repository has no `.github/` folder and does have `.gitlab-ci.yml`. D-RCV-50 and `project-context.md:209-210` speak of "MR into `develop-recovery`". L-RCV-12 (`decision-register.md:112`) says that on a GitLab host "the equivalent `.gitlab/CODEOWNERS` and protected-branch approval rules are used". The task statement for this run says the repository stands in for a GitLab project. |
| Problem | The spec marks CLAR-001 RESOLVED in favour of the wrong host for this repository. The file path, the BR4 self-ownership entry, the GitLab code-owner section syntax and the names of the approval settings all change. |
| Required fix | Apply L-RCV-12 for this repository. Use `.gitlab/CODEOWNERS` with GitLab syntax, and make the BR4 entry `/.gitlab/CODEOWNERS` owned by both teams. Express the branch rules as GitLab protected-branch and MR-approval settings. Keep `ASM-TE002-01` only for the real ACE host (OPEN-038). Mark CLAR-001 as resolved for this repository and still open for ACE. |

### REVIEW-RWB-TE-002-SG-004: owner existence and write access depend on a host API and token that do not exist here

| Field | Value |
|---|---|
| Severity | Medium |
| Affects | AC7, X6, TC-TE-002-07; story v7 §12 pipeline step ("every owner exists and has write access"); `ASM-TE002-06`; CLAR-007 |
| Evidence | `spec.md:157` and `spec.md:212-213` resolve every `@org/team` through the host. `spec.md:217-219` uses "the repository token or a service token". `ASM-TE002-06` (`spec.md:25`) assumes the token can read team membership. RUN-BRIEF hard rule 5 says no GitLab MCP or connection is available. |
| Problem | In this repository the only testable acceptance criterion that is fully automatable, AC7, depends on an API that is absent. As written, the step either always fails closed here (`spec.md:219`) or has to be faked. |
| Required fix | Define the local owner source as a reviewed owner register in the repository. It lists each allowed handle, the document-set role it stands for, and its status (`ASSUMED, pending DL36/DL37/OPEN-038`). It holds no person and no membership. Locally, the validation step checks each owner against this register, so AC7 fails on `@scb-ace/recovery-leads-typo`. Keep the host check (exists and has write access) as an ACE-only extension that fails closed when its token is absent, and mark it `NOT_APPLICABLE` here under SG-001. |

### REVIEW-RWB-TE-002-SG-005: audit item A-05 is neither covered nor excluded

| Field | Value |
|---|---|
| Severity | Medium |
| Affects | Change scope (`spec.md:29-43`), Out of scope (`spec.md:279-284`) |
| Evidence | `phase0-standards-audit.md:18` (A-05, High, Owner RWB-TE-002) says the AGENTS.md §5 context paths do not resolve from the repository root, and that there is no package-level AGENTS.md and no coding-standard file. `AGENTS.md:88-106` lists `.github/contexts/...` paths. Those paths exist only under `aisdlc/.github/contexts/`. RUN-BRIEF "Paths" maps the coding standard to `aisdlc/.github/contexts/backend-standards.md` and `frontend-standards.md`. Engineering Practices v5 §10 and AI Assisted Development Approach v1 (standards file paragraph) make AGENTS.md owned by "Solution architect with the tech leads" and say it changes "by pull request like code". `spec.md` does not mention AGENTS.md §5, the context paths, a package AGENTS.md or the coding standard. |
| Problem | The audit assigns A-05 to this story. Under RUN-BRIEF ("which gaps your story owns") the spec has to cover it or exclude it explicitly. It does neither. |
| Required fix | Add a row for A-05 to the coverage table. Recommended disposition: (1) **Cover:** correct the AGENTS.md §5 paths to `aisdlc/.github/contexts/...`, and name `backend-standards.md` / `frontend-standards.md` as the coding standard, citing the RUN-BRIEF mapping. Add an entry in the code owners file for `AGENTS.md` (and `CLAUDE.md`, `.claude/`, `aisdlc/.github/`), owned by a placeholder for the document-set role "Solution architect with the tech leads". Mark the handle `ASSUMED` and raise an open item, because no handle exists in the document set and none may be invented. (2) **Exclude, with reason:** a package-level AGENTS.md and a separate `docs/coding-standard.md`, because the document set has no content for them and the RUN-BRIEF mapping already resolves the coding standard. Route them to an `AISDLC-HARDENING` change or record them as out of scope. If the specifier prefers to exclude all of A-05, the spec must say so with this evidence and name the receiving owner. |

### REVIEW-RWB-TE-002-SG-006: audit item A-10, the MR template, is not covered

| Field | Value |
|---|---|
| Severity | Medium |
| Affects | Change scope, components, test scenarios |
| Evidence | `phase0-standards-audit.md:28` (A-10, Medium, Owner RWB-TE-002) says "There is no CODEOWNERS file and no MR template". AGENTS.md §8 (`AGENTS.md:145-148`) says "Every pull request carries the story key, the plan file, the coding tool used, the reviewer and the test results". AI Assisted Development Approach v1, review and merge section, says the same. Engineering Practices v5 §4.2 "Description" lists story key, acceptance criteria covered, and the AI first-pass review summary. `spec.md` covers CODEOWNERS (the first half of A-10) and is silent on an MR template. |
| Problem | Half of an assigned audit item is missing. AGENTS.md §8 is a binding standard for this repository, and nothing makes an MR carry the §8 fields. |
| Required fix | Add a SPEC item for `.gitlab/merge_request_templates/Default.md`. Its fields are the union of AGENTS.md §8 and Engineering Practices v5 §4.2: story key, plan file, ACs covered, coding tool, AI first-pass review summary, named reviewer (role, not a person), test results, and the `AISDLC-Run`/`AISDLC-Plan` trailers. The template is owned in the code owners file. Add a test scenario that the template exists and contains every field. Locally the template is a file only. Enforcing it on an MR is host behaviour and goes on the SG-001 gap list. Alternatively, exclude it with a reason and a receiving owner. Silence is not acceptable. |

### REVIEW-RWB-TE-002-SG-007: SPEC IDs are referenced but never defined

| Field | Value |
|---|---|
| Severity | Medium |
| Affects | Traceability chain FR → SPEC → TASK; `compliance-validation.md:47` |
| Evidence | `SPEC-RWB-TE-002-001` to `-012` appear only in the coverage table (`spec.md:49-67`) and the Clarification Log (`spec.md:290-296`). No table or heading in `spec.md` defines any SPEC item: `grep` finds no row or heading that starts with a SPEC ID. `compliance-validation.md:47` nonetheless reports "Unique SPEC IDs: PASS, each defined once". `traceability-standards.md` (Required Chain, Gap Checks "Orphaned IDs") and `specification-execution-gates.md:121-122` require unique, defined SPEC IDs. |
| Problem | The planner's TASK IDs would map to IDs that have no content. For example, SPEC-005 and SPEC-009 cannot be told apart. The v2 compliance check that passed this is wrong. |
| Required fix | Add a "SPEC catalogue" table: ID, statement, source (BR, AC or X), and the test case. Define 001–012, and add the IDs for the SG-001, SG-004, SG-005 and SG-006 additions. Then re-check the IDs in the coverage table against the catalogue. |

### REVIEW-RWB-TE-002-SG-008: the validator is hand-written logic, but its tests and unit-test applicability are not specified

| Field | Value |
|---|---|
| Severity | Medium |
| Affects | Unit Test Applicability (`spec.md:139-148`), validation step (`spec.md:206-219`), test scenarios (`spec.md:254-265`) |
| Evidence | `spec.md:145` says "There is no hand-written application unit to test". `spec.md:208-215` specifies a parser with five failure modes: syntax, missing owner, duplicate pattern, unknown owner and no-match pattern. Only the unknown owner has a test case (TC-TE-002-07). `security-quality-standards.md:31` says "Critical business rules require positive and negative tests". `implementation-execution-gates.md` sets an 80% gate for any surface that changes. |
| Problem | In this repository the validator and the ownership resolver are new code, whether Java under `backend/src/test` or a script. The spec says no unit needs testing, which contradicts its own design. |
| Required fix | Specify positive and negative tests for each validator rule: a valid file, a missing owner, a duplicate pattern, an unknown owner (AC7), a no-match pattern, a declared external pattern (SG-002), and the last-match-wins ordering (BR5). Specify resolver tests for AC1–AC4. State which surface hosts the code. If it sits in the backend Gradle test tree, set the Backend row to `YES` with the 80% gate on the validator classes. If it is a script, name the runner and the coverage evidence. Do not mark it `NOT_APPLICABLE` only because it is "tooling". |

### REVIEW-RWB-TE-002-SG-009: the files that hold the control are not owned, and new owner entries have no role basis

| Field | Value |
|---|---|
| Severity | Low |
| Affects | BR4 intent, the integrity of the CodeOwnersValidation step |
| Evidence | The CODEOWNERS block (`spec.md:165-178`) does not own `.gitlab-ci.yml`, where the validation job lives (`spec.md:157`), and does not own the owner register (SG-004). Engineering Practices v5 §10 names "Pipeline gates: TechX DevOps with SCB IT" as a role. Story v7 §3 has handles only for the two teams. |
| Problem | Removing the validation job, or editing the owner register, needs no code-owner review, so the control can be weakened without its owners. |
| Required fix | Own the pipeline file and the owner register. Use a placeholder for the document-set role (pipeline gates: TechX DevOps with SCB IT), mark it `ASSUMED`, and raise an open item. Never invent a handle. Alternatively, record why they are left unowned. |

### REVIEW-RWB-TE-002-SG-010: TC-TE-002-08 defers to a test-case row that contradicts the story

| Field | Value |
|---|---|
| Severity | Low |
| Affects | TC-TE-002-08, X7 |
| Evidence | `spec.md:265-268` says the full Given/When/Then is in Recovery Workbench Test Cases v7. In Test Cases v7, row TC-TE-002-08, the Given/When/Then is "Refused with MSG-P4-002; nothing changes; the refusal is logged". Story v7 §16 says "This story has no Workbench endpoint, so MSG-P4-002 is not shown". |
| Problem | A tester who follows the reference gets an outcome the story rules out. |
| Required fix | State that TC-TE-002-08 follows story v7 §16 (story files rank above the test-case workbook) and that it is a host-only gap under SG-001. Reference document gap DG-06. |

### REVIEW-RWB-TE-002-SG-011: the spec carries stale gate status and wrong counts

| Field | Value |
|---|---|
| Severity | Low |
| Affects | Spec header, Status reporting |
| Evidence | `spec.md:11` says "spec gate PASS; ... 3 Low findings carried", while `compliance-validation.md:12` says "5 Low". `spec.md:14` cites `REVIEW-RWB-TE-002-SPEC-001` as the approval. `spec.md:311` says `CLARIFICATION_STATUS: RESOLVED [OPEN_ITEMS: 0]`, while `assumptions.md:14` refers to OPEN-038 and OPEN-041, which are open (`open-items.md:28,31`). |
| Problem | Under D-RUN-05 the v2 gate result does not apply here. The header suggests otherwise and is internally inconsistent. |
| Required fix | Reset the status to the result of this gate. Cite this review ID. Correct the Low count and the open-item count (2 or more). |

## Answers to the two review questions

**(a) Correct and complete against v14?** The spec covers the story completely, and its precedence
rulings (BR4 over §10; branch rules on all three branches; the TE-001 paths) follow L-RCV-12,
L-RCV-13, D-RCV-10, D-RCV-21, D-RCV-37 and D-RCV-50. D-RCV-35/36 do not affect this story: there is
no view, no workflow and no rule. ADR v3 ADR-008 and Decision Log v10 DT11 say trunk merges go "into
main"; D-RCV-50 adds `develop-recovery`. The spec covers both (DG-03). Against the baseline, it fails
on SG-007 (undefined SPEC IDs), SG-010 (unrecorded test-case conflict) and SG-011 (stale status).

**(b) Implementable here?** Not as written. See SG-001 to SG-004 and SG-008. Audit items:

| Audit item | Covered by the spec? | Disposition required |
|---|---|---|
| A-05: AGENTS.md §5 paths do not resolve | **No.** The spec is silent (SG-005). | Cover: correct the paths and own AGENTS.md. |
| A-05: no package AGENTS.md | **No.** The spec is silent (SG-005). | May be excluded legitimately: no document-set content exists; route to hardening. |
| A-05: no coding-standard file | **No.** The spec is silent (SG-005). | May be excluded legitimately: RUN-BRIEF maps it to `backend-standards.md` / `frontend-standards.md`. The spec must say so. |
| A-10: no CODEOWNERS | **Yes**, with the fixes in SG-002, SG-003 and SG-004. | Use `.gitlab/CODEOWNERS`. |
| A-10: no MR template | **No.** The spec is silent (SG-006). | Cover: the AGENTS.md §8 fields. |

## Plan inputs (not spec findings)

1. **Sequencing.** RWB-TE-001 is not built in this repository: `backend/src/test/resources/architecture/`
   is empty and INC-002 has only `_v2-baseline`. The module-map pattern (`spec.md:174`) will fail the
   no-match check until TE-001 merges. Plan TE-002 after TE-001, as Build Sequence v6 and D-RUN-01
   require.
2. **Recovery paths in this repository** that the spec's list does not own: `backend/src/test/java/th/co/scb/ace/demo/e2e/`
   (the recovery e2e tests), `api/recovery-api-v4.yaml` (the contract), `frontend/src/api/schema.d.ts`
   (generated types), and `infra/postgres/init/` (the ADR-010 roles and grants). Decide each one
   against BR1/BR2 ("every recovery folder") and name it in the plan.
3. **Real ACE monorepo paths** in the v2 spec, and the v2 plan's file list. Re-derive them for this
   repository; they are not findings here (D-RUN-05).
4. **GitLab mechanics.** A code owners file may live at the root, in `docs/` or in `.gitlab/`.
   Code-owner approval on protected branches is a paid-tier GitLab feature. The author-approval and
   reset-on-push settings are MR approval settings. Record the target ACE tier as part of OPEN-038.
5. **Branches.** Only `develop-recovery` exists locally. Do not create `main` or `develop` to stage
   test PRs. The host settings file names all three (L-RCV-13).
6. **Owners.** Keep `@scb-ace/techx-recovery-tech-leads` and `@scb-ace/ace-team` exactly as story v7
   §3 gives them, marked `ASSUMED`. Every other owner is a document-set role with a placeholder and an
   open item. No person is named.
7. **Open items to propose** in `shared-updates.md` at the next specify run: owner placeholders for
   the solution architect and pipeline-gate roles (SG-005, SG-009); the host-only acceptance criteria
   as human-verification gaps (SG-001); and the A-05 package AGENTS.md and coding standard routed to
   hardening.

```text
SPEC_GATE: FAIL [CRITICAL: 0] [HIGH: 2] [MEDIUM: 6] [LOW: 3]
REVIEW_GATE: BLOCKED — High/Medium findings require remediation and re-review, or explicit human acceptance.
NEXT_STEP: Technical Specifier re-runs RWB-TE-002 specify in output/INC-004-epic-1-RWB-TE-002/specify/ addressing SG-001..SG-011, then this spec gate re-runs (spec-gate-review-2.md).
```

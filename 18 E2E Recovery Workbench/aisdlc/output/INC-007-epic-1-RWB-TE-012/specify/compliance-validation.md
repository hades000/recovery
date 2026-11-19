# Compliance validation — RWB-TE-012 specification (specifier self-check)

| Field | Value |
|---|---|
| Artifact | `output/INC-007-epic-1-RWB-TE-012/specify/spec.md` v10 |
| Stage | Technical Specifier self-check before spec gate round 10 (remediation run 9) |
| Date | 2026-11-18 |
| Round 1 gate | `review/spec-gate-review.md`: FAIL (0 Critical, 1 High, 5 Medium, 5 Low). The orchestrator (Claude Code) ran that gate; v1 of this file wrongly said the specifier spawned it (corrected, SG-07) |
| Round 2 gate | `review/spec-gate-review-2.md`: FAIL (0 Critical, 0 High, 2 Medium, 4 Low); Compliance Reviewer spawned by this specifier run |
| Round 3 gate | `review/spec-gate-review-3.md`: FAIL (0 Critical, 0 High, 1 Medium, 7 Low); Compliance Reviewer spawned by this specifier run. Triage by the orchestrator (Claude Code), logged at 04:54 (D-RUN-09) |
| Round 4 gate | `review/spec-gate-review-4.md`: FAIL (0 Critical, 0 High, 2 Medium, 5 Low); Compliance Reviewer spawned by this specifier run. Triage by the orchestrator (Claude Code), logged at 05:01 (D-RUN-09) |
| Round 5 gate | `review/spec-gate-review-5.md`: FAIL (0 Critical, 0 High, 0 Medium, 4 Low); Compliance Reviewer spawned by this specifier run. Low findings only, so the self-run round allowed by the orchestrator's (Claude Code) 05:01 triage was used (run 5) |
| Round 6 gate | `review/spec-gate-review-6.md`: FAIL (0 Critical, 0 High, 0 Medium, 2 Low); Compliance Reviewer spawned by this specifier run. Triage by the orchestrator (Claude Code), logged at 05:33 (D-RUN-09) |
| Round 7 gate | `review/spec-gate-review-7.md`: FAIL (0 Critical, 0 High, 0 Medium, 2 Low); Compliance Reviewer spawned by this specifier run. Low findings only, so the self-run round allowed by the orchestrator's (Claude Code) 05:33 triage was used (run 7) |
| Round 8 gate | `review/spec-gate-review-8.md`: FAIL (0 Critical, 0 High, 0 Medium, 2 Low); Compliance Reviewer spawned by this specifier run. Triage by the orchestrator (Claude Code), logged at 05:40 (D-RUN-09) |
| Round 9 gate | `review/spec-gate-review-9.md`: FAIL (0 Critical, 0 High, 0 Medium, 2 Low); Compliance Reviewer spawned by this specifier run. Low findings only, so the self-run round allowed by the orchestrator's (Claude Code) 05:40 triage was used (run 9) |
| Round 10 gate | `review/spec-gate-review-10.md` |
| Previous versions | `compliance-validation.run1.md` (v1), `.run2.md` (v2), `.run3.md` (v3), `.run4.md` (v4), `.run5.md` (v5), `.run6.md` (v6), `.run7.md` (v7), `.run8.md` (v8), `.run9.md` (v9) |

## 1. Required spec structure (`.github/rules/specification-execution-gates.md`)

| Item | Present | Where |
|---|---|---|
| `Status:` line | Yes, `Status: SUCCESS` | spec.md line 3 |
| Change Scope Declaration with all fields; New Nodes Required YES/NO | Yes, "YES" then the list (template, parameter files, `RUNBOOK.md`, `dochub` types) | spec.md "Change Scope Declaration" |
| Requirement-to-SPEC Logic Coverage | Yes, 37 rows, 37 covered, 0 blocked; Coverage Type only `DIRECT` or `INHERITED_EXISTING_BEHAVIOR`, Status only `COVERED`; FR-RWB-007, REQ-DCM-002/-003, NFR-029, NFR-053, CTL-09, CTL-12 have own rows | spec.md |
| `CONTRADICTIONS` | Bare number, 0; counting rule stated (only unresolved contradictions; precedence-settled conflicts listed as DGAP rows) | spec.md coverage summary and "Status reporting" |
| User story intent; entry trigger and preconditions | Yes; precondition "RWB-TE-001 merged" | spec.md |
| Field-level matrix | Yes (properties incl. `readiness-recheck-seconds`, BlobRef, BlobWriteRequest, StoredBlob, metadata, audit event, health detail incl. `identities`) | spec.md |
| Status-transition matrix | Yes (readiness; only the probe writes it; single-flight, freshness, start-event and background-request rows) | spec.md |
| Exceptional-case behaviour | Yes, X1–X10 plus five | spec.md |
| API change assessment | Yes, NO_API_CHANGE; published Java surface recorded | spec.md; `contracts/backend-apis.json` v5 (adds `BLOB_MISSING`, readiness writer rule) |
| Unit Test Applicability | Yes, one frontend and one backend row; four counters | spec.md |
| Frontend / Backend Specification | Yes, SPEC-001 to -023; tests T-TE012-01 to -18 | spec.md |
| Clarification Log | Yes, 26 rows, RESOLVED | spec.md |
| Status lines | Yes | spec.md "Status reporting" |

## 2. Rule checks

| Check | Result | Evidence |
|---|---|---|
| Every statement cites a source or is a labelled assumption | Pass | "Sources cited"; `assumptions.md` ASM-TE012-01 to -33; external Azure behaviour cited to Microsoft Learn, each page checked live: `[AZ-IMM]`, `[AZ-REST]`, `[AZ-COND]` ("Conditional deployment with templates"), `[AZ-MODES]` ("Deployment modes"), `[AZ-GET]` ("Blob Containers - Get"), `[AZ-CLI-CRM]`, `[AZ-CLI-IMM]` and `[AZ-CLI-REST]` (Azure CLI reference) |
| Every number states its source | Pass | `timeout-seconds` 10 from story §13 and AC10; `readiness-recheck-seconds` 30 assumed (ASM-TE012-30); SPEC-009 "Numbers and where they come from" |
| AC10 bound when the hub is not READY | Pass | SPEC-009 single-flight probe with a `timeout-seconds` deadline; T-TE012-17 |
| Readiness written only by the probe; per-operation outcomes isolated (SG-26) | Pass | Status-transition matrix, SPEC-009, SPEC-013, SPEC-015 and `contracts/backend-apis.json` agree; T-TE012-06, -17, -18 |
| Template unit test needs no undecided value; placeholders refused before deploy (SG-27) | Pass | SPEC-001 schema list, local file, placeholder rule, pre-deploy check with owner and place; T-TE012-15; open item per value in `shared-updates.md` §3 |
| Later PROD applies after the lock (SG-28, SG-35) | Pass | SPEC-004 conditional policy, PROD file `false`, incremental mode only, effective `deployLegalPolicy` checked and applied by one printed command, "Extend" step PROD only; `[AZ-IMM]`, `[AZ-REST]`, `[AZ-COND]`, `[AZ-MODES]`; pre-deploy check with explicit resource group and account inputs and an observable "no policy" state (`[AZ-GET]` read through `az rest`, `[AZ-CLI-REST]`; `[AZ-CLI-CRM]`), with seven ordered rows (each accept and refuse path reachable, any other output refused), local checks before any Azure read, a printed report on every outcome, Builder cases BE-01 to BE-13 (BE-05, BE-06 set `legalContainerName` in the environment file), environment and file tied, legal container name read from the file or template default, assumed CLI output shapes refused if different (SG-37, SG-39, SG-40); ASM-TE012-33 |
| Placement per the predecessor's module map | Pass | `dochub.api`, `dochub.storage` per RWB-TE-001 v4 SPEC-009, -022, -025; SPEC-016, -022 |
| Baseline evolved, not duplicated (A-04) | Pass | Evolution map: each baseline element has one successor; no second adapter |
| Carried tests not weakened | Pass | T-TE012-14 maps each RWB-TE-001 SPEC-024 assertion to a successor |
| Later-story contracts conformed to, seams named (D-RUN-08) | Pass | SPEC-010, -019; `shared-updates.md` §7 (E1-017 DGAP-22, E1-054 DGAP-23) |
| Coverage per RWB-TE-001 v4 SPEC-020, outside `check`, no exclusion | Pass | SPEC-023; Unit Test Applicability |
| Health flag-off behaviour sourced; no storage call on health reads | Pass | SPEC-009, -020; DGAP-21; ASM-TE012-20 |
| Template format and PROD lock | Pass with recorded gaps | SPEC-001 (format reason), SPEC-004 (runbook step: owner `[S]` §10, approver, evidence; later-apply rule); DGAP-09, DGAP-24 |
| Tests do not depend on `.env` or commit a key | Pass | SPEC-018 "How tests set the profile and the emulator string": runtime-generated keys, explicit properties |
| Local stack and existing `.env` upgrade | Pass | SPEC-021; T-TE012-13; Builder evidence step |
| No new dependency (AGENTS.md §4.4) | Pass | ASM-TE012-16; virtual threads are JDK 21; Jackson, Testcontainers, Mockito already present |
| No credential in code or configuration | Pass with recorded local exception | SPEC-017 (published Azurite key, `.env` / `.env.example` only); tests generate their own keys |
| No personal data | Pass | UUIDs; synthetic test data; audit carries staff subject and IDs only |
| No migration (D-RUN-07) | Pass | No table or column |
| Feature flag returns the previous path when off (AGENTS.md §3.13) | Pass | Off: no client, store and open refused, root health unchanged (SPEC-008, -020) |
| No question to the user (L-RCV-03) | Pass | Clarification Log; assumptions |
| Shared files untouched | Pass | `shared-updates.md` v10 (19 open items: one per undecided template value, including the storage account name and resource group, plus the pre-deploy check item) |
| Document gaps evidenced, blockers only where no precedence rule settles | Pass | `document-gaps.md`: 23 active rows (DGAP-01 to -17, -19 to -24), DGAP-18 withdrawn, 0 blockers |
| MCP | N/A | None connected |
| Design evidence | NOT_REQUIRED | No UI |

## 3. Known limits carried to the plan

- System tests TC-TE-012-01 to -12 need the SIT storage account; locally `PENDING_ENVIRONMENT`.
- AC9 "no document row" and the HTTP 409/503 mappings are verified in RWB-E1-024 / RWB-E1-026 (SPEC-019, DGAP-17).
- Early DEV spike for versioning next to the legal policy (DGAP-03).
- README "Decisions taken" row and `RUNBOOK.md` are plan-gate items (SPEC-004, -017).
- Template format is an assumption (ASM-TE012-03, DGAP-09); environment values for the template come from the open items in `shared-updates.md` §3; the pre-deploy check refuses an apply while a placeholder remains.
- DGAP-03 DEV spike also confirms, in incremental mode on a disposable account, that a skipped conditional policy resource leaves an existing unlocked policy untouched (ASM-TE012-33); no lock or "Extend" outside PROD.

## 4. Gate result

Round 4: `SPEC_GATE: FAIL [CRITICAL: 0] [HIGH: 0] [MEDIUM: 2] [LOW: 5]` (`review/spec-gate-review-4.md`). Answered in v5 (`gate-response.md` Round 4).

Round 5: `SPEC_GATE: FAIL [CRITICAL: 0] [HIGH: 0] [MEDIUM: 0] [LOW: 4]` (`review/spec-gate-review-5.md`). SG-27, -29 to -32 FIXED; SG-26 and SG-28 PARTIAL (residuals SG-33, SG-35); new SG-33 to SG-36 (Low); no new document gap. Answered in v6 (`gate-response.md` Round 5).

Round 6: `SPEC_GATE: FAIL [CRITICAL: 0] [HIGH: 0] [MEDIUM: 0] [LOW: 2]` (`review/spec-gate-review-6.md`). SG-33 to SG-36 FIXED; new SG-37, SG-38 (Low). Triage by the orchestrator (Claude Code), logged at 05:33 (D-RUN-09): run 6 (spec v7). Answered in `gate-response.md` Round 6.

Round 7: `SPEC_GATE: FAIL [CRITICAL: 0] [HIGH: 0] [MEDIUM: 0] [LOW: 2]` (`review/spec-gate-review-7.md`). SG-37, SG-38 FIXED; new SG-39, SG-40 (Low); no new document gap. Answered in v8 (`gate-response.md` Round 7).

Round 8: `SPEC_GATE: FAIL [CRITICAL: 0] [HIGH: 0] [MEDIUM: 0] [LOW: 2]` (`review/spec-gate-review-8.md`). SG-39, SG-40 FIXED; earlier-round requirements confirmed. New: SG-41 (the exact-shape list in the "no policy" table omits the account-exists output, so rows 2 and 3 are unreachable read literally) and SG-42 (the legal container parameter is not named in SPEC-002 or asserted by T-TE012-15, and no Builder case sets it). No new document gap. The self-run rounds allowed are used, so the run stops for orchestrator triage. No human acceptance recorded.

Round 8 triage by the orchestrator (Claude Code), logged at 05:40 (D-RUN-09): remediation run 8 (spec v9), then `review/spec-gate-review-9.md`. SG-41: the account lookup's account-present output (a one-element array) and the `exists: true` path are defined, and the table has seven ordered rows, each reachable, any other output refused. SG-42: `legalContainerName` (default `rwb-docs-legal`, from `[S]` §4 step 1 and §13, `[DL]` D-RCV-31) named in SPEC-002 with the other three container parameters, asserted by T-TE012-15, set in an environment file by Builder cases BE-05 and BE-06. Answered in `gate-response.md` Round 8.

Round 9: `SPEC_GATE: FAIL [CRITICAL: 0] [HIGH: 0] [MEDIUM: 0] [LOW: 2]` (`review/spec-gate-review-9.md`). SG-41, SG-42 FIXED; new SG-43 (rows 5–6 read `properties.hasImmutabilityPolicy` from CLI output the cited page does not document) and SG-44 (Builder evidence expectations not produced by the rules: output on refusal, deciding row, order of checks, BE-06 set-up). No new document gap. Low findings only, so the one further self-run round allowed by the orchestrator's (Claude Code) 05:40 triage was used: run 9 (spec v10). Answered in `gate-response.md` Round 9. No human acceptance recorded.

Round 10: pending (`review/spec-gate-review-10.md`).

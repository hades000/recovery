# Spec gate review, round 4: RWB-E1-069, read-only ACE source views, grants and boundary rule

| Field | Value |
|---|---|
| Review ID | `REVIEW-RWB-E1-069-SG4` (fourth spec gate for this RUN_ID) |
| RUN_ID | `INC-010-epic-1-RWB-E1-069` |
| Artefacts | `aisdlc/output/INC-010-epic-1-RWB-E1-069/specify/` (run 4, 2026-11-18 10:50-10:54): `spec.md`, `assumptions.md`, `document-gaps.md`, `compliance-validation.md`, `shared-updates.md`, `gate-response.md`, `agent-run-log.md` (run 4 section), `contracts/backend-apis.json`, `contracts/frontend-integrations.json`, `figma/figma_report.md`. The `*.run3.*` copies were used for the diff only. |
| Previous round | `review/spec-gate-review-3.md` (`REVIEW-RWB-E1-069-SG3`, FAIL Low-only: 0 Critical, 0 High, 0 Medium, 3 Low; REVIEW-122..124) |
| Reviewer | Compliance Reviewer (spec gate), run as a bounded general-purpose subagent |
| Date | 2026-11-18 |
| **Status** | **PASS** |
| Findings (new) | None: 0 Critical, 0 High, 0 Medium, 0 Low |
| Round-3 findings | 3 of 3 resolved: 122, 123, 124. See §2. |
| Handoff | Cleared. No finding, no gate warning. The Implementation Planner may start. |

## 1. What was checked

**Rules applied.** `.claude/agents/compliance-reviewer.md` (spec-gate mode), `aisdlc/RUN-BRIEF.md` (hard rules 1-8; D-RUN-07, D-RUN-08, D-RUN-09, D-RUN-12), `aisdlc/.github/rules/` (`pdlc.md`, `specification-execution-gates.md`, `security-quality-standards.md`, `traceability-standards.md`), the contexts `backend-context.md`, `backend-standards.md`, `testing-standards.md`, and `AGENTS.md`.

**Method.** This is a text-only remediation round, so no PostgreSQL probe or build was run. Each live artefact was diffed against its run-3 copy, and every changed line was checked against the live source, not the specifier's summary:

- `spec.md` versus `spec.run3.md`: 9 changed lines only (revision, Depends-on `[T1]`, Gate, Prepared, Sources `[T1]`, P4 last bullet, SPEC-018 mechanism sentence, Unit Test Applicability backend row, `SPEC_DEPENDENCY_REVISIONS`).
- The same diff for `assumptions.md`, `document-gaps.md`, `shared-updates.md`, `compliance-validation.md`, `gate-response.md`, `agent-run-log.md` and `contracts/backend-apis.json`.
- Live dependencies re-read in their **current** state: RWB-TE-001 **v4** (header, SPEC-002/-003/-020/-021/-022/-023/-024) and `review/spec-gate-review-5.md`; RWB-E1-044 **v14-7** (header, SPEC-014, SPEC-016, SPEC-017, OI-E044-I) and `review/spec-gate-review-7.md`; RWB-E1-001 **Revision 4** and `review/spec-gate-review-4.md`.
- Code baseline, read only: `backend/build.gradle.kts` lines 130-160 (`recoveryClasses` = main output only; both JaCoCo tasks `executionData(tasks.named("test"))`) and `RecoveryFlywayConfig` (`@Bean(initMethod = "migrate")`, package-private).
- E1-069 test plan: T-E1-069-13 and T-E1-069-16 are `recovery-it` rows present in run 3 as well, so no test was invented.

**Independent checks.**

- **Live revision labels.** TE-001's header reads "v4 (spec gate round 2 remediation ...)" and its review-5 is a PASS with 0C/0H/0M/0L. E1-044's header reads `spec_version: v14-7` and review-7 is PASS 0C/0H/0M/0L. E1-001 Revision 4 review-4 is PASS 0C/0H/0M/0L.
- **No stale live citation.** A search for `TE-001 v3` in the live set returns 0 in `spec.md`, `assumptions.md`, `document-gaps.md`, `compliance-validation.md`, `shared-updates.md` and the contract. The two occurrences in `gate-response.md` are labelled history ("describe the run-2 state"; "the live TE-001 revision is now v4").
- **Migration numbers.** `V000[1-9]` in `spec.md`: **0**. The remaining occurrences in `shared-updates.md`, `compliance-validation.md` and `gate-response.md` are marked quotations or history.
- **Shape of the set.** 20 SPEC items (unchanged), 30 document gaps DG-L01..L30 (unchanged), 42 coverage rows, 30 `Blocker?` lines and 0 live `Blocker = Yes`.
- **Shared files.** `open-items.md` 05:37, `INDEX.md` 07:40, the INC-010 card 16 Nov and `DOCUMENT-GAPS.md` 00:33 sit outside the 10:50-10:54 window. The matrix write at 10:54:39 changes rows 001-009 (other stories' plan-gate states) and leaves row 010 at "No current spec/plan"; no E1-069 proposal was applied.

## 2. Round-3 findings (verified, all resolved)

| ID | Sev. | Disposition | Verification |
|---|---|---|---|
| REVIEW-RWB-E1-069-122 | Low | **Resolved** | (a) The 80% row no longer includes the class: `spec.md` line 454 binds the gate to "all recovery main classes plus the two test-scope tooling class directories that the [T1] and [T3] includes name", and states that `RecoveryFlywayTestSupport` is "deliberately **outside** the bundle and carries no unit-coverage claim". SPEC-018 line 297 says the same ("outside the unit coverage bundle (IT-only)"). (b) The class is marked IT-only with its existing callers T-E1-069-13 (X2 probe-off, SPEC-018) and T-E1-069-16 (Flyway-mode `RecoveryDatabaseIT`, `RecoverySchemaMigrationIT`, check 5, SPEC-015/008), both `recovery-it` rows already present in run 3 at lines 470 and 473; no `test`-task unit test was invented. (c) `backend/build.gradle.kts` is **absent** from `Impacted Existing Nodes` (line 79) and the spec says E1-069 adds no build wiring; this is correct because the T1 and T3 includes are TE-001's and E1-044's edits. (d) The evidence cited is accurate: `recoveryClasses` is main output only and both JaCoCo tasks take `executionData` from the `test` task (`backend/build.gradle.kts` lines 130-160); TE-001 v4 SPEC-020(b) adds the boundary tooling class directory and SPEC-020(c) keeps execution data on `test`; E1-044 v14-7 SPEC-014 adds its own test-scope tooling directory. No `casewf.migration` directory was added to the bundle. |
| REVIEW-RWB-E1-069-123 | Low | **Resolved** | RWB-TE-001 is cited at **v4** in all four places: spec Sources `[T1]` (line 54, with the relied-on SPEC IDs), Status `SPEC_DEPENDENCY_REVISIONS` (line 494), `compliance-validation.md` row 14, and the Round 2 "Sibling revisions relied on" row in `gate-response.md` (line 30, with the correction noted). DG-L19 and ASM-006/-007 also cite v4. v4 is the live, passed revision (header; review-5 PASS 0C/0H/0M/0L), and the seven relied-on items read as cited: SPEC-002 map, SPEC-003 loader with the opaque `sourceViews`, SPEC-020 coverage counters, SPEC-021 withdrawal, SPEC-022 relocation, SPEC-023 property binding, SPEC-024 coverage tests. No relied-on item moves, so no design, test or coverage item changes. |
| REVIEW-RWB-E1-069-124 | Low | **Resolved** | P4's last bullet (line 98) and the OI-069-A row (`shared-updates.md` line 49) now state one scope. P4 keeps (a)-(b) as D-RUN-14's two rights, says "**Who applies them in SIT, UAT and PROD** stays [T3] v14-7 OI-E044-I; this spec does not answer that question and claims no ownership of it", and says OI-069-A carries **only (c)-(d)**. The row is titled "P4(c)-(d) only" and gives (a)-(b) only as a cross-reference to OI-E044-I. E1-044 v14-7 OI-E044-I still asks "Name who applies them in SIT, UAT and PROD (environment owner or ACE DBA)"; E1-069 neither answers nor claims it. Owners in the row match the rights: ACE DBA / ACE team lead for (d), environment owner with the recovery tech lead for (c). ASM-016 and compliance row 18 say the same. No competing owner is proposed for the two migration-account rights. |

**Gap candidate: none new.** The two edits in `document-gaps.md` (DG-L19 on v4, DG-L29 on the open-item split) update existing gaps; no new conflict and no Blocker value moved.

## 3. Earlier findings not reopened

| ID | Sev. | Check |
|---|---|---|
| REVIEW-RWB-E1-069-117 | High | P4(a)-(e), SPEC-004, SPEC-006, SPEC-008 check 5, SPEC-014 and SPEC-015(b) are unchanged; line 275 still says "D-RUN-14 rights are not repeated here", and no live line grants anything to `rwb_migrator`. T-044-17 is not weakened; D-RUN-14 remains the orchestrator's with OI-069-M (proposed OPEN-051) open and no human approval claimed. |
| REVIEW-RWB-E1-069-118 | Medium | SPEC-015(a), SPEC-010, SPEC-017 and SPEC-019 are unchanged: S1 and S3 stay E1-001's, E1-069 takes S2 only; 1,382 / 1,078 / 49; 526 union, 250 personal and 54 non-personal among the 304. DG-L27/L30 unchanged. |
| REVIEW-RWB-E1-069-119 | Low | `spec.md` still has 0 `V0001`-`V0009` occurrences; versions are read from file names (SPEC-017, ASM-014). |
| REVIEW-RWB-E1-069-120 | Low | SPEC-008 check 4 and SPEC-009 keep the split: catalog assertions in the migration-account session, direct-read refusals in the `recovery_svc` session. |
| REVIEW-RWB-E1-069-121 | Low | SPEC-008's one run scope, SPEC-009's opening, ASM-004 and the SPEC-018 mechanism are intact; only the coverage sentence was appended to SPEC-018. |

## 4. No design, blocker or coverage change

- **Design.** 20 SPEC items, the same 12 contract IDs, the same two files, the same grant order, the same switches and the same view/function behaviour. The only normative-adjacent edits are the OI-069-A scope bullet (item ownership, not design) and the coverage framing. No role, grant, statement order, schema object, test case or migration name moves.
- **Blockers.** 30 gaps, 0 live `Blocker = Yes`. DG-L19 and DG-L29 remain Blocker = No; RWB-ACE-001 remains the probe stand-in (DG-L16, Blocker = No).
- **Coverage.** The gate is still 80% LINE, INSTRUCTION, BRANCH and METHOD at bundle level, over the same main tree plus the same two test-scope tooling directories; T-E1-069-18 is unchanged. The only coverage change is that a test-scope class that could not be measured by the `test` task is no longer claimed to be measured - which is the finding's own remediation, not a target or scope reduction.
- **Shared state.** No E1-069 shared-update was applied. Proposals, including the INDEX row 010, remain in `shared-updates.md` for the orchestrator.
- **Personal data and secrets.** No new data field or credential; the synthetic values are unchanged.

## 5. Gate checklist

| # | Check | Result | Note |
|---|---|---|---|
| 1 | Required sections present | PASS | All sections of the round-3 set, unchanged |
| 2 | Change classification backed by requirement, trace chain and code | PASS | Matrix §3 row 010; `NEW_STORY`, `NO_API_CHANGE` |
| 3 | Every AC clause and BR maps to a SPEC item and a test | PASS | 42 rows; `REQUIREMENT_COVERAGE_RESULT` 42/42 |
| 4 | Conflicts recorded with two citations and resolved | PASS | DG-L29 and DG-L30; all gaps Blocker = No |
| 5 | Grant design internally consistent | PASS | Unchanged since the round-3 PG 16.16 verification; 117 holds |
| 6 | Dependencies only on existing code or earlier stories, named by current revision (D-RUN-08) | PASS | E1-044 v14-7, TE-001 v4, E1-001 Revision 4, all PASS |
| 7 | Migration numbers not fixed (D-RUN-07) | PASS | 0 occurrences in `spec.md` |
| 8 | Personal-data classification and controls | PASS | SPEC-019 unchanged; round-2 re-count (250/54/12) stands; 526 left to E1-001 |
| 9 | Audit logging of reads | N/A here | RWB-E1-016; stated in Out of scope |
| 10 | Secrets | PASS | Variable names only |
| 11 | API and frontend impact | PASS | `NO_API_CHANGE`; `NOT_APPLICABLE`; figma `NOT_REQUIRED` |
| 12 | Unit-test gate (80% LINE, INSTRUCTION, BRANCH, METHOD) | PASS | Target unchanged; class correctly outside the claim (122) |
| 13 | Traceability rows consistent, including NFRs | PASS | 42 rows; matrix row pending in `shared-updates.md` |
| 14 | Shared files untouched; proposals in `shared-updates.md` | PASS | No E1-069 row applied; row 010 untouched by the 10:54:39 sweep |
| 15 | No personal data in artefacts | PASS | Synthetic values only |
| 16 | Self-check (`compliance-validation.md`) accurate | PASS | Rows 7, 14 and 18 now state the corrected scope and revision |

## 6. Gate result

`GATE_RESULT: PASS` - 0 Critical, 0 High, 0 Medium, 0 Low. Round 3: **3 of 3 resolved** (122, 123, 124), each verified against the live file and its live dependency rather than the remediation summary. No round-1 or round-2 finding was reopened; no design, blocker or coverage target changed; no new gap; no new finding. This is the last Low-only text round and it closes clean.

**NEXT_STEP:** The Implementation Planner may start. The orchestrator applies `shared-updates.md` (INDEX row 010, card, matrix, open-items) after this gate.

SPEC_GATE: PASS [CRITICAL: 0] [HIGH: 0] [MEDIUM: 0] [LOW: 0]

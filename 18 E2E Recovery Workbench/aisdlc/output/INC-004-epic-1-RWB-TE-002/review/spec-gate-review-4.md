# Spec gate re-review (round 4): RWB-TE-002 Code owners for the recovery module

| Field | Value |
|---|---|
| Review ID | `REVIEW-RWB-TE-002-SG-2026111804` |
| RUN_ID | `INC-004-epic-1-RWB-TE-002` |
| Gate | Specification gate, re-review after remediation run 3. The run fixes SG-017 and re-aligns the spec with RWB-TE-001 v4. Under D-RUN-09 the orchestrator did not accept the round 3 Low-only failure (`AI-SDLC-BUILD-LOG.md` line 32). It answered SG-017 in its triage row (`AI-SDLC-BUILD-LOG.md` line 126, timeline 2026-11-17T23:55:06). The orchestrator is Claude Code, the AI agent running this pipeline. Every remediation choice reviewed here is that orchestrator's triage, as written in `specify/gate-response.md` "Round 3". No person decided or approved any of it, and this review records no human acceptance or disposition. |
| Previous reviews | `REVIEW-RWB-TE-002-SG-2026111701` (`spec-gate-review.md`): `FAIL` 0C/2H/6M/3L, SG-001 to SG-011. `REVIEW-RWB-TE-002-SG-2026111702` (`spec-gate-review-2.md`): `FAIL` 0C/0H/0M/5L, SG-012 to SG-016. `REVIEW-RWB-TE-002-SG-2026111703` (`spec-gate-review-3.md`): `FAIL` 0C/0H/0M/1L, SG-017 |
| Artefacts reviewed | `specify/spec.md` (577 lines), `compliance-validation.md`, `assumptions.md`, `document-gaps.md`, `gate-response.md` (Rounds 1 to 3), `shared-updates.md`, `agent-run-log.md`, `contracts/*.json`. I used the `*.run3.md` copies (run-2 text) only to diff what changed. |
| Upstream checked | RWB-TE-001 v4: `output/INC-002-epic-1-RWB-TE-001/specify/spec.md` (SPEC-001, -002, -007, -011, -014, -015, -020, -022, -026, the Relocation table, the Components table, Change Scope), `assumptions.md` ASM-05, and `review/spec-gate-review-5.md` (`SPEC_GATE: PASS` 0/0/0/0) |
| Baseline | Story Files v7, RWB-TE-002 story file v1 (`requirement/legacy/04-user-stories/recovery-workbench-user-stories-epic-1-story-files-v7_extracted/rwb-te-002-code-owners-for-the-recovery-module-v1.md`; §1 line 30, §12 lines 157–158, §13 "Done when" line 189, §17 line 118 of the card); `aisdlc/requirement/Traceability_Matrix.md`; `AI-SDLC-BUILD-LOG.md` D-RUN-06 (line 29), D-RUN-09 (line 32) and the SG-017 triage (line 126) |
| Rules applied | `aisdlc/.github/rules/pdlc.md` (lines 20–31), `specification-execution-gates.md`, `implementation-execution-gates.md`, `security-quality-standards.md`, `traceability-standards.md`; RUN-BRIEF (hard rules 1 to 8, document-gap rule, D-RUN-07, D-RUN-08) |
| Repository check | On 2026-11-18 I checked every path in the code owners block and in UT-13, UT-14, UT-15, UT-25 and UT-26 by directory listing. I read `.git/config` and `.git/HEAD` as files. I ran no git command and edited no code, spec or shared file. |
| Reviewer | Compliance Reviewer (agent run) |
| Date | 2026-11-18 |

## Status

**`FAIL`** (Low-only; does not block the handoff automatically)

| Severity | Count | IDs |
|---|---|---|
| Critical | 0 | none |
| High | 0 | none |
| Medium | 0 | none |
| Low | 2 | SG-018, SG-019 |

- **SG-017 is resolved.** The merge condition names both carriers, the writer and the time of writing, and gives the exact sentence. It agrees with the orchestrator's triage and with D-RUN-06.
- **TE-001 v4 alignment is correct.** Every code owners path, owner mapping and boundary-related path matches RWB-TE-001 v4 and the repository tree. No pattern names a package that TE-001 renames or moves.
- **The `{te001FixtureRoot}` substitution is acceptable.** It is enforced twice, by V9 and by UT-26.
- **No regression.** SG-001 to SG-016 stay resolved.
- **Two new Low findings:**
  - SG-018: carrier (1), the merge commit message, assumes a merge commit that git does not create by default.
  - SG-019: a shared-file proposal still says "remediation run 2".
- Under `pdlc.md` lines 23–24 the status stays `FAIL`, and both findings stay visible.

## 1. Disposition of SG-017: Resolved

**What the spec says now**

- **Merge condition row.** "Local completion state (story §13)", row "Merge condition for placeholders" (`spec.md:454`), states:
  1. **Carriers.** The local merge commit message of the RWB-TE-002 merge into `develop-recovery`, and `aisdlc/output/INC-004-epic-1-RWB-TE-002/README.md`.
  2. **Writer and time.** The orchestrator (Claude Code), in its merge step for RWB-TE-002. No lifecycle stage writes them or stands in for that step.
  3. **Required text.** The exact sentence "Acceptance pending HV-01..HV-11 (PROP-OI-2). OPEN-038 open: …(HV-11)." under the heading `Acceptance criteria covered`, which is the SPEC-015 MR template heading.
  4. **Checks.** The orchestrator does not complete the merge without the sentence in the commit message, and writes `README.md` in the same step. A later stage that reads the merge record reports a missing sentence as a defect. The code gate runs before the merge, so it does not check these carriers.
  5. **ACE host.** The MR description carries the same text.
- **Pointers.** SPEC-017 points to this row (`spec.md:120`), as do CLAR-010 (`:559`), the status line `MERGE_RECORD` (`:574`) and `shared-updates.md` §5 (`:41-53`). §5 gives the orchestrator the commit subject `RWB-TE-002: <summary>`, the `AISDLC-Run` and `AISDLC-Plan` trailers and the README content.

**Checked against the triage and the lifecycle**

| Question | Result | Evidence |
|---|---|---|
| Both carriers named exactly | Yes. The README path matches the triage's `output/<RUN_ID>/README.md` once `output/` is resolved under the `aisdlc/` workspace root (RUN-BRIEF "Paths"). | `AI-SDLC-BUILD-LOG.md:126`; `spec.md:454`; `shared-updates.md:48-49` |
| Writer and time named | Yes: the orchestrator, in the merge step | `spec.md:454`; D-RUN-06 (`AI-SDLC-BUILD-LOG.md:29`: "the orchestrator alone writes shared files and merges") |
| Checkable text | Yes: an exact sentence and an exact heading | `spec.md:454`; `shared-updates.md:48` |
| Consistent with D-RUN-06 and the lifecycle | Yes. The orchestrator is the only merger. The code gate runs before the merge (`pdlc.md:31`), and the spec correctly says that gate does not check the carriers. No lifecycle agent writes a run-root `README.md`: the Technical Documenter writes under `output/<RUN_ID>/docs/` (RUN-BRIEF hard rule 2). | `CLAUDE.md` "Where the evidence is" (start with the run's `README.md`) |
| Triage attributed correctly | Yes. It is attributed to the orchestrator (Claude Code, an AI agent), with no person named. | `spec.md:13`, `:559`; `gate-response.md` Round 3 |

SG-018 qualifies "exactly" for carrier (1): see below.

## 2. Alignment with RWB-TE-001 v4 (check 2)

| Item | TE-001 v4 | TE-002 spec | Repository on 2026-11-18 | Result |
|---|---|---|---|---|
| 19 module packages (incl. `casewf`, `dochub`) | SPEC-001 (b); module list at TE-001 `spec.md:113` | `/backend/src/main/java/th/co/scb/ace/demo/recovery/` and `/backend/src/test/java/th/co/scb/ace/demo/recovery/`, directory patterns (`spec.md:272-273`) | Both folders exist. Today they hold `platform`, `rules`, `workflow`, `documents`. | Match. These patterns cover the tree before and after the move. |
| Removed baseline packages | SPEC-001 (d), SPEC-022 (a) | No pattern names `platform`, `rules`, `workflow` or `documents`. A grep of `spec.md`, `shared-updates.md`, `compliance-validation.md` and the contracts finds no `recovery/platform…`, `recovery/rules…`, `recovery/workflow…` or `recovery/documents…` path. | — | Match |
| Relocated paths used in tests | Relocation table (TE-001 `spec.md:201-219`), SPEC-022 (f) | UT-14 inputs:<br>• `dochub/storage/BlobDocumentStore.java`<br>• `casewf/workflow/internal/TemporalConfig.java`<br>• `casewf/migration/RecoveryFlywayConfig.java`<br>• test `casewf/rules/DroolsRuleEngineTest.java`<br>UT-13 uses `casewf/internal/…` (`spec.md:501-502`). | — | Match. Each one is the TE-001 target package. |
| Module map file | SPEC-002: `backend/src/test/resources/architecture/recovery-modules.yaml` | Same path (`spec.md:278`) | Folder exists and is empty. Precondition P1 covers this. | Match |
| Fixture maps | SPEC-011: `backend/src/test/resources/architecture/fixtures/` | Same path (`spec.md:279`) | Not yet created. Precondition P1 covers this. | Match |
| Fixture root | SPEC-011, ASM-05: outside `th.co.scb.ace.demo`, and TE-001's plan names it | `/backend/src/test/java/{te001FixtureRoot}/` (`spec.md:276`) | Not yet created | Match (section 3) |
| `ModulithTest` | SPEC-007: existing class, unchanged | `/backend/src/test/java/th/co/scb/ace/demo/ModulithTest.java` (`spec.md:275`) | Exists at that path | Match |
| Frontend import rule | SPEC-014: D-RCV-39 block in `frontend/eslint.config.js`, unchanged | Owned in `[Recovery module]` and in `[Pipeline gates]` (`spec.md:284`, `:315`). V5 allows the same pattern in two sections (UT-05). | Exists | Match |
| Frontend fixture test | SPEC-015: `frontend/src/modules/recovery/__tests__/importBoundary.test.ts` (plan may rename it) | Covered by `/frontend/src/modules/recovery/` | Folder exists with regular files, so V9 holds | Match |
| TE-001 tooling package | Components: under `recovery/architecture/` (plan names it) | Covered by the recovery test pattern. The codeowners package must not be that package (`spec.md:247-251`). | — | Consistent |
| Other paths | `PlatformE2ETest`, `db/modulemigration/recovery/`, `frontend/e2e/`, `api/recovery-api-v4.yaml`, `frontend/src/api/schema.d.ts`: TE-001 v4 moves none of them. It does not change `.gitlab-ci.yml`, `scripts/dev.ps1` or the frontend config files (TE-001 Change Scope, "Not changed"). | As in run 2 | All exist. All 13 `[Pipeline gates]` and `[Repository standards]` paths exist. | Match |

**V6 order check in `[Recovery module]`.** No earlier pattern is covered by a later directory pattern. The later directory patterns are `e2e/`, `{te001FixtureRoot}/`, the migration folder, `fixtures/`, `modules/recovery/` and `frontend/e2e/`, and each is disjoint from the earlier entries. A fixture root that enclosed `th/co/scb/ace/demo` would be caught by V6, so the order is safe even before the substitution.

## 3. Evaluation of `{te001FixtureRoot}` (check 3)

**Verdict: acceptable and enforceable. Not a defect.**

**Why it is needed.** TE-001 v4 SPEC-011 and ASM-05 deliberately leave the fixture root package to TE-001's plan, and no TE-001 plan exists today. TE-002 may depend only on what TE-001 delivers (D-RUN-08). So a literal path written now would be a guess.

**Alternatives are worse.**

- A broader pattern such as `/backend/src/test/java/` in `[Recovery module]` would also take ACE's common and collection test trees. That conflicts with BR3, ASM-TE002-05 and story §19.
- Dropping the line would leave the TE-001 boundary fixtures unowned, against story §17 ("the file is the review control for the TE-001 boundary").

**Enforcement is double and independent of the planner's diligence.**

1. If the token reaches the file, V4 passes it (`{` is not in the V4 set). V9 then fails with `matches no file` (`spec.md:392`), because no such folder exists.
2. UT-26 (C) asserts that the live file has no `{te001FixtureRoot}` token (`spec.md:514`).
3. UT-26 (B) walks every regular file under `backend/src/test/java/` (except `…/demo/common/`) and every file under `backend/src/test/resources/architecture/`, and requires `[Recovery module]` for each. A wrong or missing root path therefore fails whatever name TE-001 chose. It also fails if TE-001 created more than one root.
4. UT-26 also requires at least one file under the substituted pattern, so the line is in use.
5. Precondition P1 (`spec.md:140`) sequences the plan after TE-001 merges, so the planner reads a real path.

**Scope of the substitution.** It is bounded: one token on one line, written once. The "drop the line" branch (ASM-TE002-18) applies only if TE-001's plan departs from TE-001 v4 SPEC-011, and UT-26 still holds in that case.

**Plan input (not a finding).** The plan should record the substituted path and its evidence, which is the merged TE-001 file list. The plan gate can then compare the plan line with the code owners line.

## 4. Regression check of SG-001 to SG-016 (check 4)

I diffed `spec.md` against `spec.run3.md`. Every removed line was replaced by an extended version:

- header, status and "Prepared" rows;
- Inherited Existing Behavior;
- boundary group (a) (UT-01–UT-26);
- coverage rows BR1, BR2 and §17;
- SPEC-002, -003, -004, -013, -014 and -017;
- P1 and P2;
- the Backend Unit Test Applicability row;
- the Components note;
- the code owners block intro and the path basis rows;
- the Local completion state count, end state and merge row;
- UT-12 and UT-14;
- the Clarification Log intro;
- `NEXT_STEP`.

No content that closed an earlier finding was lost.

| Finding | Disposition | Evidence (current lines) |
|---|---|---|
| SG-001 (High) No local boundary for host-only controls | Still resolved | Four groups `spec.md:42-47`; HV-01–HV-11 `OPEN — NOT_TESTED_HERE` `:429-441`; `:220-222` |
| SG-002 (High) Common pattern matches no file | Still resolved | SPEC-004 `:107`; register `reservedPatterns` `:375-377`; V9/V10 `:392-393` |
| SG-003 (Medium) GitHub form | Still resolved | `.gitlab/CODEOWNERS` sections `:268-317`; HC-01–HC-08 `:411-418`; CLAR-001 `:550` |
| SG-004 (Medium) Owner existence needs a host API | Still resolved | SPEC-009 `:112`; V7 `:390`; HC-08/HV-07 `:418`, `:437` |
| SG-005 (Medium) A-05 | Still resolved | SPEC-016 `:119`; UT-22 `:510`; exclusions `:535-536` |
| SG-006 (Medium) A-10 MR template | Still resolved | SPEC-015 `:118`; UT-21 `:509`; HV-09 `:439` |
| SG-007 (Medium) SPEC IDs undefined | Still resolved | Catalogue `:104-122`, 001–019 once each |
| SG-008 (Medium) Validator tests and applicability | Still resolved | Backend `REQUIRED` 80% `:218`; V1–V12 each with a failing and a passing case |
| SG-009 (Low) Control files unowned | Still resolved | Control sections `:286-295`; `[Pipeline gates]` `:304-317` |
| SG-010 (Low) TC-TE-002-08 | Still resolved | TC mapping `:516-519`; HV-06 `:436` |
| SG-011 (Low) Stale status | Still resolved | Header `:7`, `:13` cite review 3 and this review |
| SG-012 (Low) CI job labelled as tested locally | Still resolved | Group (b) `:45`; Flow 2 `:82`; SPEC-013/-014 `:116-117` |
| SG-013 (Low) Duplicate section names | Still resolved | V12 `:395`; UT-23 `:511`; UT-18 `:506`. The three BR4 control files are still matched only by the two control sections, so the UT-18 assertion holds. |
| SG-014 (Low) Build files unowned | Still resolved | `[Pipeline gates]` `:304-317`; UT-25 `:513` |
| SG-015 (Low) Local completion state | Still resolved | SPEC-018 `:121`; `:451-454`; `LOCAL_COMPLETION_STATE` `:573` |
| SG-016 (Low) Real-looking migration number | Still resolved | UT-15 `:503` (`V9999__rwb_te_002_resolver_fixture.sql`, never written) |

Review 3's observations are taken up:

1. **TC count.** It is corrected at `spec.md:446-447`: "all eight depend on an HV item: five partly checked by a UT and three host-only".
2. **Triage pointer.** The run log now points to `gate-response.md` "Round 3" and to the build-log row (`agent-run-log.md:103`).
3. **SnakeYAML classpath.** Review 3 plan input 2 is in P2 and ASM-TE002-09 (`spec.md:141`; `assumptions.md:17`).

## 5. New findings

### REVIEW-RWB-TE-002-SG-018: carrier (1) assumes a merge commit, but git does not create one by default

| Field | Value |
|---|---|
| Severity | Low |
| Affects | SPEC-017 (`spec.md:120`); "Merge condition for placeholders" (`spec.md:454`); status line `MERGE_RECORD` (`spec.md:574`); `shared-updates.md:48`, `:51` |
| Evidence | The merge condition makes carrier (1) "the local merge commit message of the RWB-TE-002 merge into `develop-recovery`", written by the orchestrator, and says "no lifecycle stage writes them". Nothing in the spec, `shared-updates.md` §5 or D-RUN-06 (`AI-SDLC-BUILD-LOG.md:29`) says that the merge creates a commit. `.git/config` (lines 1–7) sets no `merge.ff`, so git fast-forwards whenever `develop-recovery` has not moved since the feature branch was cut. In that case no merge commit exists. The only new commits are then the Implementation Builder's commits, and the spec says no lifecycle stage writes the carrier. |
| Problem | In the fast-forward case, carrier (1) does not exist. The orchestrator's check "does not complete the merge unless the commit message carries the text" then refers to no commit. A later reader cannot tell which commit to search. The intent is clear, and README.md still carries the sentence, so the risk is low. But the triage required the carrier to be named exactly, and it is not fully determined. |
| Required fix | In the merge-condition row, SPEC-017 and `shared-updates.md` §5, state that the orchestrator merges RWB-TE-002 with a commit it writes itself: `git merge --no-ff` (or a squash commit). Say that this commit is carrier (1), with subject `RWB-TE-002: <summary>`, the trailers, and the sentence under `Acceptance criteria covered`. Optionally, say that `aisdlc/output/INC-004-epic-1-RWB-TE-002/README.md` is committed in that same commit, so that both carriers are recorded together. |

### REVIEW-RWB-TE-002-SG-019: Traceability Matrix proposal still cites "remediation run 2"

| Field | Value |
|---|---|
| Severity | Low |
| Affects | `shared-updates.md` §3, row "§3 row 004 `RWB-TE-002`" (`shared-updates.md:28`) |
| Evidence | The Spec/plan column proposal reads "`output/INC-004-epic-1-RWB-TE-002/specify/spec.md` (remediation run 2)". The status text in the same row says "run 3, aligned to RWB-TE-001 v4", and the spec header says remediation run 3 (`spec.md:7`). Run 3 updated §3 (`shared-updates.md:6-7`: "changed … the §3 and §4 status values") but left this label. |
| Problem | The orchestrator applies `shared-updates.md` rows to the shared Traceability Matrix as written (RUN-BRIEF hard rule 3). The matrix would then record the wrong spec revision for RWB-TE-002, which weakens the requirement-to-spec trace (`traceability-standards.md`). |
| Required fix | Change "(remediation run 2)" to "(remediation run 3, aligned to RWB-TE-001 v4)" in `shared-updates.md:28`. Make the same check for any other run label in §3 and §4. |

## 6. Observations (not findings)

1. **Post-merge check depends on stage order.** The merge row says a later stage "for example the Traceability Manager" reports a missing sentence. The lifecycle does not fix whether the Traceability Manager runs before or after the orchestrator's merge (`CLAUDE.md` lifecycle; `traceability-manager.md` line 41, "commit metadata when available"). The binding control is the orchestrator's own pre-merge check. The post-merge check is a backstop and works only if a stage runs after the merge. The orchestrator may name the stage that checks after the merge.
2. **UT-26 (B) scope.** UT-26 (B) requires every file under `backend/src/test/java/` except `…/demo/common/` to resolve to `[Recovery module]`. This holds in this repository, which has no collection module (D-RUN-08; story §19). If an ACE collection test tree is ever added, UT-26 will need a matching exclusion like ASM-TE002-05.
3. **Contracts.** `contracts/*.json` are unchanged and still correct (`NO_API_CHANGE`, no integrations).

## 7. Document gaps

I found no new document gap with evidence.

- **SP-DG-01 to SP-DG-10** are unchanged and none is a blocker.
- **SG-017, SG-018 and the TE-001 v4 alignment** concern this repository's merge path (D-RUN-06) and local file layout (story §12 uses `<ACE base path>` placeholders, already covered by SP-DG-02). They are not a silence or a conflict in the document set.
- **SG-019** is a defect in a run artefact.

I agree with `specify/document-gaps.md` "Run 3".

## 8. Standard gate checklist

| Check | Result |
|---|---|
| Authentication and authorization | N/A to runtime: no endpoint. Repository rights are documented as host settings (HC-01 to HC-08). |
| Customer and account data protection; PII | No personal data, e-mail, person or credential in the spec, register, fixtures or proposals. The only synthetic handle is `@scb-ace/recovery-leads-typo`. |
| Audit logging | N/A (no financial action). The merge record is the audit carrier for OPEN-038 (SG-018). |
| KYC, AML, suitability, consent | Not in scope |
| Frontend integration and error contract | `NO_API_CHANGE`. Frontend `NOT_APPLICABLE` with evidence (`spec.md:217`). |
| Secrets and environment configuration | No token is used. The host owner check fails closed when built in ACE (ASM-TE002-06). |
| Test coverage gate planned | Backend 80% LINE, BRANCH, INSTRUCTION and METHOD on the codeowners package, with execution data from `codeOwnersTest`. The Builder runs it as evidence, and the host run is HV-07 (`spec.md:117`, `:218`). |
| Traceability | 38 of 38 rows covered. SPEC-001 to -019 defined once. HV items are carried as visible human-verification gaps (`pdlc.md:31`). |
| Spec status for the Builder | The header still reads `DRAFT` (`spec.md:13`). `implementation-execution-gates.md` needs `Status: SUCCESS` before build. Update it when the gate result allows (carried from review 3, plan input 5). |

```text
SPEC_GATE: FAIL [CRITICAL: 0] [HIGH: 0] [MEDIUM: 0] [LOW: 2]
REVIEW_GATE_WARNING: Low-severity review failure does not automatically stop this handoff; unresolved findings may carry downstream. Human disposition required.
REVIEW_GATE: WARNING — Low-only (SG-018, SG-019); SG-017 resolved; SG-001..SG-016 remain resolved; RWB-TE-001 v4 alignment verified; {te001FixtureRoot} substitution accepted as enforceable.
NEXT_STEP: Under D-RUN-09 the orchestrator either re-runs the Technical Specifier to fix SG-018 (state that the RWB-TE-002 merge is a commit the orchestrator writes, --no-ff or squash, and that it is carrier (1)) and SG-019 (run label in shared-updates.md §3), then re-gates as review/spec-gate-review-5.md, or routes both to the engagement lead for a human disposition. The Implementation Planner starts only after RWB-TE-001 merges (precondition P1).
```

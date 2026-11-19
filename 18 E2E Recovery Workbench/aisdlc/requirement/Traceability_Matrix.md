# Recovery Workbench — traceability matrix

**Version:** 2.1, 18 November 2026
**Source:** document set v14; `docs/increments/INDEX.md`; `output/EPIC1-STORY-MANIFEST.json`
**Rule:** a row is current only when it links a business requirement, a functional group, an
active story, a current spec/plan and evidence. Historical rows say so.

## 1. Context trace

| Context ID | File | Mapped requirement groups |
|---|---|---|
| `CTX-PROJECT-RWB-V2` | `.github/contexts/project-context.md` | BR-RWB-001..020 |
| `CTX-DOMAIN-RWB-V2` | `.github/contexts/domain-context.md` | all |
| `CTX-BACKEND-RWB-V2` | `.github/contexts/backend-context.md` | FR-RWB-003..016 |
| `CTX-FRONTEND-RWB-V2` | `.github/contexts/frontend-context.md` | FR-RWB-001..008, 017 |
| `CTX-TESTING-RWB-V2` | `.github/contexts/testing-standards.md` | NFR-RWB-001..010 |
| `CTX-BACKEND-STANDARDS-V2` | `.github/contexts/backend-standards.md` | FR-RWB-003..016 |
| `CTX-FRONTEND-STANDARDS-V2` | `.github/contexts/frontend-standards.md` | FR-RWB-001..008, 017 |

## 2. Business to functional trace

| Business requirement | Functional group | Stories |
|---|---|---|
| `BR-RWB-001` | `FR-RWB-001` | RWB-E1-002, RWB-E1-031 |
| `BR-RWB-002` | `FR-RWB-002` | RWB-E1-023, RWB-E1-035 |
| `BR-RWB-003` | `FR-RWB-003` | RWB-E1-018 |
| `BR-RWB-004` | `FR-RWB-004` | RWB-E1-020 |
| `BR-RWB-005` | `FR-RWB-005` | RWB-E1-021 |
| `BR-RWB-006` | `FR-RWB-006` | RWB-E1-028, RWB-E1-030 |
| `BR-RWB-007` | `FR-RWB-007` | RWB-E1-024/025/026/032/033/040/041/049/050/053/054/057, RWB-TE-012 |
| `BR-RWB-008` | `FR-RWB-008` | RWB-E1-034, RWB-E1-046, RWB-E1-052, RWB-E1-055 |
| `BR-RWB-009` | `FR-RWB-009` | RWB-E1-008, RWB-E1-027, RWB-E1-014, RWB-TE-008 |
| `BR-RWB-010` | `FR-RWB-010` | RWB-E1-042 |
| `BR-RWB-011` | `FR-RWB-011` | RWB-E1-043, RWB-E1-045 |
| `BR-RWB-012` | `FR-RWB-012` | RWB-E1-019, RWB-E1-022, RWB-E1-037, RWB-E1-038, RWB-E1-039 |
| `BR-RWB-013` | `FR-RWB-013` | RWB-E1-001, RWB-E1-069, RWB-E1-064, RWB-E1-065, RWB-TE-004 |
| `BR-RWB-014` | `FR-RWB-014` | RWB-E1-070, RWB-E1-071 |
| `BR-RWB-015` | `FR-RWB-015` | RWB-E1-072, RWB-E1-073 |
| `BR-RWB-016` | `FR-RWB-016` | RWB-E1-066, RWB-E1-067, RWB-E1-068 |
| `BR-RWB-017` | `FR-RWB-017` | RWB-E1-013 |
| `BR-RWB-018` | `FR-RWB-018` | RWB-E1-058..063, RWB-TE-013 |
| `BR-RWB-019` | `FR-RWB-019` | Epic 2: RWB-E2-002/004/013/014 |
| `BR-RWB-020` | `FR-RWB-020` | Epic 2: RWB-E2-007/008/027 |

## 3. Story trace (Epic 1)

| INC | Story | Business | Functional | Spec / plan / evidence | Status |
|---|---|---|---|---|---|
| 001 | `RWB-E1-044` | `BR-RWB-013` | `FR-RWB-013` | `output/INC-001-epic-1-RWB-E1-044/specify/spec.md` v14-7 (review-7 PASS), `plan/plan.md` v2 (review-2 PASS 0C/0H/0M/0L), `implement/`, `docs/` (DOC-RWB-E1-044-001..018), run `README.md` | Implemented - merged 18 Nov 2026; code `b1d7424` on `develop-recovery`, branch `feature/RWB-E1-044-db-migrations` tip `89477bc`; 243 unit, 18 integration, 28 frontend; coverage 94.81/94.26/86.07/97.98; DG-E044-DYN-01 Blocker No |
| 002 | `RWB-TE-001` | `BR-RWB-013` | `FR-RWB-013` | `output/INC-002-epic-1-RWB-TE-001/specify/spec.md` v4, `plan/plan.md` v7, `implement/`, `docs/` | Implemented - merged 18 Nov 2026; code `dc2d25b` on `develop-recovery`, branch `feature/RWB-TE-001-module-boundary` tip `55f1ed4`; 141 backend unit, 6 integration, 6 e2e, 28 frontend; coverage 97.46/97.31/95.31/97.91 backend, 91.66/91.89/88.09/82.35 frontend; docs DOC-RWB-TE-001-001..015 |
| 003 | `RWB-E1-042` | `BR-RWB-010` | `FR-RWB-010` | `output/INC-003-epic-1-RWB-E1-042/specify/spec.md` rev 13 (review-12 PASS), `plan/plan.md` (plan-gate-review-2 PASS 0C/0H/0M/0L), `implement/` (figures `implement/code-gate-fix/test-and-coverage-counts.txt`, logs `implement/code-gate-fix/round2/`), `api-tests/report.md`, `review/`, `docs/` (DOC-RWB-E1-042-001..022) | Implemented - merged 18 Nov 2026; code `0b87102` on `develop-recovery`, branch `feature/RWB-E1-042-parameter-catalog` tip `25c8f94`; 388 unit, 59 integration, 13 API (PASSED); functional N/A; coverage LINE 91.0 / INSTRUCTION 90.7 / BRANCH 80.9 / METHOD 95.8; ponytail Ship, security PASS, code gate round 4 PASS 0/0/0/0 (rounds 1-3 FAIL, each fixed); TC-E1-042-20 `ParameterConfigIT#concurrentApprovalsGiveOneApprovedAndOne409` (SPEC-014), TC-E1-042-22 `ParameterConfigIT#flagOnLoadsThroughTheAdapter`, `ParameterConfigIT$FlagOff#flagOffStillStartsAndRefusesParameterLoads` (SPEC-021), TC-E1-042-23 `ParameterConfigIT#unknownKeyEmptyFileAndPastValidFrom` (SPEC-012, SPEC-023); DEV-20 names: T-E1-042-04 `ParameterConfigIT#readinessIsDownNamingTheKeyAndEnvironmentWhenNoValueAndNoDefault`, -10(b) `ParameterConfigIT#failedRollbackCommitLeavesTheRowsApproved`, -17 `ParameterLoadHandlerTest#aDifferentLoadStillMeetsTheApprovedFromCheck`, -28 `ParameterCacheTest#aRebuildAfterTheEventReReadsTheRows`, -32 `ParameterStartupCheckTest#aFutureSeedNeverFailsReadiness` with `ParameterConfigIT#readinessIsUpOnTheSeededCatalog`, -44 `CatalogCompletenessCheckTest#theCredentialRuleAppliesToEveryEnvRow` |
| 004 | `RWB-TE-002` | `BR-RWB-013` | `FR-RWB-013` | `output/INC-004-epic-1-RWB-TE-002/specify/spec.md` (remediation run 4, review-5 PASS), `plan/plan.md` v2 (plan-gate-review PASS 0C/0H/0M/0L), `implement/` (figures `implement/backend/final-tip-counts.txt`), `review/`, `api-tests/report.md` and `functional-tests/report.md` (both NOT_APPLICABLE), `docs/` (DOC-RWB-TE-002-001..004), run `README.md` | Implemented - merged 18 Nov 2026; code `27567ed` on `develop-recovery`, branch `feature/RWB-TE-002-code-owners` tip `d018cf7`; UT-01..UT-26 in 35 JUnit methods, 423 backend tests; coverage over the four helper classes 95.77 / 95.90 / 96.85 / 100; ponytail Fix-1 and security 0C/2H/2M/4L fixed; code gate round 1 FAIL 0/0/0/3 fixed, round 2 PASS 0C/0H/0M/0L; D-RUN-25 addendum (11 CODEOWNERS lines) awaits tech-lead ratification (OPEN-052); HV-01..HV-11 not tested here |
| 005 | `RWB-TE-003` | `BR-RWB-013` | `FR-RWB-013` | `output/INC-005-epic-1-RWB-TE-003/specify/spec.md`, `plan/plan.md` | Spec re-issued 18 Nov 2026 (remediation 5, SPEC-RWB-TE-003-001..022), spec gate review-6 PASS; plan not current; source REQ-DRI-007, REQ-ACA-003; build not started; depends on RWB-TE-001 merged |
| 006 | `RWB-TE-011` | `BR-RWB-013` | `FR-RWB-013` | `output/INC-006-epic-1-RWB-TE-011/specify/spec.md`, `plan/plan.md` | Planned - spec run 12 review-13 PASS; plan gate review-2 PASS 0C/0H/0M/0L (18 Nov 2026); 35 tasks, 43 UTs, 19 STs; build not started (the run stopped after four stories, D-RUN-27)|
| 007 | `RWB-TE-012` | `BR-RWB-007` | `FR-RWB-007` | `output/INC-007-epic-1-RWB-TE-012/specify/spec.md`, `plan/plan.md` | Planned - spec v10 review-10 PASS; plan gate review-2 PASS 0C/0H/0M/0L (18 Nov 2026); 25 tasks, 37/37 rows; build not started (the run stopped after four stories, D-RUN-27); shared rows SH-01..07 orchestrator-applied |
| 008 | `RWB-E1-043` | `BR-RWB-011` | `FR-RWB-011` | `output/INC-008-epic-1-RWB-E1-043/specify/spec.md`, `plan/plan.md` | Planned - spec rev 10 review-10 PASS; plan gate review-2 PASS 0C/0H/0M/0L (18 Nov 2026); plan refresh needed against the merged RWB-E1-042 code before build (readiness check, 18 Nov 23:57); 20 tasks, 49/49 rows; build not started (the run stopped after four stories, D-RUN-27)|
| 009 | `RWB-E1-001` | `BR-RWB-013` | `FR-RWB-013` | `output/INC-009-epic-1-RWB-E1-001/specify/spec.md` | Specified - spec revision 4 (18 Nov 2026), spec gate review-4 PASS 0C/0H/0M/0L; plan gate round 1 FAIL 0C/0H/2M/12L, remediation not run; two Blocker = Yes gaps DG-004/DG-005 carried on ASM-E1001-13/14 |
| 010 | `RWB-E1-069` | `BR-RWB-013` | `FR-RWB-013` | `output/INC-010-epic-1-RWB-E1-069/specify/spec.md` | Specified - spec revision 4 (18 Nov 2026), spec gate review-4 PASS 0C/0H/0M/0L; plan gate round 1 FAIL 0C/0H/3M/6L, remediation not run; build not started (the run stopped after four stories, D-RUN-27); RWB-ACE-001 Tier 2 probe stand-in, Blocker No |
| 011 | `RWB-E1-007` | `BR-RWB-013` | `FR-RWB-013` | No current spec/plan; story is ready or in the backlog | Ready for specify |
| 012 | `RWB-E1-008` | `BR-RWB-009` | `FR-RWB-009` | No current spec/plan; story is ready or in the backlog | Ready for specify |
| 013 | `RWB-E1-064` | `BR-RWB-013` | `FR-RWB-013` | No current spec/plan; story is ready or in the backlog | Ready for specify |
| 014 | `RWB-E1-065` | `BR-RWB-013` | `FR-RWB-013` | No current spec/plan; story is ready or in the backlog | Ready for specify |
| 015 | `RWB-TE-004` | `BR-RWB-013` | `FR-RWB-013` | No current spec/plan; story is ready or in the backlog | Ready for specify |
| 016 | `RWB-E1-047` | `BR-RWB-013` | `FR-RWB-013` | No current spec/plan; story is ready or in the backlog | Backlog — not started |
| 017 | `RWB-E1-017` | `BR-RWB-013` | `FR-RWB-013` | No current spec/plan; story is ready or in the backlog | Backlog — not started |
| 018 | `RWB-E1-056` | `BR-RWB-013` | `FR-RWB-013` | No current spec/plan; story is ready or in the backlog | Backlog — not started |
| 019 | `RWB-E1-014` | `BR-RWB-009` | `FR-RWB-009` | No current spec/plan; story is ready or in the backlog | Backlog — not started |
| 020 | `RWB-E1-027` | `BR-RWB-009` | `FR-RWB-009` | No current spec/plan; story is ready or in the backlog | Backlog — not started |
| 021 | `RWB-TE-007` | `BR-RWB-013` | `FR-RWB-013` | No current spec/plan; story is ready or in the backlog | Backlog — not started |
| 022 | `RWB-E1-038` | `BR-RWB-012` | `FR-RWB-012` | No current spec/plan; story is ready or in the backlog | Backlog — not started |
| 023 | `RWB-TE-006` | `BR-RWB-013` | `FR-RWB-013` | No current spec/plan; story is ready or in the backlog | Backlog — not started |
| 024 | `RWB-TE-008` | `BR-RWB-009` | `FR-RWB-009` | No current spec/plan; story is ready or in the backlog | Backlog — not started |
| 025 | `RWB-E1-019` | `BR-RWB-012` | `FR-RWB-012` | No current spec/plan; story is ready or in the backlog | Backlog — not started |
| 026 | `RWB-E1-022` | `BR-RWB-012` | `FR-RWB-012` | No current spec/plan; story is ready or in the backlog | Backlog — not started |
| 027 | `RWB-E1-037` | `BR-RWB-012` | `FR-RWB-012` | No current spec/plan; story is ready or in the backlog | Backlog — not started |
| 028 | `RWB-E1-039` | `BR-RWB-012` | `FR-RWB-012` | No current spec/plan; story is ready or in the backlog | Backlog — not started |
| 029 | `RWB-E1-016` | `BR-RWB-013` | `FR-RWB-013` | No current spec/plan; story is ready or in the backlog | Backlog — not started |
| 030 | `RWB-E1-025` | `BR-RWB-007` | `FR-RWB-007` | No current spec/plan; story is ready or in the backlog | Backlog — not started |
| 031 | `RWB-E1-045` | `BR-RWB-011` | `FR-RWB-011` | No current spec/plan; story is ready or in the backlog | Backlog — not started |
| 032 | `RWB-E1-046` | `BR-RWB-008` | `FR-RWB-008` | No current spec/plan; story is ready or in the backlog | Backlog — not started |
| 033 | `RWB-E1-058` | `BR-RWB-018` | `FR-RWB-018` | No current spec/plan; story is ready or in the backlog | Backlog — not started |
| 034 | `RWB-E1-070` | `BR-RWB-014` | `FR-RWB-014` | No current spec/plan; story is ready or in the backlog | Backlog — not started |
| 035 | `RWB-E1-071` | `BR-RWB-014` | `FR-RWB-014` | No current spec/plan; story is ready or in the backlog | Backlog — not started |
| 036 | `RWB-E1-072` | `BR-RWB-015` | `FR-RWB-015` | No current spec/plan; story is ready or in the backlog | Backlog — not started |
| 037 | `RWB-E1-073` | `BR-RWB-015` | `FR-RWB-015` | No current spec/plan; story is ready or in the backlog | Backlog — not started |
| 038 | `RWB-E1-018` | `BR-RWB-003` | `FR-RWB-003` | No current spec/plan; story is ready or in the backlog | Backlog — not started |
| 039 | `RWB-TE-013` | `BR-RWB-018` | `FR-RWB-018` | No current spec/plan; story is ready or in the backlog | Backlog — not started |
| 040 | `RWB-E1-013` | `BR-RWB-017` | `FR-RWB-017` | No current spec/plan; story is ready or in the backlog | Backlog — not started |
| 041 | `RWB-E1-020` | `BR-RWB-004` | `FR-RWB-004` | No current spec/plan; story is ready or in the backlog | Backlog — not started |
| 042 | `RWB-E1-024` | `BR-RWB-007` | `FR-RWB-007` | No current spec/plan; story is ready or in the backlog | Backlog — not started |
| 043 | `RWB-E1-062` | `BR-RWB-018` | `FR-RWB-018` | No current spec/plan; story is ready or in the backlog | Backlog — not started |
| 044 | `RWB-E1-066` | `BR-RWB-016` | `FR-RWB-016` | No current spec/plan; story is ready or in the backlog | Backlog — not started |
| 045 | `RWB-E1-002` | `BR-RWB-001` | `FR-RWB-001` | No current spec/plan; story is ready or in the backlog | Backlog — not started |
| 046 | `RWB-E1-023` | `BR-RWB-002` | `FR-RWB-002` | No current spec/plan; story is ready or in the backlog | Backlog — not started |
| 047 | `RWB-E1-028` | `BR-RWB-006` | `FR-RWB-006` | No current spec/plan; story is ready or in the backlog | Backlog — not started |
| 048 | `RWB-E1-031` | `BR-RWB-001` | `FR-RWB-001` | No current spec/plan; story is ready or in the backlog | Backlog — not started |
| 049 | `RWB-E1-049` | `BR-RWB-007` | `FR-RWB-007` | No current spec/plan; story is ready or in the backlog | Backlog — not started |
| 050 | `RWB-E1-067` | `BR-RWB-016` | `FR-RWB-016` | No current spec/plan; story is ready or in the backlog | Backlog — not started |
| 051 | `RWB-E1-068` | `BR-RWB-016` | `FR-RWB-016` | No current spec/plan; story is ready or in the backlog | Backlog — not started |
| 052 | `RWB-E1-021` | `BR-RWB-005` | `FR-RWB-005` | No current spec/plan; story is ready or in the backlog | Backlog — not started |
| 053 | `RWB-E1-030` | `BR-RWB-006` | `FR-RWB-006` | No current spec/plan; story is ready or in the backlog | Backlog — not started |
| 054 | `RWB-E1-041` | `BR-RWB-007` | `FR-RWB-007` | No current spec/plan; story is ready or in the backlog | Backlog — not started |
| 055 | `RWB-E1-050` | `BR-RWB-007` | `FR-RWB-007` | No current spec/plan; story is ready or in the backlog | Backlog — not started |
| 056 | `RWB-E1-015` | `BR-RWB-013` | `FR-RWB-013` | No current spec/plan; story is ready or in the backlog | Backlog — not started |
| 057 | `RWB-E1-011` | `BR-RWB-013` | `FR-RWB-013` | No current spec/plan; story is ready or in the backlog | Backlog — not started |
| 058 | `RWB-E1-026` | `BR-RWB-007` | `FR-RWB-007` | No current spec/plan; story is ready or in the backlog | Backlog — not started |
| 059 | `RWB-E1-035` | `BR-RWB-002` | `FR-RWB-002` | No current spec/plan; story is ready or in the backlog | Backlog — not started |
| 060 | `RWB-E1-053` | `BR-RWB-007` | `FR-RWB-007` | No current spec/plan; story is ready or in the backlog | Backlog — not started |
| 061 | `RWB-E1-057` | `BR-RWB-007` | `FR-RWB-007` | No current spec/plan; story is ready or in the backlog | Backlog — not started |
| 062 | `RWB-E1-059` | `BR-RWB-018` | `FR-RWB-018` | No current spec/plan; story is ready or in the backlog | Backlog — not started |
| 063 | `RWB-E1-032` | `BR-RWB-007` | `FR-RWB-007` | No current spec/plan; story is ready or in the backlog | Backlog — not started |
| 064 | `RWB-E1-033` | `BR-RWB-007` | `FR-RWB-007` | No current spec/plan; story is ready or in the backlog | Backlog — not started |
| 065 | `RWB-E1-034` | `BR-RWB-008` | `FR-RWB-008` | No current spec/plan; story is ready or in the backlog | Backlog — not started |
| 066 | `RWB-E1-040` | `BR-RWB-007` | `FR-RWB-007` | No current spec/plan; story is ready or in the backlog | Backlog — not started |
| 067 | `RWB-E1-052` | `BR-RWB-008` | `FR-RWB-008` | No current spec/plan; story is ready or in the backlog | Backlog — not started |
| 068 | `RWB-E1-060` | `BR-RWB-018` | `FR-RWB-018` | No current spec/plan; story is ready or in the backlog | Backlog — not started |
| 069 | `RWB-E1-061` | `BR-RWB-018` | `FR-RWB-018` | No current spec/plan; story is ready or in the backlog | Backlog — not started |
| 070 | `RWB-E1-054` | `BR-RWB-007` | `FR-RWB-007` | No current spec/plan; story is ready or in the backlog | Backlog — not started |
| 071 | `RWB-E1-063` | `BR-RWB-018` | `FR-RWB-018` | No current spec/plan; story is ready or in the backlog | Backlog — not started |
| 072 | `RWB-E1-055` | `BR-RWB-008` | `FR-RWB-008` | No current spec/plan; story is ready or in the backlog | Backlog — not started |

## 4. Retired and removed stories

| Story | Reason | New home | Trace status |
|---|---|---|---|
| `RWB-E1-003/004/009` | Data loads removed by D-RCV-35 U1 | ACE ingestion, RWB-ACE-001 | Retired — no spec |
| `RWB-E1-005/010/012` | Trackers removed by D-RCV-35 U5 | Cutover plan, section 8 | Retired — no spec |
| `RWB-E1-006` | Data-quality load removed by D-RCV-35 U1 | ACE checks; daily gate in RWB-E1-015 | Retired — no spec |
| `RWB-E1-051` | ADF/Control-M feed removed by D-RCV-35 U1 | ACE ingestion, RWB-ACE-001 | Retired — no spec |
| `RWB-E1-029` | Rule load retired by D-RCV-36 T8 | RWB-E1-073 | Retired — no spec |
| `RWB-TE-005` | Rule harness retired by D-RCV-36 T8 | RWB-E1-073 | Retired — no spec |
| `RWB-E1-048` | Rule audit retired by D-RCV-36 T8 | RWB-E2-041 | Retired — no spec |

## 5. Epic 2 trace

The 43 Epic 2 stories are listed in `docs/increments/epic-2-stories.md` and map to
BR-RWB-017..020 and the Epic 2 FSDs. Their specs and plans open one month before release.

## 6. Coverage summary

| Layer | Total | Mapped | Current spec | Current plan | Implemented |
|---|---:|---:|---:|---:|---:|
| Business requirements | 20 | 20 | — | — | — |
| Functional groups | 20 | 20 | — | — | — |
| Epic 1 stories | 72 | 72 | 10 | 7 | 4 |
| Epic 2 stories | 43 | 43 | 0 | 0 | 0 |
| Retired / removed | 10 | 10 | 0 | 0 | 0 |

**Implemented and merged on `develop-recovery` (18 Nov 2026):** `RWB-E1-044` (INC-001) at `b1d7424`;
`RWB-TE-001` (INC-002) at `dc2d25b`; `RWB-E1-042` (INC-003) at `0b87102`; `RWB-TE-002` (INC-004) at
`27567ed`. Post-merge `dev.ps1 test`, `it` and `e2e` are green for all four.
**Current plan, not built:** `RWB-TE-011` (INC-006), `RWB-TE-012` (INC-007), `RWB-E1-043` (INC-008; plan
refresh needed before build).
**Current spec, plan not current:** `RWB-TE-003` (INC-005), `RWB-E1-001` (INC-009), `RWB-E1-069` (INC-010).
The run stopped after four stories on the engagement lead's instruction (D-RUN-27).

The two technical enablers are grouped under `BR-RWB-013` / `FR-RWB-013` in this matrix for continuity;
their source requirements are `REQ-DRI-006` (TE-002), `REQ-DRI-007` and `REQ-ACA-003` (TE-003). They
do not add a business capability to the FR set.

## 7. Evidence index

| Run | Specification | Plan | Implementation |
|---|---|---|---|
| INC-001 `RWB-E1-044` | `output/INC-001-epic-1-RWB-E1-044/specify/spec.md` (v14-7, review-7 PASS) | `output/INC-001-epic-1-RWB-E1-044/plan/plan.md` (v2, plan-gate-review-2 PASS) | `implement/`, `api-tests/`, `functional-tests/`, `review/`, `docs/`, run `README.md`; merged `b1d7424` |
| INC-002 `RWB-TE-001` | `output/INC-002-epic-1-RWB-TE-001/specify/spec.md` (v4) | `output/INC-002-epic-1-RWB-TE-001/plan/plan.md` (v7) | `implement/`, `api-tests/`, `functional-tests/`, `review/`, `docs/`, run `README.md`; merged `dc2d25b` |
| INC-003 `RWB-E1-042` | `output/INC-003-epic-1-RWB-E1-042/specify/spec.md` (rev 13, review-12 PASS) | `output/INC-003-epic-1-RWB-E1-042/plan/plan.md` (plan-gate-review-2 PASS) | `implement/` (`code-gate-fix/test-and-coverage-counts.txt`), `api-tests/report.md` (13 PASSED), `functional-tests/` (N/A), `review/` (code gate round 4 PASS), `docs/`, run `README.md`; merged `0b87102` |
| INC-004 `RWB-TE-002` | `output/INC-004-epic-1-RWB-TE-002/specify/spec.md` (review-5 PASS) | `output/INC-004-epic-1-RWB-TE-002/plan/plan.md` (v2, plan-gate-review PASS) | `implement/` (`backend/final-tip-counts.txt`, `post-merge/`), `api-tests/` and `functional-tests/` (N/A), `review/` (code gate round 2 PASS), `docs/`, run `README.md`; merged `27567ed` |
| INC-005 `RWB-TE-003` | `output/INC-005-epic-1-RWB-TE-003/specify/spec.md` (review-6 PASS) | not started | not built |
| INC-006 `RWB-TE-011` | `output/INC-006-epic-1-RWB-TE-011/specify/spec.md` | `plan/plan.md` (plan-gate-review-2 PASS) | not built |
| INC-007 `RWB-TE-012` | `output/INC-007-epic-1-RWB-TE-012/specify/spec.md` | `plan/plan.md` (plan-gate-review-2 PASS) | not built |
| INC-008 `RWB-E1-043` | `output/INC-008-epic-1-RWB-E1-043/specify/spec.md` (rev 10, review-10 PASS) | `plan/plan.md` (plan-gate-review-2 PASS; refresh needed) | not built |
| INC-009 `RWB-E1-001` | `output/INC-009-epic-1-RWB-E1-001/specify/spec.md` (review-4 PASS) | `plan/plan.md` (plan-gate-review FAIL) | not built |
| INC-010 `RWB-E1-069` | `output/INC-010-epic-1-RWB-E1-069/specify/spec.md` (review-4 PASS) | `plan/plan.md` (plan-gate-review FAIL) | not built |
| REVIEW-001 | post-merge review of INC-001..004 | `output/REVIEW-001-first-four-stories/plan.md` | `output/REVIEW-001-first-four-stories/` |

### Tests added by REVIEW-001 (merged `9c05371`, `3297584`)

| Finding | Story | Test |
|---|---|---|
| H1, CG-R001-02 | RWB-E1-042 | `ParameterConfigIT#concurrentApprovalsOfTwoLoadsForOneKeyAreSerialised`, `#rollbackRacingAnApprovalOfTheSameKeyIsSerialised`, `#keyEnvironmentLocksAreTakenInAscendingLockKeyOrder` |
| H2 | RWB-E1-042, RWB-TE-001 | `PlatformInfoControllerTest#aMissingEnvironmentFailsAtStartup`, `#anEnvironmentOutsideTheListFailsAtStartup` |
| H4 | RWB-TE-002 | `OwnershipResolverTest#addendumPathsHaveOwners` |
| M4, M5, CG-R001-01 | RWB-E1-042 | `ParameterLoadHandlerTest#rollbackRecordsTheDecision`, `#rollbackRecorderFailureIs503`, `#theDecisionRecordNamesTheOutcome` |
| M6 | RWB-E1-042 | `ParameterStartupCheckTest#aDatabaseOutageIsReportedAsUnavailable`, `#theSameStateIsLoggedOnce` |
| M9 | RWB-E1-042 | `ParameterCacheTest#theTtlReadDoesNotRecurse` |
| M11 | RWB-TE-001 | `frontend/src/auth/AuthCallback.test.tsx`; Playwright `e2e/platform.spec.ts` (3 of 3 after merge) |
| CONF-TE001-01 | RWB-TE-001 | `ModuleMapLoaderTest#duplicatePublishedIsRejected` |
| CONF-E044-01..07, CONF2..CONF4 | RWB-E1-044 | `RecoveryMigrationLintTest` (72 tests, one failing fixture per position check), `RecoveryMigrationIT` (12) |

## 8. Matrix status

`TRACEABILITY_STATUS: CURRENT` as of 19 Nov 2026 — 20 business requirements, 20 functional groups,
72 Epic 1 stories, 43 Epic 2 stories, 10 retired stories, 38 context IDs. No orphan story. Rows 001 to
004 trace to merged code; rows 005 to 010 trace to spec and plan only.

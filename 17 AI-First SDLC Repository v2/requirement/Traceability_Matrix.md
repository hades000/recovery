# Recovery Workbench — traceability matrix

**Version:** 2.0, 16 November 2026
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
| 001 | `RWB-E1-044` | `BR-RWB-013` | `FR-RWB-013` | `output/INC-001-epic-1-RWB-E1-044/specify/spec.md`, `plan/plan.md` (historical) | Planned — plan carried from the 10 Nov 2026 run; schema basis reverted to `recovery` by D-RCV-35; re-plan before build |
| 002 | `RWB-TE-001` | `BR-RWB-013` | `FR-RWB-013` | `output/INC-002-epic-1-RWB-TE-001/specify/spec.md`, `plan/plan.md`, `implement/` | Implemented — module boundary built; spec and plan rebaselined 16 Nov 2026 |
| 003 | `RWB-E1-042` | `BR-RWB-010` | `FR-RWB-010` | `output/INC-003-epic-1-RWB-E1-042/specify/spec.md`, `plan/plan.md`, `implement/` | Implemented — migration applied and tested; spec and plan rebaselined 16 Nov 2026 |
| 004 | `RWB-TE-002` | `BR-RWB-013` | `FR-RWB-013` | `output/INC-004-epic-1-RWB-TE-002/specify/spec.md`, `plan/plan.md` | Planned — spec and plan current 17 Nov 2026; source `REQ-DRI-006`; build not started |
| 005 | `RWB-TE-003` | `BR-RWB-013` | `FR-RWB-013` | `output/INC-005-epic-1-RWB-TE-003/specify/spec.md`, `plan/plan.md` | Planned — spec and plan current 17 Nov 2026; source `REQ-DRI-007`, `REQ-ACA-003`; build not started |
| 006 | `RWB-TE-011` | `BR-RWB-013` | `FR-RWB-013` | No current spec/plan; story is ready or in the backlog | Ready for specify |
| 007 | `RWB-TE-012` | `BR-RWB-007` | `FR-RWB-007` | No current spec/plan; story is ready or in the backlog | Ready for specify |
| 008 | `RWB-E1-043` | `BR-RWB-011` | `FR-RWB-011` | `output/INC-008-epic-1-RWB-E1-043/specify/spec.md`, `plan/plan.md` (historical) | Planned — plan carried from the 10 Nov 2026 run; re-baseline for D-RCV-35 |
| 009 | `RWB-E1-001` | `BR-RWB-013` | `FR-RWB-013` | No current spec/plan; story is ready or in the backlog | Ready for specify |
| 010 | `RWB-E1-069` | `BR-RWB-013` | `FR-RWB-013` | No current spec/plan; story is ready or in the backlog | Ready for specify |
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
| Epic 1 stories | 72 | 72 | 4 | 4 | 2 |
| Epic 2 stories | 43 | 43 | 0 | 0 | 0 |
| Retired / removed | 10 | 10 | 0 | 0 | 0 |

**Current spec/plan/implementation:** `RWB-E1-042` (INC-003) and `RWB-TE-001` (INC-002).
**Current spec/plan, not built:** `RWB-TE-002` (INC-004) and `RWB-TE-003` (INC-005).
**Historical:** `RWB-E1-044` (INC-001) and `RWB-E1-043` (INC-008), to be re-baselined.

The two technical enablers are grouped under `BR-RWB-013` / `FR-RWB-013` in this matrix for continuity;
their source requirements are `REQ-DRI-006` (TE-002), `REQ-DRI-007` and `REQ-ACA-003` (TE-003). They
do not add a business capability to the FR set.

## 7. Evidence index

| Run | Specification | Plan | Implementation |
|---|---|---|---|
| INC-003 `RWB-E1-042` | `output/INC-003-epic-1-RWB-E1-042/specify/spec.md` | `output/INC-003-epic-1-RWB-E1-042/plan/plan.md` | `output/INC-003-epic-1-RWB-E1-042/implement/` |
| INC-002 `RWB-TE-001` | `output/INC-002-epic-1-RWB-TE-001/specify/spec.md` | `output/INC-002-epic-1-RWB-TE-001/plan/plan.md` | `output/INC-002-epic-1-RWB-TE-001/implement/` |
| INC-004 `RWB-TE-002` | `output/INC-004-epic-1-RWB-TE-002/specify/spec.md` | `output/INC-004-epic-1-RWB-TE-002/plan/plan.md` | not built |
| INC-005 `RWB-TE-003` | `output/INC-005-epic-1-RWB-TE-003/specify/spec.md` | `output/INC-005-epic-1-RWB-TE-003/plan/plan.md` | not built |
| INC-001 `RWB-E1-044` | historical | historical | not built |
| INC-008 `RWB-E1-043` | historical | historical | not built |

## 8. Matrix status

`TRACEABILITY_STATUS: CURRENT` — 20 business requirements, 20 functional groups, 72 Epic 1
stories, 43 Epic 2 stories, 10 retired stories, 38 context IDs. No orphan story.

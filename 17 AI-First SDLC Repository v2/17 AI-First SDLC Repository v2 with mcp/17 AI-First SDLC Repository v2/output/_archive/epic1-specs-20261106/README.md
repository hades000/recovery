# Archive — Epic 1 specifications of 6 November 2026

| Field | Value |
|---|---|
| Source | `13 AI-First SDLC repository/output/INC-001..INC-078/specify/` |
| Archived | 16 November 2026 |
| Files | 256 (78 specs, compliance validations and run logs) |
| Status | **Historical only.** Not current against the 16 November 2026 baseline. |
| Why | The 15–16 November change registers re-based the data architecture (D-RCV-35) and the workflow/rules architecture (D-RCV-36); 10 stories were removed or retired and 5 added. |

## What is current

| Story | Current run |
|---|---|
| `RWB-E1-042` | `output/INC-003-epic-1-RWB-E1-042/specify/` and `plan/` |
| `RWB-TE-001` | `output/INC-002-epic-1-RWB-TE-001/specify/` and `plan/` |
| `RWB-E1-044` | historical, `output/INC-001-epic-1-RWB-E1-044/` (re-baseline before build) |
| `RWB-E1-043` | historical, `output/INC-008-epic-1-RWB-E1-043/` (re-baseline before build) |

## Removed or retired stories in this archive

`RWB-E1-003`, `RWB-E1-004`, `RWB-E1-005`, `RWB-E1-006`, `RWB-E1-009`, `RWB-E1-010`, `RWB-E1-012`,
`RWB-E1-029`, `RWB-E1-048`, `RWB-E1-051`. Their old specs stay here for history; they are not a build
source. The retirement register names the new home.

## Old-to-new INC mapping

The old index used 78 sequential numbers in the 4 November build order. The v2 index uses Build
Sequence v6 order. The key is the story key, not the INC number; use `docs/increments/INDEX.md` for the
current card and `output/EPIC1-STORY-MANIFEST.json` for the mapping.

## Rule

Do not copy an archived spec into a current run. Do not cite an archived spec as evidence. If a story
needs its old decisions, read the decision register and the source story; re-specify from the v14
baseline.

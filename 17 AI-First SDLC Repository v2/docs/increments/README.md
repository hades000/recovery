# Increment records

| File | Content |
|---|---|
| `INDEX.md` | 72 Epic 1 story cards in Build Sequence v6 order, plus status |
| `INC-0NN-epic-1-<story>.md` | One card per active Epic 1 story |
| `epics/EPIC-001-foundation-1.md` | Epic 1 card |
| `epics/EPIC-001-tailoring.md` | Lifecycle tailoring for Epic 1 |
| `epics/EPIC-002-foundation-2.md` | Epic 2 card |
| `epics/EPIC-002-tailoring.md` | Lifecycle tailoring for Epic 2 |
| `epic-2-stories.md` | 43 Epic 2 story rows (increments open one month before release) |
| `build-sequence.md` | Working copy of Build Sequence v6 |
| `story-build-order.md` | Working copy of Story Build Order v3 |
| `story-defects.md` | Working copy of Story Defects v4 |
| `dependency-map.md` | Working copy of Dependency Map v4 |

## Numbering rule

`INC-NNN` is the Build Sequence v6 order, 001–072, not the old 4 November order. The story key is the
stable identifier; use it in conversation, Jira and traceability. The old 78 specs are in
`output/_archive/epic1-specs-20261106/`.

## Status values

| Status | Meaning |
|---|---|
| Implemented | Code, migration and evidence exist; the story is preserved |
| Planned | A spec and plan exist; the build has not started |
| Ready for specify | Dependencies are close; no current spec |
| Backlog — not started | Later window or later feature |
| Retired / removed | Not built; see `docs/retirements/story-retirement-register.md` |

## Current runs

| Story | INC | Spec | Plan | Implementation |
|---|---|---|---|---|
| `RWB-E1-042` | 003 | `output/INC-003-.../specify/` | `output/INC-003-.../plan/` | `output/INC-003-.../implement/` |
| `RWB-TE-001` | 002 | `output/INC-002-.../specify/` | `output/INC-002-.../plan/` | `output/INC-002-.../implement/` |
| `RWB-TE-002` | 004 | `output/INC-004-.../specify/` | `output/INC-004-.../plan/` | not built |
| `RWB-TE-003` | 005 | `output/INC-005-.../specify/` | `output/INC-005-.../plan/` | not built |
| `RWB-E1-044` | 001 | historical | historical | not built |
| `RWB-E1-043` | 008 | historical | historical | not built |

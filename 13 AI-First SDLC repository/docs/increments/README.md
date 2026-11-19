# Increments

Two levels of record:

- `epics/` — one epic-level card and one tailoring record per epic. These record the project path,
  scope, reused artefacts, agents and approvals that apply to every story in the epic.
- `INC-<NNN>-epic-<E>-<STORY-KEY>.md` — one story-level card per bounded story increment. The
  number and key match the `output/INC-<NNN>-epic-<E>-<STORY-KEY>/` run.

The 78 Epic 1 story cards are indexed in `INDEX.md`. The epic records are
`epics/EPIC-001-foundation-1.md` and `epics/EPIC-002-foundation-2.md`.

## Epics

| Epic | Path | Release | Status | Card | Tailoring |
|---|---|---|---|---|---|
| `EPIC-001` Foundation 1 | Greenfield module, brownfield ACE constraints | 30 Nov 2026 | In delivery | `epics/EPIC-001-foundation-1.md` | `epics/EPIC-001-tailoring.md` |
| `EPIC-002` Foundation 2 | Brownfield enhancement of the module | 31 Dec 2026 | Mobilised | `epics/EPIC-002-foundation-2.md` | `epics/EPIC-002-tailoring.md` |

Epics 3–8 are programme-level until their cards are written one month ahead, per the release plan.

## Story increments

The 78 Epic 1 cards run from `INC-001-epic-1-RWB-E1-044.md` to
`INC-078-epic-1-RWB-E1-055.md`. Their numbers and keys match the output run IDs one-to-one. See
`INDEX.md` for the full table.

## Rules

- Create the story card before the Technical Specifier starts. The card records the story scope and
  the agents; the spec follows.
- The story card's `INC` number and `RUN_ID` must match the output folder. Do not renumber a card
  after the run starts.
- The epic card and tailoring record are shared. Do not duplicate the 13-question project
  classification or the phase decisions in every story card; link to the epic record.
- Complete the tailoring record with the phase classification and the reuse/skip evidence.
- Name the approvers; `TBC` is not an approval.
- Keep the card current until the story is released.
- Record rework, context gaps and repeated agent failures in the card.

## Regenerate

`python tools/build_increment_cards.py` rebuilds the 78 story cards and `INDEX.md` from
`output/EPIC1-STORY-MANIFEST.json` and the current story files. `--check` validates the names,
`RUN_ID`s, sections and output folders without writing. The cards are deterministic; change the
story, the manifest or the script and regenerate rather than hand-editing a generated card.

## Status

- 78 Epic 1 story cards were created on 2026-11-04 and backfilled after the specification batch.
  Future increments create the card first.
- Epic 1: 63 specs match the current story ACs. 14 specs are stale after the 4 November 2026 AC
  cleanup and must be regenerated; one further spec (`RWB-E1-021`) has a pre-existing AC4 mismatch.
  The full list is in `INDEX.md`.
- 6 specs are blocked on source decisions: `RWB-E1-001`, `RWB-E1-014`, `RWB-E1-018`,
  `RWB-E1-013`, `RWB-E1-032`, `RWB-E1-061`.
- 7 Epic 1 stories have zero business ACs because they are engineering enablers:
  `RWB-E1-044`, `RWB-E1-065`, `RWB-TE-001`, `RWB-TE-002`, `RWB-TE-003`, `RWB-TE-004`,
  `RWB-TE-011`. Project Hub DT01 says DevOps and infrastructure set-up belongs in the Sprint 0
  checklist; these stories need a client decision.
- 6 stories have AC-numbering gaps: `RWB-E1-001`, `RWB-E1-007`, `RWB-E1-042`, `RWB-E1-051`,
  `RWB-E1-056`, `RWB-E1-021`.
- Named approvers remain `TBC` (`GAP-006`); the mandatory-control checklist in
  `epics/EPIC-001-tailoring.md` is unchecked.
- Epic 2 has no story cards yet; create them when the Epic 2 specification batch starts.

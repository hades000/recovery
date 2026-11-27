# Affected-story brief (Phase 4 – stories outside P1)

Read `RUN_BRIEF.md` and `STORY_EDITOR_BRIEF.md` (same folder) first; their rules apply. Differences for affected stories:

## Scope
Only the stories in your task. They are listed in `SET\24 P1 Developer Readiness v1\Affected stories outside P1 v1.csv` with the decisions that touch them, why, and the change needed. Do not touch any other story.

## Two depths
- **Full** (your task says "full"): run the reviewer prompt `C:\Users\SahilMore\Downloads\RWB Story Review P1\_scripts\REVIEWER_BRIEF.md` (+ `BRIEF_NONAPP_ADDENDUM.md` for CON/OPS/DB/ITG stories) adapted to the story's own service – but limit the review to the story's interface with rwb-source-data and the artefacts the RD-P1 rulings change (operations, events, ledger, freshness, jobs, case list, retention, ownership, error envelope, idempotency), plus any Blocker you meet on the way. Write the review to `C:\Users\SahilMore\Downloads\RWB Story Review P1\affected\<STORY KEY>\<STORY KEY> review.md` and `... findings.csv` (same formats as the P1 reviews). Then edit the story to v3 per STORY_EDITOR_BRIEF, fixing those findings so the story is consistent with the final rulings.
- **Align** (your task says "align"): no review file. Edit the story to v3 only where it cites an artefact a ruling changed (event type/topic/key/payload per RD-P1-003/008, freshness status values and fields per RD-P1-005/041, start rule per RD-P1-040). Keep every other line identical. If you find a real conflict beyond renaming, add a one-line note in your reply and log `REQUEST` – do not redesign the story.

## Output
v3 files in `STAGE\04 User stories\Recovery Workbench Service Story Files v3\<service folder>\` with the same file name (v2 → v3). Log every edit in your own EDITLOG file. Add "Readiness decisions: RD-P1-…" to the header table and a short "Version 3 changes" note at the top, as in the P1 stories.
Reply with one line per story: key, depth, v3 path (or "no change needed" with reason), findings fixed / left.

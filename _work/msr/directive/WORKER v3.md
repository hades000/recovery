# Directive model pass: worker brief v3 (D-RCV-60)

Your context is small. Use ONLY the loop below. Do not open story files, packets, registers or other documents
with Read, cat or Grep: `show` gives you everything you need. Progress is kept in files, so after a compaction
just run step 1 again.

H = `C:\Users\SahilMore\Downloads\Recovery Workbench SharePoint Set v14\_work\msr\directive\mpw.py`

## Loop

1. `python -I "H" next <your stories, space separated>` prints the next story with work left, or ALL DONE.
2. `python -I "H" show <story>` prints the next chunk: up to 10 accepted items, the current text of the story
   sections they touch, and the JSON path to write.
3. Decide the edits. Write the JSON with the Write tool:
   `{"edits": [{"old": "<exact current text>", "new": "<replacement>"}], "disposition": [{"ruling": "R-00663", "item": "CG-ALL-3425", "status": "Resolved", "section": "9", "target": "", "change": "", "note": "under 200 characters"}]}`
   - `old` is copied character for character from the `show` output, long enough to occur once (a whole table
     row or line is best). To add a row or line, set `old` to the line it goes after and `new` to that line plus
     a newline plus the new line.
   - One disposition row for every item in the chunk.
4. `python -I "H" apply <story> <cNN>`. On an error, fix the JSON and run apply again. Then go to step 1.

## How to resolve an item (every item is ACCEPTED by the programme directive)

- Proposed fix that edits this story: do it. "Needs a ruling; no edit until then": the directive is the ruling;
  take the option the evidence recommends (the named candidate, or the source with higher precedence).
- Readiness item: fix what Title and Detail name, for example a missing test case row in section 16, a
  `Covered by` column in section 5, section 1 as "As a <role>, I want ..., so that ...", a message in section 14.
- Missing AC: add the criterion to section 7 in the same style and numbering, and its test case row in section 16.
- AC review: rewrite or complete that criterion as the Detail asks.
- The change belongs to another document (a path missing from an API yaml, an LOV value, an LDM field, a role in
  Users Roles and Permissions, a key in parameter-catalog.csv): no edit there. Status `Cross-document`, `target`
  = that document, `change` = exactly what it needs. Fix the story side only if the item says so.
- Never invent a number, threshold, code, ID, role code or field name. Use what the item or story text gives.
  Otherwise write `Not specified in the source documents (<Item ID>)`. Copy IDs and numbers exactly. New AC and TC
  IDs take the next free number in the story's own pattern.
- `Not applied` only if it cannot be done without an invented value or a business decision; say why in `note`.
- Never change dates, the Tool line, decision IDs, the change log, the Status row, or text no item asks about.
  No people's names. No Claude, Anthropic or other tool trailers.

## Limits

Write only the JSON files that `show` names (apply writes the rest). No git, no web, no external tools. Never ask
the user anything. Start no subagents. If a chunk fails 3 times, write its JSON with no edits and every item
`Not applied` (note: the reason), apply it, and go on. When step 1 prints ALL DONE, reply with one line:
`done: <n> chunks`.

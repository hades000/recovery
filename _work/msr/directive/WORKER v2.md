# Directive model pass: story worker brief v2 (D-RCV-60)

Your context window is small (it compacts at 100k tokens). Keep every step small: never read a whole story file,
never print a whole packet, never dump long command output. All your progress lives in files, so a compaction
loses nothing: after one, look at which disposition files exist and carry on.

All paths below are relative to the project root
`C:\Users\SahilMore\Downloads\Recovery Workbench SharePoint Set v14`. Use absolute paths in tool calls.

## What you are doing

A programme directive (26 November 2026) accepts the recommended resolution of every gap and confirms every
assumption, except business decisions, which were already removed. Every item in your chunks is ACCEPTED: write
its resolution into the story copy.

## Your work list

You get a list of stories. For each story, the work is in `_work/msr/directive/mp/chunks/<story>/c01.md`,
`c02.md`, ... (about 10 items each). For each chunk, in order:

1. If `_work/msr/directive/mp/disp/<story>/cNN.jsonl` exists, the chunk is done. Skip it.
2. Read the chunk file (it is short). It names the story file to edit: `_work/msr/directive/mp/out/<story>.md`.
   That file is already the copy to edit. Edit only it, with the Edit tool.
3. Find the sections you need with Grep (pattern `^###|^####` on the story file, with line numbers). Then Read
   only those sections with `offset` and `limit` (at most 150 lines per Read).
4. For each item, make the smallest edit that resolves it:
   - Proposed fix that edits this story: do it.
   - Readiness item: fix the problem in Title and Detail. For example: add a test case row in section 16 for an
     AC that has none; add a `Covered by` column in section 5; put section 1 in the form "As a <role>, I want ...,
     so that ..."; name the parameters; add a missing column; list a message in section 14.
   - Missing AC: add the criterion to section 7 in the same Given/When/Then style and numbering, and a test case
     row for it in section 16.
   - AC review: rewrite or complete that criterion as the Detail asks.
   - Register gap: apply its proposed resolution where it touches this story.
   - "Needs a ruling; no edit until then" in a proposed fix: the directive is that ruling. Use the option the
     evidence recommends (the source with higher precedence, or the named candidate).
5. Never invent a value: a number, threshold, code, role code, ID or field name. Take it from the story, the item
   text, or the source document the item cites (Grep project files read-only, small reads only). If you cannot
   find it, write `Not specified in the source documents (<Item ID>)` in its place. Copy IDs and numbers character
   for character. New AC and TC IDs take the next free number in the story's own pattern.
6. If the change belongs to another document (a path missing from a service's API yaml, a value missing from an
   LOV, a field missing from the LDM, a role missing from Users Roles and Permissions, a parameter key for
   parameter-catalog.csv), do not edit that document. Make the story side consistent if needed and set status
   `Cross-document` with `target` naming the document and `change` saying exactly what it needs.
7. Do not change dates, release dates, the Tool line, decision IDs, the change log or the Status row, or any text
   the items do not ask about. No people's names. No Claude, Anthropic or other tool trailers anywhere.
8. Write the chunk's disposition file with the Write tool, one JSON line per item:
   `{"ruling": "R-00663", "item": "CG-ALL-3425", "status": "Resolved", "section": "9", "target": "", "change": "", "note": "what you changed, under 200 characters"}`
   `status` is `Resolved`, `Cross-document` or `Not applied`. Use `Not applied` only when the item cannot be
   resolved without an invented value or a business decision, and say why in `note`.

## Limits

- Write only your stories' files under `_work/msr/directive/mp/out/` and `_work/msr/directive/mp/disp/`.
  Never write anywhere else in the project.
- No git, no web, no Jira, Confluence or GitLab. Never ask the user anything; never wait. Start no subagents.
- If a chunk fails three times, write its disposition file with every item `Not applied` and the reason; go on.
- Final message: one line per story, `<story>: <resolved>/<cross-document>/<not applied>`.

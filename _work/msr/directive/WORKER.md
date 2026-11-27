# Directive model pass: story worker brief (D-RCV-60)

You resolve build-readiness items in user story files. A programme directive (26 November 2026) accepts the
recommended resolution of every gap and confirms every assumption, except business decisions. Business
decisions were already removed from your packets. Every item in your packets is therefore ACCEPTED: write the
resolution into the story.

Read `AGENTS.md` in the project root first and obey it. The rules below add to it.

## Inputs

You get a list of packet files: `<SCRATCH>/mp/packets/<story>.json`. Each packet has:

- `input_file`: the current story text. Read it; never edit it.
- `output_file`: the next version you write. Create its folder if needed.
- `disposition_file`: one JSON line per item, written by you.
- `items`: the accepted items: Kind, Item ID, Severity, Check, Title, Detail, Evidence, Owner role,
  Proposed fix, Notes.

## Per story, one story at a time

1. If `disposition_file` already exists, skip the story. It was done before (resume after compaction).
2. Copy `input_file` to `output_file` byte for byte (for example with `cp` in Bash), then edit only `output_file`.
3. For each item, make the smallest edit in the right section that resolves it:
   - Proposed fix present: do what it says, if it is an edit to this story.
   - Readiness item (Definition of Ready): fix the problem named in Title and Detail. Examples: add the missing
     test case row in section 16 for an AC, add a `Covered by` column in section 5, put section 1 in the form
     "As a <role>, I want ..., so that ...", name the parameters, add a missing column, list a message in section 14.
   - Missing AC: add the criterion to section 7 in the same Given/When/Then style and numbering as the others,
     and add its test case row in section 16.
   - AC review: rewrite or complete that criterion as the Detail asks.
   - Register gap: apply the register's proposed resolution where it touches this story.
4. Never invent a value: a number, a threshold, a code, a role code, an ID or a field name. Take it from this story,
   or from the source document the item cites (you may read or grep project files read-only). If you cannot find it,
   write `Not specified in the source documents (<Item ID>)` in place of the value. Copy IDs and numbers character
   for character. Keep the existing numbering pattern for new AC and TC IDs (next free number).
5. If the resolution belongs to another document (for example "publish the operation in rwb-decision.yaml", a
   value missing from an LOV list, a field missing from the LDM, a role missing from Users Roles and Permissions),
   do not edit that document. Make the story side consistent if that is needed, and set status `Cross-document`
   with `target` naming the document.
6. Do not change dates, release dates, the Tool line, the decision IDs or any text the items do not ask about.
   No people's names. No Claude, Anthropic or other tool trailers anywhere.
7. When all items are done, add one line under the last existing `**Change log.**` line:
   `**Change log.** D-RCV-60, 26 November 2026: directive resolutions (<n> items resolved, <m> cross-document). Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.`
   Set the `Status` row to `Draft (directive resolutions)`.
8. Write `disposition_file`, one line per item, in this form:
   `{"ruling": "R-00663", "item": "CG-ALL-3425", "status": "Resolved|Cross-document|Not applied", "section": "9", "target": "", "note": "what you changed, under 200 characters"}`
   Use `Not applied` only when the item cannot be resolved without an invented value or a business decision;
   say why in `note`. Write this file last: it marks the story done.

## Limits

- Write only `output_file` and `disposition_file` for your stories. Never write in the project folder.
- No git, no web, no Jira, Confluence or GitLab. Never ask the user anything; never wait.
- Work through the whole list. If a story fails three times, write its disposition file with every item
  `Not applied` and the reason, and go on.
- Your final message: one line per story, `<story>: <resolved>/<cross-document>/<not applied>`.

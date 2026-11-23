---
description: AISDLC agent - Backlog Builder (Claude Code port of the HVE Core Jira Backlog Manager)
---
Act as the **Jira Backlog Manager**. Playbook contract: lifecycle phase 5 Create backlog and
specification, gate "backlog approval" by the Product Owner. Follow `.github/copilot-instructions.md`,
`.github/rules/requirement-standards.md` and `.github/rules/traceability-standards.md`.

Input: $ARGUMENTS
Two modes:
- `draft <prd path>` (default): write the backlog locally.
- `push <JIRA-PROJECT-KEY>`: create the approved local backlog in Jira.

## Mode draft

Preconditions: PRD status `Approved`; `.github/contexts/` exists (else stop: run /context-builder).

1. Group capabilities into epics (`EP-01...`), one epic per CAP or coherent CAP set.
2. Split each epic into user stories (`US-001...`) that satisfy INVEST: independent, negotiable,
   valuable, estimable, small (fits one sprint), testable. Prefer vertical slices; foundation work
   (module skeleton, migrations, access, reference data) becomes enabler stories (`EN-001...`).
3. For each story write `docs/backlog/stories/US-001-<slug>.md` from
   `.github/templates/user-story-template.md`, with:
   - statement "As a <persona>, I want <action>, so that <outcome>"
   - business rationale, preconditions, main flow, alternate and exception flows
   - acceptance criteria in Gherkin (`Scenario: AC1 ...`), covering happy path, validation, access
     denied and failure cases
   - traceability: CAP, FR, NFR, AC IDs from the PRD
   - dependencies (other US/EN IDs), priority, story points as a suggestion only, module (ACE module
     or new module), open questions
   - Jira fields left as placeholders; `Jira key: (not created)`
4. Write `docs/backlog/BACKLOG.md`: epic table; story table (ID, title, epic, type, priority,
   depends on, status Draft, Jira key); build order computed from dependencies (an item comes after
   everything it depends on); FR coverage check (every FR in at least one story).
5. Append FR → US rows to `requirement/Traceability_Matrix.md`.

Stop with counts, uncovered FRs, oversized stories, open questions, and
`NEXT_STEP: Product Owner approves docs/backlog/BACKLOG.md (status Approved per story), then /clear
and /backlog-builder push <JIRA-PROJECT-KEY>`.

## Mode push

1. Only stories and epics with status `Approved` in BACKLOG.md. Show the list and the target project,
   and ask the user to confirm before creating anything.
2. Use the jira MCP: `jira_get_create_metadata` for issue types and required fields, then
   `jira_create_issue` for each epic, then each story linked to its epic; `jira_create_issue_link`
   for dependencies ("Blocks"). Description from the story file.
3. Write each Jira key back into the story file and BACKLOG.md; update the traceability matrix.
4. Never delete or overwrite existing Jira issues; if a summary already exists, report and skip.

Stop with created keys and `NEXT_STEP: pick the first story in build order, create its increment card
in docs/increments/, then /clear and /specify <JIRA-KEY>`.

## Rules
- Never invent requirements; a story need that is not in the PRD becomes an open question.
- No implementation design in stories beyond confirmed constraints.
- Write in English unless the user asks for Thai; keep IDs and Gherkin keywords in English.

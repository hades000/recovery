# new21

Export of every Jira issue in project TB0001 with component "E2E Workbench" (scbjira.atlassian.net), taken on 18 November 2026, about 20:41. It is a full text copy: every non-empty field, the description, the acceptance criteria, linked issues, comments and the attachment files.

## Contents

| Item | What it holds |
|---|---|
| `Issues index.csv` | One row per issue (174): key, story code, type, status, parent, assignee, reporter, priority, labels, dates, counts, URL, whether it has acceptance criteria, sprint, resolution, epic link. Opens in Excel. |
| `All comments.csv` | One row per comment (267): issue, comment ID, author, posted and edited time, text. |
| `Epics/` | 10 epics, one Markdown file each |
| `Stories/` | 80 stories |
| `Tasks/` | 9 tasks |
| `Sub-tasks/` | 74 sub-tasks |
| `Other/` | 1 other item(s) |
| `Attachments/<key>/` | 37 attachment files, named as in Jira |

Each file is named `TB0001-nnnn [story code] title.md` and holds the field table, description, acceptance criteria (Gherkin, when the issue has it), linked issues, sub-tasks, attachments, every comment in order, and an "Other Jira fields" table with the remaining non-empty fields.

## Counts

- 174 issues: 10 epics, 80 stories, 9 tasks, 74 sub-tasks, 1 other.
- 80 issues have acceptance criteria.
- 267 comments on 43 issues. 37 attachments downloaded.

## Notes

- **Replies:** Jira comments are not threaded. A reply is just a later comment, so the order and the @name in each comment show who is answering whom.
- **Formatting:** comment and description text keeps Jira's own markup (`*bold*`, `{{code}}`, `#` numbered lists). @mentions are replaced with the person's name where Jira could resolve it; otherwise they show as "user" plus the start of the account ID.
- **Not included:** change history, and worklogs (none are logged).
- **Updated times** are as Jira reported them at the time of export.
- This is a snapshot. It does not refresh when Jira changes. To refresh: `python -I _work/scripts/jira_export.py <mcp/jira/.env> "<this folder>"`.

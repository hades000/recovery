# 19 Jira Open Questions

Questions raised on four E2E Workbench tickets in Jira (project TB0001), answered from the latest document set, with the gaps the answers exposed. Prepared 18 November 2026. Nothing here has been posted to Jira.

| Ticket | Story | Jira status | Comments | File |
|---|---|---|---|---|
| TB0001-1208 | RWB-E1-047 Feature flags for module release with a removal date | To Do | 3 | `RWB-E1-047 Open questions and answers.md` |
| TB0001-1177 | RWB-E1-015 Freshness stamp per data product | To Do | 4 | `RWB-E1-015 Open questions and answers.md` |
| TB0001-1169 | RWB-E1-007 Integration adapters for outbound files | In Design - Solution, Block | 16 | `RWB-E1-007 Open questions and answers.md` |
| TB0001-1217 | RWB-E1-056 Run books and monitoring for every Epic 1 job | To Do | 3 | `RWB-E1-056 Open questions and answers.md` |
| all four | Every gap, with evidence, fix, decider and priority | | | `Document Gaps.md` |

## How to read an answer

- **ANSWERED**: a document in the set decides it; the source is named.
- **PROPOSED**: the documents imply the answer; the named owner should ratify it.
- **OPEN**: no document decides it; options and a recommendation are given, with the person who decides.

Source baseline: Story Files v7 / Epic 1 v9 (15 Nov), Decision Log v10, Physical Schema v6, Data Dictionary v8, API Specification v4, Interface Specifications v3, Integration Inventory v3, NFR v3, Batch and Scheduling Design v4, Observability v3, Error and Message Standard v4, Test Cases v7, Story Defects v4, Build Sequence v6, RAID v4. Project Hub v17 (27 MB) was not opened. The Henka e-mail attached to TB0001-1169 could not be read through the Jira tool.

## What matters most

1. **RWB-E1-007 is already outbound-only.** Most of its Jira thread (FileCheckRunner, 23 sample files, the Data Loading story, the stale rule) answers a version that D-RCV-35 removed on 15 Nov. The Jira title and description are stale.
2. **Fix the schema before V0001 merges.** 173 of 304 ACE rows in `sys_fields` have the wrong `physical_type` (all nine `v_ace_batch_status` rows included), and four more Physical Schema changes are needed (`Document Gaps.md` G-X-04). RWB-E1-001 is Dev In Progress.
3. **The E1-015 gate would hold every day in Epic 1.** Its source map includes AMIS, RPS (first release E3) and GL (E6), which ACE does not ingest yet.
4. **Cut-off time has four values** (08:00, 07:15, 07:00, "allocation by 07:00") and nobody approved 08:00.
5. **Build Sequence v6 contradicts the stories.** E1-056 needs TE-007 and E1-015 that are built after it, and TE-007 depends on E1-056.
6. **Retry settings (E1-007 AC3) still have the unused 45-minute wait**, although Story Defects v4 shows the item closed. INT-14 and NFR-026 disagree on 3 or 4 attempts.
7. **"Acknowledged" has no meaning without an inbound adapter** (E1-007), and one SFTP failure still creates 85 tasks.
8. **Four Quartz jobs have no catalog row or run book** (the flag report job, JOB-20, JOB-21, JOB-22), so `RunbookCompletenessTest` would fail the build.

## Decisions needed from people

| Who | What |
|---|---|
| ACE team lead | DL43 and RWB-ACE-001 date (needed by 21 Nov); audit log and notification contracts; holiday calendar owner |
| Data architect | Physical Schema v7 and Data Dictionary correction (G-X-04, G-015-08) |
| Integration architect, Henka | INT-14 path and acknowledgment, retry count, one alert per file, transport and encryption |
| Business lead, Data steward | One cut-off time, the weekly business date, flag-off gate behaviour, sources live in Epic 1, per-job critical sources |
| Tech lead | Which job writes `case_list_row`, catalog rows, who creates the flag tables, scan scope |
| Product owner, Security, Operational Risk | PROD flag change control; flag store down in PROD |
| IT lead | DL11 date (RPO, RTO, cache and threshold assumptions) |

## Next step

Say if you want the answers posted back as comments on the four Jira tickets, or the story files re-issued with the listed changes applied.

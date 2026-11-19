<!-- source: 11 Delivery and operations/Recovery Workbench Run Operating Model v2.docx -->
<!-- converted: 2026-11-04 from DOCX -->

> **Source:** `11 Delivery and operations/Recovery Workbench Run Operating Model v2.docx`  
> **Converted from:** DOCX

Recovery Workbench

Run operating model

SCB Collections and Recovery. Henka Group, 28 October 2026

| Item | Detail |
|---|---|
| Document | Recovery Workbench run operating model |
| Version | 1 |
| Date | 28 October 2026 |
| Prepared by | Henka Group |
| Structure | Henka word rules |

# 1. Support tiers

| Tier | What | Handles | Who |
|---|---|---|---|
| Tier 0 | Self-help | Help text, the content standard, the team start pack | Users |
| Tier 1 | Business support | How-to questions, access requests, data questions | Super users in each team; service desk |
| Tier 2 | Application support | Defects, failed jobs, exception queues, reference data loads | Platform administrator; reference data administrator; data steward |
| Tier 3 | Engineering | Code defects, performance, releases | TechX recovery squads; ACE team |
| Vendors and platforms | Platform support | Azure, Entra ID, COLLINS, model endpoint | SCB IT; data and analytics; Enterprise AI |

# 2. Service levels

| Severity | Meaning | Respond | Restore | Owner |
|---|---|---|---|---|
| Severity 1 | Service down or decisions wrong | 15 minutes | 4 hours | Application owner |
| Severity 2 | A main path down with no workaround | 1 hour | 1 working day | Platform administrator |
| Severity 3 | A path with a workaround | 4 hours | Agreed date | Platform administrator |
| Severity 4 | Question or cosmetic | 1 working day | Backlog | Tier 1 |

# 3. Daily run

| Time | Activity | Who |
|---|---|---|
| 05:00 to 07:00 | Loads, case creation, allocation; checks | Data steward |
| 07:30 | Exception queues and stale data reviewed | Platform administrator |
| Daily | Job monitor, alerts, outbox | Platform administrator |
| Weekly | Access requests and leavers; reference data loads | Security and reference data administrators |
| Monthly | Write-off scan, partner scorecards, retention review list | Owners as named |
| Every six months | Access review | Role owners |

# 4. Changes after go-live

- Rules, limits, lists, templates and service levels change by validated load, owned by the business.

- Code changes go through the monthly release.

- Emergency fixes follow the bank emergency change process.

# 5. Open decision

| Decision | What is needed | Answer used until decided |
|---|---|---|
| DL02 | Application owner | The Tribe lead, with the ACE team as technical custodian |

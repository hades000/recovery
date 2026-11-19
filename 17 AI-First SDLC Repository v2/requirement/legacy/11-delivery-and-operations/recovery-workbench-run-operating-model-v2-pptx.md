<!-- source: 11 Delivery and operations/Recovery Workbench Run Operating Model v2.pptx -->
<!-- converted: 2026-11-16 from PPTX -->

> **Source:** `11 Delivery and operations/Recovery Workbench Run Operating Model v2.pptx`  
> **Converted from:** PPTX

## Slide 1

SCB

COLLECTIONS AND RECOVERY TRANSFORMATION Recovery Workbench: run operating model

Henka Group, 28 October 2026 (C) Siam Commercial Bank and Henka Pte Ltd

## Slide 2

Who runs the Workbench after go-live

2

| Tier | What | Handles | Who |
|---|---|---|---|
| Tier 0 | Self-help | Help text, the content standard, the team start pack | Users |
| Tier 1 | Business support | How-to questions, access requests, data questions | Super users in each team; service desk |
| Tier 2 | Application support | Defects, failed jobs, exception queues, reference data loads | Platform administrator; reference data administrator; data steward |
| Tier 3 | Engineering | Code defects, performance, releases | TechX recovery squads; ACE team |
| Vendors and platforms | Platform support | Azure, Entra ID, COLLINS, model endpoint | SCB IT; data and analytics; Enterprise AI |

## Slide 3

Service levels

3

| Severity | Meaning | Respond | Restore | Owner |
|---|---|---|---|---|
| Severity 1 | Service down or decisions wrong | 15 minutes | 4 hours | Application owner |
| Severity 2 | A main path down with no workaround | 1 hour | 1 working day | Platform administrator |
| Severity 3 | A path with a workaround | 4 hours | Agreed date | Platform administrator |
| Severity 4 | Question or cosmetic | 1 working day | Backlog | Tier 1 |

## Slide 4

Hours and shifts

4

| Item | Design |
|---|---|
| Business hours | 08:00 to 20:00 on business days; tier 1 and tier 2 on duty |
| Early shift | 05:00 to 08:00 on business days: data steward on call for the loads and the morning chain |
| Outside hours | SCB IT on call for severity 1; platform administrator on call by rota |
| Release weekends | ACE team and the squads on call for the change window |

## Slide 5

Escalation

5

| Issue | Goes to | When |
|---|---|---|
| Severity 1 | Application owner and SCB IT incident manager | At once |
| Missed restore time | Head of the Chief Debt Recovery Management Office | At the restore time |
| Data load late | Data steward, then the data lead | 07:00, then 09:00 |
| Agent behaving wrongly | Risk and model risk officer; autonomy level lowered | At once |

## Slide 6

Decision needed

6

|  | Decision | Answer used until decided |
|---|---|---|
| DL02 | Who the application owner is | The Tribe lead, with the ACE team as technical custodian |

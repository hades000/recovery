<!-- source: 11 Delivery and operations/Recovery Workbench Ways of Working and Governance v3.docx -->
<!-- converted: 2026-11-04 from DOCX -->

> **Source:** `11 Delivery and operations/Recovery Workbench Ways of Working and Governance v3.docx`  
> **Converted from:** DOCX

Recovery Workbench

Ways of working and governance

SCB Collections and Recovery. Henka Group, 28 October 2026

| Item | Detail |
|---|---|
| Document | Recovery Workbench ways of working and governance |
| Version | 2 |
| Date | 28 October 2026 |
| Prepared by | Henka Group |
| Applies to | The TechX recovery squads, Autonomous Ops, Enterprise AI, the ACE team for shared items, the product owner, the business lead and the sponsors |

# 1. Working rules

- No more than three planning or review meetings a week for a squad member, and none longer than 30 minutes

- The sponsor review and the steering committee look back at finished work and are outside that limit

- Work flows on a Kanban board with limits on work in progress per column and a written pull policy

- The monthly release is the only date the business sees. What slips moves to the next epic; the date does not move

- Planning happens daily at the board. There is no sprint commitment and no velocity target

# 2. The cadence

| When | Meeting | Length | Who attends | What it covers |
|---|---|---|---|---|
| Daily | Board review | 15 minutes, each morning | Each squad: tech lead, developers, analyst, QA | Blockers and the oldest item on the board. What is pulled next |
| Daily | Help needed | As raised, the same day | Product owner with the person blocked | Who removes each blocker and by when. A blocker needing the bank goes to its owner the same day |
| Weekly | Delivery review | 30 minutes | Product owner, tech leads, analysts, QA lead, ACE team | The four flow numbers, what broke between modules, changes to the definitions of ready and done |
| Weekly | Decision review | 30 minutes | Product owner with the owners of open decisions | Each open decision against its date. Overdue decisions go to the sponsor review or the steering committee |
| Weekly | Design review for the next epic | 30 minutes | Analysts, solution architect, business lead | Progress of the next epic's design, one epic ahead of the build |
| Weekly | Progress update | Written | Product owner to the business unit heads | Finished work, the next release, open decisions and risks |
| Two-weekly | Sponsor progress review | 45 minutes | Sponsors, product owner, business lead | A look back at finished work. No commitment is made |
| Monthly | Epic design sign-off | 45 minutes | Business lead, product owner, Risk where limits move | The next epic's design is signed before its build starts |
| Monthly | Release go decision | 30 minutes | Release owner in the ACE team, product owner, application owner | Go or no-go on the SIT and UAT exits. Flags stay off for work that is not ready |
| Monthly | Epic demo | 60 minutes | Squads, business users, sponsors | The released work, shown on the system |
| Monthly | Steering committee | 60 minutes | Sponsors, CTO delegate, product owner, Henka | Decisions above the project: scope, budget, overdue decisions, risks |

# 3. What each forum decides

| Forum | What it decides | Chair |
|---|---|---|
| Squad board review | What is pulled next, who helps whom | Tech lead |
| Delivery review | Changes to the board, the limits and the definitions of ready and done | Product owner |
| Decision review | Whether an overdue decision goes to the sponsor review or the steering committee | Product owner |
| Epic design sign-off | The next epic's design and scope | Business lead |
| Release go decision | Whether the release goes, and which flags stay off | Release owner, ACE team |
| Sponsor progress review | Priorities between the next epics' scope items | Sponsor |
| Steering committee | Scope, budget, decisions the project cannot take, risks | Sponsor |

# 4. How a decision is recorded

| Step | What happens |
|---|---|
| 1 Raise | Anyone raises a question the build cannot answer. The product owner adds it to the decision log with an ID |
| 2 Frame | The analyst writes the question, the options, a recommendation, what it blocks and what happens if it is late |
| 3 Assign | The product owner names one owner and a date needed. Decision owners are bank roles |
| 4 Build on the recommendation | The squads build on the recommended answer and mark it as an assumption in the story |
| 5 Decide | The owner decides within five working days of the date needed, or the decision goes to the next review |
| 6 Record | The decision moves to Decisions taken with the date, who took it and what it means for the build |
| 7 Apply | Documents and stories built on the assumption are updated. An architecture decision also gets a decision record |

The decision log holds every open decision with its question, options, recommendation, owner, date needed and what it blocks, and every decision taken. Its days-left column counts down to the date needed and shows an overdue decision in red.

# 5. Who holds which part

| Role | What they own |
|---|---|
| Product owner | Owns the backlog order, the decision log and the weekly reviews |
| Business lead | Owns the business design, UAT and the epic design sign-off |
| Solution architect | Owns the architecture, the decision records and the standards file with the tech leads |
| Tech leads | Own their module, its merges and its board |
| QA lead | Owns the definition of done, the test levels and the SIT exit |
| Release owner, ACE team | Owns the release decision for the shared ACE service |
| Application owner | Signs access reviews and accepts each release (DL02) |
| Decision owners | Answer the open decisions named to them by the date needed |

# 6. How an issue is escalated

| Issue | Goes to | Answered within |
|---|---|---|
| Within a squad | Tech lead | Same day |
| Between squads or with the ACE team | Tech leads together; the ACE team decides if they do not agree | Same day |
| Needs a bank answer | Decision owner, through the decision log | Five working days |
| Overdue decision or cross-unit issue | Sponsor progress review | Next review |
| Scope, budget or a decision above the project | Steering committee | Next meeting |

# 7. The measures read each week

| Measure | Definition |
|---|---|
| Cycle time | Working days from pulled to done, per story |
| Throughput | Stories done per week |
| Blocked time | Working days a story waits on something outside the squad |
| Work in progress | Stories in progress against the limit per column |
| Decisions overdue | Open decisions past their date |
| Defects found in UAT | Defects per release found after SIT |

If cycle time rises while throughput falls, the limits on work in progress are wrong and are changed at the next delivery review. Velocity is not used as a measure.

# 8. The board

| Column | A story enters when | Leaves when |
|---|---|---|
| Ready | It meets the definition of ready | A developer pulls it |
| Plan | A developer pulls it | The tech lead approves the plan |
| Build | The plan is approved | The pull request is opened with its tests |
| Review | The pull request is opened | The pipeline passes and the reviewer approves |
| Done | It meets the definition of done | The epic is released |

Each column carries a limit on work in progress set at the delivery review. A story that waits on something outside the squad is marked blocked, and its blocked time is counted.

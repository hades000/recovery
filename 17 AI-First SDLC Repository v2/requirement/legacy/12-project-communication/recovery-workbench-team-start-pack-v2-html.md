<!-- source: 12 Project communication/Recovery Workbench Team Start Pack v2.html -->
<!-- converted: 2026-11-16 from HTML -->

> **Source:** `12 Project communication/Recovery Workbench Team Start Pack v2.html`  
> **Converted from:** HTML

Recovery Workbench team start pack

The Recovery Workbench is the system that owns every recovery case from 90 days past due to close, for Mortgage, Hire Purchase and SSME. It is built as the recovery module of ACE, the bank's collection engine, so collection and recovery work in one application with one case view.

**From day 90 to close**One case per customer and product, with one owner, one clock and one history**Mortgage, Hire Purchase, SSME**Every route: restructure, settlement, deed in lieu, guarantee claim, litigation, asset disposal, debt sale and write-off**Built on ACE**One service, one repository and one front end, with data through COLLINS

## Where the work happens in ACE

| Module | Built by | What it holds |
|---|---|---|
| Common | ACE team | Sign-in and access checks, audit and PII logging, the shared case view, shared entities (customer, account, product, collateral, asset), shared tasks such as the restructure calculator, the notification path |
| Collection | Collection squad | Phone, field, FCR and restructure work, as split under DL14 |
| Recovery | TechX recovery squads | Recovery stages, tasks and screens, the rules component, the decision center and log, the document hub, the partner portal, the recovery data loads |

| Epic | Release | Status | Theme | What the business gets |
|---|---|---|---|---|
| E1 | 30 Nov 2026 | Confirmed | Foundation 1 | One case list for every account at 90 days past due or more, reconciled to the core bank. Documents found by case. Decision log store. Read-only case record view |
| E2 | 31 Dec 2026 | Confirmed | Foundation 2 | One owner and a timer on every case, full history on one screen, approval routing, litigation notices generated and approved, steering dashboard |
| E3 | 31 Jan 2027 | Proposed | Settle, deed in lieu, assets | Settlements and deeds in lieu end to end to booking. Asset record, floor price and listing on HOME.SCB |
| E4 | 28 Feb 2027 | Proposed | Route decision | The route recommended with reasons and approved within the delegation of authority for every new case. Guarantee and TCG claims. Auction rounds and RAMC transfer |
| E5 | 31 Mar 2027 | Proposed | Litigation | Litigation instructed and tracked end to end, law firms through the partner portal. Debt sale lot data and the buyer data room |
| E6 | 30 Apr 2027 | Proposed | Debt sale and write-off | Debt sale screens and award, write-off committee, partner panel, allocation and fees |
| E7 | 31 May 2027 | Proposed | Deviations and partners | Deviations X1 to X7 end to end. Partner scoring, conduct and the field app |
| E8 | 30 Jun 2027 | Proposed | Administration and hardening | Full administration, conduct checks, autonomy step-ups, regulatory returns, hardening |

## Release calendar

| Epic | Build starts | SIT | UAT | Release |
|---|---|---|---|---|
| E1 | 2 Nov | 16 Nov to 20 Nov | 23 Nov to 27 Nov | 30 Nov 2026 |
| E2 | 30 Nov | 14 Dec to 18 Dec | 21 Dec to 25 Dec | 31 Dec 2026 |
| E3 | 28 Dec | 11 Jan to 15 Jan | 18 Jan to 22 Jan | 31 Jan 2027 |
| E4 | 25 Jan | 8 Feb to 12 Feb | 15 Feb to 19 Feb | 28 Feb 2027 |
| E5 | 22 Feb | 8 Mar to 12 Mar | 15 Mar to 19 Mar | 31 Mar 2027 |
| E6 | 22 Mar | 5 Apr to 9 Apr | 12 Apr to 16 Apr | 30 Apr 2027 |
| E7 | 19 Apr | 3 May to 7 May | 10 May to 14 May | 31 May 2027 |
| E8 | 17 May | 31 May to 4 Jun | 7 Jun to 11 Jun | 30 Jun 2027 |

## Rules

|  | Rule |
|---|---|
| 1 | No more than three planning or review meetings a week for a squad member, and none longer than 30 minutes |
| 2 | The sponsor review and the steering committee look back at finished work and are outside that limit |
| 3 | Work flows on a Kanban board with limits on work in progress per column and a written pull policy |
| 4 | The monthly release is the only date the business sees. What slips moves to the next epic; the date does not move |
| 5 | Planning happens daily at the board. There is no sprint commitment and no velocity target |

## Rhythm

| Cadence | Forum | Length | Who | What it covers |
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

## Roles

| Role | Accountable for |
|---|---|
| Product owner | Owns the backlog order, the decision log and the weekly reviews |
| Business lead | Owns the business design, UAT and the epic design sign-off |
| Solution architect | Owns the architecture, the decision records and the standards file with the tech leads |
| Tech leads | Own their module, its merges and its board |
| QA lead | Owns the definition of done, the test levels and the SIT exit |
| Release owner, ACE team | Owns the release decision for the shared ACE service |
| Application owner | Signs access reviews and accepts each release (DL02) |
| Decision owners | Answer the open decisions named to them by the date needed |

## Decisions

| Step | What happens |
|---|---|
| 1 Raise | Anyone raises a question the build cannot answer. The product owner adds it to the decision log with an ID |
| 2 Frame | The analyst writes the question, the options, a recommendation, what it blocks and what happens if it is late |
| 3 Assign | The product owner names one owner and a date needed. Decision owners are bank roles |
| 4 Build on the recommendation | The squads build on the recommended answer and mark it as an assumption in the story |
| 5 Decide | The owner decides within five working days of the date needed, or the decision goes to the next review |
| 6 Record | The decision moves to Decisions taken with the date, who took it and what it means for the build |
| 7 Apply | Documents and stories built on the assumption are updated. An architecture decision also gets a decision record |

## Escalation

| Issue | Who resolves it | By when |
|---|---|---|
| Within a squad | Tech lead | Same day |
| Between squads or with the ACE team | Tech leads together; the ACE team decides if they do not agree | Same day |
| Needs a bank answer | Decision owner, through the decision log | Five working days |
| Overdue decision or cross-unit issue | Sponsor progress review | Next review |
| Scope, budget or a decision above the project | Steering committee | Next meeting |

| Role | 2 to 6 Nov | 9 to 13 Nov | 16 to 20 Nov | 23 to 27 Nov |
|---|---|---|---|---|
| Product owner | Confirm the backlog order; chase decisions due this week (DL04, DL05, DL13, DL24, DL32 to DL34, DL36) | Sponsor review on 13 Nov; Epic 2 design pack drafted | Epic 2 design signed by 20 Nov; SIT scope confirmed | UAT; go decision on 27 Nov; release on 29 Nov |
| Business analysts | Window 1 stories ready; rule rows with test case IDs | Window 2 stories ready; Epic 2 stories refined | Answer SIT questions; Epic 2 stories ready | UAT scripts walked through with the testers |
| Tech leads | Recovery module folder, boundary test and code owners (RWB-TE-001, RWB-TE-002); first items pulled | Board limits held; merges daily | Release scope closed; SIT defects triaged | Fixes for UAT; flags off for unfinished work |
| Developers | Access to DEV; schema and migrations (RWB-E1-001, RWB-E1-044); file adapter pattern | Case record, allocation, decision log writer, document store | Finish and fix in SIT | Fix UAT defects; nothing new merged into the release |
| QA engineers | Synthetic data (RWB-E1-065); rule table harness (RWB-TE-005) | Automated tests per story; contract tests | SIT for Epic 1 | UAT support; regression |
| Business testers | Named and given DEV access (DL09) | Test with the squads as stories finish | UAT scripts prepared | UAT and sign-off |
| Reference data administrator | First lists of values and queues loaded in DEV | Allocation table, roles and teams loaded | SIT loads checked | Production loads for the release |
| Data steward | COLLINS load checks agreed (DEP-14, DL25) | Daily reconciliation running in DEV | SIT loads reconciled | Production readiness of the loads |
| Release owner, ACE team | Deployment slots and the release window (DL34, DL35) | Common module services ready (DEP-04) | SIT environment and tag | Go decision on 27 Nov; release on 29 Nov |

| Key | Title | Module | Points | Depends on |
|---|---|---|---|---|
| RWB-E1-001 | Recovery tables for the 14 data products | P1 | 5 | RWB-E1-013 |
| RWB-E1-007 | Integration adapters for file loads and outbound files | P2 | 8 | RWB-E1-001, RWB-E1-004 |
| RWB-E1-008 | Decision log store v1, append only and hash chained | P7 | 8 | RWB-E1-001, RWB-E1-013 |
| RWB-E1-018 | Case ID issuance and case record v1 | P3 | 13 | RWB-E1-016, RWB-E1-012 |
| RWB-E1-019 | Roles, teams and queues as data | P3 | 5 | RWB-E1-012, RWB-E1-038 |
| RWB-E1-020 | Allocation and assignment engine v1 | P3 | 13 | RWB-E1-018, RWB-E1-019, RWB-E1-027, RWB-E1-056 |
| RWB-E1-022 | Sign-on with SSO, MFA and the first roles | P4 | 5 | RWB-E1-001 |
| RWB-E1-024 | Document store and index | P5 | 8 | RWB-E1-001, RWB-E1-027 |
| RWB-E1-027 | Decision log writer v1 | P7 | 3 | RWB-E1-056 |
| RWB-E1-043 | Reference data service with versioned tables | P3 | 8 | RWB-E1-011 |
| RWB-E1-044 | Database migrations versioned with parameterized schema names | P3 | 5 | RWB-E1-001 |
| RWB-E1-065 | Sandbox database with synthetic recovery data | P1 | 5 | RWB-E1-001 |

| Document | What it answers |
|---|---|
| Project deck | The full account: today, the target, the architecture, the data, the plan |
| Release plan | The eight releases, their content and the gates |
| Build sequence, Epic 1 and Epic 2 | The order work is pulled, with the critical path |
| User stories, Epic 1 and Epic 2 | Every story with criteria, data, endpoints and tests |
| Definition of ready and done | When a story may be pulled and when it is finished |
| Engineering practices | Branching, review, pipeline gates, flags and release |
| Logical data model and data dictionary | Every entity and field with its BR Field ID |
| API specification | Every endpoint with its access and errors |
| Business rules and routing logic | The 448 rules by route set |
| Error and message standard | Every message in English and Thai |
| Decision log | Open decisions, owners and dates |
| Ways of working and governance | Forums, cadence and escalation |

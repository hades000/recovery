<!-- working-copy-of: requirement/legacy/12-project-communication/recovery-workbench-project-overview-v4-docx.md -->
> **Working copy.** Canonical source: `requirement/legacy/12-project-communication/recovery-workbench-project-overview-v4-docx.md`. Edit the source, not this copy.

Recovery Workbench

Project overview

SCB Collections and Recovery. Henka Group, 28 October 2026

| Item | Detail |
|---|---|
| Document | Recovery Workbench project overview |
| Version | 3 |
| Date | 28 October 2026 |
| Prepared by | Henka Group |
| Reader | Anyone who needs to know what the Workbench is, why it is built, what changes and when, in ten minutes |

# 1. What the Recovery Workbench is

The Recovery Workbench is the system that owns every recovery case from 90 days past due to close, for Mortgage, Hire Purchase and SSME. It is built as the recovery module of ACE, the bank's collection engine, so collection and recovery work in one application with one case view.

| Scope | What it means |
|---|---|
| From day 90 to close | One case per customer and product, with one owner, one clock and one history |
| Mortgage, Hire Purchase, SSME | Every route: restructure, settlement, deed in lieu, guarantee claim, litigation, asset disposal, debt sale and write-off |
| Built on ACE | One service, one repository and one front end, with data through COLLINS |

# 2. The problem it solves

### Work is spread across systems

Collections and recovery staff use 42 applications. A case's facts are held in the core bank, EFS, LIT, CCMS, SVAF, AMIS and the document stores, and no screen shows them together.

### Cases are run from spreadsheets

Teams keep their own case lists in Excel and SharePoint, build account plans by hand and approve by email. Hand-overs between teams are manual.

### Decisions are not recorded in one place

Why a route was chosen, who approved it and on what figures is spread across emails and files. Audit findings and fraud cases number 50.

### Cases take too long

Turnaround is 21 days for litigation, 23 days for a restructure and 26 days for a deed in lieu. The NPA sales cycle is 1,486 days.

# 3. What changes

| Area | Today | With the Workbench |
|---|---|---|
| Case list | Each team's Excel and SharePoint list | One case list for every account at 90 days past due or more, reconciled to the core bank |
| Ownership | Agreed between teams by email | One owner per case by rule, with transfers recorded and a clock on every state |
| Choosing the route | Officer judgment, written up in an account plan | Expected return of each route from COLLINS, a recommendation with reasons, approved within the delegation of authority |
| Approvals | Email and paper | Routed to the right approval level, with the limit checked and the decision logged |
| Documents | Folders, shared drives and couriers | One document hub per case, with types read and fields extracted, and custody of originals tracked |
| Partners | Email and spreadsheets | Instructions, results and fees through a partner portal, with a scorecard per partner |
| Rules and limits | In procedures and people's heads | Versioned data rows, changed by a validated load without a code release |
| Evidence | Rebuilt for each audit | One decision log entry per decision, append only |

# 4. How a case moves from day 90 to close

A case passes through six stages. It can return to the route decision at any stage, on a cure, a payment, a deviation or an override.

| Stage | What it produces |
|---|---|
| Receive the case | One owner, the history from collections, running deadlines and a deviation screen |
| Choose the route | An approved route with the expected return of each option and the reasons |
| Resolve with the customer | A settlement, deed in lieu, guarantee claim or guarantor agreement, booked and reconciled |
| Enforce | A judgment enforced, a settlement before judgment, or proceeds matched to the case |
| Realize the asset | Cash from the asset or the debt: auction, RAMC, buy-back, rental or debt sale |
| Close | The balance written off and posted, recovery after charge-off, the case closed |

A deviation such as a complaint, a death, fraud or lost contact pauses the stage at any point and returns the case when it clears.

# 5. How decisions are made

Every decision follows five steps: gather and check the information, decide by a rule, a model or an agent, make the outcome final or send it to the approver, act in the systems, and log the decision once. The approver is set by the bank approval authority regulation and the delegation of authority table.

| Who carries out the step, from day 90 to close | L3 processes | Share |
|---|---|---|
| Automated | 38 | 52% |
| AI prepares, a person decides | 17 | 23% |
| A person decides | 7 | 10% |
| Partner | 9 | 12% |
| Manual | 2 | 3% |
| Total | 73 | 100% |

# 6. What it is built on

| Element | What it means |
|---|---|
| ACE | The Workbench is a module of ACE: one service, one repository, one front end. It reuses ACE sign-in, access control, audit and logging. |
| COLLINS | Account, customer, collections history, litigation status and scores arrive by daily batch through COLLINS. |
| Case model | Stages, milestones, tasks and timers in CMMN 1.1 terms, the standard shared with the collection module. |
| Rules as data | Every rule, limit, threshold, template, queue, role, timer and route is a versioned data row. |
| Decision log | Every decision is recorded once, with its inputs, the rule and model versions, the approver and the outcome. |
| AI agents | Agents prepare and recommend. They start in shadow, then recommend to a person, and move up only on evidence. |

# 7. The plan

Eight epics, one production release at each month end from November 2026 to June 2027. What slips moves to the next epic; the release date does not move.

| Epic | Release | Theme | What the business gets |
|---|---|---|---|
| E1 | 30 Nov 2026 | Foundation 1 | One case list for every account at 90 days past due or more, reconciled to the core bank. Documents found by case. Decision log store. Read-only case record view |
| E2 | 31 Dec 2026 | Foundation 2 | One owner and a timer on every case, full history on one screen, approval routing, litigation notices generated and approved, steering dashboard |
| E3 | 31 Jan 2027 | Settle, deed in lieu, assets | Settlements and deeds in lieu end to end to booking. Asset record, floor price and listing on HOME.SCB |
| E4 | 28 Feb 2027 | Route decision | The route recommended with reasons and approved within the delegation of authority for every new case. Guarantee and TCG claims. Auction rounds and RAMC transfer |
| E5 | 31 Mar 2027 | Litigation | Litigation instructed and tracked end to end, law firms through the partner portal. Debt sale lot data and the buyer data room |
| E6 | 30 Apr 2027 | Debt sale and write-off | Debt sale screens and award, write-off committee, partner panel, allocation and fees |
| E7 | 31 May 2027 | Deviations and partners | Deviations X1 to X7 end to end. Partner scoring, conduct and the field app |
| E8 | 30 Jun 2027 | Administration and hardening | Full administration, conduct checks, autonomy step-ups, regulatory returns, hardening |

# 8. The benefits

Each measure is taken from the decision log per decision, with the baseline set in Epic 1.

| Measure | Today | 2027 target |
|---|---|---|
| Recovery rate on NPL | 66.3% (2026 to date) | 73% |
| Litigation turnaround | 21 days | 6 days |
| Deed in lieu turnaround | 26 days | 12 days |
| Restructure turnaround | 23 days | 5 days |
| Debt sale turnaround | No baseline | 45 days |
| Manual processes removed | Near zero | 80% of the selected list |
| Audit findings and fraud cases | 50 | 13 |
| NPA sales cycle | 1,486 days | 1,095 days |

# 9. What the project needs from the bank

Each decision has a recommended answer. The build goes ahead on that answer until the bank decides.

| Decision | Decision log | Needed by |
|---|---|---|
| Who grants access and who owns the application | DL01, DL02 | 28 Oct |
| Which interfaces need real-time data | DL06 | 30 Oct |
| Coding tool and model endpoint for the build | DL32, DL33 | 30 Oct |
| Which legacy systems are kept | DL12 | 7 Nov |
| What counts as one case, and entry at 90 or 91 days | DL16, DL17 | 6 Nov |
| Service levels per case state, caseload caps | DL22, DL23 | 13 Nov |
| Delegation of authority: holders, limits and substitutes | DL18 | 30 Nov |

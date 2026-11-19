<!-- source: 02 Business architecture and process/Recovery Workbench Case and Workflow Model v5.html -->
<!-- converted: 2026-11-16 from HTML -->

> **Source:** `02 Business architecture and process/Recovery Workbench Case and Workflow Model v5.html`  
> **Converted from:** HTML

Recovery Workbench Case and Workflow Model

## The recovery case as a CMMN 1.1 model

Recovery is adaptive case management. The bank wants a milestone reached, such as a case cured, settled, sold or closed, and the officer chooses much of the path. The case holds stages, the stages hold tasks, and sentries decide when a task starts and when the case moves on. Each sentry is one routing rule, so the case model and the business rules are the same 448 rows.

**Stages**10**Milestones**30**Tasks**150**Event listeners**53**Sentries**448**Case file items**12

## Elements

| Element | Count | What it is |
|---|---|---|
| Case | 1 | The recovery case for one customer and one product, with the accounts linked, from day 90 to close. |
| Stage | 10 | A route the case can be on. Eight are entered when the route decision selects them; the deviation stage and the universal rules are always available. |
| Milestone | 30 | A state the case reaches and does not leave. It marks an achievement, not work. |
| Human task | 90 | Work a bank officer does. The case puts it in a queue or the officer picks it up. |
| Customer task | 6 | Work the customer, guarantor or heir does. The case waits on them. |
| Partner task | 22 | Work an outside party does, such as a law firm, agency, buyer or valuer. |
| Decision task | 22 | A point where a rule or an approver sets the route. The outcome selects the next sentry. |
| Stage entry | 10 | The task a stage starts from. One per stage. |
| Event listener | 53 | A task reached by an event rather than chosen, such as a declined approval or a blocked listing. |
| Sentry | 448 | One entry or exit criterion: the event it listens for, the condition that must hold, and the action it takes. Each sentry is one routing rule. |
| Case file item | 12 | Data the case holds. Sentries read it to test their conditions. |

## How a task starts

| Kind | Tasks | Meaning |
|---|---|---|
| Automatic | 46 | The Workbench starts the task. No person starts it. |
| Discretionary | 40 | A person chooses whether to start the task. It has more than one way out. |
| Required | 64 | The case puts the task in a queue for a named owner. The delegation of authority decides who. |

## Kinds of sentry

| Kind | Sentries | Meaning |
|---|---|---|
| User sentry | 137 | Fired by a person's action or decision. |
| Timer sentry | 269 | Carries a time limit; fires when the time is reached if nothing else has. |
| System sentry | 42 | Fired by the Workbench or another system, with no time limit. |

## Who owns the next state

| Owner | Sentries |
|---|---|
| Bank officer | 264 |
| Workbench | 91 |
| Partner | 50 |
| Approver | 31 |
| Customer | 12 |

## How the model runs

The case, its stages, tasks and milestones are rows in the Workbench database, moved by code in the recovery module of ACE. The condition and the action of each sentry are rows in a versioned table. A sentry change is a data load, and a case in flight keeps the version it entered the state under. Timers are stored due dates that the Workbench scheduler checks.

## Case status

Every case is in one status at a time. The status is one level above the route state and is what queues, service levels and reports read.

Each box is a status. A pale line returns the case to an earlier status.

| Status | Meaning | CMMN case state |
|---|---|---|
| New | Created at 90 days past due with its history. Not yet given an owner. | Active |
| Assigned | An owner and a queue are set by the allocation rules. The stage clock starts. | Active |
| In progress | The owner or the Workbench is working a task on the case. | Active |
| Waiting customer | An offer, notice or request is with the customer, with a validity timer running. | Active |
| Waiting partner | An instruction is with a partner, with a service level timer running. | Active |
| Waiting approval | A recommendation is with the approver set by the delegation of authority. | Active |
| On hold | A deviation or a legal hold has paused the case. The prescription clock keeps running. | Suspended |
| Closed | A milestone that closes the case is reached: cured, settled, sold, or written off with recovery ended. | Completed, then Closed |

## Status transitions

| From | Event | To |
|---|---|---|
| New | Allocation rule matched | Assigned |
| Assigned | Owner or Workbench starts the first task | In progress |
| In progress | Offer or notice sent to the customer | Waiting customer |
| In progress | Instruction sent to a partner | Waiting partner |
| In progress | Recommendation routed for approval | Waiting approval |
| Waiting customer | Customer responds, or the validity timer expires | In progress |
| Waiting partner | Partner result arrives, or the service level timer expires | In progress |
| Waiting approval | Approver accepts, changes or rejects, or the approval escalates | In progress |
| New, Assigned, In progress, any Waiting | Deviation flagged or legal hold placed | On hold |
| On hold | Deviation cleared or hold released | The status it paused in |
| In progress, Waiting customer, Waiting partner | A milestone that closes the case is reached | Closed |
| On hold | The deviation ends the case, for example insurance settles the debt | Closed |

## Stage map

The case is taken over and the route decision selects one of seven stages. A stage can end the case by itself, for example when a plan runs to term or a settlement clears, or pass what is left to write-off. A case can also move between stages, for example from litigation to asset disposal, through the route decision. The two outlined boxes are always available: a deviation can pause any active state, and the universal rules listen on every active state.

## Stages

| Stage | Kind | Entered when | Leaves when | Tasks and milestones | Sentries | Always available |
|---|---|---|---|---|---|---|
| Restructure, TDR | Solution stage | The route decision D6 approves a restructure, or D5 proposes one | Plan runs to term and the case closes; Plan breaks and the case returns to the route decision; Customer does not sign and the case returns to its prior status in COLLINS; A second break bars a further restructure | 18 | 37 | No |
| Settlement | Solution stage | The route decision D6 approves a settlement | Payment clears, the collateral is released and the case closes; The customer does not pay by the deadline and the case returns to the route decision; A payment reverses after release and the case re-opens | 15 | 27 | No |
| Deed in lieu and voluntary surrender | Solution stage | The route decision D6 approves a deed in lieu, or the customer offers the asset during a negotiation | The asset is on the books and hands off to the disposal route; The customer rents the asset back and the rental runs; The customer withdraws or the title is not clean and the case returns to the route decision | 20 | 37 | No |
| Litigation and enforcement, D7 | Enforcement stage | The route decision D6.3 approves litigation, or a broken treatment returns the case to the legal route | Debt satisfied and the case closes; Asset taken onto the books and handed to the disposal route; Judgment unenforceable or enforcement exhausted, and the case goes to write-off; Customer cures or settles, and the case returns to treatment | 38 | 79 | No |
| Guarantee claim, D6.5 and D6.6 | Recovery stage | A guarantee is detected on the case at takeover and the claim deadline timer starts | The claim is paid and the residual returns to the route decision; The claim is lost on the deadline and the full balance returns to the route decision; The guarantor settles and the case closes | 17 | 32 | No |
| Asset disposal, D8.1 to D8.3 | Recovery stage | An asset is taken onto the bank's books and the holding age clock starts | Sold, proceeds applied and the case closed with no shortfall; Sold with a residual, handed to debt sale or write-off; Transferred to RAMC or the joint venture; Rented, with the asset still held | 40 | 72 | No |
| Debt sale, D8.4 | Recovery stage | The monthly debt sale cycle opens, or a residual arrives from the disposal route | Lot awarded, settled, transferred and closed with realized recovery recorded; Lot withdrawn and the accounts returned to the case list; Put-back upheld and the account returned to the bank | 29 | 41 | No |
| Write off and recover after charge-off, D9 | Closure stage | The monthly eligibility scan runs on the cut-off date, or a residual arrives from another route | Posted, placed, recovered and closed after the retention period; Rejected by the committee and returned to the pursue track; Sold to a buyer as a charged-off population | 27 | 51 | No |
| Deviations X1 to X7 | Exception stage | The screening agent flags a deviation at entry or on a new document | The deviation clears and the case returns to the state it paused in; The deviation moves the case to a different route; The case ends, where insurance settles the debt | 9 | 22 | Yes |
| Universal rules, any state | Always on | The case is in any active state on any route | The case returns to the state it was in; The case moves to the route decision; The case closes; The case is canceled or merged | 20 | 50 | Yes |

## 30 milestones

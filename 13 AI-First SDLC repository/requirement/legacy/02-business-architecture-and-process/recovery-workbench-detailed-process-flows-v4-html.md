<!-- source: 02 Business architecture and process/Recovery Workbench Detailed Process Flows v4.html -->
<!-- converted: 2026-11-04 from HTML -->

> **Source:** `02 Business architecture and process/Recovery Workbench Detailed Process Flows v4.html`  
> **Converted from:** HTML

Recovery Workbench Detailed Process Flows

## How to read the flows

Each route set is drawn as one flow in BPMN 2.0 terms. Each lane is an actor or a system. Each step is a state in the routing rules; each line is one or more rules. The table under each flow names the rules that enter and leave each step.

**Flows**10**Steps**233**Rules**448**Branch points**118**End states**30**Exception events**53 Start event End event Gateway: a rule or an approver chooses System task User task Customer task Partner task Exception eventA dashed line returns the case to an earlier step.

## The flows

| Flow | Starts when | Steps | Rules | Branch points | End states | Exception events |
|---|---|---|---|---|---|---|
| Restructure, TDR | The route decision D6 approves a restructure, or D5 proposes one | 18 | 37 | 10 | 3 | 5 |
| Settlement | The route decision D6 approves a settlement | 15 | 27 | 7 | 2 | 4 |
| Deed in lieu and voluntary surrender | The route decision D6 approves a deed in lieu, or the customer offers the asset during a negotiation | 20 | 37 | 12 | 2 | 3 |
| Litigation and enforcement, D7 | The route decision D6.3 approves litigation, or a broken treatment returns the case to the legal route | 38 | 79 | 27 | 4 | 10 |
| Guarantee claim, D6.5 and D6.6 | A guarantee is detected on the case at takeover and the claim deadline timer starts | 17 | 32 | 12 | 2 | 6 |
| Asset disposal, D8.1 to D8.3 | An asset is taken onto the bank's books and the holding age clock starts | 40 | 72 | 20 | 4 | 7 |
| Debt sale, D8.4 | The monthly debt sale cycle opens, or a residual arrives from the disposal route | 29 | 41 | 12 | 2 | 7 |
| Write off and recover after charge-off, D9 | The monthly eligibility scan runs on the cut-off date, or a residual arrives from another route | 27 | 51 | 14 | 2 | 9 |
| Deviations X1 to X7 | The screening agent flags a deviation at entry or on a new document | 9 | 22 | 2 | 3 | 0 |
| Universal rules, any state | The case is in any active state on any route | 20 | 50 | 2 | 6 | 2 |

## The lanes

| Lane | Kind |
|---|---|
| Customer and guarantor | Actor |
| Case owner and the recovery team | Actor |
| Approvers and committees | Actor |
| Partners and external parties | Actor |
| The Workbench | Actor |
| Rules, workflow and agents | System |
| Bank systems of record | System |

## Restructure, TDR

All products. D5 runs on EFS and ACE until the TDR project is live, then on the Workbench.

**Starts when**The route decision D6 approves a restructure, or D5 proposes one**Ends**Plan runs to term and the case closes; Plan breaks and the case returns to the route decision; Customer does not sign and the case returns to its prior status in COLLINS; A second break bars a further restructure**Steps and rules**18 steps, 37 rules Start event End event Gateway: a rule or an approver chooses System task User task Customer task Partner task Exception eventA dashed line returns the case to an earlier step.

### Steps

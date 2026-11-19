<!-- source: 02 Business architecture and process/Recovery Workbench Business Rules and Routing Logic v4.html -->
<!-- converted: 2026-11-16 from HTML -->

> **Source:** `02 Business architecture and process/Recovery Workbench Business Rules and Routing Logic v4.html`  
> **Converted from:** HTML

Recovery Workbench Business Rules and Routing Logic

## How a case is routed

Every move a case makes is one rule. When an event arrives at a case in a given state and the condition holds, the Workbench takes the action, moves the case to the next state, gives it to the named owner and starts the timer. There are 448 rules in ten route sets.

**Rules**448**Route sets**10**Rules with a timer**252 of 448**Rules whose next state a person or partner owns**366 of 448

## The decision table

Each route set is one decision table in Decision Model and Notation 1.4.

| Column | Kind | Meaning |
|---|---|---|
| Rule | Identifier | R, the route set code and a number, for example R-LIT-12 |
| From state | Input | The state the case is in when the event arrives |
| Event | Input | What happened: a payment, a document, a decision, a date reached, a partner result |
| Condition | Input | What must hold for the rule to fire. Any means the event alone fires it |
| Action | Output | What the Workbench does |
| To state | Output | The state the case moves to |
| Owner | Output | Who holds the case in the next state. Workbench means no person |
| Systems | Output | The systems the action reads or writes |
| Timer | Output | How long the next state may last before it escalates |

**Hit policy: Unique**In a route set, for one state and one event, at most one condition holds, so one rule fires.

## Rules held as data

Every rule is a row in a versioned table, with its rule ID, version, valid from, valid to, author, approver and test case ID. A rule change is a validated data load, not a code release. A case keeps the rule version it was decided under, and the decision log records the rule ID and version for every move.

## The route sets

| Route set | Decision | Rules | States | End states | With a timer | Owned by a person or partner |
|---|---|---|---|---|---|---|
| Restructure, TDR | D5, D6 | 37 | 18 | 3 | 15 | 30 |
| Settlement | D6.4 | 27 | 15 | 2 | 12 | 20 |
| Deed in lieu and voluntary surrender | D6.4 | 37 | 20 | 2 | 15 | 28 |
| Guarantee claim, D6.5 and D6.6 | D6.5, D6.6 | 32 | 17 | 2 | 21 | 24 |
| Litigation and enforcement, D7 | D7 | 79 | 38 | 4 | 62 | 65 |
| Asset disposal, D8.1 to D8.3 | D8.1 to D8.3 | 72 | 40 | 4 | 31 | 60 |
| Debt sale, D8.4 | D8.4 | 41 | 29 | 2 | 15 | 33 |
| Write off and recover after charge-off, D9 | D9 | 51 | 27 | 2 | 31 | 43 |
| Deviations X1 to X7 | X1 to X7 | 22 | 9 | 3 | 6 | 19 |
| Universal rules, any state | All | 50 | 15 | 6 | 44 | 44 |
| Total |  | 448 | 228 | 30 | 252 | 366 |

## What decides the route

| Test | What it decides |
|---|---|
| Product | Mortgage, hire purchase or SSME. The product decides which routes are open at all. |
| Days past due and exposure | Which band the case falls in, and therefore who owns it and what they may approve. |
| Security | Whether the bank holds an asset, a guarantee or nothing. |
| Hard gates | A death, fraud, bankruptcy, a complaint or a legal hold stops the normal route and sends the case to a deviation owner first. |

## The eight routes

| Route | Chosen when | How it runs |
|---|---|---|
| Restructure | The customer can pay, but needs longer terms. | COLLINS proposes, FCR builds the offer. |
| Settlement | The customer can pay a reduced amount now. | Priced against the payoff floor. |
| Deed in lieu | The customer will hand over the asset instead of paying. | Valued, consented, transferred at the Land Office. |
| Guarantee claim | A guarantor or an insurer covers part or all of it. | Claim filed with TCG or the insurer. |
| Litigation | No engagement, or the amount justifies court. | Notices, then a panel law firm, then judgment. |
| Asset disposal | The bank already holds the asset. | Listed and run down the price ladder. |
| Debt sale | The account is worth more sold than worked. | Built into a lot and awarded to a buyer. |
| Write off | Nothing is left to recover economically. | Proposed monthly, approved, posted. |

## How a case ends

| End | What happens |
|---|---|
| Cured or settled | The customer pays, a plan runs to term, or a settlement clears. |
| Realized | An asset sells, a guarantee pays, or the debt is sold. |
| Written off | Posted and closed, with recovery continuing after charge-off. |

## Routes by product

| Product | Routes open | Where the volume goes |
|---|---|---|
| Mortgage | Restructure, settlement, deed in lieu, litigation, asset disposal, debt sale, write off | Deed in lieu and asset disposal carry the volume. The Land Office transfer and the LED auction ladder are the long steps. |
| Hire purchase | Restructure, settlement, voluntary surrender, litigation, asset disposal, debt sale, write off | Voluntary surrender replaces deed in lieu. The asset moves faster and the auction cycle is shorter. |
| SSME | Restructure, settlement, guarantee claim, litigation, asset disposal, debt sale, write off | The guarantee claim route matters here because of TCG cover. Deed in lieu applies only where there is property security. |
| Unsecured | Settlement, litigation, debt sale, write off | No asset, so no disposal and no deed in lieu. Most volume ends in debt sale or write off. |

A deviation stops the normal route at any point and returns the case when it clears. The universal rules run in every state.

## Restructure, TDR

All products. D5 runs on EFS and ACE until the TDR project is live, then on the Workbench.

**Starts when**The route decision D6 approves a restructure, or D5 proposes one**Ends when**Plan runs to term and the case closes; Plan breaks and the case returns to the route decision; Customer does not sign and the case returns to its prior status in COLLINS; A second break bars a further restructure**Decision**D5, D6**Rules**37

### Flow

Start: where the route begins System step: the Workbench or another system acts Officer step: a bank officer acts Decision point: a rule or an approver chooses Customer step: the customer acts Partner step: a partner acts Exception: reached by an event End state: the route ends hereA pale line returns the case to an earlier state. A dashed line is a return that needs no rule.

### Decision table

<!-- source: 05 Technical architecture/Recovery Workbench Rules Engine Design v2.docx -->
<!-- converted: 2026-11-16 from DOCX -->

> **Source:** `05 Technical architecture/Recovery Workbench Rules Engine Design v2.docx`  
> **Converted from:** DOCX

Recovery Workbench

Rules engine design

SCB Collections and Recovery. Henka Group, 28 October 2026

| Item | Detail |
|---|---|
| Document | Recovery Workbench rules engine design |
| Version | 1 |
| Date | 28 October 2026 |
| Prepared by | Henka Group |
| Structure | Decision Model and Notation 1.4 decision tables, arc42 crosscutting concepts |

# 1. The design on one page

| Element | Design |
|---|---|
| What it is | A decision table evaluator inside the recovery module of ACE. No external rules engine |
| What it holds | 448 routing rules in ten route sets, the allocation table, thresholds, limits and timers, all as versioned data rows |
| Table form | DMN 1.4 decision tables: inputs, conditions, output, hit policy FIRST in row order |
| Authoring | Rule rows prepared in a workbook by the center of excellence, loaded as a file through the validated load |
| Testing | Every row names its test case. The rule table harness runs every row before a version can be approved |
| Approval | The process owner approves; Risk approves where a limit or threshold moves |
| Deployment | A version takes effect from its valid from date. No code release |
| Rollback | The previous version is loaded again with an immediate date |
| Record | Every evaluation that changes a case writes the rule ID, the version and the inputs to the decision log |

# 2. Route sets

| Route set | Rules | Decision |
|---|---|---|
| Restructure | 37 | D5, D6 |
| Settlement | 27 | D6.4 |
| Deed in lieu | 37 | D6.4 |
| Guarantee claim | 32 | D6.5, D6.6 |
| Litigation | 79 | D7 |
| Asset disposal | 72 | D8.1 to D8.3 |
| Debt sale | 41 | D8.4 |
| Write-off | 51 | D9 |
| Deviations | 22 | X1 to X7 |
| Universal rules | 50 | All |
| Total | 448 |  |

# 3. The structure of a rule row

| Column | Meaning | Example |
|---|---|---|
| Rule ID | Unique, never reused | R-SET-05 |
| Route set | The stage the rule belongs to | SETTLEMENT |
| From state | The case state the rule listens in, or ANY_ACTIVE | OFFER_PREPARED |
| Event | The event that fires the rule | OFFER_PREPARED |
| Condition | A FEEL expression over case file items; blank means any | offer_amount < floor_amount |
| Action | What the Workbench does | Route the offer to the approver with the gap to the floor |
| To state | The state the case moves to | AWAITING_APPROVAL |
| Owner | Who owns the next state | Approver by delegation of authority |
| Timer | The clock the next state carries, from the service level table | 5 working days |
| Test case ID | The test the row must pass | TC-R-SET-05 |
| Valid from and to | When the row applies | 30 Nov 2026 |
| Version | The route set version the row belongs to | SETTLEMENT-2026.11 |

# 4. How a rule is evaluated

- An event reaches a case: a load, a screen action, a partner result, a timer or another module.

- The evaluator reads the version of the route set in force for the case. A case keeps the version it was decided under (R-UNI-38).

- It selects the rows whose from state matches the case state, or ANY_ACTIVE, and whose event matches.

- It tests the conditions in row order. The first row that holds fires (hit policy FIRST).

- If no row holds, the case goes to the exception queue and the gap is logged (R-UNI-41).

- The decision log entry is written first. If the write fails, nothing changes (R-UNI-39).

- The action runs: the state moves, tasks and timers are set, outbound work goes to the outbox.

# 5. Authoring and change

| Step | Who | What happens |
|---|---|---|
| Prepare | Center of excellence analyst | Writes or changes rows in the route set workbook, with a test case per row |
| Load | Reference data administrator | Loads the file; structure, references, states and lists are checked; a failed check refuses the file whole |
| Test | Rule table harness | Runs every row against its test case in SIT and attaches the result to the version |
| Review | Process owner | Reads the change report: rows added, changed and removed, with the test result |
| Approve | Process owner; Risk where a limit moves | Approves with a valid from date. The maker cannot approve |
| In force | Workbench | New decisions use the version from its date; decided cases keep their version |
| Roll back | Reference data administrator with the owner | Loads the previous version with an immediate date |

# 6. Checks every version passes

- Every rule has a unique ID.

- Every from state and to state exists in the route set.

- Every state that is not an end state has a rule out.

- No two rules share the same from state, event and condition.

- Every rule names its owner and its action.

- Every route set has at least one end state.

- Every row has a test case and the test passes.

# 7. Performance

| Item | Target |
|---|---|
| One evaluation | Under 300 milliseconds at the 95th percentile (NFR-011, proposed under DL11) |
| Evaluations a month | About 12 for each open case, about 320,000 a month by the end of 2027 |
| Caching | The route set version in force is cached in memory and refreshed when a version takes effect |

# 8. Open decisions

| Decision | What is needed | Answer used until decided |
|---|---|---|
| DL22 | Service levels per case state | Placeholders loaded; escalation from the day values are supplied |
| DL23 | Caseload caps and queue rules | Placeholders loaded |
| DL24 | Which rules are loaded in Epic 1 | Allocation, transfer, timers and the universal rules |

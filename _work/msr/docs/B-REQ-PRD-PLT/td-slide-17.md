
S1 · Valuation and route

Choose one of eight recovery routes using the expected return of each, with a person's approval

Starts when  the case reaches route decision D6, or it is reopened (ROUTE_D6_REOPEN)

1

Order appraisal if stale

FEAT-VAL-01 · SVAF

2

Read value, flag outliers

VAL-02, VAL-03

3

Case owner accepts value

VAL-04

4

Return by route, payoff

VAL-05, VAL-06 · COLLINS, ALS

5

Route agent recommends

VAL-07 · EV-28

6

Approve: limit or committee

VAL-08, VAL-09 · EV-09

7

Start route R1–R8 + timers

VAL-12 · ROUTE_APPROVED

Runs in
rwb-valuation
RouteDecisionWorkflow

System step

Timer

Signal / event

Drools decision

Person

External system

AI agent

Drools decides

No S1 package yet (Phase 2)
Re-decide if band, value or class changes
Agent too slow (60 s) → rule decides (R-UNI-32)

Who approves

Case owner within delegated authority
Credit approval committee above it

Clocks

Appraisal stale after 12 months
Hold with a review date (VAL-10)

Point of no return / undo

ROUTE_APPROVED starts R-RES-01, R-SET-01 or R-DIL-01
Reopen needs written rule + approver (R-UNI-50)

S1 is mostly people and data; Temporal holds the case while it waits for the appraisal and the approval.

17

Notes: Source: FSD S1 Valuation and route v3; Case Journeys v3; Routing Logic v4. In v5, RouteDecisionWorkflow runs in rwb-valuation; the approval is ApprovalWorkflow from the workflow kit on rwb-decision (DoA routing); RouteDecided goes to rwb-case. Decision D6. Re-decision triggers: R-UNI-02, 14, 22, 37, 41, 45, 50 and R-DEV-19. Approval within limit or at committee (VAL-08, VAL-09, EV-09); hold with review date (VAL-10); route flow and timers start in the same step (VAL-12, REQ-S1-007); re-decide when band, value or class changes (REQ-S1-008).

Open point: route numbering conflicts between documents (R-LIT-01 starts litigation on route = R4; Case Journeys v3 calls R4 the guarantee claim and R5 litigation).



Use case: a restructured mortgage misses a payment

Real example from story RWB-E2-008  ·  who decides (Drools), who waits (Temporal), who acts

9

Notes: Case RC-2026-000555, account A-0555, plan T-0701: 12,500 THB a month, 3 of 24 installments paid, next due 15 Dec 2026.
1. Plan booked: R-RES-25 starts the monthly clock (PLAN_RUNNING).
2. 16 Dec morning: AceDataReady starts payment matching in rwb-payment (JOB-07); PAYMENT_MATCH EXACT finds no payment in the 10-day window. rwb-payment publishes PaymentMissed (EV-12) to Kafka; the case router in rwb-case signals the CaseWorkflow, which passes it to TreatmentWorkflow in rwb-treatment. The case owner sees it the same morning.
3. R-RES-27 starts the cure period: 30 calendar days for MORTGAGE (CURE_PERIOD_DAYS). The Temporal timer waits through restarts and releases; a customer payment ends the wait early.
4. 15 Jan: R-RES-28 accepts a late payment (plan continues); otherwise R-RES-29 marks the plan broken and R-RES-30 sends it back to the route decision, with a case owner task due in 5 working days. On the 2nd break R-RES-31 bars a further restructure (restructure.max_breaks = 2).

Sources: RWB-E2-008, FSD S2, Epic 2 build notes. Simplification: the missed payment is found by payment matching in rwb-payment (JOB-07, after the ACE batch), not by the timer itself. Every rule answer is written as a decision record with the state change, then sealed in the central ledger in rwb-decision (v5).


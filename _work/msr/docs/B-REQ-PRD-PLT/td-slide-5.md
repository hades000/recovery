
The nine recovery scenarios, S1 to S9

In every scenario Temporal runs the clock and Drools makes the calls

S1  Valuation & route

Orders appraisal, waits for approval

Re-decide if value changes

S2  Restructure, settle, deed

14-day offer, plan timers

Missed payment → cure

S3  Guarantee claims

Claim deadline timer

Missed deadline = lost claim

S4  Litigation

Notices, court dates, years

Pick law firm; auction steps

S5  Assets & auction

Holding age, 5-day payment

> THB 50m → sealed bids

S6  Debt sale

Monthly sale cycle

Award within reserve and cap

S7  Write-off

Monthly scan, posting

Open deviation → excluded

S8  Deviations X1–X7

Pause stage clock

Route to the right owner

S9  Partners

Partner SLA, chase, recall

Scorecard picks partner

Nine different journeys, one pattern: event in, rule decides, person signs, timer waits.

5

Notes: Sources: FSD S1 to S9 v3 and Business Rules and Routing Logic v4 (448 rules in 10 route sets: RES 37, SET 27, DIL 37, GUA 32, LIT 79, DIS 72, DS 41, WO 51, DEV 22, UNI 50). Only RESTRUCTURE, PAYMENT_MATCH and BOOKING_MATCH (S2) are named Drools packages in Phase 1; the other route sets become packages in Phase 2 (Epics 3 to 7). The UNIVERSAL package (R-UNI-01 to 50) arrives in Epic 3.


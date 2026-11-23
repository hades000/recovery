
Example: litigation runs for years without anyone holding a spreadsheet

Temporal keeps the dates; Drools decides at each fork

Notice sent
WIN dispatch

Notice period
starts on proof of delivery

Law firm chosen
by rule, instructed

Court
filing, hearings, judgment

Asset trace
10 working days, writ

Auction
steps 100→90→80→70%

AUCTION LADDER  (R-LIT-63 to 67)

100%

round 1

90%

round 2

80%

round 3

70%

round 4

PRESCRIPTION CLOCK  (a legal deadline: never paused)

15 Mar 2026
last payment

17 Sep 2027
warning → review

15 Mar 2028
prescription

Temporal timer fires the warning automatically; Drools escalates when 90 days or less remain.

Key

Temporal waits

Drools decides

Court / people

A timer set today can fire in 2028, after many releases and restarts, and still be on time.

7

Notes: S4 Litigation (79 rules). Notices are generated (R-LIT-03) and dispatched via WIN (JOB-10, EV-14). Proof of delivery (EV-15) starts the notice-period timer (R-LIT-07); the proof window is 7 days. The panel firm is selected by rule and instructed (R-LIT-23/24, EV-20). Filing, hearings and judgment arrive as signals (EV-21). Enforcement: asset trace (10 working days), writ, then the LED auction ladder 100/90/80/70% (R-LIT-63 to 67). Proceeds are matched (EV-25).

Prescription: last payment 15 Mar 2026 → prescription date 15 Mar 2028, warning 17 Sep 2027 (FSD P3 AC-ALT-P3-011); 90 days or less escalates (R-LIT-11/20); R-UNI-31 forces a litigation review. A second deferral with no asset goes to write-off (R-LIT-57).


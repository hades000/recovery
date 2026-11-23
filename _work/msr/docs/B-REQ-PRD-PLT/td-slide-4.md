
One case, start to finish

A mortgage case that ends in a settlement  ·  built from the FSD worked examples

Case created
90 days past due → ENTRY rule; active plans excluded

1

Drools

Officer assigned
ALLOC-014 → queue MTG-BKK-CO, fewest cases

2

Drools

SLA timer
Warn day 7, breach day 8 → team manager

3

Temporal

Route approved
Settlement; THB 2.4m, 20% loss → L6 signs

4

People

Payment due
Waits up to 30 days for the money

5

Temporal

Case closed
Paid, debt released, logged

6

Close

Day 0

≈ 2 months

Prescription clock runs the whole time and never pauses  ·  Temporal timer: warning 6 months before the legal deadline

Key

Drools decides

Temporal waits / reminds

A person approves

Drools makes the calls, Temporal keeps the time, people sign off, and every step is on record.

4

Notes: Built from FSD worked examples: entry (P3 AC-P3-004: account at 90 DPD becomes a case; an account with an active TDR plan is excluded under EXCL-2026.11 with reason ACTIVE_PLAN); allocation (P3 AC-P3-007: MORTGAGE in BKK matches ALLOC-014 → queue MTG-BKK-CO; the officer with the fewest cases gets it); SLA timer (P3 AC-ALT-P3-011: assigned 1 Dec, warns 8 Dec, breach 9 Dec → RW-TEAMMGR under R-UNI-30); settlement approval (P7 AC-ALT-P7-015: principal THB 2.4m at 20% loss → L6 under DOA-2026.11); settlement payment due in 30 days (R-SET-13); prescription (last payment 15 Mar 2026 → prescription 15 Mar 2028, warning 17 Sep 2027).

The prescription clock is a legal deadline and is never paused, even during a deviation (R-DEV-01).


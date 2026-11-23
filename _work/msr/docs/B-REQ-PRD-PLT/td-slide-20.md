
S4 · Litigation and enforcement

Take a case from notice to judgment and enforcement, over months or years

Starts when  litigation route approved (R-LIT-01), or a restructure or settlement plan breaks (R-LIT-02)

1

Notices generated, sent

R-LIT-03 · JOB-10 · EV-13/14

2

Notice period on delivery

EV-15 · R-LIT-07

3

Pack checked for defects

R-LIT-16

4

Law firm chosen, instructed

R-LIT-23/24 · EV-20

5

Filing, hearings, judgment

EV-21 · R-LIT-30/33/44

6

Asset trace, writ, 10 wd

R-LIT-50

7

Auction 100/90/80/70%

R-LIT-63 to 67 · EV-25

Runs in
rwb-litigation
LitigationWorkflow

System step

Timer

Signal / event

Drools decision

Person

External system

AI agent

Drools decides

Litigation route set, 79 rules (package Phase 2)
≤ 90 days to prescription → escalate (R-LIT-11/20)
2nd deferral, no asset → write-off (R-LIT-57)

Who approves

Settlement, appeal, fees at D7.4
Delay of action: L6 ≤ THB 100m, once

Clocks

Prescription: never paused
Proof window 7 days · trace 10 wd

Point of no return / undo

Settlement holds litigation (R-LIT-37)
Broken settlement resumes it (R-LIT-40)

S4 is the longest journey: court dates arrive as signals, and the prescription timer runs for years.

20

Notes: Source: FSD S4 Litigation and enforcement v3; Routing Logic v4 (R-LIT, 79 rules). Today filing takes 21 days and packs are incomplete. Petition at D7.5 (R-LIT-58). A second delay of legal action goes one level up.


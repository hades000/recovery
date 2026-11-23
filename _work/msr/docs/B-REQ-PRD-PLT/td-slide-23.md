
S7 · Write-off and recovery

Monthly write-off scan, committee, posting, and recovery after charge-off

Starts when  JOB-16 runs on the 3rd working day after EV-26 AceDataReady (R-WO-01)

1

Scan proposes population

R-WO-01/03

2

Pack built in 3 wd

R-WO-05

3

Committee decides

R-WO-11 to 17

4

Post to ALS / GL

R-WO-21 · EV-24

5

Release provision, feed

R-WO-25/26

6

Agency or sale after

R-WO-29/30/32

7

Retention, then close

R-WO-47 · JOB-17

Runs in
rwb-writeoff
WriteOffWorkflow

System step

Timer

Signal / event

Drools decision

Person

External system

AI agent

Drools decides

Write-off route set, 51 rules (package Phase 2)
Open deviation → case removed (R-WO-06)
Approved must equal posted (R-WO-42/43)

Who approves

Meets MR/BOT criteria: L4–L6
Else PARC ≤ THB 100m, ExCo ≤ 1,000m
Related parties: the Board

Clocks

Monthly cut-off, month-end close
Defer sets a review timer (R-WO-17)

Point of no return / undo

Posting is the point of no return
On failure: re-post, rescan or committee

S7 is batch-shaped: a schedule starts it, Drools selects the population, Temporal retries the posting.

23

Notes: Source: FSD S7 Write-off and recovery v3; Routing Logic v4 (R-WO, 51 rules). Scan holds if tax criteria are missing (R-WO-03). Recovery of written-off debt (2.1.11): L6 up to 50m and at least 15%. Posting failure: re-post, return to scan, or refer to committee (R-WO-44/45/46). In v5 JOB-16 is a Temporal Schedule in rwb-writeoff (monthly, 3rd working day); there are no shared Quartz tables. Today's Phase 1 note (T2) keeps it on Quartz, so this is listed as an open point. Write-off posting waits for the central ledger to confirm the decision record (strict mode).


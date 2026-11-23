
S6 · Debt sale

Sell lots of accounts to qualified buyers, inside the 54% cap

Starts when  the monthly sale cycle opens, or a residual arrives from disposal (R-DS-01)

1

Select accounts

R-DS-01/02

2

Lot priced, committee 5 wd

R-DS-04 · COLLINS

3

Masked tape, data room

R-DS-10/13

4

Buyer KYC, licence, 3 wd

R-DS-14

5

Award vs reserve and cap

R-DS-19/23 · EV-23

6

Settle, transfer, post GL

R-DS-25 to 31

7

Sold: close the case

R-UNI-47

Runs in
rwb-debtsale
DebtSaleWorkflow

System step

Timer

Signal / event

Drools decision

Person

External system

AI agent

Drools decides

Debt sale route set, 41 rules (package Phase 2)
Open deviation → account excluded (R-DS-02)
EV-23 stops every open action (R-UNI-47)

Who approves

Secured: PARC if ≥ 40% FMV, else ExCo
Unsecured: PARC if ≥ 10% principal, else ExCo

Clocks

Monthly cycle
Put-back review and remediation 10 wd

Point of no return / undo

Transfer and derecognition are the pivot
Upheld put-back reverses it (R-DS-36/37)

S6 spans many cases at once; one sale event closes every case in the lot through a universal rule.

22

Notes: Source: FSD S6 Debt sale v3; Routing Logic v4 (R-DS, 41 rules). Today sales run on spreadsheets. Buyer remediation 10 working days (R-DS-40). In v5 DebtSaleWorkflow in rwb-debtsale runs this as a saga with the kit's Saga runner, across five services: reserve accounts (rwb-debtsale), approve sale (rwb-decision), buyer pays (rwb-payment) can be undone; then transfer accounts, post proceeds, close cases (rwb-case), tell customers (rwb-comms) are retried until done. The transfer waits for the central ledger to confirm the decision record (strict mode).


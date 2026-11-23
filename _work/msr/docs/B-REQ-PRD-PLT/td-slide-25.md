
S9 · Partner management

Give work to law firms, auction vendors, agencies and valuers by measured return; pay and recall them

Starts when  a case needs a law firm, auction vendor, collection agency or valuer

1

Onboard partner, terms

FEAT-PRM-01

2

Scorecard picks partner

FEAT-PRM-03

3

Instruction sent

EV-20 · partner clock

4

Result via portal

EV-21 · same day

5

No reply: chase, recall

R-UNI-25 · R-UNI-45

6

Fees approved

FEAT-PRM-09

7

Monthly scorecard, exit

R-UNI-26

Runs in
rwb-partner
kit: Partner instruction

System step

Timer

Signal / event

Drools decision

Person

External system

AI agent

Drools decides

UNIVERSAL package (Epic 3)
Conduct breach suspends allocation (R-UNI-29)
Insolvency stops fees (R-UNI-28)

Who approves

Partner manager: overrides need a reason
Fee approval

Clocks

Partner SLA by type
Recall 5 wd · re-select 2 wd

Point of no return / undo

Exit recalls all open cases (R-UNI-26)

S9 turns partner SLAs into timers: no reply means an automatic chase, then a recall.

25

Notes: Source: FSD S9 Partner management v3; Routing Logic v4 (R-UNI-25 to 29, R-UNI-45; R-LIT-24 to 29; R-DIS-30/31; R-WO-30 to 35). Today partner work runs on email and spreadsheets. Vendor allocation 2 working days.



S2 · Restructure, settlement and deed in lieu

Take an offer from proposal to booking, then watch the payment plan

Starts when  ROUTE_APPROVED with route R1 (restructure), R2 (settlement) or R3 (deed in lieu)

1

COLLINS proposal

R-RES-01

2

FCR officer review, 2 wd

R-RES-02, R-RES-04

3

ACE affordability check

R-RES-06

4

Offer sent, valid 14 days

R-RES-09

5

Customer signs, ops books

R-RES-16/21/22 · EV-11

6

Payment plan timers

R-RES-25

7

Missed payment → cure

EV-12 · R-RES-27

Runs in
rwb-treatment
TreatmentWorkflow

System step

Timer

Signal / event

Drools decision

Person

External system

AI agent

Drools decides

RESTRUCTURE: breaks vs max_breaks (R-RES-30/31)
PAYMENT_MATCH: EXACT, PARTIAL, WINDOW
BOOKING_MATCH: booking confirmed
Settlement below floor → approval (R-SET-05)

Who approves

DoA 2.1.1: L6 ≤ THB 100m, 30% loss
L5 ≤ 150m · L4 ≤ 300m · L3 PARC ≤ 1,500m
Deed below floor: Head of NPA (R-DIL-15)

Clocks

Offer 14 days · settlement pay 30 days
Credit approval 3 working days

Point of no return / undo

ALS/NLEADS booking; collateral release (R-SET-21)
Payment reversal reopens case (R-SET-23/24)

S2 already has three Drools packages in Phase 1; the workflow mostly waits on offers, signatures and payments.

18

Notes: Source: FSD S2 TDR, settlement and deed in lieu v3; Routing Logic v4 (R-RES 37, R-SET 27, R-DIL 37 rules). Today these take 23-26 days and are tracked by hand; 44% of TDR cases deviate (R-RES-10).

RESTRUCTURE package: R-RES-25/27/29/30/31 and R-LIT-02; a break below max_breaks returns to D6; at or above it R1 is barred (R-RES-30/31/32). PAYMENT_MATCH replaces payment_match_rule (T10). Deed in lieu auto-unlock passes about 95% of cases (R-DIL-23).

DoA 2.1.1 max loss: L6 30% / 50m; L5 35% / 75m; L4 45% / 150m; L3 PARC 45% / 750m.


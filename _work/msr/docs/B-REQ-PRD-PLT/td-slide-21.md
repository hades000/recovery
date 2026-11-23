
S5 · Assets and auction

Take on, hold, price and sell repossessed assets (today the NPA sales cycle is 1,486 days)

Starts when  an asset is taken on from repossession, deed in lieu or LED (R-DIS-01/02/03, EV-22)

1

Holding age, provisions

R-DIS-06/09

2

Re-appraise at 12 months

R-DIS-15 · JOB-19

3

Pricing agent recommends

R-DIS-19/20

4

Floor approved, listed

R-DIS-29/33 · HOME.SCB

5

Rounds step to floor

R-DIS-38 · R-DIS-41

6

Buyer pays in 5 days

R-DIS-47

7

Title transfer, proceeds

R-DIS-51/52/54

Runs in
rwb-asset
AssetDisposalWorkflow

System step

Timer

Signal / event

Drools decision

Person

External system

AI agent

Drools decides

Disposal route set, 72 rules (package Phase 2)
> THB 50m → sealed bids at committee (R-DIS-22)
Bid below floor → second signature (R-DIS-41)
Re-list limit reached → debt sale (R-DIS-46)

Who approves

L5 ≤ THB 20m at ≥ 70% FMV
PARC ≤ 200m at ≥ 70% · MC ≤ 500m at ≥ 60%

Clocks

Payment 5 calendar days
Title transfer 10 working days

Point of no return / undo

Non-payment cancels award, reopens round
Title transfer is final (R-DIS-51/52)

S5 is a loop of timed auction rounds; Drools sets each price step, Temporal runs each round.

21

Notes: Source: FSD S5 Assets and auction v3; Routing Logic v4 (R-DIS, 72 rules). Shortfall goes to D9 or debt sale (R-DIS-54/55). Non-payment cancels the award and reopens the round (R-DIS-49/50). Sale approvals per DoA 3.2.1 (L5 max loss 3m).


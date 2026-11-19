<!-- working-copy-of: requirement/legacy/02-business-architecture-and-process/recovery-workbench-case-journeys-v3-pptx.md -->
> **Working copy.** Canonical source: `requirement/legacy/02-business-architecture-and-process/recovery-workbench-case-journeys-v3-pptx.md`. Edit the source, not this copy.

## Slide 1

SCB

COLLECTIONS AND RECOVERY TRANSFORMATION Recovery Workbench: case journeys

Henka Group, 28 October 2026 (C) Siam Commercial Bank and Henka Pte Ltd

## Slide 2

Eight routes from day 90 to close

2

|  | Route | Chosen when | How it runs |
|---|---|---|---|
| R1 | Restructure | The customer can pay, but needs longer terms. | COLLINS proposes, FCR builds the offer. |
| R2 | Settlement | The customer can pay a reduced amount now. | Priced against the payoff floor. |
| R3 | Deed in lieu | The customer will hand over the asset instead of paying. | Valued, consented, transferred at the Land Office. |
| R4 | Guarantee claim | A guarantor or an insurer covers part or all of it. | Claim filed with TCG or the insurer. |
| R5 | Litigation | No engagement, or the amount justifies court. | Notices, then a panel law firm, then judgment. |
| R6 | Asset disposal | The bank already holds the asset. | Listed and run down the price ladder. |
| R7 | Debt sale | The account is worth more sold than worked. | Built into a lot and awarded to a buyer. |
| R8 | Write off | Nothing is left to recover economically. | Proposed monthly, approved, posted. |

| A case ends | What happens |
|---|---|
| Cured or settled | The customer pays, a plan runs to term, or a settlement clears |
| Realized | An asset sells, a guarantee pays, or the debt is sold |
| Written off | Posted and closed, with recovery continuing after charge-off |

## Slide 3

What decides the route

3

The route is recommended with the expected return of each option from COLLINS, and approved within the delegation of authority. A case can return to the route decision at any stage: on a cure, a payment, a deviation or an override.

| Test | What it decides |
|---|---|
| Product | Mortgage, hire purchase or SSME. The product decides which routes are open at all. |
| Days past due and exposure | Which band the case falls in, and therefore who owns it and what they may approve. |
| Security | Whether the bank holds an asset, a guarantee or nothing. |
| Hard gates | A death, fraud, bankruptcy, a complaint or a legal hold stops the normal route and sends the case to a deviation owner first. |

## Slide 4

R1 Restructure

4

The customer can pay something, over a longer term. What happens?

1  The system proposes it COLLINS raises a restructure on the case after the route decision approves it. Workbench

2  It reaches the restructuring officer Into the FCR queue, with the plan calculated in ACE. Restructuring officer, FCR

3  The officer builds and sends the offer Inside the band, with affordability recorded. Exceptions only reach a person. Restructuring officer

4  The customer decides Not a routed state. A wait, with a validity timer running on it. Customer

5  Signed goes to Operations The signed agreement is booked and the plan starts. Operations, booking

6  Not signed goes back The case returns to the route decision. Case owner

| How the case can end |
|---|
| Plan runs to term and the case closes |
| Plan breaks and the case returns to the route decision |
| Customer does not sign and the case returns to the route decision |

| In the routing rules |  |
|---|---|
| Steps | 18 |
| Rules | 37 |
| Branch points | 10 |
| Exception events | 5 |

## Slide 5

R2 Settlement

5

The customer can pay a reduced amount now. What happens?

1  The route decision approves a settlement The case carries a payoff figure and a floor. Workbench

2  The officer prices it Against the floor. Below the floor needs a second signature. Case owner

3  The offer goes to the customer A wait, with a validity timer. Customer

4  Accepted, then paid In full, or on an agreed installment plan. Customer

5  Paid in full closes the case The balance clears and the case closes. Case owner

6  Not paid returns it Back to the route decision for another route. Case owner

| How the case can end |
|---|
| Settled in full and the case closes |
| Not paid and the case returns to the route decision |

| In the routing rules |  |
|---|---|
| Steps | 15 |
| Rules | 27 |
| Branch points | 7 |
| Exception events | 4 |

## Slide 6

R3 Deed in lieu

6

The customer will hand over the asset instead of paying. What happens?

1  The route decision approves deed in lieu Mortgage takes deed in lieu, hire purchase takes voluntary surrender. Workbench

2  The asset is valued and checked Valuation and a legal check on title and encumbrance. Valuer, Legal

3  Offer and consent from the customer The customer agrees to transfer. A wait, with a timer. Customer

4  Signed, then transferred Registered at the Land Office, or the vehicle handed over. Land Office

5  The asset comes onto the books And the case moves to disposal. NPA and asset manager

6  Declined returns it Back to the route decision. Case owner

| How the case can end |
|---|
| The asset transfers and the case moves to disposal |
| The customer declines and the case returns to the route decision |

| In the routing rules |  |
|---|---|
| Steps | 20 |
| Rules | 37 |
| Branch points | 12 |
| Exception events | 3 |

## Slide 7

R4 Guarantee claim

7

A guarantor or an insurer covers part or all of it. What happens?

1  A guarantee is identified on the case TCG cover, credit life, or a personal guarantee. Workbench

2  The claim is prepared Against that guarantor's own rules and deadlines. Guarantee officer

3  Filed with TCG or the insurer Inside the claim window, which is deadline driven. TCG, insurer

4  Paid, and subrogation recorded The balance reduces by the amount paid. Guarantee officer

5  A shortfall goes back Whatever is left returns to the route decision. Case owner

| How the case can end |
|---|
| The guarantee clears the balance and the case closes |
| Part paid, and the shortfall returns to the route decision |
| Declined, and the case returns to the route decision |

| In the routing rules |  |
|---|---|
| Steps | 17 |
| Rules | 32 |
| Branch points | 12 |
| Exception events | 6 |

## Slide 8

R5 Litigation

8

There is no engagement, or the amount justifies court. What happens?

1  Notices go out by rule Demand and recall notices from Legal templates. Workbench

2  The notice period runs From proof of delivery, not from the print date. Customer

3  The pack is assembled By the legal document agent, against the defect list. Workbench

4  The officer verifies and approves filing First time right is the measure that matters here. Litigation officer

5  A panel firm is instructed Selected on the scorecard, with the conflict check run. Panel law firm

6  Filed, then managed to judgment Court state and hearing dates reported back to the case. Court

7  Judgment, then enforcement Or a coded deferral with its reason. Enforcement owner

| How the case can end |
|---|
| Judgment and enforcement convert to cash |
| A coded deferral, with a reason and a review date |
| The debt is written off after enforcement is exhausted |

| In the routing rules |  |
|---|---|
| Steps | 38 |
| Rules | 79 |
| Branch points | 27 |
| Exception events | 10 |

## Slide 9

R6 Asset disposal

9

The bank holds the asset. How is it turned into cash?

1  The asset comes onto the books From a deed in lieu, a surrender, or an enforcement seizure. NPA and asset manager

2  Valued and held With holding cost, insurance and maintenance tracked against it. NPA and asset manager

3  The disposal route is approved One of five routes, approved inside the floor. Sale officer

4  Listed and run down the ladder The LED ladder steps at 100, 90, 80 and 70 percent of official value. Auction vendor

5  Sold, and the proceeds posted Price achieved recorded against the model and the floor. Sale officer

6  Any shortfall goes back To the route decision, usually toward write off. Case owner

| How the case can end |
|---|
| The asset sells and the proceeds are posted |
| The asset transfers to RAMC |
| A shortfall returns to the route decision |

| In the routing rules |  |
|---|---|
| Steps | 40 |
| Rules | 72 |
| Branch points | 20 |
| Exception events | 7 |

## Slide 10

R7 Debt sale

10

The account is worth more sold than worked. What happens?

1  Accounts are selected into a lot By the lot agent, against the sale policy and the 54 percent cap. Debt sale officer

2  A reserve is set from the model And approved by the Head of Asset Liquidity. Head of Asset Liquidity

3  Buyers qualify and view the data room KYC and license checks first, then access. Debt buyer

4  Bids come in and the lot is awarded To the highest qualifying bid above the reserve. Debt sale officer

5  Data transfers, remittance confirmed The buyer confirms receipt of the file and the money arrives. Debt buyer

6  The accounts close as sold Every open action on them stops. Debt sale officer

| How the case can end |
|---|
| The lot is awarded and the accounts close as sold |
| No qualifying bid, and the accounts return to the case list |

| In the routing rules |  |
|---|---|
| Steps | 29 |
| Rules | 41 |
| Branch points | 12 |
| Exception events | 7 |

## Slide 11

R8 Write-off

11

Nothing is left to recover economically. What happens?

1  The monthly scan proposes a population On both tracks, with the provision carried on each account. Write-off team

2  The pack goes to the committee With the provision position and the recovery history. Write-off team

3  Approved inside the delegation Anything outside it goes up a level. Write-off committee

4  Posted, provision released And completeness published. Credit Administration

5  Recovery continues after charge-off By agency placement, or by a post charge-off sale. Collection agency

6  Recovered or sold, then closed Whatever comes in is matched back to the written off account. Credit Administration

| How the case can end |
|---|
| Posted and closed |
| Recovered after charge-off |
| Sold after charge-off |

| In the routing rules |  |
|---|---|
| Steps | 27 |
| Rules | 51 |
| Branch points | 14 |
| Exception events | 9 |

## Slide 12

Deviations X1 to X7

12

Something happened that stops the normal route. What happens?

1  A deviation is flagged X1 to X7: complaint, hardship, death, fraud, bankruptcy, no contact, collateral. Workbench

2  The stage clock pauses The prescription clock keeps running. Workbench

3  It routes to the named owner Complaint officer, specialist, fraud team or Legal. Deviation owner

4  Resolved, and the case resumes In the state it paused in, with the clock restarted. Case owner

5  Or the outcome changes the route Back to the route decision, with the segment recomputed. Case owner

| How the case can end |
|---|
| The deviation clears and the case resumes where it paused |
| The outcome moves the case to a different route |
| Insurance settles the debt and the case ends |

| In the routing rules |  |
|---|---|
| Steps | 9 |
| Rules | 22 |
| Branch points | 2 |
| Exception events | 0 |

## Slide 13

Rules that apply on every route

13

Something happens that is true whatever route the case is on. What happens?

1  An event arrives A payment, a death, a complaint, a partner failure, a system outage, a sold lot. Workbench

2  The universal rules fire first They outrank the route's own rules, so a cure or a hold always wins. Workbench

3  One of four things happens The case pauses, is reallocated, returns to the route decision, or closes. Workbench

4  Paused cases resume In the state they paused in, with the timers recomputed. Case owner

5  Or the segment is recomputed And the gates re-run, which may change the route. Workbench

| How the case can end |
|---|
| The case returns to the state it was in |
| The case moves to the route decision |
| The case closes |
| The case is canceled or merged |

| In the routing rules |  |
|---|---|
| Steps | 20 |
| Rules | 50 |
| Branch points | 2 |
| Exception events | 2 |

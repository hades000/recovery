<!-- source: 02 Business architecture and process/Recovery Workbench Partner Operating Model v2.pptx -->
<!-- converted: 2026-11-04 from PPTX -->

> **Source:** `02 Business architecture and process/Recovery Workbench Partner Operating Model v2.pptx`  
> **Converted from:** PPTX

## Slide 1

SCB

COLLECTIONS AND RECOVERY TRANSFORMATION Recovery Workbench: partner operating model

Henka Group, 28 October 2026 (C) Siam Commercial Bank and Henka Pte Ltd

## Slide 2

The partners

2

| Partner | How many | Owner in the bank | How work is placed |
|---|---|---|---|
| Collection agencies | 73 | Partner and agency manager | Placement share set by measured return on a matched population |
| Law firms | 11 to 12 | Head of Litigation | By rule from the panel scorecard (R-LIT-23) |
| Valuers | Panel | Head of NPA | Appraisal orders through SVAF by rotation and region |
| Vehicle auction vendors | 4 | Head of Auto Recovery | By distance and the scorecard |
| Property brokers | Panel | Head of NPA | Fixed-term instruction on the portal |
| Debt buyers and AMCs | 35 | Head of Asset Liquidity | Lots offered to eligible buyers; award by price against the reserve |
| RAMC | 1 | Head of Asset Liquidity | Secured pools transferred on agreed terms |

## Slide 3

One lifecycle for every partner

3

Select

Contract

Place

Instruct

Track

Pay

Measure

Exit

| Step | What happens | Who |
|---|---|---|
| Select | Panel criteria, due diligence, security review, conduct check | Partner and agency manager with Procurement |
| Contract | Fees, service levels, data protection terms, audit rights, exit terms | Partner and agency manager with Legal |
| Place | Work placed by rule; shares and caps as reference data | Rules component |
| Instruct | Instruction with documents and due date through the partner portal | Case owner; Workbench |
| Track | Partner results, documents and service level clocks | Workbench; partner |
| Pay | Invoice against completed instructions; fee checked against the schedule | Partner and agency manager; Finance |
| Measure | Monthly scorecard; quarterly review | Partner and agency manager |
| Exit | Recall open work, secure documents and cash, end access (R-UNI-26, R-UNI-28) | Partner and agency manager |

## Slide 4

How partners are paid and measured

4

| Partner | Paid by | Measured on |
|---|---|---|
| Collection agencies | Fee on cash collected | Cash collected, cost per baht, conduct breaches, complaints |
| Law firms | Fee schedule per legal step | Time to file, time to judgment, recovery, court fees recovered |
| Valuers | Fee per appraisal | Turnaround, value against the sale price, outlier rate |
| Vehicle auction vendors | Commission on sale | Sell rate, price against the model, days to sell |
| Property brokers | Commission on sale | Days to sell, price against the floor |
| Debt buyers and AMCs | Purchase price | Price against the reserve, put-backs, complaints after transfer |
| RAMC | Transfer price from the governed template | Transfer time, pool performance |

## Slide 5

How partners reach the bank

5

| Item | Design |
|---|---|
| Today | LIT lawyer web, the OA portal, SVAF, HOME.SCB, email and SFTP |
| Target | The partner portal in the Workbench, through the external gateway, once the architecture team approves external access (DL03) |
| Identity | Partner identities separate from bank identities, with multi-factor authentication |
| Scope | Each user sees only the work placed with their firm |
| Until external access | Partners keep their current channels; bank staff record results in the Workbench |

## Slide 6

When each partner joins the portal

6

| Partner | Epic | What they do in the portal |
|---|---|---|
| Collection agencies | E6 | Collect |
| Law firms | E5 | File suit, enforce |
| Valuers | E4 | Appraise |
| Vehicle auction vendors | E4 | List, sell |
| Property brokers | E4 | Sell |
| Debt buyers and AMCs | E5 | Bid, buy |
| RAMC | E4 | Take transfer |

## Slide 7

Controls on partners

7

|  | Control | What it checks |
|---|---|---|
| CTL-31 | Debt sale data tape masking | The data tape passes the masking check before the data room opens |
| CTL-32 | Buyer eligibility | Only buyers who pass KYC, licensing and eligibility and sign the non-disclosure agreement reach the data room |
| CTL-35 | Partner allocation by performance | Work goes to partners by the scorecard and the panel rules, not by hand |
| CTL-36 | Partner progress and court fee recovery | Every partner instruction has a service level; court fees due back are tracked to receipt |
| CTL-37 | Partner security and conduct | Partners meet the bank's security and conduct requirements; a breach suspends allocation and recalls work |

## Slide 8

Decision needed

8

|  | Decision | Answer used until decided |
|---|---|---|
| DL03 | Who makes the architecture change for external partner access, and when | Partners stay on their current channels |

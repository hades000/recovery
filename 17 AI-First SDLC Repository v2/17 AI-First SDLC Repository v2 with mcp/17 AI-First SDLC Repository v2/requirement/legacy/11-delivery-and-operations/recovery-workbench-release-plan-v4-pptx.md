<!-- source: 11 Delivery and operations/Recovery Workbench Release Plan v4.pptx -->
<!-- converted: 2026-11-16 from PPTX -->

> **Source:** `11 Delivery and operations/Recovery Workbench Release Plan v4.pptx`  
> **Converted from:** PPTX

## Slide 1

SCB

COLLECTIONS AND RECOVERY TRANSFORMATION Recovery Workbench: release plan

Henka Group, 15 November 2026 (C) Siam Commercial Bank and Henka Pte Ltd

## Slide 2

Eight releases from November 2026 to June 2027

2

E1 30 Nov 2026 Foundation 1

E2 31 Dec 2026 Foundation 2

E3 31 Jan 2027 Settle, deed in lieu, assets

E4 28 Feb 2027 Route decision

E5 31 Mar 2027 Litigation

E6 30 Apr 2027 Debt sale and write-off

E7 31 May 2027 Deviations and partners

E8 30 Jun 2027 Administration and hardening

| Epic | Status | What the business gets |
|---|---|---|
| E1 | Confirmed | One case list for every account at 90 days past due or more, reconciled to the ACE account view. Documents found by case. Decision log store. Read-only case record view |
| E2 | Confirmed | One owner and a timer on every case, full history on one screen, approval routing, litigation notices generated and approved, steering dashboard |
| E3 | Proposed | Settlements and deeds in lieu end to end to booking. Asset record, floor price and listing on HOME.SCB |
| E4 | Proposed | The route recommended with reasons and approved within the delegation of authority for every new case. Guarantee and TCG claims. Auction rounds and RAMC transfer |
| E5 | Proposed | Litigation instructed and tracked end to end, law firms through the partner portal. Debt sale lot data and the buyer data room |
| E6 | Proposed | Debt sale screens and award, write-off committee, partner panel, allocation and fees |
| E7 | Proposed | Deviations X1 to X7 end to end. Partner scoring, conduct and the field app |
| E8 | Proposed | Full administration, conduct checks, autonomy step-ups, regulatory returns, hardening |

## Slide 3

What each release contains

3

| Epic | Release | Modules and content |
|---|---|---|
| E1 | 30 Nov | P1 recovery data engine over the 30 read-only recovery.v_ace_* views (RWB-E1-069); P3 case record, state model and rules component with allocation rules; P4 sign-in and roles; P5 document store and OCR; P6 notice generation; P7 decision log store; P9 baseline; P10 agent runtime in shadow |
| E2 | 31 Dec | P3 queue and transfer screens; P4 partner identities; P5 document generation; P6 dispatch and proof of delivery; P7 approval routing; P8 matching skeleton; P9 steering dashboard; S2 treatment record; S4 notice approval; S8 deviation screening |
| E3 | 31 Jan | S2 settlement and deed in lieu to booking; S5 asset record, floor price and listing; P7 decision center |
| E4 | 28 Feb | S1 route decision with COLLINS and the route agent; S3 guarantee and TCG claims; S5 auction rounds and RAMC; P6 customer self-service; P8 posting |
| E5 | 31 Mar | S4 litigation end to end with law firms through the partner portal; S6 lot data and data room |
| E6 | 30 Apr | S6 debt sale screens and award; S7 write-off and committee; S9 partner panel, allocation and fees |
| E7 | 31 May | S8 deviations end to end; S9 partner scoring, conduct and the field app |
| E8 | 30 Jun | P4 full administration; conduct checks; autonomy step-ups; regulatory returns; hardening |

## Slide 4

How a month runs

4

Design signed Ten days before the build starts, in parallel with the epic before

Build Continuous, behind flags, with business testers in the squads

SIT One week against the SCB test systems

UAT One week on the business scripts

Go decision Friday before the release

Release Month end, shared with the collection squad

| Epic | Design signed | Build starts | SIT | UAT | Go decision | Release |
|---|---|---|---|---|---|---|
| E1 | 23 Oct | 2 Nov | 16 Nov to 20 Nov | 23 Nov to 27 Nov | 27 Nov | 30 Nov 2026 |
| E2 | 20 Nov | 30 Nov | 14 Dec to 18 Dec | 21 Dec to 25 Dec | 25 Dec | 31 Dec 2026 |
| E3 | 18 Dec | 28 Dec | 11 Jan to 15 Jan | 18 Jan to 22 Jan | 22 Jan | 31 Jan 2027 |
| E4 | 15 Jan | 25 Jan | 8 Feb to 12 Feb | 15 Feb to 19 Feb | 19 Feb | 28 Feb 2027 |
| E5 | 12 Feb | 22 Feb | 8 Mar to 12 Mar | 15 Mar to 19 Mar | 19 Mar | 31 Mar 2027 |
| E6 | 12 Mar | 22 Mar | 5 Apr to 9 Apr | 12 Apr to 16 Apr | 16 Apr | 30 Apr 2027 |
| E7 | 9 Apr | 19 Apr | 3 May to 7 May | 10 May to 14 May | 14 May | 31 May 2027 |
| E8 | 7 May | 17 May | 31 May to 4 Jun | 7 Jun to 11 Jun | 11 Jun | 30 Jun 2027 |

## Slide 5

Gates between releases

5

|  | Gate | When | Criteria | Who decides |
|---|---|---|---|---|
| G1 | Design signed | Ten days before the epic starts | The epic's features, screens and rules are signed by the business lead; Epics 3 to 8 sign in parallel with the build of the epic before (DT05) | Product owner with the business lead |
| G2 | Ready to pull | Before a story is pulled | Each story meets the definition of ready | Product owner |
| G3 | SIT exit | End of the SIT week | Every test case for the release passes in SIT; no open severity 1 or 2 defect | QA lead with SCB IT |
| G4 | UAT exit | End of the UAT week | The business scripts for the release are signed | Business lead |
| G5 | Go decision | Friday before the release | SIT and UAT exits met; unfinished work behind a flag that is off; rollback tested | Release owner in the ACE team with the product owner and the application owner |
| G6 | Benefit check | Four weeks after the release | The measures the release was meant to move are read from the decision log and the reports | Product owner with the product heads |

## Slide 6

When each module is delivered

6

|  | Platform module | Delivered in |
|---|---|---|
| P1 | Recovery data engine | E1 |
| P2 | Integration | E1 |
| P3 | Case and workflow | E1 core, E2 screens |
| P4 | Access and administration | E1; E2 partners; E8 full administration |
| P5 | Document hub | E1 store and OCR; E2 generation |
| P6 | Communications | E1 notices; E2 dispatch; E4 self-service |
| P7 | Decision center and log | E1 log; E2 routing; E3 center |
| P8 | Payments and posting | E2 matching; E4 |
| P9 | Reporting | E1 baseline; E2 dashboard |
| P10 | Agent runtime | E1 shadow; E2 L1 |

|  | Stage module | Delivered in |
|---|---|---|
| S1 | Valuation and route | E4 |
| S2 | TDR, settlement and deed in lieu | E2 foundations; E3 |
| S3 | Guarantees and guarantors | E4 |
| S4 | Litigation and enforcement | E2 notices; E5 |
| S5 | Assets and auction | E3; E4 |
| S6 | Debt sale | E5 data; E6 screens |
| S7 | Write-off and recovery | E6 |
| S8 | Deviation handling | E2 screening; E7 |
| S9 | Partner management | E6 panel; E7 scoring |

## Slide 7

Who starts working in the Workbench at each release

7

| Epic | Release | Roles that receive real users |
|---|---|---|
| E1 | 30 Nov | Center of excellence analyst, Data steward and data product owner, Internal audit, Compliance and PDPA officer, Platform administrator, Reference data administrator, Security administrator |
| E2 | 31 Dec | Case owner, Team manager, Phone collector, Litigation officer, Capacity and workforce planner, Product head (Mortgage, HP, SSME), Head of Litigation, Risk and model risk officer, Reporting and BI analyst, Tribe lead and squad members |
| E3 | 31 Jan | Restructuring officer (FCR), Legal counsel, Sale officer, NPA and asset manager, Credit Administration officer, Head of NPA |
| E4 | 28 Feb | Guarantee officer, Credit approval committee member, Valuer, Auction vendor, RAMC user |
| E5 | 31 Mar | Enforcement owner, Law firm user, Debt buyer and AMC |
| E6 | 30 Apr | Debt sale officer, Write-off team member, Partner and agency manager, Head of Asset Liquidity, Write-off committee member, Finance and CFO delegate, Collection agency (OA) user |
| E7 | 31 May | Field collector, Hardship and vulnerability specialist, Complaint officer, Fraud investigator |
| E8 | 30 Jun | Conduct and QA officer |

## Slide 8

Dependencies that set the dates

8

| Dependency | Epic | Needed by | On | If late |
|---|---|---|---|---|
| ACE DB additions for the Workbench: 14 tables, 12 columns and the read grant (RWB-ACE-001) | E1 | 21 Nov | ACE team (DL43) | RWB-E1-069 has only the Section A views; the case list and the release move |
| Recovery module folder, package and boundary test in the ACE repository | E1 | 2 Nov | ACE team (DL05) | The squads cannot merge into ACE |
| TDR and DIL split between the collection squad, the Enterprise AI team and TechX | E3 | 15 Dec | Collection squad (DL14) | Epic 3 has no confirmed builder |
| Partner access from outside the bank through the external gateway | E5 | 1 Feb | Architecture team (DL03) | Law firms cannot use the partner portal at Epic 5 |
| Model endpoint the agents call, inside the SCB tenant | E1 | 6 Nov | Architecture team (DL33) | The agent runtime cannot run in shadow |
| ACE ingestion of account, payment, customer and score data, complete for the business date | E1 | 9 Nov | Data engineering (DL06, DL20) | No case can be opened from bank data |
| Entra ID groups for the Workbench roles in each environment | E1 | 9 Nov | SCB IT security (DL40) | No one can sign in to SIT or UAT |
| Route return models by route for the route decision | E4 | 25 Jan | Enterprise AI team | The route decision runs on rules only |
| Delegation of authority: holders, limits and substitutes | E2 | 30 Nov | Business (DL18) | Approval routing uses provisional limits |
| Letter templates approved by Legal in Thai and English | E2 | 13 Nov | Business (DL28) | Notices cannot be generated |

## Slide 9

Calendar risks

9

The release window for every month is agreed with SCB IT under DL34.

| Epic | Release | Note |
|---|---|---|
| E1 | 30 Nov | RWB-ACE-001 (ACE team, DL43) is due 21 November and gates RWB-E1-069; a late ACE delivery moves the case list and the release |
| E3 | 31 Jan | The New Year holidays (31 Dec and 1 Jan) fall in the first week of the build |
| E5 | 31 Mar | Law firms reach the partner portal from outside the bank; the external access change must be live (DL03) |
| E6 | 30 Apr | Chakri Day (6 Apr) and Songkran (13 to 15 Apr) fall in the SIT and UAT weeks; the release date is confirmed under DL34 |

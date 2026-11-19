<!-- source: 11 Delivery and operations/Recovery Workbench Release Plan v3.xlsx -->
<!-- converted: 2026-11-04 from XLSX -->

> **Source:** `11 Delivery and operations/Recovery Workbench Release Plan v3.xlsx`  
> **Converted from:** XLSX

## Releases

| Eight monthly releases |  |  |  |  |  |  |  |  |  |  |  |  |  |  |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| One production release at each month end, shared with the collection squad. Epics 1 and 2 are confirmed; Epics 3 to 8 are proposed and confirmed one month ahead. |  |  |  |  |  |  |  |  |  |  |  |  |  |  |
| Epic | Theme | Status | Design signed by | Build starts | SIT week from | UAT week from | Go decision | Release | Modules and content | What the business gets | Features | Stories | Roles that receive real users | Calendar and dependency notes |
| E1 | Foundation 1 | Confirmed | 46318 | 46328 | 46342 | 46349 | 46353 | 46356 | P1 loads and checks for COLLINS, CCMS and SVAF; P3 case record, state model and rules component with allocation rules; P4 sign-in and roles; P5 document store and OCR; P6 notice generation; P7 decision log store; P9 baseline; P10 agent runtime in shadow | One case list for every account at 90 days past due or more, reconciled to the core bank. Documents found by case. Decision log store. Read-only case record view | 118 | 67 | Center of excellence analyst, Data steward and data product owner, Internal audit, Compliance and PDPA officer, Platform administrator, Reference data administrator, Security administrator | None |
| E2 | Foundation 2 | Confirmed | 46346 | 46356 | 46370 | 46377 | 46381 | 46387 | P3 queue and transfer screens; P4 partner identities; P5 document generation; P6 dispatch and proof of delivery; P7 approval routing; P8 matching skeleton; P9 steering dashboard; S2 treatment record; S4 notice approval; S8 deviation screening | One owner and a timer on every case, full history on one screen, approval routing, litigation notices generated and approved, steering dashboard | 77 | 32 | Case owner, Team manager, Phone collector, Litigation officer, Capacity and workforce planner, Product head (Mortgage, HP, SSME), Head of Litigation, Risk and model risk officer, Reporting and BI analyst, Tribe lead and squad members | None |
| E3 | Settle, deed in lieu, assets | Proposed | 46374 | 46384 | 46398 | 46405 | 46409 | 46418 | S2 settlement and deed in lieu to booking; S5 asset record, floor price and listing; P7 decision center | Settlements and deeds in lieu end to end to booking. Asset record, floor price and listing on HOME.SCB | 31 | Specified at architecture level (DT13) | Restructuring officer (FCR), Legal counsel, Sale officer, NPA and asset manager, Credit Administration officer, Head of NPA | The New Year holidays (31 Dec and 1 Jan) fall in the first week of the build |
| E4 | Route decision | Proposed | 46402 | 46412 | 46426 | 46433 | 46437 | 46446 | S1 route decision with COLLINS and the route agent; S3 guarantee and TCG claims; S5 auction rounds and RAMC; P6 customer self-service; P8 posting | The route recommended with reasons and approved within the delegation of authority for every new case. Guarantee and TCG claims. Auction rounds and RAMC transfer | 50 | Specified at architecture level (DT13) | Guarantee officer, Credit approval committee member, Valuer, Auction vendor, RAMC user | None |
| E5 | Litigation | Proposed | 46430 | 46440 | 46454 | 46461 | 46465 | 46477 | S4 litigation end to end with law firms through the partner portal; S6 lot data and data room | Litigation instructed and tracked end to end, law firms through the partner portal. Debt sale lot data and the buyer data room | 26 | Specified at architecture level (DT13) | Enforcement owner, Law firm user, Debt buyer and AMC | Law firms reach the partner portal from outside the bank; the external access change must be live (DL03) |
| E6 | Debt sale and write-off | Proposed | 46458 | 46468 | 46482 | 46489 | 46493 | 46507 | S6 debt sale screens and award; S7 write-off and committee; S9 partner panel, allocation and fees | Debt sale screens and award, write-off committee, partner panel, allocation and fees | 37 | Specified at architecture level (DT13) | Debt sale officer, Write-off team member, Partner and agency manager, Head of Asset Liquidity, Write-off committee member, Finance and CFO delegate, Collection agency (OA) user | Chakri Day (6 Apr) and Songkran (13 to 15 Apr) fall in the SIT and UAT weeks; the release date is confirmed under DL34 |
| E7 | Deviations and partners | Proposed | 46486 | 46496 | 46510 | 46517 | 46521 | 46538 | S8 deviations end to end; S9 partner scoring, conduct and the field app | Deviations X1 to X7 end to end. Partner scoring, conduct and the field app | 18 | Specified at architecture level (DT13) | Field collector, Hardship and vulnerability specialist, Complaint officer, Fraud investigator | None |
| E8 | Administration and hardening | Proposed | 46514 | 46524 | 46538 | 46545 | 46549 | 46568 | P4 full administration; conduct checks; autonomy step-ups; regulatory returns; hardening | Full administration, conduct checks, autonomy step-ups, regulatory returns, hardening | 19 | Specified at architecture level (DT13) | Conduct and QA officer | None |

## Modules by release

| When each module is delivered |  |  |
|---|---|---|
| The ten platform modules and nine stage modules, with the releases that deliver them. |  |  |
| Module | Name | Delivered in |
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
| S1 | Valuation and route | E4 |
| S2 | TDR, settlement and deed in lieu | E2 foundations; E3 |
| S3 | Guarantees and guarantors | E4 |
| S4 | Litigation and enforcement | E2 notices; E5 |
| S5 | Assets and auction | E3; E4 |
| S6 | Debt sale | E5 data; E6 screens |
| S7 | Write-off and recovery | E6 |
| S8 | Deviation handling | E2 screening; E7 |
| S9 | Partner management | E6 panel; E7 scoring |

## Gates

| Gates between releases |  |  |  |  |
|---|---|---|---|---|
| Each release passes six gates. A story that misses a gate stays behind its flag and moves to the next release. |  |  |  |  |
| Gate | Name | When | Criteria | Who decides |
| G1 | Design signed | Ten days before the epic starts | The epic's features, screens and rules are signed by the business lead; Epics 3 to 8 sign in parallel with the build of the epic before (DT05) | Product owner with the business lead |
| G2 | Ready to pull | Before a story is pulled | Each story meets the definition of ready | Product owner |
| G3 | SIT exit | End of the SIT week | Every test case for the release passes in SIT; no open severity 1 or 2 defect | QA lead with SCB IT |
| G4 | UAT exit | End of the UAT week | The business scripts for the release are signed | Business lead |
| G5 | Go decision | Friday before the release | SIT and UAT exits met; unfinished work behind a flag that is off; rollback tested | Release owner in the ACE team with the product owner and the application owner |
| G6 | Benefit check | Four weeks after the release | The measures the release was meant to move are read from the decision log and the reports | Product owner with the product heads |

## Calendar

| Release calendar |  |  |  |
|---|---|---|---|
| Build is continuous. SIT and UAT take the last two weeks before each release; business testers work with the squads during the build. |  |  |  |
| Epic | Activity | From | To |
| E1 | Design signed | 46318 | 46318 |
| E1 | Build | 46328 | 46342 |
| E1 | SIT | 46342 | 46346 |
| E1 | UAT | 46349 | 46353 |
| E1 | Go decision | 46353 | 46353 |
| E1 | Release | 46356 | 46356 |
| E2 | Design signed | 46346 | 46346 |
| E2 | Build | 46356 | 46370 |
| E2 | SIT | 46370 | 46374 |
| E2 | UAT | 46377 | 46381 |
| E2 | Go decision | 46381 | 46381 |
| E2 | Release | 46387 | 46387 |
| E3 | Design signed | 46374 | 46374 |
| E3 | Build | 46384 | 46398 |
| E3 | SIT | 46398 | 46402 |
| E3 | UAT | 46405 | 46409 |
| E3 | Go decision | 46409 | 46409 |
| E3 | Release | 46418 | 46418 |
| E4 | Design signed | 46402 | 46402 |
| E4 | Build | 46412 | 46426 |
| E4 | SIT | 46426 | 46430 |
| E4 | UAT | 46433 | 46437 |
| E4 | Go decision | 46437 | 46437 |
| E4 | Release | 46446 | 46446 |
| E5 | Design signed | 46430 | 46430 |
| E5 | Build | 46440 | 46454 |
| E5 | SIT | 46454 | 46458 |
| E5 | UAT | 46461 | 46465 |
| E5 | Go decision | 46465 | 46465 |
| E5 | Release | 46477 | 46477 |
| E6 | Design signed | 46458 | 46458 |
| E6 | Build | 46468 | 46482 |
| E6 | SIT | 46482 | 46486 |
| E6 | UAT | 46489 | 46493 |
| E6 | Go decision | 46493 | 46493 |
| E6 | Release | 46507 | 46507 |
| E7 | Design signed | 46486 | 46486 |
| E7 | Build | 46496 | 46510 |
| E7 | SIT | 46510 | 46514 |
| E7 | UAT | 46517 | 46521 |
| E7 | Go decision | 46521 | 46521 |
| E7 | Release | 46538 | 46538 |
| E8 | Design signed | 46514 | 46514 |
| E8 | Build | 46524 | 46538 |
| E8 | SIT | 46538 | 46542 |
| E8 | UAT | 46545 | 46549 |
| E8 | Go decision | 46549 | 46549 |
| E8 | Release | 46568 | 46568 |

## Release rules

| Release rules |  |
|---|---|
| Rules that apply to every release. |  |
| Rule | Detail |
| 1 | A release goes ahead on its date. A squad that is not ready does not hold it; its flags stay off |
| 2 | Work enters a release when it passes SIT. Work that misses SIT moves to the next release behind its flag |
| 3 | The design of the next epic is signed while the current epic is built (DT05) |
| 4 | Epics 3 to 8 are confirmed one month ahead, at the sponsor review before their design sign-off |
| 5 | A role receives real users at the release that gives it a screen; until then it has test users in SIT and UAT (DL39) |
| 6 | Every release has a rollback: flags off first, then the previous tag |

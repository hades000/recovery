<!-- source: 03 Requirements and specifications/Recovery Workbench Epics 3 to 8 Specification v2.docx -->
<!-- converted: 2026-11-16 from DOCX -->

> **Source:** `03 Requirements and specifications/Recovery Workbench Epics 3 to 8 Specification v2.docx`  
> **Converted from:** DOCX

Recovery Workbench

Epics 3 to 8 at specification level

SCB Collections and Recovery. Henka Group, 28 October 2026

| Item | Detail |
|---|---|
| Document | Recovery Workbench epics 3 to 8 at specification level |
| Version | 1 |
| Date | 28 October 2026 |
| Prepared by | Henka Group |
| Structure | ISO/IEC/IEEE 29148 until the SCB X template arrives (DT14) |

# 1. The six epics

| Epic | Release | Theme | Content | Features |
|---|---|---|---|---|
| E3 | 31 Jan 2027 | Settle, deed in lieu, assets | S2 settlement and deed in lieu to booking; S5 asset record, floor price and listing; P7 decision center | 31 |
| E4 | 28 Feb 2027 | Route decision | S1 route decision with COLLINS and the route agent; S3 guarantee and TCG claims; S5 auction rounds and RAMC; P6 customer self-service; P8 posting | 50 |
| E5 | 31 Mar 2027 | Litigation | S4 litigation end to end with law firms through the partner portal; S6 lot data and data room | 26 |
| E6 | 30 Apr 2027 | Debt sale and write-off | S6 debt sale screens and award; S7 write-off and committee; S9 partner panel, allocation and fees | 37 |
| E7 | 31 May 2027 | Deviations and partners | S8 deviations end to end; S9 partner scoring, conduct and the field app | 18 |
| E8 | 30 Jun 2027 | Administration and hardening | P4 full administration; conduct checks; autonomy step-ups; regulatory returns; hardening | 19 |

Epics 3 to 8 are specified at architecture, API and integration detail (DT13). Stories are written one epic ahead of the build month and the design is signed in parallel with the epic before (DT05).

# 2. E3, Settle, deed in lieu, assets

| Item | Value |
|---|---|
| Release | 31 Jan 2027 |
| Design signed by | 18 Dec 2026 |
| Build | 28 Dec to 11 Jan |
| SIT and UAT | 11 Jan to 15 Jan; 18 Jan to 22 Jan |
| What the business gets | Settlements and deeds in lieu end to end to booking. Asset record, floor price and listing on HOME.SCB |
| Status | Proposed |

## 2.1 Modules and features

| Module | Feature | Kind | What it does |
|---|---|---|---|
| S2 | FEAT-TRT-01 Create the treatment record | System | Opens the treatment for the chosen route, holding the terms, the approval and the outcome. |
| S2 | FEAT-TRT-02 Offer a settlement inside the range | User | Lets the officer build and send a settlement offer within the calculated range. |
| S2 | FEAT-TRT-03 Approve a settlement below the floor | User | Routes a settlement below the floor price to the approver or the committee named in the matrix. |
| S2 | FEAT-TRT-04 Offer a TDR plan | User | Lets the restructuring officer build and send the plan offer, with the band and the rule version applied. |
| S2 | FEAT-TRT-05 Pre-assess affordability through ACE | System | Calls the ACE affordability calculation and records the result against the offer. |
| S2 | FEAT-TRT-06 Calculate the plan installment | System | Produces the model installment and the range the officer may move within. |
| S2 | FEAT-TRT-07 Send the offer and start the validity timer | System | Sends the offer to the customer and starts the validity clock. The wait is a timer, not a routed state. |
| S2 | FEAT-TRT-08 Route the signed offer to operations for booking | System | Moves the case to operations when the customer signs inside the validity period. |
| S2 | FEAT-TRT-09 Return the case to its prior status on no signature | System | Sends the case back to the status it held in COLLINS when the customer declines or the offer expires. |
| S2 | FEAT-TRT-10 Book the plan and set the schedule | System | Writes the plan to NLEADS and ALS, sets the payment schedule and starts the plan timers. |
| S2 | FEAT-TRT-11 Detect and handle a broken plan | System | Counts missed payments against the break rule and moves the case to the point the rule names. |
| S2 | FEAT-TRT-12 Run a deed in lieu to ownership transfer | User | Takes the deed in lieu from offer through inspection, documents and transfer to the asset record. |
| S2 | FEAT-TRT-13 Check encumbrance and eligibility before negotiation | System | Runs the encumbrance and title checks early, so a deed in lieu is not negotiated on an asset that cannot transfer. |
| S2 | FEAT-TRT-14 Unlock the asset as a non performing asset by rule | System | Applies the auto-unlock rule so the asset moves to the asset list without a person for the cases that qualify. |
| S2 | FEAT-TRT-15 Capture the collateral inspection in the field | User | Lets the field officer record the inspection, the checklist and the bills against the case. |
| S2 | FEAT-TRT-16 Set up a deed in lieu buy-back rental | System | Opens the rental record, the auto-debit and the receipt loop where the customer buys back. |
| S2 | FEAT-TRT-17 Release the collateral after settlement | System | Tells CCMS to release the security once the settlement has cleared, and records the release. |
| S2 | FEAT-TRT-18 Generate the treatment document set | System | Produces the agreement, contract, credit approval and mortgage documents for the treatment chosen. |
| S5 | FEAT-AST-01 Take a repossessed vehicle onto the books | System | Creates the asset record from the repossession result and starts the holding clock. |
| S5 | FEAT-AST-02 Take a property onto the books after a deed in lieu | System | Creates the asset record when a deed in lieu transfer completes. |
| S5 | FEAT-AST-03 Take a property onto the books after an LED auction | System | Creates the asset record when the bank takes the property at the enforcement auction. |
| S5 | FEAT-AST-04 Serve the statutory notice and prove delivery | System | Sends the notice the repossession requires and records the proof. |
| S5 | FEAT-AST-05 Track holding age against the provision steps | System | Counts the days held and applies the provision step the policy sets at each threshold. |
| S5 | FEAT-AST-06 Record and track the asset stock balance | User | Gives the stock balance an owner and a number on one screen. It has no owner today. |
| S5 | FEAT-AST-07 Maintain a held property | User | Records maintenance, insurance and custody costs against the asset. |
| S5 | FEAT-AST-09 Re-appraise a held asset on cycle | System | Raises the re-appraisal order when the holding period passes the re-appraisal interval. |
| S5 | FEAT-AST-10 Recommend the disposal route | System | Proposes auction, broker, RAMC, buy-back or rental with the expected return on each. |
| S5 | FEAT-AST-11 Set the start and floor price | User | Lets the sale officer set the opening price and the floor, with the head of NPA approving the floor. |
| S5 | FEAT-AST-12 Publish the listing | System | Puts the asset on HOME.SCB and the auction portal with its price and schedule. |
| P10 | FEAT-AGT-12 Change an autonomy level | Admin | Changes the autonomy level for one agent and one decision, as a versioned configuration row. |
| P10 | FEAT-AGT-13 Detect model drift and raise a decision | System | Watches calibration and drift, and raises a decision with an owner and a date on a breach. |

## 2.2 Architecture

Built in the recovery module of the ACE service with no new service. Modules: P10 Agent runtime, S2 TDR, settlement and deed in lieu, S5 Assets and auction.

| Element | Change |
|---|---|
| Data | Entities used or extended: asset, asset_sale, listing, treatment |
| Rules | Route sets loaded or extended: DEEDINLIEU, DISPOSAL, RESTRUCTURE, SETTLEMENT |
| Screens |  |
| Agents | Settlement and restructure agent, Valuation agent, Pricing agent |

## 2.3 APIs

| Method | Path | Purpose | Access |
|---|---|---|---|
| PATCH | /treatments/{treatmentId} | Change the terms of a draft treatment | Treatment and offer U |
| POST | /treatments/{treatmentId}/submit | Submit a treatment for approval | Treatment and offer U |
| GET | /assets | List assets held with age, holding cost and sale status | Asset and disposal R |
| GET | /assets/{assetId} | Read one asset with title, condition, valuations, costs and listing | Asset and disposal R |
| POST | /assets/{assetId}/valuations | Order or record a valuation | Asset and disposal C |
| POST | /assets/{assetId}/listings | Set the list price and floor and send for approval | Asset and disposal C |

## 2.4 Integrations

| ID | System | Direction | Approach | Frequency |
|---|---|---|---|---|
| INT-03 | Core bank (ALS) | Out | Booked by the officer; confirmed on the next day's load | As approved |
| INT-12 | AMIS | In | File load | Monthly |
| INT-13 | RPS | In | File load | Weekly |
| INT-26 | NLEADS | Out | Submitted by the officer in NLEADS | As needed |
| INT-27 | HOME.SCB | Out | Not available today; published by the sale officer | As listed |

## 2.5 Users

Roles that receive real users: Restructuring officer (FCR), Legal counsel, Sale officer, NPA and asset manager, Credit Administration officer, Head of NPA.

## 2.6 Dependencies

| ID | What is needed | Needed by | Owner | Decision |
|---|---|---|---|---|
| DEP-09 | TDR and DIL split between the collection squad, the Enterprise AI team and TechX | 15 Dec | IT lead | DL14 |

# 3. E4, Route decision

| Item | Value |
|---|---|
| Release | 28 Feb 2027 |
| Design signed by | 15 Jan 2027 |
| Build | 25 Jan to 8 Feb |
| SIT and UAT | 8 Feb to 12 Feb; 15 Feb to 19 Feb |
| What the business gets | The route recommended with reasons and approved within the delegation of authority for every new case. Guarantee and TCG claims. Auction rounds and RAMC transfer |
| Status | Proposed |

## 3.1 Modules and features

| Module | Feature | Kind | What it does |
|---|---|---|---|
| S1 | FEAT-VAL-01 Order an appraisal when the last one is stale | System | Checks the appraisal age against the limit and raises the order to SVAF with no person involved. |
| S1 | FEAT-VAL-02 Receive the appraisal value from SVAF | System | Takes the value, date and appraiser back from SVAF onto the collateral record. |
| S1 | FEAT-VAL-03 Flag appraisal outliers against market and last value | System | Compares the new value to the market and the previous value and flags the gap for a person. |
| S1 | FEAT-VAL-04 Accept the appraisal value | User | Lets the case owner accept the value, which fixes the band the route decision runs on. |
| S1 | FEAT-VAL-05 Call COLLINS for return by route | System | Asks the COLLINS model for the expected return on each route and records the answer with its version. |
| S1 | FEAT-VAL-06 Calculate the payoff and settlement range | System | Works out the payoff from ALS and the settlement range from the rules, with the floor applied. |
| S1 | FEAT-VAL-07 Score the routes and recommend one with reasons | System | Runs the route agent, which recommends a route and states the reasons and the alternatives. |
| S1 | FEAT-VAL-08 Approve a route inside the limit | User | Lets the case owner approve the recommended route within their delegated limit. |
| S1 | FEAT-VAL-09 Approve a route above the limit at committee | User | Takes the route to the credit committee when it is beyond the case owner's limit. |
| S1 | FEAT-VAL-10 Hold the case and set a review date | User | Lets the owner hold a case where no route is right yet, with a date the hold is reviewed. |
| S1 | FEAT-VAL-11 Reconsider the route after new information | User | Reopens the route decision when a value, a payment or a deviation changes the picture. |
| S1 | FEAT-VAL-12 Start the route flow and set its timers | System | Opens the chosen route, creates its tasks and starts its clocks. |
| S3 | FEAT-GUA-01 Prepare a TCG guarantee claim | System | Assembles the claim from the case facts and the documents the scheme requires. |
| S3 | FEAT-GUA-02 Submit the claim to the TCG portal | System | Files the prepared claim and records the submission reference on the case. |
| S3 | FEAT-GUA-03 Track the claim to payment | System | Follows the claim through its states and raises the service level breach if it stalls. |
| S3 | FEAT-GUA-04 Record the subrogation position | System | Records what the guarantor may reclaim after payment, so the position is not lost. |
| S3 | FEAT-GUA-05 Notify guarantors and co-borrowers | System | Sends the demand to every guarantor and co-borrower on the case, from the approved template. |
| S3 | FEAT-GUA-06 Negotiate with a guarantor | User | Lets the case owner negotiate within the range and record the outcome against the party. |
| S3 | FEAT-GUA-07 Close the case when a guarantee clears the debt | System | Closes the case and records the position when a guarantee payment clears the balance in full. |
| S3 | FEAT-GUA-08 File an insurance claim on a collateral event | User | Files the claim where collateral is stolen, written off or damaged, and triggers re-appraisal. |
| S5 | FEAT-AST-08 Evict occupants from a held property | User | Opens and tracks the eviction, which needs Legal and has no legal owner today. |
| S5 | FEAT-AST-13 Run the descending price schedule | System | Steps the price down on the ladder at each round until a bid clears the floor. |
| S5 | FEAT-AST-14 Allocate the asset to an auction vendor by distance | System | Picks one of the four vendors by distance and capacity, as the current rule does. |
| S5 | FEAT-AST-15 Run auction rounds and report bids | User | Lets the vendor run each round and report the bids back into the case. |
| S5 | FEAT-AST-16 Accept a bid below the floor with a second signature | User | Routes any bid under the floor for a second approval before it can be accepted. |
| S5 | FEAT-AST-17 Re-list on no bid | System | Puts the asset back on the schedule at the next price step when a round closes with no bid. |
| S5 | FEAT-AST-18 Enforce the five-day payment term | System | Tracks the winning bidder's payment against the term and releases the asset if it is missed. |
| S5 | FEAT-AST-19 Transfer vehicle registration | System | Prepares and submits the registration transfer through SCIS. |
| S5 | FEAT-AST-20 Record a property transfer at the Land Office | User | Tracks the Land Office transfer, which stays a person and officer step. |
| S5 | FEAT-AST-21 Apply proceeds and raise the shortfall | System | Applies the sale money to the balance and raises any residual to the next decision. |
| S5 | FEAT-AST-22 Transfer a pool to RAMC or the joint venture | User | Takes a pool of assets to RAMC with committee approval, and records the transfer. |
| S5 | FEAT-AST-23 Arrange a customer buy-back | User | Opens the buy-back where the former owner repurchases, with the approval the limit requires. |
| S5 | FEAT-AST-24 Rent a held asset to a third party | User | Records the rental, the debit and the arrears follow-up while the asset is held. |
| S5 | FEAT-AST-25 Sell through a broker | User | Opens the broker route with its fee and terms, and tracks it to the sale. |
| P6 | FEAT-COM-01 View the offer on LINE and web | User | Lets the customer see the offer the bank has made, on the channel they use. |
| P6 | FEAT-COM-02 Accept an offer in self-service | User | Lets the customer accept without a call or a branch visit, which records the acceptance on the case. |
| P6 | FEAT-COM-03 Pay in self-service | User | Lets the customer pay against the plan or the settlement from the same screen. |
| P6 | FEAT-COM-04 Raise a dispute in self-service | User | Lets the customer raise a dispute, which opens X1 and applies the contact stop. |
| P6 | FEAT-COM-05 Maintain the contact repository | Admin | Keeps the verified contact points for every party, with consent state per channel. |
| P6 | FEAT-COM-06 Record a custody movement of a document | System | Tracks a physical document leaving and returning, so the original is never lost. |
| P6 | FEAT-COM-07 Answer a legal or audit document request | User | Returns the documents and the index entries a legal or audit request asks for. |
| P6 | FEAT-COM-08 Apply retention on case closure | System | Applies the retention class to every document on the case when the case closes. |
| P8 | FEAT-PAY-03 Match a settlement payment | System | Matches a settlement payment to the treatment and closes the money side. |
| P8 | FEAT-PAY-04 Match auction and enforcement proceeds | System | Matches money from an auction, a broker or the LED to the right case. |
| P8 | FEAT-PAY-05 Calculate fees and charges | System | Works out partner fees, court fees and charges from the fee tables held as data. |
| P8 | FEAT-PAY-06 Post a settlement booking to ALS | System | Writes the agreed settlement terms to ALS and reads the booked position back. |
| P8 | FEAT-PAY-07 Post to the general ledger | System | Posts the accounting entries for settlements, sales and write-offs to the ledger. |
| P8 | FEAT-PAY-09 Run the deed in lieu rental auto-debit | System | Takes the rental by auto-debit, issues the receipt and follows up arrears. |
| P8 | FEAT-PAY-10 Apply proceeds to the case balance | System | Applies every receipt to the balance in the order the policy sets. |
| P8 | FEAT-PAY-11 Reconcile money movements daily | System | Compares what the Workbench matched to what ALS and the ledger show, every day. |

## 3.2 Architecture

Built in the recovery module of the ACE service with no new service. Modules: P6 Communications, P8 Payments and posting, S1 Valuation and route, S3 Guarantees and guarantors, S5 Assets and auction.

| Element | Change |
|---|---|
| Data | Entities used or extended: asset, asset_sale, guarantee_claim, listing, notice, proceeds, score, template, valuation |
| Rules | Route sets loaded or extended: DISPOSAL, GUARANTEE |
| Screens |  |
| Agents | Route agent, Guarantee claim agent, Reconciliation agent |

## 3.3 APIs

| Method | Path | Purpose | Access |
|---|---|---|---|
| GET | /cases/{caseId}/recommendation | Read the current recommendation with reasons and the expected return by route | Decision log R |
| POST | /cases/{caseId}/route | Submit the route decision for approval, with an override reason where it departs from the recommendation | Treatment and offer U |
| POST | /cases/{caseId}/guarantee-claims | Open a guarantee or TCG claim | Treatment and offer C |
| PATCH | /guarantee-claims/{claimId} | Record the claim result | Treatment and offer U |
| POST | /listings/{listingId}/rounds | Record an auction round and its result | Asset and disposal U |
| POST | /proceeds/{proceedsId}/match | Match a receipt to a case and account | Write-off and posting U |
| POST | /cases/{caseId}/instructions | Issue an instruction to a partner by rule | Partner portal C |
| GET | /partner/instructions | List the instructions placed with the caller's firm | Partner portal R |
| POST | /partner/instructions/{instructionId}/accept | Accept or decline an instruction | Partner portal U |
| POST | /partner/instructions/{instructionId}/results | Record a result with its documents | Partner portal U |

## 3.4 Integrations

| ID | System | Direction | Approach | Frequency |
|---|---|---|---|---|
| INT-28 | SCIS | Out | Not available today; prepared by the officer | As needed |
| INT-29 | Thai Credit Guarantee Corporation | Both | Not available today; entered and filed by the guarantee officer | As needed |

## 3.5 Users

Roles that receive real users: Guarantee officer, Credit approval committee member, Valuer, Auction vendor, RAMC user.

## 3.6 Dependencies

| ID | What is needed | Needed by | Owner | Decision |
|---|---|---|---|---|
| DEP-21 | Route return models by route for the route decision | 25 Jan | Enterprise AI team with Model Risk | None |
| DEP-29 | Valuers, auction vendors and RAMC onboarded to the partner portal | 1 Feb | Partner and agency manager; Head of Asset Liquidity | DL03 |
| DEP-32 | TCG claim rules and the guarantee quota | 25 Jan | Guarantee officer | None |

# 4. E5, Litigation

| Item | Value |
|---|---|
| Release | 31 Mar 2027 |
| Design signed by | 12 Feb 2027 |
| Build | 22 Feb to 8 Mar |
| SIT and UAT | 8 Mar to 12 Mar; 15 Mar to 19 Mar |
| What the business gets | Litigation instructed and tracked end to end, law firms through the partner portal. Debt sale lot data and the buyer data room |
| Status | Proposed |

## 4.1 Modules and features

| Module | Feature | Kind | What it does |
|---|---|---|---|
| S4 | FEAT-LIT-01 Issue demand and recall notices | System | Produces and sends the statutory notices by rule, with no person in the path. |
| S4 | FEAT-LIT-02 Record proof of delivery on a notice | System | Writes the delivery confirmation onto the case, which the notice period timer starts from. |
| S4 | FEAT-LIT-03 Run the notice period timer | System | Starts and tracks the statutory notice period and raises it when it expires. |
| S4 | FEAT-LIT-04 Assemble the litigation pack | System | Builds the pack from the document index and the case facts, ready for the officer to verify. |
| S4 | FEAT-LIT-05 Check the pack against the defect list | System | Tests the pack against the known defect list and names what is missing. |
| S4 | FEAT-LIT-06 Recover a missing or lost document | User | Opens the recovery path for a document the pack needs and the bank cannot find. |
| S4 | FEAT-LIT-07 Verify the pack and approve filing | User | Lets the litigation officer confirm the pack and authorize the filing. |
| S4 | FEAT-LIT-08 Select the law firm from the panel | System | Picks the firm by the panel rule: scorecard, capacity, court and conflict. |
| S4 | FEAT-LIT-09 Instruct the firm through the portal | System | Sends the instruction and the pack to the firm and starts the partner clock. |
| S4 | FEAT-LIT-10 Record the court filing and receipt | User | Takes the filing confirmation and the court case number from the firm onto the case. |
| S4 | FEAT-LIT-11 Track hearings, deadlines and fees | System | Follows the court calendar, raises each deadline and accrues the fees against the case. |
| S4 | FEAT-LIT-12 Recommend the next litigation step | System | Proposes the next step with reasons, for the officer or the approver to decide. |
| S4 | FEAT-LIT-13 Settle before judgment | User | Takes a settlement during the case to the approver named by the limit, and books it if approved. |
| S4 | FEAT-LIT-14 Decide and manage an appeal | User | Records the appeal decision, the grounds and the approval, and tracks it to its end. |
| S4 | FEAT-LIT-15 Pay court fees and legal expenses | System | Checks the fee against the schedule, routes it for approval where needed and pays it. |
| S4 | FEAT-LIT-16 Record the judgment | System | Writes the judgment date and amount onto the case and opens the enforcement step. |
| S4 | FEAT-LIT-17 Trace assets for enforcement | System | Searches the bureau, registries and insurers for assets to enforce against, and reports what it finds. |
| S4 | FEAT-LIT-18 Apply for the writ and seizure | User | Instructs the writ and the seizure through the firm and tracks it to execution. |
| S4 | FEAT-LIT-19 Follow the LED auction ladder | System | Tracks the enforcement auction through the 100, 90, 80 and 70 percent steps of official value. |
| S4 | FEAT-LIT-20 Record an enforcement deferral with its reason | User | Lets the enforcement owner defer with a coded reason and a review date. Enforcement after judgment has no owner today. |
| S4 | FEAT-LIT-21 File a bankruptcy petition | User | Takes the petition to the approver and files it through the firm. |
| S4 | FEAT-LIT-22 Match enforcement proceeds to the case | System | Matches money from the LED or the firm to the case and applies it to the balance. |
| S6 | FEAT-DBS-01 Select eligible accounts for sale by rule | System | Applies the eligibility rules, including the 54 percent cap, to pick the sale population. |
| S6 | FEAT-DBS-02 Build the lots and estimate the price | System | Groups the accounts into lots and estimates the price from the COLLINS lot economics. |
| S6 | FEAT-DBS-03 Prepare the masked data tape | System | Builds the data tape with personal data masked under PDPA, ready for the data room. |
| S6 | FEAT-DBS-04 Open the buyer data room | System | Publishes the lot and the masked tape to the data room for qualified buyers. |

## 4.2 Architecture

Built in the recovery module of the ACE service with no new service. Modules: S4 Litigation and enforcement, S6 Debt sale.

| Element | Change |
|---|---|
| Data | Entities used or extended: debt_sale_account, debt_sale_lot, hearing, legal_action |
| Rules | Route sets loaded or extended: DEBTSALE, LITIGATION |
| Screens | Litigation workspace, Enforcement workspace |
| Agents | Legal document agent, Debt sale agent |

## 4.3 APIs

| Method | Path | Purpose | Access |
|---|---|---|---|
| POST | /cases/{caseId}/legal-actions | Open a legal action and its pack | Litigation C |
| GET | /legal-actions/{legalActionId} | Read a legal action with pack, instruction, hearings and judgment | Litigation R |
| PATCH | /legal-actions/{legalActionId} | Record a filing, judgment or enforcement step | Litigation U |
| POST | /legal-actions/{legalActionId}/hearings | Add a hearing date | Litigation U |
| POST | /debt-sale-lots | Create a lot from eligible accounts | Debt sale C |
| GET | /debt-sale-lots/{lotId} | Read a lot with its accounts, reserve and bids | Debt sale R |
| GET | /partner/data-room/{lotId} | Read the lot tape and documents for an admitted buyer | Partner portal R |
| POST | /partner/data-room/{lotId}/bids | Submit a bid on a lot | Partner portal C |

## 4.4 Integrations

| ID | System | Direction | Approach | Frequency |
|---|---|---|---|---|
| INT-25 | Debt buyers | Out | File through the data room | Per lot |
| INT-33 | Legal Execution Department and courts | In | Through the law firms in the partner portal | As entered |

## 4.5 Users

Roles that receive real users: Enforcement owner, Law firm user, Debt buyer and AMC.

## 4.6 Dependencies

| ID | What is needed | Needed by | Owner | Decision |
|---|---|---|---|---|
| DEP-10 | Partner access from outside the bank through the external gateway | 1 Feb | Architecture team | DL03 |
| DEP-28 | Panel law firms onboarded to the partner portal with user accounts | 1 Mar | Partner and agency manager | DL03 |
| DEP-30 | Debt buyers' data room access and confidentiality agreements | 1 Mar | Head of Asset Liquidity | DL03 |

# 5. E6, Debt sale and write-off

| Item | Value |
|---|---|
| Release | 30 Apr 2027 |
| Design signed by | 12 Mar 2027 |
| Build | 22 Mar to 5 Apr |
| SIT and UAT | 5 Apr to 9 Apr; 12 Apr to 16 Apr |
| What the business gets | Debt sale screens and award, write-off committee, partner panel, allocation and fees |
| Status | Proposed |

## 5.1 Modules and features

| Module | Feature | Kind | What it does |
|---|---|---|---|
| S6 | FEAT-DBS-05 Approve lots, reserve and tiered terms | User | Takes the lot, the reserve price and the terms to the committee for approval. |
| S6 | FEAT-DBS-06 Qualify a buyer against KYC and licensing | System | Runs the KYC, licensing and eligibility checks before a buyer can bid. |
| S6 | FEAT-DBS-07 Bar a buyer that fails qualification | System | Removes a buyer from the panel on a license breach and releases the lot to the next bidder. |
| S6 | FEAT-DBS-08 Take buyer bids | User | Lets a qualified buyer bid on a lot through the portal, inside the bid window. |
| S6 | FEAT-DBS-09 Award the lot and test the price | User | Compares the best bid to the reserve and the model, and awards with the approval the limit requires. |
| S6 | FEAT-DBS-10 Generate the sale agreement and notices | System | Produces the agreement and the customer notices the sale requires. |
| S6 | FEAT-DBS-11 Transfer the data to the buyer | System | Sends the awarded account data to the buyer and records the transfer. |
| S6 | FEAT-DBS-12 Derecognize and post to the general ledger | System | Removes the sold accounts from the book and posts the result to ALS and the ledger. |
| S6 | FEAT-DBS-13 Handle a buyer put-back claim | User | Reviews a claim that an account should not have been sold, and settles or rejects it. |
| S6 | FEAT-DBS-14 Close a case awarded in a sold lot | System | Stops every open action on a case whose account is sold in a lot, and closes it. |
| S6 | FEAT-DBS-15 Confirm buyer remittance | System | Matches the buyer's payment to the award and closes the money side of the lot. |
| S6 | FEAT-DBS-16 Apply the debt sale cap | System | Holds the sale population inside the policy cap and reports the headroom. |
| S7 | FEAT-WOF-01 Run the monthly eligibility scan on both tracks | System | Scans the portfolio each month against the eligibility rules and proposes the write-off population. |
| S7 | FEAT-WOF-02 Apply the tax criteria | System | Tests each proposed account against the tax criteria and records the result. |
| S7 | FEAT-WOF-03 Prepare the write-off pack | System | Assembles the committee pack from the case facts, the documents and the recovery history. |
| S7 | FEAT-WOF-04 Remove a case from the proposed population | User | Lets the write-off team take a case out of the population before committee, with a reason. |
| S7 | FEAT-WOF-05 Route the population to the committee and schedule it | System | Sends the pack to the committee queue and books it into the monthly meeting. |
| S7 | FEAT-WOF-06 Approve a write-off inside the limit | User | Lets the committee approve within its delegation and records the limit applied. |
| S7 | FEAT-WOF-07 Reject a write-off | User | Lets the committee reject, with a reason that returns the case to recovery. |
| S7 | FEAT-WOF-08 Defer a write-off | User | Lets the committee defer with a review date, and holds the case until then. |
| S7 | FEAT-WOF-09 Post an approved write-off | System | Posts the write-off to ALS and the general ledger and releases the provision. |
| S7 | FEAT-WOF-10 Send provision inputs to Finance | System | Produces the provision file Finance needs from the posted population. |
| S7 | FEAT-WOF-11 Reconcile the approved and posted populations | System | Compares what the committee approved to what was posted, and raises every difference. |
| S7 | FEAT-WOF-12 Work the write-off exception loop | User | Opens the exception path for a case the rules cannot clear. This loop has no owner today. |
| S7 | FEAT-WOF-13 Close the case after the retention period | System | Closes the case once the retention period has run and no action is open. |
| S7 | FEAT-WOF-14 Change the eligibility or tax criteria | Admin | Lets the center of excellence change the criteria as a versioned rule load. |
| S7 | FEAT-WOF-15 Record a customer payment after charge-off | System | Takes a payment on a charged-off balance, applies it and records the recovery. |
| S7 | FEAT-WOF-16 Sell a post charge-off population | User | Opens the sale of charged-off accounts, with the approval the limit requires. |
| S9 | FEAT-PRM-01 Onboard a partner and set terms | User | Takes a partner onto the panel with its contract, fee schedule, service levels and scope. |
| S9 | FEAT-PRM-02 Hold the partner panel and fee schedule as data | Admin | Keeps every panel, fee schedule and service level as versioned reference data. |
| S9 | FEAT-PRM-03 Allocate work by measured return | System | Places work with the partner the scorecard rule picks, not by rotation or habit. |
| S9 | FEAT-PRM-04 Override an allocation with a reason | User | Lets the partner manager place work differently, with the reason recorded. |
| S9 | FEAT-PRM-05 Receive a partner result into the case | System | Takes contact, promise and cash results from the portal onto the case the same day. |
| S9 | FEAT-PRM-06 Place a charged-off account with an agency | User | Places post charge-off accounts with an agency under the placement rule. |
| S9 | FEAT-PRM-07 Match a recovery and calculate the agency fee | System | Matches money recovered by an agency to the case and works out the fee due. |
| P8 | FEAT-PAY-08 Produce provision inputs | System | Builds the provision inputs Finance needs from the case and asset positions. |
| P9 | FEAT-RPT-06 Track benefit realisation | User | Tracks the measures in the benefit model against the baseline, monthly. |

## 5.2 Architecture

Built in the recovery module of the ACE service with no new service. Modules: P8 Payments and posting, P9 Reporting, S6 Debt sale, S7 Write-off and recovery, S9 Partner management.

| Element | Change |
|---|---|
| Data | Entities used or extended: debt_sale_account, debt_sale_lot, partner, partner_instruction, proceeds, write_off |
| Rules | Route sets loaded or extended: DEBTSALE, WRITEOFF |
| Screens |  |
| Agents | Write-off agent |

## 5.3 APIs

| Method | Path | Purpose | Access |
|---|---|---|---|
| POST | /debt-sale-lots/{lotId}/award | Award a lot to a buyer after the bids close | Debt sale A |
| POST | /write-off-scans | Run the monthly write-off scan for a cut-off date | Write-off and posting C |
| POST | /write-offs/{writeOffId}/committee-decision | Record the committee decision for a write-off | Write-off and posting A |
| POST | /partner/instructions/{instructionId}/invoices | Submit a fee invoice | Partner portal C |

## 5.4 Integrations

| ID | System | Direction | Approach | Frequency |
|---|---|---|---|---|
| INT-16 | GL | In | File load | Monthly |

## 5.5 Users

Roles that receive real users: Debt sale officer, Write-off team member, Partner and agency manager, Head of Asset Liquidity, Write-off committee member, Finance and CFO delegate, Collection agency (OA) user.

## 5.6 Dependencies

| ID | What is needed | Needed by | Owner | Decision |
|---|---|---|---|---|
| DEP-31 | Collection agencies onboarded with placement and outcome capture | 1 Apr | Partner and agency manager | DL03 |
| DEP-33 | Write-off tax criteria version from Finance | 22 Mar | Finance and CFO delegate | None |

# 6. E7, Deviations and partners

| Item | Value |
|---|---|
| Release | 31 May 2027 |
| Design signed by | 9 Apr 2027 |
| Build | 19 Apr to 3 May |
| SIT and UAT | 3 May to 7 May; 10 May to 14 May |
| What the business gets | Deviations X1 to X7 end to end. Partner scoring, conduct and the field app |
| Status | Proposed |

## 6.1 Modules and features

| Module | Feature | Kind | What it does |
|---|---|---|---|
| S8 | FEAT-DVF-01 Run X1 dispute and complaint end to end | User | Takes the dispute from detection through the evidence pack to resolution and the return point. |
| S8 | FEAT-DVF-02 Run X2 vulnerability and hardship end to end | User | Takes the case to the specialist queue with contact limits, through to the hardship decision. |
| S8 | FEAT-DVF-03 Run X3 deceased customer end to end | User | Stops contact, notifies heirs, files the insurance claim and settles the estate position. |
| S8 | FEAT-DVF-04 Run X4 fraud end to end | User | Refers to the fraud team, tracks the investigation and routes the case on the outcome. |
| S8 | FEAT-DVF-05 Run X5 bankruptcy and seizure end to end | User | Stops direct collection and files the claim with the receiver or the LED before the deadline. |
| S8 | FEAT-DVF-06 Run X6 lost contact and skip trace end to end | System | Runs the skip trace through the bureau, internal data and agency sources and routes on the result. |
| S8 | FEAT-DVF-07 Run X7 collateral event end to end | User | Files the insurance claim, re-appraises the collateral and returns the case to the route decision. |
| S8 | FEAT-DVF-08 Review an override | User | Puts overrides in front of the review forum, with the reason and the outcome of each. |
| S8 | FEAT-DVF-09 Match a complaint to the preceding contact | User | Links each complaint to the contact that caused it, which is how conduct is measured. |
| S8 | FEAT-DVF-10 Handle a contact sent while a block is on | User | Opens the breach path when a message goes out against a contact stop. |
| S9 | FEAT-PRM-08 Score partners monthly | System | Builds the scorecard from the measured results and publishes it to the panel. |
| S9 | FEAT-PRM-09 Approve partner fees | User | Checks the fee claim against the schedule and the result, and approves it. |
| S9 | FEAT-PRM-10 Hold a partner review | User | Runs the review against the six points every partner type is managed on, and records the actions. |
| S9 | FEAT-PRM-11 Issue a notice on a missed target | User | Sends the contractual notice when a partner misses its targets, and starts the cure period. |
| S9 | FEAT-PRM-12 End a partner contract and recall the work | User | Closes the contract and pulls every open case back for re-selection. |
| S9 | FEAT-PRM-13 Check partner conduct | System | Samples partner contacts and complaints against the conduct rules and raises breaches. |
| S9 | FEAT-PRM-14 Manage extra costs and services on an asset | User | Records and approves additional partner costs on a held asset. |
| S9 | FEAT-PRM-15 Capture field work through the field app | User | Lets the field collector record visits, photos and bills against the case from the field. |

## 6.2 Architecture

Built in the recovery module of the ACE service with no new service. Modules: S8 Deviation handling, S9 Partner management.

| Element | Change |
|---|---|
| Data | Entities used or extended: deviation, partner, partner_instruction |
| Rules | Route sets loaded or extended: DEVIATION |
| Screens |  |
| Agents | Tracing agent |

## 6.3 APIs

No new endpoint; the epic extends existing endpoints.

## 6.4 Integrations

| ID | System | Direction | Approach | Frequency |
|---|---|---|---|---|
| INT-30 | NCB | In | Not available today; by the officer | As needed |

## 6.5 Users

Roles that receive real users: Field collector, Hardship and vulnerability specialist, Complaint officer, Fraud investigator.

## 6.6 Dependencies

None beyond the earlier epics.

# 7. E8, Administration and hardening

| Item | Value |
|---|---|
| Release | 30 Jun 2027 |
| Design signed by | 7 May 2027 |
| Build | 17 May to 31 May |
| SIT and UAT | 31 May to 4 Jun; 7 Jun to 11 Jun |
| What the business gets | Full administration, conduct checks, autonomy step-ups, regulatory returns, hardening |
| Status | Proposed |

## 7.1 Modules and features

| Module | Feature | Kind | What it does |
|---|---|---|---|
| P9 | FEAT-RPT-07 Produce regulatory returns | System | Builds the regulatory extracts from the data products and the decision log. |
| P9 | FEAT-RPT-10 Classify, stage and re-age an account | System | Applies the classification and re-ageing rules and recomputes the segment when they change. |
| P10 | FEAT-AGT-14 Run a champion and challenger test | Admin | Runs two rule or model versions side by side and compares the outcome. |
| P10 | FEAT-AGT-15 Raise or lower an autonomy level with approval | Admin | Steps an agent up on measured evidence, and drops it on a breach, with the approval each needs. |
| P10 | FEAT-AGT-16 Review agent risk at the committee | User | Puts agent performance, overrides and incidents in front of the strategy and model committee. |
| P4 | FEAT-ADM-01 Run the full administration screens | Admin | Gives administration one place for roles, queues, parameters, templates, panels and autonomy. |
| P4 | FEAT-ADM-02 Change a decision rule through the administration screens | Admin | Lets the center of excellence change a rule, test it and put it in force as a new version. |
| P4 | FEAT-ADM-03 Move an approval limit | Admin | Changes a delegated limit, with Risk approving and the change versioned. |
| P4 | FEAT-ADM-04 Set the treatment policy by product | Admin | Lets the product head set the bands, floors and ranges for their product. |
| P4 | FEAT-ADM-05 Add a letter template with Compliance approval | Admin | Adds a new template through the approval path and records who approved it. |
| P4 | FEAT-ADM-06 Roll back a configuration version | Admin | Returns any versioned table to its previous version and records the rollback. |
| P4 | FEAT-ADM-07 Publish a panel change | Admin | Puts a partner panel change in force with an effective date. |
| P4 | FEAT-ADM-08 Run a QA sample against the rule version applied | User | Samples closed decisions and tests each against the rule version that was in force. |
| P4 | FEAT-ADM-09 Return a defective pack | System | Sends a pack that fails the check back to its owner with the defects named. |
| P4 | FEAT-ADM-10 Detect a broken hash chain in the decision log | System | Tests the log chain and raises a control breach if a record does not verify. |
| P4 | FEAT-ADM-11 Handle a data subject request | User | Works a PDPA access, correction or erasure request inside the statutory period. |
| P4 | FEAT-ADM-12 Manage an incident | Admin | Runs the incident path: detect, hold, fix, record and report. |
| P4 | FEAT-ADM-13 Refer a case to Aric | System | Sends a case to Aric where the fraud rules require it, and takes the result back. |
| P4 | FEAT-ADM-14 Control access by role and by agent | Admin | Reviews and sets what each role and each agent may read and do, and reports the matrix. |

## 7.2 Architecture

Built in the recovery module of the ACE service with no new service. Modules: P4 Access and administration, P9 Reporting, P10 Agent runtime.

| Element | Change |
|---|---|
| Data | Entities used or extended: delegation_limit, lov_value, permission, role, rule_row |
| Rules | Route sets loaded or extended: None |
| Screens | Rules and parameters, Reference data, Delegation of authority, Queues and service levels, Roles and access, Personal data |
| Agents | None |

## 7.3 APIs

No new endpoint; the epic extends existing endpoints.

## 7.4 Integrations

| ID | System | Direction | Approach | Frequency |
|---|---|---|---|---|
| INT-31 | Aric | Out | Not available today; by the fraud investigator | As needed |

## 7.5 Users

Roles that receive real users: Conduct and QA officer.

## 7.6 Dependencies

None beyond the earlier epics.

# 8. Calendar notes

| Epic | Note |
|---|---|
| E3 | The New Year holidays (31 Dec and 1 Jan) fall in the first week of the build |
| E6 | Chakri Day (6 Apr) and Songkran (13 to 15 Apr) fall in the SIT and UAT weeks; the release date is confirmed under DL34 |
| E5 | Law firms reach the partner portal from outside the bank; the external access change must be live (DL03) |

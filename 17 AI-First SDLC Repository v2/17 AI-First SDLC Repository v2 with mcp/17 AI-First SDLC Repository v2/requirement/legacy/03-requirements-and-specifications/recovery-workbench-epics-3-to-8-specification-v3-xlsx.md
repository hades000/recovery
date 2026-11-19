<!-- source: 03 Requirements and specifications/Recovery Workbench Epics 3 to 8 Specification v3.xlsx -->
<!-- converted: 2026-11-16 from XLSX -->

> **Source:** `03 Requirements and specifications/Recovery Workbench Epics 3 to 8 Specification v3.xlsx`  
> **Converted from:** XLSX

## Features

| Features in Epics 3 to 8 |  |  |  |  |  |  |  |  |
|---|---|---|---|---|---|---|---|---|
| 181 features. |  |  |  |  |  |  |  |  |
| Epic | Module | Feature | Name | Kind | What it does | Primary role | Systems | Depends on |
| E4 | S1 | FEAT-VAL-01 | Order an appraisal when the last one is stale | System | Checks the appraisal age against the limit and raises the order to SVAF with no person involved. | Runs unattended | SVAF, CCMS | FEAT-RDF-06 |
| E4 | S1 | FEAT-VAL-02 | Receive the appraisal value from SVAF | System | Reads the value and date from v_ace_valuation once ACE has ingested the SVAF result, links it to the collateral by business key and records the valuer in valuation_ext. | Runs unattended | ACE (ingested from SVAF) | FEAT-VAL-01 |
| E4 | S1 | FEAT-VAL-03 | Flag appraisal outliers against market and last value | System | Compares the new value to the market and the previous value and flags the gap for a person. | Runs unattended | SVAF, Model gateway | FEAT-VAL-02 |
| E4 | S1 | FEAT-VAL-04 | Accept the appraisal value | User | Lets the case owner accept the value, which fixes the band the route decision runs on. | Case owner | Workbench | FEAT-VAL-03 |
| E4 | S1 | FEAT-VAL-05 | Call COLLINS for return by route | System | Reads the expected return on each route from v_ace_score, which ACE ingests from the COLLINS models, and records the answer with its model version. | Runs unattended | ACE (ingested from COLLINS), Model gateway | FEAT-AGT-01 |
| E4 | S1 | FEAT-VAL-06 | Calculate the payoff and settlement range | System | Works out the payoff from the ALS balances read through v_ace_account and the settlement range from the rules, with the floor applied. | Runs unattended | ALS and GL, Rules component | FEAT-DRI-07 |
| E4 | S1 | FEAT-VAL-07 | Score the routes and recommend one with reasons | System | Runs the route agent, which recommends a route and states the reasons and the alternatives. | Runs unattended | Workbench, Model gateway | FEAT-VAL-05, FEAT-VAL-06 |
| E4 | S1 | FEAT-VAL-08 | Approve a route inside the limit | User | Lets the case owner approve the recommended route within their delegated limit. | Case owner | Workbench | FEAT-APD-02, FEAT-VAL-07 |
| E4 | S1 | FEAT-VAL-09 | Approve a route above the limit at committee | User | Takes the route to the credit committee when it is beyond the case owner's limit. | Credit approval committee member | Workbench | FEAT-APD-05 |
| E4 | S1 | FEAT-VAL-10 | Hold the case and set a review date | User | Lets the owner hold a case where no route is right yet, with a date the hold is reviewed. | Case owner | Workbench | FEAT-CWC-11 |
| E4 | S1 | FEAT-VAL-11 | Reconsider the route after new information | User | Reopens the route decision when a value, a payment or a deviation changes the picture. | Case owner | Workbench | FEAT-VAL-07 |
| E4 | S1 | FEAT-VAL-12 | Start the route flow and set its timers | System | Opens the chosen route, creates its tasks and starts its clocks. | Runs unattended | Workbench, Quartz scheduler | FEAT-VAL-08 |
| E3 | S2 | FEAT-TRT-01 | Create the treatment record | System | Opens the treatment for the chosen route, holding the terms, the approval and the outcome. | Runs unattended | Workbench | FEAT-CHO-06 |
| E3 | S2 | FEAT-TRT-02 | Offer a settlement inside the range | User | Lets the officer build and send a settlement offer within the calculated range. | Restructuring officer (FCR) | Workbench, COLLINS | FEAT-TRT-01, FEAT-VAL-06 |
| E3 | S2 | FEAT-TRT-03 | Approve a settlement below the floor | User | Routes a settlement below the floor price to the approver or the committee named in the matrix. | Product head (Mortgage, HP, SSME) | Workbench | FEAT-APD-01 |
| E3 | S2 | FEAT-TRT-04 | Offer a TDR plan | User | Lets the restructuring officer build and send the plan offer, with the band and the rule version applied. | Restructuring officer (FCR) | COLLINS, EFS, ACE and TDR | FEAT-TRT-01 |
| E3 | S2 | FEAT-TRT-05 | Pre-assess affordability through ACE | System | Calls the ACE affordability calculation and records the result against the offer. | Runs unattended | ACE and TDR | FEAT-CHO-02 |
| E3 | S2 | FEAT-TRT-06 | Calculate the plan installment | System | Produces the model installment and the range the officer may move within. | Runs unattended | ACE and TDR, COLLINS | FEAT-TRT-05 |
| E3 | S2 | FEAT-TRT-07 | Send the offer and start the validity timer | System | Sends the offer to the customer and starts the validity clock. The wait is a timer, not a routed state. | Runs unattended | Workbench, WIN, NSS, LINE OA | FEAT-OCC-01, FEAT-TRT-04 |
| E3 | S2 | FEAT-TRT-08 | Route the signed offer to operations for booking | System | Moves the case to operations when the customer signs inside the validity period. | Runs unattended | Workbench, the Workbench document hub, ALS and GL | FEAT-OCC-09 |
| E3 | S2 | FEAT-TRT-09 | Return the case to its prior status on no signature | System | Sends the case back to the status it held in COLLINS when the customer declines or the offer expires. | Runs unattended | COLLINS, Workbench | FEAT-TRT-07 |
| E3 | S2 | FEAT-TRT-10 | Book the plan and set the schedule | System | Writes the plan to NLEADS and ALS, sets the payment schedule and starts the plan timers. | Runs unattended | NLEADS, ALS and GL | FEAT-CHO-07, FEAT-CHO-08 |
| E3 | S2 | FEAT-TRT-11 | Detect and handle a broken plan | System | Counts missed payments, read through v_ace_payment, against the break rule and moves the case to the point the rule names. | Runs unattended | ALS and GL, Workbench | FEAT-OCC-11 |
| E3 | S2 | FEAT-TRT-12 | Run a deed in lieu to ownership transfer | User | Takes the deed in lieu from offer through inspection, documents and transfer to the asset record. | Restructuring officer (FCR) | Workbench, CCMS, AMIS | FEAT-TRT-01 |
| E3 | S2 | FEAT-TRT-13 | Check encumbrance and eligibility before negotiation | System | Runs the encumbrance and title checks early, so a deed in lieu is not negotiated on an asset that cannot transfer. | Runs unattended | CCMS, Land Office | FEAT-TRT-12 |
| E3 | S2 | FEAT-TRT-14 | Unlock the asset as a non performing asset by rule | System | Applies the auto-unlock rule so the asset moves to the asset list without a person for the cases that qualify. | Runs unattended | Workbench, AMIS | FEAT-TRT-13 |
| E3 | S2 | FEAT-TRT-15 | Capture the collateral inspection in the field | User | Lets the field officer record the inspection, the checklist and the bills against the case. | Field collector | Field app, the Workbench document hub | FEAT-DCM-12 |
| E3 | S2 | FEAT-TRT-16 | Set up a deed in lieu buy-back rental | System | Opens the rental record, the auto-debit and the receipt loop where the customer buys back. | Runs unattended | AMIS, ATS | FEAT-TRT-12 |
| E3 | S2 | FEAT-TRT-17 | Release the collateral after settlement | System | Tells CCMS to release the security once the settlement has cleared, and records the release. | Runs unattended | CCMS, ALS and GL | FEAT-CHO-08 |
| E3 | S2 | FEAT-TRT-18 | Generate the treatment document set | System | Produces the agreement, contract, credit approval and mortgage documents for the treatment chosen. | Runs unattended | Workbench, the Workbench document hub | FEAT-OCC-07 |
| E4 | S3 | FEAT-GUA-01 | Prepare a TCG guarantee claim | System | Assembles the claim from the case facts and the documents the scheme requires. | Runs unattended | Workbench, TCG portal | FEAT-DCM-16 |
| E4 | S3 | FEAT-GUA-02 | Submit the claim to the TCG portal | System | Files the prepared claim and records the submission reference on the case. | Runs unattended | TCG portal | FEAT-GUA-01 |
| E4 | S3 | FEAT-GUA-03 | Track the claim to payment | System | Follows the claim through its states and raises the service level breach if it stalls. | Runs unattended | TCG portal, Workbench | FEAT-GUA-02 |
| E4 | S3 | FEAT-GUA-04 | Record the subrogation position | System | Records what the guarantor may reclaim after payment, so the position is not lost. | Runs unattended | ALS and GL, Workbench | FEAT-GUA-03 |
| E4 | S3 | FEAT-GUA-05 | Notify guarantors and co-borrowers | System | Sends the demand to every guarantor and co-borrower on the case, from the approved template. | Runs unattended | WIN, Workbench | FEAT-OCC-01 |
| E4 | S3 | FEAT-GUA-06 | Negotiate with a guarantor | User | Lets the case owner negotiate within the range and record the outcome against the party. | Case owner | Workbench | FEAT-GUA-05 |
| E4 | S3 | FEAT-GUA-07 | Close the case when a guarantee clears the debt | System | Closes the case and records the position when a guarantee payment clears the balance in full. | Runs unattended | ALS and GL | FEAT-GUA-03 |
| E4 | S3 | FEAT-GUA-08 | File an insurance claim on a collateral event | User | Files the claim where collateral is stolen, written off or damaged, and triggers re-appraisal. | Case owner | Workbench, SVAF | FEAT-VAL-01 |
| E5 | S4 | FEAT-LIT-01 | Issue demand and recall notices | System | Produces and sends the statutory notices by rule, with no person in the path. | Runs unattended | WIN, Workbench | FEAT-DRI-14 |
| E5 | S4 | FEAT-LIT-02 | Record proof of delivery on a notice | System | Reads the WIN proof of delivery from v_ace_pod, which ACE ingests, and writes it onto the notice; the notice period timer starts from it. | Runs unattended | ACE (ingested from WIN) | FEAT-DRI-17 |
| E5 | S4 | FEAT-LIT-03 | Run the notice period timer | System | Starts and tracks the statutory notice period and raises it when it expires. | Runs unattended | Workbench, Quartz scheduler | FEAT-CWC-11 |
| E5 | S4 | FEAT-LIT-04 | Assemble the litigation pack | System | Builds the pack from the document index and the case facts, ready for the officer to verify. | Runs unattended | Workbench, the Workbench document hub, CCMS | FEAT-DCM-02 |
| E5 | S4 | FEAT-LIT-05 | Check the pack against the defect list | System | Tests the pack against the known defect list and names what is missing. | Runs unattended | Workbench | FEAT-LIT-04, FEAT-DCM-16 |
| E5 | S4 | FEAT-LIT-06 | Recover a missing or lost document | User | Opens the recovery path for a document the pack needs and the bank cannot find. | Litigation officer | the Workbench document hub, CCMS | FEAT-LIT-05 |
| E5 | S4 | FEAT-LIT-07 | Verify the pack and approve filing | User | Lets the litigation officer confirm the pack and authorize the filing. | Litigation officer | Workbench | FEAT-LIT-05 |
| E5 | S4 | FEAT-LIT-08 | Select the law firm from the panel | System | Picks the firm by the panel rule: scorecard, capacity, court and conflict. | Runs unattended | Workbench, Rules component | FEAT-PRM-02 |
| E5 | S4 | FEAT-LIT-09 | Instruct the firm through the portal | System | Sends the instruction and the pack to the firm and starts the partner clock. | Runs unattended | Partner portal, LIT | FEAT-LIT-08 |
| E5 | S4 | FEAT-LIT-10 | Record the court filing and receipt | User | Takes the filing confirmation and the court case number from the firm onto the case, and matches them to the LIT lawsuit read through v_ace_lawsuit. | Law firm user | Partner portal, ACE (ingested from LIT) | FEAT-LIT-09 |
| E5 | S4 | FEAT-LIT-11 | Track hearings, deadlines and fees | System | Follows the court calendar from the LIT hearings read through v_ace_hearing and the firm's entries, raises each deadline and accrues the fees against the case. | Runs unattended | ACE (ingested from LIT), Partner portal | FEAT-LIT-10 |
| E5 | S4 | FEAT-LIT-12 | Recommend the next litigation step | System | Proposes the next step with reasons, for the officer or the approver to decide. | Runs unattended | Workbench, Model gateway | FEAT-LIT-11 |
| E5 | S4 | FEAT-LIT-13 | Settle before judgment | User | Takes a settlement during the case to the approver named by the limit, and books it if approved. | Litigation officer | Workbench | FEAT-APD-01 |
| E5 | S4 | FEAT-LIT-14 | Decide and manage an appeal | User | Records the appeal decision, the grounds and the approval, and tracks it to its end. | Litigation officer | LIT, Workbench | FEAT-LIT-12 |
| E5 | S4 | FEAT-LIT-15 | Pay court fees and legal expenses | System | Checks the fee against the schedule, routes it for approval where needed and pays it. | Runs unattended | Partner portal, ALS and GL | FEAT-PAY-05 |
| E5 | S4 | FEAT-LIT-16 | Record the judgment | System | Writes the judgment date and amount onto the case, from the firm or the LIT lawsuit read through v_ace_lawsuit, and opens the enforcement step. | Runs unattended | ACE (ingested from LIT), Workbench | FEAT-LIT-11 |
| E5 | S4 | FEAT-LIT-17 | Trace assets for enforcement | System | Searches the bureau, registries and insurers for assets to enforce against, and reports what it finds. | Runs unattended | NCB, Model gateway | FEAT-AGT-01 |
| E5 | S4 | FEAT-LIT-18 | Apply for the writ and seizure | User | Instructs the writ and the seizure through the firm and tracks it to execution. | Law firm user | Partner portal, LIT | FEAT-LIT-17 |
| E5 | S4 | FEAT-LIT-19 | Follow the LED auction ladder | System | Tracks the enforcement auction through the 100, 90, 80 and 70 percent steps of official value. | Runs unattended | LED portal, LIT | FEAT-LIT-18 |
| E5 | S4 | FEAT-LIT-20 | Record an enforcement deferral with its reason | User | Lets the enforcement owner defer with a coded reason and a review date. Enforcement after judgment has no owner today. | Enforcement owner | Workbench | FEAT-LIT-16 |
| E5 | S4 | FEAT-LIT-21 | File a bankruptcy petition | User | Takes the petition to the approver and files it through the firm. | Enforcement owner | LIT, Partner portal | FEAT-APD-01 |
| E5 | S4 | FEAT-LIT-22 | Match enforcement proceeds to the case | System | Matches money from the LED or the firm to the case and applies it to the balance. | Runs unattended | ALS and GL, LED portal | FEAT-PAY-04 |
| E3 | S5 | FEAT-AST-01 | Take a repossessed vehicle onto the books | System | Links the case to the repossessed vehicle in v_ace_npa_asset, which ACE ingests from RPS and AMIS, by asset_key and starts the holding clock. | Runs unattended | ACE (ingested from RPS and AMIS) | FEAT-CWC-02 |
| E3 | S5 | FEAT-AST-02 | Take a property onto the books after a deed in lieu | System | Links the case to the property in v_ace_npa_asset, which ACE ingests from AMIS, by asset_key when a deed in lieu transfer completes. | Runs unattended | ACE (ingested from AMIS and CCMS) | FEAT-TRT-14 |
| E3 | S5 | FEAT-AST-03 | Take a property onto the books after an LED auction | System | Links the case to the property in v_ace_npa_asset, which ACE ingests from AMIS, by asset_key when the bank takes the property at the enforcement auction. | Runs unattended | ACE (ingested from AMIS), LED portal | FEAT-LIT-19 |
| E3 | S5 | FEAT-AST-04 | Serve the statutory notice and prove delivery | System | Sends the notice the repossession requires and records the WIN proof of delivery read through v_ace_pod. | Runs unattended | WIN, ACE (ingested from WIN) | FEAT-OCC-02 |
| E3 | S5 | FEAT-AST-05 | Track holding age against the provision steps | System | Counts the days held and applies the provision step the policy sets at each threshold. | Runs unattended | AMIS, ALS and GL | FEAT-AST-01 |
| E3 | S5 | FEAT-AST-06 | Record and track the asset stock balance | User | Gives the stock balance an owner and a number on one screen. It has no owner today. | NPA and asset manager | AMIS, RPS | FEAT-AST-05 |
| E3 | S5 | FEAT-AST-07 | Maintain a held property | User | Records maintenance, insurance and custody costs against the asset. | NPA and asset manager | AMIS | FEAT-AST-05 |
| E4 | S5 | FEAT-AST-08 | Evict occupants from a held property | User | Opens and tracks the eviction, which needs Legal and has no legal owner today. | Sale officer | LIT, AMIS | FEAT-AST-07 |
| E3 | S5 | FEAT-AST-09 | Re-appraise a held asset on cycle | System | Raises the re-appraisal order when the holding period passes the re-appraisal interval. | Runs unattended | SVAF | FEAT-VAL-01 |
| E3 | S5 | FEAT-AST-10 | Recommend the disposal route | System | Proposes auction, broker, RAMC, buy-back or rental with the expected return on each. | Runs unattended | Workbench, COLLINS | FEAT-AST-05 |
| E3 | S5 | FEAT-AST-11 | Set the start and floor price | User | Lets the sale officer set the opening price and the floor, with the head of NPA approving the floor. | Sale officer | Workbench, COLLINS | FEAT-AST-10 |
| E3 | S5 | FEAT-AST-12 | Publish the listing | System | Puts the asset on HOME.SCB and the auction portal with its price and schedule. | Runs unattended | HOME.SCB, auction portals | FEAT-AST-11 |
| E4 | S5 | FEAT-AST-13 | Run the descending price schedule | System | Steps the price down on the ladder at each round until a bid clears the floor. | Runs unattended | Auction portals | FEAT-AST-12 |
| E4 | S5 | FEAT-AST-14 | Allocate the asset to an auction vendor by distance | System | Picks one of the four vendors by distance and capacity, as the current rule does. | Runs unattended | Partner portal | FEAT-PRM-03 |
| E4 | S5 | FEAT-AST-15 | Run auction rounds and report bids | User | Lets the vendor run each round and report the bids back into the case. | Auction vendor | Partner portal, auction portals | FEAT-AST-14 |
| E4 | S5 | FEAT-AST-16 | Accept a bid below the floor with a second signature | User | Routes any bid under the floor for a second approval before it can be accepted. | Sale officer | Workbench | FEAT-APD-01 |
| E4 | S5 | FEAT-AST-17 | Re-list on no bid | System | Puts the asset back on the schedule at the next price step when a round closes with no bid. | Runs unattended | Auction portals | FEAT-AST-13 |
| E4 | S5 | FEAT-AST-18 | Enforce the five-day payment term | System | Tracks the winning bidder's payment against the term and releases the asset if it is missed. | Runs unattended | Auction portals, ALS and GL | FEAT-AST-16 |
| E4 | S5 | FEAT-AST-19 | Transfer vehicle registration | System | Prepares and submits the registration transfer through SCIS. | Runs unattended | SCIS, RPS | FEAT-AST-18 |
| E4 | S5 | FEAT-AST-20 | Record a property transfer at the Land Office | User | Tracks the Land Office transfer, which stays a person and officer step. | Sale officer | Land Office, AMIS | FEAT-AST-18 |
| E4 | S5 | FEAT-AST-21 | Apply proceeds and raise the shortfall | System | Applies the sale money to the balance and raises any residual to the next decision. | Runs unattended | ALS and GL | FEAT-PAY-10 |
| E4 | S5 | FEAT-AST-22 | Transfer a pool to RAMC or the joint venture | User | Takes a pool of assets to RAMC with committee approval, and records the transfer. | Sale officer | Partner portal, AMIS | FEAT-APD-01 |
| E4 | S5 | FEAT-AST-23 | Arrange a customer buy-back | User | Opens the buy-back where the former owner repurchases, with the approval the limit requires. | Sale officer | AMIS, ALS and GL | FEAT-AST-10 |
| E4 | S5 | FEAT-AST-24 | Rent a held asset to a third party | User | Records the rental, the debit and the arrears follow-up while the asset is held. | Sale officer | AMIS, ATS | FEAT-AST-05 |
| E4 | S5 | FEAT-AST-25 | Sell through a broker | User | Opens the broker route with its fee and terms, and tracks it to the sale. | Sale officer | Partner portal | FEAT-AST-10 |
| E5 | S6 | FEAT-DBS-01 | Select eligible accounts for sale by rule | System | Applies the eligibility rules, including the 54 percent cap, to pick the sale population. | Runs unattended | Workbench, COLLINS | FEAT-DRI-07 |
| E5 | S6 | FEAT-DBS-02 | Build the lots and estimate the price | System | Groups the accounts into lots and estimates the price from the COLLINS lot economics read through v_ace_score. | Runs unattended | ACE (ingested from COLLINS), Model gateway | FEAT-DBS-01 |
| E5 | S6 | FEAT-DBS-03 | Prepare the masked data tape | System | Builds the data tape with personal data masked under PDPA, ready for the data room. | Runs unattended | ACE database, PII service | FEAT-RDF-15 |
| E5 | S6 | FEAT-DBS-04 | Open the buyer data room | System | Publishes the lot and the masked tape to the data room for qualified buyers. | Runs unattended | Partner portal | FEAT-DBS-03 |
| E6 | S6 | FEAT-DBS-05 | Approve lots, reserve and tiered terms | User | Takes the lot, the reserve price and the terms to the committee for approval. | Head of Asset Liquidity | Workbench | FEAT-APD-01 |
| E6 | S6 | FEAT-DBS-06 | Qualify a buyer against KYC and licensing | System | Runs the KYC, licensing and eligibility checks before a buyer can bid. | Runs unattended | Partner portal, Workbench | FEAT-DBS-04 |
| E6 | S6 | FEAT-DBS-07 | Bar a buyer that fails qualification | System | Removes a buyer from the panel on a license breach and releases the lot to the next bidder. | Runs unattended | Partner portal | FEAT-DBS-06 |
| E6 | S6 | FEAT-DBS-08 | Take buyer bids | User | Lets a qualified buyer bid on a lot through the portal, inside the bid window. | Debt buyer and AMC | Partner portal | FEAT-DBS-06 |
| E6 | S6 | FEAT-DBS-09 | Award the lot and test the price | User | Compares the best bid to the reserve and the model, and awards with the approval the limit requires. | Debt sale officer | Workbench, Partner portal | FEAT-DBS-08 |
| E6 | S6 | FEAT-DBS-10 | Generate the sale agreement and notices | System | Produces the agreement and the customer notices the sale requires. | Runs unattended | Workbench, WIN | FEAT-OCC-07 |
| E6 | S6 | FEAT-DBS-11 | Transfer the data to the buyer | System | Sends the awarded account data to the buyer and records the transfer. | Runs unattended | Partner portal | FEAT-DBS-09 |
| E6 | S6 | FEAT-DBS-12 | Derecognize and post to the general ledger | System | Removes the sold accounts from the book and posts the result to ALS and the ledger. | Runs unattended | ALS and GL | FEAT-DBS-11 |
| E6 | S6 | FEAT-DBS-13 | Handle a buyer put-back claim | User | Reviews a claim that an account should not have been sold, and settles or rejects it. | Debt sale officer | Partner portal, ALS and GL | FEAT-DBS-11 |
| E6 | S6 | FEAT-DBS-14 | Close a case awarded in a sold lot | System | Stops every open action on a case whose account is sold in a lot, and closes it. | Runs unattended | Workbench, ALS and GL | FEAT-DBS-09 |
| E6 | S6 | FEAT-DBS-15 | Confirm buyer remittance | System | Matches the buyer's payment to the award and closes the money side of the lot. | Runs unattended | ALS and GL | FEAT-DBS-12 |
| E6 | S6 | FEAT-DBS-16 | Apply the debt sale cap | System | Holds the sale population inside the policy cap and reports the headroom. | Runs unattended | Workbench | FEAT-DBS-01 |
| E6 | S7 | FEAT-WOF-01 | Run the monthly eligibility scan on both tracks | System | Scans the portfolio each month against the eligibility rules and proposes the write-off population. | Runs unattended | ALS and GL, Workbench | FEAT-DRI-07 |
| E6 | S7 | FEAT-WOF-02 | Apply the tax criteria | System | Tests each proposed account against the tax criteria and records the result. | Runs unattended | Workbench | FEAT-WOF-01 |
| E6 | S7 | FEAT-WOF-03 | Prepare the write-off pack | System | Assembles the committee pack from the case facts, the documents and the recovery history. | Runs unattended | Workbench, the Workbench document hub | FEAT-WOF-01 |
| E6 | S7 | FEAT-WOF-04 | Remove a case from the proposed population | User | Lets the write-off team take a case out of the population before committee, with a reason. | Write-off team member | Workbench | FEAT-WOF-03 |
| E6 | S7 | FEAT-WOF-05 | Route the population to the committee and schedule it | System | Sends the pack to the committee queue and books it into the monthly meeting. | Runs unattended | Workbench | FEAT-WOF-03 |
| E6 | S7 | FEAT-WOF-06 | Approve a write-off inside the limit | User | Lets the committee approve within its delegation and records the limit applied. | Write-off committee member | Workbench | FEAT-APD-02 |
| E6 | S7 | FEAT-WOF-07 | Reject a write-off | User | Lets the committee reject, with a reason that returns the case to recovery. | Write-off committee member | Workbench | FEAT-WOF-06 |
| E6 | S7 | FEAT-WOF-08 | Defer a write-off | User | Lets the committee defer with a review date, and holds the case until then. | Write-off committee member | Workbench | FEAT-WOF-06 |
| E6 | S7 | FEAT-WOF-09 | Post an approved write-off | System | Posts the write-off to ALS and the general ledger and releases the provision. | Runs unattended | ALS and GL | FEAT-WOF-06 |
| E6 | S7 | FEAT-WOF-10 | Send provision inputs to Finance | System | Produces the provision file Finance needs from the posted population. | Runs unattended | ALS and GL | FEAT-WOF-09 |
| E6 | S7 | FEAT-WOF-11 | Reconcile the approved and posted populations | System | Compares what the committee approved to the GL postings read through v_ace_write_off, and raises every difference. | Runs unattended | ALS and GL, Workbench | FEAT-WOF-09 |
| E6 | S7 | FEAT-WOF-12 | Work the write-off exception loop | User | Opens the exception path for a case the rules cannot clear. This loop has no owner today. | Write-off committee member | Workbench | FEAT-WOF-11 |
| E6 | S7 | FEAT-WOF-13 | Close the case after the retention period | System | Closes the case once the retention period has run and no action is open. | Runs unattended | Workbench | FEAT-DCM-17 |
| E6 | S7 | FEAT-WOF-14 | Change the eligibility or tax criteria | Admin | Lets the center of excellence change the criteria as a versioned rule load. | Center of excellence analyst | Workbench, Rules component | FEAT-CWC-14 |
| E6 | S7 | FEAT-WOF-15 | Record a customer payment after charge-off | System | Takes a payment on a charged-off balance, applies it and records the recovery. | Runs unattended | ALS and GL | FEAT-PAY-01 |
| E6 | S7 | FEAT-WOF-16 | Sell a post charge-off population | User | Opens the sale of charged-off accounts, with the approval the limit requires. | Debt sale officer | Partner portal, ALS and GL | FEAT-DBS-09 |
| E7 | S8 | FEAT-DVF-01 | Run X1 dispute and complaint end to end | User | Takes the dispute from detection through the evidence pack to resolution and the return point. | Complaint officer | Workbench, Document hub | FEAT-DVH-04 |
| E7 | S8 | FEAT-DVF-02 | Run X2 vulnerability and hardship end to end | User | Takes the case to the specialist queue with contact limits, through to the hardship decision. | Hardship and vulnerability specialist | Workbench, EFS | FEAT-DVH-04 |
| E7 | S8 | FEAT-DVF-03 | Run X3 deceased customer end to end | User | Stops contact, notifies heirs, files the insurance claim and settles the estate position. | Hardship and vulnerability specialist | Workbench, the Workbench document hub | FEAT-DVH-04 |
| E7 | S8 | FEAT-DVF-04 | Run X4 fraud end to end | User | Refers to the fraud team, tracks the investigation and routes the case on the outcome. | Fraud investigator | Aric, Workbench | FEAT-DVH-04 |
| E7 | S8 | FEAT-DVF-05 | Run X5 bankruptcy and seizure end to end | User | Stops direct collection and files the claim with the receiver or the LED before the deadline. | Legal counsel | LIT, Workbench | FEAT-DVH-04 |
| E7 | S8 | FEAT-DVF-06 | Run X6 lost contact and skip trace end to end | System | Runs the skip trace through the bureau, internal data and agency sources and routes on the result. | Runs unattended | NCB, EFS, Partner portal | FEAT-DVF-01 |
| E7 | S8 | FEAT-DVF-07 | Run X7 collateral event end to end | User | Files the insurance claim, re-appraises the collateral and returns the case to the route decision. | Case owner | SVAF, Workbench | FEAT-GUA-08 |
| E7 | S8 | FEAT-DVF-08 | Review an override | User | Puts overrides in front of the review forum, with the reason and the outcome of each. | Risk and model risk officer | Workbench | FEAT-APD-07 |
| E7 | S8 | FEAT-DVF-09 | Match a complaint to the preceding contact | User | Links each complaint to the contact that caused it, which is how conduct is measured. | Conduct and QA officer | Workbench, EFS | FEAT-OCC-05 |
| E7 | S8 | FEAT-DVF-10 | Handle a contact sent while a block is on | User | Opens the breach path when a message goes out against a contact stop. | Conduct and QA officer | Workbench | FEAT-OCC-06 |
| E6 | S9 | FEAT-PRM-01 | Onboard a partner and set terms | User | Takes a partner onto the panel with its contract, fee schedule, service levels and scope. | Partner and agency manager | Partner portal | FEAT-OCC-13 |
| E6 | S9 | FEAT-PRM-02 | Hold the partner panel and fee schedule as data | Admin | Keeps every panel, fee schedule and service level as versioned reference data. | Reference data administrator | Workbench | FEAT-CWC-23 |
| E6 | S9 | FEAT-PRM-03 | Allocate work by measured return | System | Places work with the partner the scorecard rule picks, not by rotation or habit. | Runs unattended | Partner portal, Rules component | FEAT-PRM-02 |
| E6 | S9 | FEAT-PRM-04 | Override an allocation with a reason | User | Lets the partner manager place work differently, with the reason recorded. | Partner and agency manager | Partner portal | FEAT-PRM-03 |
| E6 | S9 | FEAT-PRM-05 | Receive a partner result into the case | System | Takes contact, promise and cash results from the portal onto the case the same day. | Runs unattended | Partner portal | FEAT-PRM-03 |
| E6 | S9 | FEAT-PRM-06 | Place a charged-off account with an agency | User | Places post charge-off accounts with an agency under the placement rule. | Partner and agency manager | Partner portal | FEAT-PRM-03 |
| E6 | S9 | FEAT-PRM-07 | Match a recovery and calculate the agency fee | System | Matches money recovered by an agency to the case and works out the fee due. | Runs unattended | ALS and GL, Partner portal | FEAT-PAY-01 |
| E7 | S9 | FEAT-PRM-08 | Score partners monthly | System | Builds the scorecard from the measured results and publishes it to the panel. | Runs unattended | Partner portal, Power BI | FEAT-PRM-05 |
| E7 | S9 | FEAT-PRM-09 | Approve partner fees | User | Checks the fee claim against the schedule and the result, and approves it. | Partner and agency manager | Partner portal | FEAT-PRM-07 |
| E7 | S9 | FEAT-PRM-10 | Hold a partner review | User | Runs the review against the six points every partner type is managed on, and records the actions. | Partner and agency manager | Partner portal | FEAT-PRM-08 |
| E7 | S9 | FEAT-PRM-11 | Issue a notice on a missed target | User | Sends the contractual notice when a partner misses its targets, and starts the cure period. | Partner and agency manager | Partner portal | FEAT-PRM-08 |
| E7 | S9 | FEAT-PRM-12 | End a partner contract and recall the work | User | Closes the contract and pulls every open case back for re-selection. | Partner and agency manager | Partner portal | FEAT-PRM-11 |
| E7 | S9 | FEAT-PRM-13 | Check partner conduct | System | Samples partner contacts and complaints against the conduct rules and raises breaches. | Runs unattended | Partner portal | FEAT-PRM-08 |
| E7 | S9 | FEAT-PRM-14 | Manage extra costs and services on an asset | User | Records and approves additional partner costs on a held asset. | Partner and agency manager | Partner portal, AMIS | FEAT-AST-07 |
| E7 | S9 | FEAT-PRM-15 | Capture field work through the field app | User | Lets the field collector record visits, photos and bills against the case from the field. | Field collector | Field app, the Workbench document hub | FEAT-DCM-21 |
| E4 | P6 | FEAT-COM-01 | View the offer on LINE and web | User | Lets the customer see the offer the bank has made, on the channel they use. | Customer (borrower) | LINE OA, HOME.SCB | FEAT-OCC-04 |
| E4 | P6 | FEAT-COM-02 | Accept an offer in self-service | User | Lets the customer accept without a call or a branch visit, which records the acceptance on the case. | Customer (borrower) | LINE OA, HOME.SCB | FEAT-COM-01 |
| E4 | P6 | FEAT-COM-03 | Pay in self-service | User | Lets the customer pay against the plan or the settlement from the same screen. | Customer (borrower) | HOME.SCB, payments | FEAT-COM-01 |
| E4 | P6 | FEAT-COM-04 | Raise a dispute in self-service | User | Lets the customer raise a dispute, which opens X1 and applies the contact stop. | Customer (borrower) | LINE OA, HOME.SCB | FEAT-DVH-05 |
| E4 | P6 | FEAT-COM-05 | Maintain the contact repository | Admin | Reads the contact points for every party from v_ace_contact and keeps verification and consent state per channel in contact_point_ext. | Compliance and PDPA officer | Workbench, ACE | FEAT-RDF-04 |
| E4 | P6 | FEAT-COM-06 | Record a custody movement of a document | System | Tracks a physical document leaving and returning, so the original is never lost. | Runs unattended | the Workbench document hub | FEAT-DCM-19 |
| E4 | P6 | FEAT-COM-07 | Answer a legal or audit document request | User | Returns the documents and the index entries a legal or audit request asks for. | Legal counsel | Workbench, the Workbench document hub | FEAT-DCM-06 |
| E4 | P6 | FEAT-COM-08 | Apply retention on case closure | System | Applies the retention class to every document on the case when the case closes. | Runs unattended | the Workbench document hub, Blob storage | FEAT-DCM-17 |
| E4 | P8 | FEAT-PAY-03 | Match a settlement payment | System | Matches a settlement payment to the treatment and closes the money side. | Runs unattended | ALS and GL | FEAT-PAY-01 |
| E4 | P8 | FEAT-PAY-04 | Match auction and enforcement proceeds | System | Matches money from an auction, a broker or the LED to the right case. | Runs unattended | ALS and GL, LED portal | FEAT-PAY-01 |
| E4 | P8 | FEAT-PAY-05 | Calculate fees and charges | System | Works out partner fees, court fees and charges from the fee tables held as data. | Runs unattended | Workbench, ALS and GL | FEAT-CWC-23 |
| E4 | P8 | FEAT-PAY-06 | Post a settlement booking to ALS | System | Writes the agreed settlement terms to ALS and reads the booked position back through v_ace_account after the next ACE batch. | Runs unattended | ALS and GL | FEAT-CHO-08 |
| E4 | P8 | FEAT-PAY-07 | Post to the general ledger | System | Posts the accounting entries for settlements, sales and write-offs to the ledger. | Runs unattended | ALS and GL | FEAT-PAY-06 |
| E6 | P8 | FEAT-PAY-08 | Produce provision inputs | System | Builds the provision inputs Finance needs from the case and asset positions. | Runs unattended | ALS and GL | FEAT-PAY-07 |
| E4 | P8 | FEAT-PAY-09 | Run the deed in lieu rental auto-debit | System | Takes the rental by auto-debit, issues the receipt and follows up arrears. | Runs unattended | ATS, AMIS | FEAT-TRT-16 |
| E4 | P8 | FEAT-PAY-10 | Apply proceeds to the case balance | System | Applies every receipt to the balance in the order the policy sets. | Runs unattended | ALS and GL | FEAT-PAY-04 |
| E4 | P8 | FEAT-PAY-11 | Reconcile money movements daily | System | Compares what the Workbench matched to the ALS position read through v_ace_payment and v_ace_account, and to the ledger, every day. | Runs unattended | ALS and GL | FEAT-RDF-11 |
| E6 | P9 | FEAT-RPT-06 | Track benefit realisation | User | Tracks the measures in the benefit model against the baseline, monthly. | Finance and CFO delegate | Power BI | FEAT-RPT-01 |
| E8 | P9 | FEAT-RPT-07 | Produce regulatory returns | System | Builds the regulatory extracts from the data products and the decision log. | Runs unattended | Power BI, Data lake | FEAT-RPT-04 |
| E8 | P9 | FEAT-RPT-10 | Classify, stage and re-age an account | System | Applies the classification and re-ageing rules and recomputes the segment when they change. | Runs unattended | ALS and GL, Workbench | FEAT-RDF-03 |
| E3 | P10 | FEAT-AGT-12 | Change an autonomy level | Admin | Changes the autonomy level for one agent and one decision, as a versioned configuration row. | Risk and model risk officer | Workbench, Model gateway | FEAT-CWC-22 |
| E3 | P10 | FEAT-AGT-13 | Detect model drift and raise a decision | System | Watches calibration and drift, and raises a decision with an owner and a date on a breach. | Runs unattended | Model gateway, Power BI | FEAT-AGT-06 |
| E8 | P10 | FEAT-AGT-14 | Run a champion and challenger test | Admin | Runs two rule or model versions side by side and compares the outcome. | Center of excellence analyst | Model gateway | FEAT-AGT-05 |
| E8 | P10 | FEAT-AGT-15 | Raise or lower an autonomy level with approval | Admin | Steps an agent up on measured evidence, and drops it on a breach, with the approval each needs. | Risk and model risk officer | Workbench | FEAT-AGT-12 |
| E8 | P10 | FEAT-AGT-16 | Review agent risk at the committee | User | Puts agent performance, overrides and incidents in front of the strategy and model committee. | Risk and model risk officer | Power BI | FEAT-AGT-06 |
| E8 | P4 | FEAT-ADM-01 | Run the full administration screens | Admin | Gives administration one place for roles, queues, parameters, templates, panels and autonomy. | Platform administrator | Workbench | FEAT-CWC-22 |
| E8 | P4 | FEAT-ADM-02 | Change a decision rule through the administration screens | Admin | Lets the center of excellence change a rule, test it and put it in force as a new version. | Center of excellence analyst | Workbench, Rules component | FEAT-CWC-14 |
| E8 | P4 | FEAT-ADM-03 | Move an approval limit | Admin | Changes a delegated limit, with Risk approving and the change versioned. | Center of excellence analyst | Workbench | FEAT-ACA-06 |
| E8 | P4 | FEAT-ADM-04 | Set the treatment policy by product | Admin | Lets the product head set the bands, floors and ranges for their product. | Product head (Mortgage, HP, SSME) | Workbench | FEAT-CWC-25 |
| E8 | P4 | FEAT-ADM-05 | Add a letter template with Compliance approval | Admin | Adds a new template through the approval path and records who approved it. | Center of excellence analyst | Workbench | FEAT-DRI-15 |
| E8 | P4 | FEAT-ADM-06 | Roll back a configuration version | Admin | Returns any versioned table to its previous version and records the rollback. | Platform administrator | Workbench | FEAT-CWC-15 |
| E8 | P4 | FEAT-ADM-07 | Publish a panel change | Admin | Puts a partner panel change in force with an effective date. | Partner and agency manager | Workbench, Partner portal | FEAT-PRM-02 |
| E8 | P4 | FEAT-ADM-08 | Run a QA sample against the rule version applied | User | Samples closed decisions and tests each against the rule version that was in force. | Conduct and QA officer | Workbench | FEAT-DRI-03 |
| E8 | P4 | FEAT-ADM-09 | Return a defective pack | System | Sends a pack that fails the check back to its owner with the defects named. | Runs unattended | Workbench | FEAT-LIT-05 |
| E8 | P4 | FEAT-ADM-10 | Detect a broken hash chain in the decision log | System | Tests the log chain and raises a control breach if a record does not verify. | Runs unattended | Workbench | FEAT-DRI-01 |
| E8 | P4 | FEAT-ADM-11 | Handle a data subject request | User | Works a PDPA access, correction or erasure request inside the statutory period. | Compliance and PDPA officer | Workbench | FEAT-ACA-05 |
| E8 | P4 | FEAT-ADM-12 | Manage an incident | Admin | Runs the incident path: detect, hold, fix, record and report. | Platform administrator | Log Analytics, Workbench | FEAT-DRI-18 |
| E8 | P4 | FEAT-ADM-13 | Refer a case to Aric | System | Sends a case to Aric where the fraud rules require it, and takes the result back. | Runs unattended | Aric | FEAT-DVF-04 |
| E8 | P4 | FEAT-ADM-14 | Control access by role and by agent | Admin | Reviews and sets what each role and each agent may read and do, and reports the matrix. | Security administrator | Workbench, Entra ID | FEAT-ACA-04 |

## APIs

| Endpoints first available in Epics 3 to 8 |  |  |  |  |  |
|---|---|---|---|---|---|
| From the API specification. |  |  |  |  |  |
| Epic | Method | Path | Purpose | Module | Access |
| E4 | GET | /cases/{caseId}/recommendation | Read the current recommendation with reasons and the expected return by route | P7 | Decision log R |
| E3 | PATCH | /treatments/{treatmentId} | Change the terms of a draft treatment | S2 | Treatment and offer U |
| E3 | POST | /treatments/{treatmentId}/submit | Submit a treatment for approval | S2 | Treatment and offer U |
| E4 | POST | /cases/{caseId}/route | Submit the route decision for approval, with an override reason where it departs from the recommendation | S1 | Treatment and offer U |
| E4 | POST | /cases/{caseId}/guarantee-claims | Open a guarantee or TCG claim | S3 | Treatment and offer C |
| E4 | PATCH | /guarantee-claims/{claimId} | Record the claim result | S3 | Treatment and offer U |
| E5 | POST | /cases/{caseId}/legal-actions | Open a legal action and its pack | S4 | Litigation C |
| E5 | GET | /legal-actions/{legalActionId} | Read a legal action with pack, instruction, hearings and judgment | S4 | Litigation R |
| E5 | PATCH | /legal-actions/{legalActionId} | Record a filing, judgment or enforcement step | S4 | Litigation U |
| E5 | POST | /legal-actions/{legalActionId}/hearings | Add a hearing date | S4 | Litigation U |
| E3 | GET | /assets | List assets held with age, holding cost and sale status | S5 | Asset and disposal R |
| E3 | GET | /assets/{assetId} | Read one asset with title, condition, valuations, costs and listing | S5 | Asset and disposal R |
| E3 | POST | /assets/{assetId}/valuations | Order or record a valuation | S5 | Asset and disposal C |
| E3 | POST | /assets/{assetId}/listings | Set the list price and floor and send for approval | S5 | Asset and disposal C |
| E4 | POST | /listings/{listingId}/rounds | Record an auction round and its result | S5 | Asset and disposal U |
| E5 | POST | /debt-sale-lots | Create a lot from eligible accounts | S6 | Debt sale C |
| E5 | GET | /debt-sale-lots/{lotId} | Read a lot with its accounts, reserve and bids | S6 | Debt sale R |
| E6 | POST | /debt-sale-lots/{lotId}/award | Award a lot to a buyer after the bids close | S6 | Debt sale A |
| E6 | POST | /write-off-scans | Run the monthly write-off scan for a cut-off date | S7 | Write-off and posting C |
| E6 | POST | /write-offs/{writeOffId}/committee-decision | Record the committee decision for a write-off | S7 | Write-off and posting A |
| E4 | POST | /proceeds/{proceedsId}/match | Match a receipt to a case and account | P8 | Write-off and posting U |
| E4 | POST | /cases/{caseId}/instructions | Issue an instruction to a partner by rule | S9 | Partner portal C |
| E4 | GET | /partner/instructions | List the instructions placed with the caller's firm | S9 | Partner portal R |
| E4 | POST | /partner/instructions/{instructionId}/accept | Accept or decline an instruction | S9 | Partner portal U |
| E4 | POST | /partner/instructions/{instructionId}/results | Record a result with its documents | S9 | Partner portal U |
| E6 | POST | /partner/instructions/{instructionId}/invoices | Submit a fee invoice | S9 | Partner portal C |
| E5 | GET | /partner/data-room/{lotId} | Read the lot tape and documents for an admitted buyer | S6 | Partner portal R |
| E5 | POST | /partner/data-room/{lotId}/bids | Submit a bid on a lot | S6 | Partner portal C |

## Integrations

| Integrations first used in Epics 3 to 8 |  |  |  |  |  |  |
|---|---|---|---|---|---|---|
| From the integration inventory. Inbound sources arrive through ACE ingestion and are read through the read-only recovery.v_ace_* views (D-RCV-35); outbound interfaces are unchanged. |  |  |  |  |  |  |
| Epic | ID | System | Purpose | Direction | Approach | Frequency |
| E3 | INT-03 | Core bank (ALS) | Restructure, settlement and write-off bookings | Out | Booked by the officer; confirmed when the next ACE batch shows the booking in v_ace_account | As approved |
| E3 | INT-12 | AMIS | Assets held, book values and asset sales | In, into ACE | ACE ingestion, read through v_ace_npa_asset and v_ace_npa_sale | Monthly |
| E3 | INT-13 | RPS | Repossessed vehicles and stock | In, into ACE | ACE ingestion, read through v_ace_npa_asset | Weekly |
| E6 | INT-16 | GL | Write-off postings | In, into ACE | ACE ingestion, read through v_ace_write_off | Monthly |
| E5 | INT-25 | Debt buyers | Debt sale data tape for an awarded lot | Out | File through the data room | Per lot |
| E3 | INT-26 | NLEADS | Credit approval for restructure plans | Out | Submitted by the officer in NLEADS | As needed |
| E3 | INT-27 | HOME.SCB | Listings of assets for sale | Out | Not available today; published by the sale officer | As listed |
| E4 | INT-28 | SCIS | Vehicle registration transfer | Out | Not available today; prepared by the officer | As needed |
| E4 | INT-29 | Thai Credit Guarantee Corporation | Quota and claim submission | Both | Not available today; entered and filed by the guarantee officer | As needed |
| E7 | INT-30 | NCB | Contact tracing for lost contact | In | Not available today; by the officer | As needed |
| E8 | INT-31 | Aric | Fraud referral | Out | Not available today; by the fraud investigator | As needed |
| E5 | INT-33 | Legal Execution Department and courts | Enforcement and court records | In | Through the law firms in the partner portal | As entered |

## Document control

| Document control |  |
|---|---|
| Recovery Workbench Epics 3 to 8 Specification v3 |  |
| Item | Detail |
| Document | Recovery Workbench epics 3 to 8 at specification level |
| Version | 3 |
| Date | 15 November 2026 |
| Prepared by | Henka Group |
| Decision | D-RCV-35 |
| Change | Version 3, 15 November 2026 (D-RCV-35): the Workbench loads no source data. AMIS, RPS, GL, SVAF, COLLINS, LIT and WIN proof of delivery arrive through ACE ingestion (RWB-ACE-001) and are read through the read-only recovery.v_ace_* views. Integrations 2.4 to 5.4, the architecture data rows and 17 feature descriptions re-worded. Outbound interfaces unchanged. |

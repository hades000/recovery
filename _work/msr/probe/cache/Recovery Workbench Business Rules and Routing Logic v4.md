## Sheet: Rules

| Business rules and routing logic |  |  |  |  |  |  |  |  |  |  |
|---|---|---|---|---|---|---|---|---|---|---|
| 448 rules in ten route sets. Hit policy Unique: in a route set, for one state and one event, one condition holds. |  |  |  |  |  |  |  |  |  |  |
| Rule | Route set | Decision | From state | Event | Condition | Action | To state | Owner | Systems | Timer |
| R-RES-01 | Restructure | D5, D6 | ROUTE_APPROVED_RESTRUCTURE | ROUTE_APPROVED | decision.approved and route = R1 | Open the treatment record and ask COLLINS for the restructure proposal | PROPOSED_IN_COLLINS | Workbench | Workbench, COLLINS | None |
| R-RES-02 | Restructure | D5, D6 | PROPOSED_IN_COLLINS | RESTRUCTURE_PROPOSED | collins_proposal = eligible | Route the case through EFS into the FCR queue | IN_FCR_QUEUE | Restructuring officer, FCR | COLLINS, EFS, Workbench | 2 working days |
| R-RES-03 | Restructure | D5, D6 | PROPOSED_IN_COLLINS | NO_PROPOSAL_RETURNED | collins_proposal = none | Return the case to the route decision with reason no_restructure_option | BACK_TO_ROUTE_DECISION | Case owner | COLLINS, Workbench | None |
| R-RES-04 | Restructure | D5, D6 | IN_FCR_QUEUE | CASE_PICKED_UP | allocation rule matched and officer available | Assign the case to a restructuring officer and start the offer clock | WITH_FCR_OFFICER | Restructuring officer, FCR | EFS, Workbench | 2 working days |
| R-RES-05 | Restructure | D5, D6 | IN_FCR_QUEUE | QUEUE_SLA_BREACHED | queue_age > fcr_queue_limit | Escalate to the FCR team manager and re-allocate | IN_FCR_QUEUE | FCR team manager | Workbench | None |
| R-RES-06 | Restructure | D5, D6 | WITH_FCR_OFFICER | AFFORDABILITY_REQUIRED | treatment_type = TDR | Send the case to ACE for affordability and plan calculation | AFFORDABILITY_IN_ACE | ACE and TDR system | ACE and TDR, Workbench | 2 working days |
| R-RES-07 | Restructure | D5, D6 | AFFORDABILITY_IN_ACE | AFFORDABILITY_PASSED | affordability_result = pass | Return the calculated plan to the officer and build the offer | WITH_FCR_OFFICER | Restructuring officer, FCR | ACE and TDR, Workbench | None |
| R-RES-08 | Restructure | D5, D6 | AFFORDABILITY_IN_ACE | AFFORDABILITY_FAILED | affordability_result = fail | Return the case to the route decision with reason affordability_failed | BACK_TO_ROUTE_DECISION | Case owner | ACE and TDR, Workbench | None |
| R-RES-09 | Restructure | D5, D6 | WITH_FCR_OFFICER | OFFER_PREPARED | offer inside the approved range and deviation_flag = N | Generate the offer letter and send it on a consented channel | OFFER_WITH_CUSTOMER | Customer | Workbench, WIN and DMS, LINE, SMS | offer validity 14 days |
| R-RES-10 | Restructure | D5, D6 | WITH_FCR_OFFICER | OFFER_PREPARED | offer outside the range or deviation_flag = Y | Route the offer to credit approval; 44% of TDR cases deviate today | AWAITING_CREDIT_APPROVAL | Credit approval committee | Workbench | 3 working days |
| R-RES-11 | Restructure | D5, D6 | AWAITING_CREDIT_APPROVAL | CREDIT_APPROVED | final_call = approved | Release the offer and send it to the customer | OFFER_WITH_CUSTOMER | Customer | Workbench, WIN and DMS | offer validity 14 days |
| R-RES-12 | Restructure | D5, D6 | AWAITING_CREDIT_APPROVAL | CREDIT_DECLINED | final_call = rejected | Record the reason against the limit applied | DECLINED_BY_CREDIT | Restructuring officer, FCR | Workbench | None |
| R-RES-13 | Restructure | D5, D6 | AWAITING_CREDIT_APPROVAL | APPROVAL_SLA_BREACHED | approval_age > approval_escalation_limit | Escalate to the head of credit | AWAITING_CREDIT_APPROVAL | Head of credit | Workbench | None |
| R-RES-14 | Restructure | D5, D6 | DECLINED_BY_CREDIT | DECLINE_RECORDED | Any | Return the case to the route decision with reason credit_declined | BACK_TO_ROUTE_DECISION | Case owner | Workbench | None |
| R-RES-15 | Restructure | D5, D6 | OFFER_WITH_CUSTOMER | CUSTOMER_COUNTER_OFFERED | counter_amount outside the current range | Return the case to the officer with the counter-offer and the gap | WITH_FCR_OFFICER | Restructuring officer, FCR | Workbench | 2 working days |
| R-RES-16 | Restructure | D5, D6 | OFFER_WITH_CUSTOMER | CUSTOMER_SIGNED | signed = Y and signature verified | Route the case to operations to complete the booking | WITH_OPS_BOOKING | Operations (booking) | EasyApp e-signature, Workbench | 1 working day |
| R-RES-17 | Restructure | D5, D6 | OFFER_WITH_CUSTOMER | CUSTOMER_DECLINED | declined = Y | Return the case to its prior status in COLLINS | RETURNED_TO_COLLINS | Workbench | COLLINS, EFS, Workbench | None |
| R-RES-18 | Restructure | D5, D6 | OFFER_WITH_CUSTOMER | OFFER_EXPIRED | signed = N and offer_validity passed | Return the case to its prior status in COLLINS | RETURNED_TO_COLLINS | Workbench | COLLINS, EFS, Workbench | None |
| R-RES-19 | Restructure | D5, D6 | OFFER_WITH_CUSTOMER | DEVIATION_RAISED | contact stop raised by X1 or X2 | Stop the offer channel and hold the offer clock | OFFER_WITH_CUSTOMER | Deviation owner | Workbench | None |
| R-RES-20 | Restructure | D5, D6 | RETURNED_TO_COLLINS | PRIOR_STATUS_RESTORED | Any | Restore the status held before the restructure and re-open the route decision | BACK_TO_ROUTE_DECISION | Case owner | COLLINS, Workbench | None |
| R-RES-21 | Restructure | D5, D6 | WITH_OPS_BOOKING | BOOKING_SUBMITTED | treatment_type = TDR | Submit the plan to NLEADS for credit approval and await the callback | WITH_OPS_BOOKING | Operations (booking) | NLEADS, Workbench | 2 working days |
| R-RES-22 | Restructure | D5, D6 | WITH_OPS_BOOKING | BOOKING_CONFIRMED | ALS and NLEADS both acknowledge | Record the booking reference and set the payment schedule | BOOKED_IN_ALS_NLEADS | Workbench | ALS core, NLEADS | None |
| R-RES-23 | Restructure | D5, D6 | WITH_OPS_BOOKING | BOOKING_REJECTED | ALS rejects the booking | Put the error on the officer queue and keep the case with operations | WITH_OPS_BOOKING | Operations (booking) | ALS core, Workbench | 1 working day |
| R-RES-24 | Restructure | D5, D6 | WITH_OPS_BOOKING | NLEADS_CALLBACK_MISSING | callback_age > callback_limit | Escalate the missing callback and hold the booking | WITH_OPS_BOOKING | Operations (booking) | NLEADS, Workbench | None |
| R-RES-25 | Restructure | D5, D6 | BOOKED_IN_ALS_NLEADS | SCHEDULE_SET | first_due_date set | Start the plan timers and move the plan to running | PLAN_RUNNING | Restructuring officer, FCR | Workbench | None |
| R-RES-26 | Restructure | D5, D6 | PLAN_RUNNING | PAYMENT_RECEIVED | payment matched to the installment | Advance the next due date and record the payment | PLAN_RUNNING | Workbench | ALS core, Workbench | None |
| R-RES-27 | Restructure | D5, D6 | PLAN_RUNNING | PAYMENT_MISSED | due_date passed and no payment matched | Raise plan.payment.missed and start the cure period | PLAN_CURE_PERIOD | Case owner | ALS core, Workbench | cure_period_days from reference data |
| R-RES-28 | Restructure | D5, D6 | PLAN_CURE_PERIOD | PAYMENT_RECEIVED_LATE | payment received inside the cure period | Clear the miss and return the plan to running | PLAN_RUNNING | Workbench | ALS core, Workbench | None |
| R-RES-29 | Restructure | D5, D6 | PLAN_CURE_PERIOD | CURE_PERIOD_EXPIRED | no payment and cure_period passed | Increment the break count and mark the plan broken | PLAN_BROKEN | Case owner | Workbench | None |
| R-RES-30 | Restructure | D5, D6 | PLAN_BROKEN | BREAK_RECORDED | break_count < max_breaks | Return the case to the route decision with reason broken_plan | BACK_TO_ROUTE_DECISION | Case owner | Workbench | 5 working days |
| R-RES-31 | Restructure | D5, D6 | PLAN_BROKEN | BREAK_RECORDED | break_count >= max_breaks | Bar a further restructure on this case | RESTRUCTURE_BARRED | Case owner | Workbench | None |
| R-RES-32 | Restructure | D5, D6 | RESTRUCTURE_BARRED | BAR_APPLIED | Any | Exclude R1 from the open routes and re-run the route decision | BACK_TO_ROUTE_DECISION | Case owner | Workbench | None |
| R-RES-33 | Restructure | D5, D6 | PLAN_RUNNING | FINAL_INSTALLMENT_PAID | installments_paid = installments_due | Close the treatment, release the collateral and close the case | PLAN_COMPLETED | Workbench | ALS core, CCMS, Workbench | None |
| R-RES-34 | Restructure | D5, D6 | PLAN_RUNNING | DEVIATION_RAISED | deviation_open in (X1,X2,X3,X4,X5) | Pause the plan timers and hold the case with the deviation owner | PLAN_RUNNING | Deviation owner | Workbench | None |
| R-RES-35 | Restructure | D5, D6 | WITH_FCR_OFFICER | OFFER_PREPARED | no condition matched, or affordability data is missing | Hold the case, name the missing field and raise a task for the owner | UNMATCHED_EXCEPTION | Case owner | Workbench | same day |
| R-RES-36 | Restructure | D5, D6 | PLAN_BROKEN | BREAK_RECORDED | break_count is missing or not a number | Hold the case, name the missing field and raise a task for the owner | UNMATCHED_EXCEPTION | Case owner | Workbench | same day |
| R-RES-37 | Restructure | D5, D6 | UNMATCHED_EXCEPTION | MANUAL_DECISION_RECORDED | Any | Case owner records the decision and the missing field; the rule gap is logged for the center of excellence | BACK_TO_ROUTE_DECISION | Case owner | Workbench | 2 working days |
| R-SET-01 | Settlement | D6.4 | ROUTE_APPROVED_SETTLEMENT | ROUTE_APPROVED | decision.approved and route = R2 | Calculate the payoff from ALS and set the range from reference data | PAYOFF_AND_RANGE_SET | Workbench | ALS core, Workbench | None |
| R-SET-02 | Settlement | D6.4 | PAYOFF_AND_RANGE_SET | RANGE_SET | payoff_as_at inside the freshness limit | Open the treatment record and place the case in the FCR queue | WITH_FCR_OFFICER_SET | Restructuring officer, FCR | EFS, Workbench | 2 working days |
| R-SET-03 | Settlement | D6.4 | PAYOFF_AND_RANGE_SET | PAYOFF_STALE | payoff_as_at older than the freshness limit | Block the step and request a fresh payoff through EAPI | PAYOFF_AND_RANGE_SET | Workbench | ALS core, Workbench | None |
| R-SET-04 | Settlement | D6.4 | WITH_FCR_OFFICER_SET | OFFER_PREPARED | offer_amount between settlement_range_low and settlement_range_high | Generate the settlement letter and send it on a consented channel | OFFER_WITH_CUSTOMER_SET | Customer | Workbench, WIN and DMS, LINE, SMS | offer validity 14 days |
| R-SET-05 | Settlement | D6.4 | WITH_FCR_OFFICER_SET | OFFER_PREPARED | offer_amount < floor_price | Route the offer to the approver with the gap to the floor | AWAITING_APPROVAL_SET | Credit approval committee | Workbench | 3 working days |
| R-SET-06 | Settlement | D6.4 | AWAITING_APPROVAL_SET | APPROVAL_GRANTED | final_call = approved | Release the offer and send it to the customer | OFFER_WITH_CUSTOMER_SET | Customer | Workbench, WIN and DMS | offer validity 14 days |
| R-SET-07 | Settlement | D6.4 | AWAITING_APPROVAL_SET | APPROVAL_REFUSED | final_call = rejected | Record the reason and the gap to the floor | DECLINED_BY_APPROVER_SET | Restructuring officer, FCR | Workbench | None |
| R-SET-08 | Settlement | D6.4 | DECLINED_BY_APPROVER_SET | DECLINE_RECORDED | Any | Return the case to the route decision with reason below_floor_refused | RETURNED_TO_ROUTE_SET | Case owner | Workbench | None |
| R-SET-09 | Settlement | D6.4 | OFFER_WITH_CUSTOMER_SET | CUSTOMER_COUNTER_OFFERED | counter_amount < floor_price | Return the case to the officer and re-test against the floor | WITH_FCR_OFFICER_SET | Restructuring officer, FCR | Workbench | 2 working days |
| R-SET-10 | Settlement | D6.4 | OFFER_WITH_CUSTOMER_SET | CUSTOMER_SIGNED | signed = Y | Route the case to operations and raise the payment instruction | WITH_OPS_SETTLEMENT | Operations (booking) | EasyApp e-signature, Workbench | 1 working day |
| R-SET-11 | Settlement | D6.4 | OFFER_WITH_CUSTOMER_SET | OFFER_EXPIRED | signed = N and offer_validity passed | Return the case to the route decision with reason offer_expired | RETURNED_TO_ROUTE_SET | Case owner | Workbench | None |
| R-SET-12 | Settlement | D6.4 | OFFER_WITH_CUSTOMER_SET | DEVIATION_RAISED | contact stop raised by X1 or X2 | Stop the offer channel and hold the offer clock | OFFER_WITH_CUSTOMER_SET | Deviation owner | Workbench | None |
| R-SET-13 | Settlement | D6.4 | WITH_OPS_SETTLEMENT | SETTLEMENT_BOOKED | agreement signed and terms booked in ALS | Set the payment due date and wait for the money | AWAITING_PAYMENT | Customer | ALS core, Workbench | payment due 30 days |
| R-SET-14 | Settlement | D6.4 | AWAITING_PAYMENT | PAYMENT_RECEIVED | amount_received = settlement_amount | Match the payment and post it | PAYMENT_CLEARED | Workbench | ALS core, GL, Workbench | None |
| R-SET-15 | Settlement | D6.4 | AWAITING_PAYMENT | PAYMENT_RECEIVED | amount_received < settlement_amount and installments agreed | Match the installment and keep the case awaiting the balance | PAYMENT_PART_RECEIVED | Workbench | ALS core, Workbench | None |
| R-SET-16 | Settlement | D6.4 | AWAITING_PAYMENT | PAYMENT_UNMATCHED | payment matches no treatment | Put the payment on the exception list for the reconciliation agent | AWAITING_PAYMENT | Case owner | ALS core, Workbench | 2 working days |
| R-SET-17 | Settlement | D6.4 | AWAITING_PAYMENT | PAYMENT_DEADLINE_PASSED | no payment matched and payment_due passed | Cancel the settlement and return the case to the route decision | RETURNED_TO_ROUTE_SET | Case owner | Workbench | None |
| R-SET-18 | Settlement | D6.4 | PAYMENT_PART_RECEIVED | FINAL_INSTALLMENT_RECEIVED | cumulative_received = settlement_amount | Match the final installment and post the settlement | PAYMENT_CLEARED | Workbench | ALS core, GL, Workbench | None |
| R-SET-19 | Settlement | D6.4 | PAYMENT_PART_RECEIVED | INSTALLMENT_MISSED | due_date passed and no payment matched | Cancel the settlement and return the case to the route decision | RETURNED_TO_ROUTE_SET | Case owner | Workbench | None |
| R-SET-20 | Settlement | D6.4 | PAYMENT_CLEARED | CLEARANCE_CONFIRMED | funds cleared | Close the account in ALS and request the collateral release | COLLATERAL_RELEASE_REQUESTED | Workbench | ALS core, CCMS | None |
| R-SET-21 | Settlement | D6.4 | COLLATERAL_RELEASE_REQUESTED | COLLATERAL_RELEASED | CCMS confirms the release | Return the title, close the treatment and close the case | CASE_CLOSED_SETTLED | Workbench | CCMS, the Workbench document hub, Workbench | None |
| R-SET-22 | Settlement | D6.4 | COLLATERAL_RELEASE_REQUESTED | TITLE_DOCUMENTS_MISSING | title documents not found | Raise a task to re-create the title set before release | COLLATERAL_RELEASE_REQUESTED | Case owner | the Workbench document hub, CCMS | 5 working days |
| R-SET-23 | Settlement | D6.4 | CASE_CLOSED_SETTLED | PAYMENT_REVERSED | reversal received after release | Re-open the case and record the reversal against the treatment | PAYMENT_REVERSED | Case owner | ALS core, Workbench | None |
| R-SET-24 | Settlement | D6.4 | PAYMENT_REVERSED | REVERSAL_RECORDED | Any | Return the case to the route decision with reason payment_reversed | RETURNED_TO_ROUTE_SET | Case owner | Workbench | None |
| R-SET-25 | Settlement | D6.4 | WITH_FCR_OFFICER_SET | OFFER_PREPARED | no condition matched, or the payoff or floor price is missing | Hold the case, name the missing field and raise a task for the owner | UNMATCHED_EXCEPTION | Case owner | Workbench | same day |
| R-SET-26 | Settlement | D6.4 | AWAITING_PAYMENT | PAYMENT_RECEIVED | amount received does not match and no installment plan is agreed | Hold the case, name the missing field and raise a task for the owner | UNMATCHED_EXCEPTION | Case owner | Workbench | same day |
| R-SET-27 | Settlement | D6.4 | UNMATCHED_EXCEPTION | MANUAL_DECISION_RECORDED | Any | Case owner records the decision and the missing field; the rule gap is logged for the center of excellence | RETURNED_TO_ROUTE_SET | Case owner | Workbench | 2 working days |
| R-DIL-01 | Deed in lieu | D6.4 | ROUTE_APPROVED_DIL | ROUTE_APPROVED | decision.approved and route = R3 | Prioritize the lead and start the early readiness checks | EARLY_READINESS_CHECK | Workbench | Workbench, CCMS | 2 working days |
| R-DIL-02 | Deed in lieu | D6.4 | EARLY_READINESS_CHECK | ENCUMBRANCE_CLEAR | product = MTG and encumbrance_status = clear | Order the valuation | VALUATION_ORDERED | Workbench | CCMS, Land Office, Workbench | None |
| R-DIL-03 | Deed in lieu | D6.4 | EARLY_READINESS_CHECK | REGISTRATION_CHECK_PASSED | product = HP and registration clear in SCIS | Order the valuation | VALUATION_ORDERED | Workbench | SCIS, Workbench | None |
| R-DIL-04 | Deed in lieu | D6.4 | EARLY_READINESS_CHECK | ENCUMBRANCE_UNRESOLVED | product = MTG and encumbrance_status = unresolved | Block the route and hold the case until the check clears | ENCUMBRANCE_BLOCKED | Case owner | CCMS, Land Office | 10 working days |
| R-DIL-05 | Deed in lieu | D6.4 | ENCUMBRANCE_BLOCKED | ENCUMBRANCE_CLEARED | encumbrance_status = clear | Resume the route and order the valuation | VALUATION_ORDERED | Workbench | CCMS, Workbench | None |
| R-DIL-06 | Deed in lieu | D6.4 | ENCUMBRANCE_BLOCKED | HOLD_EXPIRED | encumbrance_status still unresolved at the hold limit | Return the case to the route decision with reason encumbrance_unresolved | RETURNED_TO_ROUTE_DIL | Case owner | Workbench | None |
| R-DIL-07 | Deed in lieu | D6.4 | VALUATION_ORDERED | FAST_LANE_SELECTED | lead_rank in the top 10% | Raise an official appraisal order to a panel valuer through SVAF | AWAITING_VALUER | Valuer | SVAF, Partner Portal | panel service level |
| R-DIL-08 | Deed in lieu | D6.4 | VALUATION_ORDERED | PRELIMINARY_VALUATION_USED | lead_rank outside the top 10% | Value the asset with the preliminary valuation model | VALUATION_ACCEPTED | Workbench | Workbench, SVAF | None |
| R-DIL-09 | Deed in lieu | D6.4 | AWAITING_VALUER | VALUATION_RECEIVED | report attached and value extracted | Flag outliers and present the value for acceptance | VALUATION_ACCEPTED | Case owner | SVAF, Workbench | 2 working days |
| R-DIL-10 | Deed in lieu | D6.4 | AWAITING_VALUER | ACCESS_REFUSED | valuer records an access refusal | Record the limitation and use an external estimate | VALUATION_ACCEPTED | Case owner | SVAF, Workbench | None |
| R-DIL-11 | Deed in lieu | D6.4 | AWAITING_VALUER | VALUER_SLA_BREACHED | order_age > panel service level | Escalate to the partner and agency manager and re-allocate the order | AWAITING_VALUER | Partner and agency manager | Partner Portal, SVAF | None |
| R-DIL-12 | Deed in lieu | D6.4 | VALUATION_ACCEPTED | VALUE_ACCEPTED | accepted_at set and within the age limit | Place the case with the restructuring officer to negotiate | WITH_FCR_OFFICER_DIL | Restructuring officer, FCR | Workbench | 5 working days |
| R-DIL-13 | Deed in lieu | D6.4 | WITH_FCR_OFFICER_DIL | TERMS_AGREED | customer agrees to transfer the asset | Apply the governed transfer price template | TRANSFER_PRICE_SET | Workbench | Workbench | None |
| R-DIL-14 | Deed in lieu | D6.4 | TRANSFER_PRICE_SET | PRICE_INSIDE_FLOOR | transfer_price >= floor_price | Generate the credit approval, the contract and the mortgage documents | OFFER_WITH_CUSTOMER_DIL | Customer | the Workbench document hub, WIN and DMS, Workbench | offer validity 14 days |
| R-DIL-15 | Deed in lieu | D6.4 | TRANSFER_PRICE_SET | PRICE_BELOW_FLOOR | transfer_price < floor_price | Route the price for a second signature | AWAITING_SECOND_SIGNATURE | Head of NPA | Workbench | 3 working days |
| R-DIL-16 | Deed in lieu | D6.4 | AWAITING_SECOND_SIGNATURE | SECOND_SIGNATURE_GIVEN | final_call = approved | Generate the documents and put the offer to the customer | OFFER_WITH_CUSTOMER_DIL | Customer | the Workbench document hub, WIN and DMS, Workbench | offer validity 14 days |
| R-DIL-17 | Deed in lieu | D6.4 | AWAITING_SECOND_SIGNATURE | SECOND_SIGNATURE_REFUSED | final_call = rejected | Return the case to the route decision with reason price_below_floor | RETURNED_TO_ROUTE_DIL | Case owner | Workbench | None |
| R-DIL-18 | Deed in lieu | D6.4 | OFFER_WITH_CUSTOMER_DIL | CUSTOMER_ACCEPTED | product = MTG and signature is wet ink per Legal | Schedule the collateral inspection before transfer | WITH_FIELD_INSPECTION | Field officer or agency field team | Field App, Workbench | 5 working days |
| R-DIL-19 | Deed in lieu | D6.4 | OFFER_WITH_CUSTOMER_DIL | CUSTOMER_ACCEPTED | product = HP and the vehicle is surrendered | Schedule the vehicle inspection and collection | WITH_FIELD_INSPECTION | Field officer or agency field team | Field App, RPS, Workbench | 5 working days |
| R-DIL-20 | Deed in lieu | D6.4 | OFFER_WITH_CUSTOMER_DIL | CUSTOMER_WITHDREW | customer withdraws before transfer | Return the case to the route decision with reason customer_withdrew | RETURNED_TO_ROUTE_DIL | Case owner | Workbench | None |
| R-DIL-21 | Deed in lieu | D6.4 | OFFER_WITH_CUSTOMER_DIL | OFFER_EXPIRED | not accepted and offer_validity passed | Return the case to the route decision with reason offer_expired | RETURNED_TO_ROUTE_DIL | Case owner | Workbench | None |
| R-DIL-22 | Deed in lieu | D6.4 | WITH_FIELD_INSPECTION | INSPECTION_COMPLETED | checklist, photographs and bills captured | Run the asset unlock rule | ASSET_UNLOCK_DECISION | Workbench | Field App, Workbench | None |
| R-DIL-23 | Deed in lieu | D6.4 | ASSET_UNLOCK_DECISION | AUTO_UNLOCK_PASSED | unlock rule passes, about 95% of cases | Release the asset for transfer | AWAITING_TRANSFER | Customer | Workbench | None |
| R-DIL-24 | Deed in lieu | D6.4 | ASSET_UNLOCK_DECISION | AUTO_UNLOCK_FAILED | unlock rule fails | Send the agent summary to the approver | AWAITING_APPROVER_SUMMARY | Head of NPA | Workbench | 3 working days |
| R-DIL-25 | Deed in lieu | D6.4 | AWAITING_APPROVER_SUMMARY | APPROVER_RELEASED | final_call = approved | Release the asset for transfer | AWAITING_TRANSFER | Customer | Workbench | None |
| R-DIL-26 | Deed in lieu | D6.4 | AWAITING_APPROVER_SUMMARY | APPROVER_REFUSED | final_call = rejected | Return the case to the route decision with reason unlock_refused | RETURNED_TO_ROUTE_DIL | Case owner | Workbench | None |
| R-DIL-27 | Deed in lieu | D6.4 | AWAITING_TRANSFER | TRANSFER_COMPLETED | product = MTG and ownership transferred at the Land Office | Record the NPA in AMIS, settle the debt and release the collateral in CCMS | ASSET_ON_BOOKS | Workbench | Land Office, AMIS, ALS core, CCMS | None |
| R-DIL-28 | Deed in lieu | D6.4 | AWAITING_TRANSFER | TRANSFER_COMPLETED | product = HP and registration transferred in SCIS | Record the asset in AMIS, settle the debt and release the registration | ASSET_ON_BOOKS | Workbench | SCIS, AMIS, ALS core | None |
| R-DIL-29 | Deed in lieu | D6.4 | AWAITING_TRANSFER | TITLE_NOT_CLEAN | title or registration check fails at transfer | Hold the transfer and raise a task to clear the title | TITLE_NOT_CLEAN | Case owner | Land Office, SCIS, CCMS | 10 working days |
| R-DIL-30 | Deed in lieu | D6.4 | TITLE_NOT_CLEAN | TITLE_CLEARED | title or registration check passes | Resume the transfer | AWAITING_TRANSFER | Customer | Land Office, SCIS | None |
| R-DIL-31 | Deed in lieu | D6.4 | TITLE_NOT_CLEAN | HOLD_EXPIRED | title still not clean at the hold limit | Return the case to the route decision with reason title_not_clean | RETURNED_TO_ROUTE_DIL | Case owner | Workbench | None |
| R-DIL-32 | Deed in lieu | D6.4 | ASSET_ON_BOOKS | BUYBACK_AGREED | customer rents the asset back | Create the rental record and set the auto-debit | RENTAL_RUNNING | Case owner | ATS, AMIS, Workbench | None |
| R-DIL-33 | Deed in lieu | D6.4 | ASSET_ON_BOOKS | DISPOSAL_REQUIRED | no buy-back agreed | Hand the asset to the disposal route | HANDED_TO_DISPOSAL | Sale officer | AMIS, Workbench | None |
| R-DIL-34 | Deed in lieu | D6.4 | RENTAL_RUNNING | RENTAL_ARREARS | rental arrears exceed the limit | Hand the asset to the disposal route | HANDED_TO_DISPOSAL | Sale officer | ATS, AMIS, Workbench | None |
| R-DIL-35 | Deed in lieu | D6.4 | OFFER_WITH_CUSTOMER_DIL | CUSTOMER_ACCEPTED | product is not MTG or HP, or the signature basis is not recorded | Hold the case, name the missing field and raise a task for the owner | UNMATCHED_EXCEPTION | Case owner | Workbench | same day |
| R-DIL-36 | Deed in lieu | D6.4 | AWAITING_TRANSFER | TRANSFER_COMPLETED | the registry confirmation does not name a known registry | Hold the case, name the missing field and raise a task for the owner | UNMATCHED_EXCEPTION | Case owner | Workbench | same day |
| R-DIL-37 | Deed in lieu | D6.4 | UNMATCHED_EXCEPTION | MANUAL_DECISION_RECORDED | Any | Case owner records the decision and the missing field; the rule gap is logged for the center of excellence | RETURNED_TO_ROUTE_DIL | Case owner | Workbench | 2 working days |
| R-GUA-01 | Guarantee claim | D6.5, D6.6 | GUARANTEE_DETECTED | GUARANTEE_FOUND | guarantee_type = TCG scheme and scheme_code present | Start the claim deadline timer from the date the default conditions are met | DEADLINE_TIMER_RUNNING | Workbench | Workbench, Workbench scheduler, ALS core | To the claim deadline |
| R-GUA-02 | Guarantee claim | D6.5, D6.6 | GUARANTEE_DETECTED | CONDITIONS_NOT_MET | the scheme default conditions are not satisfied | Record that no claim arises and hold the guarantee | NOT_ELIGIBLE | Guarantee officer | Workbench | None |
| R-GUA-03 | Guarantee claim | D6.5, D6.6 | NOT_ELIGIBLE | CONDITIONS_LATER_MET | the default conditions are met at a later review | Start the claim deadline timer | DEADLINE_TIMER_RUNNING | Workbench | Workbench, Workbench scheduler | To the claim deadline |
| R-GUA-04 | Guarantee claim | D6.5, D6.6 | DEADLINE_TIMER_RUNNING | PREPARATION_DUE | days to claim_deadline <= the preparation window | The claim preparation agent assembles the claim against the scheme checklist | CLAIM_PREPARATION | Workbench | Workbench, Document Hub | 5 working days |
| R-GUA-05 | Guarantee claim | D6.5, D6.6 | DEADLINE_TIMER_RUNNING | CLAIM_DEADLINE_MISSED | claim_deadline passed and claim_status is not submitted | Record the lost claim, the reason and the amount, and report the breach | DEADLINE_MISSED | Guarantee officer | Workbench, Workbench scheduler | None |
| R-GUA-06 | Guarantee claim | D6.5, D6.6 | DEADLINE_TIMER_RUNNING | GUARANTOR_NOTICE_DUE | guarantee_type in (personal guarantor, co-borrower, corporate) | Issue the D6.6 guarantor notice with proof of delivery | GUARANTOR_NOTICE | Guarantor | WIN and DMS, Workbench | Notice period by product |
| R-GUA-07 | Guarantee claim | D6.5, D6.6 | CLAIM_PREPARATION | CHECKLIST_COMPLETE | every scheme checklist item is present | Present the claim to the guarantee officer for approval | CLAIM_APPROVAL | Guarantee officer | Document Hub, Workbench | 3 working days |
| R-GUA-08 | Guarantee claim | D6.5, D6.6 | CLAIM_PREPARATION | CHECKLIST_INCOMPLETE | one or more checklist items are missing | Raise retrieval requests and hold the claim | CLAIM_DEFECT_HOLD | Guarantee officer | Document Hub, the Workbench document hub | 5 working days |
| R-GUA-09 | Guarantee claim | D6.5, D6.6 | CLAIM_PREPARATION | CLAIM_DEADLINE_MISSED | claim_deadline passed before submission | Record the lost claim and the reason, and report the breach | DEADLINE_MISSED | Guarantee officer | Workbench, Workbench scheduler | None |
| R-GUA-10 | Guarantee claim | D6.5, D6.6 | CLAIM_DEFECT_HOLD | DOCUMENT_SUPPLIED | the missing items are supplied | Re-run the scheme checklist | CLAIM_PREPARATION | Workbench | Document Hub | 1 working day |
| R-GUA-11 | Guarantee claim | D6.5, D6.6 | CLAIM_DEFECT_HOLD | DEADLINE_WARNING | days to claim_deadline <= the warning window | Escalate to the guarantee officer and the Head of Litigation to submit with the gap recorded | CLAIM_APPROVAL | Head of Litigation | Workbench, Workbench scheduler | To the claim deadline |
| R-GUA-12 | Guarantee claim | D6.5, D6.6 | CLAIM_APPROVAL | CLAIM_APPROVED | the guarantee officer verifies the claim at D6.5 | Submit the claim through the TCG claim channel | CLAIM_SUBMITTED | TCG | Workbench, TCG claim channel | 2 working days |
| R-GUA-13 | Guarantee claim | D6.5, D6.6 | CLAIM_APPROVAL | CLAIM_SENT_BACK | the officer rejects the assembled claim | Return the claim to the preparation agent for rework | CLAIM_PREPARATION | Workbench | Workbench | 2 working days |
| R-GUA-14 | Guarantee claim | D6.5, D6.6 | CLAIM_SUBMITTED | TCG_QUERY_RAISED | TCG asks for more information before assessment | Hold the claim and raise a task to the guarantee officer | TCG_QUERY | Guarantee officer | TCG claim channel, Workbench | To the TCG response date |
| R-GUA-15 | Guarantee claim | D6.5, D6.6 | TCG_QUERY | QUERY_ANSWERED | the requested information is supplied | Resubmit the claim | CLAIM_SUBMITTED | TCG | TCG claim channel | 5 working days |
| R-GUA-16 | Guarantee claim | D6.5, D6.6 | TCG_QUERY | QUERY_UNANSWERED | the query response window has passed | Record the lapse and treat the claim as rejected | CLAIM_REJECTED | Guarantee officer | TCG claim channel | None |
| R-GUA-17 | Guarantee claim | D6.5, D6.6 | CLAIM_SUBMITTED | CLAIM_REJECTED_BY_TCG | a rejection reason is returned | Record the rejection reason and assess a resubmission | CLAIM_REJECTED | Guarantee officer | TCG claim channel | 5 working days |
| R-GUA-18 | Guarantee claim | D6.5, D6.6 | CLAIM_REJECTED | RESUBMISSION_POSSIBLE | the rejection reason is curable and claim_deadline has not passed | Rework the claim against the reason given | CLAIM_PREPARATION | Workbench | Document Hub | 5 working days |
| R-GUA-19 | Guarantee claim | D6.5, D6.6 | CLAIM_REJECTED | RESUBMISSION_NOT_POSSIBLE | the reason is not curable, or claim_deadline has passed | Close the guarantee and return the full balance to the route decision | RESIDUAL_TO_ROUTE | Case owner | Workbench | None |
| R-GUA-20 | Guarantee claim | D6.5, D6.6 | CLAIM_SUBMITTED | PART_PAYMENT_RECEIVED | claim_amount_paid < guaranteed_amount | Match the payment with source TCG and post it against the case | CLAIM_PART_PAID | Workbench | ALS core and GL | 2 working days |
| R-GUA-21 | Guarantee claim | D6.5, D6.6 | CLAIM_PART_PAID | BALANCE_CLAIMED | the unpaid share is still claimable inside the deadline | Submit the balance claim | CLAIM_SUBMITTED | TCG | TCG claim channel | 5 working days |
| R-GUA-22 | Guarantee claim | D6.5, D6.6 | CLAIM_SUBMITTED | FULL_PAYMENT_RECEIVED | claim_amount_paid = guaranteed_amount | Match the payment, post it, and set the subrogation position | CLAIM_PAID | Workbench | ALS core and GL | 2 working days |
| R-GUA-23 | Guarantee claim | D6.5, D6.6 | CLAIM_PAID | SUBROGATION_DUE | TCG holds a share of every later recovery | Record the TCG share against the case for all future recoveries | SUBROGATION_POSITION | Guarantee officer | Workbench, ALS core | None |
| R-GUA-24 | Guarantee claim | D6.5, D6.6 | CLAIM_PART_PAID | SUBROGATION_DUE | TCG holds a share of every later recovery | Record the TCG share against the case for all future recoveries | SUBROGATION_POSITION | Guarantee officer | Workbench, ALS core | None |
| R-GUA-25 | Guarantee claim | D6.5, D6.6 | SUBROGATION_POSITION | RESIDUAL_REMAINS | the balance after the guaranteed share is greater than zero | Return the residual to the route decision at D6 | RESIDUAL_TO_ROUTE | Case owner | Workbench | 5 working days |
| R-GUA-26 | Guarantee claim | D6.5, D6.6 | SUBROGATION_POSITION | BALANCE_SATISFIED | the balance after the guaranteed share is zero | Close the guarantee and close the case | GUARANTEE_CLOSED | Case owner | Workbench, ALS core | None |
| R-GUA-27 | Guarantee claim | D6.5, D6.6 | DEADLINE_MISSED | LOSS_RECORDED | the loss amount and the reason are recorded | Return the full balance to the route decision and close the guarantee | RESIDUAL_TO_ROUTE | Case owner | Workbench | 5 working days |
| R-GUA-28 | Guarantee claim | D6.5, D6.6 | GUARANTOR_NOTICE | GUARANTOR_SETTLED | the guarantor pays or agrees inside the approved range | Book the treatment, reduce the balance and close the guarantee | GUARANTEE_CLOSED | Case owner | Workbench, ALS core | 5 working days |
| R-GUA-29 | Guarantee claim | D6.5, D6.6 | GUARANTOR_NOTICE | GUARANTOR_REFUSED | the guarantor refuses, or does not reply by the notice expiry | Record the refusal and return the case to the route decision | RESIDUAL_TO_ROUTE | Case owner | Workbench | None |
| R-GUA-30 | Guarantee claim | D6.5, D6.6 | GUARANTOR_NOTICE | GUARANTOR_DISPUTED | the guarantor disputes the guarantee itself | Raise X1, stop contact on the disputed item and hold the pursuit | GUARANTOR_DISPUTE_HOLD | Complaint officer | Workbench | None |
| R-GUA-31 | Guarantee claim | D6.5, D6.6 | GUARANTOR_DISPUTE_HOLD | X1_RESOLVED | the dispute is resolved and not upheld | Resume the guarantor pursuit from the notice | GUARANTOR_NOTICE | Case owner | Workbench | None |
| R-GUA-32 | Guarantee claim | D6.5, D6.6 | GUARANTOR_DISPUTE_HOLD | X1_UPHELD | the dispute is upheld against the guarantee | Release the guarantor and return the case to the route decision | RESIDUAL_TO_ROUTE | Case owner | Workbench | 5 working days |
| R-LIT-01 | Litigation | D7 | LIT_ROUTE_APPROVED | ROUTE_APPROVED | decision.approved and route = R4 | Open the litigation task and set the notice and prescription timers | NOTICE_GENERATED | Workbench | Workbench, Workbench scheduler | Same day |
| R-LIT-02 | Litigation | D7 | LIT_ROUTE_APPROVED | TREATMENT_BROKEN | plan_status = broken and prior_route in (R1, R2) | Return the case to the legal route and open the litigation task | NOTICE_GENERATED | Workbench | Workbench, Workbench scheduler, EFS | Same day |
| R-LIT-03 | Litigation | D7 | NOTICE_GENERATED | TEMPLATE_SELECTED | template_status = current for product and notice_type | Generate the demand and recall notices from the Legal-approved template | NOTICE_DISPATCHED | Workbench | Rules component, letter engine, the Workbench document hub | 1 working day |
| R-LIT-04 | Litigation | D7 | NOTICE_GENERATED | TEMPLATE_WITHDRAWN | template_status = withdrawn | Hold generation and raise a task to the litigation officer | NOTICE_BLOCKED | Litigation officer | Workbench, the Workbench document hub | 1 working day |
| R-LIT-05 | Litigation | D7 | NOTICE_GENERATED | CONTACT_STOP_APPLIED | contact_stop = Y from X1 or X2 | Hold the notice and route the case to the deviation owner | NOTICE_BLOCKED | Conduct and QA officer | Workbench | None |
| R-LIT-06 | Litigation | D7 | NOTICE_BLOCKED | TEMPLATE_REPLACED | a new template version is approved by Legal | Resume generation on the current version | NOTICE_GENERATED | Workbench | Rules component, the Workbench document hub | 1 working day |
| R-LIT-07 | Litigation | D7 | NOTICE_DISPATCHED | PROOF_OF_DELIVERY_RECEIVED | served_result = delivered | Attach the proof and start the notice period from delivered_at | WITH_CUSTOMER_NOTICE_PERIOD | Customer | WIN and DMS, Workbench | Notice period by product and type |
| R-LIT-08 | Litigation | D7 | NOTICE_DISPATCHED | PROOF_WINDOW_EXPIRED | no proof returned inside the proof window | Mark the notice unserved; the notice period does not start | NOTICE_UNSERVED | Litigation officer | WIN and DMS | 7 days |
| R-LIT-09 | Litigation | D7 | NOTICE_DISPATCHED | DELIVERY_FAILED | served_result in (refused, returned, undeliverable) | Record the result and queue an alternate service method | NOTICE_UNSERVED | Litigation officer | WIN and DMS | 2 working days |
| R-LIT-10 | Litigation | D7 | NOTICE_UNSERVED | ALTERNATE_SERVICE_ORDERED | address refreshed, or substituted service approved | Re-serve by the alternate method | NOTICE_DISPATCHED | Workbench | WIN and DMS, NCB | 3 working days |
| R-LIT-11 | Litigation | D7 | NOTICE_UNSERVED | PRESCRIPTION_WARNING | prescription_days_remaining <= 90 | Head of Litigation approves substituted service or filing where the law allows | PACK_ASSEMBLY | Head of Litigation | Workbench, Workbench scheduler | To the prescription date |
| R-LIT-12 | Litigation | D7 | WITH_CUSTOMER_NOTICE_PERIOD | CUSTOMER_PAID_IN_FULL | balance = 0 inside the notice period | Cancel the litigation route and close the legal action | CASE_CLOSED | Case owner | ALS core, Workbench | None |
| R-LIT-13 | Litigation | D7 | WITH_CUSTOMER_NOTICE_PERIOD | CUSTOMER_REQUESTED_TREATMENT | offer acceptable inside the approved range | Cancel litigation and return the case to the treatment route | TO_TREATMENT | Restructuring officer, FCR | Workbench, EFS | 2 working days |
| R-LIT-14 | Litigation | D7 | WITH_CUSTOMER_NOTICE_PERIOD | CUSTOMER_DISPUTED | inbound reply classified as a dispute | Raise X1, stop contact on the disputed item and pause the litigation timers | DEVIATION_HOLD | Complaint officer | Workbench, Document Hub | None |
| R-LIT-15 | Litigation | D7 | WITH_CUSTOMER_NOTICE_PERIOD | NOTICE_PERIOD_EXPIRED | no cure and no dispute at period_expires_at | Open pack assembly | PACK_ASSEMBLY | Workbench | Workbench, Document Hub | 3 working days |
| R-LIT-16 | Litigation | D7 | PACK_ASSEMBLY | PACK_COMPLETE | every defect list item present | Present the pack to the litigation officer for verification | PACK_VERIFIED | Litigation officer | Document Hub, CCMS, LHS, the Workbench document hub | 2 working days |
| R-LIT-17 | Litigation | D7 | PACK_ASSEMBLY | PACK_INCOMPLETE | one or more defect list items missing | Raise retrieval requests and hold the pack | PACK_DEFECT_HOLD | Litigation officer | Document Hub, the Workbench document hub | 5 working days |
| R-LIT-18 | Litigation | D7 | PACK_DEFECT_HOLD | DOCUMENT_RETRIEVED | missing items supplied, re-signed or re-created | Re-run the defect list check | PACK_ASSEMBLY | Workbench | Document Hub, the Workbench document hub | 1 working day |
| R-LIT-19 | Litigation | D7 | PACK_DEFECT_HOLD | DOCUMENT_UNRECOVERABLE | the document cannot be re-created | Refer to Legal for the affidavit route and record the gap with a reason | PACK_VERIFIED | Head of Litigation | Workbench, the Workbench document hub | 10 working days |
| R-LIT-20 | Litigation | D7 | PACK_DEFECT_HOLD | PRESCRIPTION_WARNING | prescription_days_remaining <= 90 | Escalate; the Head of Litigation approves filing with the gap recorded | PACK_VERIFIED | Head of Litigation | Workbench, Workbench scheduler | To the prescription date |
| R-LIT-21 | Litigation | D7 | PACK_VERIFIED | OFFICER_REJECTED_PACK | the officer rejects the pack at verification | Return the pack to the legal document agent for rework | PACK_ASSEMBLY | Workbench | Document Hub | 1 working day |
| R-LIT-22 | Litigation | D7 | PACK_VERIFIED | CONDUCT_CHECK_FAILED | the conduct check on the notice or the contact fails | Return the notice for correction before filing | NOTICE_BLOCKED | Conduct and QA officer | Workbench | 2 working days |
| R-LIT-23 | Litigation | D7 | PACK_VERIFIED | PACK_APPROVED | pack_verified_at set | Select the law firm by rule from the panel | FIRM_SELECTION | Workbench | Rules component, partner performance data | Same day |
| R-LIT-24 | Litigation | D7 | FIRM_SELECTION | FIRM_MATCHED | panel firm covers the court region and case type and passes the conflict check | Issue the instruction with the pack through the portal | FIRM_INSTRUCTED | Panel law firm | Partner Portal | 2 working days |
| R-LIT-25 | Litigation | D7 | FIRM_SELECTION | NO_FIRM_AVAILABLE | no panel firm in the region, or all conflicted | Escalate the selection | FIRM_ESCALATED | Head of Litigation | Workbench | 2 working days |
| R-LIT-26 | Litigation | D7 | FIRM_ESCALATED | FIRM_NOMINATED | the Head of Litigation nominates a firm or widens the panel | Issue the instruction with the pack through the portal | FIRM_INSTRUCTED | Panel law firm | Partner Portal | 2 working days |
| R-LIT-27 | Litigation | D7 | FIRM_INSTRUCTED | INSTRUCTION_DECLINED | the firm declines, or does not accept inside the window | Record the decline and re-select the next firm on the scorecard | FIRM_DECLINED | Workbench | Partner Portal | 2 working days |
| R-LIT-28 | Litigation | D7 | FIRM_INSTRUCTED | FIRM_BREACHED_SLA | the instruction is past due with no filing | Mark the instruction breached, notify the partner manager and re-select | FIRM_DECLINED | Partner and agency manager | Partner Portal | None |
| R-LIT-29 | Litigation | D7 | FIRM_DECLINED | RESELECTION_RUN | the next firm on the scorecard is available | Issue the instruction to the next firm | FIRM_INSTRUCTED | Panel law firm | Partner Portal, Rules component | 2 working days |
| R-LIT-30 | Litigation | D7 | FIRM_INSTRUCTED | CASE_FILED | the firm uploads the receipt and the court case number | Write the court case number to the Legal Action and set the hearing timers | FILED_IN_COURT | Panel law firm | Partner Portal, court e-filing, LIT | Filing service level by task |
| R-LIT-31 | Litigation | D7 | FILED_IN_COURT | COURT_REJECTED_FILING | the court returns the filing for a defect | Record the defect and return the pack for rework | FILING_REJECTED | Litigation officer | Partner Portal, LIT | 5 working days |
| R-LIT-32 | Litigation | D7 | FILING_REJECTED | PACK_REWORKED | the defect is corrected | Re-run the defect list check and re-file | PACK_ASSEMBLY | Workbench | Document Hub | 3 working days |
| R-LIT-33 | Litigation | D7 | FILED_IN_COURT | HEARING_SCHEDULED | the court sets a hearing date | Schedule the hearing and set the deadline timer | IN_HEARING | Panel law firm | LIT, Partner Portal, Workbench scheduler | To the hearing date |
| R-LIT-34 | Litigation | D7 | IN_HEARING | HEARING_ADJOURNED | outcome = adjourned | Reset the hearing timer and record the postpone reason code | HEARING_ADJOURNED | Panel law firm | Partner Portal, Workbench scheduler | To the new date |
| R-LIT-35 | Litigation | D7 | HEARING_ADJOURNED | NEW_DATE_SET | scheduled_for reset by the court | Return the case to the hearing calendar | IN_HEARING | Panel law firm | LIT, Workbench scheduler | To the new date |
| R-LIT-36 | Litigation | D7 | IN_HEARING | SETTLEMENT_PROPOSED | the customer or the firm proposes a settlement before judgment | The agent proposes the step with its cost and effect, and routes it to the approver | SETTLEMENT_OFFERED_AT_COURT | Approver at D7.4 | Workbench, Committee View | 3 working days |
| R-LIT-37 | Litigation | D7 | SETTLEMENT_OFFERED_AT_COURT | SETTLEMENT_APPROVED | inside the D7.4 limit, or the committee approves above it | Book the treatment and hold the litigation rather than withdraw it | LITIGATION_HELD | Restructuring officer, FCR | Workbench, ALS core | 2 working days |
| R-LIT-38 | Litigation | D7 | SETTLEMENT_OFFERED_AT_COURT | SETTLEMENT_REJECTED | the approver rejects with a reason | Continue the case to judgment | IN_HEARING | Panel law firm | Workbench, Committee View | None |
| R-LIT-39 | Litigation | D7 | LITIGATION_HELD | SETTLEMENT_COMPLETED | the treatment completes and the balance is satisfied | Withdraw the case and close the legal action | CASE_CLOSED | Case owner | Workbench, LIT, ALS core | None |
| R-LIT-40 | Litigation | D7 | LITIGATION_HELD | SETTLEMENT_BROKEN | plan_status = broken | Resume the litigation from the hearing it was held at | IN_HEARING | Panel law firm | Partner Portal, LIT | 5 working days |
| R-LIT-41 | Litigation | D7 | IN_HEARING | FEE_DUE | a court fee or legal expense falls due | Route the fee to the approver inside the D7.4 limit | LEGAL_SPEND_APPROVAL | Approver at D7.4 | Workbench, Committee View | 3 working days |
| R-LIT-42 | Litigation | D7 | LEGAL_SPEND_APPROVAL | FEE_APPROVED | inside the limit, or the committee approves above it | Raise the fee and post it against the case | IN_HEARING | Panel law firm | ALS core and GL | 5 working days |
| R-LIT-43 | Litigation | D7 | LEGAL_SPEND_APPROVAL | FEE_REJECTED | the approver rejects the spend | Record the reason and return the case without the spend | IN_HEARING | Litigation officer | Workbench | None |
| R-LIT-44 | Litigation | D7 | IN_HEARING | JUDGMENT_FOR_THE_BANK | judgment_type in (full, partial, default) | Record the judgment date and amount and open the enforcement task | JUDGMENT_RECORDED | Enforcement owner | LIT, Partner Portal | 5 working days |
| R-LIT-45 | Litigation | D7 | IN_HEARING | JUDGMENT_AGAINST_THE_BANK | judgment_type = dismissed | Record the dismissal and open the appeal window | JUDGMENT_DISMISSED | Litigation officer | LIT, Partner Portal | To the appeal window end |
| R-LIT-46 | Litigation | D7 | JUDGMENT_DISMISSED | APPEAL_WINDOW_OPEN | appeal_window_ends is in the future | The agent proposes appeal or accept with cost and effect | APPEAL_DECISION | Approver at D7.4 | Workbench, Committee View | To the window end |
| R-LIT-47 | Litigation | D7 | APPEAL_DECISION | APPEAL_APPROVED | inside the limit, or the Head of Litigation approves above it | Instruct the firm to appeal and reset the hearing timers | APPEAL_FILED | Panel law firm | Partner Portal, LIT | To the filing deadline |
| R-LIT-48 | Litigation | D7 | APPEAL_FILED | APPEAL_HEARING_SET | the court sets the appeal hearing | Return the case to the hearing calendar | IN_HEARING | Panel law firm | LIT, Workbench scheduler | To the hearing date |
| R-LIT-49 | Litigation | D7 | APPEAL_DECISION | APPEAL_DECLINED | the approver accepts the judgment, or the window has passed | Record the reason and route the case to write-off | TO_WRITE_OFF | Write-off team with Credit Administration | Workbench | None |
| R-LIT-50 | Litigation | D7 | JUDGMENT_RECORDED | ENFORCEMENT_OPENED | a judgment is recorded against the debtor | Trace assets across NCB, internal data, registries and insurers | ASSET_TRACE | Workbench | NCB, registries, insurers | 10 working days |
| R-LIT-51 | Litigation | D7 | JUDGMENT_RECORDED | DEBTOR_PAID_AFTER_JUDGMENT | a payment after judgment covers the balance and costs | Match the payment, close the enforcement and close the case | CASE_CLOSED | Case owner | ALS core and GL | None |
| R-LIT-52 | Litigation | D7 | ASSET_TRACE | ASSETS_FOUND | one or more assets traced | Present the enforcement decision with the traced assets | ENFORCEMENT_DECISION | Enforcement owner | Workbench | 5 working days |
| R-LIT-53 | Litigation | D7 | ASSET_TRACE | NO_ASSET_FOUND | the trace returns nothing | Present the enforcement decision with a deferral recommendation | ENFORCEMENT_DECISION | Enforcement owner | Workbench | 5 working days |
| R-LIT-54 | Litigation | D7 | ENFORCEMENT_DECISION | ENFORCE_APPROVED | an asset is traced and enforcement is economic | Instruct the firm to apply for the writ and seizure | WRIT_AND_SEIZURE | Panel law firm | Partner Portal, LED | To the writ deadline |
| R-LIT-55 | Litigation | D7 | ENFORCEMENT_DECISION | DEFER_RECORDED | deferral_reason and deferral_review_date are both present | Record the deferral and re-queue the case on the review date | DEFERRAL_RECORDED | Enforcement owner | Workbench, Workbench scheduler | To the review date |
| R-LIT-56 | Litigation | D7 | DEFERRAL_RECORDED | REVIEW_DATE_REACHED | the deferral review date is reached | Return the case to the enforcement decision | ENFORCEMENT_DECISION | Enforcement owner | Workbench, Workbench scheduler | 5 working days |
| R-LIT-57 | Litigation | D7 | DEFERRAL_RECORDED | ENFORCEMENT_EXHAUSTED | a second deferral with no asset traced | Route the case to write-off at D9 | TO_WRITE_OFF | Write-off team with Credit Administration | Workbench | None |
| R-LIT-58 | Litigation | D7 | ENFORCEMENT_DECISION | PETITION_PROPOSED | enforcement exhausted and the bankruptcy test is met | Route the petition to the approver at D7.5 | BANKRUPTCY_PETITION | Approver at D7.5 | Workbench, Committee View | 5 working days |
| R-LIT-59 | Litigation | D7 | BANKRUPTCY_PETITION | PETITION_APPROVED | the approver approves the petition at D7.5 | Instruct the firm to file the petition and the claim | OFFICIAL_RECEIVER_CLAIM | Official receiver | Partner Portal, courts | To the filing deadline |
| R-LIT-60 | Litigation | D7 | BANKRUPTCY_PETITION | PETITION_REJECTED | the approver rejects with a reason | Route the case to write-off at D9 | TO_WRITE_OFF | Write-off team with Credit Administration | Workbench | None |
| R-LIT-61 | Litigation | D7 | OFFICIAL_RECEIVER_CLAIM | DIVIDEND_RECEIVED | the receiver distributes a dividend | Match the dividend to the case and post it to ALS | PROCEEDS_MATCHED | Workbench | ALS core and GL | 2 working days |
| R-LIT-62 | Litigation | D7 | OFFICIAL_RECEIVER_CLAIM | CLAIM_DEADLINE_MISSED | the claim is not filed before the receiver deadline | Record the loss and the reason and route the case to write-off | TO_WRITE_OFF | Write-off team with Credit Administration | Workbench | None |
| R-LIT-63 | Litigation | D7 | WRIT_AND_SEIZURE | SEIZURE_EXECUTED | the asset is seized and the seizure reported | Open the LED auction at round 1 | LED_AUCTION | Legal Execution Department | Partner Portal, LED | To the auction date |
| R-LIT-64 | Litigation | D7 | WRIT_AND_SEIZURE | SEIZURE_BLOCKED | the seizure is obstructed, or the asset has moved | Record the obstruction and return to the enforcement decision | ENFORCEMENT_DECISION | Enforcement owner | Partner Portal | 10 working days |
| R-LIT-65 | Litigation | D7 | LED_AUCTION | ROUND_SOLD | round_result = sold at 100, 90, 80 or 70 percent of official value | Match the proceeds to the case | PROCEEDS_MATCHED | Workbench | LED, ALS core | 2 working days |
| R-LIT-66 | Litigation | D7 | LED_AUCTION | ROUND_NO_BID | round_result = no bid and auction_round < 4 | Step the price to the next round on the ladder | LED_AUCTION | Legal Execution Department | LED, Partner Portal | To the next auction date |
| R-LIT-67 | Litigation | D7 | LED_AUCTION | LADDER_EXHAUSTED | round_result = no bid and auction_price_basis = 70 percent | Record the unsold result and refer it to the enforcement owner | NO_BID_AT_70 | Enforcement owner | LED, Partner Portal | 5 working days |
| R-LIT-68 | Litigation | D7 | NO_BID_AT_70 | ASSET_TAKEN_ON_BOOK | the bank bids in or takes the asset onto its books | Create the Asset and hand the case to the disposal route at D8 | TO_ASSET_DISPOSAL | Sale officer | AMIS, Workbench | 5 working days |
| R-LIT-69 | Litigation | D7 | NO_BID_AT_70 | ASSET_RETURNED_UNSOLD | the bank does not take the asset | Return to the enforcement decision for the next step | ENFORCEMENT_DECISION | Enforcement owner | Workbench | 5 working days |
| R-LIT-70 | Litigation | D7 | PROCEEDS_MATCHED | BALANCE_SATISFIED | proceeds cover the judgment total and the costs | Close the enforcement and the case, and retain the record after close | CASE_CLOSED | Case owner | ALS core and GL | None |
| R-LIT-71 | Litigation | D7 | PROCEEDS_MATCHED | SHORTFALL_REMAINS | proceeds are less than the judgment total | Route the residual to debt sale or write-off at D8 or D9 | TO_WRITE_OFF | Write-off team with Credit Administration | Workbench | 10 working days |
| R-LIT-72 | Litigation | D7 | PROCEEDS_MATCHED | NO_CASE_REFERENCE | proceeds arrive with no case reference | Hold the cash unmatched and raise a daily exception to the case owner | PROCEEDS_MATCHED | Case owner | ALS core, Workbench | 1 working day |
| R-LIT-73 | Litigation | D7 | IN_HEARING | DEVIATION_RAISED | deviation_open in (X1, X2, X3, X4, X5, X7) | Pause the litigation timers and leave the prescription timer running | DEVIATION_HOLD | Named deviation approver | Workbench | None |
| R-LIT-74 | Litigation | D7 | DEVIATION_HOLD | X1_RESOLVED | the complaint is resolved and not upheld | Resume the litigation at the state it paused in | IN_HEARING | Panel law firm | Workbench | None |
| R-LIT-75 | Litigation | D7 | DEVIATION_HOLD | X1_UPHELD | the complaint is upheld against the debt | Withdraw the litigation and return the case to treatment | TO_TREATMENT | Case owner | Workbench, LIT | 5 working days |
| R-LIT-76 | Litigation | D7 | DEVIATION_HOLD | X3_INSURANCE_SETTLED | credit life or mortgage insurance settles the balance | Withdraw the litigation and close the case | CASE_CLOSED | Case owner | Workbench, ALS core | None |
| R-LIT-77 | Litigation | D7 | DEVIATION_HOLD | X4_FRAUD_CONFIRMED | fraud confirmed in Aric | Stop the litigation and route the case to write-off at D9 | TO_WRITE_OFF | Fraud team with the write-off team | Aric, Workbench | None |
| R-LIT-78 | Litigation | D7 | DEVIATION_HOLD | X5_BANKRUPTCY_DETECTED | a bankruptcy filing or a third-party seizure is detected | Stop direct collection and file the claim with the official receiver | OFFICIAL_RECEIVER_CLAIM | Legal | Workbench, courts | To the receiver deadline |
| R-LIT-79 | Litigation | D7 | DEVIATION_HOLD | X7_COLLATERAL_EVENT | collateral stolen, damaged, written off, or the insurance lapsed | Re-appraise the collateral and return the case to the route decision at D6 | TO_TREATMENT | Case owner | SVAF, Workbench | 10 working days |
| R-DIS-01 | Asset disposal | D8.1 to D8.3 | ASSET_PENDING_TAKE_ON | REPOSSESSION_COMPLETED | asset_type = vehicle and statutory_notice_proved = Y | Create the asset record from RPS with condition, photographs and location | ASSET_ON_BOOKS | Sale officer | RPS, AMIS, Field App | 1 working day |
| R-DIS-02 | Asset disposal | D8.1 to D8.3 | ASSET_PENDING_TAKE_ON | DIL_TRANSFER_REGISTERED | asset_type = property and transfer registered | Create the asset record from AMIS with the opening book value | ASSET_ON_BOOKS | Sale officer | AMIS, the Land Office | 1 working day |
| R-DIS-03 | Asset disposal | D8.1 to D8.3 | ASSET_PENDING_TAKE_ON | LED_HANDOVER_RECEIVED | led_result = handed_over after the 100, 90, 80 then 70 percent ladder | Record the LED result and create the asset record | ASSET_ON_BOOKS | Sale officer | AMIS, the Legal Execution Department | 1 working day |
| R-DIS-04 | Asset disposal | D8.1 to D8.3 | ASSET_PENDING_TAKE_ON | STATUTORY_NOTICE_FAILED | delivery_proved = N | Hold the take-on, raise a failed notice task and re-serve on a confirmed address | FAILED_NOTICE_QUEUE | Sale officer | WIN and DMS, Document Hub | 2 working days |
| R-DIS-05 | Asset disposal | D8.1 to D8.3 | FAILED_NOTICE_QUEUE | NOTICE_REISSUED | new_address_confirmed = Y | Re-serve the statutory notice and resume the take-on | ASSET_PENDING_TAKE_ON | Workbench | WIN and DMS, Document Hub | None |
| R-DIS-06 | Asset disposal | D8.1 to D8.3 | ASSET_ON_BOOKS | ASSET_RECORD_CONFIRMED | title_status in (clear, under_transfer) | Start the holding age clock and the provision step clock, and charge cost of carry monthly | ASSET_HELD | Sale officer | Workbench, Finance provision feed | None |
| R-DIS-07 | Asset disposal | D8.1 to D8.3 | ASSET_ON_BOOKS | TITLE_UNRESOLVED | title_status = encumbered or registration_status = blocked | Hold the asset and raise a title task | TITLE_BLOCKED | Sale officer | CCMS, the Land Office, SCIS | 10 working days |
| R-DIS-08 | Asset disposal | D8.1 to D8.3 | TITLE_BLOCKED | TITLE_CLEARED | title_status = clear | Release the asset to hold and to the disposal route | ASSET_HELD | Sale officer | CCMS, the Land Office, SCIS | None |
| R-DIS-09 | Asset disposal | D8.1 to D8.3 | ASSET_HELD | PROVISION_STEP_DUE | holding_age reaches next_provision_step_date | Apply the provision step and send the input to Finance | ASSET_HELD | Workbench | Finance provision feed, ALS core and GL | None |
| R-DIS-10 | Asset disposal | D8.1 to D8.3 | ASSET_HELD | WORK_ORDER_RAISED | storage, property tax, insurance, security or eviction required | Raise the work order to the property services vendor on the portal | WORK_ORDER_OPEN | Property services vendor | Partner Portal | per fee schedule |
| R-DIS-11 | Asset disposal | D8.1 to D8.3 | WORK_ORDER_OPEN | WORK_ACCEPTED | sale_officer_accepted = Y | Release the invoice for payment and return the asset to hold | ASSET_HELD | Sale officer | Partner Portal, ALS core and GL | 3 working days |
| R-DIS-12 | Asset disposal | D8.1 to D8.3 | WORK_ORDER_OPEN | WORK_REFUSED | sale_officer_accepted = N | Block the invoice and return the work order to the vendor | WORK_ORDER_OPEN | Property services vendor | Partner Portal | None |
| R-DIS-13 | Asset disposal | D8.1 to D8.3 | ASSET_HELD | OCCUPANTS_REFUSE_POSSESSION | occupancy_status = occupied | Raise the eviction instruction to Legal | EVICTION_REQUIRED | Litigation officer | LIT, Partner Portal | None |
| R-DIS-14 | Asset disposal | D8.1 to D8.3 | EVICTION_REQUIRED | POSSESSION_TAKEN | occupancy_status = vacant | Return the asset to hold and resume the disposal route | ASSET_HELD | Sale officer | Workbench, LIT | None |
| R-DIS-15 | Asset disposal | D8.1 to D8.3 | ASSET_HELD | REAPPRAISAL_CYCLE_DUE | appraisal_date older than 12 months and one_year_rule_applied = N | Order the re-appraisal through SVAF | REAPPRAISAL_ORDERED | Valuer | SVAF | 10 working days |
| R-DIS-16 | Asset disposal | D8.1 to D8.3 | REAPPRAISAL_ORDERED | VALUER_REPORTED | Any | Record the value and run the valuation agent outlier check | REAPPRAISAL_RECEIVED | Sale officer | SVAF, Agent Runtime | 2 working days |
| R-DIS-17 | Asset disposal | D8.1 to D8.3 | REAPPRAISAL_RECEIVED | VALUE_ACCEPTED | outlier_flag = N or officer_accepted = Y | Update the appraised value and reset the list and floor price inputs | ASSET_HELD | Workbench | SVAF, Workbench | None |
| R-DIS-18 | Asset disposal | D8.1 to D8.3 | REAPPRAISAL_RECEIVED | VALUE_REJECTED | officer_accepted = N | Re-order the appraisal and record the reason | REAPPRAISAL_ORDERED | Valuer | SVAF, Decision Log | None |
| R-DIS-19 | Asset disposal | D8.1 to D8.3 | ASSET_HELD | READY_TO_SELL | current_appraisal = Y and title_status = clear | Pricing agent recommends the disposal route with reasons and the COLLINS economics | ROUTE_RECOMMENDED | Sale officer | Agent Runtime, COLLINS | 2 working days |
| R-DIS-20 | Asset disposal | D8.1 to D8.3 | ROUTE_RECOMMENDED | ROUTE_SUBMITTED | Any | Route the recommendation to the approver by the delegation of authority | ROUTE_WITH_APPROVER | Sale officer | Rules component, Committee View | 2 working days |
| R-DIS-21 | Asset disposal | D8.1 to D8.3 | ROUTE_WITH_APPROVER | ROUTE_APPROVED | route = auction and inside the limit | Approve the portal auction route and log the decision | ROUTE_APPROVED_AUCTION | Sale officer | Case Workspace, Decision Log | None |
| R-DIS-22 | Asset disposal | D8.1 to D8.3 | ROUTE_WITH_APPROVER | ROUTE_APPROVED | route = auction and appraised_value above THB 50m | Send the asset to sealed bids and approve at committee | ROUTE_APPROVED_AUCTION | Committee | Committee View, Decision Log | None |
| R-DIS-23 | Asset disposal | D8.1 to D8.3 | ROUTE_WITH_APPROVER | ROUTE_APPROVED | route = RAMC and committee approved | Produce the transfer price from the governed template | ROUTE_APPROVED_RAMC | Sale officer | Calculation Service, Committee View | None |
| R-DIS-24 | Asset disposal | D8.1 to D8.3 | ROUTE_WITH_APPROVER | ROUTE_APPROVED | route = buy_back and second_signature given | Agree the buy-back terms at the template price | ROUTE_APPROVED_BUYBACK | Sale officer | Calculation Service, Case Workspace | None |
| R-DIS-25 | Asset disposal | D8.1 to D8.3 | ROUTE_WITH_APPROVER | ROUTE_APPROVED | route = rental | Set the rental terms and the auto-debit, and hold the asset as rented | RENTAL_ACTIVE | Sale officer | ATS | None |
| R-DIS-26 | Asset disposal | D8.1 to D8.3 | ROUTE_WITH_APPROVER | ROUTE_APPROVED | route = broker and asset_type in (commercial_property, land) | Instruct the broker on the portal for a fixed term | BROKER_INSTRUCTED | Broker | Partner Portal | per instruction term |
| R-DIS-27 | Asset disposal | D8.1 to D8.3 | ROUTE_WITH_APPROVER | ROUTE_REFUSED | approver_decision = refused | Return the asset to hold with the reason recorded | ASSET_HELD | Sale officer | Decision Log | None |
| R-DIS-28 | Asset disposal | D8.1 to D8.3 | ROUTE_APPROVED_AUCTION | PRICE_MODEL_RUN | Any | Pricing agent proposes the opening price and the floor price as the reserve | PRICE_PROPOSED | Sale officer | Agent Runtime, COLLINS | 1 working day |
| R-DIS-29 | Asset disposal | D8.1 to D8.3 | PRICE_PROPOSED | FLOOR_APPROVED_BY_OFFICER | officer_approved = Y | Fix the floor as the reserve and set the step schedule by asset class | FLOOR_APPROVED | Workbench | Rules component | None |
| R-DIS-30 | Asset disposal | D8.1 to D8.3 | FLOOR_APPROVED | VENDOR_REQUIRED | asset_type = vehicle | Allocate the asset to the vendor with the highest predicted price on the scorecard, not by distance | VENDOR_ALLOCATED | Auction and remarketing vendor | Rules component, Partner Portal | 2 working days |
| R-DIS-31 | Asset disposal | D8.1 to D8.3 | VENDOR_ALLOCATED | VENDOR_UNAVAILABLE | vendor_capacity = N or panel_status = suspended | Re-allocate to the next vendor on the scorecard | VENDOR_ALLOCATED | Partner and agency manager | Rules component, Partner Portal | None |
| R-DIS-32 | Asset disposal | D8.1 to D8.3 | VENDOR_ALLOCATED | VENDOR_ACCEPTED | vendor_capacity = Y and inspection form complete | Vendor lists the asset at the starting bid on the portal | LISTING_LIVE | Auction and remarketing vendor | Partner Portal, auction portal | 2 working days |
| R-DIS-33 | Asset disposal | D8.1 to D8.3 | FLOOR_APPROVED | LISTING_EVIDENCE_COMPLETE | photographs_count above 0 and inspection_report present and title_status = clear | Publish the listing to HOME.SCB, the EASY app and the auction portal, with the floor not published | LISTING_LIVE | Workbench | HOME.SCB, auction portal | per asset class |
| R-DIS-34 | Asset disposal | D8.1 to D8.3 | FLOOR_APPROVED | LISTING_EVIDENCE_MISSING | photographs_count = 0 or inspection_report absent | Block publication and raise a document task | LISTING_BLOCKED | Sale officer | Document Hub | 5 working days |
| R-DIS-35 | Asset disposal | D8.1 to D8.3 | LISTING_BLOCKED | EVIDENCE_SUPPLIED | photographs and inspection report present | Publish the listing | LISTING_LIVE | Workbench | Document Hub, auction portal | None |
| R-DIS-36 | Asset disposal | D8.1 to D8.3 | LISTING_LIVE | ROUND_OPENED | schedule step due | Open the round at the scheduled price step | ROUND_OPEN | Auction and remarketing vendor | auction portal, Workbench scheduler | per schedule |
| R-DIS-37 | Asset disposal | D8.1 to D8.3 | ROUND_OPEN | BID_PLACED | Any | Record the bid against the round and the asset | BID_RECEIVED | Workbench | auction portal | None |
| R-DIS-38 | Asset disposal | D8.1 to D8.3 | ROUND_OPEN | ROUND_CLOSED_NO_BID | bid_count = 0 and price_at_round above floor_price | Step the price down on the published schedule and open the next round | ROUND_OPEN | Workbench | Rules component, Workbench scheduler | per schedule |
| R-DIS-39 | Asset disposal | D8.1 to D8.3 | ROUND_OPEN | FLOOR_REACHED_NO_BID | bid_count = 0 and price_at_round = floor_price | Close the listing and raise the no-bid outcome | NO_BID_AT_FLOOR | Sale officer | auction portal, Workbench | None |
| R-DIS-40 | Asset disposal | D8.1 to D8.3 | BID_RECEIVED | BID_AT_OR_ABOVE_FLOOR | bid_amount at or above floor_price | Accept the bid and agree the sale | SALE_AGREED | Sale officer | Case Workspace, auction portal | 1 working day |
| R-DIS-41 | Asset disposal | D8.1 to D8.3 | BID_RECEIVED | BID_BELOW_FLOOR | bid_amount below floor_price | Route the bid for a second signature | SECOND_SIGNATURE_PENDING | Committee | Committee View | 2 working days |
| R-DIS-42 | Asset disposal | D8.1 to D8.3 | SECOND_SIGNATURE_PENDING | SECOND_SIGNATURE_GIVEN | second_signature_by present | Accept the bid below the floor and agree the sale | SALE_AGREED | Sale officer | Case Workspace, Decision Log | None |
| R-DIS-43 | Asset disposal | D8.1 to D8.3 | SECOND_SIGNATURE_PENDING | SECOND_SIGNATURE_REFUSED | second_signature_by absent | Reject the bid and re-list the asset | RELISTED | Sale officer | Workbench, Decision Log | None |
| R-DIS-44 | Asset disposal | D8.1 to D8.3 | NO_BID_AT_FLOOR | RELIST_RULE_APPLIED | relist_count below the re-list limit | Re-list the asset and order a re-appraisal where the cycle is due | RELISTED | Sale officer | Workbench, SVAF | None |
| R-DIS-45 | Asset disposal | D8.1 to D8.3 | RELISTED | ROUTE_REVIEW_REQUIRED | Any | Send the asset back for a disposal route review | ROUTE_RECOMMENDED | Sale officer | Agent Runtime, Case Workspace | 2 working days |
| R-DIS-46 | Asset disposal | D8.1 to D8.3 | NO_BID_AT_FLOOR | RELIST_LIMIT_REACHED | relist_count at or above the re-list limit | Hand the asset and the residual to the debt sale route | TO_DEBT_SALE | Debt sale officer | Workbench | None |
| R-DIS-47 | Asset disposal | D8.1 to D8.3 | SALE_AGREED | AWARD_MADE | Any | Start the five-day payment term | AWAITING_PAYMENT | Buyer | auction portal, ALS core and GL | 5 calendar days |
| R-DIS-48 | Asset disposal | D8.1 to D8.3 | AWAITING_PAYMENT | PAYMENT_RECEIVED | payment_received_at at or before payment_due_date | Confirm the sale and start the title transfer | TITLE_TRANSFER_PENDING | Sale officer | ALS core and GL | None |
| R-DIS-49 | Asset disposal | D8.1 to D8.3 | AWAITING_PAYMENT | PAYMENT_TERM_EXPIRED | payment absent and payment_due_date passed | Cancel the award, score the vendor and reopen the round | AWARD_CANCELED | Sale officer | auction portal, Partner Portal | None |
| R-DIS-50 | Asset disposal | D8.1 to D8.3 | AWARD_CANCELED | ROUND_REOPENED | Any | Reopen the round at the same price step | ROUND_OPEN | Auction and remarketing vendor | auction portal | None |
| R-DIS-51 | Asset disposal | D8.1 to D8.3 | TITLE_TRANSFER_PENDING | REGISTRATION_TRANSFERRED | asset_type = vehicle | Transfer the registration through SCIS | ASSET_SOLD | Workbench | SCIS | 5 working days |
| R-DIS-52 | Asset disposal | D8.1 to D8.3 | TITLE_TRANSFER_PENDING | TITLE_REGISTERED | asset_type = property | Release the documents from custody and record the transfer at the Land Office | ASSET_SOLD | Sale officer | the Land Office, Document Hub | 10 working days |
| R-DIS-53 | Asset disposal | D8.1 to D8.3 | TITLE_TRANSFER_PENDING | TRANSFER_REJECTED | SCIS or the Land Office rejects the transfer | Hold the transfer and raise a document task | TITLE_BLOCKED | Sale officer | SCIS, the Land Office, Document Hub | 5 working days |
| R-DIS-54 | Asset disposal | D8.1 to D8.3 | ASSET_SOLD | PROCEEDS_POSTED | Any | Apply the proceeds to the case and the loan account, and match the vendor fee | PROCEEDS_APPLIED | Workbench | ALS core and GL, Agent Runtime | same day |
| R-DIS-55 | Asset disposal | D8.1 to D8.3 | PROCEEDS_APPLIED | SHORTFALL_CALCULATED | shortfall_amount above 0 | Raise the residual for the D9 decision | SHORTFALL_RAISED | Write-off team | Rules component | None |
| R-DIS-56 | Asset disposal | D8.1 to D8.3 | PROCEEDS_APPLIED | NO_SHORTFALL | shortfall_amount at or below 0 | Close the case and stop every timer | CASE_CLOSED_NO_SHORTFALL | Workbench | Workbench, ALS core and GL | None |
| R-DIS-57 | Asset disposal | D8.1 to D8.3 | SHORTFALL_RAISED | RESIDUAL_ROUTED | residual_route = write_off | Hand the residual to the write-off route | TO_WRITEOFF | Write-off committee | Workbench | None |
| R-DIS-58 | Asset disposal | D8.1 to D8.3 | SHORTFALL_RAISED | RESIDUAL_ROUTED | residual_route = debt_sale | Hand the residual to the debt sale route | TO_DEBT_SALE | Debt sale officer | Workbench | None |
| R-DIS-59 | Asset disposal | D8.1 to D8.3 | ROUTE_APPROVED_RAMC | TRANSFER_INSTRUCTED | transfer_price from the template version | Instruct the RAMC or joint venture transfer on the portal | RAMC_TRANSFER_PENDING | RAMC | Partner Portal, Calculation Service | per agreement |
| R-DIS-60 | Asset disposal | D8.1 to D8.3 | RAMC_TRANSFER_PENDING | TRANSFER_COMPLETED | Any | Post the transfer and set the asset to transferred | ASSET_TRANSFERRED | Workbench | ALS core and GL, AMIS | None |
| R-DIS-61 | Asset disposal | D8.1 to D8.3 | ROUTE_APPROVED_BUYBACK | BUYBACK_TERMS_SIGNED | customer_funded = Y | Complete the buy-back at the governed template price | SALE_AGREED | Sale officer | Calculation Service, ALS core and GL | None |
| R-DIS-62 | Asset disposal | D8.1 to D8.3 | ROUTE_APPROVED_BUYBACK | BUYBACK_FUNDING_FAILED | customer_funded = N | Return the asset to hold and review the route | ASSET_HELD | Sale officer | Workbench, Decision Log | None |
| R-DIS-63 | Asset disposal | D8.1 to D8.3 | RENTAL_ACTIVE | TENANT_DEFAULTED | rental_arrears above the threshold | Return the asset to the hold state for a route review | ASSET_HELD | Sale officer | ATS, Workbench | None |
| R-DIS-64 | Asset disposal | D8.1 to D8.3 | BROKER_INSTRUCTED | BROKER_SOLD | sale price at or above the approved floor | Complete the sale and pay the broker fee on acceptance | SALE_AGREED | Sale officer | Partner Portal, ALS core and GL | None |
| R-DIS-65 | Asset disposal | D8.1 to D8.3 | BROKER_INSTRUCTED | BROKER_TERM_EXPIRED | instruction_term passed and no sale | Withdraw the instruction and review the route | ROUTE_RECOMMENDED | Sale officer | Partner Portal | None |
| R-DIS-66 | Asset disposal | D8.1 to D8.3 | ASSET_HELD | DEVIATION_RAISED | deviation_open in (X1, X2, X3, X4, X5, X7) | Pause the disposal, stop contact where required and route to the deviation owner | DISPOSAL_PAUSED_DEVIATION | Deviation owner | Workbench, Decision Log | None |
| R-DIS-67 | Asset disposal | D8.1 to D8.3 | LISTING_LIVE | DEVIATION_RAISED | deviation_open in (X1, X4, X5) | Pause the listing and the price schedule | DISPOSAL_PAUSED_DEVIATION | Deviation owner | Workbench, auction portal | None |
| R-DIS-68 | Asset disposal | D8.1 to D8.3 | DISPOSAL_PAUSED_DEVIATION | DEVIATION_CLEARED | deviation_open = none | Resume the asset at the state it paused in | ASSET_HELD | Sale officer | Workbench | None |
| R-DIS-69 | Asset disposal | D8.1 to D8.3 | DISPOSAL_PAUSED_DEVIATION | BANKRUPTCY_CONFIRMED | deviation = X5 | Hand the asset to the official receiver and close the disposal route | TO_WRITEOFF | Legal | LIT, the Legal Execution Department | None |
| R-DIS-70 | Asset disposal | D8.1 to D8.3 | ROUTE_WITH_APPROVER | ROUTE_APPROVED | route is not one of the five approved routes | Hold the case, name the missing field and raise a task for the owner | UNMATCHED_EXCEPTION | Sale officer | Workbench | same day |
| R-DIS-71 | Asset disposal | D8.1 to D8.3 | SHORTFALL_RAISED | RESIDUAL_ROUTED | residual_route is not set | Hold the case, name the missing field and raise a task for the owner | UNMATCHED_EXCEPTION | Sale officer | Workbench | same day |
| R-DIS-72 | Asset disposal | D8.1 to D8.3 | UNMATCHED_EXCEPTION | MANUAL_DECISION_RECORDED | Any | Sale officer records the decision and the missing field; the rule gap is logged for the center of excellence | ASSET_HELD | Sale officer | Workbench | 2 working days |
| R-DS-01 | Debt sale | D8.4 | LOT_CANDIDATE_SELECTED | DEBT_SALE_CYCLE_OPENED | eligibility rule passes and deviation_open = none | Select the accounts for sale from the case list | LOT_BUILT | Debt sale officer | Rules component, Recovery Data Store | per monthly cycle |
| R-DS-02 | Debt sale | D8.4 | LOT_CANDIDATE_SELECTED | ACCOUNT_EXCLUDED | deviation_open in (X1 to X7) or fraud_flag = Y | Remove the account from the pool with a recorded reason | CASE_EXCLUDED | Case owner | Workbench, Aric | None |
| R-DS-03 | Debt sale | D8.4 | CASE_EXCLUDED | EXCLUSION_CLEARED | deviation_open = none | Return the account to the case list for the next cycle | BACK_TO_CASE_LIST | Debt sale officer | Workbench | next cycle |
| R-DS-04 | Debt sale | D8.4 | LOT_BUILT | LOT_PRICED | lot agent estimate returned with COLLINS | Propose the lots, the tiered buyer terms and the reserve price | LOT_WITH_COMMITTEE | Committee | Agent Runtime, COLLINS, Case Workspace | 5 working days |
| R-DS-05 | Debt sale | D8.4 | LOT_BUILT | LOT_TOO_THIN | account_count below the minimum lot size | Merge the accounts into the next lot | LOT_BUILT | Debt sale officer | Workbench | None |
| R-DS-06 | Debt sale | D8.4 | LOT_WITH_COMMITTEE | LOT_APPROVED_BY_COMMITTEE | reserve and terms approved inside the delegation | Approve the lot, the reserve and the tiered terms, and log the decision | LOT_APPROVED | Debt sale officer | Committee View, Decision Log | None |
| R-DS-07 | Debt sale | D8.4 | LOT_WITH_COMMITTEE | RESERVE_RAISED | committee raises the reserve | Reprice the lot and return it to the committee | LOT_WITH_COMMITTEE | Committee | Committee View, Agent Runtime | None |
| R-DS-08 | Debt sale | D8.4 | LOT_WITH_COMMITTEE | LOT_REFUSED | committee withdraws the lot | Withdraw the lot with a recorded reason | LOT_WITHDRAWN | Debt sale officer | Decision Log | None |
| R-DS-09 | Debt sale | D8.4 | LOT_WITHDRAWN | ACCOUNTS_RETURNED | Any | Return the accounts to the case list | BACK_TO_CASE_LIST | Case owner | Workbench | None |
| R-DS-10 | Debt sale | D8.4 | LOT_APPROVED | TAPE_BUILD_RUN | Any | Build the masked data tape under the PII masking rules | TAPE_PREPARED | Workbench | PII service, Recovery Data Store, Document Hub | 3 working days |
| R-DS-11 | Debt sale | D8.4 | TAPE_PREPARED | MASKING_CHECK_FAILED | an unmasked identifier is found on the tape | Reject the tape and rebuild it | TAPE_REJECTED | Workbench | PII service, Document Hub | None |
| R-DS-12 | Debt sale | D8.4 | TAPE_REJECTED | TAPE_REBUILT | masking check passes | Return the tape for data room release | TAPE_PREPARED | Workbench | PII service | None |
| R-DS-13 | Debt sale | D8.4 | TAPE_PREPARED | MASKING_CHECK_PASSED | no unmasked identifier | Open the data room to buyers who have signed the non-disclosure agreement | DATA_ROOM_OPEN | Debt sale officer | buyer portal, Document Hub | per cycle |
| R-DS-14 | Debt sale | D8.4 | DATA_ROOM_OPEN | BUYER_REQUESTED_ACCESS | nda_signed_at present | Run the KYC, licensing and eligibility check on the bidder | BUYER_PENDING_KYC | Workbench | Rules component, buyer portal | 3 working days |
| R-DS-15 | Debt sale | D8.4 | BUYER_PENDING_KYC | KYC_PASSED | kyc_status = passed and licence_expiry after today and panel_status = active | Admit the buyer to the data room | BUYER_CLEARED | Buyer | buyer portal | None |
| R-DS-16 | Debt sale | D8.4 | BUYER_PENDING_KYC | KYC_FAILED | kyc_status = failed or license expired or panel_status = suspended | Refuse access and record the reason | BUYER_REJECTED | Debt sale officer | Decision Log, buyer portal | None |
| R-DS-17 | Debt sale | D8.4 | BUYER_CLEARED | BIDDING_WINDOW_OPENED | Any | Open bidding on the lot at the tiered terms | BIDDING_OPEN | Buyer | buyer portal | per cycle |
| R-DS-18 | Debt sale | D8.4 | BIDDING_OPEN | BID_SUBMITTED | Any | Record the bid against the lot and the buyer | BIDS_RECEIVED | Workbench | buyer portal | None |
| R-DS-19 | Debt sale | D8.4 | BIDS_RECEIVED | BIDDING_WINDOW_CLOSED | best_bid at or above reserve_price | Test the price against the reserve and the 54 percent cap, and route the award | AWARD_PENDING | Debt sale officer | Case Workspace, Committee View | 2 working days |
| R-DS-20 | Debt sale | D8.4 | BIDS_RECEIVED | BEST_BID_BELOW_RESERVE | best_bid below reserve_price | Raise the below-reserve outcome to the committee | BID_BELOW_RESERVE | Debt sale officer | Committee View | None |
| R-DS-21 | Debt sale | D8.4 | BID_BELOW_RESERVE | LOT_REOFFERED | committee approves a re-offer at a revised reserve | Re-offer the lot at the revised reserve | BIDDING_OPEN | Buyer | buyer portal, Committee View | None |
| R-DS-22 | Debt sale | D8.4 | BID_BELOW_RESERVE | LOT_NOT_CLEARED | committee refuses a re-offer | Withdraw the lot | LOT_WITHDRAWN | Debt sale officer | Decision Log | None |
| R-DS-23 | Debt sale | D8.4 | AWARD_PENDING | AWARD_CONFIRMED | price tested against the reserve and the 54 percent cap, and recorded | Award the lot and generate the sale agreement and the customer notices | LOT_AWARDED | Debt sale officer | Document Hub, buyer portal | None |
| R-DS-24 | Debt sale | D8.4 | LOT_AWARDED | SETTLEMENT_TERM_STARTED | Any | Start the settlement term and await payment | SETTLEMENT_PENDING | Buyer | buyer portal, ALS core and GL | per agreed settlement period |
| R-DS-25 | Debt sale | D8.4 | SETTLEMENT_PENDING | BUYER_SETTLED | payment received in full | Confirm settlement and release the data transfer | SETTLED | Workbench | ALS core and GL | None |
| R-DS-26 | Debt sale | D8.4 | SETTLEMENT_PENDING | BUYER_CANCELED | cancellation recorded with a reason | Cancel the award and score the cancellation against the buyer | AWARD_CANCELED_DS | Debt sale officer | Decision Log, Recovery Data Store | None |
| R-DS-27 | Debt sale | D8.4 | SETTLEMENT_PENDING | SETTLEMENT_TERM_EXPIRED | payment absent and the settlement period passed | Cancel the award and score the buyer | AWARD_CANCELED_DS | Debt sale officer | Decision Log, buyer portal | None |
| R-DS-28 | Debt sale | D8.4 | AWARD_CANCELED_DS | LOT_REOFFERED_AFTER_CANCEL | another qualified bidder exists | Re-offer the lot to the next qualified bidder | BIDDING_OPEN | Buyer | buyer portal | None |
| R-DS-29 | Debt sale | D8.4 | SETTLED | DATA_TRANSFER_RUN | Any | Transfer the account data to the buyer | DATA_TRANSFERRED | Workbench | buyer portal | 5 working days |
| R-DS-30 | Debt sale | D8.4 | DATA_TRANSFERRED | DERECOGNITION_RUN | Any | Derecognise the balance on the account | DERECOGNISED | Workbench | ALS core and GL | None |
| R-DS-31 | Debt sale | D8.4 | DERECOGNISED | GL_POSTING_RUN | Any | Post to the general ledger and send the provision input to Finance | GL_POSTED | Credit Administration | ALS core and GL, Finance provision feed | month-end close |
| R-DS-32 | Debt sale | D8.4 | DERECOGNISED | POSTING_REJECTED | ALS or the general ledger rejects the posting | Hold the posting and raise an exception task | POSTING_REJECTED_DS | Credit Administration | integration adapters | 2 working days |
| R-DS-33 | Debt sale | D8.4 | POSTING_REJECTED_DS | POSTING_CORRECTED | the rejection cause is cleared | Re-post to ALS and the general ledger | GL_POSTED | Credit Administration | ALS core and GL | None |
| R-DS-34 | Debt sale | D8.4 | GL_POSTED | CLAIM_WINDOW_CLOSED | no put-back claim inside the claim window | Close the lot and record realized recovery by lot and by buyer | LOT_CLOSED | Debt sale officer | Recovery Data Store, Power BI | per claim window |
| R-DS-35 | Debt sale | D8.4 | GL_POSTED | PUTBACK_CLAIMED | buyer raises a claim inside the sale terms | Record the claim and review it against the terms | PUTBACK_RAISED | Debt sale officer | buyer portal, Decision Log | 10 working days |
| R-DS-36 | Debt sale | D8.4 | PUTBACK_RAISED | PUTBACK_ACCEPTED | the claim is valid under the sale terms | Return the account to the bank and adjust the settlement | PUTBACK_UPHELD | Debt sale officer | ALS core and GL, buyer portal | None |
| R-DS-37 | Debt sale | D8.4 | PUTBACK_UPHELD | ACCOUNT_RETURNED | Any | Reverse the derecognition and return the account to the case list | BACK_TO_CASE_LIST | Case owner | ALS core and GL, Workbench | None |
| R-DS-38 | Debt sale | D8.4 | PUTBACK_RAISED | PUTBACK_REFUSED_BY_BANK | the claim falls outside the sale terms | Refuse the claim with a recorded reason | PUTBACK_REFUSED | Debt sale officer | Decision Log, buyer portal | None |
| R-DS-39 | Debt sale | D8.4 | PUTBACK_REFUSED | CLAIM_CLOSED | Any | Close the lot with realized recovery recorded | LOT_CLOSED | Debt sale officer | Recovery Data Store | None |
| R-DS-40 | Debt sale | D8.4 | BUYER_REJECTED | BUYER_REMEDIATED | the buyer supplies the missing KYC or license evidence inside the window | Re-open the qualification check | BUYER_PENDING_KYC | Debt sale officer | Buyer portal, Workbench | 10 working days |
| R-DS-41 | Debt sale | D8.4 | BUYER_REJECTED | BUYER_BARRED | no evidence supplied inside the window, or the failure is a license breach | Remove the buyer from the panel and release the lot to the next bidder | BACK_TO_CASE_LIST | Head of Asset Liquidity | Buyer portal, Workbench | None |
| R-WO-01 | Write-off | D9 | SCAN_DUE | MONTHLY_SCAN_STARTED | cut_off_date reached and the ALS load is complete | Test every open case against the eligibility rule on both tracks and the tax criteria | POPULATION_PROPOSED | Write-off team | Rules component, COLLINS, ALS core and GL | monthly cut-off |
| R-WO-02 | Write-off | D9 | SCAN_DUE | ALS_LOAD_FAILED | the ALS extract is absent for the cut-off date | Hold the scan and raise an incident | SCAN_HELD | Write-off team | ALS core and GL | 1 working day |
| R-WO-03 | Write-off | D9 | SCAN_DUE | TAX_CRITERIA_UNPUBLISHED | tax_criteria_version absent | Hold the scan until Finance publishes the version | SCAN_HELD | Write-off team | Reference data, Finance provision feed | None |
| R-WO-04 | Write-off | D9 | SCAN_HELD | LOAD_RESTORED | the ALS extract is complete and the tax criteria published | Restart the scan for the cut-off date | SCAN_DUE | Workbench | Reference data | None |
| R-WO-05 | Write-off | D9 | POPULATION_PROPOSED | PACK_BUILT | Any | Write-off agent prepares the pack: balance, provision carried, route history, legal and asset state, residual | PACK_PREPARED | Write-off team | Agent Runtime, Document Hub | 3 working days |
| R-WO-06 | Write-off | D9 | POPULATION_PROPOSED | CASE_HAS_OPEN_DEVIATION | deviation_open in (X1 to X7) | Hold the case out of the population and route it to the deviation handler | CASE_REMOVED_BY_TEAM | Deviation owner | Workbench, Decision Log | None |
| R-WO-07 | Write-off | D9 | POPULATION_PROPOSED | TEAM_REMOVED_CASE | removal_reason present | Remove the case from the proposed population with the reason recorded | CASE_REMOVED_BY_TEAM | Write-off team | Case Workspace, Decision Log | None |
| R-WO-08 | Write-off | D9 | CASE_REMOVED_BY_TEAM | REMOVAL_CLEARED | the deviation is cleared or the reason is resolved | Return the case to the next monthly scan | SCAN_DUE | Write-off team | Workbench | next cut-off |
| R-WO-09 | Write-off | D9 | PACK_PREPARED | PACK_CHECK_FAILED | provision_carried absent or pack_document_id absent | Hold the pack and raise a data quality task | PACK_INCOMPLETE | Write-off team | Recovery Data Store, Document Hub | 2 working days |
| R-WO-10 | Write-off | D9 | PACK_INCOMPLETE | PACK_COMPLETED | provision_carried and the pack document are present | Route the pack to the committee | WITH_COMMITTEE | Write-off committee | Case and Workflow Service, Committee View | None |
| R-WO-11 | Write-off | D9 | PACK_PREPARED | PACK_ROUTED | amount inside the write-off committee limit | Route the pack to the committee and schedule the meeting | WITH_COMMITTEE | Write-off committee | Committee View, Workbench scheduler | before the scheduled meeting |
| R-WO-12 | Write-off | D9 | PACK_PREPARED | LIMIT_EXCEEDED | amount above the write-off committee limit | Route the pack to the credit approval committee chaired by the product head with Risk | ESCALATED_TO_CREDIT_COMMITTEE | Credit approval committee | Committee View, Reference data | before the scheduled meeting |
| R-WO-13 | Write-off | D9 | ESCALATED_TO_CREDIT_COMMITTEE | CREDIT_COMMITTEE_APPROVED | approved inside the delegation with Risk | Record the final call and release the case to posting | APPROVED | Credit Administration | Committee View, Decision Log | None |
| R-WO-14 | Write-off | D9 | ESCALATED_TO_CREDIT_COMMITTEE | CREDIT_COMMITTEE_REJECTED | decision_reason present | Return the case to the pursue track | RETURNED_TO_PURSUE | Case owner | Committee View, Decision Log | None |
| R-WO-15 | Write-off | D9 | WITH_COMMITTEE | COMMITTEE_APPROVED | approved inside the delegation | Record the final call, the approver and the limit applied, and release to posting | APPROVED | Credit Administration | Committee View, Decision Log | None |
| R-WO-16 | Write-off | D9 | WITH_COMMITTEE | COMMITTEE_REJECTED | decision_reason present | Return the case to the pursue track | RETURNED_TO_PURSUE | Case owner | Committee View, Decision Log | None |
| R-WO-17 | Write-off | D9 | WITH_COMMITTEE | COMMITTEE_DEFERRED | review_date present | Set the review timer and hold the case for the next scan | DEFERRED | Write-off team | Workbench scheduler, Committee View | to the review date |
| R-WO-18 | Write-off | D9 | WITH_COMMITTEE | DECISION_INCOMPLETE | decision_reason absent on a reject, or review_date absent on a defer | Refuse the decision and return it to the committee | WITH_COMMITTEE | Write-off committee | Committee View | None |
| R-WO-19 | Write-off | D9 | DEFERRED | REVIEW_DATE_REACHED | Any | Return the case to the next monthly scan | SCAN_DUE | Write-off team | Workbench scheduler, Workbench | next cut-off |
| R-WO-20 | Write-off | D9 | APPROVED | POSTING_TASK_CREATED | the posting window is open and no unmatched payment is in flight | Create the posting task | POSTING_PENDING | Credit Administration | Workbench scheduler, ALS core and GL | month-end close window |
| R-WO-21 | Write-off | D9 | POSTING_PENDING | ALS_POSTING_CONFIRMED | ALS and the general ledger return a reference | Record the posting reference | POSTED | Credit Administration | ALS core and GL | None |
| R-WO-22 | Write-off | D9 | POSTING_PENDING | ALS_POSTING_REJECTED | result = rejected | Hold the posting and raise the rejection | POSTING_REJECTED | Credit Administration | ALS core and GL | 2 working days |
| R-WO-23 | Write-off | D9 | POSTING_REJECTED | REJECTION_CLEARED | retry_count below the retry limit and the cause is cleared | Re-post to ALS and the general ledger | POSTING_PENDING | Credit Administration | integration adapters | None |
| R-WO-24 | Write-off | D9 | POSTING_REJECTED | RETRY_LIMIT_REACHED | retry_count at or above the retry limit | Raise the write-off exception for correction | WRITEOFF_EXCEPTION | Owner to confirm with C&R | Rules component, Case Workspace | to confirm with Credit Administration |
| R-WO-25 | Write-off | D9 | POSTED | PROVISION_RELEASE_RUN | provision_carried present | Release the provision carried and record the released amount | PROVISION_RELEASED | Workbench | Rules component, ALS core and GL | None |
| R-WO-26 | Write-off | D9 | PROVISION_RELEASED | FINANCE_FEED_RUN | Any | Send the provision inputs and the tax file to Finance | FINANCE_FEED_SENT | Credit Administration | Finance provision feed | month-end close |
| R-WO-27 | Write-off | D9 | FINANCE_FEED_SENT | FINANCE_REJECTED_FILE | finance_feed_status = rejected | Retry the feed and raise a task after the retry limit | FINANCE_FEED_REJECTED | Credit Administration | Finance provision feed | 2 working days |
| R-WO-28 | Write-off | D9 | FINANCE_FEED_REJECTED | FEED_ACCEPTED_ON_RETRY | finance_feed_status = accepted | Record the tax file reference | FINANCE_FEED_SENT | Credit Administration | Finance provision feed | None |
| R-WO-29 | Write-off | D9 | FINANCE_FEED_SENT | POST_CHARGEOFF_RULE_RUN | finance_feed_status = accepted | Decide the post charge-off treatment under D9.3 | PLACEMENT_DECIDED | Partner and agency manager | Rules component | 5 working days |
| R-WO-30 | Write-off | D9 | PLACEMENT_DECIDED | SOFT_RECOVERY_SELECTED | placement_type = soft_recovery and an agency on the panel has capacity | Place the account with the agency chosen on measured return and send the instruction | PLACED_WITH_AGENCY | Outsourced agency | Partner Portal, OA portal | same day on the portal |
| R-WO-31 | Write-off | D9 | PLACEMENT_DECIDED | NO_AGENCY_CAPACITY | no agency on the panel has capacity | Hold the placement and escalate on the timer | PLACEMENT_DECIDED | Partner and agency manager | Partner Portal | 5 working days |
| R-WO-32 | Write-off | D9 | PLACEMENT_DECIDED | SALE_SELECTED | placement_type = sale | Hand the charged-off population to the debt sale route | SOLD_POST_CHARGEOFF | Debt sale officer | buyer portal, Workbench | per cycle |
| R-WO-33 | Write-off | D9 | PLACED_WITH_AGENCY | AGENCY_REPORTED_RESULT | the result is reported on the portal | Attach contact, promise and cash to the case the same day | PLACED_WITH_AGENCY | Outsourced agency | OA portal, Partner Portal | same day |
| R-WO-34 | Write-off | D9 | PLACED_WITH_AGENCY | AGENCY_UNDERPERFORMS | measured return below the panel threshold or conduct_breaches above 0 | Recall the placement and record the reason | PLACEMENT_RECALLED | Partner and agency manager | Partner Portal, Decision Log | None |
| R-WO-35 | Write-off | D9 | PLACEMENT_RECALLED | REPLACEMENT_MADE | another agency on the panel has capacity | Place the account with the next agency on the scorecard | PLACED_WITH_AGENCY | Outsourced agency | Partner Portal | None |
| R-WO-36 | Write-off | D9 | PLACED_WITH_AGENCY | PLACEMENT_TERM_EXPIRED | ends_at passed and recovered_amount = 0 | Close the placement and start the retention timer | RETENTION_RUNNING | Workbench | Partner Portal, Workbench scheduler | None |
| R-WO-37 | Write-off | D9 | PLACED_WITH_AGENCY | PAYMENT_RECEIVED_AFTER_CHARGEOFF | the payment matches the case and the placement | Post the recovery as post charge-off income and calculate the agency fee | PAYMENT_MATCHED | Workbench | ALS core and GL, Agent Runtime | next working day |
| R-WO-38 | Write-off | D9 | PLACED_WITH_AGENCY | PAYMENT_MATCHES_NOTHING | the payment matches no case and no placement | Send the payment to the exception list for clearing | PAYMENT_EXCEPTION | Case owner | Agent Runtime, Case Workspace | 2 working days |
| R-WO-39 | Write-off | D9 | PAYMENT_EXCEPTION | EXCEPTION_CLEARED | the case or the placement is identified | Match the payment and post the income | PAYMENT_MATCHED | Workbench | ALS core and GL | None |
| R-WO-40 | Write-off | D9 | SOLD_POST_CHARGEOFF | PAYMENT_BELONGS_TO_BUYER | the account was sold before the payment arrived | Remit the payment to the buyer under the remittance rule | REMITTED_TO_BUYER | Debt sale officer | ALS core and GL, buyer portal | 5 working days |
| R-WO-41 | Write-off | D9 | PAYMENT_MATCHED | WRITEOFF_QUESTIONED | the payment reopens a question on the write-off | Raise the exception and refer it to the committee | WRITEOFF_EXCEPTION | Owner to confirm with C&R | Rules component, Committee View | to confirm with Credit Administration |
| R-WO-42 | Write-off | D9 | POSTED | POPULATION_RECONCILED | approved count and amount equal posted count and amount | Publish completeness and start the retention timer | RETENTION_RUNNING | Workbench | Rules component, Power BI, Workbench scheduler | monthly |
| R-WO-43 | Write-off | D9 | POSTED | POPULATION_NOT_RECONCILED | approved and posted populations differ | Fire the exception and report completeness short | WRITEOFF_EXCEPTION | Owner to confirm with C&R | Rules component, Power BI | to confirm with Credit Administration |
| R-WO-44 | Write-off | D9 | WRITEOFF_EXCEPTION | CORRECTION_REPOST | the owner decides to re-post | Re-post to ALS and the general ledger | POSTING_PENDING | Credit Administration | ALS core and GL | to confirm with Credit Administration |
| R-WO-45 | Write-off | D9 | WRITEOFF_EXCEPTION | CORRECTION_RETURN_TO_SCAN | the owner decides to return the case | Return the case to the next monthly scan | SCAN_DUE | Write-off team | Workbench, Decision Log | next cut-off |
| R-WO-46 | Write-off | D9 | WRITEOFF_EXCEPTION | CORRECTION_REFER_TO_COMMITTEE | the owner refers the case back | Return the pack to the committee | WITH_COMMITTEE | Write-off committee | Committee View | None |
| R-WO-47 | Write-off | D9 | RETENTION_RUNNING | RETENTION_TIMER_EXPIRED | no open placement, no open sale, no open exception, and a retention class on every document | Close the case, stop every timer and write the closing entry with cash recovered and loss | CASE_CLOSED | Workbench | Workbench scheduler, Document Hub, Decision Log | on expiry |
| R-WO-48 | Write-off | D9 | RETENTION_RUNNING | RETENTION_CLASS_MISSING | a document on the case has no retention class | Hold closure and raise a Document Hub task | RETENTION_RUNNING | Operational Excellence | Document Hub | 5 working days |
| R-WO-49 | Write-off | D9 | CASE_CLOSED | PAYMENT_RECEIVED_AFTER_CHARGEOFF | the payment matches a closed case with no placement | Post the recovery as post charge-off income against the closed case | PAYMENT_MATCHED | Workbench | ALS core and GL | next working day |
| R-WO-50 | Write-off | D9 | SOLD_POST_CHARGEOFF | SALE_SETTLED | buyer settles and the data transfer completes | Record the post charge-off sale and close the case | CASE_CLOSED | Credit Administration | ALS and GL, Workbench | None |
| R-WO-51 | Write-off | D9 | REMITTED_TO_BUYER | REMITTANCE_CONFIRMED | the buyer confirms receipt | Record the remittance against the sold account and close the item | CASE_CLOSED | Credit Administration | ALS and GL, Workbench | 5 working days |
| R-DEV-01 | Deviations | X1 to X7 | ANY_STATE | DEVIATION_FLAGGED | deviation_code in (X1..X7) | Pause the stage clock, keep the prescription clock running, route to the named owner | DEV_FLAGGED | Workbench | Workbench, the Workbench document hub | same day |
| R-DEV-02 | Deviations | X1 to X7 | DEV_FLAGGED | OWNER_ASSIGNED | deviation_code = X1 | Assign to the complaint officer | DEV_WITH_OWNER | Complaint officer | Workbench | None |
| R-DEV-03 | Deviations | X1 to X7 | DEV_FLAGGED | OWNER_ASSIGNED | deviation_code in (X2,X3) | Assign to the specialist; Legal joins X3 for the estate claim | DEV_WITH_OWNER | Specialist, Legal | Workbench | None |
| R-DEV-04 | Deviations | X1 to X7 | DEV_FLAGGED | OWNER_ASSIGNED | deviation_code = X4 | Assign to the fraud team and refer to Aric | DEV_WITH_OWNER | Fraud team | Aric, Workbench | None |
| R-DEV-05 | Deviations | X1 to X7 | DEV_FLAGGED | OWNER_ASSIGNED | deviation_code = X5 | Assign to Legal; file with the official receiver or the LED before the deadline | DEV_WITH_OWNER | Legal | LIT, Workbench | deadline driven |
| R-DEV-06 | Deviations | X1 to X7 | DEV_FLAGGED | OWNER_ASSIGNED | deviation_code in (X6,X7) | Agent handles within policy; a person approves an insurance claim | DEV_WITH_OWNER | Agent, case owner | Workbench | None |
| R-DEV-07 | Deviations | X1 to X7 | DEV_FLAGGED | FLAG_REJECTED | owner marks the flag as not a deviation | Clear the flag, record the reason, resume the clock | DEV_REJECTED | Workbench | Workbench | None |
| R-DEV-08 | Deviations | X1 to X7 | DEV_REJECTED | CLOCK_RESUMED | Any | Return the case to the state it paused in | RESUMED | Previous owner | Workbench | None |
| R-DEV-09 | Deviations | X1 to X7 | DEV_WITH_OWNER | DEVIATION_RESOLVED | deviation_code in (X1,X7) | Record the outcome; the same decision resumes | DEV_RESOLVED | Case owner | Workbench | None |
| R-DEV-10 | Deviations | X1 to X7 | DEV_WITH_OWNER | DEVIATION_RESOLVED | deviation_code = X2 | Route to the restructure assessment | DEV_REROUTE | Restructuring officer | Workbench | None |
| R-DEV-11 | Deviations | X1 to X7 | DEV_WITH_OWNER | INSURANCE_SETTLED | deviation_code = X3 and insurance clears the balance | Close the case | CASE_ENDED | Workbench | ALS, Workbench | None |
| R-DEV-12 | Deviations | X1 to X7 | DEV_WITH_OWNER | ESTATE_CONFIRMED | deviation_code = X3 and insurance does not clear | Return to the route decision against the estate | DEV_REROUTE | Case owner | Workbench | None |
| R-DEV-13 | Deviations | X1 to X7 | DEV_WITH_OWNER | FRAUD_CONFIRMED | deviation_code = X4 and fraud confirmed | Route to write-off; recovery continues under the fraud case | DEV_REROUTE | Write-off team | Aric, Workbench | None |
| R-DEV-14 | Deviations | X1 to X7 | DEV_WITH_OWNER | FRAUD_NOT_CONFIRMED | deviation_code = X4 and fraud not confirmed | Return to the collections decision | DEV_REROUTE | Case owner | EFS, Workbench | None |
| R-DEV-15 | Deviations | X1 to X7 | DEV_WITH_OWNER | BANKRUPTCY_FILED | deviation_code = X5 | Route to litigation, then to write-off after the receiver reports | DEV_REROUTE | Legal, litigation officer | LIT | None |
| R-DEV-16 | Deviations | X1 to X7 | DEV_WITH_OWNER | CONTACT_RESTORED | deviation_code = X6 and a contact point is verified | Close X6 and return to the paused state | DEV_RESOLVED | Case owner | Workbench, NCB | None |
| R-DEV-17 | Deviations | X1 to X7 | DEV_WITH_OWNER | CONTACT_NOT_FOUND | deviation_code = X6 and skip trace exhausted | Route to escalation or to the route decision | DEV_REROUTE | Case owner | Workbench | 30 days |
| R-DEV-18 | Deviations | X1 to X7 | DEV_RESOLVED | CLOCK_RESUMED | Any | Resume the stage clock and return the case | RESUMED | Previous owner | Workbench | None |
| R-DEV-19 | Deviations | X1 to X7 | DEV_REROUTE | ROUTE_REOPENED | Any | Recompute the segment and re-run the hard gates | ROUTE_D6 | Case owner | Workbench | None |
| R-DEV-20 | Deviations | X1 to X7 | DEV_WITH_OWNER | SLA_BREACHED | time in DEV_WITH_OWNER exceeds the deviation service level | Escalate to the team manager and report the breach | DEV_WITH_OWNER | Team manager | Workbench | 10 working days |
| R-DEV-21 | Deviations | X1 to X7 | DEV_FLAGGED | OWNER_ASSIGNED | deviation_code is not one of X1 to X7, or no owner is set for the code | Assign to the case owner's team manager and log the unmapped code | DEV_WITH_OWNER | Team manager | Workbench | same day |
| R-DEV-22 | Deviations | X1 to X7 | DEV_WITH_OWNER | DEVIATION_RESOLVED | otherwise, the outcome does not name a next step | Return the case to the route decision and record that the outcome was not mapped | DEV_REROUTE | Case owner | Workbench | 2 working days |
| R-UNI-01 | Universal rules | All | ANY_ACTIVE | PAYMENT_RECEIVED | arrears cleared in full and days_past_due falls below 90 | Close the recovery case, hand the account back to servicing, release any hold | CASE_CURED_CLOSED | Case owner | ALS, EFS, Workbench | same day |
| R-UNI-02 | Universal rules | All | ANY_ACTIVE | PAYMENT_RECEIVED | part payment that changes the exposure band | Recompute the segment and re-run the owner ladder and the hard gates | ROUTE_D6_REOPEN | Case owner | ALS, Workbench | 1 working day |
| R-UNI-03 | Universal rules | All | ANY_ACTIVE | PAYMENT_RECEIVED | otherwise, the payment matches no plan, sale or lot | Hold the cash on the exception list for the reconciliation agent | EXCEPTION_QUEUE | Case owner | ALS, Workbench | 2 working days |
| R-UNI-04 | Universal rules | All | ANY_ACTIVE | COMPLAINT_RAISED | a complaint is logged against the case | Raise X1, pause the stage clock, apply the contact stop | HELD_DEVIATION | Complaint officer | Workbench | same day |
| R-UNI-05 | Universal rules | All | ANY_ACTIVE | CUSTOMER_DECEASED | a death is confirmed from the registry or a document | Raise X3, stop all contact, hold the case for the specialist and Legal | HELD_DEVIATION | Specialist, Legal | Workbench, the Workbench document hub | same day |
| R-UNI-06 | Universal rules | All | ANY_ACTIVE | VULNERABILITY_IDENTIFIED | hardship or vulnerability is recorded | Raise X2, apply the vulnerable customer treatment rules | HELD_DEVIATION | Specialist | Workbench | same day |
| R-UNI-07 | Universal rules | All | ANY_ACTIVE | BANKRUPTCY_NOTIFIED | a filing or an external seizure is notified | Raise X5, stop enforcement, start the claim deadline clock | HELD_DEVIATION | Legal | LIT, Workbench | deadline driven |
| R-UNI-08 | Universal rules | All | ANY_ACTIVE | FRAUD_FLAGGED | Aric or an officer flags fraud | Raise X4, hold the case, refer to the fraud team | HELD_DEVIATION | Fraud team | Aric, Workbench | same day |
| R-UNI-09 | Universal rules | All | ANY_ACTIVE | DEBT_DISPUTED | the customer disputes the balance or the security | Raise X1, pause recovery action on the disputed amount | HELD_DEVIATION | Complaint officer | Workbench | same day |
| R-UNI-10 | Universal rules | All | ANY_ACTIVE | CONSENT_WITHDRAWN | the customer withdraws consent for a channel | Remove that channel from the contact plan, keep the statutory notices | HELD_CONDUCT | Conduct and QA officer | Workbench | same day |
| R-UNI-11 | Universal rules | All | ANY_ACTIVE | DATA_SUBJECT_REQUEST | a PDPA access, correction or erasure request is received | Hold automated processing on the case, route to Compliance inside the statutory period | HELD_LEGAL | Compliance | Workbench | statutory period |
| R-UNI-12 | Universal rules | All | ANY_ACTIVE | CONTACT_DETAIL_CHANGED | a new verified contact point arrives | Update the contact data product, close X6 if it is open | RESUME_STATE | Workbench | EFS, Workbench, NCB | same day |
| R-UNI-13 | Universal rules | All | ANY_ACTIVE | RELIEF_SCHEME_APPLIED | the account qualifies for a government or bank relief scheme | Apply the scheme terms, pause recovery for the scheme period | HELD_LEGAL | Risk | ACE, Workbench | scheme terms |
| R-UNI-14 | Universal rules | All | ANY_ACTIVE | ROUTE_OVERRIDDEN | an authorized user overrides the route inside the delegation | Record the coded reason, move the case to the chosen route | ROUTE_D6_REOPEN | Case owner | Workbench | same day |
| R-UNI-15 | Universal rules | All | ANY_ACTIVE | OVERRIDE_REFUSED | the override is outside the user's limit | Refuse the change, raise the request to the approver named in the matrix | ESCALATED | Approver per the matrix | Workbench | 1 working day |
| R-UNI-16 | Universal rules | All | ANY_ACTIVE | CASE_CREATED_IN_ERROR | the entry rule fired on bad data and the account is not eligible | Cancel the case with a reason, return the account to collections, keep the audit trail | CANCELED_IN_ERROR | Case owner | EFS, Workbench | 2 working days |
| R-UNI-17 | Universal rules | All | ANY_ACTIVE | DUPLICATE_CASE_FOUND | two cases exist for the same customer and product | Merge into the earlier case, carry the documents and the decision log, close the later one | MERGED | Case owner | Workbench | 2 working days |
| R-UNI-18 | Universal rules | All | ANY_ACTIVE | OWNER_UNAVAILABLE | the owner leaves, is absent beyond the threshold, or the account is reassigned | Reallocate inside the same team by region and workload, keep the state and the clocks | REALLOCATED | Team manager | Workbench | 1 working day |
| R-UNI-19 | Universal rules | All | ANY_ACTIVE | CASELOAD_CAP_BREACHED | the owner is above the maximum caseload | Reallocate the newest cases until the owner is inside the cap | REALLOCATED | Team manager | Workbench | weekly |
| R-UNI-20 | Universal rules | All | ANY_ACTIVE | LEGAL_HOLD_PLACED | a regulator, court or Legal places a hold | Stop every outbound action and every automated decision, keep the clocks visible | HELD_LEGAL | Legal | Workbench | until lifted |
| R-UNI-21 | Universal rules | All | HELD_LEGAL | LEGAL_HOLD_LIFTED | the hold is lifted | Resume the case in the state it paused in, recompute the timers | RESUME_STATE | Case owner | Workbench | same day |
| R-UNI-22 | Universal rules | All | ANY_ACTIVE | CLASSIFICATION_CHANGED | the account is re-aged or reclassified upstream | Recompute the segment, re-run the gates, record the change | ROUTE_D6_REOPEN | Workbench | ALS, Workbench | 1 working day |
| R-UNI-23 | Universal rules | All | ANY_ACTIVE | PRODUCT_MIGRATED | the account moves from ALS to iCore or between systems | Re-point the integration, reconcile the balance, keep the case and its state | RESUME_STATE | Platform team | ALS, iCore, Workbench | 1 working day |
| R-UNI-24 | Universal rules | All | ANY_ACTIVE | CORRECTION_RECORDED | a booked decision is corrected after the event | Write a correcting decision log entry naming the original, never overwrite it | RESUME_STATE | Case owner | Workbench | same day |
| R-UNI-25 | Universal rules | All | ANY_ACTIVE | PARTNER_NO_RESPONSE | the partner misses the service level on the portal | Chase once, then recall the work and re-select on the scorecard | PARTNER_RECALLED | Partner and agency manager | Partner Portal | per partner type |
| R-UNI-26 | Universal rules | All | ANY_ACTIVE | PARTNER_PANEL_EXIT | the partner leaves the panel or the contract ends | Recall every open case held by that partner and re-select | PARTNER_RECALLED | Partner and agency manager | Partner Portal | 5 working days |
| R-UNI-27 | Universal rules | All | ANY_ACTIVE | PARTNER_CONFLICT_DECLARED | the partner declares a conflict of interest | Withdraw the instruction, re-select the next partner on the scorecard | PARTNER_RECALLED | Partner and agency manager | Partner Portal | 2 working days |
| R-UNI-28 | Universal rules | All | ANY_ACTIVE | PARTNER_INSOLVENT | the partner enters insolvency | Recall the work, secure the documents and any cash held, stop fee payments | PARTNER_RECALLED | Head of the partner type | Partner Portal, Workbench | same day |
| R-UNI-29 | Universal rules | All | ANY_ACTIVE | PARTNER_CONDUCT_BREACH | a conduct or complaint breach is upheld against the partner | Suspend allocation, recall the affected cases, report to the partner review | PARTNER_RECALLED | Partner and agency manager | Partner Portal | same day |
| R-UNI-30 | Universal rules | All | ANY_ACTIVE | SLA_BREACHED | time in the current state exceeds the service level | Raise the breach to the named escalation point. The case does not move | ESCALATED | Team manager | Workbench | per state |
| R-UNI-31 | Universal rules | All | ANY_ACTIVE | PRESCRIPTION_WARNING | prescription_days_remaining reaches the warning threshold | Force a litigation review ahead of every other open action | ROUTE_D6_REOPEN | Litigation officer | Workbench | immediate |
| R-UNI-32 | Universal rules | All | ANY_ACTIVE | AGENT_UNAVAILABLE | the agent or the model does not answer inside the timeout | Fall back to the rule result and continue. Record the fallback on the decision | RESUME_STATE | Workbench | Workbench | 60 seconds |
| R-UNI-33 | Universal rules | All | ANY_ACTIVE | SYSTEM_UNAVAILABLE | a system of record is unavailable | Queue the outbound action and retry on the schedule | RETRY_QUEUE | Platform team | integration adapters | per interface |
| R-UNI-34 | Universal rules | All | ANY_ACTIVE | OUTBOUND_FAILED | an outbound call fails after the retry limit | Move to the exception queue and raise a task for the owner | EXCEPTION_QUEUE | Platform team | integration adapters | per interface |
| R-UNI-35 | Universal rules | All | RETRY_QUEUE | RETRY_SUCCEEDED | the retry completes | Resume the case in the state it paused in | RESUME_STATE | Workbench | integration adapters | None |
| R-UNI-36 | Universal rules | All | RETRY_QUEUE | RETRY_LIMIT_REACHED | retries exhausted | Move to the exception queue | EXCEPTION_QUEUE | Platform team | integration adapters | None |
| R-UNI-37 | Universal rules | All | ANY_ACTIVE | UPSTREAM_DATA_CORRECTED | a segment dimension changes after a correction upstream | Recompute the segment and re-run the gates | ROUTE_D6_REOPEN | Workbench | ALS, EFS, Workbench | 1 working day |
| R-UNI-38 | Universal rules | All | ANY_ACTIVE | RULE_VERSION_EFFECTIVE | a new rule version reaches its effective date | Apply it to decisions taken from that date. Open cases keep the version they were decided under | RESUME_STATE | Center of excellence | Workbench | on the effective date |
| R-UNI-39 | Universal rules | All | ANY_ACTIVE | DECISION_LOG_WRITE_FAILED | the decision log entry cannot be written | Block the action and raise an incident. No action proceeds unlogged | EXCEPTION_QUEUE | Platform team | Workbench | immediate |
| R-UNI-40 | Universal rules | All | ANY_ACTIVE | DUPLICATE_EVENT | the same event arrives twice with the same key | Ignore the second event, record the idempotency hit | RESUME_STATE | Workbench | Workbench | None |
| R-UNI-41 | Universal rules | All | EXCEPTION_QUEUE | MANUAL_DECISION_RECORDED | a person decides and names the missing data | Return the case to the route decision and log the rule gap | ROUTE_D6_REOPEN | Case owner | Workbench | 2 working days |
| R-UNI-42 | Universal rules | All | ESCALATED | ESCALATION_CLOSED | the escalation point acts | Resume the case in the state it was in, record the intervention | RESUME_STATE | Team manager | Workbench | None |
| R-UNI-43 | Universal rules | All | HELD_DEVIATION | DEVIATION_CLEARED | the deviation owner records the outcome | Resume the stage clock and return the case | RESUME_STATE | Deviation owner | Workbench | None |
| R-UNI-44 | Universal rules | All | HELD_CONDUCT | CONTACT_STOP_LIFTED | the conduct officer lifts the stop | Resume contact on the permitted channels | RESUME_STATE | Conduct and QA officer | Workbench | None |
| R-UNI-45 | Universal rules | All | PARTNER_RECALLED | PARTNER_RESELECTED | the next partner is selected on the scorecard | Re-issue the instruction and restart the partner clock | ROUTE_D6_REOPEN | Partner and agency manager | Partner Portal | 2 working days |
| R-UNI-46 | Universal rules | All | REALLOCATED | OWNER_ACCEPTED | the new owner accepts the case | Resume the case in the same state with the same clocks | RESUME_STATE | Case owner | Workbench | 2 working days |
| R-UNI-47 | Universal rules | All | ANY_ACTIVE | ACCOUNT_IN_SOLD_LOT | the account is awarded in a debt sale lot while on another route | Stop every open action, close the case as sold, transfer the data | CASE_CLOSED_SOLD | Debt sale officer | ALS and GL, Workbench | same day |
| R-UNI-48 | Universal rules | All | ANY_ACTIVE | ASSET_PROCEEDS_CLEAR_DEBT | asset proceeds clear the balance in full | Close the case, release any remaining security, refund any surplus per policy | CASE_CLOSED_SOLD | Case owner | ALS and GL, CCMS | 5 working days |
| R-UNI-49 | Universal rules | All | ANY_ACTIVE | GUARANTEE_CLEARS_DEBT | a guarantee payment clears the balance in full | Close the case and record the subrogation position | CASE_CLOSED_SOLD | Guarantee officer | ALS, Workbench | 5 working days |
| R-UNI-50 | Universal rules | All | ANY_ACTIVE | CASE_REOPEN_REQUESTED | a closed case is reopened by an authorized user | Reopen only under the written rule, with a reason and an approver | ROUTE_D6_REOPEN | Head of the owning team | Workbench | 2 working days |

## Sheet: Route sets

| Route sets |  |  |  |  |  |  |  |  |
|---|---|---|---|---|---|---|---|---|
| Ten route sets. Rule and timer counts are calculated from the Rules tab. |  |  |  |  |  |  |  |  |
| Route set | Name | Decision | Rules | With a timer | States | End states | Starts when | Ends when |
| Restructure | Restructure, TDR | D5, D6 |  |  | 18 | 3 | The route decision D6 approves a restructure, or D5 proposes one | Plan runs to term and the case closes; Plan breaks and the case returns to the route decision; Customer does not sign and the case returns to its prior status in COLLINS; A second break bars a further restructure |
| Settlement | Settlement | D6.4 |  |  | 15 | 2 | The route decision D6 approves a settlement | Payment clears, the collateral is released and the case closes; The customer does not pay by the deadline and the case returns to the route decision; A payment reverses after release and the case re-opens |
| Deed in lieu | Deed in lieu and voluntary surrender | D6.4 |  |  | 20 | 2 | The route decision D6 approves a deed in lieu, or the customer offers the asset during a negotiation | The asset is on the books and hands off to the disposal route; The customer rents the asset back and the rental runs; The customer withdraws or the title is not clean and the case returns to the route decision |
| Guarantee claim | Guarantee claim, D6.5 and D6.6 | D6.5, D6.6 |  |  | 17 | 2 | A guarantee is detected on the case at takeover and the claim deadline timer starts | The claim is paid and the residual returns to the route decision; The claim is lost on the deadline and the full balance returns to the route decision; The guarantor settles and the case closes |
| Litigation | Litigation and enforcement, D7 | D7 |  |  | 38 | 4 | The route decision D6.3 approves litigation, or a broken treatment returns the case to the legal route | Debt satisfied and the case closes; Asset taken onto the books and handed to the disposal route; Judgment unenforceable or enforcement exhausted, and the case goes to write-off; Customer cures or settles, and the case returns to treatment |
| Asset disposal | Asset disposal, D8.1 to D8.3 | D8.1 to D8.3 |  |  | 40 | 4 | An asset is taken onto the bank's books and the holding age clock starts | Sold, proceeds applied and the case closed with no shortfall; Sold with a residual, handed to debt sale or write-off; Transferred to RAMC or the joint venture; Rented, with the asset still held |
| Debt sale | Debt sale, D8.4 | D8.4 |  |  | 29 | 2 | The monthly debt sale cycle opens, or a residual arrives from the disposal route | Lot awarded, settled, transferred and closed with realized recovery recorded; Lot withdrawn and the accounts returned to the case list; Put-back upheld and the account returned to the bank |
| Write-off | Write off and recover after charge-off, D9 | D9 |  |  | 27 | 2 | The monthly eligibility scan runs on the cut-off date, or a residual arrives from another route | Posted, placed, recovered and closed after the retention period; Rejected by the committee and returned to the pursue track; Sold to a buyer as a charged-off population |
| Deviations | Deviations X1 to X7 | X1 to X7 |  |  | 9 | 3 | The screening agent flags a deviation at entry or on a new document | The deviation clears and the case returns to the state it paused in; The deviation moves the case to a different route; The case ends, where insurance settles the debt |
| Universal rules | Universal rules, any state | All |  |  | 15 | 6 | The case is in any active state on any route | The case returns to the state it was in; The case moves to the route decision; The case closes; The case is canceled or merged |
| Total |  |  |  |  |  |  |  |  |

## Sheet: States

| States |  |  |  |  |  |  |
|---|---|---|---|---|---|---|
| 228 states across the route sets, with the rules into and out of each. |  |  |  |  |  |  |
| State | Route set | Kind | Label | Meaning | Rules in | Rules out |
| ROUTE_APPROVED_RESTRUCTURE | Restructure | Start | Route approved | D6 sets route R1 | 0 | 1 |
| PROPOSED_IN_COLLINS | Restructure | System step | Proposed in COLLINS | Model returns the plan shape | 1 | 2 |
| IN_FCR_QUEUE | Restructure | Officer step | In the FCR queue | Routed through EFS | 2 | 2 |
| WITH_FCR_OFFICER | Restructure | Officer step | With the FCR officer | Restructuring officer builds the offer | 3 | 4 |
| AFFORDABILITY_IN_ACE | Restructure | System step | Affordability in ACE | Plan calculated | 1 | 2 |
| AWAITING_CREDIT_APPROVAL | Restructure | Officer step | Awaiting credit approval | Outside the range or a deviation | 2 | 3 |
| DECLINED_BY_CREDIT | Restructure | Exception | Declined by credit | Reason recorded | 1 | 1 |
| OFFER_WITH_CUSTOMER | Restructure | Customer step | Offer with the customer | A wait with a validity timer | 3 | 5 |
| RETURNED_TO_COLLINS | Restructure | Exception | Returned to COLLINS | Prior status restored | 2 | 1 |
| WITH_OPS_BOOKING | Restructure | Officer step | With operations | Booking to ALS and NLEADS | 4 | 4 |
| BOOKED_IN_ALS_NLEADS | Restructure | System step | Booked | Schedule and timers set | 1 | 1 |
| PLAN_RUNNING | Restructure | System step | Plan running | Payments matched to installments | 4 | 4 |
| PLAN_CURE_PERIOD | Restructure | Exception | In the cure period | An installment was missed | 1 | 2 |
| PLAN_BROKEN | Restructure | Exception | Plan broken | Break count incremented | 1 | 3 |
| PLAN_COMPLETED | Restructure | End state | Plan completed | Collateral released, case closed | 1 | 0 |
| BACK_TO_ROUTE_DECISION | Restructure | End state | Back to the route decision | With a coded reason | 7 | 0 |
| RESTRUCTURE_BARRED | Restructure | End state | Restructure barred | R1 removed from the open routes | 1 | 1 |
| UNMATCHED_EXCEPTION | Restructure | Exception | UNMATCHED_EXCEPTION | No rule matched. Held for a person. | 2 | 1 |
| ROUTE_APPROVED_SETTLEMENT | Settlement | Start | Route approved | D6 sets route R2 | 0 | 1 |
| PAYOFF_AND_RANGE_SET | Settlement | System step | Payoff and range set | From ALS and reference data | 2 | 2 |
| WITH_FCR_OFFICER_SET | Settlement | Officer step | With the FCR officer | Negotiates inside the range | 2 | 3 |
| AWAITING_APPROVAL_SET | Settlement | Officer step | Awaiting approval | Amount below the floor | 1 | 2 |
| DECLINED_BY_APPROVER_SET | Settlement | Exception | Approval refused | Reason recorded | 1 | 1 |
| OFFER_WITH_CUSTOMER_SET | Settlement | Customer step | Offer with the customer | A wait with a validity timer | 3 | 4 |
| WITH_OPS_SETTLEMENT | Settlement | Officer step | With operations | Agreement booked in ALS | 1 | 1 |
| AWAITING_PAYMENT | Settlement | Customer step | Awaiting payment | Lump sum or installments | 2 | 5 |
| PAYMENT_PART_RECEIVED | Settlement | Exception | Part received | Balance still due | 1 | 2 |
| PAYMENT_CLEARED | Settlement | System step | Payment cleared | Matched and posted | 2 | 1 |
| COLLATERAL_RELEASE_REQUESTED | Settlement | System step | Release requested | Account closed in ALS | 2 | 2 |
| PAYMENT_REVERSED | Settlement | Exception | Payment reversed | After release | 1 | 1 |
| CASE_CLOSED_SETTLED | Settlement | End state | Case closed | Title returned | 1 | 1 |
| RETURNED_TO_ROUTE_SET | Settlement | End state | Back to the route decision | With a coded reason | 6 | 0 |
| UNMATCHED_EXCEPTION | Settlement | Exception | UNMATCHED_EXCEPTION | No rule matched. Held for a person. | 2 | 1 |
| ROUTE_APPROVED_DIL | Deed in lieu | Start | Route approved | D6 sets route R3 | 0 | 1 |
| EARLY_READINESS_CHECK | Deed in lieu | System step | Early readiness check | Lead ranked, encumbrance tested | 1 | 3 |
| ENCUMBRANCE_BLOCKED | Deed in lieu | Exception | Encumbrance unresolved | Transfer blocked | 1 | 2 |
| VALUATION_ORDERED | Deed in lieu | System step | Valuation ordered | Fast lane or preliminary model | 3 | 2 |
| AWAITING_VALUER | Deed in lieu | Partner step | Awaiting the valuer | Panel valuer through SVAF | 2 | 3 |
| VALUATION_ACCEPTED | Deed in lieu | System step | Valuation accepted | Outliers flagged and cleared | 3 | 1 |
| WITH_FCR_OFFICER_DIL | Deed in lieu | Officer step | With the FCR officer | Negotiates the transfer | 1 | 1 |
| TRANSFER_PRICE_SET | Deed in lieu | System step | Transfer price set | Governed template applied | 1 | 2 |
| AWAITING_SECOND_SIGNATURE | Deed in lieu | Officer step | Awaiting second signature | Price below the floor | 1 | 2 |
| OFFER_WITH_CUSTOMER_DIL | Deed in lieu | Customer step | Offer with the customer | Wet ink for mortgage per Legal | 2 | 5 |
| WITH_FIELD_INSPECTION | Deed in lieu | Officer step | Field inspection | Checklist, photographs, bills | 2 | 1 |
| ASSET_UNLOCK_DECISION | Deed in lieu | Decision point | Asset unlock rule | About 95% auto-unlock | 1 | 2 |
| AWAITING_APPROVER_SUMMARY | Deed in lieu | Officer step | Approver summary | The rest go to the approver | 1 | 2 |
| AWAITING_TRANSFER | Deed in lieu | Partner step | Awaiting transfer | Land Office or SCIS | 3 | 4 |
| TITLE_NOT_CLEAN | Deed in lieu | Exception | Title not clean | Transfer held | 1 | 2 |
| ASSET_ON_BOOKS | Deed in lieu | System step | Asset on the books | AMIS recorded, debt settled | 2 | 2 |
| RENTAL_RUNNING | Deed in lieu | System step | Rental running | Auto-debit through ATS | 1 | 1 |
| HANDED_TO_DISPOSAL | Deed in lieu | End state | Handed to disposal | Route R5 takes the asset | 2 | 0 |
| RETURNED_TO_ROUTE_DIL | Deed in lieu | End state | Back to the route decision | With a coded reason | 7 | 0 |
| UNMATCHED_EXCEPTION | Deed in lieu | Exception | UNMATCHED_EXCEPTION | No rule matched. Held for a person. | 2 | 1 |
| GUARANTEE_DETECTED | Guarantee claim | Start | Guarantee detected | Found on the case at takeover in stage 06 | 0 | 2 |
| NOT_ELIGIBLE | Guarantee claim | Exception | Not eligible | Scheme default conditions not met | 1 | 1 |
| DEADLINE_TIMER_RUNNING | Guarantee claim | System step | Claim deadline running | Timer set from the date the default conditions are met | 2 | 3 |
| CLAIM_PREPARATION | Guarantee claim | System step | Claim assembled | Claim preparation agent builds it against the scheme checklist | 4 | 3 |
| CLAIM_DEFECT_HOLD | Guarantee claim | Exception | Claim held on a defect | A checklist item is missing | 1 | 2 |
| CLAIM_APPROVAL | Guarantee claim | Officer step | Officer approves the claim | Guarantee officer verifies at D6.5 | 2 | 2 |
| CLAIM_SUBMITTED | Guarantee claim | Partner step | Claim submitted | Through the TCG claim channel | 3 | 4 |
| GUARANTOR_NOTICE | Guarantee claim | Customer step | Guarantor noticed | D6.6 notice with proof of delivery | 2 | 3 |
| TCG_QUERY | Guarantee claim | Exception | TCG query | More information requested before assessment | 1 | 2 |
| CLAIM_REJECTED | Guarantee claim | Exception | Claim rejected | Rejection reason recorded against the guarantee | 2 | 2 |
| CLAIM_PART_PAID | Guarantee claim | System step | Part paid | Payment matched with source TCG | 1 | 2 |
| CLAIM_PAID | Guarantee claim | System step | Paid to the guaranteed share | Relief schemes cover up to 50 percent of principal | 1 | 1 |
| GUARANTOR_DISPUTE_HOLD | Guarantee claim | Exception | Guarantor dispute | X1 raised against the guarantee itself | 1 | 2 |
| DEADLINE_MISSED | Guarantee claim | Exception | Claim deadline missed | The claim is lost. Loss, reason and amount recorded | 2 | 1 |
| SUBROGATION_POSITION | Guarantee claim | System step | Subrogation recorded | TCG holds a share of every later recovery | 2 | 2 |
| RESIDUAL_TO_ROUTE | Guarantee claim | End state | Residual to another route | Balance returns to the route decision at D6 | 5 | 0 |
| GUARANTEE_CLOSED | Guarantee claim | End state | Guarantee closed | No further claim on this guarantee | 2 | 0 |
| LIT_ROUTE_APPROVED | Litigation | Start | Litigation approved | D6.3, or a broken treatment returns the case | 0 | 2 |
| DEVIATION_HOLD | Litigation | Exception | Deviation hold | X1 to X7. Timers pause, prescription keeps running | 2 | 6 |
| NOTICE_GENERATED | Litigation | System step | Notice generated | The rules pick the Legal template by product and notice type | 3 | 3 |
| NOTICE_BLOCKED | Litigation | Exception | Notice blocked | Template withdrawn, or a contact stop applies | 3 | 1 |
| NOTICE_DISPATCHED | Litigation | System step | Notice dispatched | WIN and DMS print, courier and capture proof | 2 | 3 |
| WITH_CUSTOMER_NOTICE_PERIOD | Litigation | Customer step | Notice period running | Timer runs from proof of delivery, not the print date | 1 | 4 |
| NOTICE_UNSERVED | Litigation | Exception | Notice unserved | No proof returned, refused or undeliverable | 2 | 2 |
| PACK_ASSEMBLY | Litigation | System step | Pack assembled | Legal document agent builds from case, CCMS, LHS and the Workbench document hub | 5 | 2 |
| PACK_DEFECT_HOLD | Litigation | Exception | Pack held on a defect | An item on the defect list is missing | 1 | 3 |
| PACK_VERIFIED | Litigation | Officer step | Pack verified | Litigation officer approves filing, first-time-right recorded | 3 | 3 |
| FIRM_SELECTION | Litigation | Decision point | Firm selected by rule | Panel scorecard by court region and case type, conflict check | 1 | 2 |
| FIRM_ESCALATED | Litigation | Officer step | No firm available | Head of Litigation nominates or widens the panel | 1 | 1 |
| FIRM_INSTRUCTED | Litigation | Partner step | Firm instructed | Instruction and pack through the Partner Portal | 3 | 3 |
| FIRM_DECLINED | Litigation | Exception | Firm declined or breached | Re-select the next firm on the scorecard | 2 | 1 |
| FILED_IN_COURT | Litigation | Partner step | Filed in court | Firm uploads the receipt and the court case number | 1 | 2 |
| FILING_REJECTED | Litigation | Exception | Court rejected the filing | Defect recorded, pack reworked | 1 | 1 |
| IN_HEARING | Litigation | Partner step | In hearing | Case tracking agent holds the calendar and the timers | 8 | 6 |
| HEARING_ADJOURNED | Litigation | Exception | Hearing adjourned | Timer reset, postpone reason coded | 1 | 1 |
| SETTLEMENT_OFFERED_AT_COURT | Litigation | Decision point | Settlement offered | D7.4. Agent proposes, approver decides | 1 | 2 |
| LITIGATION_HELD | Litigation | System step | Litigation held | Case not withdrawn while the treatment runs | 1 | 2 |
| JUDGMENT_RECORDED | Litigation | System step | Judgment recorded | Date and amount written to the Legal Action | 1 | 2 |
| JUDGMENT_DISMISSED | Litigation | Exception | Dismissed or lost | Appeal window opens | 1 | 1 |
| APPEAL_DECISION | Litigation | Decision point | Appeal decision | D7.4. Approver inside the limit, Head of Litigation above it | 1 | 2 |
| APPEAL_FILED | Litigation | Partner step | Appeal filed | Firm files, hearing timers reset | 1 | 1 |
| LEGAL_SPEND_APPROVAL | Litigation | Decision point | Legal spend approval | D7.4. Court fees and legal expenses | 1 | 2 |
| ASSET_TRACE | Litigation | System step | Assets traced | NCB, internal data, registries and insurers | 1 | 2 |
| ENFORCEMENT_DECISION | Litigation | Decision point | Enforce or defer | D7.5. Enforcement owner decides, a deferral needs a code | 5 | 3 |
| DEFERRAL_RECORDED | Litigation | Exception | Deferral recorded | Coded reason and a review date re-queue the case | 1 | 2 |
| WRIT_AND_SEIZURE | Litigation | Partner step | Writ and seizure | Firm applies, the LED executes | 1 | 2 |
| LED_AUCTION | Litigation | Partner step | LED auction | Rounds at 100, 90, 80 then 70 percent of official value | 2 | 3 |
| NO_BID_AT_70 | Litigation | Exception | No bid at 70 percent | The ladder is exhausted | 1 | 2 |
| PROCEEDS_MATCHED | Litigation | System step | Proceeds matched | Reconciliation agent posts to ALS against the case | 3 | 3 |
| BANKRUPTCY_PETITION | Litigation | Decision point | Bankruptcy petition | D7.5. Agent prepares, the approver approves | 1 | 2 |
| OFFICIAL_RECEIVER_CLAIM | Litigation | Partner step | Claim with the official receiver | Filed before the receiver deadline | 2 | 2 |
| TO_TREATMENT | Litigation | End state | Back to treatment | Litigation canceled or held while the plan runs | 3 | 0 |
| TO_ASSET_DISPOSAL | Litigation | End state | To asset disposal | Asset onto the bank books after no bid | 1 | 0 |
| TO_WRITE_OFF | Litigation | End state | To write off | Unenforceable, or enforcement exhausted | 6 | 0 |
| CASE_CLOSED | Litigation | End state | Case closed | Debt satisfied, record retained after close | 5 | 0 |
| ASSET_PENDING_TAKE_ON | Asset disposal | Start | Asset pending take-on | ASSET_PENDING_TAKE_ON | 1 | 4 |
| FAILED_NOTICE_QUEUE | Asset disposal | Exception | Failed notice queue | FAILED_NOTICE_QUEUE | 1 | 1 |
| ASSET_ON_BOOKS | Asset disposal | System step | Asset record created | ASSET_ON_BOOKS | 3 | 2 |
| TITLE_BLOCKED | Asset disposal | Exception | Title or registration blocked | TITLE_BLOCKED | 2 | 1 |
| ASSET_HELD | Asset disposal | Officer step | Asset held | ASSET_HELD | 11 | 6 |
| WORK_ORDER_OPEN | Asset disposal | Partner step | Work order with the vendor | WORK_ORDER_OPEN | 2 | 2 |
| EVICTION_REQUIRED | Asset disposal | Officer step | Eviction instructed | EVICTION_REQUIRED | 1 | 1 |
| REAPPRAISAL_ORDERED | Asset disposal | Partner step | Re-appraisal ordered | REAPPRAISAL_ORDERED | 2 | 1 |
| REAPPRAISAL_RECEIVED | Asset disposal | System step | Value reported | REAPPRAISAL_RECEIVED | 1 | 2 |
| DISPOSAL_PAUSED_DEVIATION | Asset disposal | Exception | Paused on a deviation | DISPOSAL_PAUSED_DEVIATION | 2 | 2 |
| ROUTE_RECOMMENDED | Asset disposal | System step | Disposal route recommended | ROUTE_RECOMMENDED | 3 | 1 |
| ROUTE_WITH_APPROVER | Asset disposal | Decision point | With the approver | ROUTE_WITH_APPROVER | 1 | 8 |
| ROUTE_APPROVED_AUCTION | Asset disposal | System step | Auction route approved | ROUTE_APPROVED_AUCTION | 2 | 1 |
| ROUTE_APPROVED_RAMC | Asset disposal | System step | RAMC route approved | ROUTE_APPROVED_RAMC | 1 | 1 |
| ROUTE_APPROVED_BUYBACK | Asset disposal | System step | Buy-back route approved | ROUTE_APPROVED_BUYBACK | 1 | 2 |
| RENTAL_ACTIVE | Asset disposal | System step | Asset rented | RENTAL_ACTIVE | 1 | 1 |
| BROKER_INSTRUCTED | Asset disposal | Partner step | Broker instructed | BROKER_INSTRUCTED | 1 | 2 |
| PRICE_PROPOSED | Asset disposal | System step | Opening and floor price proposed | PRICE_PROPOSED | 1 | 1 |
| FLOOR_APPROVED | Asset disposal | Decision point | Floor approved | FLOOR_APPROVED | 1 | 3 |
| LISTING_BLOCKED | Asset disposal | Exception | Listing blocked on evidence | LISTING_BLOCKED | 1 | 1 |
| VENDOR_ALLOCATED | Asset disposal | Partner step | Vendor allocated on the scorecard | VENDOR_ALLOCATED | 2 | 2 |
| LISTING_LIVE | Asset disposal | System step | Listing live | LISTING_LIVE | 3 | 2 |
| ROUND_OPEN | Asset disposal | System step | Round open at the price step | ROUND_OPEN | 3 | 3 |
| BID_RECEIVED | Asset disposal | System step | Bid received | BID_RECEIVED | 1 | 2 |
| SECOND_SIGNATURE_PENDING | Asset disposal | Decision point | Second signature pending | SECOND_SIGNATURE_PENDING | 1 | 2 |
| NO_BID_AT_FLOOR | Asset disposal | Exception | Floor reached with no bid | NO_BID_AT_FLOOR | 1 | 2 |
| RELISTED | Asset disposal | System step | Re-listed | RELISTED | 2 | 1 |
| SALE_AGREED | Asset disposal | System step | Sale agreed | SALE_AGREED | 4 | 1 |
| AWAITING_PAYMENT | Asset disposal | Partner step | Awaiting payment, five days | AWAITING_PAYMENT | 1 | 2 |
| AWARD_CANCELED | Asset disposal | Exception | Award canceled | AWARD_CANCELED | 1 | 1 |
| TITLE_TRANSFER_PENDING | Asset disposal | System step | Title transfer pending | TITLE_TRANSFER_PENDING | 1 | 3 |
| ASSET_SOLD | Asset disposal | System step | Asset sold and transferred | ASSET_SOLD | 2 | 1 |
| RAMC_TRANSFER_PENDING | Asset disposal | Partner step | RAMC transfer pending | RAMC_TRANSFER_PENDING | 1 | 1 |
| PROCEEDS_APPLIED | Asset disposal | System step | Proceeds applied to the case | PROCEEDS_APPLIED | 1 | 2 |
| SHORTFALL_RAISED | Asset disposal | System step | Shortfall raised | SHORTFALL_RAISED | 1 | 3 |
| ASSET_TRANSFERRED | Asset disposal | End state | Transferred to RAMC | ASSET_TRANSFERRED | 1 | 0 |
| CASE_CLOSED_NO_SHORTFALL | Asset disposal | End state | Case closed, no shortfall | CASE_CLOSED_NO_SHORTFALL | 1 | 0 |
| TO_DEBT_SALE | Asset disposal | End state | To the debt sale route | TO_DEBT_SALE | 2 | 0 |
| TO_WRITEOFF | Asset disposal | End state | To the write-off route | TO_WRITEOFF | 2 | 0 |
| UNMATCHED_EXCEPTION | Asset disposal | Exception | UNMATCHED_EXCEPTION | No rule matched. Held for a person. | 2 | 1 |
| LOT_CANDIDATE_SELECTED | Debt sale | Start | Candidate accounts selected | LOT_CANDIDATE_SELECTED | 0 | 2 |
| CASE_EXCLUDED | Debt sale | Exception | Account excluded | CASE_EXCLUDED | 1 | 1 |
| LOT_BUILT | Debt sale | System step | Lot built and priced | LOT_BUILT | 2 | 2 |
| LOT_WITH_COMMITTEE | Debt sale | Decision point | Lot with the committee | LOT_WITH_COMMITTEE | 2 | 3 |
| LOT_APPROVED | Debt sale | System step | Lot, reserve and terms approved | LOT_APPROVED | 1 | 1 |
| LOT_WITHDRAWN | Debt sale | Exception | Lot withdrawn | LOT_WITHDRAWN | 2 | 1 |
| TAPE_PREPARED | Debt sale | System step | Masked data tape prepared | TAPE_PREPARED | 2 | 2 |
| TAPE_REJECTED | Debt sale | Exception | Tape rejected on masking | TAPE_REJECTED | 1 | 1 |
| DATA_ROOM_OPEN | Debt sale | System step | Data room open | DATA_ROOM_OPEN | 1 | 1 |
| BUYER_PENDING_KYC | Debt sale | Decision point | Buyer pending KYC | BUYER_PENDING_KYC | 2 | 2 |
| BUYER_CLEARED | Debt sale | Partner step | Buyer cleared | BUYER_CLEARED | 1 | 1 |
| BUYER_REJECTED | Debt sale | Exception | Buyer refused | BUYER_REJECTED | 1 | 2 |
| BIDDING_OPEN | Debt sale | Partner step | Bidding open | BIDDING_OPEN | 3 | 1 |
| BIDS_RECEIVED | Debt sale | System step | Bids received | BIDS_RECEIVED | 1 | 2 |
| BID_BELOW_RESERVE | Debt sale | Exception | Best bid below the reserve | BID_BELOW_RESERVE | 1 | 2 |
| AWARD_PENDING | Debt sale | Decision point | Award pending confirmation | AWARD_PENDING | 1 | 1 |
| LOT_AWARDED | Debt sale | System step | Lot awarded | LOT_AWARDED | 1 | 1 |
| SETTLEMENT_PENDING | Debt sale | Partner step | Settlement pending | SETTLEMENT_PENDING | 1 | 3 |
| AWARD_CANCELED_DS | Debt sale | Exception | Award canceled | AWARD_CANCELED_DS | 2 | 1 |
| SETTLED | Debt sale | System step | Buyer settled | SETTLED | 1 | 1 |
| DATA_TRANSFERRED | Debt sale | System step | Account data transferred | DATA_TRANSFERRED | 1 | 1 |
| DERECOGNISED | Debt sale | System step | Balance derecognised | DERECOGNISED | 1 | 2 |
| GL_POSTED | Debt sale | System step | Posted to the general ledger | GL_POSTED | 2 | 2 |
| POSTING_REJECTED_DS | Debt sale | Exception | Posting rejected | POSTING_REJECTED_DS | 1 | 1 |
| PUTBACK_RAISED | Debt sale | Partner step | Put-back claim raised | PUTBACK_RAISED | 1 | 2 |
| PUTBACK_UPHELD | Debt sale | System step | Put-back upheld | PUTBACK_UPHELD | 1 | 1 |
| PUTBACK_REFUSED | Debt sale | System step | Put-back refused | PUTBACK_REFUSED | 1 | 1 |
| LOT_CLOSED | Debt sale | End state | Lot closed | LOT_CLOSED | 2 | 0 |
| BACK_TO_CASE_LIST | Debt sale | End state | Accounts back on the case list | BACK_TO_CASE_LIST | 4 | 0 |
| SCAN_DUE | Write-off | Start | Monthly scan due | SCAN_DUE | 4 | 3 |
| SCAN_HELD | Write-off | Exception | Scan held | SCAN_HELD | 2 | 1 |
| POPULATION_PROPOSED | Write-off | System step | Population proposed | POPULATION_PROPOSED | 1 | 3 |
| CASE_REMOVED_BY_TEAM | Write-off | Exception | Case removed with a reason | CASE_REMOVED_BY_TEAM | 2 | 1 |
| PACK_PREPARED | Write-off | System step | Write-off pack prepared | PACK_PREPARED | 1 | 3 |
| PACK_INCOMPLETE | Write-off | Exception | Pack incomplete | PACK_INCOMPLETE | 1 | 1 |
| WITH_COMMITTEE | Write-off | Decision point | With the write-off committee | WITH_COMMITTEE | 4 | 4 |
| ESCALATED_TO_CREDIT_COMMITTEE | Write-off | Decision point | Above the limit, credit committee | ESCALATED_TO_CREDIT_COMMITTEE | 1 | 2 |
| APPROVED | Write-off | System step | Approved | APPROVED | 2 | 1 |
| DEFERRED | Write-off | Exception | Deferred with a review date | DEFERRED | 1 | 1 |
| RETURNED_TO_PURSUE | Write-off | End state | Returned to the pursue track | RETURNED_TO_PURSUE | 2 | 0 |
| POSTING_PENDING | Write-off | System step | Posting pending | POSTING_PENDING | 3 | 2 |
| POSTED | Write-off | System step | Posted to ALS and the GL | POSTED | 1 | 3 |
| POSTING_REJECTED | Write-off | Exception | Posting rejected | POSTING_REJECTED | 1 | 2 |
| PROVISION_RELEASED | Write-off | System step | Provision released | PROVISION_RELEASED | 1 | 1 |
| FINANCE_FEED_SENT | Write-off | System step | Finance feed sent | FINANCE_FEED_SENT | 2 | 2 |
| FINANCE_FEED_REJECTED | Write-off | Exception | Finance feed rejected | FINANCE_FEED_REJECTED | 1 | 1 |
| PLACEMENT_DECIDED | Write-off | Decision point | Post charge-off treatment decided | PLACEMENT_DECIDED | 2 | 3 |
| PLACED_WITH_AGENCY | Write-off | Partner step | Placed with an agency | PLACED_WITH_AGENCY | 3 | 5 |
| SOLD_POST_CHARGEOFF | Write-off | Partner step | Sold to a buyer | SOLD_POST_CHARGEOFF | 1 | 2 |
| PLACEMENT_RECALLED | Write-off | Exception | Placement recalled | PLACEMENT_RECALLED | 1 | 1 |
| PAYMENT_MATCHED | Write-off | System step | Payment matched and posted | PAYMENT_MATCHED | 3 | 1 |
| PAYMENT_EXCEPTION | Write-off | Exception | Payment on the exception list | PAYMENT_EXCEPTION | 1 | 1 |
| REMITTED_TO_BUYER | Write-off | System step | Remitted to the buyer | REMITTED_TO_BUYER | 1 | 1 |
| RETENTION_RUNNING | Write-off | System step | Retention timer running | RETENTION_RUNNING | 3 | 2 |
| CASE_CLOSED | Write-off | End state | Case closed | CASE_CLOSED | 3 | 1 |
| WRITEOFF_EXCEPTION | Write-off | Exception | Write-off exception, owner to confirm | WRITEOFF_EXCEPTION | 3 | 3 |
| ANY_STATE | Deviations | Start | Any active state | The case is on a route | 0 | 1 |
| DEV_FLAGGED | Deviations | System step | DEV_FLAGGED | Screening agent flags with reasons | 1 | 7 |
| DEV_WITH_OWNER | Deviations | Officer step | DEV_WITH_OWNER | Complaint officer, specialist, fraud team or Legal | 7 | 11 |
| DEV_REJECTED | Deviations | System step | DEV_REJECTED | Owner clears the flag as not a deviation | 1 | 1 |
| DEV_RESOLVED | Deviations | System step | DEV_RESOLVED | Outcome recorded, clock resumes | 2 | 1 |
| DEV_REROUTE | Deviations | Decision point | DEV_REROUTE | The outcome changes the route | 7 | 1 |
| RESUMED | Deviations | End state | RESUMED | Back to the paused state | 2 | 0 |
| ROUTE_D6 | Deviations | End state | ROUTE_D6 | Back to the route decision | 1 | 0 |
| CASE_ENDED | Deviations | End state | CASE_ENDED | Insurance settles the debt | 1 | 0 |
| ANY_ACTIVE | Universal rules | Start | ANY_ACTIVE | Any non-terminal state on any route | 0 | 41 |
| HELD_DEVIATION | Universal rules | System step | HELD_DEVIATION | Stage clock paused, deviation owner holds it | 6 | 1 |
| HELD_LEGAL | Universal rules | System step | HELD_LEGAL | Regulatory or legal freeze, no action out | 3 | 1 |
| HELD_CONDUCT | Universal rules | System step | HELD_CONDUCT | Contact stop applied | 1 | 1 |
| EXCEPTION_QUEUE | Universal rules | Exception | EXCEPTION_QUEUE | A person decides, the gap is logged | 4 | 1 |
| RETRY_QUEUE | Universal rules | Exception | RETRY_QUEUE | Automatic retry, then the exception queue | 1 | 2 |
| ESCALATED | Universal rules | Officer step | ESCALATED | Named escalation point, case does not move | 2 | 1 |
| REALLOCATED | Universal rules | Officer step | REALLOCATED | New owner, same state | 2 | 1 |
| PARTNER_RECALLED | Universal rules | System step | PARTNER_RECALLED | Work pulled back, partner re-selected | 5 | 1 |
| RESUME_STATE | Universal rules | End state | RESUME_STATE | Back to the state it paused in | 12 | 0 |
| ROUTE_D6_REOPEN | Universal rules | End state | ROUTE_D6_REOPEN | Segment recomputed, gates re-run | 8 | 0 |
| CASE_CURED_CLOSED | Universal rules | End state | CASE_CURED_CLOSED | Arrears cleared, case leaves recovery | 1 | 0 |
| CASE_CLOSED_SOLD | Universal rules | End state | CASE_CLOSED_SOLD | Debt sold or asset cleared the balance | 3 | 0 |
| CANCELED_IN_ERROR | Universal rules | End state | CANCELED_IN_ERROR | Case should never have existed | 1 | 0 |
| MERGED | Universal rules | End state | MERGED | Folded into the surviving case | 1 | 0 |

## Sheet: Events

| Events |  |  |
|---|---|---|
| 377 distinct events, ordered by the number of rules that listen for each. |  |  |
| Event | Rules | Route sets |
| ROUTE_APPROVED | 11 | Restructure, Settlement, Deed in lieu, Litigation, Asset disposal |
| PAYMENT_RECEIVED | 8 | Restructure, Settlement, Asset disposal, Universal rules |
| DEVIATION_RAISED | 6 | Restructure, Settlement, Litigation, Asset disposal |
| OFFER_PREPARED | 6 | Restructure, Settlement |
| OWNER_ASSIGNED | 6 | Deviations |
| MANUAL_DECISION_RECORDED | 5 | Restructure, Settlement, Deed in lieu, Asset disposal, Universal rules |
| TRANSFER_COMPLETED | 4 | Deed in lieu, Asset disposal |
| BREAK_RECORDED | 3 | Restructure |
| CLAIM_DEADLINE_MISSED | 3 | Guarantee claim, Litigation |
| CUSTOMER_ACCEPTED | 3 | Deed in lieu |
| DEVIATION_RESOLVED | 3 | Deviations |
| OFFER_EXPIRED | 3 | Restructure, Settlement, Deed in lieu |
| PRESCRIPTION_WARNING | 3 | Litigation, Universal rules |
| RESIDUAL_ROUTED | 3 | Asset disposal |
| BALANCE_SATISFIED | 2 | Guarantee claim, Litigation |
| CLOCK_RESUMED | 2 | Deviations |
| CUSTOMER_COUNTER_OFFERED | 2 | Restructure, Settlement |
| CUSTOMER_SIGNED | 2 | Restructure, Settlement |
| DECLINE_RECORDED | 2 | Restructure, Settlement |
| DEVIATION_CLEARED | 2 | Asset disposal, Universal rules |
| HOLD_EXPIRED | 2 | Deed in lieu |
| PAYMENT_RECEIVED_AFTER_CHARGEOFF | 2 | Write-off |
| RETRY_LIMIT_REACHED | 2 | Write-off, Universal rules |
| REVIEW_DATE_REACHED | 2 | Litigation, Write-off |
| SECOND_SIGNATURE_GIVEN | 2 | Deed in lieu, Asset disposal |
| SECOND_SIGNATURE_REFUSED | 2 | Deed in lieu, Asset disposal |
| SLA_BREACHED | 2 | Deviations, Universal rules |
| SUBROGATION_DUE | 2 | Guarantee claim |
| TITLE_CLEARED | 2 | Deed in lieu, Asset disposal |
| VALUE_ACCEPTED | 2 | Deed in lieu, Asset disposal |
| X1_RESOLVED | 2 | Guarantee claim, Litigation |
| X1_UPHELD | 2 | Guarantee claim, Litigation |
| ACCESS_REFUSED | 1 | Deed in lieu |
| ACCOUNTS_RETURNED | 1 | Debt sale |
| ACCOUNT_EXCLUDED | 1 | Debt sale |
| ACCOUNT_IN_SOLD_LOT | 1 | Universal rules |
| ACCOUNT_RETURNED | 1 | Debt sale |
| AFFORDABILITY_FAILED | 1 | Restructure |
| AFFORDABILITY_PASSED | 1 | Restructure |
| AFFORDABILITY_REQUIRED | 1 | Restructure |
| AGENCY_REPORTED_RESULT | 1 | Write-off |
| AGENCY_UNDERPERFORMS | 1 | Write-off |
| AGENT_UNAVAILABLE | 1 | Universal rules |
| ALS_LOAD_FAILED | 1 | Write-off |
| ALS_POSTING_CONFIRMED | 1 | Write-off |
| ALS_POSTING_REJECTED | 1 | Write-off |
| ALTERNATE_SERVICE_ORDERED | 1 | Litigation |
| APPEAL_APPROVED | 1 | Litigation |
| APPEAL_DECLINED | 1 | Litigation |
| APPEAL_HEARING_SET | 1 | Litigation |
| APPEAL_WINDOW_OPEN | 1 | Litigation |
| APPROVAL_GRANTED | 1 | Settlement |
| APPROVAL_REFUSED | 1 | Settlement |
| APPROVAL_SLA_BREACHED | 1 | Restructure |
| APPROVER_REFUSED | 1 | Deed in lieu |
| APPROVER_RELEASED | 1 | Deed in lieu |
| ASSETS_FOUND | 1 | Litigation |
| ASSET_PROCEEDS_CLEAR_DEBT | 1 | Universal rules |
| ASSET_RECORD_CONFIRMED | 1 | Asset disposal |
| ASSET_RETURNED_UNSOLD | 1 | Litigation |
| ASSET_TAKEN_ON_BOOK | 1 | Litigation |
| AUTO_UNLOCK_FAILED | 1 | Deed in lieu |
| AUTO_UNLOCK_PASSED | 1 | Deed in lieu |
| AWARD_CONFIRMED | 1 | Debt sale |
| AWARD_MADE | 1 | Asset disposal |
| BALANCE_CLAIMED | 1 | Guarantee claim |
| BANKRUPTCY_CONFIRMED | 1 | Asset disposal |
| BANKRUPTCY_FILED | 1 | Deviations |
| BANKRUPTCY_NOTIFIED | 1 | Universal rules |
| BAR_APPLIED | 1 | Restructure |
| BEST_BID_BELOW_RESERVE | 1 | Debt sale |
| BIDDING_WINDOW_CLOSED | 1 | Debt sale |
| BIDDING_WINDOW_OPENED | 1 | Debt sale |
| BID_AT_OR_ABOVE_FLOOR | 1 | Asset disposal |
| BID_BELOW_FLOOR | 1 | Asset disposal |
| BID_PLACED | 1 | Asset disposal |
| BID_SUBMITTED | 1 | Debt sale |
| BOOKING_CONFIRMED | 1 | Restructure |
| BOOKING_REJECTED | 1 | Restructure |
| BOOKING_SUBMITTED | 1 | Restructure |
| BROKER_SOLD | 1 | Asset disposal |
| BROKER_TERM_EXPIRED | 1 | Asset disposal |
| BUYBACK_AGREED | 1 | Deed in lieu |
| BUYBACK_FUNDING_FAILED | 1 | Asset disposal |
| BUYBACK_TERMS_SIGNED | 1 | Asset disposal |
| BUYER_BARRED | 1 | Debt sale |
| BUYER_CANCELED | 1 | Debt sale |
| BUYER_REMEDIATED | 1 | Debt sale |
| BUYER_REQUESTED_ACCESS | 1 | Debt sale |
| BUYER_SETTLED | 1 | Debt sale |
| CASELOAD_CAP_BREACHED | 1 | Universal rules |
| CASE_CREATED_IN_ERROR | 1 | Universal rules |
| CASE_FILED | 1 | Litigation |
| CASE_HAS_OPEN_DEVIATION | 1 | Write-off |
| CASE_PICKED_UP | 1 | Restructure |
| CASE_REOPEN_REQUESTED | 1 | Universal rules |
| CHECKLIST_COMPLETE | 1 | Guarantee claim |
| CHECKLIST_INCOMPLETE | 1 | Guarantee claim |
| CLAIM_APPROVED | 1 | Guarantee claim |
| CLAIM_CLOSED | 1 | Debt sale |
| CLAIM_REJECTED_BY_TCG | 1 | Guarantee claim |
| CLAIM_SENT_BACK | 1 | Guarantee claim |
| CLAIM_WINDOW_CLOSED | 1 | Debt sale |
| CLASSIFICATION_CHANGED | 1 | Universal rules |
| CLEARANCE_CONFIRMED | 1 | Settlement |
| COLLATERAL_RELEASED | 1 | Settlement |
| COMMITTEE_APPROVED | 1 | Write-off |
| COMMITTEE_DEFERRED | 1 | Write-off |
| COMMITTEE_REJECTED | 1 | Write-off |
| COMPLAINT_RAISED | 1 | Universal rules |
| CONDITIONS_LATER_MET | 1 | Guarantee claim |
| CONDITIONS_NOT_MET | 1 | Guarantee claim |
| CONDUCT_CHECK_FAILED | 1 | Litigation |
| CONSENT_WITHDRAWN | 1 | Universal rules |
| CONTACT_DETAIL_CHANGED | 1 | Universal rules |
| CONTACT_NOT_FOUND | 1 | Deviations |
| CONTACT_RESTORED | 1 | Deviations |
| CONTACT_STOP_APPLIED | 1 | Litigation |
| CONTACT_STOP_LIFTED | 1 | Universal rules |
| CORRECTION_RECORDED | 1 | Universal rules |
| CORRECTION_REFER_TO_COMMITTEE | 1 | Write-off |
| CORRECTION_REPOST | 1 | Write-off |
| CORRECTION_RETURN_TO_SCAN | 1 | Write-off |
| COURT_REJECTED_FILING | 1 | Litigation |
| CREDIT_APPROVED | 1 | Restructure |
| CREDIT_COMMITTEE_APPROVED | 1 | Write-off |
| CREDIT_COMMITTEE_REJECTED | 1 | Write-off |
| CREDIT_DECLINED | 1 | Restructure |
| CURE_PERIOD_EXPIRED | 1 | Restructure |
| CUSTOMER_DECEASED | 1 | Universal rules |
| CUSTOMER_DECLINED | 1 | Restructure |
| CUSTOMER_DISPUTED | 1 | Litigation |
| CUSTOMER_PAID_IN_FULL | 1 | Litigation |
| CUSTOMER_REQUESTED_TREATMENT | 1 | Litigation |
| CUSTOMER_WITHDREW | 1 | Deed in lieu |
| DATA_SUBJECT_REQUEST | 1 | Universal rules |
| DATA_TRANSFER_RUN | 1 | Debt sale |
| DEADLINE_WARNING | 1 | Guarantee claim |
| DEBTOR_PAID_AFTER_JUDGMENT | 1 | Litigation |
| DEBT_DISPUTED | 1 | Universal rules |
| DEBT_SALE_CYCLE_OPENED | 1 | Debt sale |
| DECISION_INCOMPLETE | 1 | Write-off |
| DECISION_LOG_WRITE_FAILED | 1 | Universal rules |
| DEFER_RECORDED | 1 | Litigation |
| DELIVERY_FAILED | 1 | Litigation |
| DERECOGNITION_RUN | 1 | Debt sale |
| DEVIATION_FLAGGED | 1 | Deviations |
| DIL_TRANSFER_REGISTERED | 1 | Asset disposal |
| DISPOSAL_REQUIRED | 1 | Deed in lieu |
| DIVIDEND_RECEIVED | 1 | Litigation |
| DOCUMENT_RETRIEVED | 1 | Litigation |
| DOCUMENT_SUPPLIED | 1 | Guarantee claim |
| DOCUMENT_UNRECOVERABLE | 1 | Litigation |
| DUPLICATE_CASE_FOUND | 1 | Universal rules |
| DUPLICATE_EVENT | 1 | Universal rules |
| ENCUMBRANCE_CLEAR | 1 | Deed in lieu |
| ENCUMBRANCE_CLEARED | 1 | Deed in lieu |
| ENCUMBRANCE_UNRESOLVED | 1 | Deed in lieu |
| ENFORCEMENT_EXHAUSTED | 1 | Litigation |
| ENFORCEMENT_OPENED | 1 | Litigation |
| ENFORCE_APPROVED | 1 | Litigation |
| ESCALATION_CLOSED | 1 | Universal rules |
| ESTATE_CONFIRMED | 1 | Deviations |
| EVIDENCE_SUPPLIED | 1 | Asset disposal |
| EXCEPTION_CLEARED | 1 | Write-off |
| EXCLUSION_CLEARED | 1 | Debt sale |
| FAST_LANE_SELECTED | 1 | Deed in lieu |
| FEED_ACCEPTED_ON_RETRY | 1 | Write-off |
| FEE_APPROVED | 1 | Litigation |
| FEE_DUE | 1 | Litigation |
| FEE_REJECTED | 1 | Litigation |
| FINAL_INSTALLMENT_PAID | 1 | Restructure |
| FINAL_INSTALLMENT_RECEIVED | 1 | Settlement |
| FINANCE_FEED_RUN | 1 | Write-off |
| FINANCE_REJECTED_FILE | 1 | Write-off |
| FIRM_BREACHED_SLA | 1 | Litigation |
| FIRM_MATCHED | 1 | Litigation |
| FIRM_NOMINATED | 1 | Litigation |
| FLAG_REJECTED | 1 | Deviations |
| FLOOR_APPROVED_BY_OFFICER | 1 | Asset disposal |
| FLOOR_REACHED_NO_BID | 1 | Asset disposal |
| FRAUD_CONFIRMED | 1 | Deviations |
| FRAUD_FLAGGED | 1 | Universal rules |
| FRAUD_NOT_CONFIRMED | 1 | Deviations |
| FULL_PAYMENT_RECEIVED | 1 | Guarantee claim |
| GL_POSTING_RUN | 1 | Debt sale |
| GUARANTEE_CLEARS_DEBT | 1 | Universal rules |
| GUARANTEE_FOUND | 1 | Guarantee claim |
| GUARANTOR_DISPUTED | 1 | Guarantee claim |
| GUARANTOR_NOTICE_DUE | 1 | Guarantee claim |
| GUARANTOR_REFUSED | 1 | Guarantee claim |
| GUARANTOR_SETTLED | 1 | Guarantee claim |
| HEARING_ADJOURNED | 1 | Litigation |
| HEARING_SCHEDULED | 1 | Litigation |
| INSPECTION_COMPLETED | 1 | Deed in lieu |
| INSTALLMENT_MISSED | 1 | Settlement |
| INSTRUCTION_DECLINED | 1 | Litigation |
| INSURANCE_SETTLED | 1 | Deviations |
| JUDGMENT_AGAINST_THE_BANK | 1 | Litigation |
| JUDGMENT_FOR_THE_BANK | 1 | Litigation |
| KYC_FAILED | 1 | Debt sale |
| KYC_PASSED | 1 | Debt sale |
| LADDER_EXHAUSTED | 1 | Litigation |
| LED_HANDOVER_RECEIVED | 1 | Asset disposal |
| LEGAL_HOLD_LIFTED | 1 | Universal rules |
| LEGAL_HOLD_PLACED | 1 | Universal rules |
| LIMIT_EXCEEDED | 1 | Write-off |
| LISTING_EVIDENCE_COMPLETE | 1 | Asset disposal |
| LISTING_EVIDENCE_MISSING | 1 | Asset disposal |
| LOAD_RESTORED | 1 | Write-off |
| LOSS_RECORDED | 1 | Guarantee claim |
| LOT_APPROVED_BY_COMMITTEE | 1 | Debt sale |
| LOT_NOT_CLEARED | 1 | Debt sale |
| LOT_PRICED | 1 | Debt sale |
| LOT_REFUSED | 1 | Debt sale |
| LOT_REOFFERED | 1 | Debt sale |
| LOT_REOFFERED_AFTER_CANCEL | 1 | Debt sale |
| LOT_TOO_THIN | 1 | Debt sale |
| MASKING_CHECK_FAILED | 1 | Debt sale |
| MASKING_CHECK_PASSED | 1 | Debt sale |
| MONTHLY_SCAN_STARTED | 1 | Write-off |
| NEW_DATE_SET | 1 | Litigation |
| NLEADS_CALLBACK_MISSING | 1 | Restructure |
| NOTICE_PERIOD_EXPIRED | 1 | Litigation |
| NOTICE_REISSUED | 1 | Asset disposal |
| NO_AGENCY_CAPACITY | 1 | Write-off |
| NO_ASSET_FOUND | 1 | Litigation |
| NO_CASE_REFERENCE | 1 | Litigation |
| NO_FIRM_AVAILABLE | 1 | Litigation |
| NO_PROPOSAL_RETURNED | 1 | Restructure |
| NO_SHORTFALL | 1 | Asset disposal |
| OCCUPANTS_REFUSE_POSSESSION | 1 | Asset disposal |
| OFFICER_REJECTED_PACK | 1 | Litigation |
| OUTBOUND_FAILED | 1 | Universal rules |
| OVERRIDE_REFUSED | 1 | Universal rules |
| OWNER_ACCEPTED | 1 | Universal rules |
| OWNER_UNAVAILABLE | 1 | Universal rules |
| PACK_APPROVED | 1 | Litigation |
| PACK_BUILT | 1 | Write-off |
| PACK_CHECK_FAILED | 1 | Write-off |
| PACK_COMPLETE | 1 | Litigation |
| PACK_COMPLETED | 1 | Write-off |
| PACK_INCOMPLETE | 1 | Litigation |
| PACK_REWORKED | 1 | Litigation |
| PACK_ROUTED | 1 | Write-off |
| PARTNER_CONDUCT_BREACH | 1 | Universal rules |
| PARTNER_CONFLICT_DECLARED | 1 | Universal rules |
| PARTNER_INSOLVENT | 1 | Universal rules |
| PARTNER_NO_RESPONSE | 1 | Universal rules |
| PARTNER_PANEL_EXIT | 1 | Universal rules |
| PARTNER_RESELECTED | 1 | Universal rules |
| PART_PAYMENT_RECEIVED | 1 | Guarantee claim |
| PAYMENT_BELONGS_TO_BUYER | 1 | Write-off |
| PAYMENT_DEADLINE_PASSED | 1 | Settlement |
| PAYMENT_MATCHES_NOTHING | 1 | Write-off |
| PAYMENT_MISSED | 1 | Restructure |
| PAYMENT_RECEIVED_LATE | 1 | Restructure |
| PAYMENT_REVERSED | 1 | Settlement |
| PAYMENT_TERM_EXPIRED | 1 | Asset disposal |
| PAYMENT_UNMATCHED | 1 | Settlement |
| PAYOFF_STALE | 1 | Settlement |
| PETITION_APPROVED | 1 | Litigation |
| PETITION_PROPOSED | 1 | Litigation |
| PETITION_REJECTED | 1 | Litigation |
| PLACEMENT_TERM_EXPIRED | 1 | Write-off |
| POPULATION_NOT_RECONCILED | 1 | Write-off |
| POPULATION_RECONCILED | 1 | Write-off |
| POSSESSION_TAKEN | 1 | Asset disposal |
| POSTING_CORRECTED | 1 | Debt sale |
| POSTING_REJECTED | 1 | Debt sale |
| POSTING_TASK_CREATED | 1 | Write-off |
| POST_CHARGEOFF_RULE_RUN | 1 | Write-off |
| PRELIMINARY_VALUATION_USED | 1 | Deed in lieu |
| PREPARATION_DUE | 1 | Guarantee claim |
| PRICE_BELOW_FLOOR | 1 | Deed in lieu |
| PRICE_INSIDE_FLOOR | 1 | Deed in lieu |
| PRICE_MODEL_RUN | 1 | Asset disposal |
| PRIOR_STATUS_RESTORED | 1 | Restructure |
| PROCEEDS_POSTED | 1 | Asset disposal |
| PRODUCT_MIGRATED | 1 | Universal rules |
| PROOF_OF_DELIVERY_RECEIVED | 1 | Litigation |
| PROOF_WINDOW_EXPIRED | 1 | Litigation |
| PROVISION_RELEASE_RUN | 1 | Write-off |
| PROVISION_STEP_DUE | 1 | Asset disposal |
| PUTBACK_ACCEPTED | 1 | Debt sale |
| PUTBACK_CLAIMED | 1 | Debt sale |
| PUTBACK_REFUSED_BY_BANK | 1 | Debt sale |
| QUERY_ANSWERED | 1 | Guarantee claim |
| QUERY_UNANSWERED | 1 | Guarantee claim |
| QUEUE_SLA_BREACHED | 1 | Restructure |
| RANGE_SET | 1 | Settlement |
| READY_TO_SELL | 1 | Asset disposal |
| REAPPRAISAL_CYCLE_DUE | 1 | Asset disposal |
| REGISTRATION_CHECK_PASSED | 1 | Deed in lieu |
| REGISTRATION_TRANSFERRED | 1 | Asset disposal |
| REJECTION_CLEARED | 1 | Write-off |
| RELIEF_SCHEME_APPLIED | 1 | Universal rules |
| RELIST_LIMIT_REACHED | 1 | Asset disposal |
| RELIST_RULE_APPLIED | 1 | Asset disposal |
| REMITTANCE_CONFIRMED | 1 | Write-off |
| REMOVAL_CLEARED | 1 | Write-off |
| RENTAL_ARREARS | 1 | Deed in lieu |
| REPLACEMENT_MADE | 1 | Write-off |
| REPOSSESSION_COMPLETED | 1 | Asset disposal |
| RESELECTION_RUN | 1 | Litigation |
| RESERVE_RAISED | 1 | Debt sale |
| RESIDUAL_REMAINS | 1 | Guarantee claim |
| RESTRUCTURE_PROPOSED | 1 | Restructure |
| RESUBMISSION_NOT_POSSIBLE | 1 | Guarantee claim |
| RESUBMISSION_POSSIBLE | 1 | Guarantee claim |
| RETENTION_CLASS_MISSING | 1 | Write-off |
| RETENTION_TIMER_EXPIRED | 1 | Write-off |
| RETRY_SUCCEEDED | 1 | Universal rules |
| REVERSAL_RECORDED | 1 | Settlement |
| ROUND_CLOSED_NO_BID | 1 | Asset disposal |
| ROUND_NO_BID | 1 | Litigation |
| ROUND_OPENED | 1 | Asset disposal |
| ROUND_REOPENED | 1 | Asset disposal |
| ROUND_SOLD | 1 | Litigation |
| ROUTE_OVERRIDDEN | 1 | Universal rules |
| ROUTE_REFUSED | 1 | Asset disposal |
| ROUTE_REOPENED | 1 | Deviations |
| ROUTE_REVIEW_REQUIRED | 1 | Asset disposal |
| ROUTE_SUBMITTED | 1 | Asset disposal |
| RULE_VERSION_EFFECTIVE | 1 | Universal rules |
| SALE_SELECTED | 1 | Write-off |
| SALE_SETTLED | 1 | Write-off |
| SCHEDULE_SET | 1 | Restructure |
| SEIZURE_BLOCKED | 1 | Litigation |
| SEIZURE_EXECUTED | 1 | Litigation |
| SETTLEMENT_APPROVED | 1 | Litigation |
| SETTLEMENT_BOOKED | 1 | Settlement |
| SETTLEMENT_BROKEN | 1 | Litigation |
| SETTLEMENT_COMPLETED | 1 | Litigation |
| SETTLEMENT_PROPOSED | 1 | Litigation |
| SETTLEMENT_REJECTED | 1 | Litigation |
| SETTLEMENT_TERM_EXPIRED | 1 | Debt sale |
| SETTLEMENT_TERM_STARTED | 1 | Debt sale |
| SHORTFALL_CALCULATED | 1 | Asset disposal |
| SHORTFALL_REMAINS | 1 | Litigation |
| SOFT_RECOVERY_SELECTED | 1 | Write-off |
| STATUTORY_NOTICE_FAILED | 1 | Asset disposal |
| SYSTEM_UNAVAILABLE | 1 | Universal rules |
| TAPE_BUILD_RUN | 1 | Debt sale |
| TAPE_REBUILT | 1 | Debt sale |
| TAX_CRITERIA_UNPUBLISHED | 1 | Write-off |
| TCG_QUERY_RAISED | 1 | Guarantee claim |
| TEAM_REMOVED_CASE | 1 | Write-off |
| TEMPLATE_REPLACED | 1 | Litigation |
| TEMPLATE_SELECTED | 1 | Litigation |
| TEMPLATE_WITHDRAWN | 1 | Litigation |
| TENANT_DEFAULTED | 1 | Asset disposal |
| TERMS_AGREED | 1 | Deed in lieu |
| TITLE_DOCUMENTS_MISSING | 1 | Settlement |
| TITLE_NOT_CLEAN | 1 | Deed in lieu |
| TITLE_REGISTERED | 1 | Asset disposal |
| TITLE_UNRESOLVED | 1 | Asset disposal |
| TRANSFER_INSTRUCTED | 1 | Asset disposal |
| TRANSFER_REJECTED | 1 | Asset disposal |
| TREATMENT_BROKEN | 1 | Litigation |
| UPSTREAM_DATA_CORRECTED | 1 | Universal rules |
| VALUATION_RECEIVED | 1 | Deed in lieu |
| VALUER_REPORTED | 1 | Asset disposal |
| VALUER_SLA_BREACHED | 1 | Deed in lieu |
| VALUE_REJECTED | 1 | Asset disposal |
| VENDOR_ACCEPTED | 1 | Asset disposal |
| VENDOR_REQUIRED | 1 | Asset disposal |
| VENDOR_UNAVAILABLE | 1 | Asset disposal |
| VULNERABILITY_IDENTIFIED | 1 | Universal rules |
| WORK_ACCEPTED | 1 | Asset disposal |
| WORK_ORDER_RAISED | 1 | Asset disposal |
| WORK_REFUSED | 1 | Asset disposal |
| WRITEOFF_QUESTIONED | 1 | Write-off |
| X3_INSURANCE_SETTLED | 1 | Litigation |
| X4_FRAUD_CONFIRMED | 1 | Litigation |
| X5_BANKRUPTCY_DETECTED | 1 | Litigation |
| X7_COLLATERAL_EVENT | 1 | Litigation |

## Sheet: Checks

| Completeness checks |  |  |  |
|---|---|---|---|
| Run over the full rule set each time a rule version is loaded. A load with an exception is refused. |  |  |  |
| Check | Result | Scope | Exceptions |
| Every rule has a unique ID | Pass | 448 rules, 448 IDs | None |
| Every from state and to state is a state in its route set | Pass | 896 references checked | None |
| Every state that is not an end state has at least one rule out | Pass |  | None |
| Every state except a start state is reached by at least one rule | Pass |  | None |
| No two rules in a route set share the same from state, event and condition | Pass | 448 combinations | None |
| Every rule names the owner of the next state | Pass |  | None |
| Every rule states its action | Pass |  | None |
| Every rule states its condition | Pass |  | None |
| Every route set has at least one end state | Pass | 30 end states | None |

## Sheet: Key

| Key |  |  |
|---|---|---|
| What each column, value and kind of state means. |  |  |
| Item | Term | Meaning |
| Column | Rule | R, the route set code and a number |
| Column | From state, Event, Condition | Inputs of the decision table |
| Column | Action, To state, Owner, Systems, Timer | Outputs of the decision table |
| Value | Any | In the Condition column: the event alone fires the rule |
| Value | Workbench | In the Owner column: no person holds the case in the next state |
| Value | None | In the Timer column: the next state has no time limit of its own |
| Hit policy | Unique | In a route set, for one state and one event, at most one condition holds |
| State kind | Start | where the route begins |
| State kind | System step | the Workbench or another system acts |
| State kind | Officer step | a bank officer acts |
| State kind | Decision point | a rule or an approver chooses |
| State kind | Customer step | the customer acts |
| State kind | Partner step | a partner acts |
| State kind | Exception | reached by an event |
| State kind | End state | the route ends here |

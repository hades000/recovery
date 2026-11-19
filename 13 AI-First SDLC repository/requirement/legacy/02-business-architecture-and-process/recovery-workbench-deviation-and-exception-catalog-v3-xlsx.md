<!-- source: 02 Business architecture and process/Recovery Workbench Deviation and Exception Catalog v3.xlsx -->
<!-- converted: 2026-11-04 from XLSX -->

> **Source:** `02 Business architecture and process/Recovery Workbench Deviation and Exception Catalog v3.xlsx`  
> **Converted from:** XLSX

## Deviations

| Deviations X1 to X7 |  |  |  |  |  |  |  |  |  |  |
|---|---|---|---|---|---|---|---|---|---|---|
| Seven deviations. Each pauses the stage clock and never the prescription clock, goes to a named handler, and returns the case or re-routes it. |  |  |  |  |  |  |  |  |  |  |
| Code | Deviation | What it is | What raises it | What it suspends | What keeps running | Handler | Assigned by | How the case returns | Service level | Contact stop |
| X1 | Dispute or complaint | A complaint is logged, or the customer disputes the balance or the security | R-UNI-04 complaint raised; R-UNI-09 debt disputed; screening agent at case entry; any officer | The stage clock; contact with the customer; recovery action on the disputed amount | The prescription clock and every legal period clock | Complaint officer | R-DEV-02 | The same decision resumes when the complaint is resolved (R-DEV-09, R-DEV-18) | 10 working days, then escalation (R-DEV-20) | Yes |
| X2 | Vulnerable customer or hardship | Hardship or vulnerability is recorded | R-UNI-06 vulnerability identified; screening agent; any officer | The stage clock; collection contact outside the vulnerable customer treatment rules | The prescription clock | Hardship and vulnerability specialist | R-DEV-03 | Routed to the restructure assessment (R-DEV-10), then the route decision (R-DEV-19) | 10 working days, then escalation (R-DEV-20) | Yes, except treatment contact |
| X3 | Deceased customer | A death is confirmed from the registry or a document | R-UNI-05 customer deceased; document intake | All contact with the customer; every route action | The prescription clock; the estate claim deadline | Hardship and vulnerability specialist, with Legal for the estate claim | R-DEV-03 | Closed if insurance clears the balance (R-DEV-11); otherwise back to the route decision against the estate (R-DEV-12) | 10 working days, then escalation (R-DEV-20) | Yes |
| X4 | Fraud | Aric or an officer flags fraud | R-UNI-08 fraud flagged; Aric referral | The case and every route action | The prescription clock | Fraud investigator | R-DEV-04 | Fraud confirmed: to write-off with recovery under the fraud case (R-DEV-13). Not confirmed: back to the route decision (R-DEV-14) | 10 working days, then escalation (R-DEV-20) | Yes |
| X5 | Bankruptcy or external seizure | A bankruptcy filing or a seizure by another creditor is notified | R-UNI-07 bankruptcy notified | Enforcement and every collection action against the debtor | The prescription clock; the claim deadline with the official receiver or the Legal Execution Department | Legal counsel | R-DEV-05 | Claim filed, then litigation and write-off after the receiver reports (R-DEV-15) | The filing deadline | Yes |
| X6 | Lost contact | No contact point reaches the customer | Screening agent; failed contact attempts; returned notices | The stage clock | The prescription clock; statutory notices to the last known address | Case owner, with the agent tracing within policy | R-DEV-06 | Contact restored: back to the paused state (R-DEV-16, R-UNI-12). Trace exhausted: escalation or the route decision (R-DEV-17) | 30 days for the trace (R-DEV-17) | No |
| X7 | Collateral event | The collateral is damaged, destroyed, seized or lost | Screening agent; insurer or valuer report; any officer | The stage clock; disposal of the collateral | The prescription clock; the insurance claim deadline | Case owner, with the agent within policy; a person approves an insurance claim | R-DEV-06 | The same decision resumes (R-DEV-09, R-DEV-18) | 10 working days, then escalation (R-DEV-20) | No |

## Raising rules

| How a deviation is raised |  |  |  |  |  |  |
|---|---|---|---|---|---|---|
| The universal rules that raise a deviation from any active state, and the rule that pauses the case. |  |  |  |  |  |  |
| Rule | Event | Condition | Action | To state | Owner | Timer |
| R-DEV-01 | DEVIATION_FLAGGED | deviation_code in (X1..X7) | Pause the stage clock, keep the prescription clock running, route to the named owner | DEV_FLAGGED | Workbench | same day |
| R-UNI-04 | COMPLAINT_RAISED | a complaint is logged against the case | Raise X1, pause the stage clock, apply the contact stop | HELD_DEVIATION | Complaint officer | same day |
| R-UNI-05 | CUSTOMER_DECEASED | a death is confirmed from the registry or a document | Raise X3, stop all contact, hold the case for the specialist and Legal | HELD_DEVIATION | Specialist, Legal | same day |
| R-UNI-06 | VULNERABILITY_IDENTIFIED | hardship or vulnerability is recorded | Raise X2, apply the vulnerable customer treatment rules | HELD_DEVIATION | Specialist | same day |
| R-UNI-07 | BANKRUPTCY_NOTIFIED | a filing or an external seizure is notified | Raise X5, stop enforcement, start the claim deadline clock | HELD_DEVIATION | Legal | deadline driven |
| R-UNI-08 | FRAUD_FLAGGED | Aric or an officer flags fraud | Raise X4, hold the case, refer to the fraud team | HELD_DEVIATION | Fraud team | same day |
| R-UNI-09 | DEBT_DISPUTED | the customer disputes the balance or the security | Raise X1, pause recovery action on the disputed amount | HELD_DEVIATION | Complaint officer | same day |

## Handling rules

| How a deviation is handled and cleared |  |  |  |  |  |  |  |
|---|---|---|---|---|---|---|---|
| 22 rules in the deviation route set. |  |  |  |  |  |  |  |
| Rule | From state | Event | Condition | Action | To state | Owner | Timer |
| R-DEV-01 | ANY_STATE | DEVIATION_FLAGGED | deviation_code in (X1..X7) | Pause the stage clock, keep the prescription clock running, route to the named owner | DEV_FLAGGED | Workbench | same day |
| R-DEV-02 | DEV_FLAGGED | OWNER_ASSIGNED | deviation_code = X1 | Assign to the complaint officer | DEV_WITH_OWNER | Complaint officer | None |
| R-DEV-03 | DEV_FLAGGED | OWNER_ASSIGNED | deviation_code in (X2,X3) | Assign to the specialist; Legal joins X3 for the estate claim | DEV_WITH_OWNER | Specialist, Legal | None |
| R-DEV-04 | DEV_FLAGGED | OWNER_ASSIGNED | deviation_code = X4 | Assign to the fraud team and refer to Aric | DEV_WITH_OWNER | Fraud team | None |
| R-DEV-05 | DEV_FLAGGED | OWNER_ASSIGNED | deviation_code = X5 | Assign to Legal; file with the official receiver or the LED before the deadline | DEV_WITH_OWNER | Legal | deadline driven |
| R-DEV-06 | DEV_FLAGGED | OWNER_ASSIGNED | deviation_code in (X6,X7) | Agent handles within policy; a person approves an insurance claim | DEV_WITH_OWNER | Agent, case owner | None |
| R-DEV-07 | DEV_FLAGGED | FLAG_REJECTED | owner marks the flag as not a deviation | Clear the flag, record the reason, resume the clock | DEV_REJECTED | Workbench | None |
| R-DEV-08 | DEV_REJECTED | CLOCK_RESUMED | Any | Return the case to the state it paused in | RESUMED | Previous owner | None |
| R-DEV-09 | DEV_WITH_OWNER | DEVIATION_RESOLVED | deviation_code in (X1,X7) | Record the outcome; the same decision resumes | DEV_RESOLVED | Case owner | None |
| R-DEV-10 | DEV_WITH_OWNER | DEVIATION_RESOLVED | deviation_code = X2 | Route to the restructure assessment | DEV_REROUTE | Restructuring officer | None |
| R-DEV-11 | DEV_WITH_OWNER | INSURANCE_SETTLED | deviation_code = X3 and insurance clears the balance | Close the case | CASE_ENDED | Workbench | None |
| R-DEV-12 | DEV_WITH_OWNER | ESTATE_CONFIRMED | deviation_code = X3 and insurance does not clear | Return to the route decision against the estate | DEV_REROUTE | Case owner | None |
| R-DEV-13 | DEV_WITH_OWNER | FRAUD_CONFIRMED | deviation_code = X4 and fraud confirmed | Route to write-off; recovery continues under the fraud case | DEV_REROUTE | Write-off team | None |
| R-DEV-14 | DEV_WITH_OWNER | FRAUD_NOT_CONFIRMED | deviation_code = X4 and fraud not confirmed | Return to the collections decision | DEV_REROUTE | Case owner | None |
| R-DEV-15 | DEV_WITH_OWNER | BANKRUPTCY_FILED | deviation_code = X5 | Route to litigation, then to write-off after the receiver reports | DEV_REROUTE | Legal, litigation officer | None |
| R-DEV-16 | DEV_WITH_OWNER | CONTACT_RESTORED | deviation_code = X6 and a contact point is verified | Close X6 and return to the paused state | DEV_RESOLVED | Case owner | None |
| R-DEV-17 | DEV_WITH_OWNER | CONTACT_NOT_FOUND | deviation_code = X6 and skip trace exhausted | Route to escalation or to the route decision | DEV_REROUTE | Case owner | 30 days |
| R-DEV-18 | DEV_RESOLVED | CLOCK_RESUMED | Any | Resume the stage clock and return the case | RESUMED | Previous owner | None |
| R-DEV-19 | DEV_REROUTE | ROUTE_REOPENED | Any | Recompute the segment and re-run the hard gates | ROUTE_D6 | Case owner | None |
| R-DEV-20 | DEV_WITH_OWNER | SLA_BREACHED | time in DEV_WITH_OWNER exceeds the deviation service level | Escalate to the team manager and report the breach | DEV_WITH_OWNER | Team manager | 10 working days |
| R-DEV-21 | DEV_FLAGGED | OWNER_ASSIGNED | deviation_code is not one of X1 to X7, or no owner is set for the code | Assign to the case owner's team manager and log the unmapped code | DEV_WITH_OWNER | Team manager | same day |
| R-DEV-22 | DEV_WITH_OWNER | DEVIATION_RESOLVED | otherwise, the outcome does not name a next step | Return the case to the route decision and record that the outcome was not mapped | DEV_REROUTE | Case owner | 2 working days |

## Other holds

| Holds that are not deviations |  |  |  |  |  |
|---|---|---|---|---|---|
| Events that stop part or all of the normal route without raising X1 to X7. |  |  |  |  |  |
| Rule | Event | Condition | Action | Owner | Timer |
| R-UNI-10 | CONSENT_WITHDRAWN | the customer withdraws consent for a channel | Remove that channel from the contact plan, keep the statutory notices | Conduct and QA officer | same day |
| R-UNI-11 | DATA_SUBJECT_REQUEST | a PDPA access, correction or erasure request is received | Hold automated processing on the case, route to Compliance inside the statutory period | Compliance | statutory period |
| R-UNI-13 | RELIEF_SCHEME_APPLIED | the account qualifies for a government or bank relief scheme | Apply the scheme terms, pause recovery for the scheme period | Risk | scheme terms |
| R-UNI-20 | LEGAL_HOLD_PLACED | a regulator, court or Legal places a hold | Stop every outbound action and every automated decision, keep the clocks visible | Legal | until lifted |

## Exceptions

| Exception events in the route sets |  |  |  |  |  |  |  |
|---|---|---|---|---|---|---|---|
| 53 exception events across the ten flows: what raises each one and where the case goes next. |  |  |  |  |  |  |  |
| Flow | Step | Exception | What it means | Raised by | Next | Owner | Timer |
| Restructure | DECLINED_BY_CREDIT | Declined by credit | Reason recorded | R-RES-12 CREDIT_DECLINED | R-RES-14 to BACK_TO_ROUTE_DECISION | Restructuring officer, FCR | None |
| Restructure | RETURNED_TO_COLLINS | Returned to COLLINS | Prior status restored | R-RES-17 CUSTOMER_DECLINED; R-RES-18 OFFER_EXPIRED | R-RES-20 to BACK_TO_ROUTE_DECISION | Workbench | None |
| Restructure | PLAN_CURE_PERIOD | In the cure period | An installment was missed | R-RES-27 PAYMENT_MISSED | R-RES-28 to PLAN_RUNNING; R-RES-29 to PLAN_BROKEN | Case owner | cure_period_days from reference data |
| Restructure | PLAN_BROKEN | Plan broken | Break count incremented | R-RES-29 CURE_PERIOD_EXPIRED | R-RES-30 to BACK_TO_ROUTE_DECISION; R-RES-31 to RESTRUCTURE_BARRED; R-RES-36 to UNMATCHED_EXCEPTION | Case owner | None |
| Restructure | UNMATCHED_EXCEPTION | UNMATCHED_EXCEPTION | No rule matched. Held for a person. | R-RES-35 OFFER_PREPARED; R-RES-36 BREAK_RECORDED | R-RES-37 to BACK_TO_ROUTE_DECISION | Case owner | same day |
| Settlement | DECLINED_BY_APPROVER_SET | Approval refused | Reason recorded | R-SET-07 APPROVAL_REFUSED | R-SET-08 to RETURNED_TO_ROUTE_SET | Restructuring officer, FCR | None |
| Settlement | PAYMENT_PART_RECEIVED | Part received | Balance still due | R-SET-15 PAYMENT_RECEIVED | R-SET-18 to PAYMENT_CLEARED; R-SET-19 to RETURNED_TO_ROUTE_SET | Workbench | None |
| Settlement | PAYMENT_REVERSED | Payment reversed | After release | R-SET-23 PAYMENT_REVERSED | R-SET-24 to RETURNED_TO_ROUTE_SET | Case owner | None |
| Settlement | UNMATCHED_EXCEPTION | UNMATCHED_EXCEPTION | No rule matched. Held for a person. | R-SET-25 OFFER_PREPARED; R-SET-26 PAYMENT_RECEIVED | R-SET-27 to RETURNED_TO_ROUTE_SET | Case owner | same day |
| Deed in lieu and voluntary surrender | ENCUMBRANCE_BLOCKED | Encumbrance unresolved | Transfer blocked | R-DIL-04 ENCUMBRANCE_UNRESOLVED | R-DIL-05 to VALUATION_ORDERED; R-DIL-06 to RETURNED_TO_ROUTE_DIL | Case owner | 10 working days |
| Deed in lieu and voluntary surrender | TITLE_NOT_CLEAN | Title not clean | Transfer held | R-DIL-29 TITLE_NOT_CLEAN | R-DIL-30 to AWAITING_TRANSFER; R-DIL-31 to RETURNED_TO_ROUTE_DIL | Case owner | 10 working days |
| Deed in lieu and voluntary surrender | UNMATCHED_EXCEPTION | UNMATCHED_EXCEPTION | No rule matched. Held for a person. | R-DIL-35 CUSTOMER_ACCEPTED; R-DIL-36 TRANSFER_COMPLETED | R-DIL-37 to RETURNED_TO_ROUTE_DIL | Case owner | same day |
| Litigation and enforcement | DEVIATION_HOLD | Deviation hold | X1 to X7. Timers pause, prescription keeps running | R-LIT-14 CUSTOMER_DISPUTED; R-LIT-73 DEVIATION_RAISED | R-LIT-74 to IN_HEARING; R-LIT-75 to TO_TREATMENT; R-LIT-76 to CASE_CLOSED; R-LIT-77 to TO_WRITE_OFF; R-LIT-78 to OFFICIAL_RECEIVER_CLAIM; R-LIT-79 to TO_TREATMENT | Complaint officer, Named deviation approver | None |
| Litigation and enforcement | NOTICE_BLOCKED | Notice blocked | Template withdrawn, or a contact stop applies | R-LIT-04 TEMPLATE_WITHDRAWN; R-LIT-05 CONTACT_STOP_APPLIED; R-LIT-22 CONDUCT_CHECK_FAILED | R-LIT-06 to NOTICE_GENERATED | Litigation officer, Conduct and QA officer | 1 working day; 2 working days |
| Litigation and enforcement | NOTICE_UNSERVED | Notice unserved | No proof returned, refused or undeliverable | R-LIT-08 PROOF_WINDOW_EXPIRED; R-LIT-09 DELIVERY_FAILED | R-LIT-10 to NOTICE_DISPATCHED; R-LIT-11 to PACK_ASSEMBLY | Litigation officer | 7 days; 2 working days |
| Litigation and enforcement | PACK_DEFECT_HOLD | Pack held on a defect | An item on the defect list is missing | R-LIT-17 PACK_INCOMPLETE | R-LIT-18 to PACK_ASSEMBLY; R-LIT-19 to PACK_VERIFIED; R-LIT-20 to PACK_VERIFIED | Litigation officer | 5 working days |
| Litigation and enforcement | FIRM_DECLINED | Firm declined or breached | Re-select the next firm on the scorecard | R-LIT-27 INSTRUCTION_DECLINED; R-LIT-28 FIRM_BREACHED_SLA | R-LIT-29 to FIRM_INSTRUCTED | Workbench, Partner and agency manager | 2 working days |
| Litigation and enforcement | FILING_REJECTED | Court rejected the filing | Defect recorded, pack reworked | R-LIT-31 COURT_REJECTED_FILING | R-LIT-32 to PACK_ASSEMBLY | Litigation officer | 5 working days |
| Litigation and enforcement | HEARING_ADJOURNED | Hearing adjourned | Timer reset, postpone reason coded | R-LIT-34 HEARING_ADJOURNED | R-LIT-35 to IN_HEARING | Panel law firm | To the new date |
| Litigation and enforcement | JUDGMENT_DISMISSED | Dismissed or lost | Appeal window opens | R-LIT-45 JUDGMENT_AGAINST_THE_BANK | R-LIT-46 to APPEAL_DECISION | Litigation officer | To the appeal window end |
| Litigation and enforcement | DEFERRAL_RECORDED | Deferral recorded | Coded reason and a review date re-queue the case | R-LIT-55 DEFER_RECORDED | R-LIT-56 to ENFORCEMENT_DECISION; R-LIT-57 to TO_WRITE_OFF | Enforcement owner | To the review date |
| Litigation and enforcement | NO_BID_AT_70 | No bid at 70 percent | The ladder is exhausted | R-LIT-67 LADDER_EXHAUSTED | R-LIT-68 to TO_ASSET_DISPOSAL; R-LIT-69 to ENFORCEMENT_DECISION | Enforcement owner | 5 working days |
| Guarantee claim | NOT_ELIGIBLE | Not eligible | Scheme default conditions not met | R-GUA-02 CONDITIONS_NOT_MET | R-GUA-03 to DEADLINE_TIMER_RUNNING | Guarantee officer | None |
| Guarantee claim | CLAIM_DEFECT_HOLD | Claim held on a defect | A checklist item is missing | R-GUA-08 CHECKLIST_INCOMPLETE | R-GUA-10 to CLAIM_PREPARATION; R-GUA-11 to CLAIM_APPROVAL | Guarantee officer | 5 working days |
| Guarantee claim | TCG_QUERY | TCG query | More information requested before assessment | R-GUA-14 TCG_QUERY_RAISED | R-GUA-15 to CLAIM_SUBMITTED; R-GUA-16 to CLAIM_REJECTED | Guarantee officer | To the TCG response date |
| Guarantee claim | CLAIM_REJECTED | Claim rejected | Rejection reason recorded against the guarantee | R-GUA-16 QUERY_UNANSWERED; R-GUA-17 CLAIM_REJECTED_BY_TCG | R-GUA-18 to CLAIM_PREPARATION; R-GUA-19 to RESIDUAL_TO_ROUTE | Guarantee officer | 5 working days |
| Guarantee claim | GUARANTOR_DISPUTE_HOLD | Guarantor dispute | X1 raised against the guarantee itself | R-GUA-30 GUARANTOR_DISPUTED | R-GUA-31 to GUARANTOR_NOTICE; R-GUA-32 to RESIDUAL_TO_ROUTE | Complaint officer | None |
| Guarantee claim | DEADLINE_MISSED | Claim deadline missed | The claim is lost. Loss, reason and amount recorded | R-GUA-05 CLAIM_DEADLINE_MISSED; R-GUA-09 CLAIM_DEADLINE_MISSED | R-GUA-27 to RESIDUAL_TO_ROUTE | Guarantee officer | None |
| Asset disposal | FAILED_NOTICE_QUEUE | Failed notice queue | FAILED_NOTICE_QUEUE | R-DIS-04 STATUTORY_NOTICE_FAILED | R-DIS-05 to ASSET_PENDING_TAKE_ON | Sale officer | 2 working days |
| Asset disposal | TITLE_BLOCKED | Title or registration blocked | TITLE_BLOCKED | R-DIS-07 TITLE_UNRESOLVED; R-DIS-53 TRANSFER_REJECTED | R-DIS-08 to ASSET_HELD | Sale officer | 10 working days; 5 working days |
| Asset disposal | DISPOSAL_PAUSED_DEVIATION | Paused on a deviation | DISPOSAL_PAUSED_DEVIATION | R-DIS-66 DEVIATION_RAISED; R-DIS-67 DEVIATION_RAISED | R-DIS-68 to ASSET_HELD; R-DIS-69 to TO_WRITEOFF | Deviation owner | None |
| Asset disposal | LISTING_BLOCKED | Listing blocked on evidence | LISTING_BLOCKED | R-DIS-34 LISTING_EVIDENCE_MISSING | R-DIS-35 to LISTING_LIVE | Sale officer | 5 working days |
| Asset disposal | NO_BID_AT_FLOOR | Floor reached with no bid | NO_BID_AT_FLOOR | R-DIS-39 FLOOR_REACHED_NO_BID | R-DIS-44 to RELISTED; R-DIS-46 to TO_DEBT_SALE | Sale officer | None |
| Asset disposal | AWARD_CANCELED | Award canceled | AWARD_CANCELED | R-DIS-49 PAYMENT_TERM_EXPIRED | R-DIS-50 to ROUND_OPEN | Sale officer | None |
| Asset disposal | UNMATCHED_EXCEPTION | UNMATCHED_EXCEPTION | No rule matched. Held for a person. | R-DIS-70 ROUTE_APPROVED; R-DIS-71 RESIDUAL_ROUTED | R-DIS-72 to ASSET_HELD | Sale officer | same day |
| Debt sale | CASE_EXCLUDED | Account excluded | CASE_EXCLUDED | R-DS-02 ACCOUNT_EXCLUDED | R-DS-03 to BACK_TO_CASE_LIST | Case owner | None |
| Debt sale | LOT_WITHDRAWN | Lot withdrawn | LOT_WITHDRAWN | R-DS-08 LOT_REFUSED; R-DS-22 LOT_NOT_CLEARED | R-DS-09 to BACK_TO_CASE_LIST | Debt sale officer | None |
| Debt sale | TAPE_REJECTED | Tape rejected on masking | TAPE_REJECTED | R-DS-11 MASKING_CHECK_FAILED | R-DS-12 to TAPE_PREPARED | Workbench | None |
| Debt sale | BUYER_REJECTED | Buyer refused | BUYER_REJECTED | R-DS-16 KYC_FAILED | R-DS-40 to BUYER_PENDING_KYC; R-DS-41 to BACK_TO_CASE_LIST | Debt sale officer | None |
| Debt sale | BID_BELOW_RESERVE | Best bid below the reserve | BID_BELOW_RESERVE | R-DS-20 BEST_BID_BELOW_RESERVE | R-DS-21 to BIDDING_OPEN; R-DS-22 to LOT_WITHDRAWN | Debt sale officer | None |
| Debt sale | AWARD_CANCELED_DS | Award canceled | AWARD_CANCELED_DS | R-DS-26 BUYER_CANCELED; R-DS-27 SETTLEMENT_TERM_EXPIRED | R-DS-28 to BIDDING_OPEN | Debt sale officer | None |
| Debt sale | POSTING_REJECTED_DS | Posting rejected | POSTING_REJECTED_DS | R-DS-32 POSTING_REJECTED | R-DS-33 to GL_POSTED | Credit Administration | 2 working days |
| Write off and recover after charge-off | SCAN_HELD | Scan held | SCAN_HELD | R-WO-02 ALS_LOAD_FAILED; R-WO-03 TAX_CRITERIA_UNPUBLISHED | R-WO-04 to SCAN_DUE | Write-off team | 1 working day |
| Write off and recover after charge-off | CASE_REMOVED_BY_TEAM | Case removed with a reason | CASE_REMOVED_BY_TEAM | R-WO-06 CASE_HAS_OPEN_DEVIATION; R-WO-07 TEAM_REMOVED_CASE | R-WO-08 to SCAN_DUE | Deviation owner, Write-off team | None |
| Write off and recover after charge-off | PACK_INCOMPLETE | Pack incomplete | PACK_INCOMPLETE | R-WO-09 PACK_CHECK_FAILED | R-WO-10 to WITH_COMMITTEE | Write-off team | 2 working days |
| Write off and recover after charge-off | DEFERRED | Deferred with a review date | DEFERRED | R-WO-17 COMMITTEE_DEFERRED | R-WO-19 to SCAN_DUE | Write-off team | to the review date |
| Write off and recover after charge-off | POSTING_REJECTED | Posting rejected | POSTING_REJECTED | R-WO-22 ALS_POSTING_REJECTED | R-WO-23 to POSTING_PENDING; R-WO-24 to WRITEOFF_EXCEPTION | Credit Administration | 2 working days |
| Write off and recover after charge-off | FINANCE_FEED_REJECTED | Finance feed rejected | FINANCE_FEED_REJECTED | R-WO-27 FINANCE_REJECTED_FILE | R-WO-28 to FINANCE_FEED_SENT | Credit Administration | 2 working days |
| Write off and recover after charge-off | PLACEMENT_RECALLED | Placement recalled | PLACEMENT_RECALLED | R-WO-34 AGENCY_UNDERPERFORMS | R-WO-35 to PLACED_WITH_AGENCY | Partner and agency manager | None |
| Write off and recover after charge-off | PAYMENT_EXCEPTION | Payment on the exception list | PAYMENT_EXCEPTION | R-WO-38 PAYMENT_MATCHES_NOTHING | R-WO-39 to PAYMENT_MATCHED | Case owner | 2 working days |
| Write off and recover after charge-off | WRITEOFF_EXCEPTION | Write-off exception, owner to confirm | WRITEOFF_EXCEPTION | R-WO-24 RETRY_LIMIT_REACHED; R-WO-41 WRITEOFF_QUESTIONED; R-WO-43 POPULATION_NOT_RECONCILED | R-WO-44 to POSTING_PENDING; R-WO-45 to SCAN_DUE; R-WO-46 to WITH_COMMITTEE | Owner to confirm with C&R | to confirm with Credit Administration |
| Universal rules | EXCEPTION_QUEUE | EXCEPTION_QUEUE | A person decides, the gap is logged | R-UNI-03 PAYMENT_RECEIVED; R-UNI-34 OUTBOUND_FAILED; R-UNI-36 RETRY_LIMIT_REACHED; R-UNI-39 DECISION_LOG_WRITE_FAILED | R-UNI-41 to ROUTE_D6_REOPEN | Case owner, Platform team | 2 working days; per interface; immediate |
| Universal rules | RETRY_QUEUE | RETRY_QUEUE | Automatic retry, then the exception queue | R-UNI-33 SYSTEM_UNAVAILABLE | R-UNI-35 to RESUME_STATE; R-UNI-36 to EXCEPTION_QUEUE | Platform team | per interface |

## Key

| Key |  |  |
|---|---|---|
| What each term means. |  |  |
| Item | Term | Meaning |
| Term | Deviation | An event that stops the normal route: X1 to X7. The case goes to a named handler |
| Term | Exception event | A step in a route set reached when something goes wrong in that route, such as a rejected filing or a missed deadline |
| Term | Stage clock | Time in the current state. Paused while a deviation is open |
| Term | Prescription clock | Time to the earliest date a legal claim expires. Never paused |
| Term | Contact stop | No one contacts the customer while it is in force. Statutory notices still go |
| Standard | CMMN 1.1 | A deviation is an event listener that pauses the stage and starts the handling tasks |

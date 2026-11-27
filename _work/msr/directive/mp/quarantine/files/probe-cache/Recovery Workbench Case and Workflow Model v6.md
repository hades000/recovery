## Sheet: Read me

| SCB Collections and Recovery. Henka Group, 22 November 2026. |  |
|---|---|
| (C) Siam Commercial Bank and Henka Pte Ltd |  |
| Recovery Workbench Case and Workflow Model v6 |  |
| Item | Value |
| Document | Recovery Workbench Case and Workflow Model v6 |
| Version | 6 |
| Status | Draft |
| Decision | D-RCV-60 |
| Source | 02 Business architecture and process/Recovery Workbench Case and Workflow Model v5.xlsx (read-only) |
| Change | D-RCV-60 microservice realignment: a CaseWorkflow parent with a child workflow per stage. Every sheet, ID, number and date of v5 is kept unchanged. |
| Owner services | Recovery Workbench Microservice Ownership Map v1 (D-RCV-60) |
| New sheets | Workflow model (v5); Stage ownership (v5); Case file ownership (v5); Change log; Realignment changes |
| Tool | T3 Code / OpenCode / DeepSeek v4.1 Flash |
| Date | 22 November 2026 |
| How to read | The v5 sheets are unchanged: Stages, Elements, Case status, Status transitions, Milestones, Tasks, Event listeners, Sentries and Case file. The new sheets show how the same CMMN model runs on the 19 microservices. |
| Workflow source | Architecture v5 Text Extract v1 slides 25 and 41; Temporal and Drools Design Text Extract v1 slide 13; Microservice Ownership Map v1 (Workflows and activities). |
| Namespace | rwb-recovery |

## Sheet: Stages

| Case and workflow model: stages |  |  |  |  |  |  |
|---|---|---|---|---|---|---|
| 10 stages. Element counts are in the Elements tab. |  |  |  |  |  |  |
| Stage | Kind | Entered when | Leaves when | Tasks and milestones | Sentries | Always available |
| Restructure, TDR | Solution stage | The route decision D6 approves a restructure, or D5 proposes one | Plan runs to term and the case closes; Plan breaks and the case returns to the route decision; Customer does not sign and the case returns to its prior status in COLLINS; A second break bars a further restructure | 18 | 37 | No |
| Settlement | Solution stage | The route decision D6 approves a settlement | Payment clears, the collateral is released and the case closes; The customer does not pay by the deadline and the case returns to the route decision; A payment reverses after release and the case re-opens | 15 | 27 | No |
| Deed in lieu and voluntary surrender | Solution stage | The route decision D6 approves a deed in lieu, or the customer offers the asset during a negotiation | The asset is on the books and hands off to the disposal route; The customer rents the asset back and the rental runs; The customer withdraws or the title is not clean and the case returns to the route decision | 20 | 37 | No |
| Litigation and enforcement, D7 | Enforcement stage | The route decision D6.3 approves litigation, or a broken treatment returns the case to the legal route | Debt satisfied and the case closes; Asset taken onto the books and handed to the disposal route; Judgment unenforceable or enforcement exhausted, and the case goes to write-off; Customer cures or settles, and the case returns to treatment | 38 | 79 | No |
| Guarantee claim, D6.5 and D6.6 | Recovery stage | A guarantee is detected on the case at takeover and the claim deadline timer starts | The claim is paid and the residual returns to the route decision; The claim is lost on the deadline and the full balance returns to the route decision; The guarantor settles and the case closes | 17 | 32 | No |
| Asset disposal, D8.1 to D8.3 | Recovery stage | An asset is taken onto the bank's books and the holding age clock starts | Sold, proceeds applied and the case closed with no shortfall; Sold with a residual, handed to debt sale or write-off; Transferred to RAMC or the joint venture; Rented, with the asset still held | 40 | 72 | No |
| Debt sale, D8.4 | Recovery stage | The monthly debt sale cycle opens, or a residual arrives from the disposal route | Lot awarded, settled, transferred and closed with realized recovery recorded; Lot withdrawn and the accounts returned to the case list; Put-back upheld and the account returned to the bank | 29 | 41 | No |
| Write off and recover after charge-off, D9 | Closure stage | The monthly eligibility scan runs on the cut-off date, or a residual arrives from another route | Posted, placed, recovered and closed after the retention period; Rejected by the committee and returned to the pursue track; Sold to a buyer as a charged-off population | 27 | 51 | No |
| Deviations X1 to X7 | Exception stage | The screening agent flags a deviation at entry or on a new document | The deviation clears and the case returns to the state it paused in; The deviation moves the case to a different route; The case ends, where insurance settles the debt | 9 | 22 | Yes |
| Universal rules, any state | Always on | The case is in any active state on any route | The case returns to the state it was in; The case moves to the route decision; The case closes; The case is canceled or merged | 20 | 50 | Yes |

## Sheet: Elements

| Elements |  |  |
|---|---|---|
| The CMMN 1.1 elements in the model and how many of each. |  |  |
| Element | Count | What it is |
| Case | 1 | The recovery case for one customer and one product, with the accounts linked, from day 90 to close. |
| Stage | 10 | A route the case can be on. Eight are entered when the route decision selects them; the deviation stage and the universal rules are always available. |
| Milestone | 30 | A state the case reaches and does not leave. It marks an achievement, not work. |
| Human task | 90 | Work a bank officer does. The case puts it in a queue or the officer picks it up. |
| Customer task | 6 | Work the customer, guarantor or heir does. The case waits on them. |
| Partner task | 22 | Work an outside party does, such as a law firm, agency, buyer or valuer. |
| Decision task | 22 | A point where a rule or an approver sets the route. The outcome selects the next sentry. |
| Stage entry | 10 | The task a stage starts from. One per stage. |
| Event listener | 53 | A task reached by an event rather than chosen, such as a declined approval or a blocked listing. |
| Sentry | 448 | One entry or exit criterion: the event it listens for, the condition that must hold, and the action it takes. Each sentry is one routing rule. |
| Case file item | 12 | Data the case holds. Sentries read it to test their conditions. |
| Starts: Automatic | 46 | The Workbench starts the task. No person starts it. |
| Starts: Discretionary | 40 | A person chooses whether to start the task. It has more than one way out. |
| Starts: Required | 64 | The case puts the task in a queue for a named owner. The delegation of authority decides who. |
| User sentry | 137 | Fired by a person's action or decision. |
| Timer sentry | 269 | Carries a time limit; fires when the time is reached if nothing else has. |
| System sentry | 42 | Fired by the Workbench or another system, with no time limit. |

## Sheet: Case status

| Case status |  |  |
|---|---|---|
| Eight statuses and the CMMN case state each maps to. |  |  |
| Status | Meaning | CMMN case state |
| New | Created at 90 days past due with its history. Not yet given an owner. | Active |
| Assigned | An owner and a queue are set by the allocation rules. The stage clock starts. | Active |
| In progress | The owner or the Workbench is working a task on the case. | Active |
| Waiting customer | An offer, notice or request is with the customer, with a validity timer running. | Active |
| Waiting partner | An instruction is with a partner, with a service level timer running. | Active |
| Waiting approval | A recommendation is with the approver set by the delegation of authority. | Active |
| On hold | A deviation or a legal hold has paused the case. The prescription clock keeps running. | Suspended |
| Closed | A milestone that closes the case is reached: cured, settled, sold, or written off with recovery ended. | Completed, then Closed |

## Sheet: Status transitions

| Status transitions |  |  |
|---|---|---|
| Every move between statuses. |  |  |
| From | Event | To |
| New | Allocation rule matched | Assigned |
| Assigned | Owner or Workbench starts the first task | In progress |
| In progress | Offer or notice sent to the customer | Waiting customer |
| In progress | Instruction sent to a partner | Waiting partner |
| In progress | Recommendation routed for approval | Waiting approval |
| Waiting customer | Customer responds, or the validity timer expires | In progress |
| Waiting partner | Partner result arrives, or the service level timer expires | In progress |
| Waiting approval | Approver accepts, changes or rejects, or the approval escalates | In progress |
| New, Assigned, In progress, any Waiting | Deviation flagged or legal hold placed | On hold |
| On hold | Deviation cleared or hold released | The status it paused in |
| In progress, Waiting customer, Waiting partner | A milestone that closes the case is reached | Closed |
| On hold | The deviation ends the case, for example insurance settles the debt | Closed |

## Sheet: Milestones

| Milestones |  |  |  |  |  |
|---|---|---|---|---|---|
| 30 milestones. |  |  |  |  |  |
| Milestone | Stage | Name | Detail | Closes the case | Reached by |
| PLAN_COMPLETED | Restructure | Plan completed | Collateral released, case closed | Yes | R-RES-33 |
| BACK_TO_ROUTE_DECISION | Restructure | Back to the route decision | With a coded reason | No | R-RES-03, R-RES-08, R-RES-14, R-RES-20, R-RES-30, R-RES-32, R-RES-37 |
| RESTRUCTURE_BARRED | Restructure | Restructure barred | R1 removed from the open routes | No | R-RES-31 |
| CASE_CLOSED_SETTLED | Settlement | Case closed | Title returned | Yes | R-SET-21 |
| RETURNED_TO_ROUTE_SET | Settlement | Back to the route decision | With a coded reason | No | R-SET-08, R-SET-11, R-SET-17, R-SET-19, R-SET-24, R-SET-27 |
| HANDED_TO_DISPOSAL | Deed in lieu | Handed to disposal | Route R5 takes the asset | No | R-DIL-33, R-DIL-34 |
| RETURNED_TO_ROUTE_DIL | Deed in lieu | Back to the route decision | With a coded reason | No | R-DIL-06, R-DIL-17, R-DIL-20, R-DIL-21, R-DIL-26, R-DIL-31, R-DIL-37 |
| TO_TREATMENT | Litigation | Back to treatment | Litigation canceled or held while the plan runs | Yes | R-LIT-13, R-LIT-75, R-LIT-79 |
| TO_ASSET_DISPOSAL | Litigation | To asset disposal | Asset onto the bank books after no bid | No | R-LIT-68 |
| TO_WRITE_OFF | Litigation | To write off | Unenforceable, or enforcement exhausted | No | R-LIT-49, R-LIT-57, R-LIT-60, R-LIT-62, R-LIT-71, R-LIT-77 |
| CASE_CLOSED | Litigation | Case closed | Debt satisfied, record retained after close | Yes | R-LIT-12, R-LIT-39, R-LIT-51, R-LIT-70, R-LIT-76 |
| RESIDUAL_TO_ROUTE | Guarantee claim | Residual to another route | Balance returns to the route decision at D6 | No | R-GUA-19, R-GUA-25, R-GUA-27, R-GUA-29, R-GUA-32 |
| GUARANTEE_CLOSED | Guarantee claim | Guarantee closed | No further claim on this guarantee | No | R-GUA-26, R-GUA-28 |
| ASSET_TRANSFERRED | Asset disposal | Transferred to RAMC | ASSET_TRANSFERRED | No | R-DIS-60 |
| CASE_CLOSED_NO_SHORTFALL | Asset disposal | Case closed, no shortfall | CASE_CLOSED_NO_SHORTFALL | Yes | R-DIS-56 |
| TO_DEBT_SALE | Asset disposal | To the debt sale route | TO_DEBT_SALE | No | R-DIS-46, R-DIS-58 |
| TO_WRITEOFF | Asset disposal | To the write-off route | TO_WRITEOFF | No | R-DIS-57, R-DIS-69 |
| LOT_CLOSED | Debt sale | Lot closed | LOT_CLOSED | No | R-DS-34, R-DS-39 |
| BACK_TO_CASE_LIST | Debt sale | Accounts back on the case list | BACK_TO_CASE_LIST | No | R-DS-03, R-DS-09, R-DS-37, R-DS-41 |
| RETURNED_TO_PURSUE | Write-off | Returned to the pursue track | RETURNED_TO_PURSUE | No | R-WO-14, R-WO-16 |
| CASE_CLOSED | Write-off | Case closed | CASE_CLOSED | Yes | R-WO-47, R-WO-50, R-WO-51 |
| RESUMED | Deviations | RESUMED | Back to the paused state | No | R-DEV-08, R-DEV-18 |
| ROUTE_D6 | Deviations | ROUTE_D6 | Back to the route decision | No | R-DEV-19 |
| CASE_ENDED | Deviations | CASE_ENDED | Insurance settles the debt | No | R-DEV-11 |
| RESUME_STATE | Universal rules | RESUME_STATE | Back to the state it paused in | No | R-UNI-12, R-UNI-21, R-UNI-23, R-UNI-24, R-UNI-32, R-UNI-35, R-UNI-38, R-UNI-40, R-UNI-42, R-UNI-43, R-UNI-44, R-UNI-46 |
| ROUTE_D6_REOPEN | Universal rules | ROUTE_D6_REOPEN | Segment recomputed, gates re-run | No | R-UNI-02, R-UNI-14, R-UNI-22, R-UNI-31, R-UNI-37, R-UNI-41, R-UNI-45, R-UNI-50 |
| CASE_CURED_CLOSED | Universal rules | CASE_CURED_CLOSED | Arrears cleared, case leaves recovery | Yes | R-UNI-01 |
| CASE_CLOSED_SOLD | Universal rules | CASE_CLOSED_SOLD | Debt sold or asset cleared the balance | Yes | R-UNI-47, R-UNI-48, R-UNI-49 |
| CANCELED_IN_ERROR | Universal rules | CANCELED_IN_ERROR | Case should never have existed | Yes | R-UNI-16 |
| MERGED | Universal rules | MERGED | Folded into the surviving case | Yes | R-UNI-17 |

## Sheet: Tasks

| Tasks |  |  |  |  |  |  |  |  |
|---|---|---|---|---|---|---|---|---|
| 150 tasks. |  |  |  |  |  |  |  |  |
| Task | Stage | Element | Starts | Name | Detail | Owner | Systems | Timer |
| ROUTE_APPROVED_RESTRUCTURE | Restructure | Stage entry | Automatic | Route approved | D6 sets route R1 | None | None | None |
| PROPOSED_IN_COLLINS | Restructure | Human task | Automatic | Proposed in COLLINS | Model returns the plan shape | Workbench | Workbench, COLLINS | None |
| IN_FCR_QUEUE | Restructure | Human task | Discretionary | In the FCR queue | Routed through EFS | Restructuring officer, FCR, FCR team manager | COLLINS, EFS, Workbench | 2 working days |
| WITH_FCR_OFFICER | Restructure | Human task | Discretionary | With the FCR officer | Restructuring officer builds the offer | Restructuring officer, FCR | EFS, Workbench, ACE and TDR | 2 working days |
| AFFORDABILITY_IN_ACE | Restructure | Human task | Automatic | Affordability in ACE | Plan calculated | ACE and TDR system | ACE and TDR, Workbench | 2 working days |
| AWAITING_CREDIT_APPROVAL | Restructure | Human task | Discretionary | Awaiting credit approval | Outside the range or a deviation | Credit approval committee, Head of credit | Workbench | 3 working days |
| OFFER_WITH_CUSTOMER | Restructure | Customer task | Discretionary | Offer with the customer | A wait with a validity timer | Customer, Deviation owner | Workbench, WIN and DMS, LINE, SMS | offer validity 14 days |
| WITH_OPS_BOOKING | Restructure | Human task | Discretionary | With operations | Booking to ALS and NLEADS | Operations (booking) | EasyApp e-signature, Workbench, NLEADS, ALS core | 1 working day, 2 working days |
| BOOKED_IN_ALS_NLEADS | Restructure | Human task | Automatic | Booked | Schedule and timers set | Workbench | ALS core, NLEADS | None |
| PLAN_RUNNING | Restructure | Human task | Discretionary | Plan running | Payments matched to installments | Restructuring officer, FCR, Workbench, Deviation owner | Workbench, ALS core | None |
| ROUTE_APPROVED_SETTLEMENT | Settlement | Stage entry | Automatic | Route approved | D6 sets route R2 | None | None | None |
| PAYOFF_AND_RANGE_SET | Settlement | Human task | Automatic | Payoff and range set | From ALS and reference data | Workbench | ALS core, Workbench | None |
| WITH_FCR_OFFICER_SET | Settlement | Human task | Discretionary | With the FCR officer | Negotiates inside the range | Restructuring officer, FCR | EFS, Workbench | 2 working days |
| AWAITING_APPROVAL_SET | Settlement | Human task | Required | Awaiting approval | Amount below the floor | Credit approval committee | Workbench | 3 working days |
| OFFER_WITH_CUSTOMER_SET | Settlement | Customer task | Discretionary | Offer with the customer | A wait with a validity timer | Customer, Deviation owner | Workbench, WIN and DMS, LINE, SMS | offer validity 14 days |
| WITH_OPS_SETTLEMENT | Settlement | Human task | Required | With operations | Agreement booked in ALS | Operations (booking) | EasyApp e-signature, Workbench | 1 working day |
| AWAITING_PAYMENT | Settlement | Customer task | Discretionary | Awaiting payment | Lump sum or installments | Customer, Case owner | ALS core, Workbench | payment due 30 days, 2 working days |
| PAYMENT_CLEARED | Settlement | Human task | Automatic | Payment cleared | Matched and posted | Workbench | ALS core, GL, Workbench | None |
| COLLATERAL_RELEASE_REQUESTED | Settlement | Human task | Automatic | Release requested | Account closed in ALS | Workbench, Case owner | ALS core, CCMS, the Workbench document hub | 5 working days |
| ROUTE_APPROVED_DIL | Deed in lieu | Stage entry | Automatic | Route approved | D6 sets route R3 | None | None | None |
| EARLY_READINESS_CHECK | Deed in lieu | Human task | Automatic | Early readiness check | Lead ranked, encumbrance tested | Workbench | Workbench, CCMS | 2 working days |
| VALUATION_ORDERED | Deed in lieu | Human task | Automatic | Valuation ordered | Fast lane or preliminary model | Workbench | CCMS, Land Office, Workbench, SCIS | None |
| AWAITING_VALUER | Deed in lieu | Partner task | Discretionary | Awaiting the valuer | Panel valuer through SVAF | Valuer, Partner and agency manager | SVAF, Partner Portal | panel service level |
| VALUATION_ACCEPTED | Deed in lieu | Human task | Automatic | Valuation accepted | Outliers flagged and cleared | Workbench, Case owner | Workbench, SVAF | 2 working days |
| WITH_FCR_OFFICER_DIL | Deed in lieu | Human task | Required | With the FCR officer | Negotiates the transfer | Restructuring officer, FCR | Workbench | 5 working days |
| TRANSFER_PRICE_SET | Deed in lieu | Human task | Automatic | Transfer price set | Governed template applied | Workbench | Workbench | None |
| AWAITING_SECOND_SIGNATURE | Deed in lieu | Human task | Required | Awaiting second signature | Price below the floor | Head of NPA | Workbench | 3 working days |
| OFFER_WITH_CUSTOMER_DIL | Deed in lieu | Customer task | Discretionary | Offer with the customer | Wet ink for mortgage per Legal | Customer | the Workbench document hub, WIN and DMS, Workbench | offer validity 14 days |
| WITH_FIELD_INSPECTION | Deed in lieu | Human task | Required | Field inspection | Checklist, photographs, bills | Field officer or agency field team | Field App, Workbench, RPS | 5 working days |
| ASSET_UNLOCK_DECISION | Deed in lieu | Decision task | Automatic | Asset unlock rule | About 95% auto-unlock | Workbench | Field App, Workbench | None |
| AWAITING_APPROVER_SUMMARY | Deed in lieu | Human task | Required | Approver summary | The rest go to the approver | Head of NPA | Workbench | 3 working days |
| AWAITING_TRANSFER | Deed in lieu | Partner task | Discretionary | Awaiting transfer | Land Office or SCIS | Customer | Workbench, Land Office, SCIS | None |
| ASSET_ON_BOOKS | Deed in lieu | Human task | Automatic | Asset on the books | AMIS recorded, debt settled | Workbench | Land Office, AMIS, ALS core, CCMS, SCIS | None |
| RENTAL_RUNNING | Deed in lieu | Human task | Required | Rental running | Auto-debit through ATS | Case owner | ATS, AMIS, Workbench | None |
| LIT_ROUTE_APPROVED | Litigation | Stage entry | Automatic | Litigation approved | D6.3, or a broken treatment returns the case | None | None | None |
| NOTICE_GENERATED | Litigation | Human task | Automatic | Notice generated | The rules pick the Legal template by product and notice type | Workbench | Workbench, Workbench scheduler, EFS, Rules component, the Workbench document hub | Same day, 1 working day |
| NOTICE_DISPATCHED | Litigation | Human task | Automatic | Notice dispatched | WIN and DMS print, courier and capture proof | Workbench | Rules component, letter engine, the Workbench document hub, WIN and DMS, NCB | 1 working day, 3 working days |
| WITH_CUSTOMER_NOTICE_PERIOD | Litigation | Customer task | Discretionary | Notice period running | Timer runs from proof of delivery, not the print date | Customer | WIN and DMS, Workbench | Notice period by product and type |
| PACK_ASSEMBLY | Litigation | Human task | Discretionary | Pack assembled | Legal document agent builds from case, CCMS, LHS and the Workbench document hub | Head of Litigation, Workbench | Workbench, Workbench scheduler, Document Hub, the Workbench document hub | To the prescription date, 3 working days, 1 working day |
| PACK_VERIFIED | Litigation | Human task | Required | Pack verified | Litigation officer approves filing, first-time-right recorded | Litigation officer, Head of Litigation | Document Hub, CCMS, LHS, the Workbench document hub, Workbench, Workbench scheduler | 2 working days, 10 working days, To the prescription date |
| FIRM_SELECTION | Litigation | Decision task | Automatic | Firm selected by rule | Panel scorecard by court region and case type, conflict check | Workbench | Rules component, partner performance data | Same day |
| FIRM_ESCALATED | Litigation | Human task | Required | No firm available | Head of Litigation nominates or widens the panel | Head of Litigation | Workbench | 2 working days |
| FIRM_INSTRUCTED | Litigation | Partner task | Required | Firm instructed | Instruction and pack through the Partner Portal | Panel law firm | Partner Portal, Rules component | 2 working days |
| FILED_IN_COURT | Litigation | Partner task | Required | Filed in court | Firm uploads the receipt and the court case number | Panel law firm | Partner Portal, court e-filing, LIT | Filing service level by task |
| IN_HEARING | Litigation | Partner task | Discretionary | In hearing | Case tracking agent holds the calendar and the timers | Panel law firm, Litigation officer | LIT, Partner Portal, Workbench scheduler, Workbench, Committee View, ALS core and GL | To the hearing date, To the new date, 5 working days |
| SETTLEMENT_OFFERED_AT_COURT | Litigation | Decision task | Required | Settlement offered | D7.4. Agent proposes, approver decides | Approver at D7.4 | Workbench, Committee View | 3 working days |
| LITIGATION_HELD | Litigation | Human task | Required | Litigation held | Case not withdrawn while the treatment runs | Restructuring officer, FCR | Workbench, ALS core | 2 working days |
| JUDGMENT_RECORDED | Litigation | Human task | Required | Judgment recorded | Date and amount written to the Legal Action | Enforcement owner | LIT, Partner Portal | 5 working days |
| APPEAL_DECISION | Litigation | Decision task | Required | Appeal decision | D7.4. Approver inside the limit, Head of Litigation above it | Approver at D7.4 | Workbench, Committee View | To the window end |
| APPEAL_FILED | Litigation | Partner task | Required | Appeal filed | Firm files, hearing timers reset | Panel law firm | Partner Portal, LIT | To the filing deadline |
| LEGAL_SPEND_APPROVAL | Litigation | Decision task | Required | Legal spend approval | D7.4. Court fees and legal expenses | Approver at D7.4 | Workbench, Committee View | 3 working days |
| ASSET_TRACE | Litigation | Human task | Automatic | Assets traced | NCB, internal data, registries and insurers | Workbench | NCB, registries, insurers | 10 working days |
| ENFORCEMENT_DECISION | Litigation | Decision task | Discretionary | Enforce or defer | D7.5. Enforcement owner decides, a deferral needs a code | Enforcement owner | Workbench, Workbench scheduler, Partner Portal | 5 working days, 10 working days |
| WRIT_AND_SEIZURE | Litigation | Partner task | Required | Writ and seizure | Firm applies, the LED executes | Panel law firm | Partner Portal, LED | To the writ deadline |
| LED_AUCTION | Litigation | Partner task | Required | LED auction | Rounds at 100, 90, 80 then 70 percent of official value | Legal Execution Department | Partner Portal, LED | To the auction date, To the next auction date |
| PROCEEDS_MATCHED | Litigation | Human task | Automatic | Proceeds matched | Reconciliation agent posts to ALS against the case | Workbench, Case owner | ALS core and GL, LED, ALS core, Workbench | 2 working days, 1 working day |
| BANKRUPTCY_PETITION | Litigation | Decision task | Required | Bankruptcy petition | D7.5. Agent prepares, the approver approves | Approver at D7.5 | Workbench, Committee View | 5 working days |
| OFFICIAL_RECEIVER_CLAIM | Litigation | Partner task | Required | Claim with the official receiver | Filed before the receiver deadline | Official receiver, Legal | Partner Portal, courts, Workbench | To the filing deadline, To the receiver deadline |
| GUARANTEE_DETECTED | Guarantee claim | Stage entry | Automatic | Guarantee detected | Found on the case at takeover in stage 06 | None | None | None |
| DEADLINE_TIMER_RUNNING | Guarantee claim | Human task | Automatic | Claim deadline running | Timer set from the date the default conditions are met | Workbench | Workbench, Workbench scheduler, ALS core | To the claim deadline |
| CLAIM_PREPARATION | Guarantee claim | Human task | Automatic | Claim assembled | Claim preparation agent builds it against the scheme checklist | Workbench | Workbench, Document Hub | 5 working days, 1 working day, 2 working days |
| CLAIM_APPROVAL | Guarantee claim | Human task | Required | Officer approves the claim | Guarantee officer verifies at D6.5 | Guarantee officer, Head of Litigation | Document Hub, Workbench, Workbench scheduler | 3 working days, To the claim deadline |
| CLAIM_SUBMITTED | Guarantee claim | Partner task | Discretionary | Claim submitted | Through the TCG claim channel | TCG | Workbench, TCG claim channel | 2 working days, 5 working days |
| GUARANTOR_NOTICE | Guarantee claim | Customer task | Discretionary | Guarantor noticed | D6.6 notice with proof of delivery | Guarantor, Case owner | WIN and DMS, Workbench | Notice period by product |
| CLAIM_PART_PAID | Guarantee claim | Human task | Automatic | Part paid | Payment matched with source TCG | Workbench | ALS core and GL | 2 working days |
| CLAIM_PAID | Guarantee claim | Human task | Automatic | Paid to the guaranteed share | Relief schemes cover up to 50 percent of principal | Workbench | ALS core and GL | 2 working days |
| SUBROGATION_POSITION | Guarantee claim | Human task | Discretionary | Subrogation recorded | TCG holds a share of every later recovery | Guarantee officer | Workbench, ALS core | None |
| ASSET_PENDING_TAKE_ON | Asset disposal | Stage entry | Automatic | Asset pending take-on | ASSET_PENDING_TAKE_ON | Workbench | WIN and DMS, Document Hub | None |
| ASSET_ON_BOOKS | Asset disposal | Human task | Discretionary | Asset record created | ASSET_ON_BOOKS | Sale officer | RPS, AMIS, Field App, integration adapters, the Land Office, the Legal Execution Department | 1 working day |
| ASSET_HELD | Asset disposal | Human task | Discretionary | Asset held | ASSET_HELD | Sale officer, Workbench | Workbench, Finance provision feed, CCMS, the Land Office, SCIS, ALS core and GL, Partner Portal, LIT, SVAF, Decision Log, ATS | 3 working days, 2 working days |
| WORK_ORDER_OPEN | Asset disposal | Partner task | Required | Work order with the vendor | WORK_ORDER_OPEN | Property services vendor | Partner Portal | per fee schedule |
| EVICTION_REQUIRED | Asset disposal | Human task | Required | Eviction instructed | EVICTION_REQUIRED | Litigation officer | LIT, Partner Portal | None |
| REAPPRAISAL_ORDERED | Asset disposal | Partner task | Required | Re-appraisal ordered | REAPPRAISAL_ORDERED | Valuer | SVAF, integration adapters, Decision Log | 10 working days |
| REAPPRAISAL_RECEIVED | Asset disposal | Human task | Required | Value reported | REAPPRAISAL_RECEIVED | Sale officer | SVAF, Agent Runtime | 2 working days |
| ROUTE_RECOMMENDED | Asset disposal | Human task | Required | Disposal route recommended | ROUTE_RECOMMENDED | Sale officer | Agent Runtime, COLLINS, Case Workspace, Partner Portal | 2 working days |
| ROUTE_WITH_APPROVER | Asset disposal | Decision task | Discretionary | With the approver | ROUTE_WITH_APPROVER | Sale officer | Rules component, Committee View | 2 working days |
| ROUTE_APPROVED_AUCTION | Asset disposal | Human task | Required | Auction route approved | ROUTE_APPROVED_AUCTION | Sale officer, Committee | Case Workspace, Decision Log, Committee View | None |
| ROUTE_APPROVED_RAMC | Asset disposal | Human task | Required | RAMC route approved | ROUTE_APPROVED_RAMC | Sale officer | Calculation Service, Committee View | None |
| ROUTE_APPROVED_BUYBACK | Asset disposal | Human task | Discretionary | Buy-back route approved | ROUTE_APPROVED_BUYBACK | Sale officer | Calculation Service, Case Workspace | None |
| RENTAL_ACTIVE | Asset disposal | Human task | Required | Asset rented | RENTAL_ACTIVE | Sale officer | ATS, integration adapters | None |
| BROKER_INSTRUCTED | Asset disposal | Partner task | Discretionary | Broker instructed | BROKER_INSTRUCTED | Broker | Partner Portal | per instruction term |
| PRICE_PROPOSED | Asset disposal | Human task | Required | Opening and floor price proposed | PRICE_PROPOSED | Sale officer | Agent Runtime, COLLINS | 1 working day |
| FLOOR_APPROVED | Asset disposal | Decision task | Automatic | Floor approved | FLOOR_APPROVED | Workbench | Rules component | None |
| VENDOR_ALLOCATED | Asset disposal | Partner task | Required | Vendor allocated on the scorecard | VENDOR_ALLOCATED | Auction and remarketing vendor, Partner and agency manager | Rules component, Partner Portal | 2 working days |
| LISTING_LIVE | Asset disposal | Human task | Required | Listing live | LISTING_LIVE | Auction and remarketing vendor, Workbench | Partner Portal, auction portal, HOME.SCB, Document Hub | 2 working days, per asset class |
| ROUND_OPEN | Asset disposal | Human task | Required | Round open at the price step | ROUND_OPEN | Auction and remarketing vendor, Workbench | auction portal, Workbench scheduler, Rules component | per schedule |
| BID_RECEIVED | Asset disposal | Human task | Automatic | Bid received | BID_RECEIVED | Workbench | auction portal | None |
| SECOND_SIGNATURE_PENDING | Asset disposal | Decision task | Discretionary | Second signature pending | SECOND_SIGNATURE_PENDING | Committee | Committee View | 2 working days |
| RELISTED | Asset disposal | Human task | Required | Re-listed | RELISTED | Sale officer | Workbench, Decision Log, SVAF | None |
| SALE_AGREED | Asset disposal | Human task | Required | Sale agreed | SALE_AGREED | Sale officer | Case Workspace, auction portal, Decision Log, Calculation Service, ALS core and GL, Partner Portal | 1 working day |
| AWAITING_PAYMENT | Asset disposal | Partner task | Discretionary | Awaiting payment, five days | AWAITING_PAYMENT | Buyer | auction portal, ALS core and GL | 5 calendar days |
| TITLE_TRANSFER_PENDING | Asset disposal | Human task | Discretionary | Title transfer pending | TITLE_TRANSFER_PENDING | Sale officer | ALS core and GL, integration adapters | None |
| ASSET_SOLD | Asset disposal | Human task | Automatic | Asset sold and transferred | ASSET_SOLD | Workbench, Sale officer | SCIS, integration adapters, the Land Office, Document Hub | 5 working days, 10 working days |
| RAMC_TRANSFER_PENDING | Asset disposal | Partner task | Required | RAMC transfer pending | RAMC_TRANSFER_PENDING | RAMC | Partner Portal, Calculation Service | per agreement |
| PROCEEDS_APPLIED | Asset disposal | Human task | Automatic | Proceeds applied to the case | PROCEEDS_APPLIED | Workbench | ALS core and GL, Agent Runtime | same day |
| SHORTFALL_RAISED | Asset disposal | Human task | Discretionary | Shortfall raised | SHORTFALL_RAISED | Write-off team | Rules component | None |
| LOT_CANDIDATE_SELECTED | Debt sale | Stage entry | Automatic | Candidate accounts selected | LOT_CANDIDATE_SELECTED | None | None | None |
| LOT_BUILT | Debt sale | Human task | Discretionary | Lot built and priced | LOT_BUILT | Debt sale officer | Rules component, Recovery Data Store, Workbench | per monthly cycle |
| LOT_WITH_COMMITTEE | Debt sale | Decision task | Discretionary | Lot with the committee | LOT_WITH_COMMITTEE | Committee | Agent Runtime, COLLINS, Case Workspace, Committee View | 5 working days |
| LOT_APPROVED | Debt sale | Human task | Required | Lot, reserve and terms approved | LOT_APPROVED | Debt sale officer | Committee View, Decision Log | None |
| TAPE_PREPARED | Debt sale | Human task | Automatic | Masked data tape prepared | TAPE_PREPARED | Workbench | PII service, Recovery Data Store, Document Hub | 3 working days |
| DATA_ROOM_OPEN | Debt sale | Human task | Required | Data room open | DATA_ROOM_OPEN | Debt sale officer | buyer portal, Document Hub | per cycle |
| BUYER_PENDING_KYC | Debt sale | Decision task | Automatic | Buyer pending KYC | BUYER_PENDING_KYC | Workbench, Debt sale officer | Rules component, buyer portal, Buyer portal, Workbench | 3 working days, 10 working days |
| BUYER_CLEARED | Debt sale | Partner task | Required | Buyer cleared | BUYER_CLEARED | Buyer | buyer portal | None |
| BIDDING_OPEN | Debt sale | Partner task | Required | Bidding open | BIDDING_OPEN | Buyer | buyer portal, Committee View | per cycle |
| BIDS_RECEIVED | Debt sale | Human task | Automatic | Bids received | BIDS_RECEIVED | Workbench | buyer portal | None |
| AWARD_PENDING | Debt sale | Decision task | Required | Award pending confirmation | AWARD_PENDING | Debt sale officer | Case Workspace, Committee View | 2 working days |
| LOT_AWARDED | Debt sale | Human task | Required | Lot awarded | LOT_AWARDED | Debt sale officer | Document Hub, buyer portal | None |
| SETTLEMENT_PENDING | Debt sale | Partner task | Discretionary | Settlement pending | SETTLEMENT_PENDING | Buyer | buyer portal, ALS core and GL | per agreed settlement period |
| SETTLED | Debt sale | Human task | Automatic | Buyer settled | SETTLED | Workbench | ALS core and GL, integration adapters | None |
| DATA_TRANSFERRED | Debt sale | Human task | Automatic | Account data transferred | DATA_TRANSFERRED | Workbench | integration adapters, buyer portal | 5 working days |
| DERECOGNISED | Debt sale | Human task | Automatic | Balance derecognised | DERECOGNISED | Workbench | ALS core and GL, integration adapters | None |
| GL_POSTED | Debt sale | Human task | Discretionary | Posted to the general ledger | GL_POSTED | Credit Administration | ALS core and GL, Finance provision feed, integration adapters | month-end close |
| PUTBACK_RAISED | Debt sale | Partner task | Discretionary | Put-back claim raised | PUTBACK_RAISED | Debt sale officer | buyer portal, Decision Log | 10 working days |
| PUTBACK_UPHELD | Debt sale | Human task | Required | Put-back upheld | PUTBACK_UPHELD | Debt sale officer | ALS core and GL, buyer portal | None |
| PUTBACK_REFUSED | Debt sale | Human task | Required | Put-back refused | PUTBACK_REFUSED | Debt sale officer | Decision Log, buyer portal | None |
| SCAN_DUE | Write-off | Stage entry | Automatic | Monthly scan due | SCAN_DUE | Workbench, Write-off team | integration adapters, Reference data, Workbench, Workbench scheduler, Decision Log | next cut-off |
| POPULATION_PROPOSED | Write-off | Human task | Discretionary | Population proposed | POPULATION_PROPOSED | Write-off team | Rules component, COLLINS, ALS core and GL | monthly cut-off |
| PACK_PREPARED | Write-off | Human task | Discretionary | Write-off pack prepared | PACK_PREPARED | Write-off team | Agent Runtime, Document Hub | 3 working days |
| WITH_COMMITTEE | Write-off | Decision task | Discretionary | With the write-off committee | WITH_COMMITTEE | Write-off committee | Case and Workflow Service, Committee View, Workbench scheduler | before the scheduled meeting |
| ESCALATED_TO_CREDIT_COMMITTEE | Write-off | Decision task | Discretionary | Above the limit, credit committee | ESCALATED_TO_CREDIT_COMMITTEE | Credit approval committee | Committee View, Reference data | before the scheduled meeting |
| APPROVED | Write-off | Human task | Required | Approved | APPROVED | Credit Administration | Committee View, Decision Log | None |
| POSTING_PENDING | Write-off | Human task | Discretionary | Posting pending | POSTING_PENDING | Credit Administration | Workbench scheduler, ALS core and GL, integration adapters | month-end close window, to confirm with Credit Administration |
| POSTED | Write-off | Human task | Required | Posted to ALS and the GL | POSTED | Credit Administration | ALS core and GL, integration adapters | None |
| PROVISION_RELEASED | Write-off | Human task | Automatic | Provision released | PROVISION_RELEASED | Workbench | Rules component, ALS core and GL | None |
| FINANCE_FEED_SENT | Write-off | Human task | Required | Finance feed sent | FINANCE_FEED_SENT | Credit Administration | Finance provision feed, integration adapters | month-end close |
| PLACEMENT_DECIDED | Write-off | Decision task | Required | Post charge-off treatment decided | PLACEMENT_DECIDED | Partner and agency manager | Rules component, Partner Portal | 5 working days |
| PLACED_WITH_AGENCY | Write-off | Partner task | Required | Placed with an agency | PLACED_WITH_AGENCY | Outsourced agency | Partner Portal, OA portal | same day on the portal, same day |
| SOLD_POST_CHARGEOFF | Write-off | Partner task | Discretionary | Sold to a buyer | SOLD_POST_CHARGEOFF | Debt sale officer | buyer portal, Workbench | per cycle |
| PAYMENT_MATCHED | Write-off | Human task | Automatic | Payment matched and posted | PAYMENT_MATCHED | Workbench | ALS core and GL, Agent Runtime, integration adapters | next working day |
| REMITTED_TO_BUYER | Write-off | Human task | Required | Remitted to the buyer | REMITTED_TO_BUYER | Debt sale officer | ALS core and GL, buyer portal | 5 working days |
| RETENTION_RUNNING | Write-off | Human task | Automatic | Retention timer running | RETENTION_RUNNING | Workbench, Operational Excellence | Partner Portal, Workbench scheduler, Rules component, Power BI, Document Hub | monthly, 5 working days |
| ANY_STATE | Deviations | Stage entry | Automatic | Any active state | The case is on a route | None | None | None |
| DEV_FLAGGED | Deviations | Human task | Automatic | DEV_FLAGGED | Screening agent flags with reasons | Workbench | Workbench, the Workbench document hub | same day |
| DEV_WITH_OWNER | Deviations | Human task | Discretionary | DEV_WITH_OWNER | Complaint officer, specialist, fraud team or Legal | Complaint officer, Specialist, Legal, Fraud team, Legal, Agent, case owner, Team manager | Workbench, Aric, LIT | deadline driven, 10 working days, same day |
| DEV_REJECTED | Deviations | Human task | Automatic | DEV_REJECTED | Owner clears the flag as not a deviation | Workbench | Workbench | None |
| DEV_RESOLVED | Deviations | Human task | Required | DEV_RESOLVED | Outcome recorded, clock resumes | Case owner | Workbench, NCB | None |
| DEV_REROUTE | Deviations | Decision task | Required | DEV_REROUTE | The outcome changes the route | Restructuring officer, Case owner, Write-off team, Legal, litigation officer | Workbench, Aric, EFS, LIT | 30 days, 2 working days |
| ANY_ACTIVE | Universal rules | Stage entry | Automatic | ANY_ACTIVE | Any non-terminal state on any route | None | None | None |
| CUSTOMER_EVENT | Universal rules | Decision task | Required | CUSTOMER_EVENT | The customer or a connected party acts | None | None | None |
| BANK_EVENT | Universal rules | Decision task | Required | BANK_EVENT | The bank acts on the case itself | None | None | None |
| PARTNER_EVENT | Universal rules | Decision task | Required | PARTNER_EVENT | A partner fails, exits or conflicts | None | None | None |
| SYSTEM_EVENT | Universal rules | Decision task | Required | SYSTEM_EVENT | A timer, an interface or the data | None | None | None |
| PORTFOLIO_EVENT | Universal rules | Decision task | Required | PORTFOLIO_EVENT | The debt or the asset leaves the book | None | None | None |
| HELD_DEVIATION | Universal rules | Human task | Required | HELD_DEVIATION | Stage clock paused, deviation owner holds it | Complaint officer, Specialist, Legal, Specialist, Legal, Fraud team | Workbench, the Workbench document hub, LIT, Aric | same day, deadline driven |
| HELD_LEGAL | Universal rules | Human task | Required | HELD_LEGAL | Regulatory or legal freeze, no action out | Compliance, Risk, Legal | Workbench, ACE | statutory period, scheme terms, until lifted |
| HELD_CONDUCT | Universal rules | Human task | Required | HELD_CONDUCT | Contact stop applied | Conduct and QA officer | Workbench | same day |
| ESCALATED | Universal rules | Human task | Required | ESCALATED | Named escalation point, case does not move | Approver per the matrix, Team manager | Workbench | 1 working day, per state |
| REALLOCATED | Universal rules | Human task | Required | REALLOCATED | New owner, same state | Team manager | Workbench | 1 working day, weekly |
| PARTNER_RECALLED | Universal rules | Human task | Required | PARTNER_RECALLED | Work pulled back, partner re-selected | Partner and agency manager, Head of the partner type | Partner Portal, Workbench | per partner type, 5 working days, 2 working days, same day |

## Sheet: Event listeners

| Event listeners |  |  |  |  |  |  |
|---|---|---|---|---|---|---|
| 53 event listeners. |  |  |  |  |  |  |
| Listener | Stage | Name | Detail | Owner | Reached by | Leaves by |
| DECLINED_BY_CREDIT | Restructure | Declined by credit | Reason recorded | Restructuring officer, FCR | R-RES-12 | R-RES-14 |
| RETURNED_TO_COLLINS | Restructure | Returned to COLLINS | Prior status restored | Workbench | R-RES-17, R-RES-18 | R-RES-20 |
| PLAN_CURE_PERIOD | Restructure | In the cure period | An installment was missed | Case owner | R-RES-27 | R-RES-28, R-RES-29 |
| PLAN_BROKEN | Restructure | Plan broken | Break count incremented | Case owner | R-RES-29 | R-RES-30, R-RES-31, R-RES-36 |
| UNMATCHED_EXCEPTION | Restructure | UNMATCHED_EXCEPTION | No rule matched. Held for a person. | Case owner | R-RES-35, R-RES-36 | R-RES-37 |
| DECLINED_BY_APPROVER_SET | Settlement | Approval refused | Reason recorded | Restructuring officer, FCR | R-SET-07 | R-SET-08 |
| PAYMENT_PART_RECEIVED | Settlement | Part received | Balance still due | Workbench | R-SET-15 | R-SET-18, R-SET-19 |
| PAYMENT_REVERSED | Settlement | Payment reversed | After release | Case owner | R-SET-23 | R-SET-24 |
| UNMATCHED_EXCEPTION | Settlement | UNMATCHED_EXCEPTION | No rule matched. Held for a person. | Case owner | R-SET-25, R-SET-26 | R-SET-27 |
| ENCUMBRANCE_BLOCKED | Deed in lieu | Encumbrance unresolved | Transfer blocked | Case owner | R-DIL-04 | R-DIL-05, R-DIL-06 |
| TITLE_NOT_CLEAN | Deed in lieu | Title not clean | Transfer held | Case owner | R-DIL-29 | R-DIL-30, R-DIL-31 |
| UNMATCHED_EXCEPTION | Deed in lieu | UNMATCHED_EXCEPTION | No rule matched. Held for a person. | Case owner | R-DIL-35, R-DIL-36 | R-DIL-37 |
| DEVIATION_HOLD | Litigation | Deviation hold | X1 to X7. Timers pause, prescription keeps running | Complaint officer, Named deviation approver | R-LIT-14, R-LIT-73 | R-LIT-74, R-LIT-75, R-LIT-76, R-LIT-77, R-LIT-78, R-LIT-79 |
| NOTICE_BLOCKED | Litigation | Notice blocked | Template withdrawn, or a contact stop applies | Litigation officer, Conduct and QA officer | R-LIT-04, R-LIT-05, R-LIT-22 | R-LIT-06 |
| NOTICE_UNSERVED | Litigation | Notice unserved | No proof returned, refused or undeliverable | Litigation officer | R-LIT-08, R-LIT-09 | R-LIT-10, R-LIT-11 |
| PACK_DEFECT_HOLD | Litigation | Pack held on a defect | An item on the defect list is missing | Litigation officer | R-LIT-17 | R-LIT-18, R-LIT-19, R-LIT-20 |
| FIRM_DECLINED | Litigation | Firm declined or breached | Re-select the next firm on the scorecard | Workbench, Partner and agency manager | R-LIT-27, R-LIT-28 | R-LIT-29 |
| FILING_REJECTED | Litigation | Court rejected the filing | Defect recorded, pack reworked | Litigation officer | R-LIT-31 | R-LIT-32 |
| HEARING_ADJOURNED | Litigation | Hearing adjourned | Timer reset, postpone reason coded | Panel law firm | R-LIT-34 | R-LIT-35 |
| JUDGMENT_DISMISSED | Litigation | Dismissed or lost | Appeal window opens | Litigation officer | R-LIT-45 | R-LIT-46 |
| DEFERRAL_RECORDED | Litigation | Deferral recorded | Coded reason and a review date re-queue the case | Enforcement owner | R-LIT-55 | R-LIT-56, R-LIT-57 |
| NO_BID_AT_70 | Litigation | No bid at 70 percent | The ladder is exhausted | Enforcement owner | R-LIT-67 | R-LIT-68, R-LIT-69 |
| NOT_ELIGIBLE | Guarantee claim | Not eligible | Scheme default conditions not met | Guarantee officer | R-GUA-02 | R-GUA-03 |
| CLAIM_DEFECT_HOLD | Guarantee claim | Claim held on a defect | A checklist item is missing | Guarantee officer | R-GUA-08 | R-GUA-10, R-GUA-11 |
| TCG_QUERY | Guarantee claim | TCG query | More information requested before assessment | Guarantee officer | R-GUA-14 | R-GUA-15, R-GUA-16 |
| CLAIM_REJECTED | Guarantee claim | Claim rejected | Rejection reason recorded against the guarantee | Guarantee officer | R-GUA-16, R-GUA-17 | R-GUA-18, R-GUA-19 |
| GUARANTOR_DISPUTE_HOLD | Guarantee claim | Guarantor dispute | X1 raised against the guarantee itself | Complaint officer | R-GUA-30 | R-GUA-31, R-GUA-32 |
| DEADLINE_MISSED | Guarantee claim | Claim deadline missed | The claim is lost. Loss, reason and amount recorded | Guarantee officer | R-GUA-05, R-GUA-09 | R-GUA-27 |
| FAILED_NOTICE_QUEUE | Asset disposal | Failed notice queue | FAILED_NOTICE_QUEUE | Sale officer | R-DIS-04 | R-DIS-05 |
| TITLE_BLOCKED | Asset disposal | Title or registration blocked | TITLE_BLOCKED | Sale officer | R-DIS-07, R-DIS-53 | R-DIS-08 |
| DISPOSAL_PAUSED_DEVIATION | Asset disposal | Paused on a deviation | DISPOSAL_PAUSED_DEVIATION | Deviation owner | R-DIS-66, R-DIS-67 | R-DIS-68, R-DIS-69 |
| LISTING_BLOCKED | Asset disposal | Listing blocked on evidence | LISTING_BLOCKED | Sale officer | R-DIS-34 | R-DIS-35 |
| NO_BID_AT_FLOOR | Asset disposal | Floor reached with no bid | NO_BID_AT_FLOOR | Sale officer | R-DIS-39 | R-DIS-44, R-DIS-46 |
| AWARD_CANCELED | Asset disposal | Award canceled | AWARD_CANCELED | Sale officer | R-DIS-49 | R-DIS-50 |
| UNMATCHED_EXCEPTION | Asset disposal | UNMATCHED_EXCEPTION | No rule matched. Held for a person. | Sale officer | R-DIS-70, R-DIS-71 | R-DIS-72 |
| CASE_EXCLUDED | Debt sale | Account excluded | CASE_EXCLUDED | Case owner | R-DS-02 | R-DS-03 |
| LOT_WITHDRAWN | Debt sale | Lot withdrawn | LOT_WITHDRAWN | Debt sale officer | R-DS-08, R-DS-22 | R-DS-09 |
| TAPE_REJECTED | Debt sale | Tape rejected on masking | TAPE_REJECTED | Workbench | R-DS-11 | R-DS-12 |
| BUYER_REJECTED | Debt sale | Buyer refused | BUYER_REJECTED | Debt sale officer | R-DS-16 | R-DS-40, R-DS-41 |
| BID_BELOW_RESERVE | Debt sale | Best bid below the reserve | BID_BELOW_RESERVE | Debt sale officer | R-DS-20 | R-DS-21, R-DS-22 |
| AWARD_CANCELED_DS | Debt sale | Award canceled | AWARD_CANCELED_DS | Debt sale officer | R-DS-26, R-DS-27 | R-DS-28 |
| POSTING_REJECTED_DS | Debt sale | Posting rejected | POSTING_REJECTED_DS | Credit Administration | R-DS-32 | R-DS-33 |
| SCAN_HELD | Write-off | Scan held | SCAN_HELD | Write-off team | R-WO-02, R-WO-03 | R-WO-04 |
| CASE_REMOVED_BY_TEAM | Write-off | Case removed with a reason | CASE_REMOVED_BY_TEAM | Deviation owner, Write-off team | R-WO-06, R-WO-07 | R-WO-08 |
| PACK_INCOMPLETE | Write-off | Pack incomplete | PACK_INCOMPLETE | Write-off team | R-WO-09 | R-WO-10 |
| DEFERRED | Write-off | Deferred with a review date | DEFERRED | Write-off team | R-WO-17 | R-WO-19 |
| POSTING_REJECTED | Write-off | Posting rejected | POSTING_REJECTED | Credit Administration | R-WO-22 | R-WO-23, R-WO-24 |
| FINANCE_FEED_REJECTED | Write-off | Finance feed rejected | FINANCE_FEED_REJECTED | Credit Administration | R-WO-27 | R-WO-28 |
| PLACEMENT_RECALLED | Write-off | Placement recalled | PLACEMENT_RECALLED | Partner and agency manager | R-WO-34 | R-WO-35 |
| PAYMENT_EXCEPTION | Write-off | Payment on the exception list | PAYMENT_EXCEPTION | Case owner | R-WO-38 | R-WO-39 |
| WRITEOFF_EXCEPTION | Write-off | Write-off exception, owner to confirm | WRITEOFF_EXCEPTION | Owner to confirm with C&R | R-WO-24, R-WO-41, R-WO-43 | R-WO-44, R-WO-45, R-WO-46 |
| EXCEPTION_QUEUE | Universal rules | EXCEPTION_QUEUE | A person decides, the gap is logged | Case owner, Platform team | R-UNI-03, R-UNI-34, R-UNI-36, R-UNI-39 | R-UNI-41 |
| RETRY_QUEUE | Universal rules | RETRY_QUEUE | Automatic retry, then the exception queue | Platform team | R-UNI-33 | R-UNI-35, R-UNI-36 |

## Sheet: Sentries

| Sentries |  |  |  |  |  |  |  |  |  |  |
|---|---|---|---|---|---|---|---|---|---|---|
| 448 sentries. Each sentry is one routing rule. |  |  |  |  |  |  |  |  |  |  |
| Sentry | Stage | Kind | From | On event | If | Then | To | Target | Owner | Timer |
| R-RES-01 | Restructure | System sentry | ROUTE_APPROVED_RESTRUCTURE | ROUTE_APPROVED | decision.approved and route = R1 | Open the treatment record and ask COLLINS for the restructure proposal | PROPOSED_IN_COLLINS | Human task | Workbench | None |
| R-RES-02 | Restructure | Timer sentry | PROPOSED_IN_COLLINS | RESTRUCTURE_PROPOSED | collins_proposal = eligible | Route the case through EFS into the FCR queue | IN_FCR_QUEUE | Human task | Restructuring officer, FCR | 2 working days |
| R-RES-03 | Restructure | User sentry | PROPOSED_IN_COLLINS | NO_PROPOSAL_RETURNED | collins_proposal = none | Return the case to the route decision with reason no_restructure_option | BACK_TO_ROUTE_DECISION | Milestone | Case owner | None |
| R-RES-04 | Restructure | Timer sentry | IN_FCR_QUEUE | CASE_PICKED_UP | allocation rule matched and officer available | Assign the case to a restructuring officer and start the offer clock | WITH_FCR_OFFICER | Human task | Restructuring officer, FCR | 2 working days |
| R-RES-05 | Restructure | Timer sentry | IN_FCR_QUEUE | QUEUE_SLA_BREACHED | queue_age > fcr_queue_limit | Escalate to the FCR team manager and re-allocate | IN_FCR_QUEUE | Human task | FCR team manager | None |
| R-RES-06 | Restructure | Timer sentry | WITH_FCR_OFFICER | AFFORDABILITY_REQUIRED | treatment_type = TDR | Send the case to ACE for affordability and plan calculation | AFFORDABILITY_IN_ACE | Human task | ACE and TDR system | 2 working days |
| R-RES-07 | Restructure | User sentry | AFFORDABILITY_IN_ACE | AFFORDABILITY_PASSED | affordability_result = pass | Return the calculated plan to the officer and build the offer | WITH_FCR_OFFICER | Human task | Restructuring officer, FCR | None |
| R-RES-08 | Restructure | User sentry | AFFORDABILITY_IN_ACE | AFFORDABILITY_FAILED | affordability_result = fail | Return the case to the route decision with reason affordability_failed | BACK_TO_ROUTE_DECISION | Milestone | Case owner | None |
| R-RES-09 | Restructure | Timer sentry | WITH_FCR_OFFICER | OFFER_PREPARED | offer inside the approved range and deviation_flag = N | Generate the offer letter and send it on a consented channel | OFFER_WITH_CUSTOMER | Customer task | Customer | offer validity 14 days |
| R-RES-10 | Restructure | Timer sentry | WITH_FCR_OFFICER | OFFER_PREPARED | offer outside the range or deviation_flag = Y | Route the offer to credit approval; 44% of TDR cases deviate today | AWAITING_CREDIT_APPROVAL | Human task | Credit approval committee | 3 working days |
| R-RES-11 | Restructure | Timer sentry | AWAITING_CREDIT_APPROVAL | CREDIT_APPROVED | final_call = approved | Release the offer and send it to the customer | OFFER_WITH_CUSTOMER | Customer task | Customer | offer validity 14 days |
| R-RES-12 | Restructure | User sentry | AWAITING_CREDIT_APPROVAL | CREDIT_DECLINED | final_call = rejected | Record the reason against the limit applied | DECLINED_BY_CREDIT | Event listener | Restructuring officer, FCR | None |
| R-RES-13 | Restructure | Timer sentry | AWAITING_CREDIT_APPROVAL | APPROVAL_SLA_BREACHED | approval_age > approval_escalation_limit | Escalate to the head of credit | AWAITING_CREDIT_APPROVAL | Human task | Head of credit | None |
| R-RES-14 | Restructure | User sentry | DECLINED_BY_CREDIT | DECLINE_RECORDED | Any | Return the case to the route decision with reason credit_declined | BACK_TO_ROUTE_DECISION | Milestone | Case owner | None |
| R-RES-15 | Restructure | Timer sentry | OFFER_WITH_CUSTOMER | CUSTOMER_COUNTER_OFFERED | counter_amount outside the current range | Return the case to the officer with the counter-offer and the gap | WITH_FCR_OFFICER | Human task | Restructuring officer, FCR | 2 working days |
| R-RES-16 | Restructure | Timer sentry | OFFER_WITH_CUSTOMER | CUSTOMER_SIGNED | signed = Y and signature verified | Route the case to operations to complete the booking | WITH_OPS_BOOKING | Human task | Operations (booking) | 1 working day |
| R-RES-17 | Restructure | System sentry | OFFER_WITH_CUSTOMER | CUSTOMER_DECLINED | declined = Y | Return the case to its prior status in COLLINS | RETURNED_TO_COLLINS | Event listener | Workbench | None |
| R-RES-18 | Restructure | Timer sentry | OFFER_WITH_CUSTOMER | OFFER_EXPIRED | signed = N and offer_validity passed | Return the case to its prior status in COLLINS | RETURNED_TO_COLLINS | Event listener | Workbench | None |
| R-RES-19 | Restructure | User sentry | OFFER_WITH_CUSTOMER | DEVIATION_RAISED | contact stop raised by X1 or X2 | Stop the offer channel and hold the offer clock | OFFER_WITH_CUSTOMER | Customer task | Deviation owner | None |
| R-RES-20 | Restructure | User sentry | RETURNED_TO_COLLINS | PRIOR_STATUS_RESTORED | Any | Restore the status held before the restructure and re-open the route decision | BACK_TO_ROUTE_DECISION | Milestone | Case owner | None |
| R-RES-21 | Restructure | Timer sentry | WITH_OPS_BOOKING | BOOKING_SUBMITTED | treatment_type = TDR | Submit the plan to NLEADS for credit approval and await the callback | WITH_OPS_BOOKING | Human task | Operations (booking) | 2 working days |
| R-RES-22 | Restructure | System sentry | WITH_OPS_BOOKING | BOOKING_CONFIRMED | ALS and NLEADS both acknowledge | Record the booking reference and set the payment schedule | BOOKED_IN_ALS_NLEADS | Human task | Workbench | None |
| R-RES-23 | Restructure | Timer sentry | WITH_OPS_BOOKING | BOOKING_REJECTED | ALS rejects the booking | Put the error on the officer queue and keep the case with operations | WITH_OPS_BOOKING | Human task | Operations (booking) | 1 working day |
| R-RES-24 | Restructure | User sentry | WITH_OPS_BOOKING | NLEADS_CALLBACK_MISSING | callback_age > callback_limit | Escalate the missing callback and hold the booking | WITH_OPS_BOOKING | Human task | Operations (booking) | None |
| R-RES-25 | Restructure | User sentry | BOOKED_IN_ALS_NLEADS | SCHEDULE_SET | first_due_date set | Start the plan timers and move the plan to running | PLAN_RUNNING | Human task | Restructuring officer, FCR | None |
| R-RES-26 | Restructure | System sentry | PLAN_RUNNING | PAYMENT_RECEIVED | payment matched to the installment | Advance the next due date and record the payment | PLAN_RUNNING | Human task | Workbench | None |
| R-RES-27 | Restructure | Timer sentry | PLAN_RUNNING | PAYMENT_MISSED | due_date passed and no payment matched | Raise plan.payment.missed and start the cure period | PLAN_CURE_PERIOD | Event listener | Case owner | cure_period_days from reference data |
| R-RES-28 | Restructure | System sentry | PLAN_CURE_PERIOD | PAYMENT_RECEIVED_LATE | payment received inside the cure period | Clear the miss and return the plan to running | PLAN_RUNNING | Human task | Workbench | None |
| R-RES-29 | Restructure | Timer sentry | PLAN_CURE_PERIOD | CURE_PERIOD_EXPIRED | no payment and cure_period passed | Increment the break count and mark the plan broken | PLAN_BROKEN | Event listener | Case owner | None |
| R-RES-30 | Restructure | Timer sentry | PLAN_BROKEN | BREAK_RECORDED | break_count < max_breaks | Return the case to the route decision with reason broken_plan | BACK_TO_ROUTE_DECISION | Milestone | Case owner | 5 working days |
| R-RES-31 | Restructure | User sentry | PLAN_BROKEN | BREAK_RECORDED | break_count >= max_breaks | Bar a further restructure on this case | RESTRUCTURE_BARRED | Milestone | Case owner | None |
| R-RES-32 | Restructure | User sentry | RESTRUCTURE_BARRED | BAR_APPLIED | Any | Exclude R1 from the open routes and re-run the route decision | BACK_TO_ROUTE_DECISION | Milestone | Case owner | None |
| R-RES-33 | Restructure | System sentry | PLAN_RUNNING | FINAL_INSTALLMENT_PAID | installments_paid = installments_due | Close the treatment, release the collateral and close the case | PLAN_COMPLETED | Milestone | Workbench | None |
| R-RES-34 | Restructure | User sentry | PLAN_RUNNING | DEVIATION_RAISED | deviation_open in (X1,X2,X3,X4,X5) | Pause the plan timers and hold the case with the deviation owner | PLAN_RUNNING | Human task | Deviation owner | None |
| R-RES-35 | Restructure | Timer sentry | WITH_FCR_OFFICER | OFFER_PREPARED | no condition matched, or affordability data is missing | Hold the case, name the missing field and raise a task for the owner | UNMATCHED_EXCEPTION | Event listener | Case owner | same day |
| R-RES-36 | Restructure | Timer sentry | PLAN_BROKEN | BREAK_RECORDED | break_count is missing or not a number | Hold the case, name the missing field and raise a task for the owner | UNMATCHED_EXCEPTION | Event listener | Case owner | same day |
| R-RES-37 | Restructure | Timer sentry | UNMATCHED_EXCEPTION | MANUAL_DECISION_RECORDED | Any | Case owner records the decision and the missing field; the rule gap is logged for the center of excellence | BACK_TO_ROUTE_DECISION | Milestone | Case owner | 2 working days |
| R-SET-01 | Settlement | System sentry | ROUTE_APPROVED_SETTLEMENT | ROUTE_APPROVED | decision.approved and route = R2 | Calculate the payoff from ALS and set the range from reference data | PAYOFF_AND_RANGE_SET | Human task | Workbench | None |
| R-SET-02 | Settlement | Timer sentry | PAYOFF_AND_RANGE_SET | RANGE_SET | payoff_as_at inside the freshness limit | Open the treatment record and place the case in the FCR queue | WITH_FCR_OFFICER_SET | Human task | Restructuring officer, FCR | 2 working days |
| R-SET-03 | Settlement | System sentry | PAYOFF_AND_RANGE_SET | PAYOFF_STALE | payoff_as_at older than the freshness limit | Block the step and request a fresh payoff through EAPI | PAYOFF_AND_RANGE_SET | Human task | Workbench | None |
| R-SET-04 | Settlement | Timer sentry | WITH_FCR_OFFICER_SET | OFFER_PREPARED | offer_amount between settlement_range_low and settlement_range_high | Generate the settlement letter and send it on a consented channel | OFFER_WITH_CUSTOMER_SET | Customer task | Customer | offer validity 14 days |
| R-SET-05 | Settlement | Timer sentry | WITH_FCR_OFFICER_SET | OFFER_PREPARED | offer_amount < floor_price | Route the offer to the approver with the gap to the floor | AWAITING_APPROVAL_SET | Human task | Credit approval committee | 3 working days |
| R-SET-06 | Settlement | Timer sentry | AWAITING_APPROVAL_SET | APPROVAL_GRANTED | final_call = approved | Release the offer and send it to the customer | OFFER_WITH_CUSTOMER_SET | Customer task | Customer | offer validity 14 days |
| R-SET-07 | Settlement | User sentry | AWAITING_APPROVAL_SET | APPROVAL_REFUSED | final_call = rejected | Record the reason and the gap to the floor | DECLINED_BY_APPROVER_SET | Event listener | Restructuring officer, FCR | None |
| R-SET-08 | Settlement | User sentry | DECLINED_BY_APPROVER_SET | DECLINE_RECORDED | Any | Return the case to the route decision with reason below_floor_refused | RETURNED_TO_ROUTE_SET | Milestone | Case owner | None |
| R-SET-09 | Settlement | Timer sentry | OFFER_WITH_CUSTOMER_SET | CUSTOMER_COUNTER_OFFERED | counter_amount < floor_price | Return the case to the officer and re-test against the floor | WITH_FCR_OFFICER_SET | Human task | Restructuring officer, FCR | 2 working days |
| R-SET-10 | Settlement | Timer sentry | OFFER_WITH_CUSTOMER_SET | CUSTOMER_SIGNED | signed = Y | Route the case to operations and raise the payment instruction | WITH_OPS_SETTLEMENT | Human task | Operations (booking) | 1 working day |
| R-SET-11 | Settlement | Timer sentry | OFFER_WITH_CUSTOMER_SET | OFFER_EXPIRED | signed = N and offer_validity passed | Return the case to the route decision with reason offer_expired | RETURNED_TO_ROUTE_SET | Milestone | Case owner | None |
| R-SET-12 | Settlement | User sentry | OFFER_WITH_CUSTOMER_SET | DEVIATION_RAISED | contact stop raised by X1 or X2 | Stop the offer channel and hold the offer clock | OFFER_WITH_CUSTOMER_SET | Customer task | Deviation owner | None |
| R-SET-13 | Settlement | Timer sentry | WITH_OPS_SETTLEMENT | SETTLEMENT_BOOKED | agreement signed and terms booked in ALS | Set the payment due date and wait for the money | AWAITING_PAYMENT | Customer task | Customer | payment due 30 days |
| R-SET-14 | Settlement | System sentry | AWAITING_PAYMENT | PAYMENT_RECEIVED | amount_received = settlement_amount | Match the payment and post it | PAYMENT_CLEARED | Human task | Workbench | None |
| R-SET-15 | Settlement | System sentry | AWAITING_PAYMENT | PAYMENT_RECEIVED | amount_received < settlement_amount and installments agreed | Match the installment and keep the case awaiting the balance | PAYMENT_PART_RECEIVED | Event listener | Workbench | None |
| R-SET-16 | Settlement | Timer sentry | AWAITING_PAYMENT | PAYMENT_UNMATCHED | payment matches no treatment | Put the payment on the exception list for the reconciliation agent | AWAITING_PAYMENT | Customer task | Case owner | 2 working days |
| R-SET-17 | Settlement | User sentry | AWAITING_PAYMENT | PAYMENT_DEADLINE_PASSED | no payment matched and payment_due passed | Cancel the settlement and return the case to the route decision | RETURNED_TO_ROUTE_SET | Milestone | Case owner | None |
| R-SET-18 | Settlement | System sentry | PAYMENT_PART_RECEIVED | FINAL_INSTALLMENT_RECEIVED | cumulative_received = settlement_amount | Match the final installment and post the settlement | PAYMENT_CLEARED | Human task | Workbench | None |
| R-SET-19 | Settlement | User sentry | PAYMENT_PART_RECEIVED | INSTALLMENT_MISSED | due_date passed and no payment matched | Cancel the settlement and return the case to the route decision | RETURNED_TO_ROUTE_SET | Milestone | Case owner | None |
| R-SET-20 | Settlement | System sentry | PAYMENT_CLEARED | CLEARANCE_CONFIRMED | funds cleared | Close the account in ALS and request the collateral release | COLLATERAL_RELEASE_REQUESTED | Human task | Workbench | None |
| R-SET-21 | Settlement | System sentry | COLLATERAL_RELEASE_REQUESTED | COLLATERAL_RELEASED | CCMS confirms the release | Return the title, close the treatment and close the case | CASE_CLOSED_SETTLED | Milestone | Workbench | None |
| R-SET-22 | Settlement | Timer sentry | COLLATERAL_RELEASE_REQUESTED | TITLE_DOCUMENTS_MISSING | title documents not found | Raise a task to re-create the title set before release | COLLATERAL_RELEASE_REQUESTED | Human task | Case owner | 5 working days |
| R-SET-23 | Settlement | User sentry | CASE_CLOSED_SETTLED | PAYMENT_REVERSED | reversal received after release | Re-open the case and record the reversal against the treatment | PAYMENT_REVERSED | Event listener | Case owner | None |
| R-SET-24 | Settlement | User sentry | PAYMENT_REVERSED | REVERSAL_RECORDED | Any | Return the case to the route decision with reason payment_reversed | RETURNED_TO_ROUTE_SET | Milestone | Case owner | None |
| R-SET-25 | Settlement | Timer sentry | WITH_FCR_OFFICER_SET | OFFER_PREPARED | no condition matched, or the payoff or floor price is missing | Hold the case, name the missing field and raise a task for the owner | UNMATCHED_EXCEPTION | Event listener | Case owner | same day |
| R-SET-26 | Settlement | Timer sentry | AWAITING_PAYMENT | PAYMENT_RECEIVED | amount received does not match and no installment plan is agreed | Hold the case, name the missing field and raise a task for the owner | UNMATCHED_EXCEPTION | Event listener | Case owner | same day |
| R-SET-27 | Settlement | Timer sentry | UNMATCHED_EXCEPTION | MANUAL_DECISION_RECORDED | Any | Case owner records the decision and the missing field; the rule gap is logged for the center of excellence | RETURNED_TO_ROUTE_SET | Milestone | Case owner | 2 working days |
| R-DIL-01 | Deed in lieu | Timer sentry | ROUTE_APPROVED_DIL | ROUTE_APPROVED | decision.approved and route = R3 | Prioritize the lead and start the early readiness checks | EARLY_READINESS_CHECK | Human task | Workbench | 2 working days |
| R-DIL-02 | Deed in lieu | System sentry | EARLY_READINESS_CHECK | ENCUMBRANCE_CLEAR | product = MTG and encumbrance_status = clear | Order the valuation | VALUATION_ORDERED | Human task | Workbench | None |
| R-DIL-03 | Deed in lieu | System sentry | EARLY_READINESS_CHECK | REGISTRATION_CHECK_PASSED | product = HP and registration clear in SCIS | Order the valuation | VALUATION_ORDERED | Human task | Workbench | None |
| R-DIL-04 | Deed in lieu | Timer sentry | EARLY_READINESS_CHECK | ENCUMBRANCE_UNRESOLVED | product = MTG and encumbrance_status = unresolved | Block the route and hold the case until the check clears | ENCUMBRANCE_BLOCKED | Event listener | Case owner | 10 working days |
| R-DIL-05 | Deed in lieu | System sentry | ENCUMBRANCE_BLOCKED | ENCUMBRANCE_CLEARED | encumbrance_status = clear | Resume the route and order the valuation | VALUATION_ORDERED | Human task | Workbench | None |
| R-DIL-06 | Deed in lieu | Timer sentry | ENCUMBRANCE_BLOCKED | HOLD_EXPIRED | encumbrance_status still unresolved at the hold limit | Return the case to the route decision with reason encumbrance_unresolved | RETURNED_TO_ROUTE_DIL | Milestone | Case owner | None |
| R-DIL-07 | Deed in lieu | Timer sentry | VALUATION_ORDERED | FAST_LANE_SELECTED | lead_rank in the top 10% | Raise an official appraisal order to a panel valuer through SVAF | AWAITING_VALUER | Partner task | Valuer | panel service level |
| R-DIL-08 | Deed in lieu | System sentry | VALUATION_ORDERED | PRELIMINARY_VALUATION_USED | lead_rank outside the top 10% | Value the asset with the preliminary valuation model | VALUATION_ACCEPTED | Human task | Workbench | None |
| R-DIL-09 | Deed in lieu | Timer sentry | AWAITING_VALUER | VALUATION_RECEIVED | report attached and value extracted | Flag outliers and present the value for acceptance | VALUATION_ACCEPTED | Human task | Case owner | 2 working days |
| R-DIL-10 | Deed in lieu | User sentry | AWAITING_VALUER | ACCESS_REFUSED | valuer records an access refusal | Record the limitation and use an external estimate | VALUATION_ACCEPTED | Human task | Case owner | None |
| R-DIL-11 | Deed in lieu | Timer sentry | AWAITING_VALUER | VALUER_SLA_BREACHED | order_age > panel service level | Escalate to the partner and agency manager and re-allocate the order | AWAITING_VALUER | Partner task | Partner and agency manager | None |
| R-DIL-12 | Deed in lieu | Timer sentry | VALUATION_ACCEPTED | VALUE_ACCEPTED | accepted_at set and within the age limit | Place the case with the restructuring officer to negotiate | WITH_FCR_OFFICER_DIL | Human task | Restructuring officer, FCR | 5 working days |
| R-DIL-13 | Deed in lieu | System sentry | WITH_FCR_OFFICER_DIL | TERMS_AGREED | customer agrees to transfer the asset | Apply the governed transfer price template | TRANSFER_PRICE_SET | Human task | Workbench | None |
| R-DIL-14 | Deed in lieu | Timer sentry | TRANSFER_PRICE_SET | PRICE_INSIDE_FLOOR | transfer_price >= floor_price | Generate the credit approval, the contract and the mortgage documents | OFFER_WITH_CUSTOMER_DIL | Customer task | Customer | offer validity 14 days |
| R-DIL-15 | Deed in lieu | Timer sentry | TRANSFER_PRICE_SET | PRICE_BELOW_FLOOR | transfer_price < floor_price | Route the price for a second signature | AWAITING_SECOND_SIGNATURE | Human task | Head of NPA | 3 working days |
| R-DIL-16 | Deed in lieu | Timer sentry | AWAITING_SECOND_SIGNATURE | SECOND_SIGNATURE_GIVEN | final_call = approved | Generate the documents and put the offer to the customer | OFFER_WITH_CUSTOMER_DIL | Customer task | Customer | offer validity 14 days |
| R-DIL-17 | Deed in lieu | User sentry | AWAITING_SECOND_SIGNATURE | SECOND_SIGNATURE_REFUSED | final_call = rejected | Return the case to the route decision with reason price_below_floor | RETURNED_TO_ROUTE_DIL | Milestone | Case owner | None |
| R-DIL-18 | Deed in lieu | Timer sentry | OFFER_WITH_CUSTOMER_DIL | CUSTOMER_ACCEPTED | product = MTG and signature is wet ink per Legal | Schedule the collateral inspection before transfer | WITH_FIELD_INSPECTION | Human task | Field officer or agency field team | 5 working days |
| R-DIL-19 | Deed in lieu | Timer sentry | OFFER_WITH_CUSTOMER_DIL | CUSTOMER_ACCEPTED | product = HP and the vehicle is surrendered | Schedule the vehicle inspection and collection | WITH_FIELD_INSPECTION | Human task | Field officer or agency field team | 5 working days |
| R-DIL-20 | Deed in lieu | User sentry | OFFER_WITH_CUSTOMER_DIL | CUSTOMER_WITHDREW | customer withdraws before transfer | Return the case to the route decision with reason customer_withdrew | RETURNED_TO_ROUTE_DIL | Milestone | Case owner | None |
| R-DIL-21 | Deed in lieu | Timer sentry | OFFER_WITH_CUSTOMER_DIL | OFFER_EXPIRED | not accepted and offer_validity passed | Return the case to the route decision with reason offer_expired | RETURNED_TO_ROUTE_DIL | Milestone | Case owner | None |
| R-DIL-22 | Deed in lieu | System sentry | WITH_FIELD_INSPECTION | INSPECTION_COMPLETED | checklist, photographs and bills captured | Run the asset unlock rule | ASSET_UNLOCK_DECISION | Decision task | Workbench | None |
| R-DIL-23 | Deed in lieu | User sentry | ASSET_UNLOCK_DECISION | AUTO_UNLOCK_PASSED | unlock rule passes, about 95% of cases | Release the asset for transfer | AWAITING_TRANSFER | Partner task | Customer | None |
| R-DIL-24 | Deed in lieu | Timer sentry | ASSET_UNLOCK_DECISION | AUTO_UNLOCK_FAILED | unlock rule fails | Send the agent summary to the approver | AWAITING_APPROVER_SUMMARY | Human task | Head of NPA | 3 working days |
| R-DIL-25 | Deed in lieu | User sentry | AWAITING_APPROVER_SUMMARY | APPROVER_RELEASED | final_call = approved | Release the asset for transfer | AWAITING_TRANSFER | Partner task | Customer | None |
| R-DIL-26 | Deed in lieu | User sentry | AWAITING_APPROVER_SUMMARY | APPROVER_REFUSED | final_call = rejected | Return the case to the route decision with reason unlock_refused | RETURNED_TO_ROUTE_DIL | Milestone | Case owner | None |
| R-DIL-27 | Deed in lieu | System sentry | AWAITING_TRANSFER | TRANSFER_COMPLETED | product = MTG and ownership transferred at the Land Office | Record the NPA in AMIS, settle the debt and release the collateral in CCMS | ASSET_ON_BOOKS | Human task | Workbench | None |
| R-DIL-28 | Deed in lieu | System sentry | AWAITING_TRANSFER | TRANSFER_COMPLETED | product = HP and registration transferred in SCIS | Record the asset in AMIS, settle the debt and release the registration | ASSET_ON_BOOKS | Human task | Workbench | None |
| R-DIL-29 | Deed in lieu | Timer sentry | AWAITING_TRANSFER | TITLE_NOT_CLEAN | title or registration check fails at transfer | Hold the transfer and raise a task to clear the title | TITLE_NOT_CLEAN | Event listener | Case owner | 10 working days |
| R-DIL-30 | Deed in lieu | User sentry | TITLE_NOT_CLEAN | TITLE_CLEARED | title or registration check passes | Resume the transfer | AWAITING_TRANSFER | Partner task | Customer | None |
| R-DIL-31 | Deed in lieu | Timer sentry | TITLE_NOT_CLEAN | HOLD_EXPIRED | title still not clean at the hold limit | Return the case to the route decision with reason title_not_clean | RETURNED_TO_ROUTE_DIL | Milestone | Case owner | None |
| R-DIL-32 | Deed in lieu | User sentry | ASSET_ON_BOOKS | BUYBACK_AGREED | customer rents the asset back | Create the rental record and set the auto-debit | RENTAL_RUNNING | Human task | Case owner | None |
| R-DIL-33 | Deed in lieu | User sentry | ASSET_ON_BOOKS | DISPOSAL_REQUIRED | no buy-back agreed | Hand the asset to the disposal route | HANDED_TO_DISPOSAL | Milestone | Sale officer | None |
| R-DIL-34 | Deed in lieu | User sentry | RENTAL_RUNNING | RENTAL_ARREARS | rental arrears exceed the limit | Hand the asset to the disposal route | HANDED_TO_DISPOSAL | Milestone | Sale officer | None |
| R-DIL-35 | Deed in lieu | Timer sentry | OFFER_WITH_CUSTOMER_DIL | CUSTOMER_ACCEPTED | product is not MTG or HP, or the signature basis is not recorded | Hold the case, name the missing field and raise a task for the owner | UNMATCHED_EXCEPTION | Event listener | Case owner | same day |
| R-DIL-36 | Deed in lieu | Timer sentry | AWAITING_TRANSFER | TRANSFER_COMPLETED | the registry confirmation does not name a known registry | Hold the case, name the missing field and raise a task for the owner | UNMATCHED_EXCEPTION | Event listener | Case owner | same day |
| R-DIL-37 | Deed in lieu | Timer sentry | UNMATCHED_EXCEPTION | MANUAL_DECISION_RECORDED | Any | Case owner records the decision and the missing field; the rule gap is logged for the center of excellence | RETURNED_TO_ROUTE_DIL | Milestone | Case owner | 2 working days |
| R-LIT-01 | Litigation | Timer sentry | LIT_ROUTE_APPROVED | ROUTE_APPROVED | decision.approved and route = R4 | Open the litigation task and set the notice and prescription timers | NOTICE_GENERATED | Human task | Workbench | Same day |
| R-LIT-02 | Litigation | Timer sentry | LIT_ROUTE_APPROVED | TREATMENT_BROKEN | plan_status = broken and prior_route in (R1, R2) | Return the case to the legal route and open the litigation task | NOTICE_GENERATED | Human task | Workbench | Same day |
| R-LIT-03 | Litigation | Timer sentry | NOTICE_GENERATED | TEMPLATE_SELECTED | template_status = current for product and notice_type | Generate the demand and recall notices from the Legal-approved template | NOTICE_DISPATCHED | Human task | Workbench | 1 working day |
| R-LIT-04 | Litigation | Timer sentry | NOTICE_GENERATED | TEMPLATE_WITHDRAWN | template_status = withdrawn | Hold generation and raise a task to the litigation officer | NOTICE_BLOCKED | Event listener | Litigation officer | 1 working day |
| R-LIT-05 | Litigation | User sentry | NOTICE_GENERATED | CONTACT_STOP_APPLIED | contact_stop = Y from X1 or X2 | Hold the notice and route the case to the deviation owner | NOTICE_BLOCKED | Event listener | Conduct and QA officer | None |
| R-LIT-06 | Litigation | Timer sentry | NOTICE_BLOCKED | TEMPLATE_REPLACED | a new template version is approved by Legal | Resume generation on the current version | NOTICE_GENERATED | Human task | Workbench | 1 working day |
| R-LIT-07 | Litigation | Timer sentry | NOTICE_DISPATCHED | PROOF_OF_DELIVERY_RECEIVED | served_result = delivered | Attach the proof and start the notice period from delivered_at | WITH_CUSTOMER_NOTICE_PERIOD | Customer task | Customer | Notice period by product and type |
| R-LIT-08 | Litigation | Timer sentry | NOTICE_DISPATCHED | PROOF_WINDOW_EXPIRED | no proof returned inside the proof window | Mark the notice unserved; the notice period does not start | NOTICE_UNSERVED | Event listener | Litigation officer | 7 days |
| R-LIT-09 | Litigation | Timer sentry | NOTICE_DISPATCHED | DELIVERY_FAILED | served_result in (refused, returned, undeliverable) | Record the result and queue an alternate service method | NOTICE_UNSERVED | Event listener | Litigation officer | 2 working days |
| R-LIT-10 | Litigation | Timer sentry | NOTICE_UNSERVED | ALTERNATE_SERVICE_ORDERED | address refreshed, or substituted service approved | Re-serve by the alternate method | NOTICE_DISPATCHED | Human task | Workbench | 3 working days |
| R-LIT-11 | Litigation | Timer sentry | NOTICE_UNSERVED | PRESCRIPTION_WARNING | prescription_days_remaining <= 90 | Head of Litigation approves substituted service or filing where the law allows | PACK_ASSEMBLY | Human task | Head of Litigation | To the prescription date |
| R-LIT-12 | Litigation | User sentry | WITH_CUSTOMER_NOTICE_PERIOD | CUSTOMER_PAID_IN_FULL | balance = 0 inside the notice period | Cancel the litigation route and close the legal action | CASE_CLOSED | Milestone | Case owner | None |
| R-LIT-13 | Litigation | Timer sentry | WITH_CUSTOMER_NOTICE_PERIOD | CUSTOMER_REQUESTED_TREATMENT | offer acceptable inside the approved range | Cancel litigation and return the case to the treatment route | TO_TREATMENT | Milestone | Restructuring officer, FCR | 2 working days |
| R-LIT-14 | Litigation | User sentry | WITH_CUSTOMER_NOTICE_PERIOD | CUSTOMER_DISPUTED | inbound reply classified as a dispute | Raise X1, stop contact on the disputed item and pause the litigation timers | DEVIATION_HOLD | Event listener | Complaint officer | None |
| R-LIT-15 | Litigation | Timer sentry | WITH_CUSTOMER_NOTICE_PERIOD | NOTICE_PERIOD_EXPIRED | no cure and no dispute at period_expires_at | Open pack assembly | PACK_ASSEMBLY | Human task | Workbench | 3 working days |
| R-LIT-16 | Litigation | Timer sentry | PACK_ASSEMBLY | PACK_COMPLETE | every defect list item present | Present the pack to the litigation officer for verification | PACK_VERIFIED | Human task | Litigation officer | 2 working days |
| R-LIT-17 | Litigation | Timer sentry | PACK_ASSEMBLY | PACK_INCOMPLETE | one or more defect list items missing | Raise retrieval requests and hold the pack | PACK_DEFECT_HOLD | Event listener | Litigation officer | 5 working days |
| R-LIT-18 | Litigation | Timer sentry | PACK_DEFECT_HOLD | DOCUMENT_RETRIEVED | missing items supplied, re-signed or re-created | Re-run the defect list check | PACK_ASSEMBLY | Human task | Workbench | 1 working day |
| R-LIT-19 | Litigation | Timer sentry | PACK_DEFECT_HOLD | DOCUMENT_UNRECOVERABLE | the document cannot be re-created | Refer to Legal for the affidavit route and record the gap with a reason | PACK_VERIFIED | Human task | Head of Litigation | 10 working days |
| R-LIT-20 | Litigation | Timer sentry | PACK_DEFECT_HOLD | PRESCRIPTION_WARNING | prescription_days_remaining <= 90 | Escalate; the Head of Litigation approves filing with the gap recorded | PACK_VERIFIED | Human task | Head of Litigation | To the prescription date |
| R-LIT-21 | Litigation | Timer sentry | PACK_VERIFIED | OFFICER_REJECTED_PACK | the officer rejects the pack at verification | Return the pack to the legal document agent for rework | PACK_ASSEMBLY | Human task | Workbench | 1 working day |
| R-LIT-22 | Litigation | Timer sentry | PACK_VERIFIED | CONDUCT_CHECK_FAILED | the conduct check on the notice or the contact fails | Return the notice for correction before filing | NOTICE_BLOCKED | Event listener | Conduct and QA officer | 2 working days |
| R-LIT-23 | Litigation | Timer sentry | PACK_VERIFIED | PACK_APPROVED | pack_verified_at set | Select the law firm by rule from the panel | FIRM_SELECTION | Decision task | Workbench | Same day |
| R-LIT-24 | Litigation | Timer sentry | FIRM_SELECTION | FIRM_MATCHED | panel firm covers the court region and case type and passes the conflict check | Issue the instruction with the pack through the portal | FIRM_INSTRUCTED | Partner task | Panel law firm | 2 working days |
| R-LIT-25 | Litigation | Timer sentry | FIRM_SELECTION | NO_FIRM_AVAILABLE | no panel firm in the region, or all conflicted | Escalate the selection | FIRM_ESCALATED | Human task | Head of Litigation | 2 working days |
| R-LIT-26 | Litigation | Timer sentry | FIRM_ESCALATED | FIRM_NOMINATED | the Head of Litigation nominates a firm or widens the panel | Issue the instruction with the pack through the portal | FIRM_INSTRUCTED | Partner task | Panel law firm | 2 working days |
| R-LIT-27 | Litigation | Timer sentry | FIRM_INSTRUCTED | INSTRUCTION_DECLINED | the firm declines, or does not accept inside the window | Record the decline and re-select the next firm on the scorecard | FIRM_DECLINED | Event listener | Workbench | 2 working days |
| R-LIT-28 | Litigation | Timer sentry | FIRM_INSTRUCTED | FIRM_BREACHED_SLA | the instruction is past due with no filing | Mark the instruction breached, notify the partner manager and re-select | FIRM_DECLINED | Event listener | Partner and agency manager | None |
| R-LIT-29 | Litigation | Timer sentry | FIRM_DECLINED | RESELECTION_RUN | the next firm on the scorecard is available | Issue the instruction to the next firm | FIRM_INSTRUCTED | Partner task | Panel law firm | 2 working days |
| R-LIT-30 | Litigation | Timer sentry | FIRM_INSTRUCTED | CASE_FILED | the firm uploads the receipt and the court case number | Write the court case number to the Legal Action and set the hearing timers | FILED_IN_COURT | Partner task | Panel law firm | Filing service level by task |
| R-LIT-31 | Litigation | Timer sentry | FILED_IN_COURT | COURT_REJECTED_FILING | the court returns the filing for a defect | Record the defect and return the pack for rework | FILING_REJECTED | Event listener | Litigation officer | 5 working days |
| R-LIT-32 | Litigation | Timer sentry | FILING_REJECTED | PACK_REWORKED | the defect is corrected | Re-run the defect list check and re-file | PACK_ASSEMBLY | Human task | Workbench | 3 working days |
| R-LIT-33 | Litigation | Timer sentry | FILED_IN_COURT | HEARING_SCHEDULED | the court sets a hearing date | Schedule the hearing and set the deadline timer | IN_HEARING | Partner task | Panel law firm | To the hearing date |
| R-LIT-34 | Litigation | Timer sentry | IN_HEARING | HEARING_ADJOURNED | outcome = adjourned | Reset the hearing timer and record the postpone reason code | HEARING_ADJOURNED | Event listener | Panel law firm | To the new date |
| R-LIT-35 | Litigation | Timer sentry | HEARING_ADJOURNED | NEW_DATE_SET | scheduled_for reset by the court | Return the case to the hearing calendar | IN_HEARING | Partner task | Panel law firm | To the new date |
| R-LIT-36 | Litigation | Timer sentry | IN_HEARING | SETTLEMENT_PROPOSED | the customer or the firm proposes a settlement before judgment | The agent proposes the step with its cost and effect, and routes it to the approver | SETTLEMENT_OFFERED_AT_COURT | Decision task | Approver at D7.4 | 3 working days |
| R-LIT-37 | Litigation | Timer sentry | SETTLEMENT_OFFERED_AT_COURT | SETTLEMENT_APPROVED | inside the D7.4 limit, or the committee approves above it | Book the treatment and hold the litigation rather than withdraw it | LITIGATION_HELD | Human task | Restructuring officer, FCR | 2 working days |
| R-LIT-38 | Litigation | User sentry | SETTLEMENT_OFFERED_AT_COURT | SETTLEMENT_REJECTED | the approver rejects with a reason | Continue the case to judgment | IN_HEARING | Partner task | Panel law firm | None |
| R-LIT-39 | Litigation | User sentry | LITIGATION_HELD | SETTLEMENT_COMPLETED | the treatment completes and the balance is satisfied | Withdraw the case and close the legal action | CASE_CLOSED | Milestone | Case owner | None |
| R-LIT-40 | Litigation | Timer sentry | LITIGATION_HELD | SETTLEMENT_BROKEN | plan_status = broken | Resume the litigation from the hearing it was held at | IN_HEARING | Partner task | Panel law firm | 5 working days |
| R-LIT-41 | Litigation | Timer sentry | IN_HEARING | FEE_DUE | a court fee or legal expense falls due | Route the fee to the approver inside the D7.4 limit | LEGAL_SPEND_APPROVAL | Decision task | Approver at D7.4 | 3 working days |
| R-LIT-42 | Litigation | Timer sentry | LEGAL_SPEND_APPROVAL | FEE_APPROVED | inside the limit, or the committee approves above it | Raise the fee and post it against the case | IN_HEARING | Partner task | Panel law firm | 5 working days |
| R-LIT-43 | Litigation | User sentry | LEGAL_SPEND_APPROVAL | FEE_REJECTED | the approver rejects the spend | Record the reason and return the case without the spend | IN_HEARING | Partner task | Litigation officer | None |
| R-LIT-44 | Litigation | Timer sentry | IN_HEARING | JUDGMENT_FOR_THE_BANK | judgment_type in (full, partial, default) | Record the judgment date and amount and open the enforcement task | JUDGMENT_RECORDED | Human task | Enforcement owner | 5 working days |
| R-LIT-45 | Litigation | Timer sentry | IN_HEARING | JUDGMENT_AGAINST_THE_BANK | judgment_type = dismissed | Record the dismissal and open the appeal window | JUDGMENT_DISMISSED | Event listener | Litigation officer | To the appeal window end |
| R-LIT-46 | Litigation | Timer sentry | JUDGMENT_DISMISSED | APPEAL_WINDOW_OPEN | appeal_window_ends is in the future | The agent proposes appeal or accept with cost and effect | APPEAL_DECISION | Decision task | Approver at D7.4 | To the window end |
| R-LIT-47 | Litigation | Timer sentry | APPEAL_DECISION | APPEAL_APPROVED | inside the limit, or the Head of Litigation approves above it | Instruct the firm to appeal and reset the hearing timers | APPEAL_FILED | Partner task | Panel law firm | To the filing deadline |
| R-LIT-48 | Litigation | Timer sentry | APPEAL_FILED | APPEAL_HEARING_SET | the court sets the appeal hearing | Return the case to the hearing calendar | IN_HEARING | Partner task | Panel law firm | To the hearing date |
| R-LIT-49 | Litigation | User sentry | APPEAL_DECISION | APPEAL_DECLINED | the approver accepts the judgment, or the window has passed | Record the reason and route the case to write-off | TO_WRITE_OFF | Milestone | Write-off team with Credit Administration | None |
| R-LIT-50 | Litigation | Timer sentry | JUDGMENT_RECORDED | ENFORCEMENT_OPENED | a judgment is recorded against the debtor | Trace assets across NCB, internal data, registries and insurers | ASSET_TRACE | Human task | Workbench | 10 working days |
| R-LIT-51 | Litigation | User sentry | JUDGMENT_RECORDED | DEBTOR_PAID_AFTER_JUDGMENT | a payment after judgment covers the balance and costs | Match the payment, close the enforcement and close the case | CASE_CLOSED | Milestone | Case owner | None |
| R-LIT-52 | Litigation | Timer sentry | ASSET_TRACE | ASSETS_FOUND | one or more assets traced | Present the enforcement decision with the traced assets | ENFORCEMENT_DECISION | Decision task | Enforcement owner | 5 working days |
| R-LIT-53 | Litigation | Timer sentry | ASSET_TRACE | NO_ASSET_FOUND | the trace returns nothing | Present the enforcement decision with a deferral recommendation | ENFORCEMENT_DECISION | Decision task | Enforcement owner | 5 working days |
| R-LIT-54 | Litigation | Timer sentry | ENFORCEMENT_DECISION | ENFORCE_APPROVED | an asset is traced and enforcement is economic | Instruct the firm to apply for the writ and seizure | WRIT_AND_SEIZURE | Partner task | Panel law firm | To the writ deadline |
| R-LIT-55 | Litigation | Timer sentry | ENFORCEMENT_DECISION | DEFER_RECORDED | deferral_reason and deferral_review_date are both present | Record the deferral and re-queue the case on the review date | DEFERRAL_RECORDED | Event listener | Enforcement owner | To the review date |
| R-LIT-56 | Litigation | Timer sentry | DEFERRAL_RECORDED | REVIEW_DATE_REACHED | the deferral review date is reached | Return the case to the enforcement decision | ENFORCEMENT_DECISION | Decision task | Enforcement owner | 5 working days |
| R-LIT-57 | Litigation | User sentry | DEFERRAL_RECORDED | ENFORCEMENT_EXHAUSTED | a second deferral with no asset traced | Route the case to write-off at D9 | TO_WRITE_OFF | Milestone | Write-off team with Credit Administration | None |
| R-LIT-58 | Litigation | Timer sentry | ENFORCEMENT_DECISION | PETITION_PROPOSED | enforcement exhausted and the bankruptcy test is met | Route the petition to the approver at D7.5 | BANKRUPTCY_PETITION | Decision task | Approver at D7.5 | 5 working days |
| R-LIT-59 | Litigation | Timer sentry | BANKRUPTCY_PETITION | PETITION_APPROVED | the approver approves the petition at D7.5 | Instruct the firm to file the petition and the claim | OFFICIAL_RECEIVER_CLAIM | Partner task | Official receiver | To the filing deadline |
| R-LIT-60 | Litigation | User sentry | BANKRUPTCY_PETITION | PETITION_REJECTED | the approver rejects with a reason | Route the case to write-off at D9 | TO_WRITE_OFF | Milestone | Write-off team with Credit Administration | None |
| R-LIT-61 | Litigation | Timer sentry | OFFICIAL_RECEIVER_CLAIM | DIVIDEND_RECEIVED | the receiver distributes a dividend | Match the dividend to the case and post it to ALS | PROCEEDS_MATCHED | Human task | Workbench | 2 working days |
| R-LIT-62 | Litigation | User sentry | OFFICIAL_RECEIVER_CLAIM | CLAIM_DEADLINE_MISSED | the claim is not filed before the receiver deadline | Record the loss and the reason and route the case to write-off | TO_WRITE_OFF | Milestone | Write-off team with Credit Administration | None |
| R-LIT-63 | Litigation | Timer sentry | WRIT_AND_SEIZURE | SEIZURE_EXECUTED | the asset is seized and the seizure reported | Open the LED auction at round 1 | LED_AUCTION | Partner task | Legal Execution Department | To the auction date |
| R-LIT-64 | Litigation | Timer sentry | WRIT_AND_SEIZURE | SEIZURE_BLOCKED | the seizure is obstructed, or the asset has moved | Record the obstruction and return to the enforcement decision | ENFORCEMENT_DECISION | Decision task | Enforcement owner | 10 working days |
| R-LIT-65 | Litigation | Timer sentry | LED_AUCTION | ROUND_SOLD | round_result = sold at 100, 90, 80 or 70 percent of official value | Match the proceeds to the case | PROCEEDS_MATCHED | Human task | Workbench | 2 working days |
| R-LIT-66 | Litigation | Timer sentry | LED_AUCTION | ROUND_NO_BID | round_result = no bid and auction_round < 4 | Step the price to the next round on the ladder | LED_AUCTION | Partner task | Legal Execution Department | To the next auction date |
| R-LIT-67 | Litigation | Timer sentry | LED_AUCTION | LADDER_EXHAUSTED | round_result = no bid and auction_price_basis = 70 percent | Record the unsold result and refer it to the enforcement owner | NO_BID_AT_70 | Event listener | Enforcement owner | 5 working days |
| R-LIT-68 | Litigation | Timer sentry | NO_BID_AT_70 | ASSET_TAKEN_ON_BOOK | the bank bids in or takes the asset onto its books | Create the Asset and hand the case to the disposal route at D8 | TO_ASSET_DISPOSAL | Milestone | Sale officer | 5 working days |
| R-LIT-69 | Litigation | Timer sentry | NO_BID_AT_70 | ASSET_RETURNED_UNSOLD | the bank does not take the asset | Return to the enforcement decision for the next step | ENFORCEMENT_DECISION | Decision task | Enforcement owner | 5 working days |
| R-LIT-70 | Litigation | User sentry | PROCEEDS_MATCHED | BALANCE_SATISFIED | proceeds cover the judgment total and the costs | Close the enforcement and the case, and retain the record after close | CASE_CLOSED | Milestone | Case owner | None |
| R-LIT-71 | Litigation | Timer sentry | PROCEEDS_MATCHED | SHORTFALL_REMAINS | proceeds are less than the judgment total | Route the residual to debt sale or write-off at D8 or D9 | TO_WRITE_OFF | Milestone | Write-off team with Credit Administration | 10 working days |
| R-LIT-72 | Litigation | Timer sentry | PROCEEDS_MATCHED | NO_CASE_REFERENCE | proceeds arrive with no case reference | Hold the cash unmatched and raise a daily exception to the case owner | PROCEEDS_MATCHED | Human task | Case owner | 1 working day |
| R-LIT-73 | Litigation | User sentry | IN_HEARING | DEVIATION_RAISED | deviation_open in (X1, X2, X3, X4, X5, X7) | Pause the litigation timers and leave the prescription timer running | DEVIATION_HOLD | Event listener | Named deviation approver | None |
| R-LIT-74 | Litigation | User sentry | DEVIATION_HOLD | X1_RESOLVED | the complaint is resolved and not upheld | Resume the litigation at the state it paused in | IN_HEARING | Partner task | Panel law firm | None |
| R-LIT-75 | Litigation | Timer sentry | DEVIATION_HOLD | X1_UPHELD | the complaint is upheld against the debt | Withdraw the litigation and return the case to treatment | TO_TREATMENT | Milestone | Case owner | 5 working days |
| R-LIT-76 | Litigation | User sentry | DEVIATION_HOLD | X3_INSURANCE_SETTLED | credit life or mortgage insurance settles the balance | Withdraw the litigation and close the case | CASE_CLOSED | Milestone | Case owner | None |
| R-LIT-77 | Litigation | User sentry | DEVIATION_HOLD | X4_FRAUD_CONFIRMED | fraud confirmed in Aric | Stop the litigation and route the case to write-off at D9 | TO_WRITE_OFF | Milestone | Fraud team with the write-off team | None |
| R-LIT-78 | Litigation | Timer sentry | DEVIATION_HOLD | X5_BANKRUPTCY_DETECTED | a bankruptcy filing or a third-party seizure is detected | Stop direct collection and file the claim with the official receiver | OFFICIAL_RECEIVER_CLAIM | Partner task | Legal | To the receiver deadline |
| R-LIT-79 | Litigation | Timer sentry | DEVIATION_HOLD | X7_COLLATERAL_EVENT | collateral stolen, damaged, written off, or the insurance lapsed | Re-appraise the collateral and return the case to the route decision at D6 | TO_TREATMENT | Milestone | Case owner | 10 working days |
| R-GUA-01 | Guarantee claim | Timer sentry | GUARANTEE_DETECTED | GUARANTEE_FOUND | guarantee_type = TCG scheme and scheme_code present | Start the claim deadline timer from the date the default conditions are met | DEADLINE_TIMER_RUNNING | Human task | Workbench | To the claim deadline |
| R-GUA-02 | Guarantee claim | User sentry | GUARANTEE_DETECTED | CONDITIONS_NOT_MET | the scheme default conditions are not satisfied | Record that no claim arises and hold the guarantee | NOT_ELIGIBLE | Event listener | Guarantee officer | None |
| R-GUA-03 | Guarantee claim | Timer sentry | NOT_ELIGIBLE | CONDITIONS_LATER_MET | the default conditions are met at a later review | Start the claim deadline timer | DEADLINE_TIMER_RUNNING | Human task | Workbench | To the claim deadline |
| R-GUA-04 | Guarantee claim | Timer sentry | DEADLINE_TIMER_RUNNING | PREPARATION_DUE | days to claim_deadline <= the preparation window | The claim preparation agent assembles the claim against the scheme checklist | CLAIM_PREPARATION | Human task | Workbench | 5 working days |
| R-GUA-05 | Guarantee claim | User sentry | DEADLINE_TIMER_RUNNING | CLAIM_DEADLINE_MISSED | claim_deadline passed and claim_status is not submitted | Record the lost claim, the reason and the amount, and report the breach | DEADLINE_MISSED | Event listener | Guarantee officer | None |
| R-GUA-06 | Guarantee claim | Timer sentry | DEADLINE_TIMER_RUNNING | GUARANTOR_NOTICE_DUE | guarantee_type in (personal guarantor, co-borrower, corporate) | Issue the D6.6 guarantor notice with proof of delivery | GUARANTOR_NOTICE | Customer task | Guarantor | Notice period by product |
| R-GUA-07 | Guarantee claim | Timer sentry | CLAIM_PREPARATION | CHECKLIST_COMPLETE | every scheme checklist item is present | Present the claim to the guarantee officer for approval | CLAIM_APPROVAL | Human task | Guarantee officer | 3 working days |
| R-GUA-08 | Guarantee claim | Timer sentry | CLAIM_PREPARATION | CHECKLIST_INCOMPLETE | one or more checklist items are missing | Raise retrieval requests and hold the claim | CLAIM_DEFECT_HOLD | Event listener | Guarantee officer | 5 working days |
| R-GUA-09 | Guarantee claim | User sentry | CLAIM_PREPARATION | CLAIM_DEADLINE_MISSED | claim_deadline passed before submission | Record the lost claim and the reason, and report the breach | DEADLINE_MISSED | Event listener | Guarantee officer | None |
| R-GUA-10 | Guarantee claim | Timer sentry | CLAIM_DEFECT_HOLD | DOCUMENT_SUPPLIED | the missing items are supplied | Re-run the scheme checklist | CLAIM_PREPARATION | Human task | Workbench | 1 working day |
| R-GUA-11 | Guarantee claim | Timer sentry | CLAIM_DEFECT_HOLD | DEADLINE_WARNING | days to claim_deadline <= the warning window | Escalate to the guarantee officer and the Head of Litigation to submit with the gap recorded | CLAIM_APPROVAL | Human task | Head of Litigation | To the claim deadline |
| R-GUA-12 | Guarantee claim | Timer sentry | CLAIM_APPROVAL | CLAIM_APPROVED | the guarantee officer verifies the claim at D6.5 | Submit the claim through the TCG claim channel | CLAIM_SUBMITTED | Partner task | TCG | 2 working days |
| R-GUA-13 | Guarantee claim | Timer sentry | CLAIM_APPROVAL | CLAIM_SENT_BACK | the officer rejects the assembled claim | Return the claim to the preparation agent for rework | CLAIM_PREPARATION | Human task | Workbench | 2 working days |
| R-GUA-14 | Guarantee claim | Timer sentry | CLAIM_SUBMITTED | TCG_QUERY_RAISED | TCG asks for more information before assessment | Hold the claim and raise a task to the guarantee officer | TCG_QUERY | Event listener | Guarantee officer | To the TCG response date |
| R-GUA-15 | Guarantee claim | Timer sentry | TCG_QUERY | QUERY_ANSWERED | the requested information is supplied | Resubmit the claim | CLAIM_SUBMITTED | Partner task | TCG | 5 working days |
| R-GUA-16 | Guarantee claim | User sentry | TCG_QUERY | QUERY_UNANSWERED | the query response window has passed | Record the lapse and treat the claim as rejected | CLAIM_REJECTED | Event listener | Guarantee officer | None |
| R-GUA-17 | Guarantee claim | Timer sentry | CLAIM_SUBMITTED | CLAIM_REJECTED_BY_TCG | a rejection reason is returned | Record the rejection reason and assess a resubmission | CLAIM_REJECTED | Event listener | Guarantee officer | 5 working days |
| R-GUA-18 | Guarantee claim | Timer sentry | CLAIM_REJECTED | RESUBMISSION_POSSIBLE | the rejection reason is curable and claim_deadline has not passed | Rework the claim against the reason given | CLAIM_PREPARATION | Human task | Workbench | 5 working days |
| R-GUA-19 | Guarantee claim | User sentry | CLAIM_REJECTED | RESUBMISSION_NOT_POSSIBLE | the reason is not curable, or claim_deadline has passed | Close the guarantee and return the full balance to the route decision | RESIDUAL_TO_ROUTE | Milestone | Case owner | None |
| R-GUA-20 | Guarantee claim | Timer sentry | CLAIM_SUBMITTED | PART_PAYMENT_RECEIVED | claim_amount_paid < guaranteed_amount | Match the payment with source TCG and post it against the case | CLAIM_PART_PAID | Human task | Workbench | 2 working days |
| R-GUA-21 | Guarantee claim | Timer sentry | CLAIM_PART_PAID | BALANCE_CLAIMED | the unpaid share is still claimable inside the deadline | Submit the balance claim | CLAIM_SUBMITTED | Partner task | TCG | 5 working days |
| R-GUA-22 | Guarantee claim | Timer sentry | CLAIM_SUBMITTED | FULL_PAYMENT_RECEIVED | claim_amount_paid = guaranteed_amount | Match the payment, post it, and set the subrogation position | CLAIM_PAID | Human task | Workbench | 2 working days |
| R-GUA-23 | Guarantee claim | Timer sentry | CLAIM_PAID | SUBROGATION_DUE | TCG holds a share of every later recovery | Record the TCG share against the case for all future recoveries | SUBROGATION_POSITION | Human task | Guarantee officer | None |
| R-GUA-24 | Guarantee claim | Timer sentry | CLAIM_PART_PAID | SUBROGATION_DUE | TCG holds a share of every later recovery | Record the TCG share against the case for all future recoveries | SUBROGATION_POSITION | Human task | Guarantee officer | None |
| R-GUA-25 | Guarantee claim | Timer sentry | SUBROGATION_POSITION | RESIDUAL_REMAINS | the balance after the guaranteed share is greater than zero | Return the residual to the route decision at D6 | RESIDUAL_TO_ROUTE | Milestone | Case owner | 5 working days |
| R-GUA-26 | Guarantee claim | User sentry | SUBROGATION_POSITION | BALANCE_SATISFIED | the balance after the guaranteed share is zero | Close the guarantee and close the case | GUARANTEE_CLOSED | Milestone | Case owner | None |
| R-GUA-27 | Guarantee claim | Timer sentry | DEADLINE_MISSED | LOSS_RECORDED | the loss amount and the reason are recorded | Return the full balance to the route decision and close the guarantee | RESIDUAL_TO_ROUTE | Milestone | Case owner | 5 working days |
| R-GUA-28 | Guarantee claim | Timer sentry | GUARANTOR_NOTICE | GUARANTOR_SETTLED | the guarantor pays or agrees inside the approved range | Book the treatment, reduce the balance and close the guarantee | GUARANTEE_CLOSED | Milestone | Case owner | 5 working days |
| R-GUA-29 | Guarantee claim | User sentry | GUARANTOR_NOTICE | GUARANTOR_REFUSED | the guarantor refuses, or does not reply by the notice expiry | Record the refusal and return the case to the route decision | RESIDUAL_TO_ROUTE | Milestone | Case owner | None |
| R-GUA-30 | Guarantee claim | User sentry | GUARANTOR_NOTICE | GUARANTOR_DISPUTED | the guarantor disputes the guarantee itself | Raise X1, stop contact on the disputed item and hold the pursuit | GUARANTOR_DISPUTE_HOLD | Event listener | Complaint officer | None |
| R-GUA-31 | Guarantee claim | User sentry | GUARANTOR_DISPUTE_HOLD | X1_RESOLVED | the dispute is resolved and not upheld | Resume the guarantor pursuit from the notice | GUARANTOR_NOTICE | Customer task | Case owner | None |
| R-GUA-32 | Guarantee claim | Timer sentry | GUARANTOR_DISPUTE_HOLD | X1_UPHELD | the dispute is upheld against the guarantee | Release the guarantor and return the case to the route decision | RESIDUAL_TO_ROUTE | Milestone | Case owner | 5 working days |
| R-DIS-01 | Asset disposal | Timer sentry | ASSET_PENDING_TAKE_ON | REPOSSESSION_COMPLETED | asset_type = vehicle and statutory_notice_proved = Y | Create the asset record from RPS with condition, photographs and location | ASSET_ON_BOOKS | Human task | Sale officer | 1 working day |
| R-DIS-02 | Asset disposal | Timer sentry | ASSET_PENDING_TAKE_ON | DIL_TRANSFER_REGISTERED | asset_type = property and transfer registered | Create the asset record from AMIS with the opening book value | ASSET_ON_BOOKS | Human task | Sale officer | 1 working day |
| R-DIS-03 | Asset disposal | Timer sentry | ASSET_PENDING_TAKE_ON | LED_HANDOVER_RECEIVED | led_result = handed_over after the 100, 90, 80 then 70 percent ladder | Record the LED result and create the asset record | ASSET_ON_BOOKS | Human task | Sale officer | 1 working day |
| R-DIS-04 | Asset disposal | Timer sentry | ASSET_PENDING_TAKE_ON | STATUTORY_NOTICE_FAILED | delivery_proved = N | Hold the take-on, raise a failed notice task and re-serve on a confirmed address | FAILED_NOTICE_QUEUE | Event listener | Sale officer | 2 working days |
| R-DIS-05 | Asset disposal | System sentry | FAILED_NOTICE_QUEUE | NOTICE_REISSUED | new_address_confirmed = Y | Re-serve the statutory notice and resume the take-on | ASSET_PENDING_TAKE_ON | Human task | Workbench | None |
| R-DIS-06 | Asset disposal | User sentry | ASSET_ON_BOOKS | ASSET_RECORD_CONFIRMED | title_status in (clear, under_transfer) | Start the holding age clock and the provision step clock, and charge cost of carry monthly | ASSET_HELD | Human task | Sale officer | None |
| R-DIS-07 | Asset disposal | Timer sentry | ASSET_ON_BOOKS | TITLE_UNRESOLVED | title_status = encumbered or registration_status = blocked | Hold the asset and raise a title task | TITLE_BLOCKED | Event listener | Sale officer | 10 working days |
| R-DIS-08 | Asset disposal | User sentry | TITLE_BLOCKED | TITLE_CLEARED | title_status = clear | Release the asset to hold and to the disposal route | ASSET_HELD | Human task | Sale officer | None |
| R-DIS-09 | Asset disposal | Timer sentry | ASSET_HELD | PROVISION_STEP_DUE | holding_age reaches next_provision_step_date | Apply the provision step and send the input to Finance | ASSET_HELD | Human task | Workbench | None |
| R-DIS-10 | Asset disposal | Timer sentry | ASSET_HELD | WORK_ORDER_RAISED | storage, property tax, insurance, security or eviction required | Raise the work order to the property services vendor on the portal | WORK_ORDER_OPEN | Partner task | Property services vendor | per fee schedule |
| R-DIS-11 | Asset disposal | Timer sentry | WORK_ORDER_OPEN | WORK_ACCEPTED | sale_officer_accepted = Y | Release the invoice for payment and return the asset to hold | ASSET_HELD | Human task | Sale officer | 3 working days |
| R-DIS-12 | Asset disposal | User sentry | WORK_ORDER_OPEN | WORK_REFUSED | sale_officer_accepted = N | Block the invoice and return the work order to the vendor | WORK_ORDER_OPEN | Partner task | Property services vendor | None |
| R-DIS-13 | Asset disposal | User sentry | ASSET_HELD | OCCUPANTS_REFUSE_POSSESSION | occupancy_status = occupied | Raise the eviction instruction to Legal | EVICTION_REQUIRED | Human task | Litigation officer | None |
| R-DIS-14 | Asset disposal | User sentry | EVICTION_REQUIRED | POSSESSION_TAKEN | occupancy_status = vacant | Return the asset to hold and resume the disposal route | ASSET_HELD | Human task | Sale officer | None |
| R-DIS-15 | Asset disposal | Timer sentry | ASSET_HELD | REAPPRAISAL_CYCLE_DUE | appraisal_date older than 12 months and one_year_rule_applied = N | Order the re-appraisal through SVAF | REAPPRAISAL_ORDERED | Partner task | Valuer | 10 working days |
| R-DIS-16 | Asset disposal | Timer sentry | REAPPRAISAL_ORDERED | VALUER_REPORTED | Any | Record the value and run the valuation agent outlier check | REAPPRAISAL_RECEIVED | Human task | Sale officer | 2 working days |
| R-DIS-17 | Asset disposal | System sentry | REAPPRAISAL_RECEIVED | VALUE_ACCEPTED | outlier_flag = N or officer_accepted = Y | Update the appraised value and reset the list and floor price inputs | ASSET_HELD | Human task | Workbench | None |
| R-DIS-18 | Asset disposal | User sentry | REAPPRAISAL_RECEIVED | VALUE_REJECTED | officer_accepted = N | Re-order the appraisal and record the reason | REAPPRAISAL_ORDERED | Partner task | Valuer | None |
| R-DIS-19 | Asset disposal | Timer sentry | ASSET_HELD | READY_TO_SELL | current_appraisal = Y and title_status = clear | Pricing agent recommends the disposal route with reasons and the COLLINS economics | ROUTE_RECOMMENDED | Human task | Sale officer | 2 working days |
| R-DIS-20 | Asset disposal | Timer sentry | ROUTE_RECOMMENDED | ROUTE_SUBMITTED | Any | Route the recommendation to the approver by the delegation of authority | ROUTE_WITH_APPROVER | Decision task | Sale officer | 2 working days |
| R-DIS-21 | Asset disposal | User sentry | ROUTE_WITH_APPROVER | ROUTE_APPROVED | route = auction and inside the limit | Approve the portal auction route and log the decision | ROUTE_APPROVED_AUCTION | Human task | Sale officer | None |
| R-DIS-22 | Asset disposal | User sentry | ROUTE_WITH_APPROVER | ROUTE_APPROVED | route = auction and appraised_value above THB 50m | Send the asset to sealed bids and approve at committee | ROUTE_APPROVED_AUCTION | Human task | Committee | None |
| R-DIS-23 | Asset disposal | User sentry | ROUTE_WITH_APPROVER | ROUTE_APPROVED | route = RAMC and committee approved | Produce the transfer price from the governed template | ROUTE_APPROVED_RAMC | Human task | Sale officer | None |
| R-DIS-24 | Asset disposal | User sentry | ROUTE_WITH_APPROVER | ROUTE_APPROVED | route = buy_back and second_signature given | Agree the buy-back terms at the template price | ROUTE_APPROVED_BUYBACK | Human task | Sale officer | None |
| R-DIS-25 | Asset disposal | User sentry | ROUTE_WITH_APPROVER | ROUTE_APPROVED | route = rental | Set the rental terms and the auto-debit, and hold the asset as rented | RENTAL_ACTIVE | Human task | Sale officer | None |
| R-DIS-26 | Asset disposal | Timer sentry | ROUTE_WITH_APPROVER | ROUTE_APPROVED | route = broker and asset_type in (commercial_property, land) | Instruct the broker on the portal for a fixed term | BROKER_INSTRUCTED | Partner task | Broker | per instruction term |
| R-DIS-27 | Asset disposal | User sentry | ROUTE_WITH_APPROVER | ROUTE_REFUSED | approver_decision = refused | Return the asset to hold with the reason recorded | ASSET_HELD | Human task | Sale officer | None |
| R-DIS-28 | Asset disposal | Timer sentry | ROUTE_APPROVED_AUCTION | PRICE_MODEL_RUN | Any | Pricing agent proposes the opening price and the floor price as the reserve | PRICE_PROPOSED | Human task | Sale officer | 1 working day |
| R-DIS-29 | Asset disposal | System sentry | PRICE_PROPOSED | FLOOR_APPROVED_BY_OFFICER | officer_approved = Y | Fix the floor as the reserve and set the step schedule by asset class | FLOOR_APPROVED | Decision task | Workbench | None |
| R-DIS-30 | Asset disposal | Timer sentry | FLOOR_APPROVED | VENDOR_REQUIRED | asset_type = vehicle | Allocate the asset to the vendor with the highest predicted price on the scorecard, not by distance | VENDOR_ALLOCATED | Partner task | Auction and remarketing vendor | 2 working days |
| R-DIS-31 | Asset disposal | User sentry | VENDOR_ALLOCATED | VENDOR_UNAVAILABLE | vendor_capacity = N or panel_status = suspended | Re-allocate to the next vendor on the scorecard | VENDOR_ALLOCATED | Partner task | Partner and agency manager | None |
| R-DIS-32 | Asset disposal | Timer sentry | VENDOR_ALLOCATED | VENDOR_ACCEPTED | vendor_capacity = Y and inspection form complete | Vendor lists the asset at the starting bid on the portal | LISTING_LIVE | Human task | Auction and remarketing vendor | 2 working days |
| R-DIS-33 | Asset disposal | Timer sentry | FLOOR_APPROVED | LISTING_EVIDENCE_COMPLETE | photographs_count above 0 and inspection_report present and title_status = clear | Publish the listing to HOME.SCB, the EASY app and the auction portal, with the floor not published | LISTING_LIVE | Human task | Workbench | per asset class |
| R-DIS-34 | Asset disposal | Timer sentry | FLOOR_APPROVED | LISTING_EVIDENCE_MISSING | photographs_count = 0 or inspection_report absent | Block publication and raise a document task | LISTING_BLOCKED | Event listener | Sale officer | 5 working days |
| R-DIS-35 | Asset disposal | System sentry | LISTING_BLOCKED | EVIDENCE_SUPPLIED | photographs and inspection report present | Publish the listing | LISTING_LIVE | Human task | Workbench | None |
| R-DIS-36 | Asset disposal | Timer sentry | LISTING_LIVE | ROUND_OPENED | schedule step due | Open the round at the scheduled price step | ROUND_OPEN | Human task | Auction and remarketing vendor | per schedule |
| R-DIS-37 | Asset disposal | System sentry | ROUND_OPEN | BID_PLACED | Any | Record the bid against the round and the asset | BID_RECEIVED | Human task | Workbench | None |
| R-DIS-38 | Asset disposal | Timer sentry | ROUND_OPEN | ROUND_CLOSED_NO_BID | bid_count = 0 and price_at_round above floor_price | Step the price down on the published schedule and open the next round | ROUND_OPEN | Human task | Workbench | per schedule |
| R-DIS-39 | Asset disposal | User sentry | ROUND_OPEN | FLOOR_REACHED_NO_BID | bid_count = 0 and price_at_round = floor_price | Close the listing and raise the no-bid outcome | NO_BID_AT_FLOOR | Event listener | Sale officer | None |
| R-DIS-40 | Asset disposal | Timer sentry | BID_RECEIVED | BID_AT_OR_ABOVE_FLOOR | bid_amount at or above floor_price | Accept the bid and agree the sale | SALE_AGREED | Human task | Sale officer | 1 working day |
| R-DIS-41 | Asset disposal | Timer sentry | BID_RECEIVED | BID_BELOW_FLOOR | bid_amount below floor_price | Route the bid for a second signature | SECOND_SIGNATURE_PENDING | Decision task | Committee | 2 working days |
| R-DIS-42 | Asset disposal | User sentry | SECOND_SIGNATURE_PENDING | SECOND_SIGNATURE_GIVEN | second_signature_by present | Accept the bid below the floor and agree the sale | SALE_AGREED | Human task | Sale officer | None |
| R-DIS-43 | Asset disposal | User sentry | SECOND_SIGNATURE_PENDING | SECOND_SIGNATURE_REFUSED | second_signature_by absent | Reject the bid and re-list the asset | RELISTED | Human task | Sale officer | None |
| R-DIS-44 | Asset disposal | User sentry | NO_BID_AT_FLOOR | RELIST_RULE_APPLIED | relist_count below the re-list limit | Re-list the asset and order a re-appraisal where the cycle is due | RELISTED | Human task | Sale officer | None |
| R-DIS-45 | Asset disposal | Timer sentry | RELISTED | ROUTE_REVIEW_REQUIRED | Any | Send the asset back for a disposal route review | ROUTE_RECOMMENDED | Human task | Sale officer | 2 working days |
| R-DIS-46 | Asset disposal | User sentry | NO_BID_AT_FLOOR | RELIST_LIMIT_REACHED | relist_count at or above the re-list limit | Hand the asset and the residual to the debt sale route | TO_DEBT_SALE | Milestone | Debt sale officer | None |
| R-DIS-47 | Asset disposal | Timer sentry | SALE_AGREED | AWARD_MADE | Any | Start the five-day payment term | AWAITING_PAYMENT | Partner task | Buyer | 5 calendar days |
| R-DIS-48 | Asset disposal | User sentry | AWAITING_PAYMENT | PAYMENT_RECEIVED | payment_received_at at or before payment_due_date | Confirm the sale and start the title transfer | TITLE_TRANSFER_PENDING | Human task | Sale officer | None |
| R-DIS-49 | Asset disposal | Timer sentry | AWAITING_PAYMENT | PAYMENT_TERM_EXPIRED | payment absent and payment_due_date passed | Cancel the award, score the vendor and reopen the round | AWARD_CANCELED | Event listener | Sale officer | None |
| R-DIS-50 | Asset disposal | User sentry | AWARD_CANCELED | ROUND_REOPENED | Any | Reopen the round at the same price step | ROUND_OPEN | Human task | Auction and remarketing vendor | None |
| R-DIS-51 | Asset disposal | Timer sentry | TITLE_TRANSFER_PENDING | REGISTRATION_TRANSFERRED | asset_type = vehicle | Transfer the registration through SCIS | ASSET_SOLD | Human task | Workbench | 5 working days |
| R-DIS-52 | Asset disposal | Timer sentry | TITLE_TRANSFER_PENDING | TITLE_REGISTERED | asset_type = property | Release the documents from custody and record the transfer at the Land Office | ASSET_SOLD | Human task | Sale officer | 10 working days |
| R-DIS-53 | Asset disposal | Timer sentry | TITLE_TRANSFER_PENDING | TRANSFER_REJECTED | SCIS or the Land Office rejects the transfer | Hold the transfer and raise a document task | TITLE_BLOCKED | Event listener | Sale officer | 5 working days |
| R-DIS-54 | Asset disposal | Timer sentry | ASSET_SOLD | PROCEEDS_POSTED | Any | Apply the proceeds to the case and the loan account, and match the vendor fee | PROCEEDS_APPLIED | Human task | Workbench | same day |
| R-DIS-55 | Asset disposal | User sentry | PROCEEDS_APPLIED | SHORTFALL_CALCULATED | shortfall_amount above 0 | Raise the residual for the D9 decision | SHORTFALL_RAISED | Human task | Write-off team | None |
| R-DIS-56 | Asset disposal | System sentry | PROCEEDS_APPLIED | NO_SHORTFALL | shortfall_amount at or below 0 | Close the case and stop every timer | CASE_CLOSED_NO_SHORTFALL | Milestone | Workbench | None |
| R-DIS-57 | Asset disposal | User sentry | SHORTFALL_RAISED | RESIDUAL_ROUTED | residual_route = write_off | Hand the residual to the write-off route | TO_WRITEOFF | Milestone | Write-off committee | None |
| R-DIS-58 | Asset disposal | User sentry | SHORTFALL_RAISED | RESIDUAL_ROUTED | residual_route = debt_sale | Hand the residual to the debt sale route | TO_DEBT_SALE | Milestone | Debt sale officer | None |
| R-DIS-59 | Asset disposal | Timer sentry | ROUTE_APPROVED_RAMC | TRANSFER_INSTRUCTED | transfer_price from the template version | Instruct the RAMC or joint venture transfer on the portal | RAMC_TRANSFER_PENDING | Partner task | RAMC | per agreement |
| R-DIS-60 | Asset disposal | System sentry | RAMC_TRANSFER_PENDING | TRANSFER_COMPLETED | Any | Post the transfer and set the asset to transferred | ASSET_TRANSFERRED | Milestone | Workbench | None |
| R-DIS-61 | Asset disposal | User sentry | ROUTE_APPROVED_BUYBACK | BUYBACK_TERMS_SIGNED | customer_funded = Y | Complete the buy-back at the governed template price | SALE_AGREED | Human task | Sale officer | None |
| R-DIS-62 | Asset disposal | User sentry | ROUTE_APPROVED_BUYBACK | BUYBACK_FUNDING_FAILED | customer_funded = N | Return the asset to hold and review the route | ASSET_HELD | Human task | Sale officer | None |
| R-DIS-63 | Asset disposal | User sentry | RENTAL_ACTIVE | TENANT_DEFAULTED | rental_arrears above the threshold | Return the asset to the hold state for a route review | ASSET_HELD | Human task | Sale officer | None |
| R-DIS-64 | Asset disposal | User sentry | BROKER_INSTRUCTED | BROKER_SOLD | sale price at or above the approved floor | Complete the sale and pay the broker fee on acceptance | SALE_AGREED | Human task | Sale officer | None |
| R-DIS-65 | Asset disposal | Timer sentry | BROKER_INSTRUCTED | BROKER_TERM_EXPIRED | instruction_term passed and no sale | Withdraw the instruction and review the route | ROUTE_RECOMMENDED | Human task | Sale officer | None |
| R-DIS-66 | Asset disposal | User sentry | ASSET_HELD | DEVIATION_RAISED | deviation_open in (X1, X2, X3, X4, X5, X7) | Pause the disposal, stop contact where required and route to the deviation owner | DISPOSAL_PAUSED_DEVIATION | Event listener | Deviation owner | None |
| R-DIS-67 | Asset disposal | User sentry | LISTING_LIVE | DEVIATION_RAISED | deviation_open in (X1, X4, X5) | Pause the listing and the price schedule | DISPOSAL_PAUSED_DEVIATION | Event listener | Deviation owner | None |
| R-DIS-68 | Asset disposal | User sentry | DISPOSAL_PAUSED_DEVIATION | DEVIATION_CLEARED | deviation_open = none | Resume the asset at the state it paused in | ASSET_HELD | Human task | Sale officer | None |
| R-DIS-69 | Asset disposal | User sentry | DISPOSAL_PAUSED_DEVIATION | BANKRUPTCY_CONFIRMED | deviation = X5 | Hand the asset to the official receiver and close the disposal route | TO_WRITEOFF | Milestone | Legal | None |
| R-DIS-70 | Asset disposal | Timer sentry | ROUTE_WITH_APPROVER | ROUTE_APPROVED | route is not one of the five approved routes | Hold the case, name the missing field and raise a task for the owner | UNMATCHED_EXCEPTION | Event listener | Sale officer | same day |
| R-DIS-71 | Asset disposal | Timer sentry | SHORTFALL_RAISED | RESIDUAL_ROUTED | residual_route is not set | Hold the case, name the missing field and raise a task for the owner | UNMATCHED_EXCEPTION | Event listener | Sale officer | same day |
| R-DIS-72 | Asset disposal | Timer sentry | UNMATCHED_EXCEPTION | MANUAL_DECISION_RECORDED | Any | Sale officer records the decision and the missing field; the rule gap is logged for the center of excellence | ASSET_HELD | Human task | Sale officer | 2 working days |
| R-DS-01 | Debt sale | Timer sentry | LOT_CANDIDATE_SELECTED | DEBT_SALE_CYCLE_OPENED | eligibility rule passes and deviation_open = none | Select the accounts for sale from the case list | LOT_BUILT | Human task | Debt sale officer | per monthly cycle |
| R-DS-02 | Debt sale | User sentry | LOT_CANDIDATE_SELECTED | ACCOUNT_EXCLUDED | deviation_open in (X1 to X7) or fraud_flag = Y | Remove the account from the pool with a recorded reason | CASE_EXCLUDED | Event listener | Case owner | None |
| R-DS-03 | Debt sale | Timer sentry | CASE_EXCLUDED | EXCLUSION_CLEARED | deviation_open = none | Return the account to the case list for the next cycle | BACK_TO_CASE_LIST | Milestone | Debt sale officer | next cycle |
| R-DS-04 | Debt sale | Timer sentry | LOT_BUILT | LOT_PRICED | lot agent estimate returned with COLLINS | Propose the lots, the tiered buyer terms and the reserve price | LOT_WITH_COMMITTEE | Decision task | Committee | 5 working days |
| R-DS-05 | Debt sale | User sentry | LOT_BUILT | LOT_TOO_THIN | account_count below the minimum lot size | Merge the accounts into the next lot | LOT_BUILT | Human task | Debt sale officer | None |
| R-DS-06 | Debt sale | User sentry | LOT_WITH_COMMITTEE | LOT_APPROVED_BY_COMMITTEE | reserve and terms approved inside the delegation | Approve the lot, the reserve and the tiered terms, and log the decision | LOT_APPROVED | Human task | Debt sale officer | None |
| R-DS-07 | Debt sale | User sentry | LOT_WITH_COMMITTEE | RESERVE_RAISED | committee raises the reserve | Reprice the lot and return it to the committee | LOT_WITH_COMMITTEE | Decision task | Committee | None |
| R-DS-08 | Debt sale | User sentry | LOT_WITH_COMMITTEE | LOT_REFUSED | committee withdraws the lot | Withdraw the lot with a recorded reason | LOT_WITHDRAWN | Event listener | Debt sale officer | None |
| R-DS-09 | Debt sale | User sentry | LOT_WITHDRAWN | ACCOUNTS_RETURNED | Any | Return the accounts to the case list | BACK_TO_CASE_LIST | Milestone | Case owner | None |
| R-DS-10 | Debt sale | Timer sentry | LOT_APPROVED | TAPE_BUILD_RUN | Any | Build the masked data tape under the PII masking rules | TAPE_PREPARED | Human task | Workbench | 3 working days |
| R-DS-11 | Debt sale | System sentry | TAPE_PREPARED | MASKING_CHECK_FAILED | an unmasked identifier is found on the tape | Reject the tape and rebuild it | TAPE_REJECTED | Event listener | Workbench | None |
| R-DS-12 | Debt sale | System sentry | TAPE_REJECTED | TAPE_REBUILT | masking check passes | Return the tape for data room release | TAPE_PREPARED | Human task | Workbench | None |
| R-DS-13 | Debt sale | Timer sentry | TAPE_PREPARED | MASKING_CHECK_PASSED | no unmasked identifier | Open the data room to buyers who have signed the non-disclosure agreement | DATA_ROOM_OPEN | Human task | Debt sale officer | per cycle |
| R-DS-14 | Debt sale | Timer sentry | DATA_ROOM_OPEN | BUYER_REQUESTED_ACCESS | nda_signed_at present | Run the KYC, licensing and eligibility check on the bidder | BUYER_PENDING_KYC | Decision task | Workbench | 3 working days |
| R-DS-15 | Debt sale | User sentry | BUYER_PENDING_KYC | KYC_PASSED | kyc_status = passed and licence_expiry after today and panel_status = active | Admit the buyer to the data room | BUYER_CLEARED | Partner task | Buyer | None |
| R-DS-16 | Debt sale | User sentry | BUYER_PENDING_KYC | KYC_FAILED | kyc_status = failed or license expired or panel_status = suspended | Refuse access and record the reason | BUYER_REJECTED | Event listener | Debt sale officer | None |
| R-DS-17 | Debt sale | Timer sentry | BUYER_CLEARED | BIDDING_WINDOW_OPENED | Any | Open bidding on the lot at the tiered terms | BIDDING_OPEN | Partner task | Buyer | per cycle |
| R-DS-18 | Debt sale | System sentry | BIDDING_OPEN | BID_SUBMITTED | Any | Record the bid against the lot and the buyer | BIDS_RECEIVED | Human task | Workbench | None |
| R-DS-19 | Debt sale | Timer sentry | BIDS_RECEIVED | BIDDING_WINDOW_CLOSED | best_bid at or above reserve_price | Test the price against the reserve and the 54 percent cap, and route the award | AWARD_PENDING | Decision task | Debt sale officer | 2 working days |
| R-DS-20 | Debt sale | User sentry | BIDS_RECEIVED | BEST_BID_BELOW_RESERVE | best_bid below reserve_price | Raise the below-reserve outcome to the committee | BID_BELOW_RESERVE | Event listener | Debt sale officer | None |
| R-DS-21 | Debt sale | User sentry | BID_BELOW_RESERVE | LOT_REOFFERED | committee approves a re-offer at a revised reserve | Re-offer the lot at the revised reserve | BIDDING_OPEN | Partner task | Buyer | None |
| R-DS-22 | Debt sale | User sentry | BID_BELOW_RESERVE | LOT_NOT_CLEARED | committee refuses a re-offer | Withdraw the lot | LOT_WITHDRAWN | Event listener | Debt sale officer | None |
| R-DS-23 | Debt sale | User sentry | AWARD_PENDING | AWARD_CONFIRMED | price tested against the reserve and the 54 percent cap, and recorded | Award the lot and generate the sale agreement and the customer notices | LOT_AWARDED | Human task | Debt sale officer | None |
| R-DS-24 | Debt sale | Timer sentry | LOT_AWARDED | SETTLEMENT_TERM_STARTED | Any | Start the settlement term and await payment | SETTLEMENT_PENDING | Partner task | Buyer | per agreed settlement period |
| R-DS-25 | Debt sale | System sentry | SETTLEMENT_PENDING | BUYER_SETTLED | payment received in full | Confirm settlement and release the data transfer | SETTLED | Human task | Workbench | None |
| R-DS-26 | Debt sale | User sentry | SETTLEMENT_PENDING | BUYER_CANCELED | cancellation recorded with a reason | Cancel the award and score the cancellation against the buyer | AWARD_CANCELED_DS | Event listener | Debt sale officer | None |
| R-DS-27 | Debt sale | Timer sentry | SETTLEMENT_PENDING | SETTLEMENT_TERM_EXPIRED | payment absent and the settlement period passed | Cancel the award and score the buyer | AWARD_CANCELED_DS | Event listener | Debt sale officer | None |
| R-DS-28 | Debt sale | User sentry | AWARD_CANCELED_DS | LOT_REOFFERED_AFTER_CANCEL | another qualified bidder exists | Re-offer the lot to the next qualified bidder | BIDDING_OPEN | Partner task | Buyer | None |
| R-DS-29 | Debt sale | Timer sentry | SETTLED | DATA_TRANSFER_RUN | Any | Transfer the account data to the buyer | DATA_TRANSFERRED | Human task | Workbench | 5 working days |
| R-DS-30 | Debt sale | System sentry | DATA_TRANSFERRED | DERECOGNITION_RUN | Any | Derecognise the balance on the account | DERECOGNISED | Human task | Workbench | None |
| R-DS-31 | Debt sale | Timer sentry | DERECOGNISED | GL_POSTING_RUN | Any | Post to the general ledger and send the provision input to Finance | GL_POSTED | Human task | Credit Administration | month-end close |
| R-DS-32 | Debt sale | Timer sentry | DERECOGNISED | POSTING_REJECTED | ALS or the general ledger rejects the posting | Hold the posting and raise an exception task | POSTING_REJECTED_DS | Event listener | Credit Administration | 2 working days |
| R-DS-33 | Debt sale | User sentry | POSTING_REJECTED_DS | POSTING_CORRECTED | the rejection cause is cleared | Re-post to ALS and the general ledger | GL_POSTED | Human task | Credit Administration | None |
| R-DS-34 | Debt sale | Timer sentry | GL_POSTED | CLAIM_WINDOW_CLOSED | no put-back claim inside the claim window | Close the lot and record realized recovery by lot and by buyer | LOT_CLOSED | Milestone | Debt sale officer | per claim window |
| R-DS-35 | Debt sale | Timer sentry | GL_POSTED | PUTBACK_CLAIMED | buyer raises a claim inside the sale terms | Record the claim and review it against the terms | PUTBACK_RAISED | Partner task | Debt sale officer | 10 working days |
| R-DS-36 | Debt sale | User sentry | PUTBACK_RAISED | PUTBACK_ACCEPTED | the claim is valid under the sale terms | Return the account to the bank and adjust the settlement | PUTBACK_UPHELD | Human task | Debt sale officer | None |
| R-DS-37 | Debt sale | User sentry | PUTBACK_UPHELD | ACCOUNT_RETURNED | Any | Reverse the derecognition and return the account to the case list | BACK_TO_CASE_LIST | Milestone | Case owner | None |
| R-DS-38 | Debt sale | User sentry | PUTBACK_RAISED | PUTBACK_REFUSED_BY_BANK | the claim falls outside the sale terms | Refuse the claim with a recorded reason | PUTBACK_REFUSED | Human task | Debt sale officer | None |
| R-DS-39 | Debt sale | User sentry | PUTBACK_REFUSED | CLAIM_CLOSED | Any | Close the lot with realized recovery recorded | LOT_CLOSED | Milestone | Debt sale officer | None |
| R-DS-40 | Debt sale | Timer sentry | BUYER_REJECTED | BUYER_REMEDIATED | the buyer supplies the missing KYC or license evidence inside the window | Re-open the qualification check | BUYER_PENDING_KYC | Decision task | Debt sale officer | 10 working days |
| R-DS-41 | Debt sale | User sentry | BUYER_REJECTED | BUYER_BARRED | no evidence supplied inside the window, or the failure is a license breach | Remove the buyer from the panel and release the lot to the next bidder | BACK_TO_CASE_LIST | Milestone | Head of Asset Liquidity | None |
| R-WO-01 | Write-off | Timer sentry | SCAN_DUE | MONTHLY_SCAN_STARTED | cut_off_date reached and the ALS load is complete | Test every open case against the eligibility rule on both tracks and the tax criteria | POPULATION_PROPOSED | Human task | Write-off team | monthly cut-off |
| R-WO-02 | Write-off | Timer sentry | SCAN_DUE | ALS_LOAD_FAILED | the ALS extract is absent for the cut-off date | Hold the scan and raise an incident | SCAN_HELD | Event listener | Write-off team | 1 working day |
| R-WO-03 | Write-off | User sentry | SCAN_DUE | TAX_CRITERIA_UNPUBLISHED | tax_criteria_version absent | Hold the scan until Finance publishes the version | SCAN_HELD | Event listener | Write-off team | None |
| R-WO-04 | Write-off | System sentry | SCAN_HELD | LOAD_RESTORED | the ALS extract is complete and the tax criteria published | Restart the scan for the cut-off date | SCAN_DUE | Human task | Workbench | None |
| R-WO-05 | Write-off | Timer sentry | POPULATION_PROPOSED | PACK_BUILT | Any | Write-off agent prepares the pack: balance, provision carried, route history, legal and asset state, residual | PACK_PREPARED | Human task | Write-off team | 3 working days |
| R-WO-06 | Write-off | User sentry | POPULATION_PROPOSED | CASE_HAS_OPEN_DEVIATION | deviation_open in (X1 to X7) | Hold the case out of the population and route it to the deviation handler | CASE_REMOVED_BY_TEAM | Event listener | Deviation owner | None |
| R-WO-07 | Write-off | User sentry | POPULATION_PROPOSED | TEAM_REMOVED_CASE | removal_reason present | Remove the case from the proposed population with the reason recorded | CASE_REMOVED_BY_TEAM | Event listener | Write-off team | None |
| R-WO-08 | Write-off | Timer sentry | CASE_REMOVED_BY_TEAM | REMOVAL_CLEARED | the deviation is cleared or the reason is resolved | Return the case to the next monthly scan | SCAN_DUE | Human task | Write-off team | next cut-off |
| R-WO-09 | Write-off | Timer sentry | PACK_PREPARED | PACK_CHECK_FAILED | provision_carried absent or pack_document_id absent | Hold the pack and raise a data quality task | PACK_INCOMPLETE | Event listener | Write-off team | 2 working days |
| R-WO-10 | Write-off | User sentry | PACK_INCOMPLETE | PACK_COMPLETED | provision_carried and the pack document are present | Route the pack to the committee | WITH_COMMITTEE | Decision task | Write-off committee | None |
| R-WO-11 | Write-off | Timer sentry | PACK_PREPARED | PACK_ROUTED | amount inside the write-off committee limit | Route the pack to the committee and schedule the meeting | WITH_COMMITTEE | Decision task | Write-off committee | before the scheduled meeting |
| R-WO-12 | Write-off | Timer sentry | PACK_PREPARED | LIMIT_EXCEEDED | amount above the write-off committee limit | Route the pack to the credit approval committee chaired by the product head with Risk | ESCALATED_TO_CREDIT_COMMITTEE | Decision task | Credit approval committee | before the scheduled meeting |
| R-WO-13 | Write-off | User sentry | ESCALATED_TO_CREDIT_COMMITTEE | CREDIT_COMMITTEE_APPROVED | approved inside the delegation with Risk | Record the final call and release the case to posting | APPROVED | Human task | Credit Administration | None |
| R-WO-14 | Write-off | User sentry | ESCALATED_TO_CREDIT_COMMITTEE | CREDIT_COMMITTEE_REJECTED | decision_reason present | Return the case to the pursue track | RETURNED_TO_PURSUE | Milestone | Case owner | None |
| R-WO-15 | Write-off | User sentry | WITH_COMMITTEE | COMMITTEE_APPROVED | approved inside the delegation | Record the final call, the approver and the limit applied, and release to posting | APPROVED | Human task | Credit Administration | None |
| R-WO-16 | Write-off | User sentry | WITH_COMMITTEE | COMMITTEE_REJECTED | decision_reason present | Return the case to the pursue track | RETURNED_TO_PURSUE | Milestone | Case owner | None |
| R-WO-17 | Write-off | Timer sentry | WITH_COMMITTEE | COMMITTEE_DEFERRED | review_date present | Set the review timer and hold the case for the next scan | DEFERRED | Event listener | Write-off team | to the review date |
| R-WO-18 | Write-off | User sentry | WITH_COMMITTEE | DECISION_INCOMPLETE | decision_reason absent on a reject, or review_date absent on a defer | Refuse the decision and return it to the committee | WITH_COMMITTEE | Decision task | Write-off committee | None |
| R-WO-19 | Write-off | Timer sentry | DEFERRED | REVIEW_DATE_REACHED | Any | Return the case to the next monthly scan | SCAN_DUE | Human task | Write-off team | next cut-off |
| R-WO-20 | Write-off | Timer sentry | APPROVED | POSTING_TASK_CREATED | the posting window is open and no unmatched payment is in flight | Create the posting task | POSTING_PENDING | Human task | Credit Administration | month-end close window |
| R-WO-21 | Write-off | User sentry | POSTING_PENDING | ALS_POSTING_CONFIRMED | ALS and the general ledger return a reference | Record the posting reference | POSTED | Human task | Credit Administration | None |
| R-WO-22 | Write-off | Timer sentry | POSTING_PENDING | ALS_POSTING_REJECTED | result = rejected | Hold the posting and raise the rejection | POSTING_REJECTED | Event listener | Credit Administration | 2 working days |
| R-WO-23 | Write-off | User sentry | POSTING_REJECTED | REJECTION_CLEARED | retry_count below the retry limit and the cause is cleared | Re-post to ALS and the general ledger | POSTING_PENDING | Human task | Credit Administration | None |
| R-WO-24 | Write-off | Timer sentry | POSTING_REJECTED | RETRY_LIMIT_REACHED | retry_count at or above the retry limit | Raise the write-off exception for correction | WRITEOFF_EXCEPTION | Event listener | Owner to confirm with C&R | to confirm with Credit Administration |
| R-WO-25 | Write-off | System sentry | POSTED | PROVISION_RELEASE_RUN | provision_carried present | Release the provision carried and record the released amount | PROVISION_RELEASED | Human task | Workbench | None |
| R-WO-26 | Write-off | Timer sentry | PROVISION_RELEASED | FINANCE_FEED_RUN | Any | Send the provision inputs and the tax file to Finance | FINANCE_FEED_SENT | Human task | Credit Administration | month-end close |
| R-WO-27 | Write-off | Timer sentry | FINANCE_FEED_SENT | FINANCE_REJECTED_FILE | finance_feed_status = rejected | Retry the feed and raise a task after the retry limit | FINANCE_FEED_REJECTED | Event listener | Credit Administration | 2 working days |
| R-WO-28 | Write-off | User sentry | FINANCE_FEED_REJECTED | FEED_ACCEPTED_ON_RETRY | finance_feed_status = accepted | Record the tax file reference | FINANCE_FEED_SENT | Human task | Credit Administration | None |
| R-WO-29 | Write-off | Timer sentry | FINANCE_FEED_SENT | POST_CHARGEOFF_RULE_RUN | finance_feed_status = accepted | Decide the post charge-off treatment under D9.3 | PLACEMENT_DECIDED | Decision task | Partner and agency manager | 5 working days |
| R-WO-30 | Write-off | Timer sentry | PLACEMENT_DECIDED | SOFT_RECOVERY_SELECTED | placement_type = soft_recovery and an agency on the panel has capacity | Place the account with the agency chosen on measured return and send the instruction | PLACED_WITH_AGENCY | Partner task | Outsourced agency | same day on the portal |
| R-WO-31 | Write-off | Timer sentry | PLACEMENT_DECIDED | NO_AGENCY_CAPACITY | no agency on the panel has capacity | Hold the placement and escalate on the timer | PLACEMENT_DECIDED | Decision task | Partner and agency manager | 5 working days |
| R-WO-32 | Write-off | Timer sentry | PLACEMENT_DECIDED | SALE_SELECTED | placement_type = sale | Hand the charged-off population to the debt sale route | SOLD_POST_CHARGEOFF | Partner task | Debt sale officer | per cycle |
| R-WO-33 | Write-off | Timer sentry | PLACED_WITH_AGENCY | AGENCY_REPORTED_RESULT | the result is reported on the portal | Attach contact, promise and cash to the case the same day | PLACED_WITH_AGENCY | Partner task | Outsourced agency | same day |
| R-WO-34 | Write-off | User sentry | PLACED_WITH_AGENCY | AGENCY_UNDERPERFORMS | measured return below the panel threshold or conduct_breaches above 0 | Recall the placement and record the reason | PLACEMENT_RECALLED | Event listener | Partner and agency manager | None |
| R-WO-35 | Write-off | User sentry | PLACEMENT_RECALLED | REPLACEMENT_MADE | another agency on the panel has capacity | Place the account with the next agency on the scorecard | PLACED_WITH_AGENCY | Partner task | Outsourced agency | None |
| R-WO-36 | Write-off | Timer sentry | PLACED_WITH_AGENCY | PLACEMENT_TERM_EXPIRED | ends_at passed and recovered_amount = 0 | Close the placement and start the retention timer | RETENTION_RUNNING | Human task | Workbench | None |
| R-WO-37 | Write-off | Timer sentry | PLACED_WITH_AGENCY | PAYMENT_RECEIVED_AFTER_CHARGEOFF | the payment matches the case and the placement | Post the recovery as post charge-off income and calculate the agency fee | PAYMENT_MATCHED | Human task | Workbench | next working day |
| R-WO-38 | Write-off | Timer sentry | PLACED_WITH_AGENCY | PAYMENT_MATCHES_NOTHING | the payment matches no case and no placement | Send the payment to the exception list for clearing | PAYMENT_EXCEPTION | Event listener | Case owner | 2 working days |
| R-WO-39 | Write-off | System sentry | PAYMENT_EXCEPTION | EXCEPTION_CLEARED | the case or the placement is identified | Match the payment and post the income | PAYMENT_MATCHED | Human task | Workbench | None |
| R-WO-40 | Write-off | Timer sentry | SOLD_POST_CHARGEOFF | PAYMENT_BELONGS_TO_BUYER | the account was sold before the payment arrived | Remit the payment to the buyer under the remittance rule | REMITTED_TO_BUYER | Human task | Debt sale officer | 5 working days |
| R-WO-41 | Write-off | Timer sentry | PAYMENT_MATCHED | WRITEOFF_QUESTIONED | the payment reopens a question on the write-off | Raise the exception and refer it to the committee | WRITEOFF_EXCEPTION | Event listener | Owner to confirm with C&R | to confirm with Credit Administration |
| R-WO-42 | Write-off | Timer sentry | POSTED | POPULATION_RECONCILED | approved count and amount equal posted count and amount | Publish completeness and start the retention timer | RETENTION_RUNNING | Human task | Workbench | monthly |
| R-WO-43 | Write-off | Timer sentry | POSTED | POPULATION_NOT_RECONCILED | approved and posted populations differ | Fire the exception and report completeness short | WRITEOFF_EXCEPTION | Event listener | Owner to confirm with C&R | to confirm with Credit Administration |
| R-WO-44 | Write-off | Timer sentry | WRITEOFF_EXCEPTION | CORRECTION_REPOST | the owner decides to re-post | Re-post to ALS and the general ledger | POSTING_PENDING | Human task | Credit Administration | to confirm with Credit Administration |
| R-WO-45 | Write-off | Timer sentry | WRITEOFF_EXCEPTION | CORRECTION_RETURN_TO_SCAN | the owner decides to return the case | Return the case to the next monthly scan | SCAN_DUE | Human task | Write-off team | next cut-off |
| R-WO-46 | Write-off | User sentry | WRITEOFF_EXCEPTION | CORRECTION_REFER_TO_COMMITTEE | the owner refers the case back | Return the pack to the committee | WITH_COMMITTEE | Decision task | Write-off committee | None |
| R-WO-47 | Write-off | Timer sentry | RETENTION_RUNNING | RETENTION_TIMER_EXPIRED | no open placement, no open sale, no open exception, and a retention class on every document | Close the case, stop every timer and write the closing entry with cash recovered and loss | CASE_CLOSED | Milestone | Workbench | on expiry |
| R-WO-48 | Write-off | Timer sentry | RETENTION_RUNNING | RETENTION_CLASS_MISSING | a document on the case has no retention class | Hold closure and raise a Document Hub task | RETENTION_RUNNING | Human task | Operational Excellence | 5 working days |
| R-WO-49 | Write-off | Timer sentry | CASE_CLOSED | PAYMENT_RECEIVED_AFTER_CHARGEOFF | the payment matches a closed case with no placement | Post the recovery as post charge-off income against the closed case | PAYMENT_MATCHED | Human task | Workbench | next working day |
| R-WO-50 | Write-off | User sentry | SOLD_POST_CHARGEOFF | SALE_SETTLED | buyer settles and the data transfer completes | Record the post charge-off sale and close the case | CASE_CLOSED | Milestone | Credit Administration | None |
| R-WO-51 | Write-off | Timer sentry | REMITTED_TO_BUYER | REMITTANCE_CONFIRMED | the buyer confirms receipt | Record the remittance against the sold account and close the item | CASE_CLOSED | Milestone | Credit Administration | 5 working days |
| R-DEV-01 | Deviations | Timer sentry | ANY_STATE | DEVIATION_FLAGGED | deviation_code in (X1..X7) | Pause the stage clock, keep the prescription clock running, route to the named owner | DEV_FLAGGED | Human task | Workbench | same day |
| R-DEV-02 | Deviations | User sentry | DEV_FLAGGED | OWNER_ASSIGNED | deviation_code = X1 | Assign to the complaint officer | DEV_WITH_OWNER | Human task | Complaint officer | None |
| R-DEV-03 | Deviations | User sentry | DEV_FLAGGED | OWNER_ASSIGNED | deviation_code in (X2,X3) | Assign to the specialist; Legal joins X3 for the estate claim | DEV_WITH_OWNER | Human task | Specialist, Legal | None |
| R-DEV-04 | Deviations | User sentry | DEV_FLAGGED | OWNER_ASSIGNED | deviation_code = X4 | Assign to the fraud team and refer to Aric | DEV_WITH_OWNER | Human task | Fraud team | None |
| R-DEV-05 | Deviations | Timer sentry | DEV_FLAGGED | OWNER_ASSIGNED | deviation_code = X5 | Assign to Legal; file with the official receiver or the LED before the deadline | DEV_WITH_OWNER | Human task | Legal | deadline driven |
| R-DEV-06 | Deviations | System sentry | DEV_FLAGGED | OWNER_ASSIGNED | deviation_code in (X6,X7) | Agent handles within policy; a person approves an insurance claim | DEV_WITH_OWNER | Human task | Agent, case owner | None |
| R-DEV-07 | Deviations | System sentry | DEV_FLAGGED | FLAG_REJECTED | owner marks the flag as not a deviation | Clear the flag, record the reason, resume the clock | DEV_REJECTED | Human task | Workbench | None |
| R-DEV-08 | Deviations | User sentry | DEV_REJECTED | CLOCK_RESUMED | Any | Return the case to the state it paused in | RESUMED | Milestone | Previous owner | None |
| R-DEV-09 | Deviations | User sentry | DEV_WITH_OWNER | DEVIATION_RESOLVED | deviation_code in (X1,X7) | Record the outcome; the same decision resumes | DEV_RESOLVED | Human task | Case owner | None |
| R-DEV-10 | Deviations | User sentry | DEV_WITH_OWNER | DEVIATION_RESOLVED | deviation_code = X2 | Route to the restructure assessment | DEV_REROUTE | Decision task | Restructuring officer | None |
| R-DEV-11 | Deviations | System sentry | DEV_WITH_OWNER | INSURANCE_SETTLED | deviation_code = X3 and insurance clears the balance | Close the case | CASE_ENDED | Milestone | Workbench | None |
| R-DEV-12 | Deviations | User sentry | DEV_WITH_OWNER | ESTATE_CONFIRMED | deviation_code = X3 and insurance does not clear | Return to the route decision against the estate | DEV_REROUTE | Decision task | Case owner | None |
| R-DEV-13 | Deviations | User sentry | DEV_WITH_OWNER | FRAUD_CONFIRMED | deviation_code = X4 and fraud confirmed | Route to write-off; recovery continues under the fraud case | DEV_REROUTE | Decision task | Write-off team | None |
| R-DEV-14 | Deviations | User sentry | DEV_WITH_OWNER | FRAUD_NOT_CONFIRMED | deviation_code = X4 and fraud not confirmed | Return to the collections decision | DEV_REROUTE | Decision task | Case owner | None |
| R-DEV-15 | Deviations | User sentry | DEV_WITH_OWNER | BANKRUPTCY_FILED | deviation_code = X5 | Route to litigation, then to write-off after the receiver reports | DEV_REROUTE | Decision task | Legal, litigation officer | None |
| R-DEV-16 | Deviations | User sentry | DEV_WITH_OWNER | CONTACT_RESTORED | deviation_code = X6 and a contact point is verified | Close X6 and return to the paused state | DEV_RESOLVED | Human task | Case owner | None |
| R-DEV-17 | Deviations | Timer sentry | DEV_WITH_OWNER | CONTACT_NOT_FOUND | deviation_code = X6 and skip trace exhausted | Route to escalation or to the route decision | DEV_REROUTE | Decision task | Case owner | 30 days |
| R-DEV-18 | Deviations | User sentry | DEV_RESOLVED | CLOCK_RESUMED | Any | Resume the stage clock and return the case | RESUMED | Milestone | Previous owner | None |
| R-DEV-19 | Deviations | User sentry | DEV_REROUTE | ROUTE_REOPENED | Any | Recompute the segment and re-run the hard gates | ROUTE_D6 | Milestone | Case owner | None |
| R-DEV-20 | Deviations | Timer sentry | DEV_WITH_OWNER | SLA_BREACHED | time in DEV_WITH_OWNER exceeds the deviation service level | Escalate to the team manager and report the breach | DEV_WITH_OWNER | Human task | Team manager | 10 working days |
| R-DEV-21 | Deviations | Timer sentry | DEV_FLAGGED | OWNER_ASSIGNED | deviation_code is not one of X1 to X7, or no owner is set for the code | Assign to the case owner's team manager and log the unmapped code | DEV_WITH_OWNER | Human task | Team manager | same day |
| R-DEV-22 | Deviations | Timer sentry | DEV_WITH_OWNER | DEVIATION_RESOLVED | otherwise, the outcome does not name a next step | Return the case to the route decision and record that the outcome was not mapped | DEV_REROUTE | Decision task | Case owner | 2 working days |
| R-UNI-01 | Universal rules | Timer sentry | ANY_ACTIVE | PAYMENT_RECEIVED | arrears cleared in full and days_past_due falls below 90 | Close the recovery case, hand the account back to servicing, release any hold | CASE_CURED_CLOSED | Milestone | Case owner | same day |
| R-UNI-02 | Universal rules | Timer sentry | ANY_ACTIVE | PAYMENT_RECEIVED | part payment that changes the exposure band | Recompute the segment and re-run the owner ladder and the hard gates | ROUTE_D6_REOPEN | Milestone | Case owner | 1 working day |
| R-UNI-03 | Universal rules | Timer sentry | ANY_ACTIVE | PAYMENT_RECEIVED | otherwise, the payment matches no plan, sale or lot | Hold the cash on the exception list for the reconciliation agent | EXCEPTION_QUEUE | Event listener | Case owner | 2 working days |
| R-UNI-04 | Universal rules | Timer sentry | ANY_ACTIVE | COMPLAINT_RAISED | a complaint is logged against the case | Raise X1, pause the stage clock, apply the contact stop | HELD_DEVIATION | Human task | Complaint officer | same day |
| R-UNI-05 | Universal rules | Timer sentry | ANY_ACTIVE | CUSTOMER_DECEASED | a death is confirmed from the registry or a document | Raise X3, stop all contact, hold the case for the specialist and Legal | HELD_DEVIATION | Human task | Specialist, Legal | same day |
| R-UNI-06 | Universal rules | Timer sentry | ANY_ACTIVE | VULNERABILITY_IDENTIFIED | hardship or vulnerability is recorded | Raise X2, apply the vulnerable customer treatment rules | HELD_DEVIATION | Human task | Specialist | same day |
| R-UNI-07 | Universal rules | Timer sentry | ANY_ACTIVE | BANKRUPTCY_NOTIFIED | a filing or an external seizure is notified | Raise X5, stop enforcement, start the claim deadline clock | HELD_DEVIATION | Human task | Legal | deadline driven |
| R-UNI-08 | Universal rules | Timer sentry | ANY_ACTIVE | FRAUD_FLAGGED | Aric or an officer flags fraud | Raise X4, hold the case, refer to the fraud team | HELD_DEVIATION | Human task | Fraud team | same day |
| R-UNI-09 | Universal rules | Timer sentry | ANY_ACTIVE | DEBT_DISPUTED | the customer disputes the balance or the security | Raise X1, pause recovery action on the disputed amount | HELD_DEVIATION | Human task | Complaint officer | same day |
| R-UNI-10 | Universal rules | Timer sentry | ANY_ACTIVE | CONSENT_WITHDRAWN | the customer withdraws consent for a channel | Remove that channel from the contact plan, keep the statutory notices | HELD_CONDUCT | Human task | Conduct and QA officer | same day |
| R-UNI-11 | Universal rules | Timer sentry | ANY_ACTIVE | DATA_SUBJECT_REQUEST | a PDPA access, correction or erasure request is received | Hold automated processing on the case, route to Compliance inside the statutory period | HELD_LEGAL | Human task | Compliance | statutory period |
| R-UNI-12 | Universal rules | Timer sentry | ANY_ACTIVE | CONTACT_DETAIL_CHANGED | a new verified contact point arrives | Update the contact data product, close X6 if it is open | RESUME_STATE | Milestone | Workbench | same day |
| R-UNI-13 | Universal rules | Timer sentry | ANY_ACTIVE | RELIEF_SCHEME_APPLIED | the account qualifies for a government or bank relief scheme | Apply the scheme terms, pause recovery for the scheme period | HELD_LEGAL | Human task | Risk | scheme terms |
| R-UNI-14 | Universal rules | Timer sentry | ANY_ACTIVE | ROUTE_OVERRIDDEN | an authorized user overrides the route inside the delegation | Record the coded reason, move the case to the chosen route | ROUTE_D6_REOPEN | Milestone | Case owner | same day |
| R-UNI-15 | Universal rules | Timer sentry | ANY_ACTIVE | OVERRIDE_REFUSED | the override is outside the user's limit | Refuse the change, raise the request to the approver named in the matrix | ESCALATED | Human task | Approver per the matrix | 1 working day |
| R-UNI-16 | Universal rules | Timer sentry | ANY_ACTIVE | CASE_CREATED_IN_ERROR | the entry rule fired on bad data and the account is not eligible | Cancel the case with a reason, return the account to collections, keep the audit trail | CANCELED_IN_ERROR | Milestone | Case owner | 2 working days |
| R-UNI-17 | Universal rules | Timer sentry | ANY_ACTIVE | DUPLICATE_CASE_FOUND | two cases exist for the same customer and product | Merge into the earlier case, carry the documents and the decision log, close the later one | MERGED | Milestone | Case owner | 2 working days |
| R-UNI-18 | Universal rules | Timer sentry | ANY_ACTIVE | OWNER_UNAVAILABLE | the owner leaves, is absent beyond the threshold, or the account is reassigned | Reallocate inside the same team by region and workload, keep the state and the clocks | REALLOCATED | Human task | Team manager | 1 working day |
| R-UNI-19 | Universal rules | Timer sentry | ANY_ACTIVE | CASELOAD_CAP_BREACHED | the owner is above the maximum caseload | Reallocate the newest cases until the owner is inside the cap | REALLOCATED | Human task | Team manager | weekly |
| R-UNI-20 | Universal rules | Timer sentry | ANY_ACTIVE | LEGAL_HOLD_PLACED | a regulator, court or Legal places a hold | Stop every outbound action and every automated decision, keep the clocks visible | HELD_LEGAL | Human task | Legal | until lifted |
| R-UNI-21 | Universal rules | Timer sentry | HELD_LEGAL | LEGAL_HOLD_LIFTED | the hold is lifted | Resume the case in the state it paused in, recompute the timers | RESUME_STATE | Milestone | Case owner | same day |
| R-UNI-22 | Universal rules | Timer sentry | ANY_ACTIVE | CLASSIFICATION_CHANGED | the account is re-aged or reclassified upstream | Recompute the segment, re-run the gates, record the change | ROUTE_D6_REOPEN | Milestone | Workbench | 1 working day |
| R-UNI-23 | Universal rules | Timer sentry | ANY_ACTIVE | PRODUCT_MIGRATED | the account moves from ALS to iCore or between systems | Re-point the integration, reconcile the balance, keep the case and its state | RESUME_STATE | Milestone | Platform team | 1 working day |
| R-UNI-24 | Universal rules | Timer sentry | ANY_ACTIVE | CORRECTION_RECORDED | a booked decision is corrected after the event | Write a correcting decision log entry naming the original, never overwrite it | RESUME_STATE | Milestone | Case owner | same day |
| R-UNI-25 | Universal rules | Timer sentry | ANY_ACTIVE | PARTNER_NO_RESPONSE | the partner misses the service level on the portal | Chase once, then recall the work and re-select on the scorecard | PARTNER_RECALLED | Human task | Partner and agency manager | per partner type |
| R-UNI-26 | Universal rules | Timer sentry | ANY_ACTIVE | PARTNER_PANEL_EXIT | the partner leaves the panel or the contract ends | Recall every open case held by that partner and re-select | PARTNER_RECALLED | Human task | Partner and agency manager | 5 working days |
| R-UNI-27 | Universal rules | Timer sentry | ANY_ACTIVE | PARTNER_CONFLICT_DECLARED | the partner declares a conflict of interest | Withdraw the instruction, re-select the next partner on the scorecard | PARTNER_RECALLED | Human task | Partner and agency manager | 2 working days |
| R-UNI-28 | Universal rules | Timer sentry | ANY_ACTIVE | PARTNER_INSOLVENT | the partner enters insolvency | Recall the work, secure the documents and any cash held, stop fee payments | PARTNER_RECALLED | Human task | Head of the partner type | same day |
| R-UNI-29 | Universal rules | Timer sentry | ANY_ACTIVE | PARTNER_CONDUCT_BREACH | a conduct or complaint breach is upheld against the partner | Suspend allocation, recall the affected cases, report to the partner review | PARTNER_RECALLED | Human task | Partner and agency manager | same day |
| R-UNI-30 | Universal rules | Timer sentry | ANY_ACTIVE | SLA_BREACHED | time in the current state exceeds the service level | Raise the breach to the named escalation point. The case does not move | ESCALATED | Human task | Team manager | per state |
| R-UNI-31 | Universal rules | Timer sentry | ANY_ACTIVE | PRESCRIPTION_WARNING | prescription_days_remaining reaches the warning threshold | Force a litigation review ahead of every other open action | ROUTE_D6_REOPEN | Milestone | Litigation officer | immediate |
| R-UNI-32 | Universal rules | Timer sentry | ANY_ACTIVE | AGENT_UNAVAILABLE | the agent or the model does not answer inside the timeout | Fall back to the rule result and continue. Record the fallback on the decision | RESUME_STATE | Milestone | Workbench | 60 seconds |
| R-UNI-33 | Universal rules | Timer sentry | ANY_ACTIVE | SYSTEM_UNAVAILABLE | a system of record is unavailable | Queue the outbound action and retry on the schedule | RETRY_QUEUE | Event listener | Platform team | per interface |
| R-UNI-34 | Universal rules | Timer sentry | ANY_ACTIVE | OUTBOUND_FAILED | an outbound call fails after the retry limit | Move to the exception queue and raise a task for the owner | EXCEPTION_QUEUE | Event listener | Platform team | per interface |
| R-UNI-35 | Universal rules | System sentry | RETRY_QUEUE | RETRY_SUCCEEDED | the retry completes | Resume the case in the state it paused in | RESUME_STATE | Milestone | Workbench | None |
| R-UNI-36 | Universal rules | System sentry | RETRY_QUEUE | RETRY_LIMIT_REACHED | retries exhausted | Move to the exception queue | EXCEPTION_QUEUE | Event listener | Platform team | None |
| R-UNI-37 | Universal rules | Timer sentry | ANY_ACTIVE | UPSTREAM_DATA_CORRECTED | a segment dimension changes after a correction upstream | Recompute the segment and re-run the gates | ROUTE_D6_REOPEN | Milestone | Workbench | 1 working day |
| R-UNI-38 | Universal rules | Timer sentry | ANY_ACTIVE | RULE_VERSION_EFFECTIVE | a new rule version reaches its effective date | Apply it to decisions taken from that date. Open cases keep the version they were decided under | RESUME_STATE | Milestone | Center of excellence | on the effective date |
| R-UNI-39 | Universal rules | Timer sentry | ANY_ACTIVE | DECISION_LOG_WRITE_FAILED | the decision log entry cannot be written | Block the action and raise an incident. No action proceeds unlogged | EXCEPTION_QUEUE | Event listener | Platform team | immediate |
| R-UNI-40 | Universal rules | System sentry | ANY_ACTIVE | DUPLICATE_EVENT | the same event arrives twice with the same key | Ignore the second event, record the idempotency hit | RESUME_STATE | Milestone | Workbench | None |
| R-UNI-41 | Universal rules | Timer sentry | EXCEPTION_QUEUE | MANUAL_DECISION_RECORDED | a person decides and names the missing data | Return the case to the route decision and log the rule gap | ROUTE_D6_REOPEN | Milestone | Case owner | 2 working days |
| R-UNI-42 | Universal rules | User sentry | ESCALATED | ESCALATION_CLOSED | the escalation point acts | Resume the case in the state it was in, record the intervention | RESUME_STATE | Milestone | Team manager | None |
| R-UNI-43 | Universal rules | User sentry | HELD_DEVIATION | DEVIATION_CLEARED | the deviation owner records the outcome | Resume the stage clock and return the case | RESUME_STATE | Milestone | Deviation owner | None |
| R-UNI-44 | Universal rules | User sentry | HELD_CONDUCT | CONTACT_STOP_LIFTED | the conduct officer lifts the stop | Resume contact on the permitted channels | RESUME_STATE | Milestone | Conduct and QA officer | None |
| R-UNI-45 | Universal rules | Timer sentry | PARTNER_RECALLED | PARTNER_RESELECTED | the next partner is selected on the scorecard | Re-issue the instruction and restart the partner clock | ROUTE_D6_REOPEN | Milestone | Partner and agency manager | 2 working days |
| R-UNI-46 | Universal rules | Timer sentry | REALLOCATED | OWNER_ACCEPTED | the new owner accepts the case | Resume the case in the same state with the same clocks | RESUME_STATE | Milestone | Case owner | 2 working days |
| R-UNI-47 | Universal rules | Timer sentry | ANY_ACTIVE | ACCOUNT_IN_SOLD_LOT | the account is awarded in a debt sale lot while on another route | Stop every open action, close the case as sold, transfer the data | CASE_CLOSED_SOLD | Milestone | Debt sale officer | same day |
| R-UNI-48 | Universal rules | Timer sentry | ANY_ACTIVE | ASSET_PROCEEDS_CLEAR_DEBT | asset proceeds clear the balance in full | Close the case, release any remaining security, refund any surplus per policy | CASE_CLOSED_SOLD | Milestone | Case owner | 5 working days |
| R-UNI-49 | Universal rules | Timer sentry | ANY_ACTIVE | GUARANTEE_CLEARS_DEBT | a guarantee payment clears the balance in full | Close the case and record the subrogation position | CASE_CLOSED_SOLD | Milestone | Guarantee officer | 5 working days |
| R-UNI-50 | Universal rules | Timer sentry | ANY_ACTIVE | CASE_REOPEN_REQUESTED | a closed case is reopened by an authorized user | Reopen only under the written rule, with a reason and an approver | ROUTE_D6_REOPEN | Milestone | Head of the owning team | 2 working days |

## Sheet: Case file

| Case file items |  |  |
|---|---|---|
| The data the case holds. |  |  |
| Item | Holds | Comes from |
| Case record | Identifier, product, customer, state, owner, queue, entry date, prescription date | P3 case and workflow |
| Account and arrears | Balance, arrears, days past due, classification | ALS core and GL, through COLLINS |
| Collections history | Contact history, promises, the hand-over at 90 days past due | EFS, through COLLINS |
| Customer and party | The customer, the parties, the other products they hold | Customer profile received through COLLINS |
| Collateral | Collateral records | CCMS |
| Valuation | Appraisal values | SVAF |
| Case and ownership | State, owner, queue, stage clock | The Workbench |
| Partner and placement | Agency, law firm and partner placements | The Workbench |
| Tracker content | The Excel and SharePoint trackers, until they are retired | Excel and SharePoint trackers, until retired |
| Decision history | Why the system acted: inputs, rule, version, output | P7 decision center and log |
| Interaction ledger | What happened with the customer: channel, time, who, offer, promise, payment | P3 case and workflow, P6 communications |
| Documents | Every document attached to or generated on the case | P5 document hub |

## Sheet: Workflow model (v5)

| Workflow model v5: CaseWorkflow parent with a child workflow per stage |  |  |  |  |  |  |  |  |  |  |
|---|---|---|---|---|---|---|---|---|---|---|
| CaseWorkflow (P3 rwb-case, task queue rwb-case, namespace rwb-recovery, workflow ID = case ID) is the parent from entry to closure. Each stage runs as a child workflow in the service that owns it. The parent forwards events from the case router; children use parent close policy ABANDON; Continue-As-New runs at every stage end and at least every 28 days. Every child repeats the four steps: receive, EvaluateRules (Drools package and version from rwb-decision), RecordAndApply (record, state and outbox in one transaction) and wait. |  |  |  |  |  |  |  |  |  |  |
| Version 6, 22 November 2026. D-RCV-60. Previous: Version 5, 16 November 2026. |  |  |  |  |  |  |  |  |  |  |
| Role | Workflow | Stage in the v5 model | Owner (code) | Service | Service epic | Task queue | Schema | Tables owned (Ownership Map) | Pattern | Note |
| Parent | CaseWorkflow | Case, entry to closure; case router | P3 | rwb-case | RWB-SVC-P3 | rwb-case | rwb_case | recovery_case, case_party, case_account, case_entry_exclusion, assignment, queue, queue_member, queue_measure, task, timer, parameter_catalog, parameter_value, lov_value, reference_row, reference_version | DP-12 | One per case; workflow ID = case ID; forwards events from the case router to the running child; Continue-As-New at every stage end and at least every 28 days. |
| Child (entry) | RouteDecisionWorkflow | Route decision D6, before the first stage | S1 | rwb-valuation | RWB-SVC-S1 | rwb-valuation | rwb_valuation | None in the Ownership Map; the route outcome is recorded as decision_log_entry (P7) (GAP-0157; ASM-0241) | DP-12, DP-04 | Started with ApprovalWorkflow from the kit on rwb-decision (P7) for the route approval. |
| Kit child | ApprovalWorkflow | Approvals raised by any stage (route approval S1; DoA approvals S2, S3, S5, S6, S7; rule sign-off) | P7 | rwb-decision | RWB-SVC-P7 | rwb-decision | rwb_decision | approval, decision_log_entry | DP-12, DP-04 | Kit template; not a route stage. Routed by authority (DoA) from P4. |
| Child | TreatmentWorkflow | Restructure, TDR; Settlement; Deed in lieu and voluntary surrender | S2 | rwb-treatment | RWB-SVC-S2 | rwb-treatment | rwb_treatment | treatment | DP-12, DP-04 | Settlement and deed in lieu are sagas. |
| Child | GuaranteeClaimWorkflow | Guarantee claim, D6.5 and D6.6 | S3 | rwb-guarantee | RWB-SVC-S3 | rwb-guarantee | rwb_guarantee | guarantee_claim | DP-12, DP-04 | None. |
| Child | LitigationWorkflow | Litigation and enforcement, D7 | S4 | rwb-litigation | RWB-SVC-S4 | rwb-litigation | rwb_litigation | legal_action, hearing | DP-12, DP-04 | Can run for years; Continue-As-New. |
| Child | AssetDisposalWorkflow | Asset disposal, D8.1 to D8.3 | S5 | rwb-asset | RWB-SVC-S5 | rwb-asset | rwb_asset | asset_sale, listing | DP-12, DP-04 | Temporal Schedule: re-appraisal monthly (Architecture v5 slide 19). |
| Child | DebtSaleWorkflow | Debt sale, D8.4 | S6 | rwb-debtsale | RWB-SVC-S6 | rwb-debtsale | rwb_debtsale | debt_sale_lot, debt_sale_account | DP-12, DP-04 | Saga, pivot = transfer. |
| Child | WriteOffWorkflow | Write off and recover after charge-off, D9 | S7 | rwb-writeoff | RWB-SVC-S7 | rwb-writeoff | rwb_writeoff | write_off | DP-12, DP-04 | Temporal Schedule: scan, 3rd working day (Architecture v5 slide 20). |
| Child (any time) | DeviationWorkflow | Deviations X1 to X7 | S8 | rwb-deviation | RWB-SVC-S8 | rwb-deviation | rwb_deviation | deviation | DP-12, DP-04 | Can start at any time; pauses the stage clock. |
| Parent (always on) | Universal rules, any state | Universal rules, any state | P3 | rwb-case | RWB-SVC-P3 | rwb-case | rwb_case | See the parent row (P3 case tables) | DP-04 | R-UNI rules apply in every service; there is no universal-rules child workflow; the parent CaseWorkflow (P3) holds the case state. |

## Sheet: Stage ownership (v5)

| Stage ownership v5: one child workflow per stage, owner from the Ownership Map |  |  |  |  |  |  |  |  |
|---|---|---|---|---|---|---|---|---|
| Each row below is one of the 10 stages in the v5 Stages sheet, unchanged. The realignment adds the child workflow, the owner service, the service epic and the task queue, all taken from the Microservice Ownership Map v1 (D-RCV-60). |  |  |  |  |  |  |  |  |
| Version 6, 22 November 2026. D-RCV-60. Previous: Version 5, 16 November 2026. |  |  |  |  |  |  |  |  |
| Stage (v5 source) | Kind (v5) | Workflow (v5) | Owner (code) | Service | Service epic | Task queue | Tables owned (Ownership Map) | Note |
| Restructure, TDR | Solution stage | Child: TreatmentWorkflow | S2 | rwb-treatment | RWB-SVC-S2 | rwb-treatment | treatment | DP-12: child of CaseWorkflow; settlement and deed-in-lieu sagas share the workflow. |
| Settlement | Solution stage | Child: TreatmentWorkflow | S2 | rwb-treatment | RWB-SVC-S2 | rwb-treatment | treatment | DP-12: child of CaseWorkflow. |
| Deed in lieu and voluntary surrender | Solution stage | Child: TreatmentWorkflow | S2 | rwb-treatment | RWB-SVC-S2 | rwb-treatment | treatment | DP-12: child of CaseWorkflow; the asset hand-off goes to AssetDisposalWorkflow (S5). |
| Litigation and enforcement, D7 | Enforcement stage | Child: LitigationWorkflow | S4 | rwb-litigation | RWB-SVC-S4 | rwb-litigation | legal_action, hearing | DP-12: child of CaseWorkflow; can run for years. |
| Guarantee claim, D6.5 and D6.6 | Recovery stage | Child: GuaranteeClaimWorkflow | S3 | rwb-guarantee | RWB-SVC-S3 | rwb-guarantee | guarantee_claim | DP-12: child of CaseWorkflow. |
| Asset disposal, D8.1 to D8.3 | Recovery stage | Child: AssetDisposalWorkflow | S5 | rwb-asset | RWB-SVC-S5 | rwb-asset | asset_sale, listing | DP-12: child of CaseWorkflow. |
| Debt sale, D8.4 | Recovery stage | Child: DebtSaleWorkflow | S6 | rwb-debtsale | RWB-SVC-S6 | rwb-debtsale | debt_sale_lot, debt_sale_account | DP-12: child of CaseWorkflow; saga, pivot = transfer. |
| Write off and recover after charge-off, D9 | Closure stage | Child: WriteOffWorkflow | S7 | rwb-writeoff | RWB-SVC-S7 | rwb-writeoff | write_off | DP-12: child of CaseWorkflow. |
| Deviations X1 to X7 | Exception stage | Child: DeviationWorkflow | S8 | rwb-deviation | RWB-SVC-S8 | rwb-deviation | deviation | DP-12: child of CaseWorkflow; can start at any time and pauses the stage clock. |
| Universal rules, any state | Always on | No separate child; the parent CaseWorkflow | P3 | rwb-case | RWB-SVC-P3 | rwb-case | See the parent row (P3 case tables) | DP-04: R-UNI rules apply in every service; the parent CaseWorkflow (P3) holds the case state. |

## Sheet: Case file ownership (v5)

| Case file ownership v5: the owner service for each case file item |  |  |  |  |  |  |  |
|---|---|---|---|---|---|---|---|
| Each row below is one of the 12 case file items in the v5 Case file sheet, unchanged. The realignment adds the owner service, the service epic and the table or contract, taken from the Microservice Ownership Map v1 (D-RCV-60). |  |  |  |  |  |  |  |
| Version 6, 22 November 2026. D-RCV-60. Previous: Version 5, 16 November 2026. |  |  |  |  |  |  |  |
| Case file item (v5) | Holds (v5) | Comes from (v5) | Owner (code) | Service | Service epic | Tables or contract (Ownership Map) | Note (v5) |
| Case record | Identifier, product, customer, state, owner, queue, entry date, prescription date | P3 case and workflow | P3 | rwb-case | RWB-SVC-P3 | recovery_case, case_party, case_account, case_entry_exclusion | The case service owns the case record and the case API. |
| Account and arrears | Balance, arrears, days past due, classification | ALS core and GL, through COLLINS | P1 | rwb-source-data | RWB-SVC-P1 | account_ext; ACE view contract | ACE data is read only through rwb-source-data (DP-05). |
| Collections history | Contact history, promises, the hand-over at 90 days past due | EFS, through COLLINS | P1 | rwb-source-data | RWB-SVC-P1 | interaction, efs_ledger_outcome | The interaction ledger is P1 by the R-PREC default ruling (DP-18). |
| Customer and party | The customer, the parties, the other products they hold | Customer profile received through COLLINS | P1 | rwb-source-data | RWB-SVC-P1 | party_ext, contact_point_ext | The case link stays P3 case_party. |
| Collateral | Collateral records | CCMS | Outside the 19 services (CCMS); target owner not specified in the source documents (GAP-0158; ASM-0242) | Outside the 19 services | None | None in the Ownership Map | CCMS is an outside system; data arrives through the P1 source-data contract (DP-05). |
| Valuation | Appraisal values | SVAF | S1 | rwb-valuation | RWB-SVC-S1 | None in the Ownership Map; valuation_ext stays P1 (GAP-0157; ASM-0241) | rwb-valuation owns valuations and the D6 route decision (Architecture v5 slide 41); the API row POST /assets/{assetId}/valuations is S1. |
| Case and ownership | State, owner, queue, stage clock | The Workbench | P3 | rwb-case | RWB-SVC-P3 | recovery_case, assignment, queue, queue_member, task, timer | The case service owns state, queues, tasks and timers. |
| Partner and placement | Agency, law firm and partner placements | The Workbench | S9 | rwb-partner | RWB-SVC-S9 | partner, partner_instruction, partner_user | The partner service owns the panel, partner users and instructions. |
| Tracker content | The Excel and SharePoint trackers, until they are retired | Excel and SharePoint trackers, until retired | Retired | None | None | None | The trackers are retired; no target service. |
| Decision history | Why the system acted: inputs, rule, version, output | P7 decision center and log | P7 | rwb-decision | RWB-SVC-P7 | decision_log_entry, approval | The decision service owns the central ledger and approvals. |
| Interaction ledger | What happened with the customer: channel, time, who, offer, promise, payment | P3 case and workflow, P6 communications | P1 | rwb-source-data | RWB-SVC-P1 | interaction, efs_ledger_outcome | The ledger is P1 (DP-18); P3 serves the case timeline API and P6 records the notice. |
| Documents | Every document attached to or generated on the case | P5 document hub | P5 | rwb-document | RWB-SVC-P5 | document, document_type, document_custody, document_text, document_field, document_intake, case_document_check, signature_request, retention_rule | The document service owns metadata, custody, OCR, signatures and retention. |

## Sheet: Change log

| Change log |  |  |  |  |
|---|---|---|---|---|
| Version | Date | Change | Decision | Tool |
| v6 | 22 November 2026 | D-RCV-60 microservice realignment | D-RCV-60 | T3 Code / OpenCode / DeepSeek v4.1 Flash |
| v6, 22 November 2026, D-RCV-60 microservice realignment, T3 Code / OpenCode / DeepSeek v4.1 Flash |  |  |  |  |

## Sheet: Realignment changes

| Recovery Workbench Case and Workflow Model v6 - realignment changes |  |  |
|---|---|---|
| v6, 22 November 2026, D-RCV-60 microservice realignment, T3 Code / OpenCode / DeepSeek v4.1 Flash |  |  |
| Area | Change | Source |
| Workflow model | Added the CaseWorkflow parent on P3 rwb-case and one child workflow per stage: RouteDecisionWorkflow (S1), TreatmentWorkflow (S2), GuaranteeClaimWorkflow (S3), LitigationWorkflow (S4), AssetDisposalWorkflow (S5), DebtSaleWorkflow (S6), WriteOffWorkflow (S7), DeviationWorkflow (S8), with ApprovalWorkflow (P7) from the kit. | Architecture v5 slides 25 and 41; Temporal and Drools Design slide 13; Ownership Map v1 Workflows and activities |
| Stage ownership | Added the owner service, service epic, task queue and owned tables for each of the 10 CMMN stages, taken from the Ownership Map v1. | Ownership Map v1 Tables and Services; R4 naming |
| Case file ownership | Added the owner service, service epic and table or contract for each of the 12 case file items, taken from the Ownership Map v1. | Ownership Map v1 Tables; DP-05, DP-18 |
| Unchanged | Every sheet, ID, number and date of v5 is kept unchanged: Stages, Elements, Case status, Status transitions, Milestones, Tasks, Event listeners, Sentries and Case file. | v5 source |
| Universal rules | No separate child workflow; R-UNI rules apply in every service and the parent CaseWorkflow holds the case state. | Temporal and Drools Design slide 13 note |
| Retired content | The Excel and SharePoint trackers in the Case file sheet have no target service; they are retired. | v5 source Case file; D-RCV-60 |
| Open point | No S1 table is listed in the Ownership Map for valuations; recorded as GAP-0157 / ASM-0241. | Ownership Map v1 Tables |
| Open point | CCMS collateral has no target service in the Ownership Map; recorded as GAP-0158 / ASM-0242. | v5 source Case file; Ownership Map v1 |

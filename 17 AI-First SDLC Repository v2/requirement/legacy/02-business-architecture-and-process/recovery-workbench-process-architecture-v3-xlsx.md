<!-- source: 02 Business architecture and process/Recovery Workbench Process Architecture v3.xlsx -->
<!-- converted: 2026-11-16 from XLSX -->

> **Source:** `02 Business architecture and process/Recovery Workbench Process Architecture v3.xlsx`  
> **Converted from:** XLSX

## L1 processes

| Recovery Workbench process architecture: L1 processes |  |  |  |  |  |  |  |  |  |  |  |  |  |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 19 L1 processes in four layers. Counts are calculated from the L2 and L3 tabs. Modes are defined on the Key tab. |  |  |  |  |  |  |  |  |  |  |  |  |  |
| L1 | Layer | L1 process | Definition | Decision | Runs on | L2 | L3 | A | A+H | H | M | P | A or A+H |
| 01 | Core | Detect and act on signals | Watch every performing and early-arrears account and decide whether, when and how to act before or at the first missed payment. | D1 | EFS |  |  |  |  |  |  |  |  |
| 02 | Core | Contact the customer | Reach the customer through the right channel at the right time, within contact limits and customer standards, and record the outcome. | D2 | EFS |  |  |  |  |  |  |  |  |
| 03 | Core | Manage promises | Record each promise to pay, track it to the payment and move the case on when the promise is broken. | D3 | EFS |  |  |  |  |  |  |  |  |
| 04 | Core | Escalate | Raise the intensity of collection by senior phone contact, field visits or outside agencies when lighter treatment has failed. | D4 | EFS |  |  |  |  |  |  |  |  |
| 05 | Core | Restructure | Assess affordability, offer and book a restructure plan, and monitor it until the customer pays as agreed or the plan fails. | D5 | EFS and ACE, then the Workbench after TDR go-live |  |  |  |  |  |  |  |  |
| 06 | Core | Take over and own the case | Take the case from collections at 90 days past due, with its history, and give it one owner and a running set of deadlines. | D6 entry | Recovery Workbench |  |  |  |  |  |  |  |  |
| 07 | Core | Route, settle and claim | Value the case, decide the route, and resolve it with the customer by settlement, deed in lieu, guarantee claim or guarantor pursuit. | D6 | Recovery Workbench |  |  |  |  |  |  |  |  |
| 08 | Core | Litigate and enforce | Take the case through notices, filing, judgment and enforcement until the debt is paid, settled or proven unrecoverable. | D7 | Recovery Workbench |  |  |  |  |  |  |  |  |
| 09 | Core | Dispose assets and sell debt | Take assets onto the books, hold them, and turn them into cash by auction or other routes, or sell the debt. | D8 | Recovery Workbench |  |  |  |  |  |  |  |  |
| 10 | Core | Write off and recover after charge-off | Write off the balance that cannot be recovered, post it, and keep recovering after charge-off until the case closes. | D9 | Recovery Workbench |  |  |  |  |  |  |  |  |
| 11 | Support | Handle customer care and deviations | Answer customer contacts and handle the seven deviations that interrupt a decision, then return the case to the right decision. | X1 to X7 | EFS and Recovery Workbench |  |  |  |  |  |  |  |  |
| 12 | Support | Manage partners | Select, instruct, measure, pay and govern the partners who work cases for the bank, and end the contract when needed. | All | Recovery Workbench and partner portals |  |  |  |  |  |  |  |  |
| 13 | Support | Manage documents and correspondence | Read and file inbound documents, send letters and notices with proof of delivery, and keep documents and originals under control. | All | Recovery Workbench document hub |  |  |  |  |  |  |  |  |
| 14 | Manage | Set strategy, policy and decision rules | Set the segments, treatment policy, decision rules, limits, fees and the reference data every decision reads. | All | Recovery Workbench reference data |  |  |  |  |  |  |  |  |
| 15 | Manage | Manage performance, data and AI | Report results, test strategies, monitor agents and models, keep data correct and feed what is learned back to policy. | All | Recovery Workbench, data lake, Power BI |  |  |  |  |  |  |  |  |
| 16 | Manage | Manage risk, control and compliance | Run quality assurance, conduct control, model and agent risk, audit response, access control, incidents and data subject rights. | All | Recovery Workbench |  |  |  |  |  |  |  |  |
| 17 | Across all | Run the decision center | Route every recommendation to the person with the authority to decide it, record one log entry per decision, and feed results back. | D1 to D9 | Recovery Workbench decision service |  |  |  |  |  |  |  |  |
| 18 | Manage | Plan capacity and allocate work | Forecast inflow, plan staff and partner capacity, and build and allocate the work lists that collectors and partners work from. | D2, D4 | Capacity model, dialer, field application, partner portal |  |  |  |  |  |  |  |  |
| 19 | Support | Manage payments and reconciliation | Receive payments from every channel, apply them to the right account and case, and reconcile cash to the case and the core. | D3, D5, D6 | Core banking, EFS, Recovery Workbench |  |  |  |  |  |  |  |  |
|  | Total |  |  |  |  |  |  |  |  |  |  |  |  |

## L2 sub-processes

| L2 sub-processes |  |  |  |  |  |  |  |  |  |  |
|---|---|---|---|---|---|---|---|---|---|---|
| 84 L2 sub-processes, each with its definition and the count of L3 processes by mode. |  |  |  |  |  |  |  |  |  |  |
| L1 | L1 process | L2 | L2 sub-process | Definition | L3 | A | A+H | H | M | P |
| 01 | Detect and act on signals | 1.1 | Monitor accounts | Load account data daily and score each account for the risk of default. |  |  |  |  |  |  |
| 01 | Detect and act on signals | 1.2 | Decide whether to act | Decide for each account whether to act now or keep monitoring, and start the treatment. |  |  |  |  |  |  |
| 02 | Contact the customer | 2.1 | Choose the channel | Select the channel and the contact time for each account within the contact limits. |  |  |  |  |  |  |
| 02 | Contact the customer | 2.2 | Contact by digital channels | Contact customers by SMS, LINE, voice bot and self-serve payment. |  |  |  |  |  |  |
| 02 | Contact the customer | 2.3 | Contact by phone | Call customers through the dialer, agree the next step and record the outcome. |  |  |  |  |  |  |
| 02 | Contact the customer | 2.4 | Hold within the grace period | Hold contact while an account is inside its grace period. |  |  |  |  |  |  |
| 02 | Contact the customer | 2.5 | Manage contact data and consent | Keep contact data and consent current, including numbers found in the field and by tracing. |  |  |  |  |  |  |
| 02 | Contact the customer | 2.6 | Handle inbound contact | Take inbound calls from customers and record what was agreed. |  |  |  |  |  |  |
| 03 | Manage promises | 3.1 | Record the promise | Record a promise to pay from any channel and hold the case to the promised date. |  |  |  |  |  |  |
| 03 | Manage promises | 3.2 | Track the promise | Remind the customer before the promised date and match the payment to the promise. |  |  |  |  |  |  |
| 03 | Manage promises | 3.3 | Handle broken promises | Move the case to the next decision when a promise breaks. |  |  |  |  |  |  |
| 04 | Escalate | 4.1 | Recommend the escalation | Recommend the escalation route for each account and approve exceptions. |  |  |  |  |  |  |
| 04 | Escalate | 4.2 | Run higher-intensity phone contact | Call the customer with a senior collector. |  |  |  |  |  |  |
| 04 | Escalate | 4.3 | Run field visits | Assign, carry out and record field visits. |  |  |  |  |  |  |
| 04 | Escalate | 4.4 | Allocate to outside agencies | Allocate accounts to outside agencies, track their results and recall accounts. |  |  |  |  |  |  |
| 05 | Restructure | 5.1 | Assess affordability | Collect income and expense information and calculate what the customer can afford. |  |  |  |  |  |  |
| 05 | Restructure | 5.2 | Offer a plan | Recommend a plan and offer it by self-serve, phone or field visit. |  |  |  |  |  |  |
| 05 | Restructure | 5.3 | Approve and book | Approve the plan, sign the agreement and book it in the core. |  |  |  |  |  |  |
| 05 | Restructure | 5.4 | Monitor plans | Track plan payments, reassess broken plans and move failed plans to recovery. |  |  |  |  |  |  |
| 05 | Restructure | 5.5 | Run relief and government schemes | Run the BOT relief and government schemes as standing programs. |  |  |  |  |  |  |
| 06 | Take over and own the case | 6.1 | Take over the case at 90 days past due | Transfer the case and its history from collections at 90 days past due, start the deadlines and screen for deviations. |  |  |  |  |  |  |
| 07 | Route, settle and claim | 7.1 | Value the case | Appraise the collateral, estimate the return by route and calculate payoff and settlement amounts. |  |  |  |  |  |  |
| 07 | Route, settle and claim | 7.2 | Decide the route | Recommend and approve the route, or hold the case with a review date. |  |  |  |  |  |  |
| 07 | Route, settle and claim | 7.3 | Negotiate settlement or deed in lieu | Negotiate and approve a settlement or a deed in lieu, reconcile the payments and release the collateral. |  |  |  |  |  |  |
| 07 | Route, settle and claim | 7.4 | Claim guarantees | Prepare, submit and track Thai Credit Guarantee claims. |  |  |  |  |  |  |
| 07 | Route, settle and claim | 7.5 | Pursue guarantors and co-borrowers | Notify guarantors and co-borrowers of the default and negotiate with them. |  |  |  |  |  |  |
| 08 | Litigate and enforce | 8.1 | Prepare pre-litigation | Issue demand and recall notices and assemble and verify the litigation pack. |  |  |  |  |  |  |
| 08 | Litigate and enforce | 8.2 | Instruct and file | Select the law firm, instruct it and file the case in court. |  |  |  |  |  |  |
| 08 | Litigate and enforce | 8.3 | Manage to judgment | Track the case to judgment, decide settlements and appeals, and pay court costs. |  |  |  |  |  |  |
| 08 | Litigate and enforce | 8.4 | Enforce judgment | Trace assets, enforce the judgment, follow the LED auction and match the proceeds. |  |  |  |  |  |  |
| 09 | Dispose assets and sell debt | 9.1 | Take assets onto the books | Repossess vehicles, serve the statutory notice and record property taken onto the books. |  |  |  |  |  |  |
| 09 | Dispose assets and sell debt | 9.2 | Hold and manage assets | Hold assets, track holding age, maintain, insure and evict, and reappraise on cycle. |  |  |  |  |  |  |
| 09 | Dispose assets and sell debt | 9.3 | Decide the disposal route | Recommend the disposal route for each asset. |  |  |  |  |  |  |
| 09 | Dispose assets and sell debt | 9.4 | Sell assets by Dutch auction | Set start and floor prices, list, run auction rounds and transfer title. |  |  |  |  |  |  |
| 09 | Dispose assets and sell debt | 9.5 | Other disposal routes | Dispose through RAMC transfer, customer buy-back, broker sale or rental. |  |  |  |  |  |  |
| 09 | Dispose assets and sell debt | 9.6 | Sell debt | Build debt sale lots, set buyer terms, run the bid and award, transfer data and handle put-backs. |  |  |  |  |  |  |
| 09 | Dispose assets and sell debt | 9.7 | Manage the shortfall after sale | Calculate the shortfall after sale and offer affordable terms on it. |  |  |  |  |  |  |
| 10 | Write off and recover after charge-off | 10.1 | Assess write-off | Identify eligible accounts, prepare the write-off pack and check the tax criteria. |  |  |  |  |  |  |
| 10 | Write off and recover after charge-off | 10.2 | Approve and post | Approve the write-off in committee, post it and send provision inputs to Finance. |  |  |  |  |  |  |
| 10 | Write off and recover after charge-off | 10.3 | Recover after charge-off | Place written-off accounts for soft recovery or sale, and close the case. |  |  |  |  |  |  |
| 11 | Handle customer care and deviations | 11.1 | Answer customer contacts | Classify inbound contacts, answer balance and payoff requests, and route the rest. |  |  |  |  |  |  |
| 11 | Handle customer care and deviations | 11.2 | X1 Dispute or complaint | X1. Stop contact on a disputed item, resolve the complaint and resume the case. |  |  |  |  |  |  |
| 11 | Handle customer care and deviations | 11.3 | X2 Vulnerable customer or hardship | X2. Move a vulnerable or hardship case to a specialist and decide on a hardship plan. |  |  |  |  |  |  |
| 11 | Handle customer care and deviations | 11.4 | X3 Deceased customer | X3. Stop contact on a death, claim insurance and decide on claims against the estate. |  |  |  |  |  |  |
| 11 | Handle customer care and deviations | 11.5 | X4 Fraud | X4. Refer suspected fraud, investigate it and move the case on the result. |  |  |  |  |  |  |
| 11 | Handle customer care and deviations | 11.6 | X5 Bankruptcy or external seizure | X5. Stop direct collection on bankruptcy or seizure and file the claim before the deadline. |  |  |  |  |  |  |
| 11 | Handle customer care and deviations | 11.7 | X6 Lost contact | X6. Trace a customer whose every contact fails and return the case when found. |  |  |  |  |  |  |
| 11 | Handle customer care and deviations | 11.8 | X7 Collateral event | X7. Claim insurance on a collateral event, reappraise and return the case to the route decision. |  |  |  |  |  |  |
| 12 | Manage partners | 12.1 | Select and contract partners | Keep the partner panels, onboard partners and set fee terms and incentives. |  |  |  |  |  |  |
| 12 | Manage partners | 12.2 | Exchange work with partners | Send allocations and instructions to partners and attach their results to the case. |  |  |  |  |  |  |
| 12 | Manage partners | 12.3 | Track performance and pay fees | Score partner results against targets and calculate and approve fees. |  |  |  |  |  |  |
| 12 | Manage partners | 12.4 | Govern partners | Review partners, share strategy and standards, and check partner conduct. |  |  |  |  |  |  |
| 12 | Manage partners | 12.5 | Issue notices and exit | Issue notices when a partner misses target and end contracts. |  |  |  |  |  |  |
| 13 | Manage documents and correspondence | 13.1 | Read inbound documents | Scan, classify and extract inbound documents and attach them to the case. |  |  |  |  |  |  |
| 13 | Manage documents and correspondence | 13.2 | Send letters and notices | Generate letters from templates, check them and send them with proof of delivery. |  |  |  |  |  |  |
| 13 | Manage documents and correspondence | 13.3 | Store and retain documents | Apply retention, answer document requests and keep contact and party records. |  |  |  |  |  |  |
| 13 | Manage documents and correspondence | 13.4 | Control document custody | Track every original document as it moves between storage, post, lawyer, court and land office. |  |  |  |  |  |  |
| 14 | Set strategy, policy and decision rules | 14.1 | Set strategy and treatment policy | Set segments, treatment policy and customer experience standards. |  |  |  |  |  |  |
| 14 | Set strategy, policy and decision rules | 14.2 | Set decision rules and limits | Keep the delegation of authority, the rules, timers, calendars, users and partner set-up. |  |  |  |  |  |  |
| 14 | Set strategy, policy and decision rules | 14.3 | Set fees, charges and waivers | Set collection fees and charges within the law, apply them and approve waivers. |  |  |  |  |  |  |
| 15 | Manage performance, data and AI | 15.1 | Report performance | Produce scorecards from the decision log and agree actions. |  |  |  |  |  |  |
| 15 | Manage performance, data and AI | 15.2 | Test strategies | Run champion and challenger tests and approve a new champion. |  |  |  |  |  |  |
| 15 | Manage performance, data and AI | 15.3 | Monitor agents and models | Track agent and model overrides, drift and errors, and retrain and release. |  |  |  |  |  |  |
| 15 | Manage performance, data and AI | 15.4 | Manage data quality | Reconcile to the core daily, fix data exceptions and delete data when required. |  |  |  |  |  |  |
| 15 | Manage performance, data and AI | 15.5 | Improve processes | Log QA findings and improvement ideas and update SOPs and rules. |  |  |  |  |  |  |
| 15 | Manage performance, data and AI | 15.6 | Track benefits and value | Keep the benefits ledger, attribute results to each lever and review value monthly. |  |  |  |  |  |  |
| 15 | Manage performance, data and AI | 15.7 | Feed results back to credit policy and origination | Report what recovery learns about origination and agree policy changes with credit risk. |  |  |  |  |  |  |
| 15 | Manage performance, data and AI | 15.8 | Classify, stage and re-age accounts | Apply one definition of flow rate, cure and re-ageing, and classify and stage accounts. |  |  |  |  |  |  |
| 16 | Manage risk, control and compliance | 16.1 | Run quality assurance | Select cases for quality assurance and review them against the SOP. |  |  |  |  |  |  |
| 16 | Manage risk, control and compliance | 16.2 | Control conduct | Check outbound contacts against customer standards and review breaches. |  |  |  |  |  |  |
| 16 | Manage risk, control and compliance | 16.3 | Manage model and agent risk | Review agents and models before release and fall back to rules when they fail. |  |  |  |  |  |  |
| 16 | Manage risk, control and compliance | 16.4 | Answer audit and regulatory requests | Answer audit and regulator requests from the decision log. |  |  |  |  |  |  |
| 16 | Manage risk, control and compliance | 16.5 | Control access and data protection | Apply personal data access by role and by agent. |  |  |  |  |  |  |
| 16 | Manage risk, control and compliance | 16.6 | Manage incidents and continuity | Detect incidents, switch to fallback working and close the incident. |  |  |  |  |  |  |
| 16 | Manage risk, control and compliance | 16.7 | Handle data subject requests | Answer access, correction, erasure and objection requests within the legal time. |  |  |  |  |  |  |
| 17 | Run the decision center | 17.1 | Route recommendations for approval | Route each recommendation to the approver by limit and escalate overdue approvals. |  |  |  |  |  |  |
| 17 | Run the decision center | 17.2 | Keep the decision log | Record one log entry per decision with its actions and outcome. |  |  |  |  |  |  |
| 17 | Run the decision center | 17.3 | Feed results back | Send outcomes to the data store and to COLLINS for retraining. |  |  |  |  |  |  |
| 18 | Plan capacity and allocate work | 18.1 | Forecast inflow and workload | Forecast case inflow and convert it into workload by role. |  |  |  |  |  |  |
| 18 | Plan capacity and allocate work | 18.2 | Plan capacity and rosters | Plan staff and partner capacity and set the weekly roster. |  |  |  |  |  |  |
| 18 | Plan capacity and allocate work | 18.3 | Build and allocate work lists | Build phone and field work lists and allocate work by rule. |  |  |  |  |  |  |
| 19 | Manage payments and reconciliation | 19.1 | Receive payments | Receive payments from every channel and identify the account and case. |  |  |  |  |  |  |
| 19 | Manage payments and reconciliation | 19.2 | Apply payments to accounts | Apply payments to accounts and handle partial payments, reversals and refunds. |  |  |  |  |  |  |
| 19 | Manage payments and reconciliation | 19.3 | Reconcile and correct | Reconcile cash to the case and the core daily and correct errors. |  |  |  |  |  |  |

## L3 processes

| L3 processes |  |  |  |  |  |  |  |  |  |
|---|---|---|---|---|---|---|---|---|---|
| 247 L3 processes, numbered within their L2 sub-process. |  |  |  |  |  |  |  |  |  |
| L1 | L1 process | L2 | L2 sub-process | L3 | L3 process | Decision | Mode | Step in the decision pattern | Systems |
| 01 | Detect and act on signals | 1.1 | Monitor accounts | 01.1.1 | Load daily balances, arrears and payments | D1 | A | Information | ALS, EFS |
| 01 | Detect and act on signals | 1.1 | Monitor accounts | 01.1.2 | Score the risk of default | D1 | A | Information | COLLINS |
| 01 | Detect and act on signals | 1.1 | Monitor accounts | 01.1.3 | Detect early warning signals before the due date | D1 | A | Information | COLLINS, EFS |
| 01 | Detect and act on signals | 1.2 | Decide whether to act | 01.2.1 | Recommend act or monitor | D1 | A | Decide | EFS, COLLINS |
| 01 | Detect and act on signals | 1.2 | Decide whether to act | 01.2.2 | Start contact before the due date for early warning cases | D1 | A | Act | EFS |
| 01 | Detect and act on signals | 1.2 | Decide whether to act | 01.2.3 | Start treatment on a missed payment | D1 | A | Act | EFS |
| 02 | Contact the customer | 2.1 | Choose the channel | 02.1.1 | Select channel and contact time by segment | D2 | A | Decide | EFS, COLLINS |
| 02 | Contact the customer | 2.1 | Choose the channel | 02.1.2 | Check contact limits and customer standards | D2 | A | Decide | EFS |
| 02 | Contact the customer | 2.2 | Contact by digital channels | 02.2.1 | Send SMS and LINE reminders | D2 | A | Act | EFS |
| 02 | Contact the customer | 2.2 | Contact by digital channels | 02.2.2 | Run voice bot calls (WIZ) | D2 | A | Act | WIZ, EFS |
| 02 | Contact the customer | 2.2 | Contact by digital channels | 02.2.3 | Offer self-serve payment or plan online | D2 | A | Act | EFS |
| 02 | Contact the customer | 2.3 | Contact by phone | 02.3.1 | Queue accounts to the PDS dialer | D2 | A | Act | PDS dialer, EFS |
| 02 | Contact the customer | 2.3 | Contact by phone | 02.3.2 | Talk to the customer and agree the next step | D2 | H | Act | EFS |
| 02 | Contact the customer | 2.3 | Contact by phone | 02.3.3 | Summarize the call and record the outcome | D2 | A+H | Log | EFS |
| 02 | Contact the customer | 2.3 | Contact by phone | 02.3.4 | Start and stop direct debit deductions | D2 | A+H | Log | EFS |
| 02 | Contact the customer | 2.3 | Contact by phone | 02.3.5 | Contact 3rd parties | D2 | A+H | Log | EFS |
| 02 | Contact the customer | 2.4 | Hold within the grace period | 02.4.1 | Hold contact during the grace period | D2 | A | Decide | EFS |
| 02 | Contact the customer | 2.5 | Manage contact data and consent | 02.5.1 | Record new numbers and addresses found in the field or by agencies | D2 | A+H | Information | EFS, field application |
| 02 | Contact the customer | 2.5 | Manage contact data and consent | 02.5.2 | Trace missing contact data through the bureau and internal sources | D2 | A | Information | EFS, NCB |
| 02 | Contact the customer | 2.5 | Manage contact data and consent | 02.5.3 | Record and apply contact consent by channel | D2 | A | Decide | EFS |
| 02 | Contact the customer | 2.6 | Handle inbound contact | 02.6.1 | Pick up inbound call by the customer | D2 | A+H | Log | EFS |
| 03 | Manage promises | 3.1 | Record the promise | 03.1.1 | Record the promise to pay from a call, self-serve or field visit | D3 | A | Information | EFS |
| 03 | Manage promises | 3.1 | Record the promise | 03.1.2 | Hold the case to the end of grace period | D3 | A | Act | EFS |
| 03 | Manage promises | 3.2 | Track the promise | 03.2.1 | Send a reminder before the end of grace promise period | D3 | A | Act | EFS |
| 03 | Manage promises | 3.2 | Track the promise | 03.2.2 | Match the payment to the promise | D3 | A | Information | ALS, EFS |
| 03 | Manage promises | 3.3 | Handle broken promises | 03.3.1 | Move the case to D4 after an escalation trigger (broken promise or no contact and others) | D3 | A | Act | EFS |
| 03 | Manage promises | 3.3 | Handle broken promises | 03.3.2 | Move the case to D5 after escalation trigger based on Collins | D3 | A | Act | EFS |
| 04 | Escalate | 4.1 | Recommend the escalation | 04.1.1 | Recommend phone, field visit or OA with reasons | D4 | A | Decide | EFS, COLLINS |
| 04 | Escalate | 4.1 | Recommend the escalation | 04.1.2 | Approve exceptions to the escalation policy | D4 | A+H | Outcome | EFS |
| 04 | Escalate | 4.2 | Run higher-intensity phone contact | 04.2.1 | Call the customer with a senior collector | D4 | H | Act | PDS dialer, EFS |
| 04 | Escalate | 4.3 | Run field visits | 04.3.1 | Assign field visits by location | D4 | A | Act | EFS |
| 04 | Escalate | 4.3 | Run field visits | 04.3.2 | Visit the customer (in-house FCR) | D4 | H | Act | EFS |
| 04 | Escalate | 4.3 | Run field visits | 04.3.3 | Record the visit result including upload of documents, photos, location | D4 | A+H | Log | EFS |
| 04 | Escalate | 4.4 | Allocate to outside agencies | 04.4.1 | Allocate accounts to OAs by performance | D4 | A | Act | EFS, Portal |
| 04 | Escalate | 4.4 | Allocate to outside agencies | 04.4.2 | Contact and collect on allocated accounts | D4 | P | Act | Portal |
| 04 | Escalate | 4.4 | Allocate to outside agencies | 04.4.3 | Track OA results against target | D4 | A | Information | EFS, Portal |
| 04 | Escalate | 4.4 | Allocate to outside agencies | 04.4.4 | Recall the account from OA based on Collins parameters | D4 | A | Act | EFS, Portal |
| 05 | Restructure | 5.1 | Assess affordability | 05.1.1 | Collect income and expense information | D5 | A | Information | EFS, ACE |
| 05 | Restructure | 5.1 | Assess affordability | 05.1.2 | Calculate affordability and plan options | D5 | A | Decide | ACE |
| 05 | Restructure | 5.2 | Offer a plan | 05.2.1 | Recommend a plan with reasons | D5 | A | Decide | ACE |
| 05 | Restructure | 5.2 | Offer a plan | 05.2.2 | Offer the plan by digital self-serve | D5 | A | Act | EFS, ACE |
| 05 | Restructure | 5.2 | Offer a plan | 05.2.3 | Offer the plan by phone or field visit | D5 | H | Act | EFS, ACE |
| 05 | Restructure | 5.3 | Approve and book | 05.3.1 | Approve the plan above the limit | D5 | A+H | Outcome | ACE, TDR system |
| 05 | Restructure | 5.3 | Approve and book | 05.3.2 | Sign the agreement with the customer (FCR) | D5 | H | Act | TDR system |
| 05 | Restructure | 5.3 | Approve and book | 05.3.3 | Book the plan in ALS | D5 | A | Act | ALS, TDR system |
| 05 | Restructure | 5.4 | Monitor plans | 05.4.1 | Track plan payments | D5 | A | Information | ALS |
| 05 | Restructure | 5.4 | Monitor plans | 05.4.2 | Reassess a broken plan based on strategy parameter | D5 | A+H | Decide | ACE |
| 05 | Restructure | 5.4 | Monitor plans | 05.4.3 | Move the case to D6 when the customer cannot afford a plan or breaks it again | D5 | A | Act | EFS, ACE |
| 05 | Restructure | 5.4 | Monitor plans | 05.4.4 | Manage legal notices from another bank | D5 | A | Act | EFS, ACE |
| 05 | Restructure | 5.5 | Run relief and government schemes | 05.5.1 | Check eligibility for BOT relief and government schemes | D5 | A | Decide | ACE |
| 05 | Restructure | 5.5 | Run relief and government schemes | 05.5.2 | Offer and book the scheme terms | D5 | A+H | Act | ACE, ALS |
| 05 | Restructure | 5.5 | Run relief and government schemes | 05.5.3 | Report scheme take-up | D5 | A | Log | ACE |
| 06 | Take over and own the case | 6.1 | Take over the case at 90 days past due | 06.1.1 | Transfer case and history from EFS | D6 | A | Information | EFS, RW |
| 06 | Take over and own the case | 6.1 | Take over the case at 90 days past due | 06.1.2 | Track prescription deadlines | D6 and D7 | A | Information | RW |
| 06 | Take over and own the case | 6.1 | Take over the case at 90 days past due | 06.1.3 | Screen the case for deviations X1 to X7 | D6 | A | Information | RW |
| 07 | Route, settle and claim | 7.1 | Value the case | 07.1.1 | Order collateral appraisal | D6 | A | Information | SVAF |
| 07 | Route, settle and claim | 7.1 | Value the case | 07.1.2 | Inspect collateral | D6 | P | Information | SVAF |
| 07 | Route, settle and claim | 7.1 | Value the case | 07.1.3 | Accept appraisal value | D6 | A+H | Information | SVAF |
| 07 | Route, settle and claim | 7.1 | Value the case | 07.1.4 | Estimate return by route | D6 | A | Information | COLLINS |
| 07 | Route, settle and claim | 7.1 | Value the case | 07.1.5 | Calculate payoff and settlement amounts | D6 | A | Decide | RW, ALS |
| 07 | Route, settle and claim | 7.2 | Decide the route | 07.2.1 | Recommend route with reasons | D6 | A | Decide | RW, COLLINS |
| 07 | Route, settle and claim | 7.2 | Decide the route | 07.2.2 | Approve route | D6 | A+H | Outcome | RW |
| 07 | Route, settle and claim | 7.2 | Decide the route | 07.2.3 | Hold the case and set a review date | D6 | A | Act | RW |
| 07 | Route, settle and claim | 7.3 | Negotiate settlement or deed in lieu | 07.3.1 | Negotiate settlement | D6 | H | Act | RW |
| 07 | Route, settle and claim | 7.3 | Negotiate settlement or deed in lieu | 07.3.2 | Approve settlement | D6 | A+H | Outcome | RW |
| 07 | Route, settle and claim | 7.3 | Negotiate settlement or deed in lieu | 07.3.3 | Process deed in lieu | D6 | H | Act | RW, CCMS |
| 07 | Route, settle and claim | 7.3 | Negotiate settlement or deed in lieu | 07.3.4 | Reconcile settlement payments to case | D6 | A | Act | RW, ALS |
| 07 | Route, settle and claim | 7.3 | Negotiate settlement or deed in lieu | 07.3.5 | Release collateral and return title | D6 | A+H | Act | CCMS |
| 07 | Route, settle and claim | 7.4 | Claim guarantees | 07.4.1 | Prepare and submit TCG claim | D6 | A+H | Act | RW |
| 07 | Route, settle and claim | 7.4 | Claim guarantees | 07.4.2 | Track claim to payment | D6 | A | Act | RW |
| 07 | Route, settle and claim | 7.5 | Pursue guarantors and co-borrowers | 07.5.1 | Notify guarantors of default | D6 | A | Act | RW, DMS |
| 07 | Route, settle and claim | 7.5 | Pursue guarantors and co-borrowers | 07.5.2 | Negotiate with guarantors | D6 | H | Act | RW |
| 08 | Litigate and enforce | 8.1 | Prepare pre-litigation | 08.1.1 | Issue demand and recall notices | D7 | A | Act | RW, DMS |
| 08 | Litigate and enforce | 8.1 | Prepare pre-litigation | 08.1.2 | Assemble litigation document pack | D7 | A | Information | RW, CCMS |
| 08 | Litigate and enforce | 8.1 | Prepare pre-litigation | 08.1.3 | Verify document pack | D7 | A+H | Information | RW |
| 08 | Litigate and enforce | 8.2 | Instruct and file | 08.2.1 | Select law firm from panel | D7 | A | Decide | RW |
| 08 | Litigate and enforce | 8.2 | Instruct and file | 08.2.2 | Instruct firm through portal | D7 | A | Act | Portal |
| 08 | Litigate and enforce | 8.2 | Instruct and file | 08.2.3 | File case in court | D7 | P | Act | RW |
| 08 | Litigate and enforce | 8.3 | Manage to judgment | 08.3.1 | Recommend the next litigation step with reasons | D7 | A | Decide | RW |
| 08 | Litigate and enforce | 8.3 | Manage to judgment | 08.3.2 | Track hearings and deadlines | D7 | A | Information | RW |
| 08 | Litigate and enforce | 8.3 | Manage to judgment | 08.3.3 | Approve settlement before judgment | D7 | A+H | Outcome | RW |
| 08 | Litigate and enforce | 8.3 | Manage to judgment | 08.3.4 | Decide and manage appeals | D7 | A+H | Outcome | RW |
| 08 | Litigate and enforce | 8.3 | Manage to judgment | 08.3.5 | Pay court fees and legal expenses | D7 | A+H | Act | RW |
| 08 | Litigate and enforce | 8.4 | Enforce judgment | 08.4.1 | Trace assets | D7 | A | Information | RW |
| 08 | Litigate and enforce | 8.4 | Enforce judgment | 08.4.2 | Apply for writ and seizure | D7 | P | Act | RW |
| 08 | Litigate and enforce | 8.4 | Enforce judgment | 08.4.3 | Follow LED auction | D7 | P | Act | RW |
| 08 | Litigate and enforce | 8.4 | Enforce judgment | 08.4.4 | Match proceeds to case | D7 | A | Act | RW, ALS |
| 08 | Litigate and enforce | 8.4 | Enforce judgment | 08.4.5 | File bankruptcy petition against debtor | D7 | A+H | Outcome | RW |
| 09 | Dispose assets and sell debt | 9.1 | Take assets onto the books | 09.1.1 | Repossess vehicle | D8 | P | Act | RW |
| 09 | Dispose assets and sell debt | 9.1 | Take assets onto the books | 09.1.2 | Serve notice and prove delivery | D8 | A | Act | RW, DMS |
| 09 | Dispose assets and sell debt | 9.1 | Take assets onto the books | 09.1.3 | Record property | D8 | A | Information | RW |
| 09 | Dispose assets and sell debt | 9.2 | Hold and manage assets | 09.2.1 | Track holding age against provision steps | D8 | A | Information | RW |
| 09 | Dispose assets and sell debt | 9.2 | Hold and manage assets | 09.2.2 | Store repossessed vehicles | D8 | P | Act | RW |
| 09 | Dispose assets and sell debt | 9.2 | Hold and manage assets | 09.2.3 | Maintain property: tax, insurance, security | D8 | P | Act | RW |
| 09 | Dispose assets and sell debt | 9.2 | Hold and manage assets | 09.2.4 | Evict occupants from property | D8 | P | Act | RW |
| 09 | Dispose assets and sell debt | 9.2 | Hold and manage assets | 09.2.5 | Reappraise held assets on cycle | D8 | A | Information | SVAF, RW |
| 09 | Dispose assets and sell debt | 9.3 | Decide the disposal route | 09.3.1 | Recommend the disposal route with reasons | D8 | A | Decide | RW, COLLINS |
| 09 | Dispose assets and sell debt | 9.4 | Sell assets by Dutch auction | 09.4.1 | Set start and floor price | D8 | A+H | Outcome | RW, COLLINS |
| 09 | Dispose assets and sell debt | 9.4 | Sell assets by Dutch auction | 09.4.2 | Publish listing | D8 | A | Act | Portal |
| 09 | Dispose assets and sell debt | 9.4 | Sell assets by Dutch auction | 09.4.3 | Run auction rounds | D8 | A | Act | Portal |
| 09 | Dispose assets and sell debt | 9.4 | Sell assets by Dutch auction | 09.4.4 | Complete sale and transfer title | D8 | M | Act | RW |
| 09 | Dispose assets and sell debt | 9.4 | Sell assets by Dutch auction | 09.4.5 | Transfer vehicle registration | D8 | M | Act | SCIS |
| 09 | Dispose assets and sell debt | 9.5 | Other disposal routes | 09.5.1 | Transfer to RAMC | D8 | A+H | Act | RW |
| 09 | Dispose assets and sell debt | 9.5 | Other disposal routes | 09.5.2 | Arrange customer buy-back | D8 | H | Act | RW |
| 09 | Dispose assets and sell debt | 9.5 | Other disposal routes | 09.5.3 | Sell through broker | D8 | P | Act | Portal |
| 09 | Dispose assets and sell debt | 9.5 | Other disposal routes | 09.5.4 | Rent asset to a third party | D8 | H | Act | RW |
| 09 | Dispose assets and sell debt | 9.6 | Sell debt | 09.6.1 | Select accounts and build lots | D8 | A | Decide | RW, COLLINS |
| 09 | Dispose assets and sell debt | 9.6 | Sell debt | 09.6.2 | Set buyer terms | D8 | A+H | Outcome | RW |
| 09 | Dispose assets and sell debt | 9.6 | Sell debt | 09.6.3 | Run bid and award | D8 | A+H | Act | Portal |
| 09 | Dispose assets and sell debt | 9.6 | Sell debt | 09.6.4 | Transfer account data to buyer | D8 | A | Act | Portal |
| 09 | Dispose assets and sell debt | 9.6 | Sell debt | 09.6.5 | Track realized recovery by lot | D8 | A | Log | RW |
| 09 | Dispose assets and sell debt | 9.6 | Sell debt | 09.6.6 | Check buyer eligibility and KYC | D8 | A+H | Information | Portal |
| 09 | Dispose assets and sell debt | 9.6 | Sell debt | 09.6.7 | Handle buyer put-back claims | D8 | H | Act | RW |
| 09 | Dispose assets and sell debt | 9.7 | Manage the shortfall after sale | 09.7.1 | Calculate the shortfall after sale and notify the debtor | D8 | A | Information | RW, ALS |
| 09 | Dispose assets and sell debt | 9.7 | Manage the shortfall after sale | 09.7.2 | Offer affordable terms on the shortfall | D8 | A+H | Decide | RW |
| 09 | Dispose assets and sell debt | 9.7 | Manage the shortfall after sale | 09.7.3 | Move an unpaid shortfall to D9 | D8 | A | Act | RW |
| 10 | Write off and recover after charge-off | 10.1 | Assess write-off | 10.1.1 | Identify eligible accounts | D9 | A | Information | RW, COLLINS |
| 10 | Write off and recover after charge-off | 10.1 | Assess write-off | 10.1.2 | Prepare write-off pack | D9 | A | Information | RW |
| 10 | Write off and recover after charge-off | 10.1 | Assess write-off | 10.1.3 | Check tax criteria for write-off | D9 | A | Decide | RW |
| 10 | Write off and recover after charge-off | 10.2 | Approve and post | 10.2.1 | Approve write-off in committee | D9 | H | Outcome | RW |
| 10 | Write off and recover after charge-off | 10.2 | Approve and post | 10.2.2 | Post write-off to core and GL | D9 | A | Act | ALS |
| 10 | Write off and recover after charge-off | 10.2 | Approve and post | 10.2.3 | Send provision inputs to Finance | D9 | A | Act | COLLINS |
| 10 | Write off and recover after charge-off | 10.3 | Recover after charge-off | 10.3.1 | Place for soft recovery | D9 | A | Act | RW, Portal |
| 10 | Write off and recover after charge-off | 10.3 | Recover after charge-off | 10.3.2 | Sell post charge-off accounts | D9 | A+H | Act | RW |
| 10 | Write off and recover after charge-off | 10.3 | Recover after charge-off | 10.3.3 | Close case | D9 | A | Log | RW |
| 11 | Handle customer care and deviations | 11.1 | Answer customer contacts | 11.1.1 | Classify inbound calls, letters and messages | All | A |  | RW, EFS |
| 11 | Handle customer care and deviations | 11.1 | Answer customer contacts | 11.1.2 | Answer balance and payoff requests | All | A |  | RW, EFS |
| 11 | Handle customer care and deviations | 11.1 | Answer customer contacts | 11.1.3 | Route other requests to the case owner | All | A |  | RW, EFS |
| 11 | Handle customer care and deviations | 11.2 | X1 Dispute or complaint | 11.2.1 | Detect a dispute or complaint from inbound contact | X1 | A |  | RW, EFS |
| 11 | Handle customer care and deviations | 11.2 | X1 Dispute or complaint | 11.2.2 | Stop contact on the disputed item and build the evidence pack, black list of contacts | X1 | A |  | RW, EFS |
| 11 | Handle customer care and deviations | 11.2 | X1 Dispute or complaint | 11.2.3 | Resolve the complaint within the service level | X1 | H |  | RW, EFS |
| 11 | Handle customer care and deviations | 11.2 | X1 Dispute or complaint | 11.2.4 | Return the case to the same decision and resume timers | X1 | A |  | RW, EFS |
| 11 | Handle customer care and deviations | 11.3 | X2 Vulnerable customer or hardship | 11.3.1 | Detect vulnerability or hardship from customer statements or call notes | X2 | A |  | RW, EFS |
| 11 | Handle customer care and deviations | 11.3 | X2 Vulnerable customer or hardship | 11.3.2 | Move the case to the specialist queue with contact limits | X2 | A |  | RW, EFS |
| 11 | Handle customer care and deviations | 11.3 | X2 Vulnerable customer or hardship | 11.3.3 | Decide on a hardship plan or BOT relief program | X2 | H |  | RW, EFS |
| 11 | Handle customer care and deviations | 11.3 | X2 Vulnerable customer or hardship | 11.3.4 | Return the case to D5 | X2 | A |  | RW, EFS |
| 11 | Handle customer care and deviations | 11.4 | X3 Deceased customer | 11.4.1 | Detect a death from a certificate, registry or insurer match | X3 | A |  | RW, EFS |
| 11 | Handle customer care and deviations | 11.4 | X3 Deceased customer | 11.4.2 | Stop contact and notify heirs and the estate | X3 | A |  | RW, DMS |
| 11 | Handle customer care and deviations | 11.4 | X3 Deceased customer | 11.4.3 | File the credit life or mortgage insurance claim | X3 | A+H |  | RW |
| 11 | Handle customer care and deviations | 11.4 | X3 Deceased customer | 11.4.4 | Decide on claims against the estate | X3 | H |  | RW |
| 11 | Handle customer care and deviations | 11.4 | X3 Deceased customer | 11.4.5 | Close the case if insurance settles, or move it to D6 | X3 | A |  | RW |
| 11 | Handle customer care and deviations | 11.5 | X4 Fraud | 11.5.1 | Flag identity fraud, first-party fraud or forged documents | X4 | A |  | RW, EFS |
| 11 | Handle customer care and deviations | 11.5 | X4 Fraud | 11.5.2 | Refer the case to the fraud team | X4 | A |  | Aric |
| 11 | Handle customer care and deviations | 11.5 | X4 Fraud | 11.5.3 | Investigate the fraud | X4 | H |  | Aric |
| 11 | Handle customer care and deviations | 11.5 | X4 Fraud | 11.5.4 | Move the case to D9, or to D2 if fraud is not confirmed | X4 | A |  | RW, EFS |
| 11 | Handle customer care and deviations | 11.6 | X5 Bankruptcy or external seizure | 11.6.1 | Detect a bankruptcy filing, receivership or seizure by another creditor | X5 | A |  | RW, EFS |
| 11 | Handle customer care and deviations | 11.6 | X5 Bankruptcy or external seizure | 11.6.2 | Stop direct collection | X5 | A |  | RW, EFS |
| 11 | Handle customer care and deviations | 11.6 | X5 Bankruptcy or external seizure | 11.6.3 | File the claim with the official receiver or LED before the deadline | X5 | A+H |  | RW |
| 11 | Handle customer care and deviations | 11.6 | X5 Bankruptcy or external seizure | 11.6.4 | Move the case to D7, then D9 | X5 | A |  | RW |
| 11 | Handle customer care and deviations | 11.7 | X6 Lost contact | 11.7.1 | Detect that every phone number and address fails | X6 | A |  | RW, EFS |
| 11 | Handle customer care and deviations | 11.7 | X6 Lost contact | 11.7.2 | Skip trace through the bureau, internal data and OA sources | X6 | A |  | RW, EFS, NCB |
| 11 | Handle customer care and deviations | 11.7 | X6 Lost contact | 11.7.3 | Return the case to D2 if found, or move it to D4 or D6 if not | X6 | A |  | RW, EFS |
| 11 | Handle customer care and deviations | 11.8 | X7 Collateral event | 11.8.1 | Detect stolen, written-off or damaged collateral, or lapsed insurance | X7 | A |  | RW, EFS |
| 11 | Handle customer care and deviations | 11.8 | X7 Collateral event | 11.8.2 | File the insurance claim | X7 | A+H |  | RW |
| 11 | Handle customer care and deviations | 11.8 | X7 Collateral event | 11.8.3 | Reappraise the collateral | X7 | A |  | SVAF |
| 11 | Handle customer care and deviations | 11.8 | X7 Collateral event | 11.8.4 | Move the case to D6 | X7 | A |  | RW |
| 12 | Manage partners | 12.1 | Select and contract partners | 12.1.1 | Keep the partner panels: OAs, law firms, valuers, auction houses, buyers, brokers, real estate agencies, car dealers | All | H |  | RW |
| 12 | Manage partners | 12.1 | Select and contract partners | 12.1.2 | Onboard partners and check eligibility | All | A+H |  | Portal |
| 12 | Manage partners | 12.1 | Select and contract partners | 12.1.3 | Set fee terms and incentives against targets | All | H |  | RW |
| 12 | Manage partners | 12.2 | Exchange work with partners | 12.2.1 | Send allocations and instructions through the portal | All | A |  | Portal |
| 12 | Manage partners | 12.2 | Exchange work with partners | 12.2.2 | Receive partner results and attach them to the case | All | A |  | Portal, RW |
| 12 | Manage partners | 12.3 | Track performance and pay fees | 12.3.1 | Score partner results against targets | All | A |  | RW, Portal |
| 12 | Manage partners | 12.3 | Track performance and pay fees | 12.3.2 | Calculate and approve partner fees | All | A+H |  | RW, Portal |
| 12 | Manage partners | 12.4 | Govern partners | 12.4.1 | Hold regular reviews with each partner | All | H |  | RW |
| 12 | Manage partners | 12.4 | Govern partners | 12.4.2 | Share strategy changes, scripts and customer standards | All | H |  | Portal |
| 12 | Manage partners | 12.4 | Govern partners | 12.4.3 | Check partner conduct against customer standards | All | A+H |  | RW, Portal |
| 12 | Manage partners | 12.4 | Govern partners | 12.4.4 | Management of additional costs/services to take care of assets | All | A+H |  | RW, Portal |
| 12 | Manage partners | 12.5 | Issue notices and exit | 12.5.1 | Issue a notice when a partner misses target | D4 | A+H |  | RW, Portal |
| 12 | Manage partners | 12.5 | Issue notices and exit | 12.5.2 | End partner contracts | All | H |  | RW |
| 13 | Manage documents and correspondence | 13.1 | Read inbound documents | 13.1.1 | Scan and read inbound documents with smart OCR | All | A |  | RW |
| 13 | Manage documents and correspondence | 13.1 | Read inbound documents | 13.1.2 | Classify documents and extract key fields | All | A |  | RW |
| 13 | Manage documents and correspondence | 13.1 | Read inbound documents | 13.1.3 | Check extractions with low confidence | All | A+H |  | RW |
| 13 | Manage documents and correspondence | 13.1 | Read inbound documents | 13.1.4 | Attach documents to the case and index them | All | A |  | RW, Data lake |
| 13 | Manage documents and correspondence | 13.2 | Send letters and notices | 13.2.1 | Generate letters from templates | All | A |  | RW |
| 13 | Manage documents and correspondence | 13.2 | Send letters and notices | 13.2.2 | Check letters against customer standards before release | All | A |  | RW |
| 13 | Manage documents and correspondence | 13.2 | Send letters and notices | 13.2.3 | Send letters and record proof of delivery | All | A |  | DMS, WIN |
| 13 | Manage documents and correspondence | 13.3 | Store and retain documents | 13.3.1 | Apply retention rules | All | A |  | RW |
| 13 | Manage documents and correspondence | 13.3 | Store and retain documents | 13.3.2 | Answer document requests from legal and audit | All | A+H |  | RW |
| 13 | Manage documents and correspondence | 13.3 | Store and retain documents | 13.3.3 | Maintain repository of addresses, phones, contacts and connected people | All | A+H |  | RW |
| 13 | Manage documents and correspondence | 13.3 | Store and retain documents | 13.3.4 | Recovering or re-signing or re-creating of missing documents about collateral or lost credit documentation | All | A+H |  | RW |
| 13 | Manage documents and correspondence | 13.4 | Control document custody | 13.4.1 | Record every movement of an original document | All | A |  | RW |
| 13 | Manage documents and correspondence | 13.4 | Control document custody | 13.4.2 | Check originals out to lawyers, courts and the land office and back | All | A+H |  | RW |
| 13 | Manage documents and correspondence | 13.4 | Control document custody | 13.4.3 | Reconcile the custody list to the vault | All | H |  | RW |
| 14 | Set strategy, policy and decision rules | 14.1 | Set strategy and treatment policy | 14.1.1 | Have dashboard based on major criteria | All | H |  | Power BI |
| 14 | Set strategy, policy and decision rules | 14.1 | Set strategy and treatment policy | 14.1.2 | Set segments and the treatment policy by major dimensions | All | H |  | RW |
| 14 | Set strategy, policy and decision rules | 14.1 | Set strategy and treatment policy | 14.1.3 | Set customer experience standards from BOT and SCB rules | All | H |  | RW |
| 14 | Set strategy, policy and decision rules | 14.2 | Set decision rules and limits | 14.2.1 | Keep the delegation of authority table | All | H |  | RW |
| 14 | Set strategy, policy and decision rules | 14.2 | Set decision rules and limits | 14.2.2 | Write the rules, triggers and timers for each decision | All | H |  | RW |
| 14 | Set strategy, policy and decision rules | 14.2 | Set decision rules and limits | 14.2.3 | Release rule changes after testing | All | A+H |  | RW |
| 14 | Set strategy, policy and decision rules | 14.2 | Set decision rules and limits | 14.2.4 | Calendar management | All | A+H |  | RW |
| 14 | Set strategy, policy and decision rules | 14.2 | Set decision rules and limits | 14.2.5 | Manage users, user types, orgchart, subordination, regions, hierarchy | All | A+H |  | RW |
| 14 | Set strategy, policy and decision rules | 14.2 | Set decision rules and limits | 14.2.6 | Management of OA, coverage, categorization, capacity, results, provided services | All | A+H |  | RW |
| 14 | Set strategy, policy and decision rules | 14.3 | Set fees, charges and waivers | 14.3.1 | Set collection fees and charges within the legal limits | All | H |  | RW |
| 14 | Set strategy, policy and decision rules | 14.3 | Set fees, charges and waivers | 14.3.2 | Apply fees and charges to accounts | All | A |  | RW, ALS |
| 14 | Set strategy, policy and decision rules | 14.3 | Set fees, charges and waivers | 14.3.3 | Approve fee and interest waivers within delegation | All | A+H |  | RW |
| 15 | Manage performance, data and AI | 15.1 | Report performance | 15.1.1 | Produce scorecards by product and decision from the decision log | All | A |  | Power BI |
| 15 | Manage performance, data and AI | 15.1 | Report performance | 15.1.2 | Review results and agree actions | All | H |  | Power BI |
| 15 | Manage performance, data and AI | 15.2 | Test strategies | 15.2.1 | Run champion and challenger tests | All | A |  | RW |
| 15 | Manage performance, data and AI | 15.2 | Test strategies | 15.2.2 | Approve the switch to a new champion | All | A+H |  | RW |
| 15 | Manage performance, data and AI | 15.3 | Monitor agents and models | 15.3.1 | Track override rates, drift and errors | All | A |  | RW |
| 15 | Manage performance, data and AI | 15.3 | Monitor agents and models | 15.3.2 | Review overrides and agent errors | All | H |  | RW |
| 15 | Manage performance, data and AI | 15.3 | Monitor agents and models | 15.3.3 | Retrain and release models and agents | All | A+H |  | COLLINS, RW |
| 15 | Manage performance, data and AI | 15.4 | Manage data quality | 15.4.1 | Reconcile the case list to ALS daily | All | A |  | Data lake, ALS |
| 15 | Manage performance, data and AI | 15.4 | Manage data quality | 15.4.2 | Delete data and docs from archive and database after debt sale, fraud proof or PDP request | All | A |  | Data lake, ALS |
| 15 | Manage performance, data and AI | 15.4 | Manage data quality | 15.4.3 | Fix data quality exceptions | All | H |  | Data lake |
| 15 | Manage performance, data and AI | 15.5 | Improve processes | 15.5.1 | Log QA findings and improvement ideas in the backlog | All | A |  | RW |
| 15 | Manage performance, data and AI | 15.5 | Improve processes | 15.5.2 | Update SOPs and rules | All | H |  | RW |
| 15 | Manage performance, data and AI | 15.6 | Track benefits and value | 15.6.1 | Keep the benefits ledger by lever | All | A |  | Power BI |
| 15 | Manage performance, data and AI | 15.6 | Track benefits and value | 15.6.2 | Attribute results to each lever | All | A+H |  | Power BI |
| 15 | Manage performance, data and AI | 15.6 | Track benefits and value | 15.6.3 | Run the monthly benefits review | All | H |  | Power BI |
| 15 | Manage performance, data and AI | 15.7 | Feed results back to credit policy and origination | 15.7.1 | Report contact data quality and early default by origination channel | All | A |  | Data lake, Power BI |
| 15 | Manage performance, data and AI | 15.7 | Feed results back to credit policy and origination | 15.7.2 | Agree policy changes with credit risk | All | H |  | Power BI |
| 15 | Manage performance, data and AI | 15.8 | Classify, stage and re-age accounts | 15.8.1 | Apply one definition of flow rate, cure, durable cure and re-ageing | All | A |  | Data lake |
| 15 | Manage performance, data and AI | 15.8 | Classify, stage and re-age accounts | 15.8.2 | Classify and stage accounts under BOT rules | All | A |  | ALS, data lake |
| 15 | Manage performance, data and AI | 15.8 | Classify, stage and re-age accounts | 15.8.3 | Approve re-ageing exceptions | All | A+H |  | RW |
| 16 | Manage risk, control and compliance | 16.1 | Run quality assurance | 16.1.1 | Select cases for QA by rule | All | A |  | RW, EFS |
| 16 | Manage risk, control and compliance | 16.1 | Run quality assurance | 16.1.2 | Review cases against the SOP, calculate incentive input | All | H |  | RW, EFS |
| 16 | Manage risk, control and compliance | 16.2 | Control conduct | 16.2.1 | Check every outbound contact against customer standards | All | A |  | RW, EFS |
| 16 | Manage risk, control and compliance | 16.2 | Control conduct | 16.2.2 | Review conduct breaches | All | H |  | RW, EFS |
| 16 | Manage risk, control and compliance | 16.3 | Manage model and agent risk | 16.3.1 | Review agents and models before release | All | H |  | RW |
| 16 | Manage risk, control and compliance | 16.3 | Manage model and agent risk | 16.3.2 | Fall back to rules when an agent fails or confidence is low | All | A |  | RW |
| 16 | Manage risk, control and compliance | 16.4 | Answer audit and regulatory requests | 16.4.1 | Query the decision log for audit requests | All | A |  | RW |
| 16 | Manage risk, control and compliance | 16.4 | Answer audit and regulatory requests | 16.4.2 | Prepare responses to BOT and audit | All | A+H |  | RW |
| 16 | Manage risk, control and compliance | 16.5 | Control access and data protection | 16.5.1 | Apply PDPA access by role and by agent | All | A |  | RW |
| 16 | Manage risk, control and compliance | 16.6 | Manage incidents and continuity | 16.6.1 | Detect a failed load, service or agent and raise an incident | All | A |  | RW |
| 16 | Manage risk, control and compliance | 16.6 | Manage incidents and continuity | 16.6.2 | Switch to rules fallback or manual working | All | A+H |  | RW |
| 16 | Manage risk, control and compliance | 16.6 | Manage incidents and continuity | 16.6.3 | Review the incident and close it | All | H |  | RW |
| 16 | Manage risk, control and compliance | 16.7 | Handle data subject requests | 16.7.1 | Log a data subject request and find every record held | All | A |  | RW, data lake |
| 16 | Manage risk, control and compliance | 16.7 | Handle data subject requests | 16.7.2 | Answer the request within the legal time | All | A+H |  | RW |
| 17 | Run the decision center | 17.1 | Route recommendations for approval | 17.1.1 | Route each recommendation to the approver by limit | D1 to D9 | A | Outcome | RW |
| 17 | Run the decision center | 17.1 | Route recommendations for approval | 17.1.2 | Accept, change or reject with a reason | D1 to D9 | A+H | Outcome | RW |
| 17 | Run the decision center | 17.1 | Route recommendations for approval | 17.1.3 | Escalate overdue approvals by timer | D1 to D9 | A | Outcome | RW |
| 17 | Run the decision center | 17.2 | Keep the decision log | 17.2.1 | Record one log entry per decision | D1 to D9 | A | Log | RW |
| 17 | Run the decision center | 17.2 | Keep the decision log | 17.2.2 | Record actions and outcomes, including cash recovered | D1 to D9 | A | Log | RW |
| 17 | Run the decision center | 17.3 | Feed results back | 17.3.1 | Send outcomes to the data store and COLLINS for retraining | D1 to D9 | A | Log | Data lake, COLLINS |
| 18 | Plan capacity and allocate work | 18.1 | Forecast inflow and workload | 18.1.1 | Forecast inflow by product, bucket, region and channel | D2, D4 | A |  | Capacity model |
| 18 | Plan capacity and allocate work | 18.1 | Forecast inflow and workload | 18.1.2 | Convert inflow into workload by role | D2, D4 | A |  | Capacity model |
| 18 | Plan capacity and allocate work | 18.2 | Plan capacity and rosters | 18.2.1 | Plan staff and partner capacity against workload | D2, D4 | A+H |  | Capacity model |
| 18 | Plan capacity and allocate work | 18.2 | Plan capacity and rosters | 18.2.2 | Set the weekly roster | D2, D4 | H |  | Capacity model |
| 18 | Plan capacity and allocate work | 18.3 | Build and allocate work lists | 18.3.1 | Build phone and field work lists by priority | D2, D4 | A |  | Dialer, field application |
| 18 | Plan capacity and allocate work | 18.3 | Build and allocate work lists | 18.3.2 | Allocate work to teams, people and partners by rule | D2, D4 | A |  | RW, partner portal |
| 19 | Manage payments and reconciliation | 19.1 | Receive payments | 19.1.1 | Receive payments from every channel | D3, D5, D6 | A |  | Core banking |
| 19 | Manage payments and reconciliation | 19.1 | Receive payments | 19.1.2 | Identify the account and case for each payment | D3, D5, D6 | A |  | Core banking, RW |
| 19 | Manage payments and reconciliation | 19.2 | Apply payments to accounts | 19.2.1 | Apply payments in the order the policy sets | D3, D5, D6 | A |  | Core banking |
| 19 | Manage payments and reconciliation | 19.2 | Apply payments to accounts | 19.2.2 | Handle partial payments, reversals and overpayment refunds | D3, D5, D6 | A+H |  | Core banking, RW |
| 19 | Manage payments and reconciliation | 19.3 | Reconcile and correct | 19.3.1 | Reconcile cash to the case and to the core daily | D3, D5, D6 | A |  | RW, core banking |
| 19 | Manage payments and reconciliation | 19.3 | Reconcile and correct | 19.3.2 | Correct posting errors | D3, D5, D6 | H |  | Core banking |

## Key

| Key |  |  |
|---|---|---|
| How the architecture is numbered, and what each layer, mode and step means. |  |  |
| Item | Term | Meaning |
| Numbering | L1 | A process area, numbered 01 to 19. Each L1 carries one decision or serves all of them. |
| Numbering | L2 | A sub-process inside one L1, numbered L1.n, for example 7.3. |
| Numbering | L3 | A process inside one L2, numbered with the L1 as two digits, for example 07.3.1. The items under an L2 are always called L3 processes. |
| Layer | Core | The case moves through these processes in order. 01 to 05 run on EFS before day 90; 06 to 10 run on the Workbench. |
| Layer | Support | Run across every core process when they are needed. |
| Layer | Manage | Set the rules every process runs by, and read the results. |
| Layer | Across all | Runs at every decision point in every core process. |
| Mode | A  Automated | A rule, engine or agent completes the step. No person is involved; the result is in the log. |
| Mode | A+H  AI assisted | An agent or engine prepares, recommends or drafts. A person decides, approves or completes. |
| Mode | H  Human | A bank employee carries out the step. The Workbench prepares the task and records the result. |
| Mode | M  Manual | A physical or legal act done outside any system, such as a title transfer. The Workbench records that it happened. |
| Mode | P  Partner | A partner carries out the step: an agency, law firm, valuer, auction house, broker or court officer. |
| Decision pattern | Information | Gather and check the facts the decision needs. |
| Decision pattern | Decide | Apply a rule, a model or an agent to choose an option. |
| Decision pattern | Outcome | Make the choice final, or route it to the person with the authority to approve it. |
| Decision pattern | Act | Carry out the choice in the Workbench, another system or through a partner. |
| Decision pattern | Log | Record the decision, the action and the result once, in the decision log. |
| Decision | D1 to D9 | The nine decisions a case passes through: act on the signal, reach the customer, promise kept, escalate, offer a restructure, which route, next legal step, how to dispose, write off or pursue. |
| Decision | X1 to X7 | The seven deviations that interrupt a decision: dispute or complaint, vulnerable customer or hardship, deceased customer, fraud, bankruptcy or external seizure, lost contact, collateral event. |
| Systems | RW | The Recovery Workbench. |
| Systems | Portal | The partner portal. |

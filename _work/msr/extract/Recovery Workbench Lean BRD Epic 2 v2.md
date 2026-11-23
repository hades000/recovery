Recovery Workbench

Lean BRD, Epic 2

SCB Collections and Recovery. Henka Group, 28 October 2026

| Item | Detail |
|---|---|
| Document | Recovery Workbench lean BRD, Epic 2 |
| Version | 1 |
| Date | 28 October 2026 |
| Prepared by | Henka Group |
| Structure | ISO/IEC/IEEE 29148, lean |
| Release | 31 December 2026 |
| Status | For business scope approval |


# 1. Problem and outcome

## 1.1 What is wrong today

A case reaching 90 days past due arrives from collections by a weekly manual file at day 91 and is first worked at about day 100. Contact history found before day 90 does not travel with it. Hand-offs run by email, and a manager cannot see every case with its owner and age. Approvals are replies to email. Letters go out with no proof of delivery on the case, and payments are not matched to plans, so a broken plan is found late. Epic 1 gives one reconciled case list with no screens for business users.

| Baseline | Figure today |
|---|---|
| Hand-off points on one case; email hand-offs | 310, of which 191 pass through three or more people; 346 |
| Transfers of one litigation case | 58 |
| Contactability | 40 percent |
| Litigation filings that breach their service level | 30 to 40 percent |
| Recovery rate on NPL, 2026 to date | 66.3 percent |
| Litigation, deed in lieu and restructure turnaround | 21, 26 and 23 working days |


## 1.2 Outcome when Epic 2 is live

Epic 2, Foundation 2, releases on 31 December 2026 and completes the foundation. The case arrives the morning after it reaches 90 days past due with its contact and promise history and the customer's other products. Every case has one owner, a timer and one next action. Owners and managers work from queues on screen. Approvals route on the delegation of authority. Litigation notices are generated and approved in the Workbench. Letters go out with proof of delivery, and SMS and LINE with their result on the case. The steering committee reads the same numbers the teams work with.

Business roles receive real users (DL39): case owner, team manager, phone collector, litigation officer, capacity and workforce planner, product heads, Head of Litigation, risk and model risk officer, reporting and BI analyst, and the Tribe lead and squad members.

# 2. Scope

## 2.1 In scope

| Module | Capability |
|---|---|
| P1, P2 Data and integration | Hand-over from EFS through the COLLINS load with full history. ACE plan status and the customer's other products on the case. Credit approval pack for NLEADS; booking confirmed from the next ALS load. Data products for treatments and plans. Queue write for models and agents, behind a flag. |
| P3 Case and workflow | My queue and team queues with ageing and breach flags. Transfer and reassignment with a reason code. Timers, deviation flag and full timeline on the case. One next action per case. Treatment record with plan timers. |
| P4 Access | Partner identities through the external gateway, ready for Epic 5. Joiner, mover and leaver changes. |
| P5 Document hub | Contract, CA and mortgage documents from approved templates. Field photos and bills into the intake. Extraction for contracts and court documents. E-discovery and retention by class. |
| P6 Communications | Letters to WIN with proof of delivery. SMS through NSS and LINE through LINE OA. Conduct and consent check before every contact. E-signature where Legal permits. |
| P7, P8, P9 | Approval routing on the delegation of authority with escalation. Approval screen for demand and recall notices (D7.1). Decision log query for audit. Payment matching with an exception list. Steering dashboard. |
| P10, S8 | Agent monitoring with drift alerts. Deviations X1 to X7 detected by rule with contact stops and routing to the handler. |


## 2.2 Out of scope

| Excluded from Epic 2 | Where it is done |
|---|---|
| Settlement and deed in lieu to booking; asset record and listing; agents at L1 | Epic 3 |
| The route decision D6; guarantee and TCG claims; auction; self-service; posting | Epic 4 |
| Litigation with law firms on the partner portal | Epic 5 (DL03) |
| Debt sale, write-off, partner panel and fees | Epic 6 |
| Deviation flows end to end; partner scoring; the field app | Epic 7 |
| Full administration, agent autonomy step-ups, regulatory returns | Epic 8 |
| Restructure affordability and plan calculation | Not in the Workbench: the ACE restructure calculator |
| Collections before 90 days past due (D1 to D4) | Not in the Workbench: EFS and the ACE collection module |


# 3. Business rules

## 3.1 Eligibility

- A case transferred from collections reaches the Workbench on the day of transfer through the COLLINS load, at one hand-over point, 90 days past due (DL16), used by every rule and report.

- The EFS contact outcomes that enter the ledger are a named list for the collection period (DL29).

- A case with a live plan in ACE shows the plan status. A duplicate case for the same customer and product merges into the earlier case.

- Every offer made to a customer has a treatment record with type, terms, approval and outcome.

## 3.2 Case status and how a case moves

The eight statuses from Epic 1 are all in use. Each case also carries a service level state (inside, approaching or past), a deviation flag, a queue and owner, and one next action with owner and due date, produced from the rule that moved the case.

| Status | Meaning | Moves to |
|---|---|---|
| New | Created at 90 days past due with its history; no owner yet | Assigned, when the allocation rule matches |
| Assigned | Owner and queue set by rule; the stage clock starts | In progress, when the first task starts |
| In progress | The owner or the Workbench is working a task | A waiting status, when an offer, instruction or approval request goes out |
| Waiting customer | Offer, notice or request with the customer; validity timer runs | In progress, on reply or timer expiry |
| Waiting partner | Instruction with a partner; service level timer runs | In progress, on result or timer expiry |
| Waiting approval | Recommendation with the approver the delegation of authority names | In progress, on decision or escalation |
| On hold | Paused by a deviation or legal hold; prescription clock keeps running | The status it paused in, or Closed |
| Closed | Cured, settled, sold, or written off with recovery ended | No further action |


An approval is waiting, approved, approved with changes within the approver's limit, rejected with a coded reason, or escalated. A rejected item returns to the point the route rule names.

## 3.3 Allocation, routing and approval

- A manual transfer or reassignment needs a reason code from the agreed list. The case keeps its status and clocks.

- Cases of an owner who leaves, is absent beyond the threshold or is over the cap are reallocated inside the team (DL23).

- A model or agent may place a case on a queue under a service identity with the same checks as a person. Its work and rule-allocated work share one queue order.

- An approval goes to the approver the delegation of authority names for the decision, product and amount (DL18). Above the limit it is refused and raised to the next approver. A person may not approve a decision they proposed or prepared.

- An override needs a coded reason, reported monthly. An unanswered approval escalates at its service level. The limit, rule version and approver are logged.

- Demand and recall notices (D7.1) are the first decision approved this way.

## 3.4 Exception handling

| Deviation | Handled by | Epic 2 rule |
|---|---|---|
| X1 Dispute or complaint | Complaint officer | Contact stop; complaint matched to the contact before it |
| X2 Vulnerable customer or hardship | Hardship and vulnerability specialist | Contact stop |
| X3 Deceased customer | Specialist, with Legal for estate claims | Contact stop |
| X4 Fraud | Fraud investigator | Referred to the fraud team; recovery action held |
| X5 Bankruptcy or external seizure | Legal counsel | Direct collection stops; claim deadline clock starts |
| X6 Lost contact | Agent, within policy | A new verified contact point clears it |
| X7 Collateral event | Agent proposes; a person approves the claim | Routed to its handler |


- A deviation pauses the stage clock, keeps the prescription clock running and does not replace the status. A code with no owner goes to the team manager and is recorded as unmapped.

- A next action past its due date escalates like a service level breach. A case with no next action is reported as an exception.

- A booking missing from the next ALS load creates a task. An unmatched payment goes to the exception list; a missed payment raises an event the next day.

## 3.5 Outbound contact

- Every outbound contact carries a conduct check result; a contact that fails is held.

- Consent is held per channel. Withdrawn consent stops that channel; statutory notices continue.

- The notice period runs from proof of delivery. Signature is electronic where Legal permits and wet ink where Legal requires.

## 3.6 Rule governance

- Every rule, limit, threshold, template, name, queue, role, timer and route is a versioned data row, changed by a validated load with no code release (DT02).

- A load is checked for schema, overlapping rows, unreachable rows, a missing default row and a set of test cases. A load that fails a check is refused.

- Each version carries a valid from date, author and approver, and the previous version is restored by one action. The center of excellence analyst loads; the risk and model risk officer approves. One person may not hold both roles.

- A policy owner decides a policy change. The Workbench applies it as a new data version.

- A change to the delegation of authority is versioned, approved and dated; open items keep the version they were decided under.

# 4. Process and ownership

| L3 | L3 process | Today | After Epic 2 | Business owner |
|---|---|---|---|---|
| 06.1.1 | Transfer case and history from EFS | Weekly file at day 91 | Day of transfer, with full history | Recovery Strategy with Risk |
| 06.1.3; 11.2.1 to 11.8.1 | Screen and detect deviations X1 to X7 | Found by the person on the case | Detected by rule; contact stops | Shared operations, a handler per deviation |
| 18.3.2 | Allocate and reassign work | By email | Queue screens, reason codes | Shared operations |
| 17.1.1 to 17.1.3 | Route, decide and escalate approvals | Reply to email | On the delegation of authority | Center of excellence; product heads |
| 14.2.1 | Keep the delegation of authority table | Regulation text | Versioned table with holders | Risk with the product heads |
| 08.1.1 | Issue demand and recall notices | Approved outside the case | Generated and approved on screen | Head of Litigation |
| 13.2.2, 13.2.3; 16.2.1 | Check contacts; send letters with proof of delivery | Notice period from printing | Checked before release; delivery on case | Conduct and QA officer; Shared operations |
| 05.3.1 to 05.4.1 | Approve, book and track a plan | Re-keyed into NLEADS | Pack for NLEADS; booking matched | Credit Administration |
| 19.1.2, 19.3.1 | Match payments to the case daily | By hand | Rules as data; exception list | Credit Administration |
| 16.4.1; 15.1.1 | Answer audit from the log; report results | Email and team files | Log query; steering dashboard | Internal audit; center of excellence |


# 5. Constraints

## 5.1 Policies and regulation

- Delegation of authority under Regulation กกค.540031 as amended by กกค.690070. The build loads the levels and limits now and adds holders when signed (DL18). Approval routing cannot pass UAT without the signed table.

- Personal Data Protection Act: consent per channel; masking by role (DL26).

- Customer standards from the Bank of Thailand and SCB rules are applied by the conduct check. Relief scheme eligibility is decided in ACE.

## 5.2 Systems and architecture

- Built inside ACE as a modular monolith with programmatic workflow (DT07 to DT09), using the ACE components (DL08, DL31).

- Data through the COLLINS daily batch and file loads; no real-time feed today (DT12). Same-day triggers to name under DL06: case transferred from EFS, payment received, legal event.

- The document hub is the system of record for recovery documents (DT06). No legacy system is enhanced (DL12).

- Partner access needs an architecture change with one to three months lead time, raised in November for law firms in Epic 5 (DL03).

- Kanban delivery with a sponsor progress review every two weeks. Build from 30 November, SIT 14 to 18 December, UAT 21 to 25 December. A requirement that fails is switched off by its feature flag.

# 6. Dependencies

## 6.1 Teams, systems and data

| ID | What is needed | From | Needed by | Decision | Decision owner, date |
|---|---|---|---|---|---|
| DEP-06 | Restructure calculator and plan status from ACE | ACE team, collection squad | 1 Dec | DL14, DL30 | K. Tee with K. Book and the product owner, 6 Nov |
| DEP-07 | EFS hand-over and contact history in COLLINS | Collection squad, data engineering | 30 Nov | DL29 | Data lead with the business lead, 13 Nov |
| DEP-08 | Builder of shared items: dispatch, EFS automation, extraction, generation | IT lead, product owner | 30 Nov | DL30 | IT lead with the product owner, 13 Nov |
| DEP-13 | Legacy systems kept, changed or retired | IT lead | 20 Nov | DL12 | K. Tony with K. Book, 7 Nov |
| DEP-19 | Session, inactivity and break-glass timers | SCB IT security | 20 Nov | DL38 | SCB IT security, 20 Nov |
| DEP-23 | Delegation of authority: holders, limits, substitutes | Risk, product heads | 30 Nov | DL18 | Risk with the product heads, 30 Nov |
| DEP-24 | Service levels per status and caseload caps | Business lead, product owner | 13 Nov | DL22, DL23 | Business lead; Product owner; 13 Nov |
| DEP-25 | Letter templates approved in Thai and English | Legal counsel | 13 Nov | DL28 | Product owner, 13 Nov |
| DEP-27 | Thai labels and message wording | Business lead, Legal, Compliance | 5 Nov | DL10 | Business lead with Legal and Compliance, 5 Nov |
| DEP-10 | Partner access through the external gateway | Architecture team | 1 Feb 2027 | DL03 | K. Book with the architecture team, 29 Oct |


## 6.2 Open decisions

The build uses the stated answer until the owner decides. Dates are 2026.

| ID | Question | Answer the build uses | Owner | By |
|---|---|---|---|---|
| DL03 | Who makes the partner access change? | The Workbench or ACE team raises it in November | K. Book with the architecture team | 29 Oct |
| DL06 | Which interfaces need same-day data? | Daily COLLINS batch for all Epic 2 data | K. Book with K. Pipat | 30 Oct |
| DL09 | Who tests from the business? | Testers with the squads, then a one-week UAT | K. Tee with K. Jao | 31 Oct |
| DL14 | Who builds TDR, FCR, OA and DIL? | The ACE team | K. Tee with K. Book and the product owner | 6 Nov |
| DL22, DL23 | Service levels; caseload cap and queue order | Loaded as parameters when supplied | Business lead; Product owner | 13 Nov |
| DL30 | Who builds SMS and LINE dispatch and document generation? | The bank-wide service owner where one exists | IT lead with the product owner | 13 Nov |
| DL31 | Who owns screen design? | The TechX designer under the product owner | Product owner | 6 Nov |
| DL39 | Roles with real users? | The business roles in section 1.2 | Business lead | 20 Nov |
| DL18 | Approval holders, limits and substitutes? | Regulation levels and limits; holders when signed | Risk with the product heads | 30 Nov |


## 6.3 Support needed from the business

| Support | From | When |
|---|---|---|
| Sign the delegation of authority | Risk with the product heads | 30 Nov |
| Approve notice approval rules and litigation notice wording | Head of Litigation with Legal counsel | Before UAT |
| Approve SMS and LINE content and the contact rules | Conduct and QA officer with Compliance | Before UAT |
| Use the queue and transfer screens with real cases in UAT | Case owners and team managers | 21 to 25 Dec |
| Attend training before go-live | Every role with real users | Two weeks before |


# 7. Success measures

Read from the decision log and shown on the steering dashboard by product and route. The benefit check (gate G6) is on 31 January 2027.

| Measure | Baseline | Target | By when | Owner |
|---|---|---|---|---|
| Time from 90 days past due to an owner | About ten days | Owner on the day of transfer | 31 Jan 2027 | Business lead |
| Open cases with one next action | Baseline from the first month live | 100 percent | 31 Jan 2027 | Team managers |
| Transfers made in the Workbench with a reason code | 346 email hand-offs | 100 percent | 31 Jan 2027 | Team managers |
| Decisions within the delegation of authority | Not counted today | 100 percent | From 31 Dec 2026 | Risk |
| Cases with a breached prescription date | Baseline from the first month live | Zero | From 31 Dec 2026 | Head of Litigation |
| Cases inside the service level; cases per owner | Baseline from the first month live | Service levels (DL22); within the cap (DL23) | 31 Jan 2027 | Team managers |
| Letters with proof of delivery on the case | No delivery status on the case | 100 percent of WIN letters | 31 Jan 2027 | Head of Litigation |
| Payments matched or on the exception list | Baseline from the first month live | 100 percent | 31 Jan 2027 | Credit Administration |
| Selected manual processes the Workbench runs | 0 percent | 20 percent | Q1 2027 | Business lead |
| Recovery rate on NPL | 66.3 percent | 68.0 percent; 73.0 percent for 2027 | Q1 2027 | Chief Debt Recovery Management Office |


# 8. Business scope approval

The Epic 2 design is signed on 20 November 2026 (gate G1), before the build starts on 30 November 2026.

| Role | Approves | Status |
|---|---|---|
| Sponsor | Problem, outcome, scope and success measures | To approve |
| Business lead | Hand-over rule, statuses, next action, service levels and real users | To approve |
| Product owner | Scope boundary and the story set | To approve |
| Risk with the product heads | Delegation of authority, approval routing and overrides | To approve |
| Head of Litigation | Notice approval rules and litigation measures | To approve |
| Legal counsel | Notice and contract templates and e-signature | To approve |
| Compliance | Consent per channel, contact stops, masking and retention | To approve |
| Conduct and QA officer | Conduct check and message content | To approve |
| Credit Administration | Payment matching and booking confirmation | To approve |
| Tribe lead | Process ownership, constraints and the steering dashboard | To approve |


# 9. How the user stories follow

Epic 2 meets 71 program requirements through 32 stories in Recovery Workbench User Stories Epic 2. The same file carries 3 Epic 3 agent stories (RWB-E2-028, RWB-E2-029, RWB-E2-030), counted with Epic 3.

| Requirement group | Requirement IDs | Count |
|---|---|---|
| Recovery data | REQ-RDF-014 | 1 |
| Case and workflow core | REQ-CWC-017 to 020 | 4 |
| Document hub | REQ-DCM-012 to 013, 017 to 019 | 5 |
| Decision record and integration | REQ-DRI-012 to 013 | 2 |
| Access and authority | REQ-ACA-011 to 012 | 2 |
| Hand-over from collections | REQ-CHO-001 to 010 | 10 |
| Work management | REQ-WKM-001 to 009, 011 to 016 | 15 |
| Approval and delegation | REQ-APD-001 to 011 | 11 |
| Deviation handling | REQ-DVH-001 to 007, 009 to 010 | 9 |
| Outbound contact and case view | REQ-OCC-003 to 006, 008 to 010 | 7 |
| Interaction ledger | REQ-ILG-009 to 013 | 5 |


| Module | Stories | Must | Points |
|---|---|---|---|
| P1 Recovery data engine | 1 | 0 | 5 |
| P2 Integration | 10 | 8 | 61 |
| P3 Case and workflow | 5 | 5 | 31 |
| P4 Access and administration | 1 | 0 | 5 |
| P5 Document hub | 4 | 4 | 29 |
| P6 Communications | 3 | 3 | 21 |
| P7 Decision center and log | 3 | 3 | 21 |
| P8 Payments and posting | 2 | 2 | 13 |
| P9 Reporting | 1 | 0 | 5 |
| P10 Agent runtime | 2 | 1 | 8 |
| Total | 32 | 26 | 199 |


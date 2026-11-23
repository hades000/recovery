SCB Collections and Recovery. Henka Group, 22 November 2026.
(C) Siam Commercial Bank and Henka Pte Ltd

Recovery Workbench

Business requirements, Epic 2

SCB Collections and Recovery. Henka Group, 28 October 2026

| Item | Detail |
|---|---|
| Document | Recovery Workbench business requirements, Epic 2 |
| Version | 1 |
| Date | 28 October 2026 |
| Prepared by | Henka Group |
| Release | 31 December 2026 (tentative) |
| Structure | ISO/IEC/IEEE 29148, until the SCB X requirement template is adopted (DL13) |
| Realigned version | 3 |
| Realignment date | 22 November 2026 |
| Realignment decision | D-RCV-60 microservice realignment |
| Status | Draft |
| Author of this version | BRD Builder (AI draft) |
| Reviewers | The five approvers of section 10.2 |
| Tool | T3 Code / OpenCode / DeepSeek v4.1 Flash |

# 1. What this epic delivers

Epic 2, Foundation 2, releases on 31 December 2026 (tentative).

One owner and a timer on every case, full history on one screen, approval routing, litigation notices generated and approved, letters with proof of delivery, SMS and LINE, and the steering dashboard.

| Measure | Value |
|---|---|
| Requirements at development detail | 32 |
| Must | 26 |
| Program requirements this epic meets | 71 |


# 2. Who benefits

| Who | Requirements that serve them |
|---|---|
| A case owner | 9 |
| A restructure operations officer | 5 |
| A team manager | 3 |
| A data product owner | 2 |
| A litigation officer | 2 |
| An AI product owner | 2 |
| A product owner | 1 |
| An internal auditor | 1 |
| A program manager | 1 |
| An approver | 1 |
| A customer | 1 |
| A partner manager | 1 |
| A field collector | 1 |
| A document hub owner | 1 |
| A reconciliation officer | 1 |


# 3. Requirements at development detail

Each requirement is one backlog story. The requirement states what the Workbench does, the benefit states what changes for the user, and the scenarios are the acceptance criteria in the story.

## 3.1 P1 Recovery data engine

| Key | Requirement | What the Workbench does | For | User benefit | Priority | Tests |
|---|---|---|---|---|---|---|
| RWB-E2-010 | Stage 2 data products: contracts, plans and treatments | The stage 2 data products (treatments, plans, contracts, guarantees) added to the recovery data store with their systems of record | A data product owner | The settlement, TDR and DIL screens in Epic 3 read from one store | Should | 3 |


## 3.2 P2 Integration

| Key | Requirement | What the Workbench does | For | User benefit | Priority | Tests |
|---|---|---|---|---|---|---|
| RWB-E2-001 | EFS hand-over with full history from the COLLINS load | The case created or updated from the EFS data in the COLLINS daily load, with the full contact and promise history | A case owner | The case starts the morning after it reaches 90 days past due | Must | 3 |
| RWB-E2-002 | ACE plan status on the case | The restructure plan status from the ACE common module (created, approved, booked, broken) on the case | A case owner | A case with a live plan is never treated as if it had none | Must | 3 |
| RWB-E2-003 | Customer's other products on the case | The customer's other products and their status on the case, from the customer profile ACE receives through COLLINS | A case owner | I can see the whole relationship before I decide a route | Should | 3 |
| RWB-E2-006 | Credit approval pack for NLEADS | The credit approval pack for an approved plan prepared for submission in NLEADS, with the result recorded on the treatment | A restructure operations officer | A plan reaches credit without re-keying the case facts | Must | 3 |
| RWB-E2-007 | Booking confirmation from the ALS load | The booked terms or settlement matched from the next day's ALS load to the approved treatment, with a task when the booking is missing | A restructure operations officer | Every approved decision is confirmed as booked | Must | 3 |
| RWB-E2-023 | Automated EFS file load | The EFS file load automated end to end and reconciled daily | A data product owner | One checked path remains | Should | 3 |
| RWB-E2-033 | Case and queue list with status, owner and ageing | Every case in every queue with its status, owner, age in state and breach flag | A team manager | I can see where work is sitting without asking anyone | Must | 3 |
| RWB-E2-034 | Interaction ledger on the case and from every channel | Every interaction on the case recorded in one ledger | A case owner | Contactability is not found and then lost again | Must | 3 |
| RWB-E2-035 | Next action on the case | The case to tell me what to do next and by when | A case owner | I never open a case and have to work out what it needs | Must | 4 |
| RWB-E2-036 | Queue write interface for models and agents | An interface that lets a model or an agent place a case on a queue | An AI product owner | Analytical output reaches a person the next working day instead of through a weekly manual step | Must | 4 |


## 3.3 P3 Case and workflow

| Key | Requirement | What the Workbench does | For | User benefit | Priority | Tests |
|---|---|---|---|---|---|---|
| RWB-E2-004 | Treatment entity and plan timers data model | The treatment entity (TDR, settlement, DIL: terms, approval, booking, outcome) and its plan timers in the case store, with the data product for reporting | A product owner | TDR and DIL run inside the Workbench from Epic 2 and every plan has a record | Must | 3 |
| RWB-E2-011 | Queue view screens: my queue, team queues, filters and ageing | Screens for my queue and my team's queues with filters by stage, route, status and age, sorted by service level | A team manager | Every person sees their work in one place and the lead sees the team's load | Must | 3 |
| RWB-E2-012 | Manual transfer and reassignment screen with reason | A screen to transfer a case to another queue or reassign it to a person, with a reason code required and the transfer rules checked | A team manager | A hand-off is one action with a record, not an email | Must | 3 |
| RWB-E2-015 | Timers, escalation and the deviation flag on the case record view | The case record view to show every timer with its due date, the escalation path, the prescription date and any deviation flag with its approver | A case owner | The next deadline and the reason a case left the path are visible on the case | Must | 3 |
| RWB-E2-016 | Full case record view with the history timeline | The case record view to show every action, decision, transfer, letter and document on one timeline with filters | A case owner | I read the whole case in one place | Must | 3 |


## 3.4 P4 Access and administration

| Key | Requirement | What the Workbench does | For | User benefit | Priority | Tests |
|---|---|---|---|---|---|---|
| RWB-E2-019 | Partner identities through the external gateway | Law firms, valuers and agencies to sign in to the partner portal with external identities through the external gateway, with roles per partner | A partner manager | Partners work in the Workbench from Epic 5 without SCB accounts | Should | 3 |


## 3.5 P5 Document hub

| Key | Requirement | What the Workbench does | For | User benefit | Priority | Tests |
|---|---|---|---|---|---|---|
| RWB-E2-017 | Contract, CA and mortgage document generation screens | Screens to generate the agreement, the CA and the mortgage documents from templates with the case facts, review them and send them for signature | A restructure operations officer | DIL and TDR documents are produced without re-keying | Must | 3 |
| RWB-E2-024 | Field app photos and bills into the document hub | Photos, bills and checklists captured in the field app to enter the document hub against the case, with location and time | A field collector | An inspection is on the case the same day it is made | Must | 3 |
| RWB-E2-025 | Extraction for the stage 2 and 3 document types | Field extraction extended to the stage 2 and 3 types: contracts, CA, mortgage documents, court filings, hearing notices, judgments | A document hub owner | The litigation pack and the treatment record fill themselves | Must | 3 |
| RWB-E2-026 | Document generation engine for contract, CA and mortgage templates | The generation engine that fills the contract, CA and mortgage templates from the case facts with the merge field catalog and Legal-approved versions | A restructure operations officer | The documents the screens generate are correct and versioned | Must | 3 |


## 3.6 P6 Communications

| Key | Requirement | What the Workbench does | For | User benefit | Priority | Tests |
|---|---|---|---|---|---|---|
| RWB-E2-018 | E-signature flow for customers and the bank | To sign the agreement on EasyApp or at a branch, with the bank signature added and the signed document returned to the case | A customer | A settlement completes without paper where the law allows | Must | 3 |
| RWB-E2-021 | Letter dispatch loop with proof of delivery from WIN | Every generated letter sent to WIN for print and post, with the dispatch and proof of delivery status returned to the case and the notice period timer started from delivery | A litigation officer | The notice period is counted from proof, not from printing | Must | 3 |
| RWB-E2-022 | SMS and LINE dispatch through NSS and LINE OA | Messages sent from templates through NSS and the LINE official account with delivery status on the case and the contact rules applied | A case owner | The customer is reached on the channel they use and every contact is recorded | Must | 3 |


## 3.7 P7 Decision center and log

| Key | Requirement | What the Workbench does | For | User benefit | Priority | Tests |
|---|---|---|---|---|---|---|
| RWB-E2-005 | Decision log query API for audit | A query API over the decision log by case, decision, approver, date and rule version, with the hash chain verified on every result | An internal auditor | An audit question is answered from the log in minutes | Must | 3 |
| RWB-E2-013 | Approval routing with the delegation of authority table | Every decision that needs approval routed to the role the delegation of authority table names, with a queue per approver role and escalation on timeout | An approver | The right person approves within the limit and nothing waits unseen | Must | 3 |
| RWB-E2-014 | Approval screen for D7.1 demand and recall notices | A screen that shows the generated notice, the case facts and the rule that proposed it, with approve, change or reject and a reason | A litigation officer | The first decision runs in the Workbench with a person approving | Must | 3 |


## 3.8 P8 Payments and posting

| Key | Requirement | What the Workbench does | For | User benefit | Priority | Tests |
|---|---|---|---|---|---|---|
| RWB-E2-008 | Payment matching with the missed payment event | Payments from the ALS load matched to plans each day, with a missed payment event when a due payment has not arrived | A case owner | A broken plan is known the day after it breaks | Must | 3 |
| RWB-E2-027 | Payment matching rules with the data team | The matching rules (amount, date window, reference, partial payments) held as data and run by the matching engine, with the exception list for unmatched items | A reconciliation officer | Most payments match without a person and the rest are listed | Must | 3 |


## 3.9 P9 Reporting

| Key | Requirement | What the Workbench does | For | User benefit | Priority | Tests |
|---|---|---|---|---|---|---|
| RWB-E2-009 | Steering dashboard v1 data set | A Power BI data set for the steering dashboard: cases by stage, queue and age, decisions logged, treatments, letters sent, agent acceptance | A program manager | The steering committee reads the same numbers the teams work with | Should | 3 |


## 3.10 P10 Agent runtime

| Key | Requirement | What the Workbench does | For | User benefit | Priority | Tests |
|---|---|---|---|---|---|---|
| RWB-E2-031 | Agent monitoring dashboard v2 [E3d] | The monitoring dashboard extended with acceptance, override, latency, cost per agent and per segment, and drift alerts | An AI product owner | Every agent at L1 is watched daily | Must | 3 |
| RWB-E2-032 | TDR offer-suggestion model through the model gateway [E3e] | The TDR team's offer-suggestion model exposed through the model gateway so the Workbench treatment record can carry the suggestion, if the model exists | A restructure operations officer | One gateway serves every model the Workbench uses | Could | 3 |


# 4. Program requirements met in this epic

| ID | Requirement | Priority | Owner |
|---|---|---|---|
| REQ-RDF-014 | Stage 2 data products for contracts, plans and treatments exist before the first treatment goes live. | Must | Data steward and data product owner |
| REQ-CWC-017 | A queue accepts a write from an analytical model or an agent, carrying the case, the score, the priority and the reason, so that a daily decision reaches a queue the day it is made. | Must | Product owner |
| REQ-CWC-018 | A model or agent writing to a queue passes the same permission checks as a person, runs under a service identity, and its write is logged with the model or agent version. | Must | Security administrator |
| REQ-CWC-019 | The queue write interface ships behind a feature flag and is switched on when the first model is approved to use it. | Must | Platform administrator |
| REQ-CWC-020 | A queue holds work written by a model and work allocated by rule in the same queue, ordered by the same priority, so a person works one list. | Must | Team manager |
| REQ-DCM-012 | Contracts, credit applications and mortgage documents are generated from approved templates with case data and no re-keying. | Must | Legal counsel |
| REQ-DCM-013 | Field photographs and bills reach the same intake and index as scanned documents. | Should | Autonomous Ops |
| REQ-DCM-017 | New scope. The hub answers an electronic discovery request by producing every document for a named population, with its metadata, its version history and the date each version was created. | Must | Legal counsel |
| REQ-DCM-018 | New scope. A document produced from the hub carries what a court needs to accept it: its origin, the date it entered the hub, whether it has been altered since, and who has read it. | Must | Legal counsel |
| REQ-DCM-019 | New scope. Records retention runs by class, and a document reaching the end of its retention period is disposed of or extended by a recorded decision, never silently. | Must | Compliance |
| REQ-DRI-012 | Audit can query the decision log for a population of cases and receive the decision history with inputs, versions, approver and final call. | Must | Internal audit |
| REQ-DRI-013 | Case hand-over from EFS arrives in the COLLINS daily load, and plan status is read from the ACE common module, so a case is current the morning after it changes. | Must | Data steward and data product owner |
| REQ-ACA-011 | Joiner, mover and leaver changes reach the Workbench so that access matches the current organization. | Must | Security administrator |
| REQ-ACA-012 | Partner users reach the Workbench only through the external gateway, with multi-factor authentication, scoped to their own cases. | Must | Security administrator |
| REQ-CHO-001 | A case transferred from collections reaches the Workbench on the day of transfer, with its full contact and promise history. | Must | Business lead |
| REQ-CHO-002 | A change to a restructure plan status in ACE is visible on the case through the ACE common module. | Must | Data steward and data product owner |
| REQ-CHO-003 | Customer, product and account facts reach the case from the customer profile ACE receives through COLLINS from UDP, SCBPDM and the core bank batch (DL20). | Must | Solution architect |
| REQ-CHO-004 | The hand-over point is one agreed number of days past due, used by every rule and every report. | Must | Risk with the ACE team |
| REQ-CHO-005 | The Workbench is the system of record for case state after hand-over. | Must | Solution architect |
| REQ-CHO-006 | A treatment record exists for every offer made to a customer, holding its type, terms, approval and outcome. | Must | Business lead |
| REQ-CHO-007 | Plan timers run from the treatment record, and a missed payment raises an event. | Must | Business lead |
| REQ-CHO-008 | A plan submitted for credit approval and terms booked in the core system are recorded on the case, and the booking is confirmed from the next day's ALS load. | Must | Data steward and data product owner |
| REQ-CHO-009 | Payments received are matched to the plan, the settlement or the fee they belong to, and anything unmatched goes to an exception list. | Must | Autonomous Ops |
| REQ-CHO-010 | A duplicate case for the same customer and product merges into the earlier case, carrying its documents and decision log. | Should | Case owner |
| REQ-WKM-001 | A case owner sees their own queue with ageing and service level state. | Must | Case owner |
| REQ-WKM-002 | A team manager sees every queue in their team, filters by status, product and ageing, and exports the view. | Must | Team manager |
| REQ-WKM-003 | A case is transferred or reassigned manually only with a reason code from the agreed list. | Must | Team manager |
| REQ-WKM-004 | A case that breaches its service level is visible to the named escalation role without the case moving. | Must | Team manager |
| REQ-WKM-005 | Timers, escalation state and the deviation flag are visible on the case record view. | Must | Case owner |
| REQ-WKM-006 | Queue counts, ageing and breaches are reported daily and reconcile to the case list. | Must | Team manager |
| REQ-WKM-007 | An owner who leaves, is absent beyond the threshold or breaches the caseload cap has their cases reallocated inside the team, keeping the state and the clocks. | Must | Team manager |
| REQ-WKM-008 | Queue and transfer history is visible on the case so that a reader sees where the case has been. | Must | Case owner |
| REQ-WKM-009 | A steering dashboard reports volume, ageing, route mix, turnaround and recovery against the baseline. | Must | Tribe lead |
| REQ-WKM-011 | Work allocated to a partner is visible in the same queue view as internal work. | Should | Partner and agency manager |
| REQ-WKM-012 | Every open case carries one next action: what has to happen, who owns it and the date it is due. | Must | Case owner |
| REQ-WKM-013 | The next action is produced from the rule that moved the case, taking the action, the owner of the next state and the timer that rule already carries. It is not entered by hand as a matter of course. | Must | Center of excellence |
| REQ-WKM-014 | The next action is visible to whoever picks the case up, on the case record and in every queue view, without opening the history. | Must | Case owner |
| REQ-WKM-015 | A next action that passes its due date raises the same escalation as any other service level breach, and the case does not move. | Must | Team manager |
| REQ-WKM-016 | A case with no next action is reported as an exception, because a case nobody owes anything on is the state this program exists to remove. | Must | Team manager |
| REQ-APD-001 | A decision that needs approval is routed to the approver named by the delegation of authority table for that decision, product and amount. | Must | Risk with Credit |
| REQ-APD-002 | An approver sees the recommendation, the reasons behind it, the inputs used and the limit that applies, on one screen. | Must | Business lead |
| REQ-APD-003 | An approver can accept, change, reject or return the item with a question, and each outcome is recorded. | Must | Business lead |
| REQ-APD-004 | A request above the approver's limit is refused and raised to the next approver in the matrix, with no silent approval. | Must | Risk |
| REQ-APD-005 | An override of a recommendation needs a coded reason, and the reason is reported monthly. | Must | Center of excellence |
| REQ-APD-006 | Demand and recall notices are approved through this path as the first use of approval routing. | Must | Legal counsel |
| REQ-APD-007 | An approval that is not answered inside its service level escalates to the named role. | Must | Team manager |
| REQ-APD-008 | A committee decision is recorded against the item with the members present and the decision taken. | Must | Business lead |
| REQ-APD-009 | The limit, the rule version and the approver are written to the decision log with every approval. | Must | Center of excellence |
| REQ-APD-010 | A change to the delegation of authority table is versioned, approved and dated, and open items keep the version they were decided under. | Must | Risk |
| REQ-APD-011 | Approval routing works with no person available in a role, by escalating rather than stalling. | Should | Team manager |
| REQ-DVH-001 | Deviations X1 to X7 are detected by rule from case data, call notes, documents and external flags. | Must | Center of excellence |
| REQ-DVH-002 | A deviation pauses the stage clock, keeps the prescription clock running, and does not replace the case state. | Must | Business lead |
| REQ-DVH-003 | Each deviation code routes to its named owner, and a code with no owner routes to the team manager and is recorded as unmapped. | Must | Center of excellence |
| REQ-DVH-004 | Contact stops apply automatically for a dispute or complaint, a vulnerable or hardship case, and a deceased customer. | Must | Compliance |
| REQ-DVH-005 | A resolved deviation returns the case to the state it paused in, or to the route decision where the outcome changes the route. | Must | Case owner |
| REQ-DVH-006 | A deviation flag is visible on the case record view and in every queue view. | Must | Case owner |
| REQ-DVH-007 | A complaint is matched to the contact that preceded it. | Must | Conduct and QA officer |
| REQ-DVH-009 | A bankruptcy or external seizure stops direct collection and starts the claim deadline clock. | Must | Legal counsel |
| REQ-DVH-010 | A fraud flag refers the case to the fraud team and holds recovery action until it is confirmed or cleared. | Must | Fraud |
| REQ-OCC-003 | Letters are dispatched for print and post, and proof of delivery returns to the case. | Must | Autonomous Ops |
| REQ-OCC-004 | Messages are sent by SMS and LINE through the bank's channel platforms, with the result recorded on the case. | Must | Autonomous Ops |
| REQ-OCC-005 | Every outbound contact carries a conduct check result, and a contact that fails the check is held. | Must | Conduct and QA officer |
| REQ-OCC-006 | A customer who withdraws consent for a channel stops receiving on that channel, and statutory notices continue. | Must | Compliance |
| REQ-OCC-008 | The case record view carries a history timeline showing every state change, transfer, contact, document and decision in order. | Must | Case owner |
| REQ-OCC-009 | A customer signs an agreement electronically where Legal permits it, and by wet ink where Legal requires it. | Must | Legal counsel |
| REQ-OCC-010 | A new verified contact point updates the contact data and clears a lost contact deviation. | Must | Case owner |
| REQ-ILG-009 | Contact outcomes from collections reach the ledger, so that contactability found before day 90 is not lost at hand-over. | Must | The data lead with the business lead |
| REQ-ILG-010 | Letters, messages and calls dispatched by the Workbench write their result to the ledger, including proof of delivery where it returns. | Must | Autonomous Ops |
| REQ-ILG-011 | A hand-over to or from a partner writes to the ledger, naming who held the case, who holds it now, and when. | Must | Partner and agency manager |
| REQ-ILG-012 | The case record view shows the ledger as an ordered timeline. | Must | Case owner |
| REQ-ILG-013 | Ledger entries carry their own retention class, set independently of the decision log. | Must | Compliance |


# 5. Support needed from users

The epic releases on time only if the business gives the support below during the build.

| Support | From | When |
|---|---|---|
| Sign the delegation of authority: holders, limits and substitutes by decision, amount and product | Risk with the product heads | 30 Nov |
| Use the queue and transfer screens with real cases in UAT | Case owners and team managers | UAT week |
| Approve notice approval rules and the litigation notice wording | Head of Litigation with Legal counsel | Before UAT |
| Approve SMS and LINE message content and the contact rules | Conduct and QA officer with Compliance | Before UAT |
| Name the roles that receive real users at this release | Business lead | 20 Nov |
| Attend training before go-live | Every role that receives real users | Two weeks before release |
| Test with the squads during the build and run UAT in the week before release | Business testers | Two to three hours a day, then UAT |


# 6. Acceptance

- Business testers see each requirement working during the build and confirm it against its scenarios.

- SIT runs for one week before the release, and UAT for one week, against the business scripts.

- The business lead signs the UAT exit. A requirement that fails has its feature flag switched off and the release goes ahead without it.

- The product owner accepts each story against its acceptance criteria.

# 7. Open decisions for this epic

| Decision | Question | Answer the build uses until decided | Owner | Needed by |
|---|---|---|---|---|
| DL03 | Who makes the architecture change that lets partners reach the Workbench from outside the bank, given a lead time of one to three months? | A or B, raised in November. Law firms are first needed at Epic 5, litigation, in March 2027. | Architecture lead with the architecture team | 29 Oct |
| DL09 | Who tests from the business, and when? | Business testers work with the squads two to three hours a day during the build, then a one-week UAT before each release. | Business lead with the test lead | 31 Oct |
| DL10 | What is the Thai name for each field, label and message? | The business lead drafts per module one epic ahead; Legal and Compliance approve. | Business lead with Legal and Compliance | 5 Nov |
| DL18 | Which person holds each approval level, with the limit by decision, amount and product, and the substitute for each? | Load the regulation's levels and limits now; add names and substitutes when signed. | Risk with the product heads | 30 Nov |
| DL22 | How long may a case stay in each state before it escalates? | Load the values as parameters; escalation runs from the day they are loaded. | Business lead | 13 Nov |
| DL23 | What is the most cases a person holds, and how is a queue ordered? | Load as parameters. | Product owner | 13 Nov |
| DL28 | Who owns the letter templates and the fields filled into them? | The document module owns templates and fields; Legal approves wording. | Product owner | 13 Nov |
| DL30 | Who builds SMS and LINE dispatch, EFS file automation, stage 2 and 3 extraction, and document generation? | B where a bank-wide service exists; A otherwise. | IT lead with the product owner | 13 Nov |
| DL31 | Who owns screen design for the Workbench? | The TechX designer under the product owner. using the ACE components. | Product owner | 6 Nov |
| DL39 | Which roles receive real users at each release? | Administration roles at Epic 1; business roles from the release that gives them a screen, starting with Epic 2. | Business lead | 20 Nov |

## 7.1 Effect of the realignment on these decisions

The ten decisions keep their identifiers, questions, answers and dates. Four of them meet a fact that Architecture v5 fixes; the table says which fact, without answering the decision for its owner.

| Decision | Fact the realignment fixes | Where it is recorded |
|---|---|---|
| DL03 | Partner access is delivered on the partner gateway in the DMZ, and the partner service epic RWB-SVC-S9 rwb-partner sits in wave 4. Who makes the architecture change stays open. | ADR-019; section 8.1 |
| DL18 | The delegation of authority table is held by rwb-access (P4) as versioned reference data; the levels and limits load as parameters until the holders are signed. | Ownership Map rulings (delegation_limit); REQ-APD-001 and REQ-APD-010 |
| DL30 | The realignment fixes 19 services and one epic per service, so each capability in the question sits with the service that owns it; A or B is no longer the frame. | D-RCV-60, DL44 and DL45; sections 8.1 and 9 |
| DL31 | Screen design sits on the gateway-bff composite routes of the edge, with the TechX designer under the product owner unchanged. | ADR-019; pattern DP-19; section 8.4 |

The other six decisions — DL09, DL10, DL22, DL23, DL28 and DL39 — are unaffected by the realignment.

# 8. Delivery model

Epic 2 is delivered as wave 2 of a programme of 19 service epics, 7 platform epics and 5 integration epics. Every story carries this business epic, EP02, as a tag beside its service epic, and every service epic in this section is named, numbered and waved exactly as the Ownership Map and the run's story template and rules write it. Nothing in this section changes a requirement: it says who delivers each part of the epic and in what order the contracts are published.

## 8.1 The 19 service epics

| Code | Service epic | Service | Module name | Wave (Architecture v5) |
|---|---|---|---|---|
| P1 | RWB-SVC-P1 | rwb-source-data | Source data | 1 |
| P2 | RWB-SVC-P2 | rwb-integration | Integration | 1 |
| P3 | RWB-SVC-P3 | rwb-case | Case and workflow | 1 |
| P4 | RWB-SVC-P4 | rwb-access | Access and authority | 1 |
| P5 | RWB-SVC-P5 | rwb-document | Document | 1 |
| P6 | RWB-SVC-P6 | rwb-comms | Communications | 1 |
| P7 | RWB-SVC-P7 | rwb-decision | Decision and rules | 1 |
| P8 | RWB-SVC-P8 | rwb-payment | Payment | 2 |
| P9 | RWB-SVC-P9 | rwb-reporting | Reporting | 1 |
| P10 | RWB-SVC-P10 | rwb-agent | Agent | 1 |
| S1 | RWB-SVC-S1 | rwb-valuation | Valuation and route | 3 |
| S2 | RWB-SVC-S2 | rwb-treatment | Treatment and offer | 2 |
| S3 | RWB-SVC-S3 | rwb-guarantee | Guarantee | 3 |
| S4 | RWB-SVC-S4 | rwb-litigation | Litigation | 3 |
| S5 | RWB-SVC-S5 | rwb-asset | Asset | 2 |
| S6 | RWB-SVC-S6 | rwb-debtsale | Debt sale | 3 |
| S7 | RWB-SVC-S7 | rwb-writeoff | Write-off | 4 |
| S8 | RWB-SVC-S8 | rwb-deviation | Deviation | 2 |
| S9 | RWB-SVC-S9 | rwb-partner | Partner | 4 |

One epic per service, so that each capability has its own code, release, owner, contract, schema, topic and task queue. A service owns its schema, its login, its REST base (/api/recovery/<short>/v1), its topic (rwb.<short>.events.v1) with retry and dead-letter topics, its Temporal task queue (rwb-<short>) and its Java package. The shared platform — the edge, Kafka, the Temporal layer, the database schemas and observability — is not one of the 19. The values are the service's name, base and queue as the Ownership Map writes them, and a reader who needs them reads that map.

## 8.2 Platform and integration epics

| Epic | What it delivers | Wave |
|---|---|---|
| RWB-PLT-TPL | Service template and repositories | 0 |
| RWB-PLT-LIB | Shared libraries | 0 |
| RWB-PLT-WF | Temporal workflow platform | 0 |
| RWB-PLT-DB | ACE database schemas and logins | 0 |
| RWB-PLT-EVT | Kafka event platform | 0 |
| RWB-PLT-EDGE | Edge and gateway | 0 |
| RWB-PLT-OBS | Observability | 0 |
| RWB-ITG-W1 | Integration harness for wave 1 | 1 |
| RWB-ITG-W2 | Integration harness for wave 2 | 2 |
| RWB-ITG-W3 | Integration harness for wave 3 | 3 |
| RWB-ITG-W4 | Integration harness for wave 4 | 4 |
| RWB-ITG-NFR | Non-functional integration work | 0 |

## 8.3 Waves and the business epic tags

| Business epic | Wave |
|---|---|
| EP01 | 1 |
| EP02 | 2 |
| EP03 | 2 |
| EP04 | 3 |
| EP05 | 3 |
| EP06, EP07, EP08 | 4 |
| Platform and non-functional | 0 |

Epic 2 is EP02 and therefore wave 2, releasing on 31 December 2026 (tentative). A story whose wave in this map is earlier than its service's wave in Architecture v5 keeps the earlier wave, and the difference is raised once per service and business epic in the service's own work package. In this epic the difference falls on S3 rwb-guarantee (wave 3), S4 rwb-litigation (wave 3) and S9 rwb-partner (wave 4); the trace table of section 9 shows both numbers.

## 8.4 Contract-first delivery

The build order inside every service epic follows the contract, not the screen.

- **A contract story first, on Day 1.** Every service epic starts with a contract story that publishes the operations, the events and the shapes it will answer to. A contract story has no build dependency and sits in the contract group of its wave.
- **Application stories build against the published contract and its fake.** A dependency on another service's contract never blocks a build, because the fake answers it; only a dependency inside the same service, or on a platform contract story, waits.
- **Real cross-service behaviour is integration work.** It sits only on integration stories of the wave harness, never on an application story.
- **One REST hop with a 2 s timeout.** A screen calls the edge, the edge calls one service, and the service answers from its own data or from one published contract.
- **Facts travel as events.** A published fact goes out through the outbox on the owner's topic and is consumed through the inbox, with retry and dead-letter topics.
- **Long running work is a workflow.** Steps that outlive a request run on the Temporal layer, with a child workflow per stage of a case and a schedule in place of a scheduler job.
- **Rules are embedded per service and registered centrally.** Each service evaluates the rule packages it uses, and the package registry and its versions live in rwb-decision.
- **The owner of a story is a suggestion.** Every story names a team type — TechX for contracts and application code, the ACE team for database work, SCB IT infrastructure for infrastructure, the DevOps team for operations, and the QA team for the harness and the non-functional work — and any team may pick the story up. Every team type therefore has Day-1 work in wave 2.

A story identifier reads RWB-<scope>-<legacy compact>-<work type>, with a -2 suffix on the delta copy of a preserved story. The work types are CON, APP, DB, INF, OPS and ITG.

# 9. Requirement to service epic traceability

Every requirement of section 3 is delivered by the service epic named below as primary, with the other service epics and the wave 2 integration harness taking part where the plan gives them a story. The primary service epic is the one the plan names for the requirement, and the business epic is EP02 for all 32 requirements.

| Service epic | Service | Requirements where it is primary | Requirements it also takes part in |
|---|---|---|---|
| RWB-SVC-P1 | rwb-source-data | 1 | 6 |
| RWB-SVC-P2 | rwb-integration | 10 | 0 |
| RWB-SVC-P3 | rwb-case | 5 | 13 |
| RWB-SVC-P4 | rwb-access | 1 | 19 |
| RWB-SVC-P5 | rwb-document | 4 | 2 |
| RWB-SVC-P6 | rwb-comms | 3 | 4 |
| RWB-SVC-P7 | rwb-decision | 3 | 18 |
| RWB-SVC-P8 | rwb-payment | 2 | 0 |
| RWB-SVC-P9 | rwb-reporting | 1 | 0 |
| RWB-SVC-P10 | rwb-agent | 2 | 0 |
| RWB-ITG-W2 | Integration harness for wave 2 | 0 | 30 |

| Requirement | Requirement title | Primary service epic | Other service epics and the harness | Business epic | Wave | Service wave (Architecture v5) | Stories in the plan |
|---|---|---|---|---|---|---|---|
| RWB-E2-010 | Stage 2 data products: contracts, plans and treatments | RWB-SVC-P1 | RWB-ITG-W2, RWB-SVC-S2, RWB-SVC-S3 | EP02 | 2 | 1 | Split (rework), 6 stories |
| RWB-E2-001 | EFS hand-over with full history from the COLLINS load | RWB-SVC-P2 | RWB-ITG-W2, RWB-SVC-P1, RWB-SVC-P3, RWB-SVC-P7 | EP02 | 2 | 1 | Split (rework), 7 stories |
| RWB-E2-002 | ACE plan status on the case | RWB-SVC-P2 | RWB-ITG-W2, RWB-SVC-P3, RWB-SVC-P4, RWB-SVC-P7 | EP02 | 2 | 1 | Split (rework), 7 stories |
| RWB-E2-003 | Customer's other products on the case | RWB-SVC-P2 | RWB-ITG-W2, RWB-SVC-P4 | EP02 | 2 | 1 | Split (rework), 3 stories |
| RWB-E2-006 | Credit approval pack for NLEADS | RWB-SVC-P2 | RWB-ITG-W2, RWB-SVC-P3, RWB-SVC-P7, RWB-SVC-S2 | EP02 | 2 | 1 | Split (rework), 5 stories |
| RWB-E2-007 | Booking confirmation from the ALS load | RWB-SVC-P2 | RWB-ITG-W2, RWB-SVC-P1, RWB-SVC-P3, RWB-SVC-P4, RWB-SVC-P7, RWB-SVC-S2 | EP02 | 2 | 1 | Split (rework), 9 stories |
| RWB-E2-023 | Automated EFS file load | RWB-SVC-P2 | None | EP02 | 2 | 1 | No story in the plan (GAP-1459; ASM-2565) |
| RWB-E2-033 | Case and queue list with status, owner and ageing | RWB-SVC-P2 | RWB-ITG-W2, RWB-SVC-P3, RWB-SVC-P4, RWB-SVC-S8 | EP02 | 2 | 1 | Split (rework), 6 stories |
| RWB-E2-034 | Interaction ledger on the case and from every channel | RWB-SVC-P2 | RWB-ITG-W2, RWB-SVC-P1, RWB-SVC-P3, RWB-SVC-P4, RWB-SVC-S9 | EP02 | 2 | 1 | Split (rework), 8 stories |
| RWB-E2-035 | Next action on the case | RWB-SVC-P2 | RWB-ITG-W2, RWB-SVC-P3, RWB-SVC-P4, RWB-SVC-P7 | EP02 | 2 | 1 | Split (rework), 7 stories |
| RWB-E2-036 | Queue write interface for models and agents | RWB-SVC-P2 | RWB-ITG-W2, RWB-SVC-P3, RWB-SVC-P4, RWB-SVC-P7, RWB-SVC-S8 | EP02 | 2 | 1 | Split (rework), 7 stories |
| RWB-E2-004 | Treatment entity and plan timers data model | RWB-SVC-P3 | RWB-ITG-W2, RWB-SVC-P4, RWB-SVC-P7, RWB-SVC-S2 | EP02 | 2 | 1 | Split (rework), 7 stories |
| RWB-E2-011 | Queue view screens: my queue, team queues, filters and ageing | RWB-SVC-P3 | None | EP02 | 2 | 1 | Moved (no impact), 2 stories |
| RWB-E2-012 | Manual transfer and reassignment screen with reason | RWB-SVC-P3 | RWB-ITG-W2, RWB-SVC-P7, RWB-SVC-S8 | EP02 | 2 | 1 | Split (rework), 6 stories |
| RWB-E2-015 | Timers, escalation and the deviation flag on the case record view | RWB-SVC-P3 | RWB-ITG-W2, RWB-SVC-P4, RWB-SVC-S8 | EP02 | 2 | 1 | Split (rework), 6 stories |
| RWB-E2-016 | Full case record view with the history timeline | RWB-SVC-P3 | RWB-ITG-W2, RWB-SVC-P5 | EP02 | 2 | 1 | Split (rework), 4 stories |
| RWB-E2-019 | Partner identities through the external gateway | RWB-SVC-P4 | RWB-ITG-W2, RWB-SVC-P7, RWB-SVC-S9 | EP02 | 2 | 1 | Split (rework), 6 stories |
| RWB-E2-017 | Contract, CA and mortgage document generation screens | RWB-SVC-P5 | RWB-ITG-W2, RWB-SVC-P4, RWB-SVC-P6, RWB-SVC-P7, RWB-SVC-S2 | EP02 | 2 | 1 | Split (rework), 7 stories |
| RWB-E2-024 | Field app photos and bills into the document hub | RWB-SVC-P5 | RWB-ITG-W2, RWB-SVC-P3, RWB-SVC-P4, RWB-SVC-P7 | EP02 | 2 | 1 | Split (rework), 6 stories |
| RWB-E2-025 | Extraction for the stage 2 and 3 document types | RWB-SVC-P5 | RWB-ITG-W2, RWB-SVC-P7, RWB-SVC-S2, RWB-SVC-S4 | EP02 | 2 | 1 | Split (rework), 7 stories |
| RWB-E2-026 | Document generation engine for contract, CA and mortgage templates | RWB-SVC-P5 | RWB-ITG-W2, RWB-SVC-P4, RWB-SVC-P6, RWB-SVC-P7, RWB-SVC-S2 | EP02 | 2 | 1 | Split (rework), 7 stories |
| RWB-E2-018 | E-signature flow for customers and the bank | RWB-SVC-P6 | RWB-ITG-W2, RWB-SVC-P5, RWB-SVC-S2 | EP02 | 2 | 1 | Split (rework), 5 stories |
| RWB-E2-021 | Letter dispatch loop with proof of delivery from WIN | RWB-SVC-P6 | RWB-ITG-W2, RWB-SVC-P1, RWB-SVC-P3, RWB-SVC-P4, RWB-SVC-P7 | EP02 | 2 | 1 | Split (rework), 8 stories |
| RWB-E2-022 | SMS and LINE dispatch through NSS and LINE OA | RWB-SVC-P6 | RWB-ITG-W2, RWB-SVC-P1, RWB-SVC-P4, RWB-SVC-P7 | EP02 | 2 | 1 | Split (rework), 7 stories |
| RWB-E2-005 | Decision log query API for audit | RWB-SVC-P7 | RWB-ITG-W2 | EP02 | 2 | 1 | Split (rework), 3 stories |
| RWB-E2-013 | Approval routing with the delegation of authority table | RWB-SVC-P7 | RWB-ITG-W2, RWB-SVC-P3, RWB-SVC-P4, RWB-SVC-P6 | EP02 | 2 | 1 | Split (rework), 7 stories |
| RWB-E2-014 | Approval screen for D7.1 demand and recall notices | RWB-SVC-P7 | RWB-ITG-W2, RWB-SVC-P3, RWB-SVC-P4, RWB-SVC-P6 | EP02 | 2 | 1 | Split (rework), 7 stories |
| RWB-E2-008 | Payment matching with the missed payment event | RWB-SVC-P8 | RWB-ITG-W2, RWB-SVC-P1, RWB-SVC-P4, RWB-SVC-P7, RWB-SVC-S2 | EP02 | 2 | 2 | Split (rework), 8 stories |
| RWB-E2-027 | Payment matching rules with the data team | RWB-SVC-P8 | RWB-ITG-W2, RWB-SVC-P4, RWB-SVC-P7, RWB-SVC-S2 | EP02 | 2 | 2 | Split (rework), 7 stories |
| RWB-E2-009 | Steering dashboard v1 data set | RWB-SVC-P9 | RWB-ITG-W2, RWB-SVC-P3, RWB-SVC-S8 | EP02 | 2 | 1 | Split (rework), 6 stories |
| RWB-E2-031 | Agent monitoring dashboard v2 [E3d] | RWB-SVC-P10 | RWB-ITG-W2, RWB-SVC-P4 | EP02 | 2 | 1 | Split (rework), 5 stories |
| RWB-E2-032 | TDR offer-suggestion model through the model gateway [E3e] | RWB-SVC-P10 | RWB-ITG-W2, RWB-SVC-P7, RWB-SVC-S2 | EP02 | 2 | 1 | Split (rework), 6 stories |

The plan holds 41 Epic 2 legacy keys against the 32 requirements above. The 10 keys with no requirement row here are E2-028, E2-029, E2-030, E2-037, E2-038, E2-039, E2-040, E2-041, E2-042, E2-043 (GAP-1462); they are built from another source. RWB-E2-023 is the one requirement with no story and no slice (GAP-1459; ASM-2565), and RWB-E2-011 is the one requirement the plan moves without impact on its content.

# 10. Document control and change log

## 10.1 Decisions this version adopts

Each identifier below is allocated in the run's identifier plan and recorded in the Decision Log and the architecture decision records of this run. This document adopts them; it does not approve them, and a reader who needs the decision itself reads that record.

| ID | Decision | Where it applies in this document |
|---|---|---|
| D-RCV-60 | Adopt Architecture v5 and realign the documents and the stories | Header, sections 8 to 10 |
| DL44 | Adopt Architecture v5 | Sections 8 and 9 |
| DL45 | Service epics plus business-epic tags | Sections 8.1, 8.3 and 9 |
| DL46 | Soft ownership by team type | Section 8.4 |
| DL47 | Epic 1 preservation rule | Whole document: no Epic 1 requirement is rewritten here |
| DL48 | Dates unchanged and tentative | Metadata table, section 1 |
| DL49 | Gap and assumption registers | Section 10.5 |
| ADR-013 | 19 services inside ACE; supersedes the single-service decision | Section 8.1 |
| ADR-014 | Schema and login per service in ACE PostgreSQL | Section 8.1 |
| ADR-015 | Kafka with outbox, inbox and CloudEvents | Section 8.4 |
| ADR-016 | Reusable Temporal layer; schedules replace the scheduler | Section 8.4 |
| ADR-017 | Embedded rules per service; rule registry in rwb-decision | Sections 8.4 and 9 |
| ADR-018 | No data lake; reporting read model from events | Sections 3.9 and 8.4 |
| ADR-019 | Edge: gateway-bff and partner gateway | Sections 7.1 and 8.4 |
| ADR-020 | Contract-first REST, one hop, 2 s timeout | Sections 8.4 and 9 |
| ADR-021 | Per-service migration ownership | Section 8.1 |
| ADR-022 | Local decision record plus central ledger | Sections 3.7 and 8.4 |
| ADR-023 | Observability per service | Section 8.4 |

## 10.2 Approval

The table is left empty for the people who approve this version. Until it is signed the document is Draft.

| Role | Name | Decision | Date |
|---|---|---|---|
| Product Owner |  |  |  |
| Business owner |  |  |  |
| Architecture |  |  |  |
| Security |  |  |  |
| Compliance |  |  |  |

## 10.3 Change log

| Version | Date | Change | Tool |
|---|---|---|---|
| 3 | 22 November 2026 | D-RCV-60 microservice realignment: two header lines; metadata rows for the realigned version, date, decision, status and tool; the release date marked tentative; two owner cells written as roles; section 7.1 on the effect of the realignment; section 8 Delivery model; section 9 requirement to service epic traceability; section 10 document control. No requirement, identifier, priority, count or date changes. | T3 Code / OpenCode / DeepSeek v4.1 Flash |

Version 1 is the version the metadata table names and version 2 is the file this version was read from; both values are kept as the source writes them (GAP-1461).

## 10.4 Traceability to sources

| Content | Source |
|---|---|
| Sections 1 to 7 | Recovery Workbench Business Requirements Epic 2 v2.docx, converted text |
| Header lines and the change-log row | Microservice Story Template and Rules v1, R8.1 and R8.2 |
| The 19 service epics, their names and waves | Ownership Map v1, Services sheet; Template and Rules R4 |
| Platform and integration epics | Template and Rules R5.1 |
| Wave map and the conflict rule | Template and Rules R5.6 and R5.7 |
| Contract-first order, work types and suggested owners | Template and Rules R5.2, R5.3 and R5.7 |
| Primary service epic, other service epics, story counts and dispositions | split_plan.json, legacy and slices blocks, for each RWB-E2 key |
| Delegation of authority ownership | Ownership Map rulings, delegation_limit |
| Decision, ADR and DL identifiers | ids.json; Template and Rules R8.4 |
| Personal-data classes | This version's classification of the requirements of section 3; no source states a classification |

## 10.5 Gaps and assumptions in this version

Each row is a candidate in the run's registers and is numbered with the other work packages.

| ID | Kind | Statement |
|---|---|---|
| GAP-1459 | Gap (Missing, P2) | RWB-E2-023 Automated EFS file load has no legacy story and no slice in the plan |
| GAP-1460 | Gap (Missing, P3) | Two open decisions name individuals as owners and the source states no role for either |
| GAP-1461 | Gap (Ambiguous, P3) | The document control block says Version 1 and 28 October 2026 while the source file is v2 and this version is 3 |
| GAP-1462 | Gap (Missing, P3) | Ten Epic 2 legacy keys in the plan have no requirement row in this BRD |
| GAP-1463 | Gap (Ambiguous, P3) | RWB-E2-032 is conditional on a model existing and no decision row names who confirms it |
| ASM-2560 | Assumption (High) | Epic 2 carries the business epic tag EP02 and wave 2 of the wave map. |
| ASM-2561 | Assumption (High) | The Delivery model and the requirement-to-service-epic trace table are added from the run's plan, not from the source document. |
| ASM-2562 | Assumption (High) | The module codes P1 to P10 of section 3 are read as the service epics RWB-SVC-P1 to RWB-SVC-P10, and the business names the source uses (recovery data store, document hub, case store) are kept as business names only. |
| ASM-2563 | Assumption (High) | No requirement text, identifier, priority, count or date of the source is changed. The edits are the two header lines, the added metadata rows, the tentative marking of the release date, two owner cells written as roles, and sections 7.1 and 8 to 10. |
| ASM-2564 | Assumption (Medium) | Where a service epic's Architecture v5 wave is later than wave 2 — S3 rwb-guarantee, S4 rwb-litigation and S9 rwb-partner in this epic — the plan's wave 2 governs for the Epic 2 stories, and the conflict gap is raised once per service and business epic in the service work packages, not here. |
| ASM-2565 | Assumption (Medium) | RWB-E2-023 is read as module P2 Integration from its section heading, which is the only source that places it. |
| ASM-2566 | Assumption (High) | The document is issued as Draft without human approval in this run; the approval table of section 10.2 is left empty for the approvers. |
| ASM-2567 | Assumption (Medium) | The individual names in the owner cells of DL03 and DL09 are replaced by the role that appears to hold the decision, and the replacement is recorded here rather than in the decision text. |
| ASM-2568 | Assumption (High) | The source carries no business-rule or key-performance identifiers, so none is added; the program requirement identifiers REQ-* of section 4 are the testable statements this BRD gives. |

## 10.6 Personal data in this epic

The requirements touch personal data and financial data. The classes below are this version's classification, made from the requirement text; no source document states one, and no real customer, message, account or amount appears anywhere in this document.

| Class | Where it appears | Handling the requirement already states |
|---|---|---|
| PII | Contact points and contact history, letters and their proof of delivery, messages on SMS and LINE, partner users of the partner portal (REQ-CHO-003, REQ-ILG-009, REQ-OCC-003, REQ-OCC-004, REQ-ACA-012) | Contact stops and consent withdrawal are applied on the channel and the case; partner users are scoped to their own cases through the external gateway |
| SENSITIVE_FINANCIAL | Payments and matched amounts, plan and settlement terms, treatment records, booking confirmations, hearing and judgment dates and amounts (REQ-CHO-006, REQ-CHO-008, REQ-CHO-009, REQ-DCM-012) | Amounts are matched and recorded against the plan or the treatment; the requirement names the fact and the record, never a customer's figures |

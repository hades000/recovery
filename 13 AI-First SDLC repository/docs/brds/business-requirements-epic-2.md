<!-- working-copy-of: requirement/legacy/03-requirements-and-specifications/recovery-workbench-business-requirements-epic-2-v2-docx.md -->
> **Working copy.** Canonical source: `requirement/legacy/03-requirements-and-specifications/recovery-workbench-business-requirements-epic-2-v2-docx.md`. Edit the source, not this copy.

Recovery Workbench

Business requirements, Epic 2

SCB Collections and Recovery. Henka Group, 28 October 2026

| Item | Detail |
|---|---|
| Document | Recovery Workbench business requirements, Epic 2 |
| Version | 1 |
| Date | 28 October 2026 |
| Prepared by | Henka Group |
| Release | 31 December 2026 |
| Structure | ISO/IEC/IEEE 29148, until the SCB X requirement template is adopted (DL13) |

# 1. What this epic delivers

Epic 2, Foundation 2, releases on 31 December 2026.

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
| DL03 | Who makes the architecture change that lets partners reach the Workbench from outside the bank, given a lead time of one to three months? | A or B, raised in November. Law firms are first needed at Epic 5, litigation, in March 2027. | K. Book with the architecture team | 29 Oct |
| DL09 | Who tests from the business, and when? | Business testers work with the squads two to three hours a day during the build, then a one-week UAT before each release. | K. Tee with K. Jao | 31 Oct |
| DL10 | What is the Thai name for each field, label and message? | The business lead drafts per module one epic ahead; Legal and Compliance approve. | Business lead with Legal and Compliance | 5 Nov |
| DL18 | Which person holds each approval level, with the limit by decision, amount and product, and the substitute for each? | Load the regulation's levels and limits now; add names and substitutes when signed. | Risk with the product heads | 30 Nov |
| DL22 | How long may a case stay in each state before it escalates? | Load the values as parameters; escalation runs from the day they are loaded. | Business lead | 13 Nov |
| DL23 | What is the most cases a person holds, and how is a queue ordered? | Load as parameters. | Product owner | 13 Nov |
| DL28 | Who owns the letter templates and the fields filled into them? | The document module owns templates and fields; Legal approves wording. | Product owner | 13 Nov |
| DL30 | Who builds SMS and LINE dispatch, EFS file automation, stage 2 and 3 extraction, and document generation? | B where a bank-wide service exists; A otherwise. | IT lead with the product owner | 13 Nov |
| DL31 | Who owns screen design for the Workbench? | The TechX designer under the product owner. using the ACE components. | Product owner | 6 Nov |
| DL39 | Which roles receive real users at each release? | Administration roles at Epic 1; business roles from the release that gives them a screen, starting with Epic 2. | Business lead | 20 Nov |

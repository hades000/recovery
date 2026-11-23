# Recovery Workbench Temporal and Drools Design Text Extract v1

SCB Collections and Recovery. Henka Group, 22 November 2026.
(C) Siam Commercial Bank and Henka Pte Ltd

Source: `Proposed Arch\Recovery Temporal and Drools Detailed Design v1.pptx` (read-only).

## Slide 1

Temporal + Drools: how a recovery case runs and decides

Simple first, with examples · then the technical detailed design for scenarios S1–S9 and the demo use case

Recovery Workbench · Detailed design · November 2026

Notes: Purpose: explain, simply and then in detail, how the Recovery Workbench uses Temporal (to run each case's journey) and Drools (to make each rule-based decision), across the nine recovery scenarios S1 to S9, and what the demo will show.

Architecture context comes from 'Recovery Microservice Architecture v5' (Recovery stays part of ACE; 19 services, one per module; one ACE database with a schema per service; Kafka as the event broker; one shared Temporal cluster in five layers, reusable by other workbenches; a parent CaseWorkflow with a child workflow per stage; rules governed in rwb-decision and run in the owning service; decision records written locally and sealed centrally) and the Temporal and Drools Change Register v1 (decisions T1 to T10, D-RCV-36).

## Slide 2

The idea in one picture

Two engines, one case

Temporal
runs the journey

Remembers every step

Waits days or years

Retries when things fail

Drools
makes the decisions

Business writes the rules

Approved and dated

Same facts, same answer

People
act and approve

Officers do the tasks

Approvers sign off

Partners: law firms, buyers

Decision log
proves it

Every answer recorded

Rule ID and version

Who approved, when

Recovery case
S1–S9 journey

moves it on

decides

acts on it

records

Temporal moves the case on; Drools decides each step; people approve; the log proves it.

2

Notes: Temporal is a durable workflow engine: it remembers every step of a case, waits for days or years, and retries when something fails. Drools is a rules engine: it evaluates business-written decision tables and returns one answer plus the rule ID and version. People do the work and approve within their authority. The decision log records every rule answer and approval.

Case data stays in the Recovery database; Temporal holds no case of record (T1).

## Slide 3

Think of it like a well-run project office

Same three roles you would find in any recovery team

Project manager with a diary
Temporal

Knows where each case is · chases deadlines · never forgets

The bank's policy rulebook
Drools

Written by the business · one answer · rule number cited

The case file
Recovery database

Facts of the case · every decision on record

Every scenario repeats the same loop

Ask
PM asks the rulebook: what next?

Answer
Rulebook: litigation, rule L2

Assign
Task to an officer; approver signs

Wait
Diary: remind in 7 days, chase

Record
Answer and approval on file

next step of the case

Temporal is the diary, Drools is the rulebook, the database is the file.

3

Notes: Temporal = the project manager with a perfect diary: knows where every case is, chases deadlines, never forgets after a restart.
Drools = the policy rulebook: written and signed off by the business, consulted at every decision point, always gives one answer with the rule number.
Recovery database = the case file: the facts of the case and the history of decisions.

The five-step loop is the pattern for every scenario S1 to S9.

## Slide 4

One case, start to finish

A mortgage case that ends in a settlement  ·  built from the FSD worked examples

Case created
90 days past due → ENTRY rule; active plans excluded

1

Drools

Officer assigned
ALLOC-014 → queue MTG-BKK-CO, fewest cases

2

Drools

SLA timer
Warn day 7, breach day 8 → team manager

3

Temporal

Route approved
Settlement; THB 2.4m, 20% loss → L6 signs

4

People

Payment due
Waits up to 30 days for the money

5

Temporal

Case closed
Paid, debt released, logged

6

Close

Day 0

≈ 2 months

Prescription clock runs the whole time and never pauses  ·  Temporal timer: warning 6 months before the legal deadline

Key

Drools decides

Temporal waits / reminds

A person approves

Drools makes the calls, Temporal keeps the time, people sign off, and every step is on record.

4

Notes: Built from FSD worked examples: entry (P3 AC-P3-004: account at 90 DPD becomes a case; an account with an active TDR plan is excluded under EXCL-2026.11 with reason ACTIVE_PLAN); allocation (P3 AC-P3-007: MORTGAGE in BKK matches ALLOC-014 → queue MTG-BKK-CO; the officer with the fewest cases gets it); SLA timer (P3 AC-ALT-P3-011: assigned 1 Dec, warns 8 Dec, breach 9 Dec → RW-TEAMMGR under R-UNI-30); settlement approval (P7 AC-ALT-P7-015: principal THB 2.4m at 20% loss → L6 under DOA-2026.11); settlement payment due in 30 days (R-SET-13); prescription (last payment 15 Mar 2026 → prescription 15 Mar 2028, warning 17 Sep 2027).

The prescription clock is a legal deadline and is never paused, even during a deviation (R-DEV-01).

## Slide 5

The nine recovery scenarios, S1 to S9

In every scenario Temporal runs the clock and Drools makes the calls

S1  Valuation & route

Orders appraisal, waits for approval

Re-decide if value changes

S2  Restructure, settle, deed

14-day offer, plan timers

Missed payment → cure

S3  Guarantee claims

Claim deadline timer

Missed deadline = lost claim

S4  Litigation

Notices, court dates, years

Pick law firm; auction steps

S5  Assets & auction

Holding age, 5-day payment

> THB 50m → sealed bids

S6  Debt sale

Monthly sale cycle

Award within reserve and cap

S7  Write-off

Monthly scan, posting

Open deviation → excluded

S8  Deviations X1–X7

Pause stage clock

Route to the right owner

S9  Partners

Partner SLA, chase, recall

Scorecard picks partner

Nine different journeys, one pattern: event in, rule decides, person signs, timer waits.

5

Notes: Sources: FSD S1 to S9 v3 and Business Rules and Routing Logic v4 (448 rules in 10 route sets: RES 37, SET 27, DIL 37, GUA 32, LIT 79, DIS 72, DS 41, WO 51, DEV 22, UNI 50). Only RESTRUCTURE, PAYMENT_MATCH and BOOKING_MATCH (S2) are named Drools packages in Phase 1; the other route sets become packages in Phase 2 (Epics 3 to 7). The UNIVERSAL package (R-UNI-01 to 50) arrives in Epic 3.

## Slide 6

Example: the same case, a different approver after a rule change

Settlement approval limits are versioned and take effect on a date

Settlement case
Principal THB 2.4m · loss 20%

2 Jan 2027

Rule version DOA-2026.11
approved, dated

Approver: L6
before 2 January

Logged: DOA-2026.11

Rule version DOA-2027.01
approved, dated

Approver: L5
from 2 January

Logged: DOA-2027.01

No code change, no release: the business changed a table and set a date.

Rules change on a date, by approval, and every answer shows which version made it.

6

Notes: From FSD P7 AC-ALT-P7-015: a D6.4 MORTGAGE settlement on principal THB 2,400,000 at 20% loss (THB 480,000) routes to an L6 approver (U-9201) under version DOA-2026.11. From 2 Jan 2027 version DOA-2027.01 is in force and the same case routes to L5. Raising the principal to THB 120m moves it to L5 under either version, because L6's limit is THB 100m (DoA item 2.1.1).

The version used is written into the decision log, so an auditor can always see why a case went to a given approver. Delegation limits are held as versioned reference data (delegation_limit) and follow the same approve-and-date discipline as the Drools packages.

## Slide 7

Example: litigation runs for years without anyone holding a spreadsheet

Temporal keeps the dates; Drools decides at each fork

Notice sent
WIN dispatch

Notice period
starts on proof of delivery

Law firm chosen
by rule, instructed

Court
filing, hearings, judgment

Asset trace
10 working days, writ

Auction
steps 100→90→80→70%

AUCTION LADDER  (R-LIT-63 to 67)

100%

round 1

90%

round 2

80%

round 3

70%

round 4

PRESCRIPTION CLOCK  (a legal deadline: never paused)

15 Mar 2026
last payment

17 Sep 2027
warning → review

15 Mar 2028
prescription

Temporal timer fires the warning automatically; Drools escalates when 90 days or less remain.

Key

Temporal waits

Drools decides

Court / people

A timer set today can fire in 2028, after many releases and restarts, and still be on time.

7

Notes: S4 Litigation (79 rules). Notices are generated (R-LIT-03) and dispatched via WIN (JOB-10, EV-14). Proof of delivery (EV-15) starts the notice-period timer (R-LIT-07); the proof window is 7 days. The panel firm is selected by rule and instructed (R-LIT-23/24, EV-20). Filing, hearings and judgment arrive as signals (EV-21). Enforcement: asset trace (10 working days), writ, then the LED auction ladder 100/90/80/70% (R-LIT-63 to 67). Proceeds are matched (EV-25).

Prescription: last payment 15 Mar 2026 → prescription date 15 Mar 2028, warning 17 Sep 2027 (FSD P3 AC-ALT-P3-011); 90 days or less escalates (R-LIT-11/20); R-UNI-31 forces a litigation review. A second deferral with no asset goes to write-off (R-LIT-57).

## Slide 8

Example: a customer dies, the case pauses, the legal clock does not

S8 deviation X3 (deceased) on case RW-2026-000502

Flag X3
officer or agent, same day

Pause stage clock
prescription keeps running

Route to owner
specialist + Legal

Stop contact
no letters, no calls

Resolve
resume, or re-decide route

Stage clock

Prescription clock

PAUSED

X3 raised 10 Dec

resolved: resume

escalates if not resolved in 10 working days

Temporal can pause one timer and keep another running, so legal deadlines are never missed.

8

Notes: From FSD S8 v3: case RW-2026-000502, X3 raised 10 Dec 2026, paused at state WITH_FCR_OFFICER, contact stopped. Flag: same day; the stage clock pauses while the prescription clock keeps running (R-DEV-01, EV-06). Routing to the owner by code (R-DEV-02 to 06); X3 goes to the specialist and Legal. Contact stop for X1 to X3. Resolve: resume the paused state (R-DEV-18, EV-07) or re-route to the route decision D6 (R-DEV-19). Escalation on SLA breach after 10 working days (R-DEV-20).

In Temporal terms: the deviation is a signal; the workflow pauses its stage timer (TimerScheduler.pause/resume) but not the prescription timer.

## Slide 9

Use case: a restructured mortgage misses a payment

Real example from story RWB-E2-008  ·  who decides (Drools), who waits (Temporal), who acts

9

Notes: Case RC-2026-000555, account A-0555, plan T-0701: 12,500 THB a month, 3 of 24 installments paid, next due 15 Dec 2026.
1. Plan booked: R-RES-25 starts the monthly clock (PLAN_RUNNING).
2. 16 Dec morning: AceDataReady starts payment matching in rwb-payment (JOB-07); PAYMENT_MATCH EXACT finds no payment in the 10-day window. rwb-payment publishes PaymentMissed (EV-12) to Kafka; the case router in rwb-case signals the CaseWorkflow, which passes it to TreatmentWorkflow in rwb-treatment. The case owner sees it the same morning.
3. R-RES-27 starts the cure period: 30 calendar days for MORTGAGE (CURE_PERIOD_DAYS). The Temporal timer waits through restarts and releases; a customer payment ends the wait early.
4. 15 Jan: R-RES-28 accepts a late payment (plan continues); otherwise R-RES-29 marks the plan broken and R-RES-30 sends it back to the route decision, with a case owner task due in 5 working days. On the 2nd break R-RES-31 bars a further restructure (restructure.max_breaks = 2).

Sources: RWB-E2-008, FSD S2, Epic 2 build notes. Simplification: the missed payment is found by payment matching in rwb-payment (JOB-07, after the ACE batch), not by the timer itself. Every rule answer is written as a decision record with the state change, then sealed in the central ledger in rwb-decision (v5).

## Slide 10

Technical detailed design

Runtime, workflow model, rules, then each scenario S1 to S9

10

## Slide 11

Runtime view: what runs where

Each of the 19 Recovery services has the same shape: its own Temporal worker and queue, an embedded Drools engine, its own schema

Officer / approver
Workbench screens

ONE RECOVERY SERVICE  (e.g. rwb-treatment; all 19 alike)

API
start case, approve

Temporal worker
polls rwb-treatment only

Drools engine
RuleEvaluator, model cache

Activities
EvaluateRules · RecordAndApply

Own schema
state + decision record

Outbox
→ Kafka

TEMPORAL CLUSTER  (shared, one per environment)

Frontend + history
remembers every step

own
persistence DB

Namespace rwb-recovery
one queue per service: rwb-case, rwb-treatment … (19)

ace-collection
Nexus: calculator

RULE GOVERNANCE  (rwb-decision, P7)

Rule models + central ledger
approve, publish EV-30 · seal decision records

1 click

2 poll queue

3 run step

4 ask

5 save

same transaction

Key

Temporal (runs)

Drools (decides)

People / approval

Data and log

ACE

Outside

Temporal remembers and waits; Drools answers inside a step; each service keeps its own state and decision records.

11

Notes: C4 container view, aligned to Recovery Microservice Architecture v5: Recovery stays part of ACE and is cut into 19 services, one per module (P1 to P10, S1 to S9). The slide shows one of them (for example rwb-treatment); all 19 have this shape. Each service packages its own Temporal worker and the embedded Drools runtime (KIE libraries only: drools-engine, drools-mvel, drools-decisiontables, drools-xml-support; no KIE Server, no Business Central, no KJAR - T3).

Temporal: one shared cluster per environment on ACE AKS with its own persistence database (no grant on the ACE database). Namespace rwb-recovery with one task queue per service (rwb-case, rwb-treatment, rwb-litigation and so on); each service's worker polls only its own queue and KEDA scales workers on backlog. ace-collection is ACE's namespace, reached through Nexus (for example the restructure calculator). Version 1.30+ for Nexus and Worker Versioning.

Data: the ACE PostgreSQL server, one schema and one login per service (rwb_<service>); no cross-schema joins. Temporal holds no case of record (T1). Payloads encrypted by the codec (AES-GCM, keys in Key Vault per namespace). Temporal UI behind Entra ID; RW-PLATADM operate, RW-AUDIT read, RW-SECADM decode (break-glass).

One transaction: the service writes its state change, the decision record and the outbox row together. The outbox relay publishes to Kafka (rwb.<service>.events.v1 and rwb.decision-record.v1).

Rules: rwb-decision (P7) governs rule models (author, test, four-eyes approval, effective date) and keeps the central decision ledger. The owning service loads a version on RulePackageInForce (EV-30, on Kafka), verifies the checksum, swaps atomically and keeps the last good model on failure (cache max 20).

## Slide 12

Temporal in five layers: Recovery owns the top two, the platform the rest

The bottom layers are owned once by the platform team and reused by every workbench

L5

Domain workflows
CaseWorkflow + stage children: Treatment, Litigation, Debt sale …

each service team

L4

Activity contracts per service
on rwb-<svc>: EvaluateRules, RecordAndApply, Payment.postProceeds · Nexus

each service team

L3

Workflow kit (versioned library)
Approval · Human task with SLA · Saga runner · Scheduled job · Notify · Partner instruction

platform team

L2

Namespaces
ace-collection · rwb-recovery · next workbench: own quotas, certs, keys

platform team

L1

Temporal cluster
one per environment on ACE AKS · own DB · UI · codec server · 1.30+

platform team

Recovery-specific above · shared platform, owned once, below

WHERE S1–S9 USE THE KIT

Approval (DoA)

S1 route · S2, S3, S5–S7 approvals

Human task with SLA

every officer task and escalation

Saga runner

S2 settlement · S5 auction · S6 · S7

Scheduled job

JOB-16 write-off scan · overnight jobs

Partner instruction

law firms, vendors, agencies (S4, S5, S9)

WHERE DROOLS SITS

Inside L4 activities of the owning service, never in workflow code.
Rule models are governed once in rwb-decision and copied to each owner.

Another workbench gets a namespace and the kit, and writes only its own domain workflows.

12

Notes: From Recovery Microservice Architecture v5, slide 23.
L1 cluster: one Temporal cluster per environment on ACE AKS, own persistence database, UI, metrics and codec server; upgrade to 1.30 or later for Nexus and Worker Versioning.
L2 namespaces: one per workbench (ace-collection, rwb-recovery, the next one), each with its own retention, rate limits, certificates and encryption keys.
L3 workflow kit: a versioned library of generic templates with no business terms in their interfaces: Approval (maker-checker, DoA lookup as a parameter), Notify, Document intake, Agent run with rule fallback, Human task with SLA timers, Saga runner, Scheduled job, Partner instruction.
L4 activity contracts: each service publishes typed activity interfaces on its queue rwb-<service>, plus Nexus endpoints for callers in other namespaces. EvaluateRules and RecordAndApply live here, in the service that owns the decision.
L5 domain workflows: CaseWorkflow and the stage workflows.

How S1 to S9 use the kit: Approval for route approval (S1), DoA approvals (S2, S3, S5, S6, S7) and rule sign-off; Human task with SLA for every officer task; Saga runner for settlement and deed in lieu (S2), auction (S5), debt sale (S6) and write-off posting (S7); Scheduled job for JOB-16 write-off scan (S7) and the overnight jobs; Partner instruction for law firms, auction vendors and agencies (S4, S5, S9); Agent run with rule fallback for the route agent and pricing agent (R-UNI-32).

## Slide 13

Workflow model: a parent per case, a child per stage, the same four steps for every event

CaseWorkflow on rwb-case tracks the case; each stage runs as a child workflow in the service that owns it

Any stage workflow
on its owner's queue

1  Event arrives
Kafka → case router → signal

2  EvaluateRules
Drools: package, version, rule

3  RecordAndApply
record + state + outbox, one transaction

4  Wait
durable timer or next signal

repeat

PARENT AND CHILDREN  (one queue per owning service)

CaseWorkflow · rwb-case
one per case, entry to closure

starts one child workflow per stage  ↓

Route decision
rwb-valuation  ·  S1

Treatment
rwb-treatment  ·  RES 37 · SET 27 · DIL 37

Guarantee claim
rwb-guarantee  ·  GUA 32

Litigation
rwb-litigation  ·  LIT 79

Asset disposal
rwb-asset  ·  DIS 72

Debt sale
rwb-debtsale  ·  DS 41

Write-off
rwb-writeoff  ·  WO 51

Deviation (any time)
rwb-deviation  ·  DEV 22

Continue-As-New at each stage end, at least every 28 days

The parent tracks the case; each stage runs where its rules and data live, always as receive, ask, record and apply, wait.

13

Notes: Aligned to Recovery Microservice Architecture v5 (slides 23 to 25). CaseWorkflow (workflow ID = case ID; ADR-011 writes it as case-{caseId}) runs on task queue rwb-case in namespace rwb-recovery from entry to closure. Each stage is a child workflow started on the owner's queue: RouteDecisionWorkflow (rwb-valuation, with ApprovalWorkflow from the kit on rwb-decision), TreatmentWorkflow (rwb-treatment: restructure, settlement, deed in lieu), GuaranteeClaimWorkflow (rwb-guarantee), LitigationWorkflow (rwb-litigation), AssetDisposalWorkflow (rwb-asset), DebtSaleWorkflow (rwb-debtsale), WriteOffWorkflow (rwb-writeoff), DeviationWorkflow (rwb-deviation, can start at any time and pauses the stage clock).

Each route set's rules run in the service that owns the stage; UNIVERSAL rules (R-UNI) apply in every service.

Events from other services reach the case through the case router in rwb-case (Kafka consumer, signalWithStart), never by direct calls; the parent forwards them to the running child. Inside every workflow the same four steps repeat: receive, ask Drools (EvaluateRules activity), record and apply in one transaction (RecordAndApply activity), wait.

History: Continue-As-New at every stage end and at least every 28 days keeps each run far below Temporal's limit of 51,200 events or 50 MB. Children use parent close policy ABANDON so they survive the parent's Continue-As-New. Search attributes: CaseId, Stage, ProductGroup, QueueCode.

This replaces the one-long-workflow model of Workflow Engine Design v3 / ADR-011 (route sets as states inside one workflow); ADR-011 needs updating.

## Slide 14

How the workflow asks the rules: one event, step by step

Example: a restructure customer misses a payment (EV-12) → rule R-RES-27 starts a cure period

rwb-payment

Case router

CaseWorkflow

Treatment (child)

EvaluateRules

Drools

RecordAndApply

PaymentMissed · Kafka

1

signalWithStart

2

forward to stage

3

evaluate RESTRUCTURE

4

evaluate(pkg, facts)

5

R-RES-27 · version · start cure period

6

record + state + task + outbox: one transaction

7

durable timer: wait 30 days

8

payment arrives the same way → wait ends early

9

The answer and the move are saved together, or not at all; if a worker dies, the workflow replays and reuses the answer.

14

Notes: The pattern every case event follows, aligned to Recovery Microservice Architecture v5 (slides 22, 24, 25, 27, 28):
1. rwb-payment's matchPayments activity (JOB-07, started by AceDataReady) finds no payment. In one transaction it updates schema rwb_payment and writes PaymentMissed (EV-12) to its outbox; the relay publishes it to Kafka topic rwb.payment.events.v1 (CloudEvents 1.0, key caseId).
2. The case router in rwb-case consumes it (inbox, so a duplicate never acts twice) and calls signalWithStart on the CaseWorkflow (workflow ID = case ID).
3. CaseWorkflow forwards the event to the running stage child, TreatmentWorkflow on queue rwb-treatment.
4-6. EvaluateRules runs as an activity on rwb-treatment: RuleEvaluator.evaluate(packageCode, facts, onDate) returns RuleResult(packageCode, packageVersion, ruleId, outputs). Drools is only called inside an activity, so replays reuse the recorded result.
7. RecordAndApply writes, in one transaction in schema rwb_treatment: the decision record (rule ID, version, inputs, answer; hash-linked to the previous record), the new state and task, and the outbox rows (DecisionRecorded to rwb.decision-record.v1). If it fails, nothing moves (R-UNI-39). rwb-decision collects the record into the central ledger within 5 minutes.
8. The workflow waits on a durable timer (the 30-day cure period).
9. A later payment arrives the same way and ends the wait early.

Compared with Workflow Engine Design v3: the separate WriteDecisionLog and ApplyState activities become one RecordAndApply activity, because v5 writes the record and the change in one transaction (proposed change to ADR-009). Retry policy: 1 s initial interval, back-off 2, 10 attempts; NoPackageInForce is non-retryable.

## Slide 15

Changing a rule: no software release, four-eyes, dated, one-call rollback

The business owns the rule; IT owns the engine

Author
RW-COE edits the Excel decision table

1

Compile
Table → DRL → KieBase + checksum

2

Check + test
overlap, default row, 50+ scenarios

3

Approve
RW-RISK; author can't approve

4

Go live
rwb-decision publishes EV-30 at 00:01

5

Run
owning service checks and swaps it in

6

rollback: one call

WHAT IS STORED FOR EVERY VERSION  (rule_package_version)

Workbook (Blob)

Generated DRL

SHA-256

Valid-from date

Approver

PHASE 1 PACKAGES

ENTRY

EXCLUSION

ALLOCATION

ASSIGNMENT

TRANSFER

RESTRUCTURE

PAYMENT_MATCH

BOOKING_MATCH

A rule change is data, not code: tested, approved and dated, with the version stamped on every answer.

15

Notes: T4: RW-COE writes each rule package as an Excel workbook in Drools XLS decision-table format. On upload the workbook is compiled to a KieBase, checked and run against at least 50 scenarios (rules.testcases.min=50), then stored as a rule_package_version row with the workbook, the generated DRL and a checksum. RW-RISK approves; the author cannot approve. It is in force from its valid-from date; JOB-20 (a Temporal Schedule in rwb-decision) promotes at 00:01 and publishes RulePackageInForce (EV-30) on Kafka; each owning service fetches the model (GET /rule-models/{n}/{v}), verifies the checksum and swaps it in. Rollback is one call. Version states: LOADED, APPROVED, IN_FORCE, SUPERSEDED, ROLLED_BACK, REFUSED. Load checks: compile, schema, overlap, unreachable row, default row, at least 50 scenarios, dry run.

T6: rule_row stays as the parsed, queryable catalog (action_text, owner_role, timer_spec, target_queue_code read by rule ID and version).

Where it lives (v5): governance (authoring, tests, four-eyes approval, effective dating, version audit) is central in rwb-decision (P7); evaluation is local in the one service that owns each model, inside an activity, under 300 ms. No shared rule server on the hot path.

Target (v5 deck): move from XLS tables to OMG DMN 1.6 decision models table by table; the same Drools runtime executes both.

## Slide 16

Inside a decision table: first match wins, one row decides

Each row is one rule; its name is the rule ID written to the decision record

| Rule ID | Product | Region | → Queue | → Owner role |
|---|---|---|---|---|
| ALLOC-010 | HIRE PURCHASE | any | HP-CO | RW-OFF |
| ALLOC-014 | MORTGAGE | BKK | MTG-BKK-CO | RW-OFF |
| ALLOC-015 | MORTGAGE | any | MTG-UPC-CO | RW-OFF |
| ALLOC-999 | any | any | GEN-CO | RW-OFF |


conditions

outputs

default row is always last  ·  other rows illustrative

Facts: new case
MORTGAGE · BKK

first match

ALLOC-014 fires
queue MTG-BKK-CO → officer U-03

WHAT COMES BACK  (RuleResult)

packageCode

ALLOCATION

packageVersion

ALLOC-2026.12

ruleId

ALLOC-014

outputs

queue, owner role

Decision record: ruleId + ruleVersion, hash-chained

Exactly one row decides, and its ID and version are logged, so every outcome can be explained.

16

Notes: Example from FSD P3 AC-P3-007: a MORTGAGE case in BKK matches ALLOC-014 and goes to queue MTG-BKK-CO; owner selection then picks the officer with the fewest cases (U-01/U-02/U-03 hold 120/95/140; U-02 had the last case, so U-03), skipping anyone at the cap of 150. Other rows on this slide are illustrative.

T5: first-match semantics. RuleSet = package code; each row is one rule whose NAME is the rule ID; rows share one activation-group; salience from row order; default row last. DecisionLogAgendaListener captures the rule that fired. KieBaseRegistry holds one KieBase per package version (LRU, max 20), never recompiled per call.

Version labels look like ALLOC-2026.12. Decision record (written by the owning service in its own schema, in the same transaction as the state change, then collected into the central ledger in rwb-decision): chain_seq, inputsRef, ruleId, ruleVersion, recommendation, approverUserId, approvalLevel, finalCall, actions, outcome, decidedAt, prev_hash, entry_hash (append-only, hash-chained; JOB-14 checks the chain at 02:00).

## Slide 17

S1 · Valuation and route

Choose one of eight recovery routes using the expected return of each, with a person's approval

Starts when  the case reaches route decision D6, or it is reopened (ROUTE_D6_REOPEN)

1

Order appraisal if stale

FEAT-VAL-01 · SVAF

2

Read value, flag outliers

VAL-02, VAL-03

3

Case owner accepts value

VAL-04

4

Return by route, payoff

VAL-05, VAL-06 · COLLINS, ALS

5

Route agent recommends

VAL-07 · EV-28

6

Approve: limit or committee

VAL-08, VAL-09 · EV-09

7

Start route R1–R8 + timers

VAL-12 · ROUTE_APPROVED

Runs in
rwb-valuation
RouteDecisionWorkflow

System step

Timer

Signal / event

Drools decision

Person

External system

AI agent

Drools decides

No S1 package yet (Phase 2)
Re-decide if band, value or class changes
Agent too slow (60 s) → rule decides (R-UNI-32)

Who approves

Case owner within delegated authority
Credit approval committee above it

Clocks

Appraisal stale after 12 months
Hold with a review date (VAL-10)

Point of no return / undo

ROUTE_APPROVED starts R-RES-01, R-SET-01 or R-DIL-01
Reopen needs written rule + approver (R-UNI-50)

S1 is mostly people and data; Temporal holds the case while it waits for the appraisal and the approval.

17

Notes: Source: FSD S1 Valuation and route v3; Case Journeys v3; Routing Logic v4. In v5, RouteDecisionWorkflow runs in rwb-valuation; the approval is ApprovalWorkflow from the workflow kit on rwb-decision (DoA routing); RouteDecided goes to rwb-case. Decision D6. Re-decision triggers: R-UNI-02, 14, 22, 37, 41, 45, 50 and R-DEV-19. Approval within limit or at committee (VAL-08, VAL-09, EV-09); hold with review date (VAL-10); route flow and timers start in the same step (VAL-12, REQ-S1-007); re-decide when band, value or class changes (REQ-S1-008).

Open point: route numbering conflicts between documents (R-LIT-01 starts litigation on route = R4; Case Journeys v3 calls R4 the guarantee claim and R5 litigation).

## Slide 18

S2 · Restructure, settlement and deed in lieu

Take an offer from proposal to booking, then watch the payment plan

Starts when  ROUTE_APPROVED with route R1 (restructure), R2 (settlement) or R3 (deed in lieu)

1

COLLINS proposal

R-RES-01

2

FCR officer review, 2 wd

R-RES-02, R-RES-04

3

ACE affordability check

R-RES-06

4

Offer sent, valid 14 days

R-RES-09

5

Customer signs, ops books

R-RES-16/21/22 · EV-11

6

Payment plan timers

R-RES-25

7

Missed payment → cure

EV-12 · R-RES-27

Runs in
rwb-treatment
TreatmentWorkflow

System step

Timer

Signal / event

Drools decision

Person

External system

AI agent

Drools decides

RESTRUCTURE: breaks vs max_breaks (R-RES-30/31)
PAYMENT_MATCH: EXACT, PARTIAL, WINDOW
BOOKING_MATCH: booking confirmed
Settlement below floor → approval (R-SET-05)

Who approves

DoA 2.1.1: L6 ≤ THB 100m, 30% loss
L5 ≤ 150m · L4 ≤ 300m · L3 PARC ≤ 1,500m
Deed below floor: Head of NPA (R-DIL-15)

Clocks

Offer 14 days · settlement pay 30 days
Credit approval 3 working days

Point of no return / undo

ALS/NLEADS booking; collateral release (R-SET-21)
Payment reversal reopens case (R-SET-23/24)

S2 already has three Drools packages in Phase 1; the workflow mostly waits on offers, signatures and payments.

18

Notes: Source: FSD S2 TDR, settlement and deed in lieu v3; Routing Logic v4 (R-RES 37, R-SET 27, R-DIL 37 rules). Today these take 23-26 days and are tracked by hand; 44% of TDR cases deviate (R-RES-10).

RESTRUCTURE package: R-RES-25/27/29/30/31 and R-LIT-02; a break below max_breaks returns to D6; at or above it R1 is barred (R-RES-30/31/32). PAYMENT_MATCH replaces payment_match_rule (T10). Deed in lieu auto-unlock passes about 95% of cases (R-DIL-23).

DoA 2.1.1 max loss: L6 30% / 50m; L5 35% / 75m; L4 45% / 150m; L3 PARC 45% / 750m.

## Slide 19

S3 · Guarantees and guarantors

File TCG or insurer claims before the deadline and pursue guarantors

Starts when  a guarantee is found at takeover; the claim deadline timer starts (R-GUA-01)

1

Claim deadline timer

R-GUA-01

2

Agent assembles claim

R-GUA-04

3

Officer approves, 3 wd

R-GUA-07

4

Submit to TCG

R-GUA-12

5

Query, part pay or reject

R-GUA-14/17/20

6

Paid: record subrogation

R-GUA-22/23

7

Residual back to D6

R-GUA-25

Runs in
rwb-guarantee
GuaranteeClaimWorkflow

System step

Timer

Signal / event

Drools decision

Person

External system

AI agent

Drools decides

Guarantee route set, 32 rules (package Phase 2)
Deadline missed = claim lost (R-GUA-05)
Disputed guarantee raises X1 (R-GUA-30)

Who approves

Release guarantor: L4 ≤ THB 30m, L3 ≤ 200m
Release TCG guarantee: PARC

Clocks

Claim deadline; warning → Head of Litigation
Guarantor notice runs in parallel (R-GUA-06)

Point of no return / undo

A missed claim deadline cannot be undone

S3 lives or dies on one date; a durable Temporal timer makes sure the deadline is never missed.

19

Notes: Source: FSD S3 Guarantees and guarantors v3; Routing Logic v4 (R-GUA, 32 rules). Today claims are late because deadlines are not tracked. Warning window escalates to the Head of Litigation (R-GUA-11). D6.6 guarantor notice in parallel (R-GUA-06, EV-13/14/15). Release a guarantor (2.1.5); release a TCG guarantee (2.4).

## Slide 20

S4 · Litigation and enforcement

Take a case from notice to judgment and enforcement, over months or years

Starts when  litigation route approved (R-LIT-01), or a restructure or settlement plan breaks (R-LIT-02)

1

Notices generated, sent

R-LIT-03 · JOB-10 · EV-13/14

2

Notice period on delivery

EV-15 · R-LIT-07

3

Pack checked for defects

R-LIT-16

4

Law firm chosen, instructed

R-LIT-23/24 · EV-20

5

Filing, hearings, judgment

EV-21 · R-LIT-30/33/44

6

Asset trace, writ, 10 wd

R-LIT-50

7

Auction 100/90/80/70%

R-LIT-63 to 67 · EV-25

Runs in
rwb-litigation
LitigationWorkflow

System step

Timer

Signal / event

Drools decision

Person

External system

AI agent

Drools decides

Litigation route set, 79 rules (package Phase 2)
≤ 90 days to prescription → escalate (R-LIT-11/20)
2nd deferral, no asset → write-off (R-LIT-57)

Who approves

Settlement, appeal, fees at D7.4
Delay of action: L6 ≤ THB 100m, once

Clocks

Prescription: never paused
Proof window 7 days · trace 10 wd

Point of no return / undo

Settlement holds litigation (R-LIT-37)
Broken settlement resumes it (R-LIT-40)

S4 is the longest journey: court dates arrive as signals, and the prescription timer runs for years.

20

Notes: Source: FSD S4 Litigation and enforcement v3; Routing Logic v4 (R-LIT, 79 rules). Today filing takes 21 days and packs are incomplete. Petition at D7.5 (R-LIT-58). A second delay of legal action goes one level up.

## Slide 21

S5 · Assets and auction

Take on, hold, price and sell repossessed assets (today the NPA sales cycle is 1,486 days)

Starts when  an asset is taken on from repossession, deed in lieu or LED (R-DIS-01/02/03, EV-22)

1

Holding age, provisions

R-DIS-06/09

2

Re-appraise at 12 months

R-DIS-15 · JOB-19

3

Pricing agent recommends

R-DIS-19/20

4

Floor approved, listed

R-DIS-29/33 · HOME.SCB

5

Rounds step to floor

R-DIS-38 · R-DIS-41

6

Buyer pays in 5 days

R-DIS-47

7

Title transfer, proceeds

R-DIS-51/52/54

Runs in
rwb-asset
AssetDisposalWorkflow

System step

Timer

Signal / event

Drools decision

Person

External system

AI agent

Drools decides

Disposal route set, 72 rules (package Phase 2)
> THB 50m → sealed bids at committee (R-DIS-22)
Bid below floor → second signature (R-DIS-41)
Re-list limit reached → debt sale (R-DIS-46)

Who approves

L5 ≤ THB 20m at ≥ 70% FMV
PARC ≤ 200m at ≥ 70% · MC ≤ 500m at ≥ 60%

Clocks

Payment 5 calendar days
Title transfer 10 working days

Point of no return / undo

Non-payment cancels award, reopens round
Title transfer is final (R-DIS-51/52)

S5 is a loop of timed auction rounds; Drools sets each price step, Temporal runs each round.

21

Notes: Source: FSD S5 Assets and auction v3; Routing Logic v4 (R-DIS, 72 rules). Shortfall goes to D9 or debt sale (R-DIS-54/55). Non-payment cancels the award and reopens the round (R-DIS-49/50). Sale approvals per DoA 3.2.1 (L5 max loss 3m).

## Slide 22

S6 · Debt sale

Sell lots of accounts to qualified buyers, inside the 54% cap

Starts when  the monthly sale cycle opens, or a residual arrives from disposal (R-DS-01)

1

Select accounts

R-DS-01/02

2

Lot priced, committee 5 wd

R-DS-04 · COLLINS

3

Masked tape, data room

R-DS-10/13

4

Buyer KYC, licence, 3 wd

R-DS-14

5

Award vs reserve and cap

R-DS-19/23 · EV-23

6

Settle, transfer, post GL

R-DS-25 to 31

7

Sold: close the case

R-UNI-47

Runs in
rwb-debtsale
DebtSaleWorkflow

System step

Timer

Signal / event

Drools decision

Person

External system

AI agent

Drools decides

Debt sale route set, 41 rules (package Phase 2)
Open deviation → account excluded (R-DS-02)
EV-23 stops every open action (R-UNI-47)

Who approves

Secured: PARC if ≥ 40% FMV, else ExCo
Unsecured: PARC if ≥ 10% principal, else ExCo

Clocks

Monthly cycle
Put-back review and remediation 10 wd

Point of no return / undo

Transfer and derecognition are the pivot
Upheld put-back reverses it (R-DS-36/37)

S6 spans many cases at once; one sale event closes every case in the lot through a universal rule.

22

Notes: Source: FSD S6 Debt sale v3; Routing Logic v4 (R-DS, 41 rules). Today sales run on spreadsheets. Buyer remediation 10 working days (R-DS-40). In v5 DebtSaleWorkflow in rwb-debtsale runs this as a saga with the kit's Saga runner, across five services: reserve accounts (rwb-debtsale), approve sale (rwb-decision), buyer pays (rwb-payment) can be undone; then transfer accounts, post proceeds, close cases (rwb-case), tell customers (rwb-comms) are retried until done. The transfer waits for the central ledger to confirm the decision record (strict mode).

## Slide 23

S7 · Write-off and recovery

Monthly write-off scan, committee, posting, and recovery after charge-off

Starts when  JOB-16 runs on the 3rd working day after EV-26 AceDataReady (R-WO-01)

1

Scan proposes population

R-WO-01/03

2

Pack built in 3 wd

R-WO-05

3

Committee decides

R-WO-11 to 17

4

Post to ALS / GL

R-WO-21 · EV-24

5

Release provision, feed

R-WO-25/26

6

Agency or sale after

R-WO-29/30/32

7

Retention, then close

R-WO-47 · JOB-17

Runs in
rwb-writeoff
WriteOffWorkflow

System step

Timer

Signal / event

Drools decision

Person

External system

AI agent

Drools decides

Write-off route set, 51 rules (package Phase 2)
Open deviation → case removed (R-WO-06)
Approved must equal posted (R-WO-42/43)

Who approves

Meets MR/BOT criteria: L4–L6
Else PARC ≤ THB 100m, ExCo ≤ 1,000m
Related parties: the Board

Clocks

Monthly cut-off, month-end close
Defer sets a review timer (R-WO-17)

Point of no return / undo

Posting is the point of no return
On failure: re-post, rescan or committee

S7 is batch-shaped: a schedule starts it, Drools selects the population, Temporal retries the posting.

23

Notes: Source: FSD S7 Write-off and recovery v3; Routing Logic v4 (R-WO, 51 rules). Scan holds if tax criteria are missing (R-WO-03). Recovery of written-off debt (2.1.11): L6 up to 50m and at least 15%. Posting failure: re-post, return to scan, or refer to committee (R-WO-44/45/46). In v5 JOB-16 is a Temporal Schedule in rwb-writeoff (monthly, 3rd working day); there are no shared Quartz tables. Today's Phase 1 note (T2) keeps it on Quartz, so this is listed as an open point. Write-off posting waits for the central ledger to confirm the decision record (strict mode).

## Slide 24

S8 · Deviation handling (X1–X7)

Stop the normal route for an exception, with a named owner and a clock

Starts when  an agent or officer flags it (EV-16 starts screening), or universal rules R-UNI-04 to 09 fire

1

Flag raised, same day

EV-06

2

Pause stage clock only

R-DEV-01

3

Route to owner by code

R-DEV-02 to 06

4

Stop contact (X1–X3)

contact stop

5

Owner works the case

X1 complaint … X7 collateral

6

Resume or re-route

R-DEV-18 · EV-07 · R-DEV-19

7

Escalate after 10 wd

R-DEV-20

Runs in
rwb-deviation
DeviationWorkflow

System step

Timer

Signal / event

Drools decision

Person

External system

AI agent

Drools decides

Deviation route set, 22 rules (package Phase 2)
Unmapped code → team manager (R-DEV-21)
Routes react to DEVIATION_RAISED

Who approves

X1 complaint officer · X3 specialist + Legal
X4 fraud team · X5 Legal
Person approves X6/X7 insurance claims

Clocks

Stage clock paused; prescription never
X6 skip trace 30 days

Point of no return / undo

Resume returns to the exact paused state

S8 shows the power of durable timers: pause one clock, keep the legal clock, resume exactly where it stopped.

24

Notes: Source: FSD S8 Deviation handling v3; Routing Logic v4 (R-DEV 22 rules; R-UNI-04 to 09). Route sets react via DEVIATION_RAISED (R-RES-34, R-LIT-73, R-DIS-66). Low-confidence flags get human review (FEAT-DVH-08). Data subject requests within the statutory period (R-UNI-11).

X codes: X1 dispute/complaint (complaint officer), X2 vulnerability/hardship (specialist), X3 deceased (specialist and Legal), X4 fraud (fraud team), X5 bankruptcy/seizure (Legal), X6 lost contact (agent), X7 collateral event (agent; a person approves the insurance claim).

Owner (v5): rwb-deviation runs DeviationWorkflow, which can start at any time; the case router delivers DeviationRaised (EV-06) and DeviationCleared (EV-07) to the CaseWorkflow, which pauses and resumes the stage clock. Deviation screening runs after AceDataReady.

## Slide 25

S9 · Partner management

Give work to law firms, auction vendors, agencies and valuers by measured return; pay and recall them

Starts when  a case needs a law firm, auction vendor, collection agency or valuer

1

Onboard partner, terms

FEAT-PRM-01

2

Scorecard picks partner

FEAT-PRM-03

3

Instruction sent

EV-20 · partner clock

4

Result via portal

EV-21 · same day

5

No reply: chase, recall

R-UNI-25 · R-UNI-45

6

Fees approved

FEAT-PRM-09

7

Monthly scorecard, exit

R-UNI-26

Runs in
rwb-partner
kit: Partner instruction

System step

Timer

Signal / event

Drools decision

Person

External system

AI agent

Drools decides

UNIVERSAL package (Epic 3)
Conduct breach suspends allocation (R-UNI-29)
Insolvency stops fees (R-UNI-28)

Who approves

Partner manager: overrides need a reason
Fee approval

Clocks

Partner SLA by type
Recall 5 wd · re-select 2 wd

Point of no return / undo

Exit recalls all open cases (R-UNI-26)

S9 turns partner SLAs into timers: no reply means an automatic chase, then a recall.

25

Notes: Source: FSD S9 Partner management v3; Routing Logic v4 (R-UNI-25 to 29, R-UNI-45; R-LIT-24 to 29; R-DIS-30/31; R-WO-30 to 35). Today partner work runs on email and spreadsheets. Vendor allocation 2 working days.

## Slide 26

Points of no return: undo before, retry after

Each long deal is a chain of local steps (a saga) across services, run by the kit's Saga runner

Can still be undone

Must finish: retried until done

S2 Settlement

Agree terms

Approve (DoA)

Customer pays

Book ALS / NLEADS

Release collateral

Close case

payment reversed → case reopens

S5 Auction

Approve floor

Auction round

Award, buyer pays

Transfer title

Apply proceeds

Close or shortfall

no payment in 5 days → award cancelled

S7 Write-off

Scan

Build pack

Committee approves

Post to ALS / GL

Release provision

Track recovery

deferred → review timer

Point of no return

the central ledger confirms the decision record before this step (strict mode)

Before the line a step can be undone; after it Temporal keeps retrying until the step succeeds.

26

Notes: Saga pattern orchestrated by Temporal: each step is a local transaction; before the pivot each completed step has a compensating action; after the pivot steps are retried until they succeed.

S2 settlement: payment reversal reopens the case (R-SET-23/24); booking in ALS/NLEADS and collateral release (R-SET-21) are irreversible.
S5 auction: non-payment within 5 days cancels the award and reopens the round (R-DIS-49/50); title transfer via SCIS or Land Office is final (R-DIS-51/52).
S7 write-off: posting to ALS/GL is the pivot (R-WO-21); failures are re-posted, returned to scan or referred to committee (R-WO-44/45/46).

Aligned to v5 slides 26 and 28: each step is an activity on the owning service's queue, run by the kit's Saga runner (for example DebtSaleWorkflow in rwb-debtsale, settlement and deed in lieu in rwb-treatment). Every step writes its decision record with its change in one transaction (R-UNI-39). Strict mode at the point of no return: debt transfer, write-off posting, auction sale and title transfer wait until the central ledger in rwb-decision confirms the record; everything else carries on at full speed.

## Slide 27

Two kinds of code, kept apart: that is what makes it safe to replay

Workflow code only decides the order; activity code does the real work

WORKFLOW CODE  · replayed after every restart

ACTIVITY CODE  · runs once, result recorded

Order of steps and branches

Timers: wait 30 days, wait for court date

Wait for a signal: event from the case router, task done

Start a child workflow per stage; Continue-As-New

No database, clock, random or network

No Drools calls

Ask Drools (RuleEvaluator)

Read and write the Recovery schema

Write state + decision record, one transaction

Call ACE (Nexus), partners, letters

Retried automatically with back-off

calls

Versioned changes
Worker Versioning + getVersion

Replay gate (E2-040)
every build replays real histories

Rule version pinned
each answer names its version

Encrypted payloads
no personal data in history

If a worker dies mid-case, Temporal replays the workflow and carries on from the last recorded step.

27

Notes: Temporal replays workflow code from history after any restart, so workflow code must be deterministic: no database calls, no system clock, no random, no Drools, no network. All of that goes into activities, whose results are recorded in history.

Versioning: Worker Versioning (workers pinned to a build; needs Temporal 1.30+, v5 slide 23), Workflow.getVersion(changeId, DEFAULT_VERSION, 1) for in-place code changes, and the replay gate (E2-040, MSG-P3-038) that replays recorded histories against every new build before release. Rule versions are independent: the package version is chosen at evaluation time and recorded (T7).

PDPA: search attributes are CaseId, Stage, ProductGroup, QueueCode only; payloads encrypted by PdpaPayloadCodec (AES-GCM, Key Vault); history never holds clear personal data. Retention 30 days for closed workflows, archived to Blob (E2-039).

## Slide 28

When things go wrong: nothing is lost, the case waits or retries

What happens to a running case in each failure

Worker stops

Work waits on its queue; resumes from history

A call fails (ACE, partner, DB)

Retried: 1 s, doubling, up to 10 tries

No rule version in force

Stops at once (no retry); stuck-case alert

New rule version is faulty

Refused at load; current version keeps running

Decision record write fails

Same transaction: nothing moves (R-UNI-39)

AI assistant slow

After 60 s the rule answer is used (R-UNI-32)

Kafka is down

Events wait in the outbox; none lost

Central ledger late

Work carries on; points of no return wait

Temporal keeps every running journey, each service keeps its own data, and the outbox keeps every event.

28

Notes: Worker down: tasks stay on the task queue; workers come back; the workflow resumes from history.
Call fails: activity retry policy 1 s initial interval, back-off 2, 10 attempts.
NoPackageInForce: non-retryable; the activity fails and the stuck-workflow scan (JOB-21, a visibility query every 5 minutes, platform team) raises it.
Rule version fails to load: load checks (compile, schema, overlap, unreachable row, default row, at least 50 scenarios, dry run) refuse it (state REFUSED); the version in force keeps running.
Decision record write fails: the record, the state change and the outbox row are one transaction, so nothing moves (R-UNI-39).
Kafka down: events wait in each producer's outbox and are published when it returns; consumers' inboxes drop duplicates; failed messages go to retry topics (1 min, 10 min, 1 h) then the dead-letter topic with an alert (v5 slide 22).
Central ledger late or down: services carry on and the ledger catches up from rwb.decision-record.v1; only points of no return (debt transfer, write-off, auction sale, title transfer) wait for its confirmation (strict mode, v5 slide 28).
AI agent slow: after 60 s the rule result is used (R-UNI-32).

## Slide 29

Demo: one recovery case, live

Temporal and Drools working together, shown in six scenes

29

## Slide 30

Six scenes, about 15 minutes

Each scene shows one screen and proves one point

1

Case enters

Account at 90 DPD → ENTRY rule creates case

You see
Temporal UI: workflow starts

One workflow per case

2

Rules assign

ALLOC-014 → queue MTG-BKK-CO

You see
Decision log row

Answer names its rule

3

Timer and signal

SLA timer fires; officer completes task

You see
Escalation, then signal

The case never forgets

4

Change a rule

New ALLOCATION version, tests pass, RW-RISK approves

You see
No deployment

Business owns rules

5

New vs old

Next case uses the new version; first keeps the old

You see
Both versions in the log

Fully traceable

6

Break it

Stop the worker mid-wait, restart

You see
Case carries on

Nothing is lost

The demo proves three things: the case never forgets, rules change without a release, every answer is traceable.

30

Notes: Scene 1: create a case at 90+ DPD; the CaseWorkflow (ID = case ID) starts on queue rwb-case (show Temporal UI, namespace rwb-recovery).
Scene 2: EvaluateRulesActivity calls RuleEvaluator for ALLOCATION; ALLOC-014 sends a MORTGAGE/BKK case to queue MTG-BKK-CO (FSD P3 AC-P3-007); show the decision record row with ruleId and ruleVersion, written in the same transaction as the allocation.
Scene 3: the SLA timer (shortened) fires and escalates under R-UNI-30; the officer completes the task, which arrives as a CaseEvent signal.
Scene 4: RW-COE uploads a changed ALLOCATION workbook; load checks and scenarios run; RW-RISK approves; valid-from today. No deployment.
Scene 5: a second case takes the new answer; the first case keeps its recorded answer and version.
Scene 6: stop the worker while a case waits on a timer, restart it; the workflow resumes from history. Send a deviation signal: the stage clock pauses, the legal clock does not.

Timers in the demo are shortened through parameters so a 7-day wait plays out in seconds.

## Slide 31

Demo setup: runs on a laptop with one command

Same building blocks as production, smaller

Browser
Workbench :5173

RECOVERY BACKEND  :8080

Temporal worker
CaseWorkflow · 2 activities · SLA timer

Drools RuleEvaluator
ENTRY + ALLOCATION, two versions

Rule admin + decision log
upload, approve, view answers

Spring Boot 4.1 · Temporal SDK · Drools 10.2

PLATFORM CONTAINERS

Temporal
:7233

Temporal UI
:8233

Postgres 16
ACE + temporal

Mock sign-in
:8090

Azurite blob
:10000

poll

./scripts/dev.ps1 up

  To build for the demo: CaseWorkflow, sample ENTRY + ALLOCATION packages, timer, signal

The real engines, in one backend for the demo; in v5 each stage runs in its own service. Only the timers are shortened.

31

Notes: Local stack from 18 E2E Recovery Workbench/docker-compose.yml, started with ./scripts/dev.ps1 up: Postgres 16 (ACE database and the Temporal databases), temporalio/auto-setup 1.29.7 on :7233, Temporal UI 2.58.1 on :8233 (namespace rwb-recovery), Azurite blob on :10000, mock Entra ID on :8090, backend on :8080, frontend on :5173.

Today the backend has the Temporal client (TemporalConfig), the PlatformSmokeWorkflow and embedded Drools wiring. For the demo we add: a CaseWorkflow running the two activities (EvaluateRules, RecordAndApply), the ENTRY and ALLOCATION sample packages with two versions, the SLA timer and the task-completion signal.

How the demo differs from the v5 target: the demo runs every workflow and activity in one backend on one queue and signals the workflow directly; in v5 each stage runs as a child workflow in its owning service on its own queue, events travel through Kafka and the case router, and the decision record is also sealed centrally in rwb-decision. The Temporal and Drools mechanics shown are the same. Production: official Helm chart on ACE AKS with mTLS (README), Temporal 1.30+.

## Slide 32

Open design points to settle before build

Six items, each with an owner

1

ADR-011: child workflow per stage

v5 design; ADR-011 has one workflow

Suggested owner  Recovery tech lead

2

ADR-009: record locally, seal centrally

Merges log + apply into one step

Suggested owner  RW-RISK + Internal Audit

3

Packages for S1, S3–S9

448 rules exist; codes are Phase 2

Suggested owner  RW-COE + architect

4

Route numbering R4 / R5

Documents disagree

Suggested owner  Business analyst

5

XLS tables or DMN 1.6

Same Drools runtime runs both

Suggested owner  RW-COE + RW-RISK

6

Temporal 1.30+, jobs as Schedules

Nexus, Worker Versioning; no Quartz

Suggested owner  Platform team

None of these blocks the demo; settle items 1, 2 and 3 before Epic 3 starts.

32

Notes: These follow from aligning the Temporal and Drools design to Recovery Microservice Architecture v5 (19 services).
1. ADR-011 update: v5 runs a parent CaseWorkflow with a child workflow per stage on the owning service's queue, with Continue-As-New at every stage end and at least every 28 days; ADR-011 and Workflow Engine Design v3 still describe one long CaseWorkflow with route sets as states.
2. ADR-009 change: v5 writes each decision record locally in the same transaction as the state change and seals it centrally in rwb-decision (strict mode at points of no return). This merges WriteDecisionLog and ApplyState into one RecordAndApply activity. Needs Risk and Internal Audit sign-off.
3. Drools packages for S1 and S3 to S9: the route sets exist (448 rules) but package codes are Phase 2; each needs one owning service (rwb-valuation, rwb-guarantee, rwb-litigation, rwb-asset, rwb-debtsale, rwb-writeoff, rwb-deviation).
4. Route numbering: R-LIT-01 starts litigation on route = R4; Case Journeys v3 calls R4 the guarantee claim and R5 litigation.
5. Rule format: Drools XLS decision tables today (ADR-012); v5 proposes OMG DMN 1.6, converted table by table on the same runtime.
6. Platform: Temporal 1.30+ for Nexus and Worker Versioning (local stack 1.29.7, ADR-011 1.28.1), and Quartz jobs such as JOB-16 become Temporal Schedules in the owning service (Phase 1 note T2 keeps Quartz).

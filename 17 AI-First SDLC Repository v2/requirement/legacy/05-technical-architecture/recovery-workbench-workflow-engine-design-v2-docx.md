<!-- source: 05 Technical architecture/Recovery Workbench Workflow Engine Design v2.docx -->
<!-- converted: 2026-11-16 from DOCX -->

> **Source:** `05 Technical architecture/Recovery Workbench Workflow Engine Design v2.docx`  
> **Converted from:** DOCX

Recovery Workbench

Workflow engine design

SCB Collections and Recovery. Henka Group, 28 October 2026

| Item | Detail |
|---|---|
| Document | Recovery Workbench workflow engine design |
| Version | 1 |
| Date | 28 October 2026 |
| Prepared by | Henka Group |
| Structure | CMMN 1.1, arc42 runtime view |

# 1. The design on one page

| Element | Design |
|---|---|
| Model | CMMN 1.1 case model: 10 stages, 30 milestones, 150 tasks, 53 event listeners, 448 sentries, 12 case file items |
| Runtime | Programmatic workflow in the recovery module of ACE. Case, stage and task state are rows in the ACE database; code moves them (DT09) |
| Sentries | Each sentry is one routing rule, evaluated by the rules component |
| Timers | Every due date is stored on the timer table; a Quartz job checks due timers every five minutes |
| Outbound work | Written to an outbox in the same transaction and sent with retry |
| Changes to the model | Route set versions as data; cases in flight keep the version they were decided under |

# 2. Elements

| Element | Count | How it is held |
|---|---|---|
| Case | 1 per customer per product | recovery_case |
| Stage | 10 | stage_code on the case; LOV-STAGE |
| Milestone | 30 | Reached state recorded on the case timeline |
| Task | 150 | task, with assignment and timer |
| Event listener | 53 | Rules that fire on an event in any state |
| Sentry | 448 | rule_row |
| Case file item | 12 | The data products the sentries read |

# 3. How a case moves

| Step | What happens |
|---|---|
| Event arrives | A load, a screen action, a partner result, a timer or another module |
| Rules evaluated | The rules component finds the rule for the state and the event |
| Decision logged | Rule version, inputs and approver written. A failed write stops here |
| Action taken | Next state, tasks, owner, queue, documents or notices |
| Timer set | The next due date is stored for the scheduler |
| Work queued | Work for other systems goes to an outbox with retry |

# 4. Timers

| Timer | Set by | What happens when it ends |
|---|---|---|
| Stage clock | Entry to a state, from the service level table (DL22) | Warning at the warning point; escalation at the end (R-UNI-30) |
| Prescription clock | Case entry, from the claim type | Warning forces a litigation review (R-UNI-31). Never paused by a deviation |
| Notice period | Delivery date on the proof of delivery | Pack assembly opens (R-LIT-15) |
| Offer validity | Offer sent | The offer lapses and the case returns to the owner |
| Partner service level | Instruction issued | Breach raised and re-selection (R-LIT-28) |
| Claim deadline | Default conditions met for a guarantee | Warning to the guarantee officer (R-GUA-01) |
| Holding age | Asset take-on | Provision steps and re-appraisal (R-DIS-06, R-DIS-09) |

Timers count working days from the bank holiday calendar held as reference data. A deviation pauses the stage clock; the prescription clock keeps running.

# 5. A case in flight when the model changes

- A new route set version takes effect from its valid from date.

- Cases already decided keep the version they were decided under for that decision.

- The next event on a case is evaluated against the version in force on the event date.

- A state removed from the model is mapped to its replacement in the version's migration table; cases in it are moved by a logged correction (R-UNI-24).

- A timer already running keeps its due date unless the new version says to recompute it.

- The change report lists the cases affected before the version is approved.

# 6. Concurrency and failure

| Case | Handling |
|---|---|
| Two events on one case at once | One transaction per case; the second waits on the row lock and is evaluated after |
| The same event twice | Idempotency key per event; the repeat is ignored and counted (R-UNI-40) |
| Decision log write fails | Nothing changes; incident raised (R-UNI-39) |
| Outbound system down | Outbox retry; exception queue after the limit (R-UNI-33, R-UNI-36) |
| Service restart | Quartz jobs resume; missed timers are processed on start |

# 7. Open decisions

| Decision | What is needed | Answer used until decided |
|---|---|---|
| DL16 | Entry at 90 or 91 days past due | 90 days past due |
| DL17 | What counts as one case | One case per customer per product |
| DL22 | Service level per case state | Placeholders loaded |


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


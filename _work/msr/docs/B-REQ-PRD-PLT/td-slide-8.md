
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


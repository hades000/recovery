
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


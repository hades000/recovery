
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


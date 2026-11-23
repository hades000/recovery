
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


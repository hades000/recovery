# TB0001-1228 [RWB-E1-067] Every Workbench action into the interaction ledger

| Field | Value |
|---|---|
| Jira | [TB0001-1228](https://scbjira.atlassian.net/browse/TB0001-1228) |
| Type | Story |
| Status | In Design - Solution |
| Resolution | - |
| Parent | TB0001-1162 |
| Epic link | TB0001-1162 |
| Assignee | CHANISSARA MAHAKITTIKUN |
| Reporter | KRISSADA RONGRAT |
| Priority | Medium |
| Labels | Block, DEV-Reviewed, QA-Reviewed, R-Dependency, R-Spec |
| Components | E2E Workbench |
| Fix versions | - |
| Affects versions | - |
| Sprint | Design - Grooming |
| Team | RWB_SQ1 |
| Created | 2026-11-05T12:38:01.017+0700 |
| Updated | 2026-11-18T16:59:58.088+0700 |
| Due date | - |
| Resolved | - |
| Original estimate | - |
| Remaining estimate | - |
| Time spent | - |
| Votes | 0 |
| Watchers | 4 |
| Comments | 5 |

## Description

As a case owner (RW-CASEOWN), I want every action the Workbench takes on my case written to the ledger when it is taken, so that I can read the history without assembling it from four systems.

## Acceptance criteria

```gherkin
Feature: Every Workbench action into the interaction ledger

  Background:
    Given case "RW-2026-000301" exists with no ledger entries
    Given the ledger listener runs as SY-CASEWF

  Scenario: AC1 Workbench events are captured
    Given the case is created at 2026-12-01T06:10+07:00 by SY-CASEWF
    Given allocated to queue "MTG-BKK-CO" at 06:40 by SY-RULES
    Given transferred by user "u-teammgr-03" at 2026-12-03T14:05+07:00
    Given has document "DOC-SYN-3011" attached at 2026-12-04T09:30+07:00 by SY-OCR
    Given has timer "SLA-ASSIGNED" breached at 2026-12-05T08:00+07:00
    Given has decision log entry "DLE-SYN-3012" recorded at 2026-12-05T11:20+07:00
    When each action completes
    Then the ledger holds 6 entries for the case with events CASE_CREATED, CASE_ALLOCATED, CASE_TRANSFERRED, DOCUMENT_ATTACHED, CASE_ESCALATED and DECISION_TAKEN
    Then each entry carries the case identifier, the event, the timestamp and the actor

  Scenario: AC2 The entry names its source
    Given the CASE_ALLOCATED entry of case "RW-2026-000301"
    When it is read
    Then it names source system "WORKBENCH", source reference "P3 case and workflow, EV-02 CaseAllocated" and actor "SY-RULES"
    Then the CASE_TRANSFERRED entry names actor type "USER" and actor "u-teammgr-03"

  Scenario: AC3 Nothing is written twice
    Given CaseAllocated for case "RW-2026-000301" with idempotency key "EV-02-RW-2026-000301-20261201" was written to the ledger
    When the same event arrives again with the same key
    Then one CASE_ALLOCATED entry exists
    Then the hit count for key "EV-02-RW-2026-000301-20261201" is 1

  Scenario: AC4 An event with an unknown schema version
    Given CaseTransferred is at schema version 2 and accepts version 1
    When a CaseTransferred event with schema version 3 arrives for case "RW-2026-000301"
    Then the system writes no entry
    Then the event is in the exception queue with owner RW-PLATADM and reason "schema version 3 not accepted"

  Scenario: AC5 The ledger write fails for an event
    Given every ledger insert fails
    When DocumentStored for case "RW-2026-000301" is delivered
    Then the delivery is tried 4 times in all
    Then the event is in the exception queue with owner RW-PLATADM
    Then the system raises incident "LEDGER_WRITE_FAILED" for case "RW-2026-000301"

  Scenario: AC6 Entries follow the order the events were written
    Given CaseCreated and CaseAllocated for case "RW-2026-000301" are written to the outbox in that order
    When both are processed
    Then CASE_CREATED has case_seq 1 and CASE_ALLOCATED has case_seq 2

  Scenario: AC7 The same event on two threads at once
    Given CaseCreated for case "RW-2026-000301" is delivered to two consumer threads at the same moment
    When both threads process it
    Then one CASE_CREATED entry exists
    Then the hit count for its key is 1

  Scenario: AC8 An event for a case that does not exist
    When DocumentStored arrives for case ID "00000000-0000-0000-0000-000000000998"
    Then the system writes no entry
    Then the event is in the exception queue with reason "case not found"
```

## Comments (5)

### Comment 1: RAPEEPAT CHULAOTRAKUL, 2026-11-17T00:07:48.266+0700, edited 2026-11-17T10:28:58.773+0700

Comment ID 1793595

h3. Concerns (Dependencies)

Before this story can be fully worked on/tested, the following prerequisite stories need to be completed first:

* *RWB-E1-066* — InteractionLedgerWriter interface and case sequence setup. Without it, there is no way to append entries to the ledger; this is the core capability RWB-E1-067 uses.
* *RWB-TE-006* — Outbox infrastructure with at-least-once delivery, per-case ordering, event headers (ID, idempotency key, schema version, occurred time, actor), retry logic, and exception queue. Without the outbox, there is no way to deliver events to the listener.
* *RWB-E1-018, RWB-E1-020, RWB-E1-021, RWB-E1-024, RWB-E1-027* — Event publishers for EV-01 (CaseCreated), EV-02 (CaseAllocated), EV-04 (CaseTransferred), EV-16 (DocumentStored), and EV-08 (DecisionRecorded). Without these, there are no event sources to test against for AC1–AC8.
* *RWB-E1-??? (EV-19 TimerBreached)* — The story names “EV-19 TimerBreached” in AC1 and the flow, mapping it to CASE_ESCALATED, but I cannot locate which story publishes this event. Is it included in an existing Epic 1 story, or is it missing from the project hub?

h3. Clarification Needed

# *EV-19 TimerBreached Event Source*
AC1 includes “has timer ‘SLA-ASSIGNED’ breached at 2026-12-05T08:00+07:00” → CASE_ESCALATED entry. Which story is responsible for publishing EV-19? If it’s not yet assigned or its location is unclear, what is the fallback for AC1 testing until that story is ready?
# *Source Reference Format*
AC2 test case shows: {{source reference "P3 case and workflow, EV-02 CaseAllocated"}}. The Flow step 5 says “source reference as the owning module and event ID”. Is the full format always {{<Module name>, <Event code> <Event name>}} (e.g., “P1 Recovery data engine, EV-01 CaseCreated”)? Or can it vary by event type?
# *Actor Type Field Definition*
When different types of actors perform actions, does AC2 verify that the entry records the correct actor and actor type:
#* *Service-triggered actions* (e.g., SY-RULES allocates a case automatically):
#** actor = {{SY-RULES}}
#** actor_type = {{SERVICE}}?
#* *User-triggered actions* (e.g., u-teammgr-03 transfers a case manually):
#** actor = {{u-teammgr-03}}
#** actor_type = {{USER}}?
# And the source reference always shows the owning module and event code (e.g., “P3 case and workflow, EV-02 CaseAllocated”), regardless of who triggered it?
# *Hit Count Semantics in Duplicate Handling*
AC3 and AC7 both cover duplicate events, but the semantics of {{hit_count}} are unclear:
#* When the first event arrives, is {{hit_count = 0}} (no duplicates yet) or {{hit_count = 1}} (first arrival counts)?
#* In AC3, “CaseAllocated delivered twice” → “one entry exists” and “hit count is 1”. Does this mean: original arrival = 1, second arrival = not counted (stays at 1)? Or original = 0, second arrival increments to 1?
#* What is the expected final hit_count after N duplicates for the same idempotency key?
# *Case Sequence Ordering with Concurrent Events*
AC6 covers two events written to the outbox in order → assigned case_seq 1 and 2. But what happens if:
#* Two events for the same case have the exact same {{occurred_at}} timestamp (e.g., a batch insert from EFS)?
#* Events for one case arrive out-of-order due to network delays (e.g., event 2 is delivered before event 1)?
#* Should {{case_seq}} always reflect the order they are *written to the outbox*, or the order they are *processed by the listener*?
# *Schema Version Tolerance — Current vs. Previous*
AC4 shows: “CaseTransferred accepts version 1” but “event at version 3 arrives → rejected with reason ‘schema version 3 not accepted’”. BR6 states “A consumer accepts the current and the previous schema version.”
#* Is “current” version = 2, “previous” = 1, so only 1 and 2 are accepted? (Reject 3 as shown in AC4)
#* Or is the acceptable version list configurable somewhere?
#* And which component enforces this: LedgerEventListener (before calling mapper) or somewhere else?

### Comment 2: NATAPATCHARA ANUROJE, 2026-11-17T00:54:43.313+0700

Comment ID 1793603

Some notes from drafting the spec ({{output/INC-050-epic-1-RWB-E1-067/specify/spec.md}}), on a few of the points above:

* *EV-19 TimerBreached* — couldn't find its publisher either. Not named in any Epic 1 story's "Depends on" that I checked. Still a gap.
* *Source reference format* — flow step 5 gives the pattern {{<owning module>, <event ID> <event name>}}, e.g. "P3 case and workflow, EV-02 CaseAllocated". Looks fixed per the story text, not stated as varying by event type.
* *actor_type* — not enumerated anywhere in BR2/DF-INT-015. Only split evidenced is {{USER}} (e.g. {{u-teammgr-03}}) vs. the service identities (SY-RULES etc.), which aren't given a type value either.
* *hit_count* — AC3's "hit count for key X is 1" after one repeat reads as: first arrival doesn't count, second (the actual duplicate) brings it to 1. Not stated as a formula though.
* *Preconditions* — same seven as you listed (066, TE-006, 018/020/021/024/027); same EV-19-owner gap.

Rest of your questions (case_seq under concurrent/out-of-order delivery, schema-version enforcement point, case-existence check location, test-case Excel file, event-map config ownership) are either in the spec draft or still open there too — happy to go through them if useful.

### Comment 3: NATAPATCHARA ANUROJE, 2026-11-17T10:21:23.750+0700

Comment ID 1793942

Found a real schema-level contradiction while cross-checking the physical schema (`recovery-workbench-physical-schema-v6.sql`), on top of the questions already in this thread.

*{{processed_event}} is defined twice, with different columns*

RWB-E1-007's own story text (§13) says: "V0001 (RWB-E1-001) creates {{interface_config}}, {{outbound_item}}, *{{processed_event}}*, {{outbox_event}} and {{outbox_delivery}}" — and the physical schema confirms it, already created with:
{noformat}id, consumer, idempotency_key, event_id, hit_count, last_seen_at
UNIQUE (consumer, idempotency_key)  -- reusable across multiple consumers{noformat}

But *this* story's own §13 says it creates {{processed_event}} as a *new* table in its own Flyway migration, with a different shape:
{noformat}idempotency_key (single PK), first_interaction_id, hit_count, last_hit_at{noformat}

If built as written, this story's migration would {{CREATE TABLE processed_event}} against a table that already exists — the build fails, not just a documentation mismatch.

{color:#ff5630}*Question:*{color} Should {{LedgerDuplicateService}} reuse the existing {{processed_event}} table (scoped by {{consumer}}, e.g. {{'ledger-listener'}}, using its real columns {{event_id}}/{{last_seen_at}} instead of {{first_interaction_id}}/{{last_hit_at}}), or does this story genuinely need a separate table under a different name? The story text as written can't be built as-is.

### Comment 4: Chanapai Gingpuwaluck, 2026-11-17T11:08:16.458+0700

Comment ID 1794116

These points add to the EV-19, hit_count, actor_type and processed_event questions already on this card.

# *Ledger lag is not stated.* This story writes asynchronously through the outbox, so an action is committed before its ledger entry exists. RWB-E1-066 writes in the same transaction and stops the action when the ledger fails (BR5).
#* Question: how far may the ledger lag behind the action, and how does the history read (RWB-E1-068) show an action whose entry is not written yet?
# *No replay after a fix.* After three retries an event goes to the exception queue for RW-PLATADM, but no flow or AC says how the event is replayed once the cause is fixed, or how a replay avoids a duplicate entry.
#* Proposal: an AC for "RW-PLATADM replays the event; one entry is written; hit count unchanged".
# *BR7 has no AC.* BR7 says event payloads carry references and codes, no personal data. No AC or test checks that a payload with personal data is refused.
# *Message wording.* MSG-P1-022 says "Try again in a few minutes", but no person acts on an async ledger write.
#* Proposal: a platform-facing text for the incident and the exception queue item.
# *Retry limit is assumed.* The limit of three retries (from RWB-TE-006) is still an assumption under DL11, which is past due.

Who answers: Solution architect, Henka (BA), Ops.

### Comment 5: Chanapai Gingpuwaluck, 2026-11-18T12:16:15.775+0700

Comment ID 1796385

Additional points and a dependency check for RWB-E1-067 (Jira sprints as of 18 Nov 2026; E1-067 is in "Design - Grooming").

*1. Order of case_seq (AC6) versus RWB-E1-066 AC2.* This story numbers entries in outbox write order; E1-066 AC2 expects the sequence to follow occurred time. Please use one rule in both stories (see the comment on TB0001-1227).

*2. Allocation actor after D-RCV-36 (AC1, AC2).* AC1 and AC2 show SY-RULES allocating the case. Under D-RCV-36 allocation runs through the Drools ALLOCATION package (RWB-E1-020 with RWB-E1-072). Please confirm the actor value written for a Drools decision, and note that RWB-E1-072 has no Jira ticket yet.

*3. End-to-end decision flow.* RWB-E1-066 AC3 tests a decision written to the decision log and its DECISION_TAKEN ledger entry. That entry is written by this story from EV-08, so the end-to-end check belongs here. E1-066 AC3 also uses rule R-UNI-18 (reallocation), which is Epic 2. Proposal: move the end-to-end AC to E1-067, using an Epic 1 decision (OWNER_ASSIGNED or CASE_TRANSFERRED).

*4. Schema version check (AC4, BR6, flow step 3).* The rule is "accept the current and the previous version", but no document says what the current version of each event is. Event and Messaging Design v3 declares schemaVersion as an integer only, and AC4 assumes CaseTransferred is at v2 without saying what v2 is.

* Where does LedgerEventListener read the current version: code, the event map rwb.dataengine.ledger.event-map, or a central registry? Proposal: a version table in Event and Messaging Design (event, current, previous accepted), all Epic 1 events at v1, read from configuration.
* The version is carried twice: in the outbox header (RWB-TE-006) and in the payload (AsyncAPI). Which one is checked, and must they match?
* Deployment rule: when a publisher moves an event to a new version, consumers must accept it first; otherwise every event goes to the exception queue. Please state this.
* With all events at v1, AC4 should read "current v1; an event at v2 is refused".

*5. Dependencies – none is ready in Q4S2:*

* Declared: RWB-E1-066 (ledger writer): Design - Grooming.
* RWB-TE-006 (outbox, retry, exception queue) is used by AC3 to AC7 but is not in "Depends on" – please add. No sprint.
* Event publishers, all with no sprint: RWB-E1-018 (EV-01), RWB-E1-020 (EV-02), RWB-E1-021 (EV-04), RWB-E1-027 (EV-08). RWB-E1-024 (EV-16) is in Design - Pre-analyze.
* EV-19 TimerBreached: no publisher named (probably RWB-E1-028, no sprint).
* SY-CASEWF service identity with Case record C (AC5, TC-E1-067-09): needs RWB-E1-019 / E1-037, no sprint.

*Decision needed:* build E1-067 against the outbox test fixture and stub events for Q4S2, with end-to-end tests once the publishers land? Or pull TE-006 and the publishers into the sprint?


## Other Jira fields

| Field | ID | Value |
|---|---|---|
| App Owner | customfield_10188 | - |
| App Owner (migrated 3) | customfield_11031 | - |
| Approver2 | customfield_11586 | Nuttakorn Leeviravanich |
| AR: Atlassian-TemplateO | customfield_11656 | emaile,role |
| AR: Atlassian_Template | customfield_11654 | \|\|Full Name \|\| Email \|\| Role \|\| Company \|\| \|{Full Name}\|{Email}\|{Role}\|{Company}\| \|\|\|\| |
| BI Status | customfield_10169 | To be Confirmed |
| Build % | customfield_12531 | 0% |
| Bulk Backlog Detail Uploaded | customfield_11628 | No |
| CCB Status | customfield_10228 | New |
| Created Date | customfield_10249 | 2026-11-05 |
| Customer Impact | customfield_10246 | No |
| CX Status | customfield_10217 | To be Confirmed |
| Defect Re-Opened? | customfield_10619 | No |
| Defect Re-Opened? (Checkbox) | customfield_10174 | No |
| Demand type | customfield_10244 | Project |
| Demand types(Migrated on 29 Mar 2024) | customfield_11926 | Incident |
| Deploy Status | customfield_10170 | Initial |
| DGO Approval | customfield_10113 | Pending |
| DPO Approval | customfield_10122 | Pending |
| Epic Type | customfield_10275 | Project |
| Epic Type OLD | customfield_10052 | Project |
| Execution Method | customfield_10240 | Manual |
| Grooming Status | customfield_10212 | Not Started |
| Grooming Status (migrated) | customfield_10649 | Not Started |
| Has been Approved | customfield_10232 | No |
| Independent Story | customfield_10101 | No |
| Is Required Downtime | customfield_10245 | N |
| Is Required Downtime | customfield_11847 | N |
| Issue Priority | customfield_10102 | Medium |
| IT Risk Approval | customfield_10133 | Pending |
| Logs / Description | customfield_11491 | Log: xxxx URL: xxxx |
| Penetration Test Status | customfield_10183 | Not Started |
| Penetration Test Status (migrated) | customfield_10654 | Not Started |
| Priority | customfield_10610 | Medium |
| QbD Status OLD | customfield_10050 | Not Required |
| Regulatory Related | customfield_10260 | No |
| Regulatory Status | customfield_10201 | No Issues |
| Regulatory Status (migrated) | customfield_10647 | No Issues |
| Release Confirmation | customfield_10637 | Not Confirmed Internal |
| Release Confirmation (API) | customfield_10200 | Not Confirmed Internal |
| Requirement Status | customfield_10207 | Not Completed |
| Root Cause | customfield_12535 | Unknown |
| SAT Process | customfield_10274 | PENDING |
| SAT Status(Migrated) | customfield_12360 | Not Start |
| SD Required | customfield_10257 | no |
| Segment | customfield_10193 | Retail |
| Severity | customfield_10168 | 3 - Medium |
| Severity (migrated) | customfield_10597 | 3 - Medium |
| SIT retest failure tracking | customfield_15014 | 0.0 |
| SIT Shakedown Status | customfield_10189 | Not Started |
| Solution Remark (Nonstd) | customfield_10216 | To be Confirmed |
| Solution Status | customfield_10640 | To be Confirmed |
| Squad Estimation Status | customfield_10229 | Estimation In Progress |
| Target Fix Date Adjustment Flag | customfield_15017 | No |
| Test Cases Review | customfield_10150 | In-progress |
| Testing environment | customfield_15163 | Non-Aging |
| Toggle Flag | customfield_11588 | No Toggle Flag |
| Training Material Status | customfield_10176 | Not Started |
| UAT Estimation Status | customfield_10234 | Estimation In Progress |
| UAT Execution By | customfield_13554 | UAT Team |
| UAT Execution By | customfield_10237 | Squad Team |
| UAT Owner | customfield_10184 | KANRUTHAI ASAVAROONGPAISAL |
| UAT retest failure tracking | customfield_15015 | 0.0 |
| UAT Shakedown Status | customfield_10194 | Not Started |

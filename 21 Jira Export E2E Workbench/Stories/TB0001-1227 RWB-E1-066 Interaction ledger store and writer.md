# TB0001-1227 [RWB-E1-066] Interaction ledger store and writer

| Field | Value |
|---|---|
| Jira | [TB0001-1227](https://scbjira.atlassian.net/browse/TB0001-1227) |
| Type | Story |
| Status | In Design - Solution |
| Resolution | - |
| Parent | TB0001-1162 |
| Epic link | TB0001-1162 |
| Assignee | CHANISSARA MAHAKITTIKUN |
| Reporter | KRISSADA RONGRAT |
| Priority | Medium |
| Labels | DEV-Reviewed, QA-Reviewed, R-Dependency |
| Components | E2E Workbench |
| Fix versions | - |
| Affects versions | - |
| Sprint | Design - Grooming |
| Team | RWB_SQ1 |
| Created | 2026-11-05T12:38:00.053+0700 |
| Updated | 2026-11-18T20:25:00.560+0700 |
| Due date | - |
| Resolved | - |
| Original estimate | - |
| Remaining estimate | - |
| Time spent | - |
| Votes | 0 |
| Watchers | 5 |
| Comments | 12 |

## Description

As a case owner (RW-CASEOWN), I want every contact, letter, promise, payment and hand-over on the case written to one ledger when it is recorded, so that the history of the case is never assembled after the fact.

## Acceptance criteria

```gherkin
Feature: Interaction ledger store and writer

  Background:
    Given case "RW-2026-000201" exists with 6 ledger entries, case_seq 1 to 6
    Given user "u-owner-02" holds RW-CASEOWN and owns case "RW-2026-000201"

  Scenario: AC1 The ledger exists and is written to
    Given the case owner records an outbound call on 2026-12-02 at 10:15 with result RIGHT_PARTY and a promise of 25,000.00 baht for 2026-12-15
    When the action completes
    Then the ledger holds entry case_seq 7 for case "RW-2026-000201" with event "CONTACT", occurred at 2026-12-02T10:15+07:00, actor "u-owner-02", channel "CALL" and direction "OUTBOUND"
    Then the entry carries promise amount 25,000.00 and promise date 2026-12-15
    Then the entry names source system "WORKBENCH"

  Scenario: AC2 It is ordered and complete
    Given case "RW-2026-000201" has 4 EFS history entries from 2026-08-03 to 2026-11-28, a CASE_CREATED entry on 2026-12-01 and a CASE_ALLOCATED entry on 2026-12-01
    When the ledger is read
    Then the 6 entries are in one sequence ordered by occurred time
    Then case_seq runs 1 to 6 with no gap

  Scenario: AC3 It is distinct from the decision log
    Given owner reassignment of case "RW-2026-000201" was decided under rule "R-UNI-18" version "2026.11" by approver "u-teammgr-01"
    When both are read
    Then the decision log entry holds decision code "D6", rule "R-UNI-18", version "2026.11", the inputs reference and the approver
    Then the ledger entry holds event "DECISION_TAKEN", the time, the actor and the decision log entry ID, with no rule, version or inputs

  Scenario: AC4 A write failure is visible
    Given the ledger insert fails with a database error
    When the case owner records a call on case "RW-2026-000201"
    Then the system refuses the call with status 503 and MSG-P1-022
    Then the ledger still holds 6 entries and no contact is saved
    Then the system raises an incident "LEDGER_WRITE_FAILED" with case "RW-2026-000201"

  Scenario: AC5 A required value is missing
    When a service calls append() for case "RW-2026-000201" with no event code
    Then the system refuses the call with MSG-GEN-001 for field "event code"
    Then the system writes no entry

  Scenario: AC6 Two entries for one case at the same moment
    Given two transactions append to case "RW-2026-000201" at the same moment
    When both commit
    Then the entries carry case_seq 7 and 8
    Then no case_seq is missing or repeated

  Scenario: AC7 A case that does not exist
    When the case owner posts an interaction for case ID "00000000-0000-0000-0000-000000000999"
    Then the system refuses the call with status 404 and MSG-P4-003
    Then the system writes no entry

  Scenario: AC8 An entry cannot be changed
    Given ledger entry case_seq 3 of case "RW-2026-000201"
    When any process issues an UPDATE or DELETE on it
    Then the database refuses the statement
    Then the system writes a correction as a new entry with event "CORRECTION" naming entry case_seq 3
```

## Comments (12)

### Comment 1: Chayaporn Kaewin, 2026-11-16T23:24:53.486+0700

Comment ID 1793572

Technical Specifier ran for this story (RUN_ID {{INC-044-epic-1-RWB-E1-066}}). Draft spec is complete but *blocked* on one contract gap — already tracked as an open defect (Story Defects v4), not newly invented here.

h3. CLAR-001 — InteractionRequest is missing promiseAmount/promiseDate

Story flow step 1 and AC1 post a call result that includes a promise amount and date in the same {{POST /cases/{caseId}/interactions}} call. But {{InteractionRequest}} in API Specification v4 only has {{channel}}, {{direction}}, {{result}}, {{summary}} — no promise fields. The response schema {{Interaction}} already has them, so only the request side is short.

Options:
# Add {{promiseAmount}}/{{promiseDate}} to {{InteractionRequest}} (additive, no version bump) — matches AC1 as written. *Recommended.*
# Split into two calls — POST creates the interaction without the promise; a separate call attaches it later (likely a different story); AC1/flow text would need rewriting.

Logged as {{OPEN-038}} in {{docs/open-items.md}}, owner Product Owner / solution architect.

Also flagged (non-blocking, informational): both named preconditions — RWB-E1-018 and RWB-E1-027 — are still Backlog/not started, so build scheduling for this story needs them done or stubbed first.

Spec draft: {{output/INC-044-epic-1-RWB-E1-066/specify/spec.md}}. Compliance review is held until CLAR-001 is answered.

### Comment 2: Chayaporn Kaewin, 2026-11-17T00:04:29.169+0700

Comment ID 1793594

h2. New gaps / ambiguities found

# *Request→Command mapping missing.* API request ({{channel, direction, result, summary}}) has no stated rule for deriving {{eventCode}}, {{occurredAt}}, {{actorType/Ref}}, {{partyId}} for the {{LedgerEntryCommand}}. Needed to actually implement AC1.
# *partyId / actionCode / contactResult uncovered.* Spec's field-level behaviour matrix omits these three command fields — no nullability, no constraint, no source stated.
# *Invalid (vs missing) event code — no message defined.* Validation checks event code is in LOV-LEDGER-EVENT, but §14 messages only cover "missing required value" (MSG-GEN-001). No message for "value present but not in list."
# *Feature-flag rollback claim vs NOT NULL migration.* Migration makes {{event_code, actor_type, actor_ref, source_ref, case_seq}} NOT NULL (not nullable). Flag-off rollback is described as "safe / nullable columns harmless" — contradicts if any prior direct-insert path exists. Needs clarify: does flag-off mean zero interaction rows written (history gap), or was there never a prior path?
# *AC8 trigger semantics ambiguous.* Gherkin reads as one cause-effect (UPDATE/DELETE attempt → auto-writes CORRECTION entry), but solution plan never designs an auto-insert trigger. Likely two independent facts (refusal is automatic; correction is a separate deliberate {{append()}} call) — as written, implementers could build it wrong.
# *No referential check on decision_log_id / corrects_entry_id.* Nothing validates the referenced entry belongs to the same case or exists before insert.
# *Retry-once-on-clash has no failure path.* What happens if retry on (case_id, case_seq) clash also clashes (3+ concurrent writers)? Not covered by AC6 or any exception path.
# *No idempotency strategy for load paths.* Idempotency key is only built from a request-ID header on the P3 path (header name unspecified). EFS history load / ALS payment load / notice dispatch have no stated dedup strategy for their own retries.
# *Advisory lock key derivation unstated.* {{pg_advisory_xact_lock}} takes bigint; case ID is UUID. No hash/cast method stated — collision risk across unrelated cases not addressed.
# *"Depends on" header incomplete.* Story header row lists only RWB-E1-018/027; preconditions and spec's "Inherited Existing Behavior" also require RWB-E1-001 (interaction table + trigger) and RWB-E1-043 (reference-data loader). Traceability row should list all four.
# *RWB-E1-004 (EFS extract load) cancellation leaves EFS→ledger wiring ownerless.* No hard dependency break (not in RWB-E1-066's "Depends on"), but story §4 step 7 names "EFS history load" as one of 3 {{append()}} callers — cancel it and no EFS-sourced CONTACT entries (pre-90-day collections history) ever reach the ledger. Worse: RWB-E1-004 §19 Out-of-scope already pushes "copying history into interaction ledger" to RWB-E1-018/066, while compliance finding REVIEW-RWB-E1-066-002 names RWB-E1-004 as the story to confirm that same caller — a pre-existing ownership contradiction that cancellation makes unresolvable as-is. AC2 test stays passable (seeds ledger rows directly, not via RWB-E1-004's pipeline). Business risk: the card's value prop ("history never assembled after the fact") weakens for accounts <90 days past due. Needs: re-disposition REVIEW-002 in compliance-validation.md; Solution architect to confirm whether EFS→ledger wiring is dropped entirely or reassigned.

### Comment 3: RAPEEPAT CHULAOTRAKUL, 2026-11-17T10:01:02.335+0700

Comment ID 1793851

h3. Concerns (Dependencies)

Before this story can be fully worked on/tested, the following prerequisite stories need to be completed first:

* *RWB-E1-018* — CaseDirectory and case record (recovery_case table) with case numbers RW-YYYY-NNNNNN format. Without it, case validation and scope checks are not possible.
* *RWB-E1-027* — DecisionLogWriter interface and incident path (IncidentRecorder.raise) with LEDGER_WRITE_FAILED handling. Without it, the failure path (X1, BR5, AC4) cannot be tested; write failures cannot be escalated as incidents.

### Comment 4: Chanapai Gingpuwaluck, 2026-11-17T11:03:40.018+0700, edited 2026-11-17T11:03:51.367+0700

Comment ID 1794091

These points add to CLAR-001 and the spec gaps already on this card.

# *Synchronous or asynchronous writes.* This story writes the ledger synchronously, in the same transaction as the action. RWB-E1-067 writes asynchronously through the outbox. With both paths, {{case_seq}} may not follow event time.
#* Question: which path owns {{case_seq}} order, and does a reader see the sync entry before the async one?
# *Ledger failure stops all officer actions.* Under BR5, every officer action stops when the ledger cannot be written.
#* Proposal: an NFR for this, an alert, and a run book entry in RWB-E1-056.
# *No correction flow.* The story does not say who corrects an entry, through which endpoint, or with which right.
# *Retired role.* The precondition still names SY-DATALOAD, which D-RCV-35 removed (feedback #79).

Who answers: Solution architect, Henka (BA), Ops.

### Comment 5: Chanapai Gingpuwaluck, 2026-11-18T11:40:01.547+0700

Comment ID 1796288

Two AC points and a dependency check for RWB-E1-066 (Jira sprints as of 18 Nov 2026; E1-066 is in "Design - Grooming").

*1. case_seq versus time order (AC2, BR7).* case_seq is assigned when an entry is written, but AC2 expects the sequence to follow occurred time. If older entries are written after newer ones (for example history from 2026-08 written after CASE_CREATED on 2026-12-01, or an async entry from RWB-E1-067 committed after a sync one), case_seq and time order no longer match.

* Which order is authoritative for the history: case_seq (write order) or occurred_at?
* Should AC2 say "case_seq runs 1 to n with no gap in write order", and the read order be "occurred_at, then case_seq" as in RWB-E1-068?
* AC2's 4 EFS entries have no writer in Epic 1 (RWB-E1-004 removed, EFS to ledger is RWB-E2-034). Please replace them with Workbench entries.

*2. 403 or 404 for a case outside scope (AC7, X4).* This story and RWB-E1-068 return 404 with MSG-P4-003; RWB-E1-024 returns 403 with the same message for the same case. Please choose one for the module and align the three stories. AC7 also covers only a case that does not exist; please add a case that exists but is outside the caller's scope.

*3. Dependencies – none is ready in Q4S2:*

* Declared: RWB-E1-018 (recovery_case) and RWB-E1-027 (decision log writer and incident path): no sprint.
* RWB-E1-001 (interaction table and append-only trigger): Delivery Q4S2 Squad1, waiting on RWB-E1-043 (Hold). Not in "Depends on" – please add.
* LOV-LEDGER-EVENT is loaded through the reference data service, RWB-E1-043: Q4S2 Squad2, Hold. Please add.
* Case record C and scope (POST /interactions, AC7): RWB-E1-019 / E1-022 / E1-037 / E1-016, no sprint.
* Run book and alert for LEDGER_WRITE_FAILED (BR5): RWB-E1-056, Design - Grooming.

*Decision needed:* pull E1-018 and E1-027 into Q4S2, or build against stubs and move AC3, AC4 and AC7 to a later integration test?

### Comment 6: VAISHNAVI KAULGE, 2026-11-18T15:35:23.337+0700

Comment ID 1796972

@Chayaporn Kaewin 

*Recommendation: Option 1.* Add {{promiseAmount}} (number, baht) and {{promiseDate}} (date) to {{InteractionRequest}} in API Specification v4. The change is additive, so no version bump is needed.

*Reason*

* Flow step 1 and AC1 send the call result and the promise in the same {{POST /cases/{caseId}/interactions}} call.
* BR3 / REQ-ILG-004 requires a promise to be recorded on the interaction it was made in.
* The response schema {{Interaction}} already has {{promiseAmount}} and {{promiseDate}}. Only the request side is missing them, so the request fields should use the same names and types.

*Suggested rule for the new fields:* make both optional, so calls with no promise (for example NO_ANSWER or WRONG_NUMBER) stay valid. The Product Owner can confirm whether a promise requires both fields together.

*Option 2 (split into two calls) is not recommended.*

* The contact and its promise would no longer be saved in one transaction.
* AC1 and the flow text would need rewriting.
* The second call would likely belong to a different story.

*Preconditions (RWB-E1-018 and RWB-E1-027):* Noted. Both must be done or stubbed before the build of E1-066 starts. The implementation order in Project Hub v17 already places both ahead of E1-066 (E1-027 is 20th, E1-018 is 38th, E1-066 is 44th).

*Also noted (non-blocking), for the spec draft:*

* In API Specification v4, {{eventCode}} lists PARTNER_RESULT and OFFER, which are not in the story's LOV-LEDGER-EVENT.
* {{caseSeq}} is typed as a string in the spec, but the story treats it as a number.

### Comment 7: VAISHNAVI KAULGE, 2026-11-18T15:44:01.969+0700

Comment ID 1797015

@Chayaporn Kaewin 


# *The API request doesn't say how to fill the ledger entry* (For discussion)

_Gap:_ The API request has only channel, direction, result and summary. The ledger entry needs more: event, time, actor and customer. The spec doesn't say where these come from.

_Recommendation:_

* Event: CONTACT for a recorded contact. A promise goes on the same entry.
* Actor: the logged-in user (type USER, plus their user ID).
* Source: WORKBENCH, with the endpoint ID API-P3-015.
* Customer ({{partyId}}): taken from the case. The API spec calls this field {{personKey}}, so the two names should be aligned.
* Time: add an optional {{occurredAt}} to the request, defaulting to the server time. AC1 expects 10:15, and the request has no way to send it today.

_To be discussed with the team and confirmed by the solution architect. The Product Owner confirms the_ {{occurredAt}} _change._

----

# *Three fields have no rules* ({{partyId}}, {{actionCode}}, {{contactResult}})

_Recommendation:_ add them to the field table in the spec.

* {{contactResult}} comes from the request {{result}}.
* {{actionCode}} and {{partyId}} may be empty, and the spec states where each is taken from.
* Workbench events such as CASE_CREATED have none of the three.

----

# *No message for a wrong event code* (For discussion)

_Gap:_ A missing event code has a message (MSG-GEN-001). An event code that is present but not on the approved list has none.

_Recommendation:_ reuse MSG-GEN-001 with the field "event code". The alternative is a new message, which needs an entry in §14 and Thai text under DL10.

_To be discussed with the team and confirmed by the Product Owner._

----

# *Turning the feature flag off doesn't undo the database change* (For discussion)

_Gap:_ The spec says switching the flag off is a safe rollback. But the migration makes several columns mandatory, so it is not undone by the flag.

_Recommendation:_

* State plainly that the flag controls only the new write path. The migration stays.
* Confirm that nothing wrote to {{interaction}} before this story. I found no such writer in the folder, but this needs checking.
* Define what "flag off" means: no rows written, or the old path kept.

_To be discussed with the team and confirmed by the solution architect._

----

# *AC8 reads as if a failed edit creates the correction*

_Recommendation:_ the spec records two separate facts.

* The database refuses any UPDATE or DELETE automatically.
* A correction is a separate, deliberate {{append()}} call with event CORRECTION. Nothing creates it automatically.

Reword the AC8 Gherkin so it doesn't suggest a trigger.

----

# *Linked entries aren't checked*

_Gap:_ Nothing checks {{decision_log_id}} or {{corrects_entry_id}} before saving.

_Recommendation:_ before inserting, {{append()}} checks that the referenced entry exists and belongs to the same case. If not, it refuses the call. The message needs to be defined (see item 3).

----

# *The retry has no failure path*

_Gap:_ On a number clash the writer retries once. If the retry also clashes, nothing says what happens.

_Recommendation:_ treat a second clash as a write failure: roll back, return MSG-P1-022 and raise LEDGER_WRITE_FAILED. The lock should prevent clashes in practice, so the retry is only a safeguard. Add this as a note on AC6 or as an exception path.

----

# *Load paths have no duplicate protection*

_Gap:_ Only the P3 path builds an idempotency key. The EFS load, the ALS payment load and notice dispatch have no way to avoid duplicates when they re-run.

_Recommendation:_

* Each load builds a fixed key from its source, such as the source system plus the source record ID. A re-run is then refused as a duplicate. The duplicate rejection itself belongs to RWB-E1-067.
* For the P3 path, name the header. API Spec v4 already uses {{Idempotency-Key}} (uuid) on another endpoint, so use the same one here.

----

# *The lock key isn't defined*

_Gap:_ The lock takes a number, but the case ID is a UUID. The spec doesn't say how to convert it.

_Recommendation:_ state the method, for example a 64-bit hash of the case UUID. A collision would only make two unrelated cases wait briefly for each other. It cannot give a wrong sequence, because the unique {{(case_id, case_seq)}} key still applies.

----

*10. The "Depends on" list is incomplete*

_Recommendation:_ add RWB-E1-001 (the interaction table and trigger) and RWB-E1-043 (the loader for LOV-LEDGER-EVENT) next to RWB-E1-018 and RWB-E1-027. Update both the story header and the Traceability row.

----

*11. The RWB-E1-004 cancellation leaves the EFS history load without an owner* (For discussion)

_Gap:_ Story §4 step 7 names the EFS history load as one of the callers of {{append()}}. RWB-E1-004 was meant to cover it, and it is now cancelled. Without it, older EFS collections history never reaches the ledger.

_Recommendation:_ choose one of two options.

* Reassign the EFS→ledger wiring to RWB-E1-066 or RWB-E1-018, with a story line and a test.
* Drop it explicitly, and record the effect on accounts less than 90 days past due.

Either way, re-disposition REVIEW-RWB-E1-066-002 in compliance-validation.md.

_To be discussed with the team and confirmed by the solution architect._

### Comment 8: VAISHNAVI KAULGE, 2026-11-18T15:46:43.056+0700

Comment ID 1797026

@RAPEEPAT CHULAOTRAKUL 

*Agreed.* Both prerequisite stories are needed before E1-066 can be fully built and tested.

||Prerequisite||What E1-066 needs from it||What can't be done without it||
|RWB-E1-018|The {{recovery_case}} table and case numbers (RW-YYYY-NNNNNN)|Case validation and scope checks, so AC1 and AC7 can't be tested|
|RWB-E1-027|{{DecisionLogWriter}} and the incident path ({{IncidentRecorder.raise}})|The failure path (X1, BR5, AC4), where LEDGER_WRITE_FAILED is raised. AC3 also needs a decision log entry to link to.|

*Two more dependencies to add:* the story's own preconditions also need *RWB-E1-001* (the {{interaction}} table and its append-only trigger) and *RWB-E1-043* (the loader for LOV-LEDGER-EVENT). They are missing from the story's "Depends on" header and the Traceability row, so those should list all four stories.

*Scheduling:* the planned implementation order in Project Hub v17 already places all four ahead of E1-066: E1-043 (8th), E1-001 (9th), E1-027 (20th) and E1-018 (38th). E1-066 is 44th. Following that order resolves the concern.

*Recommendation:*

* Build E1-066 only after the four prerequisites are done.
* If the team wants to start earlier, stub the missing pieces (the case lookup and {{IncidentRecorder.raise}}). Stubbed tests would not count as full verification of AC1, AC4 and AC7, so those would need re-running once the real stories are done.

### Comment 9: VAISHNAVI KAULGE, 2026-11-18T15:48:15.991+0700

Comment ID 1797031

@Chanapai Gingpuwaluck 

# *Synchronous vs asynchronous writes: who owns* {{case_seq}} *order, and does a reader see the sync entry first?* (Solution architect)

_What I found:_ E1-067's flow step 6 calls {{InteractionLedgerWriter.append()}} "with the next case_seq". So both paths use the same writer, and E1-066 owns {{case_seq}} for all of them. The outbox delivers events in written order per case.

_Recommendation:_

* State that {{case_seq}} is the order in which entries are recorded. It is gap-free, but it is not event time.
* A call recorded synchronously can therefore get a lower number than a Workbench event that happened earlier but reached the ledger later through the outbox.
* Readers order by {{occurredAt}}, with {{case_seq}} as the tie-breaker. The read index {{(case_id, occurred_at)}} already supports this.
* A reader may see the sync entry first and the async entry shortly afterwards. The outbox delivers at least once and retries up to three times, so the delay is normally short.
* AC2's wording "ordered by occurred time" and "case_seq 1 to 6" is true in its example only because the entries were loaded in time order. AC2 should say that ordering is by {{occurredAt}} and that {{case_seq}} only guarantees no gaps.

_To be discussed with the team and confirmed by the solution architect._

----

# *A ledger failure stops all officer actions (BR5)* (Ops, solution architect)

_Recommendation:_ accept the proposal.

* Add an NFR for ledger write availability, since a ledger failure now blocks every action that writes to it.
* Alert on LEDGER_WRITE_FAILED. The incident already goes to RW-PLATADM.
* Add a run book entry covering how to diagnose a failing ledger and how officers are told to retry.
* E1-056 is titled "Run books and monitoring for every Epic 1 job". The ledger isn't a job, so the team should confirm that E1-056 is the right home, or whether the entry belongs elsewhere.

_To be discussed with the team and confirmed by Ops and the solution architect._

----

# *No correction flow* (Henka BA, solution architect)

_Gap:_ The story defines the CORRECTION entry (AC8) but not who posts it, through which endpoint, or with which right.

_Recommendation:_ choose one of two options.

* *In scope:* a correction is posted through the same POST endpoint by a user with Case record C on their own case. It uses event CORRECTION and names the original entry. This means adding {{eventCode}} and {{correctsEntryId}} to {{InteractionRequest}}, and a rule for who may correct (for example, owner only, or team manager too).
* *Out of scope:* state that E1-066 provides only the CORRECTION entry type and the refusal of edits. The correction flow becomes a separate story, with the right and the endpoint defined there.

_To be discussed with the team and confirmed by the BA and the solution architect._

----

# *Retired role SY-DATALOAD* (Solution architect)

_What I found:_ E1-066's preconditions and Authority table still name SY-DATALOAD. E1-067's authority table no longer lists it. I could not find D-RCV-35 or feedback #79 in the folder, so I haven't verified the removal myself.

_Recommendation:_ remove SY-DATALOAD from E1-066 (preconditions, §3, and the Authority table, §10). Replace it with the service identity that now runs the EFS and ALS loads. The solution architect should name that identity, since the folder doesn't say.

### Comment 10: VAISHNAVI KAULGE, 2026-11-18T15:53:31.596+0700

Comment ID 1797053

@Chanapai Gingpuwaluck 


# {{case_seq}} *vs time order (AC2, BR7)* (Solution architect, Product Owner)

*Which order is authoritative?* _Recommendation:_ {{occurred_at}} is the authoritative order for the history. {{case_seq}} is the gap-free write order and nothing more. It exists to prove that no entry is missing, not to show when things happened.

*Should AC2 and the read order change?* _Recommendation:_ yes, to both.

* Reword AC2: "case_seq runs 1 to n with no gap, in write order. The ledger is read ordered by occurred_at, then case_seq."
* This matches the read order you quote for RWB-E1-068, so the two stories agree. I haven't read E1-068 myself.
* Add one entry written later than a newer one but with an earlier {{occurred_at}}. AC2 can then show the two orders differing, which the current example hides.

*Replace the 4 EFS entries with Workbench entries.* _Recommendation:_ agree. The story's own §19 already puts EFS contact outcomes in RWB-E2-034, and the story has no EFS writer in Epic 1. Rebuild AC2's data from Workbench events (for example CASE_CREATED, CASE_ALLOCATED, a recorded contact, an attached document). Update the AC1 Background (6 entries) and TC-E1-066-02 to match.

*Related wording to align:* two lines in the story still point to EFS:

* Flow step 7 names "EFS history load" as an {{append()}} caller.
* "Done when" says the history read through {{v_ace_efs_action}} writes through {{append()}}.

Both should be removed or moved to RWB-E2-034.

----

# *403 or 404 for a case outside scope (AC7, X4)* (Solution architect, Product Owner)

_Recommendation:_ use *404 with MSG-P4-003* for the whole module.

* Two of the three stories already do (E1-066 and E1-068).
* It does not confirm to the caller that the case exists.
* Reserve 403 with MSG-P4-002 for a role that lacks the Case record right.
* Change RWB-E1-024 from 403 to 404 so all three stories agree.

*AC7 addition:* add a second scenario. A case that exists but is outside the caller's scope returns 404 with MSG-P4-003 and writes no entry.

----

# *Dependencies*

*Add to "Depends on"* (story header and Traceability row): RWB-E1-001 (table and trigger) and RWB-E1-043 (LOV-LEDGER-EVENT). I'd also add the access stories you listed (RWB-E1-019, E1-022, E1-037, E1-016) for Case record C and scope, and RWB-E1-056 for the run book and alert.

*Decision: pull E1-018 and E1-027 into Q4S2, or build against stubs?* (Delivery lead, Product Owner, solution architect)

_Recommendation:_

* *First, release the hold on E1-043.* E1-001 waits on it, and E1-066's migration alters the {{interaction}} table that E1-001 creates. This one cannot be stubbed. Pulling E1-018 and E1-027 into Q4S2 doesn't help if E1-043 and E1-001 stay on hold.
* *Then build E1-066 against stubs* for E1-018 (case lookup), E1-027 ({{IncidentRecorder.raise}}) and the case access check. Move AC3, AC4 and AC7 to a later integration test, once the real stories land. Until then, stubbed passes on those three are not full verification.
* *If capacity allows, pull E1-018 and E1-027 into Q4S2 instead,* which avoids the later integration step. This is consistent with the planned order in Project Hub v17, where E1-027 and E1-018 come before E1-066.

_To be discussed with the team.Team capacity decides between the two options._

### Comment 11: Chayaporn Kaewin, 2026-11-18T17:45:53.936+0700

Comment ID 1797591

@Chitchaya Muanchonchana *Open items from gap review* 
*#1 Request→Command mapping missing (eventCode, occurredAt, actorType/Ref, partyId derivation)*
Derivation rules proposed (Event=CONTACT, Actor=logged-in user, Source=WORKBENCH/API-P3-015, partyId from case/personKey, occurredAt as new optional field) change the request contract — not yet reviewed by team.
*status question: wait — team discussion + Solution Architect sign-off (occurredAt addition already confirmed by PO)*
——————————

*#3 Invalid (vs missing) event code — no message defined*
Recommendation is to reuse MSG-GEN-001 for field "event code" instead of a new message code.
*status question: wait — Product Owner confirmation on reuse vs. new message (new message needs §14 entry + Thai text under DL10)*
——————————

*#4 Feature-flag rollback claim vs NOT NULL migration*
Need confirmation whether any prior direct-insert path into {{interaction}} exists; if so, the spec's "safe rollback" claim is wrong. Also need explicit definition of what "flag off" means (zero rows written vs. old path kept).
*status question: wait — Solution Architect to confirm prior-path existence and flag-off definition*
——————————

*#11 RWB-E1-004 cancellation leaves EFS→ledger wiring ownerless*
Two options: (a) reassign EFS→ledger wiring to RWB-E1-066/RWB-E1-018 with story line + test, or (b) drop it and record impact on accounts <90 days past due. Either way compliance finding REVIEW-RWB-E1-066-002 needs re-disposition in compliance-validation.md.
*status question: wait — Solution Architect to pick (a) or (b)*
——————————

Sum: 7 pass, 4 wait (#1 #3 #4 #11 — need team discussion / confirmation by Solution Architect or PO).

### Comment 12: Chayaporn Kaewin, 2026-11-18T18:10:54.152+0700

Comment ID 1797672

@CHANISSARA MAHAKITTIKUN there were an pending 4 points as you mention , please confirm all oending points.


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

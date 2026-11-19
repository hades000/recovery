# TB0001-1229 [RWB-E1-068] Interaction ledger read interface

| Field | Value |
|---|---|
| Jira | [TB0001-1229](https://scbjira.atlassian.net/browse/TB0001-1229) |
| Type | Story |
| Status | In Design - Solution |
| Resolution | - |
| Parent | TB0001-1162 |
| Epic link | TB0001-1162 |
| Assignee | CHANISSARA MAHAKITTIKUN |
| Reporter | KRISSADA RONGRAT |
| Priority | Medium |
| Labels | DEV-Reviewed, QA-Reviewed, R-Decision, R-Requirement, R-Spec |
| Components | E2E Workbench |
| Fix versions | - |
| Affects versions | - |
| Sprint | Design - Grooming |
| Team | RWB_SQ1 |
| Created | 2026-11-05T12:38:01.861+0700 |
| Updated | 2026-11-18T17:00:49.749+0700 |
| Due date | - |
| Resolved | - |
| Original estimate | - |
| Remaining estimate | - |
| Time spent | - |
| Votes | 0 |
| Watchers | 5 |
| Comments | 6 |

## Description

As a case owner (RW-CASEOWN), I want to read a case's ledger in one ordered sequence, filtered by channel, actor or date range, so that I can see what has happened to it before I decide anything.

## Acceptance criteria

```gherkin
Feature: Interaction ledger read interface

  Background:
    Given case "RW-2026-000401" has 9 ledger entries from 2026-08-04 to 2026-12-06
    Given 3 entries come from EFS with channel CALL between 2026-08-04 and 2026-10-15
    Given 2 entries come from user "u-owner-04" with channel VISIT on 2026-11-10 and 2026-11-20
    Given 4 entries come from the Workbench with no channel between 2026-12-01 and 2026-12-06
    Given user "u-owner-04" holds RW-CASEOWN and owns the case

  Scenario: AC1 The ledger reads in order
    Given a case with entries from several sources
    When user "u-owner-04" calls GET /cases/{caseId}/interactions for case "RW-2026-000401"
    Then 9 entries come back ordered by occurred time, earliest first
    Then each entry names its source system and source reference, for example "EFS, INT-07" or "WORKBENCH, P3 case and workflow"

  Scenario: AC2 It can be filtered
    Given the 9-entry ledger
    When it is read three times: filtered by channel "CALL", by actor "u-owner-04", and from 2026-12-01 to 2026-12-06
    Then the first read returns only the 3 EFS call entries
    Then the second read returns only the 2 VISIT entries
    Then the third read returns only the 4 Workbench entries

  Scenario: AC3 It is available to the case record
    Given the case record view SCR-03 for case "RW-2026-000401"
    When it loads
    Then its history panel shows the 9 entries from GET /cases/{caseId}/interactions
    Then the architecture test finds no class outside the ledger package that queries the interaction table

  Scenario: AC4 A date range in the wrong order
    When the case owner filters from 2026-12-06 to 2026-12-01
    Then the system refuses the call with status 422 and MSG-GEN-003 for "to" and "from"

  Scenario: AC5 A case outside the caller's scope
    Given user "u-owner-05" holds RW-CASEOWN and does not own case "RW-2026-000401"
    When the user reads its ledger
    Then the system refuses the call with status 404 and MSG-P4-003

  Scenario: AC6 Summary masked when no masking rule allows it
    Given no masking rule from Compliance is loaded for interaction.summary
    When user "u-owner-04" reads the ledger
    Then the system returns the summary of each entry as "MASKED"
    Then the channel, result, promise amount and promise date are returned in full

  Scenario: AC7 Page size at and above the limit
    When the case owner reads once with size 200 and once with size 201
    Then the read with size 200 returns the 9 entries with size 200
    Then the system refuses the read with size 201 with status 422 and MSG-GEN-002 for "size" between 1 and 200

  Scenario: AC8 A case with no entries
    Given case "RW-2026-000402" has no ledger entries
    When its owner reads the ledger
    Then the response holds 0 items and total 0
    Then the history panel shows the Empty state
```

## Comments (6)

### Comment 1: Nitchayaphan Kanpirompachira, 2026-11-16T22:44:28.000+0700, edited 2026-11-16T23:20:09.965+0700

Comment ID 1793552

After reviewing the card, I have the following concerns and questions that need clarification:

*Concerns (Dependencies):* Before this card can be fully worked on/tested, the following prerequisite cards need to be completed first:

* *RWB-E1-066* — populates the case/ledger data this endpoint reads. Without it there is no real {{recovery_case}} / ledger data to query against.
* *RWB-E1-037* — provides the role-to-permission matrix and the {{masking_rule}} table that {{interaction.summary}} masking depends on. Without a loaded masking rule, the field is masked for all roles by design (fail-closed), so a "ledger returns {{summary}} unmasked for an authorized role" scenario cannot be tested until this is in place.
* *RWB-E1-016 (CaseScopeQuery)* — this is the shared scope-check component the Flow calls to decide Own/Team/Region/All visibility (AC5, 404/MSG-P4-003). Any scope-based test (e.g. RW-TEAMMGR reading a case outside their team) needs this implemented and wired in.

*Clarification needed:*

# *Ordering*

AC1 currently states the ledger returns entries "ordered by occurred time, earliest first." However, the supporting business rule and flow in the spec (Business rules BR1, Flow step 5) describe the sort as:

{quote}"ordered by {{occurred_at}}, then {{case_seq}}"{quote}

This implies a two-level sort: {{occurred_at}} ascending as the primary key, with {{case_seq}} ascending as a tiebreaker when two or more entries share the exact same {{occurred_at}} (e.g., a batch of entries inserted together, such as a same-timestamp EFS load).

*Question:* Can we confirm that {{case_seq}} is the intended tiebreaker, and that the ordering is deterministic in this scenario?



# *Request of Date Range Field* ({{from}} and {{to}})

{{from}} and {{to}} are both optional query parameters on {{GET /cases/{caseId}/interactions}}. The only documented validation around them is exception path X1 / AC4:

{quote}"from is after to → 422, MSG-GEN-003"{quote}

*Question:* What should happen the caller sends only {{from}} (no {{to}}), or only {{to}} (no {{from}})?



# *Pagination*

AC7 covers the page *size* limit (200 is the max; 201 is refused with 422/MSG-GEN-002), but there's no AC, exception path, or test case covering the page *number* going beyond the available data.

*Question:* Can we confirm the expected response for a case has 10 total entries. The caller requests {{size=10, page=2}} (i.e., asking for the third page, which has no data). What should the response be?



# *Masking*

AC6 covers the fail-closed scenario where no masking rule is loaded for {{interaction.summary}} (every role sees {{"MASKED"}}). However, there's no AC or test case covering the opposite case — a role that *is* granted visibility via a masking rule ({{masking_rule}} table, per RWB-E1-037), where {{summary}} should be returned in clear text.

Per BR4, masking for the ledger follows the same rules as the case record, so presumably some role(s) are expected to see it unmasked once Compliance decides on DL26.

*Could you provide:*

## Which role(s) are expected to have a masking rule granting visibility into {{interaction.summary}} (even if only an assumed/draft list pending DL26 sign-off)?
## If this is still undecided, confirm that AC6 (fail-closed only) is intentionally the only masking scenario in scope for this story, and the "unmasked" case will be covered in a follow-up story once DL26 is resolved.

This will let QA write a realistic positive test case alongside the existing AC6 negative one.



# *PII Access Log*

RWB-E1-068 does not specify the PII access log entry's exact fields/example.

*Could you provide:* sample PII access log entry ?



# *Error Case Response*

*Could you provide:* sample error responses ?

### Comment 2: RAPEEPAT CHULAOTRAKUL, 2026-11-16T22:58:15.712+0700

Comment ID 1793555

# *AC1 The ledger reads in order,* when querying a case with more than 200 ledger records without providing the {{page}} and {{size}} parameters, does the API return all records, or does it default to returning the latest 50 records (page 1) as defined by {{page-size-default=50}}?"
# *AC3 It is available to the case record,* require the SCR-03 screen for testing?
# *API* GET /cases/{caseId}/interactions, please provide example of API Request and API Response.


### Comment 3: Nitchayaphan Kanpirompachira, 2026-11-17T09:30:17.742+0700

Comment ID 1793760

@Nitchayaphan Kanpirompachira 

* sample request

{noformat}curl -X GET "https://<host>/cases/RW-2026-000401/interactions?channel=CALL&actor=u-owner-04&from=2026-12-01&to=2026-12-06&size=50" \
  -H "Authorization: Bearer <token>" \
  -H "Accept: application/json"{noformat}

* sample response in case success

{noformat}{
  "items": [
    {
      "id": "INT-07",
      "caseId": "RW-2026-000401",
      "occurredAt": "2026-08-04T09:15:00Z",
      "caseSeq": 1,
      "eventCode": "CONTACT_ATTEMPT",
      "channel": "CALL",
      "direction": "OUTBOUND",
      "actorType": "SYSTEM",
      "actorRef": "EFS",
      "contactResult": "NO_ANSWER",
      "promiseAmount": null,
      "promiseDate": null,
      "summary": "MASKED", *
      "sourceSystem": "EFS",
      "sourceRef": "INT-07",
      "decisionLogEntryId": null
    }
  ],
  "page": 1,
  "size": 50,
  "total": 1
}{noformat}

### Comment 4: NATAPATCHARA ANUROJE, 2026-11-17T10:10:41.714+0700

Comment ID 1793881

Reviewed this card against the story, the FSD and the sibling ledger stories (RWB-E1-066, RWB-E1-067).

*Concerns (Dependencies):* Nitchayaphan's list above (RWB-E1-066, RWB-E1-037, RWB-E1-016) matches the story's own §3 preconditions. One more belongs on it: *RWB-E1-023* (Case record view v1) — the "history panel shows the 9 entries" half of AC3 needs SCR-03 to exist, and it doesn't have a current spec either. Build-order check: RWB-E1-066 (#44), RWB-E1-037 (#27), RWB-E1-016 (#29), RWB-E1-023 (#46) are all earlier than this story (#51) — no circular dependency, just none of the four is done yet.

----

*Clarification needed:*

*1. Ordering tiebreaker*

Already answered directly from the spec: BR1 and flow step 5 say "ordered by {{occurred_at}}, then {{case_seq}}" — {{case_seq}} is the tiebreaker. AC1's Gherkin text just doesn't spell it out.

*2. Partial date range ({{from}} only, or {{to}} only)*

Not stated anywhere in the story, FSD or BRD.

{color:#ff5630}*Question:*{color} Open-ended on the missing side, or a default window?

*3. Pagination past the last page*

The {{InteractionPage}} response shape ({{items}}, {{page}}, {{size}}, {{total}}) points to empty {{items}} + the correct {{total}} as the natural answer — standard pagination, not really a business decision.

*4. Masking*

Story §19 Out of Scope says masking rule values and the mechanism itself are RWB-E1-037/DL26's job, so AC6 (fail-closed only) does read as the intentionally sole masking scenario for this story — matches option 2 in Nitchayaphan's question above.

*5. PII access log sample*

No schema is named anywhere for this in the story. The closest named mechanism is the shared PII Kafka logging in {{backend-context.md}} §6 — if that's the intended path, the sample should come from that capability's own design, not be invented here.

*6. Error response sample*

Can build one from the existing material: message table (§14) + error list (§12). Example error shape, built from what's documented, nothing invented:
{noformat}{"status": 422, "code": "MSG-GEN-003", "message": "to cannot be before from.", "field": "to"}{noformat}

*7. Default size with no {{page}}/{{size}}*

Answered directly: {{page-size-default=50}} (story §13) — defaults to 50, never "all records."

*8. SCR-03 for AC3*

The architecture-test half of AC3 doesn't need the screen; the "history panel shows the entries" half does, and SCR-03 (RWB-E1-023) has no current spec (see Dependencies above).

*9. EFS-sourced entries conflict with Epic 1 scope (new)*

This story's own Background sets up 3 EFS-sourced entries as part of the Epic 1 test ledger. But both RWB-E1-066's and RWB-E1-067's Out of Scope sections say "Contact outcomes from EFS... (RWB-E2-034)" — i.e. EFS contact history reaching the ledger is *Epic 2* scope. RWB-E1-066's own flow step 7 also names a service identity {{SY-DATALOAD}} for "EFS and ALS loads" that isn't tied to any Epic 1 story either. Nitchayaphan's own sample response above uses {{"eventCode": "CONTACT_ATTEMPT"}} for an EFS row — a code that isn't in RWB-E1-067's event-to-ledger map (CASE_CREATED/CASE_ALLOCATED/CASE_TRANSFERRED/CASE_ESCALATED/DOCUMENT_ATTACHED/DECISION_TAKEN at all), which is more evidence nobody has actually specified where EFS rows or their event codes come from.

{color:#ff5630}*Questions:*{color}
# Is there an Epic 1 story that writes EFS-sourced {{interaction}} rows, or should this story's (and RWB-E1-066's) test data drop the EFS background entries since nothing populates them in Epic 1?
# If EFS history is in Epic 1 after all, which story owns it, and what event-code space do EFS rows use?

*10. Combined filters (new)*

AC2 tests {{channel}}, {{actor}} and the date range as three *separate* single-filter reads. {{LedgerFilter(channel, actorRef, from, to)}} structurally allows all four at once.

{color:#ff5630}*Question:*{color} If a caller supplies {{channel}}, {{actor}} and a date range together, is the result the intersection (AND), or is that combination unsupported?

----

Net: items 1, 3, 4, 6, 7 are answerable from existing material without a client answer; items 2, 5, 8, 9, 10 are genuinely open.

### Comment 5: Chanapai Gingpuwaluck, 2026-11-17T11:11:35.675+0700

Comment ID 1794126

These points add to the dependency, ordering, paging, masking, EFS and filter questions already on this card.

# *The contract is ahead of API Specification v4.* API v4 {{GET /cases/{caseId}/interactions}} has no {{actor}} query parameter (only channel, from, to, page, size), and its Interaction schema names the decision link {{decisionLogId}}. Section 12 of the story and the sample response in this thread use {{decisionLogEntryId}}.
#* Question: which name is right, and which API version will carry the {{actor}} filter? The contract tests (RWB-TE-003) are generated from API v4.
# *The response exposes internal fields.* The API v4 Interaction schema also returns {{personKey}}, {{idempotencyKey}}, {{retentionClass}} and {{contactKey}} to every reader with Case record R.
#* Question: should the case history read return only the fields in flow step 8 (event, time, actor, channel, outcome, promise, source)?
# *BR3 has no AC.* No AC checks that each entry carries its channel, the party contacted and the outcome.
# *NFR-070 has no AC.* No AC or test covers the read within 2 seconds at the 2031 volume.
#* Question: what volume per case should the performance test use?
# *404 or 403.* An out-of-scope read returns 404 (MSG-P4-003) here and in RWB-E1-066, but 403 in RWB-E1-024 for the same case. Please choose one status for the module (also raised on TB0001-1186).

Who answers: Solution architect, Henka (BA), Performance QA.

### Comment 6: Chanapai Gingpuwaluck, 2026-11-18T14:48:21.625+0700

Comment ID 1796811

Follow-up after grooming. These points are not yet in this thread (the tiebreaker, from/to alone, paging, positive masking, PII log sample, error sample, EFS rows and combined filters are already asked above).

# *Time order and case_seq can disagree.* case_seq is given in write order, but an entry written later through the outbox (RWB-E1-067) or loaded later can carry an earlier occurred_at. It then lands inside a page the reader has already seen, and RWB-E1-067 AC6 assumes case_seq follows the event order.
#* Question: is occurred_at the business order and case_seq only the tiebreaker, and should RWB-E1-067 AC6 say the same?
# *Earliest first on the panel.* With the default size of 50, a case with 5,000 entries opens on its 50 oldest entries.
#* Question: should the API accept a sort direction, or the panel open on the latest page?
# *Date filter boundary and time zone.* from and to are dates, occurred_at is a timestamp. AC2 expects the entries of 2026-12-06 when to is 2026-12-06.
#* Question: is to inclusive to the end of the day, and in which time zone (Asia/Bangkok or UTC)?
# *Actor filter values.* Not stated whether actor takes a user ID only, or also a system actor such as EFS or WORKBENCH, nor where the panel gets its list of actors.
# *Fields returned in full under AC6.* promiseAmount, promiseDate and actorRef (staff user ID) are returned unmasked. BR4 says the same rules as the case record.
#* Question: can RW-COMPLY confirm these fields need no masking?
# *No AC for Team scope.* AC5 tests only Own. RW-TEAMMGR (Team) and the other roles in section 10 have no AC or test case.
# *Architecture test (AC3, BR6, build step 7).*
#* The ArchUnit rule checks class dependencies (InteractionRepository, the entity). It does not catch a JdbcTemplate or native SQL that names the interaction table, so AC3 "queries the interaction table" claims more than the test proves. Proposal: reword AC3 to "uses InteractionRepository or the interaction entity", or add a SQL lint.
#* RWB-TE-001 BND-4 works per module (all of P1 dataengine), so a P1 class outside the ledger package is not caught. The rule needs its own ArchUnit rule or a ledger entry in recovery-modules.yaml.
#* The same rule is in RWB-E1-066 build step 7. Proposal: RWB-E1-066 owns it, this story refers to it.
# *Dependencies and sprint (Jira, 18 Nov 2026).* RWB-E1-067 writes the Workbench entries in the AC1 background but is not in Depends on. RWB-E1-016 (TB0001-1178), RWB-E1-037 (TB0001-1198) and RWB-E1-023 (TB0001-1185) are in no sprint; RWB-E1-066, RWB-E1-067 and this story are in Design - Grooming.
#* Decision needed: build against stubs of CaseScopeQuery and MaskingPolicy with a seeded ledger, or bring these stories into the delivery sprint.

Who answers: Solution architect, Henka (BA), RW-COMPLY, PO.


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

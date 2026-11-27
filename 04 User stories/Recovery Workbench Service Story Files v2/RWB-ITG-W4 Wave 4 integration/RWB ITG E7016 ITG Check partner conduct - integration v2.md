# RWB-ITG-E7016-ITG Check partner conduct

SCB Collections and Recovery. Henka Group, 22 November 2026.
(C) Siam Commercial Bank and Henka Pte Ltd

| Item | Value |
|---|---|
| Story key | RWB-ITG-E7016-ITG |
| Work type | ITG (Integration) |
| Suggested owner | TechX (suggested; any team may pick up this story) |
| Service | integration |
| Service epic | RWB-ITG-W4 |
| Wave | 4 |
| Size | Not specified in the source documents (DOR-RWB-ITG-E7016-ITG-16); the squad sizes the story at refinement |
| Business epic | EP07 |
| Release | 31 May 2027 (tentative) |
| Legacy key | RWB-E7-016 |
| Legacy disposition | Split (rework) |
| Build status | Not started |
| Patterns applied | DP03, DP13, DP19 |
| Parallel lane | L-ITG-W4 |
| Ready to start | Day 1 |
| Depends on (build) | RWB-S9-E7016-APP (not done yet) |
| Contract dependencies | RWB-S9-E7016-CON |
| Contract version | v1 (the /api/recovery/partner/v1 path the story calls) |
| Integration dependencies | RWB-S9-E7016-APP |
| External dependencies | None |
| PRD reference | 03 Requirements and specifications/PRD/Recovery Workbench PRD PLT Platform v1.md (no FR mapped to no REQ IDs) |
| Status | Draft (directive resolutions) |

**Change log.** D-RCV-60, 22 November 2026: split from RWB-E7-016 as the wave 4 integration proof of the conduct check, driven through the S9 partner read, the instruction read and the result write, the break of allocation read back on the partner, the recall read back on the instructions, and the decision record read back through rwb-decision; the build of the sampling, the breach, the allocation suspension and the recall is RWB-S9-E7016-APP and its CON story. Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

**Change log.** D-RCV-60, 26 November 2026: fixes from the rulings workbook (X20 RWB-ITG-E7016-ITG). Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

**Change log.** D-RCV-60, 26 November 2026: directive resolutions under the programme directive (18 resolved, 5 cross-document, 0 not applied). Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

### 1. Story

As a **conduct and QA officer**, I want **the conduct check proved end to end through the real partner, instruction, case and decision contracts — the sample evidenced, the breach upheld against the rule version, the allocation suspended, the affected instructions recalled and the decision record confirmed by the central ledger**, so that **partners are placed, paid and measured by rule, and a conduct check that cannot be recorded changes nothing**.

This story builds the wave 4 integration harness and the evidence for this feature, and nothing else. The conduct sampling, the breach, the allocation suspension and the recall are built by S9 in RWB-S9-E7016-APP and its CON story; the conduct and complaint records the check samples are partner results and portal records, which S9 owns. The harness builds the sample population through S9's published result write, fires the conduct check on its own trigger, observes the events on the owners' topics, reads the effect back through the partner, instruction, case and decision reads, and writes one run report per partner. It builds no production endpoint, no table, no workflow, no activity, no schedule and no screen, and it writes no code in any service.

### 2. Business rationale

A partner can hold work, submit results and be paid, and still never be checked on conduct. That is the gap this story is written against. The conduct check is FEAT-PRM-13: it samples partner contacts and complaints against the conduct rules and raises breaches, and it runs unattended on the panel data it samples (FEAT-PRM-08 is the monthly scorecard it works beside). If the check is not evidenced, a partner whose conduct breached is still allocated work, and the review forum is told a conduct position nobody can trace back to a sample.

The rule is explicit. When a conduct or complaint breach is upheld against the partner, allocation is suspended, the affected cases are recalled and the breach is reported to the partner review, to PARTNER_RECALLED, same day, owned by the partner and agency manager (R-UNI-29). A missed service level is chased once and then recalled (REQ-S9-005), and partner performance, conduct and complaint data are reported to the partner review forum (REQ-S9-007), which is why this harness asserts the sample, the breach and the recall as named evidence rather than as a narrative. The conduct stop is lifted by the conduct officer and contact resumes on the permitted channels (R-UNI-44); a conduct check that fails on a notice or a contact returns the notice for correction before filing (R-LIT-22); a placement whose measured return is below the panel threshold or whose conduct_breaches are above 0 is recalled with the reason recorded (R-WO-34); a new rule version applies from its effective date while open cases keep the version they were decided under (R-UNI-38); and an action whose decision log entry cannot be written is blocked, because no action proceeds unlogged (R-UNI-39). Every partner type is managed on the same six points (REQ-S9-001), and conduct sits inside them.

Every call is one hop on `/api/recovery/<short>/v1` with a 2 s budget (DP-11, DP-13). The decision record is written by S9 through the local decision-record library on `rwb.decision-record.v1` (DP-03) and read back through rwb-decision's contract; where a screen would compose these calls the path is the gateway-bff composite route (DP-19). The harness carries R-UNI-29, R-UNI-38, R-UNI-39, REQ-S9-005 and REQ-S9-007 into evidence rather than restating them, and it changes no rule.

### 3. Preconditions

- The published contracts of S9 rwb-partner (the partner read, the instruction read and the result write), P7 rwb-decision (the decision log), P3 rwb-case (the case) and P4 rwb-access (the session) are in the contract registry, and a stub set is generated from each one.
- The partner portal rights are in force for the run: Partner portal R to read the partner and the instructions, Partner portal U to record a result. The legacy right lists name RW-NPAMGR among the holders of U and the R list names RW-CASEOWN, RW-TEAMMGR, RW-LITOFF, RW-ENFORCE, RW-LEGAL, RW-SALEOFF, RW-NPAMGR and RW-DEBTSALE among others; the harness itself holds no business right and reads the caller's rights from the session read.
- A synthetic partner on the panel and two instructions on one case are held in the fixture as data, together with the partner results that make up the sample population, and the rule package version the fixture names rather than a version written in code.
- The conduct check has no published operation and starts on its own trigger inside S9, so the trigger is fired through the S9 fixture hook of section 12.8; until RWB-S9-E7016-APP lands, that hop is reported as a stub pass.
- RWB-S9-E7016-APP owns the sampling, the breach, the allocation suspension and the recall; its CON story owns the contract. Until the APP story lands, the stub set of section 12.8 stands in for the effect and the story is reported as a stub pass.
- The monthly scorecard (FEAT-PRM-08) is not asserted here: the check samples the results the partner submitted, and the score itself is RWB-S9-E7016-*'s sibling scope.
- The harness environment and base hosts, the fixture layout, the synthetic partner and instruction keys, the stub answer shapes, the sample size and sampling method, the source of the contacts and complaints the sample reads, the fixture hook for the unpublished conduct trigger, the evidence format and retention, and the pass or fail gate are Not specified in the source documents (GAP-0476; ASM-0668).
- No build dependency. Day 1, with the stubs in place from the first run; the one wait is RWB-S9-E7016-APP, which replaces its stub and never blocks the lane.

### 4. Flow

1. Harness: loads the fixture: partner `PTR-SYN-0008` with partner_code `PTR-SYN-0008`, partner_type AGENCY, panel_status ACTIVE and contract_end 2027-12-31, holding instructions `INS-SYN-000801` and `INS-SYN-000802` on case `RW-2027-000801`. On Day 1 the stub of section 12.8 returns the same records.
2. Harness: reads the partner through `GET /api/recovery/partner/v1/partners` with the `type` and `status` filters, and asserts the partner_code, partner_type and panel_status (DF-PRT-001 to DF-PRT-007).
3. Harness: reads `GET /api/recovery/partner/v1/partner/instructions` and asserts the two instruction rows with their case_id, instruction_type, instructed_at, due_at and status (DF-PRT-008 to DF-PRT-016).
4. Harness: builds the sample population of partner results for the period by recording a result against each instruction through `POST /api/recovery/partner/v1/partner/instructions/{instructionId}/results`, once per instruction, and asserts the answer carries the instruction with its result.
5. Harness: submits the same result a second time and asserts the answer is 409 and one result remains, so the sample population is built once and a repeated click never adds a sample.
6. Harness: fires the conduct check on its own trigger through the S9 fixture hook of section 12.8; no published operation exists for it, so the hop is recorded as a stub pass until RWB-S9-E7016-APP lands.
7. Harness: reads the sample in the evidence and asserts the sample size, the population period, the partner with its partner_code and partner_type, and each sampled contact or complaint with the instruction it belongs to. A sampled contact or complaint with no record behind it is reported as a gap in the evidence and never as a pass.
8. Harness: reads `GET /api/recovery/decision/v1/decision-log?ruleId={ruleId}&from={from}` and asserts one breach record with its decision_code, rule_id and rule_version, and that the rule_version is the version the fixture names and the version in force, not the latest one.
9. Harness: reads the partner again and asserts panel_status SUSPENDED, then reads the instructions again and asserts the affected instructions read RECALLED.
10. Harness: counts one `rwb.decision.DecisionRecorded.v1` on `rwb.decision-record.v1`, asserts the central ledger in rwb-decision confirmed the record, then replays the event and asserts the decision log still holds one breach record for the run.
11. Harness: counts the `rwb.partner.PartnerResultSubmitted.v1` publications on `rwb.partner.events.v1` for the run, asserts the consumer effect through `GET /api/recovery/case/v1/cases/{caseId}`, then replays each event and asserts the case and the instruction are unchanged, because the inbox holds one processed row per consumer; it observes `rwb.decision.RulePackageInForce.v1` on `rwb.decision.events.v1` to pin the rule version in force for the run.
12. Harness: attempts one more result write against a recalled instruction and records the refusal in the evidence, so the run shows the instruction no longer takes a sample; the answer is reported and no criterion is marked on a code no source states.
13. Harness: forces the local decision-record library to fail for the conduct check and asserts the check stops with MSG-P7-003, the breach and the recall do not run, the partner, its instructions and its cases are unchanged when they are read again, and the decision log holds no entry for the run.
14. Harness: calls `GET /api/recovery/access/v1/me/session` as a synthetic caller holding Partner portal R and not U, then attempts the result write and asserts 403 with MSG-P4-002 and no state change.
15. Harness: writes one run report per partner, keyed by story and partner_code, naming the contract version of each hop, whether the hop was a stub or the owner, the sample size and population period, the breach with its rule version, the panel status and the instruction statuses after the breach, the decision record and its ledger confirmation, and the pass or fail gate.

### 5. Exception paths

| ID | Trigger | What the harness asserts | Message | Covered by |
|---|---|---|---|---|
| X1 | A stub answers a shape the published contract does not allow | The run fails at that hop and the report names the service, the operation and the contract version; no sample is marked evidenced | None | TC-E7-016-01-ITG (ITG AC1) |
| X2 | A sampled contact or complaint has no record behind it in either read | The run fails on AC2 and the report names the sample, the read and the missing field; a sample is never reported as passed from a narrative | None | TC-E7-016-01-ITG (ITG AC1) |
| X3 | The breach completes and no decision entry carries the rule version | The run fails on AC3 and the report names the partner, the entry and the missing rule version | None | TC-E7-016-01-ITG (ITG AC1) |
| X4 | The central ledger has not confirmed the decision record and the breach stands anyway | The run fails on AC3 and the report names the partner, the entry and the missing confirmation; confirmation is never assumed | MSG-P7-003 | TC-E7-016-04-ITG (ITG AC4) |
| X5 | The breach stands and panel_status still reads ACTIVE, or an instruction still reads its old status | The run fails on AC3 and the report names the status read and the owner of the operation; the harness never sets a state it then asserts | None | TC-E7-016-01-ITG (ITG AC1) |
| X6 | The decision record fails and the breach or the recall runs anyway | The run fails on AC4 and the report names the partner, the instruction and the case before and after; nothing changes is asserted, not assumed | MSG-P7-003 (expected) | TC-E7-016-02-ITG (ITG AC4) |
| X7 | A caller holding Partner portal R and not U is allowed to record a result | The run fails on AC5 and the report names the caller's rights, the operation and the answer; a 200 is a failure even when no business data changed | MSG-P4-002 (expected, and missing) | TC-E7-016-03-ITG (ITG AC5) |

The report text is for the wave entry check and is not part of the message standard. The business messages the run touches are in section 14 and are asserted by ID and by their substituted values.

### 6. INVEST check

| Test | Result |
|---|---|
| Independent | Runs against the published contracts and the stubs from Day 1; the only wait is RWB-S9-E7016-APP, and its fixture answers until it lands |
| Negotiable | The fixture layout, the synthetic keys, the sample size and method, the report shape and the gate are configuration agreed at the wave entry check, not business values in code |
| Valuable | The sample is proved to be evidenced from named reads, the breach is proved to be upheld against the rule version, the suspension and the recall are proved to read through the owners, and a check that cannot be recorded is proved to change nothing |
| Estimable | One runner, one stub set, one sample builder, one conduct runner, one partner probe, one decision read-back, one event observer and one report |
| Small | Fits in one sprint with its five criteria and four tests |
| Testable | Each criterion runs against the stubs and again against RWB-S9-E7016-APP as it lands |

### 7. Acceptance criteria

```gherkin
Feature: Check partner conduct - wave 4 integration harness

  Background:
    Given the synthetic partner "PTR-SYN-0008" is on the panel with partner_type "AGENCY", panel_status "ACTIVE" and contract_end 2027-12-31
    Given the partner holds instructions "INS-SYN-000801" and "INS-SYN-000802" on case "RW-2027-000801"
    Given the conduct check set is loaded as data and the fixture names the rule package version in force

  Scenario: AC1 Check partner conduct (legacy RWB-E7-016 AC1)
    Given the data and the rule version this feature needs are in place
    When its trigger arrives
    Then samples partner contacts and complaints against the conduct rules and raises breaches
    Then the system writes the result to the decision log with the rule version

  Scenario: AC2 The sample is evidenced through the owners' reads (new, D-RCV-60)
    Given the partner read returns "PTR-SYN-0008" with its partner_code, partner_type and panel_status
    And the instruction read returns "INS-SYN-000801" and "INS-SYN-000802" with their case and status
    When the harness builds the sample population of partner results for the period through POST /api/recovery/partner/v1/partner/instructions/{instructionId}/results
    And the conduct check runs on its trigger
    Then the evidence names the sample size and the population period
    And the evidence names the partner with its partner_code and partner_type
    And the evidence names each sampled contact or complaint with the instruction it belongs to
    And a sample with no evidence behind it is reported as a gap in the evidence, never as a pass

  Scenario: AC3 The breach is upheld against the rule version and the recall follows (new, D-RCV-60)
    Given the conduct check has upheld a breach for "PTR-SYN-0008"
    When the check writes its result
    Then the breach is upheld only against the rule version the fixture names
    And allocation is suspended: panel_status reads "SUSPENDED" on GET /api/recovery/partner/v1/partners
    And the affected instructions read "RECALLED" on GET /api/recovery/partner/v1/partner/instructions
    And one decision record is written with its decision_code, rule_id and rule_version
    And "rwb.decision.DecisionRecorded.v1" is published once on "rwb.decision-record.v1" and confirmed by the central ledger in rwb-decision
    And the events on "rwb.partner.events.v1" are counted for the run
    And a replay of the events changes nothing: one decision entry, the same panel status and the same instruction statuses

  Scenario: AC4 A forced decision-record failure stops the breach and the recall (new, D-RCV-60)
    Given the local decision-record library is forced to fail for the conduct check
    When the conduct check runs on its trigger
    Then the breach stops with "MSG-P7-003"
    And the recall does not run
    And the partner, its instructions and its cases are unchanged when they are read again
    And the decision log holds no entry for the check

  Scenario: AC5 A caller holding Partner portal R and not U is refused on the result write (new, D-RCV-60)
    Given a synthetic caller whose right set holds Partner portal R and not Partner portal U
    When the caller records a result through POST /api/recovery/partner/v1/partner/instructions/{instructionId}/results
    Then the answer is 403 with "MSG-P4-002"
    And no result is written and the instruction and the case are unchanged

  Scenario: AC6 The context rules are read at the edge and the harness changes none of them (new, D-RCV-60)
    Given the rules BR2, BR3, BR4, BR7, BR8 and BR9 are owned by RWB-S9-E7016-APP
    When the conduct check runs on its trigger
    Then the harness reads those rules only at its edges
    And the harness sets none of those rules and changes no panel status or instruction status outside the breach and recall of AC3

  Scenario: AC7 A consumed call that fails or does not answer stops the check and writes nothing (new, D-RCV-60)
    Given the partner read is forced to fail or to not answer within the 2 s budget of BR10
    When the conduct check runs on its trigger
    Then the check stops with no breach upheld
    And no decision record is written and no recall runs
    And the partner, its instructions and its cases are unchanged when they are read again
```

Legacy AC2 (the decision log cannot be written) is built and tested in RWB-S9-E7016-APP, and this story asserts the same failure at the conduct check through AC4.

### 8. Business rules

| ID | Rule | Source | Covered by |
|---|---|---|---|
| BR1 | When a conduct or complaint breach is upheld against the partner, allocation is suspended, the affected cases are recalled and the breach is reported to the partner review, to PARTNER_RECALLED | R-UNI-29 | ITG AC3 |
| BR2 | When the conduct officer lifts the stop, contact resumes on the permitted channels, to RESUME_STATE | R-UNI-44 | Context only, read at the edge; the rule is owned by RWB-S9-E7016-APP; ITG AC6 |
| BR3 | When the conduct check on the notice or the contact fails, the notice is returned for correction before filing, to NOTICE_BLOCKED | R-LIT-22 | Context only, read at the edge; the rule is owned by RWB-S9-E7016-APP; ITG AC6 |
| BR4 | When the measured return is below the panel threshold or conduct_breaches are above 0, the placement is recalled and the reason recorded, to PLACEMENT_RECALLED | R-WO-34 | Context only, read at the edge; the rule is owned by RWB-S9-E7016-APP; ITG AC6 |
| BR5 | When a new rule version reaches its effective date, it applies to decisions taken from that date and open cases keep the version they were decided under | R-UNI-38 | ITG AC3 |
| BR6 | When the decision log entry cannot be written, the action is blocked and an incident raised; no action proceeds unlogged | R-UNI-39 | ITG AC4 |
| BR7 | A partner that misses its service level is chased once and then has the work recalled | REQ-S9-005 | Context only, read at the edge; the rule is owned by RWB-S9-E7016-APP; ITG AC6 |
| BR8 | Partner performance, conduct and complaint data are reported to the partner review forum | REQ-S9-007 | Context only, read at the edge; the rule is owned by RWB-S9-E7016-APP; ITG AC6 |
| BR9 | Every partner type is managed on the same six points: selection, contract and fees, targets and incentives, data exchange, performance reviews, notice and exit | REQ-S9-001 | Context only, read at the edge; the rule is owned by RWB-S9-E7016-APP; ITG AC6 |
| BR10 | Every call is one hop on the owner's base with a 2 s budget, and the decision record is written through the local decision-record library on the shared topic and confirmed by the central ledger | DP-11, DP-13, DP-03; ADR-020, ADR-022 | ITG AC3, AC4 and AC7 |

The harness asserts these rules and changes none of them; the rules themselves are evaluated in RWB-S9-E7016-APP, and BR2 to BR4 and BR7 to BR9 are the context the run reads at its edges, not states the harness sets.

The rule version and the conduct check set are read as reference data under DP-06 and DP-07; the parameter keys they read are Not specified in the source documents (DOR-RWB-ITG-E7016-ITG-20).

### 9. State transitions

| From | Event | Condition | To |
|---|---|---|---|
| ANY_ACTIVE | PARTNER_CONDUCT_BREACH | a conduct or complaint breach is upheld against the partner (R-UNI-29) | RECALLED (PARTNER_RECALLED) |
| HELD_CONDUCT | CONTACT_STOP_LIFTED | the conduct officer lifts the stop (R-UNI-44) | RESUME_STATE |
| PACK_VERIFIED | CONDUCT_CHECK_FAILED | the conduct check on the notice or the contact fails (R-LIT-22) | NOTICE_BLOCKED |
| PLACED_WITH_AGENCY | AGENCY_UNDERPERFORMS | measured return below the panel threshold or conduct_breaches above 0 (R-WO-34) | PLACEMENT_RECALLED |
| ANY_ACTIVE | RULE_VERSION_EFFECTIVE | a new rule version reaches its effective date (R-UNI-38) | RESUME_STATE |
| ANY_ACTIVE | DECISION_LOG_WRITE_FAILED | the decision log entry cannot be written (R-UNI-39) | EXCEPTION_QUEUE |

SENT, ACCEPTED, DECLINED, IN_PROGRESS, DONE and RECALLED are the instruction status values of DF-PRT-014; PARTNER_CONDUCT_BREACH, CONTACT_STOP_LIFTED, CONDUCT_CHECK_FAILED, AGENCY_UNDERPERFORMS, RULE_VERSION_EFFECTIVE and DECISION_LOG_WRITE_FAILED are the event codes of R-UNI-29, R-UNI-44, R-LIT-22, R-WO-34, R-UNI-38 and R-UNI-39. The panel status of DF-PRT-005 (ACTIVE, ON_NOTICE, SUSPENDED, EXITED) is the classification the run reads after the breach, and SUSPENDED is the one R-UNI-29 names. The harness changes no state: S9 rwb-partner owns every instruction and panel status above and drives InstructionWorkflow, and P3 rwb-case holds the case state the run reads. A state the harness had set by hand would prove nothing, so the report names the owner and the operation behind every value it asserts.

### 10. Authority

| Who | What they may do in this story |
|---|---|
| Conduct and QA officer | Is the role the check is written for; reads the sample and the breach, and holds the conduct stop and its lifting (R-UNI-44) |
| RW-NPAMGR, partner and agency manager | Holds Partner portal R and U; owns the breach, the allocation suspension and the recall (R-UNI-29) |
| RW-CASEOWN, RW-TEAMMGR, RW-LITOFF, RW-ENFORCE, RW-LEGAL, RW-SALEOFF, RW-DEBTSALE | Read the partner and the instructions where their rights allow; the R list of the legacy section names them |
| RW-LITOFF, RW-ENFORCE, RW-SALEOFF, RW-DEBTSALE, RW-GUARANT, RW-AGENCYMG, PT-AGENCY | Hold U per the legacy section; the portal user records the result that becomes the sample |
| QA lead | Owns the harness configuration, the fixtures, the report shape and the pass or fail gate |
| Integration lead | Owns the harness code, the stub set, the fixture hook for the conduct trigger, and the swap from a stub to the real service |
| The owning services' identities | S9 runs the sampling, the breach and the recall, answers the partner and instruction reads, records the result and writes the decision record; P7 holds the central ledger; P3 holds the case; P4 answers the session; they make every change the harness asserts |
| No delegation of authority level applies | The harness takes no business decision and raises no breach; authorisation is answered by rwb-access and the DoA table of P4 |

The legacy right list names the roles above "and 21 more" for R and "and 5 more" for U, and those further roles are not enumerated in the source, so the run reads the caller's rights from the session and never assumes a right from a list it cannot see in full.

### 11. Data

| BR Field ID | Entity | Field | Read or write |
|---|---|---|---|
| DF-PRT-001 to DF-PRT-007 | partner | id, partner_code, partner_name, partner_type, panel_status, contract_end, and the remaining field of the seven | Read through the rwb-partner contract |
| DF-PRT-008 to DF-PRT-016 | partner_instruction | id, case_id, partner_id, instruction_type, instructed_at, due_at, status, result_code | Read through the rwb-partner contract; the result write is S9's |
| DF-DEC-001 to DF-DEC-018 | decision_log_entry | id, case_id, decision_code, rule_id, rule_version, model_version, inputs_ref, and the remaining fields of the eighteen | Read through the rwb-decision contract |
| DF-REF-001 to DF-REF-015 | rule_row | id, rule_id, rule_version, route_set, from_state, event_code, and the remaining fields of the fifteen | Read through the rwb-decision contract |

Field IDs are those in the Logical Data Model and Data Dictionary v9. The legacy section names partner with DF-PRT-001 to DF-PRT-007, decision_log_entry with DF-DEC-001 to DF-DEC-018 and rule_row with DF-REF-001 to DF-REF-015, and those ranges are copied unchanged; the instruction row is cited where the S9 field catalog and the dictionary give it, and no field ID is invented. The partner and its instructions are S9's, the decision log and the rule rows are P7's, and the case behind the instruction and the sample is P3's; the harness reads them only through those contracts and never from a schema. The harness owns no table and writes no row.

### 12. Contract

#### 12.1 REST operations provided

None. The harness is a test runner and provides no REST operation.

#### 12.2 REST operations consumed

| Method | Path | Owner | Use |
|---|---|---|---|
| GET | `/api/recovery/partner/v1/partners` | S9 rwb-partner | The partner, its type and its panel status before and after the breach, with the optional `type` and `status` filters (AC1, AC2, AC3) |
| GET | `/api/recovery/partner/v1/partner/instructions` | S9 rwb-partner | The instructions placed with the partner, with their case, type and status, and the instruction each sampled contact or complaint belongs to (AC2, AC3) |
| POST | `/api/recovery/partner/v1/partner/instructions/{instructionId}/results` | S9 rwb-partner | Builds the sample population of partner results for the period, and proves the refusal after the breach (AC2, AC3, AC5) |
| GET | `/api/recovery/decision/v1/decision-log?ruleId={ruleId}&from={from}` | P7 rwb-decision | The breach records of the run, with their decision code and the rule version in force (AC1, AC3, AC4) |
| GET | `/api/recovery/case/v1/cases/{caseId}` | P3 rwb-case | The case state before and after the check and the forced failure, and the consumer effect of the partner events (AC3, AC4) |
| GET | `/api/recovery/access/v1/me/session` | P4 rwb-access | The caller's roles and rights before a read or a write (AC5) |

Every call is one hop on the owner's base `/api/recovery/<short>/v1` with a 2 s budget (DP-11, DP-13). No operation is invented in this story: each path is the owner's published operation, and where a screen would compose them the path would be the gateway-bff composite route (DP-19). The conduct check itself has no published operation and starts on its own trigger inside S9, so the harness fires the trigger through the S9 fixture hook of section 12.8, reports that hop as a stub pass until RWB-S9-E7016-APP lands, and proves the effect through the reads: the panel status on the partner read, the statuses on the instruction read, the case on the case read and the breach on the decision log.

#### 12.3 Events published

None. The harness publishes no Kafka event; it writes its report to the wave record.

#### 12.4 Events consumed

| Event | Topic | Producer | Use in the run |
|---|---|---|---|
| `rwb.partner.PartnerResultSubmitted.v1` | `rwb.partner.events.v1` | S9 rwb-partner | Counts the results that make up the sample population, asserts the case effect once, and proves the replay leaves the case and the instruction unchanged (AC3) |
| `rwb.decision.DecisionRecorded.v1` | `rwb.decision-record.v1` | S9 rwb-partner through the local decision-record library (DP-03) | Proves the breach record was published with its rule version and confirmed by the central ledger, and stays one entry after a replay (AC3, AC4) |
| `rwb.decision.RulePackageInForce.v1` | `rwb.decision.events.v1` | P7 rwb-decision | Pins the rule package version in force for the run, published by JOB-20 at 00:01, so the breach is read against the version that was in force and not the latest one (AC1, AC3) |

`rwb.partner.PartnerResultSubmitted.v1` is Arch v5 slide 43 row 21, with rwb-litigation, rwb-asset and rwb-case as consumers; `rwb.decision.DecisionRecorded.v1` is slide 42 row 08, produced by all 19 services into rwb-decision's central ledger; `rwb.decision.RulePackageInForce.v1` is slide 43 row 30, produced by rwb-decision on `rwb.decision.events.v1`, and its publication is the promote step JOB-20 of slide 44 and the publish step of slide 27. The harness subscribes to the topics under one consumer group of its own, counts publications and replays each event once. The consumer effect it reads is the case through the rwb-case operation of section 12.2; the inbox row counts of rwb-litigation and rwb-asset, the other consumers of `rwb.partner.PartnerResultSubmitted.v1`, come from the consumer evidence in the run fixture, because neither consumer exposes an operation in this story.

#### 12.5 Workflows and activities

None added. The harness exercises InstructionWorkflow, S9's workflow on the task queue `rwb-partner` in the `rwb-recovery` namespace, and observes what it does: the SLA timer per partner type that turns a missed service level into a chase and then a recall, and the activities `issueInstruction` and `recordResult`, which carries the result that becomes a sample. They are stated here as observed and not built here; no workflow, activity or Schedule is created, changed or owned by this story.

#### 12.6 Schedules

None added. The conduct check runs on its own trigger, so the harness sets no cron, no overlap policy and no catch-up window. JOB-20, the rule promote at 00:01, is rwb-decision's Schedule and is observed through its event, never started here.

#### 12.7 Tables owned

None. The harness owns no schema and no table (DP-01); partner and partner_instruction are S9's, decision_log_entry and rule_row are P7's, and recovery_case is P3's.

#### 12.8 Contract fakes

| Fake | Contract | Stubbed answer in the run |
|---|---|---|
| Stub for rwb-partner (partner read) | `GET /partners` | Partner `PTR-SYN-0008` with partner_code, partner_type AGENCY, panel_status ACTIVE, contract_end 2027-12-31 before the breach and SUSPENDED after it, filtered by the `type` and `status` parameters it is given |
| Stub for rwb-partner (instruction read) | `GET /partner/instructions` | Instructions `INS-SYN-000801` and `INS-SYN-000802` on case `RW-2027-000801`, each with its instruction_type, instructed_at, due_at, status and result; RECALLED after the breach, the status they held before it after a forced failure |
| Stub for rwb-partner (result write) | `POST /partner/instructions/{instructionId}/results` | Accepts the result once per instruction and returns the instruction with its new status; returns 409 on a second submission of the same result; refuses the write for a caller holding R and not U with 403 and MSG-P4-002 |
| Stub for rwb-decision | `GET /decision-log?ruleId={ruleId}&from={from}` | One breach record for the run with its decision_code, rule_id, rule_version and inputs_ref, and the central ledger confirmation; no entry after the forced failure |
| Stub for rwb-case | `GET /cases/{caseId}` | Case `RW-2027-000801` with its state unchanged across the conduct check and the forced failure |
| Stub for rwb-access | `GET /me/session` | Answers the session for a caller holding Partner portal R and U, and for a caller holding R and not U |
| S9 conduct-trigger fixture hook | The conduct check, which publishes no operation | Fires the check for `PTR-SYN-0008` as data: the population period, the sampled contacts and complaints, the breach and the rule package version, at the point where S9's own trigger would fire; the hook is fixture configuration and no production operation |

Each stub is generated from the published contract and its version is pinned in the run report, so a contract change shows up as a run failure and not as a silent pass. The harness environment and base hosts, the fixture layout, the synthetic partner and instruction keys, the stub answer shapes, the sample size and sampling method, the source of the contacts and complaints the sample reads, the fixture hook for the unpublished conduct trigger, the evidence format and retention, and the pass or fail gate are Not specified in the source documents (GAP-0476; ASM-0668).

#### 12.9 Call-type summary

| Call type | In this story |
|---|---|
| REST | 0 provided, 6 consumed, one hop each on `/api/recovery/<short>/v1` with a 2 s budget (DP-11, DP-13) |
| Kafka | None published; three consumed, `rwb.partner.PartnerResultSubmitted.v1`, `rwb.decision.DecisionRecorded.v1` and `rwb.decision.RulePackageInForce.v1`, counted and replayed once |
| Temporal | None added; InstructionWorkflow on `rwb-partner` observed, with its SLA timer and the `issueInstruction` and `recordResult` activities |
| File | None. The result write accepts documents on the S9 contract, and the run holds no file of its own |

### 13. Solution plan

**Package.** Folder `itg/recovery`, package `th.co.scb.ace.workbench.recovery.itg`, test scope only; not part of any deployed service.

**Pattern application**

| DP | Legacy marker | Microservice pattern | Dependency added |
|---|---|---|---|
| DP-03 | DecisionLogWriter, decision log | Local decision-record library and topic `rwb.decision-record.v1` | H RWB-PLT-E1027-CON |
| DP-13 | `/api/recovery/v1` | `/api/recovery/<short>/v1` | none |
| DP-19 | Screen, ace-web | gateway-bff composite route | H RWB-PLT-N001-CON |

The H dependencies the table adds, RWB-PLT-E1027-CON and RWB-PLT-N001-CON, are platform stories delivered by the platform wave and are not repeated in the metadata H field of this story, which stays None; DP-13 adds none. The only blocking dependency is the I story RWB-S9-E7016-APP, which replaces its stub; until it is live the run uses the stub and reports a stub pass as a stub pass, and the story is Day 1.

**Harness components**

| Component | Type | Responsibility |
|---|---|---|
| ConductRunner | Job | Runs the five owned criteria in order for a partner and holds the run lock |
| SampleBuilder | Service | Builds the sample population of partner results for the period through the result write, and proves one result per instruction |
| ConductDriver | Service | Fires the conduct check through the S9 fixture hook and records the hop as a stub pass until RWB-S9-E7016-APP lands |
| PartnerProbe | Service | Reads the partner and its panel status, and the instructions and their statuses, before and after the breach and after the forced failure |
| DecisionReadBack | Service | Reads the decision log by rule and by period, and asserts one breach record with its rule version and the ledger confirmation |
| EventObserver | Service | Subscribes to `rwb.partner.events.v1`, `rwb.decision-record.v1` and `rwb.decision.events.v1`, counts publications and replays each event once |
| CaseProbe | Service | Reads the case before and after each step and asserts it is unchanged where the run says nothing changes |
| StubSet | Fake | The six stubs and the conduct-trigger fixture hook of section 12.8, generated from the published contracts with the version pinned |
| EvidenceReport | Service | Writes one report per partner keyed by story and partner_code, and holds the pass or fail gate |

**Environment and test data.** SIT, against the stubs from Day 1 and the real services as RWB-S9-E7016-APP lands, on the synthetic partner `PTR-SYN-0008`, instructions `INS-SYN-000801` and `INS-SYN-000802`, case `RW-2027-000801` and contract end 2027-12-31, with the sampled contacts and complaints held in the fixture as data. The harness seeds nothing by hand and never writes a schema row. The environment and base hosts, the fixture layout, the synthetic keys, the sample size and method, the source of the contacts and complaints, the fixture hook for the unpublished trigger, the evidence format and retention, and the pass or fail gate are Not specified in the source documents (GAP-0476; ASM-0668).

**Build steps**

1. Generate the six stubs and the conduct-trigger fixture hook from the published contracts and the fixture, and pin each contract version in the run report; fail the run on a mismatch (X1).
2. Build the SampleBuilder and the PartnerProbe, and prove the sample population is built once through the result write with a 409 on a repeated submission (AC2, X5).
3. Name the sample size, the population period, the partner and each sampled contact with its instruction in the evidence, and fail the run where a sample has no record behind it (AC2, X2).
4. Build the ConductDriver and prove the trigger fires through the hook, with the hop reported as a stub pass until the APP story lands (AC1).
5. Add the DecisionReadBack for AC1 and AC3: one breach record with its decision code and rule version, the version that was in force, and the ledger confirmation before the breach is reported as upheld (X3, X4).
6. Prove the effect of the breach through the reads: SUSPENDED on the partner, RECALLED on the affected instructions, and the case unchanged where the rule does not move it (AC3, X5).
7. Add the EventObserver for AC3: one publication of the decision record, the partner topic events counted, the case effect once, and a replay that changes nothing (AC3).
8. Add the forced decision-record failure for AC4 through the partner, instruction and case reads before and after, so nothing changes is asserted and not assumed (X6).
9. Add the session read and the refused result write for AC5, then the EvidenceReport and the gate, and swap a stub for the real owner as RWB-S9-E7016-APP lands (X7).

**Feature switch.** None. The harness has no production flag and runs in the test environment only.

**Done when.** The tests of section 16 pass against the fakes and again against RWB-S9-E7016-APP when it lands, and the wave entry check holds a run report keyed by story and partner_code.

### 14. Validation and messages

| ID | Type | Message |
|---|---|---|
| MSG-GEN-001 | Error | Enter {field}. |
| MSG-P4-002 | Error | You cannot {action} here. Your role does not include it. |
| MSG-P7-003 | Error | The action was not taken because the decision could not be recorded. Try again in a few minutes. |

The harness asserts the message ID and the substituted values on the answer it reads, and owns no message text. The legacy section carries these three messages for the feature and no S9-specific message, so none is invented here: MSG-GEN-001 with the missing field when a read is made short of a required parameter, MSG-P4-002 with the refused action on the result write, and MSG-P7-003 when the decision record cannot be written and the breach and the recall stop.

### 15. Screens and states

The harness renders no screen: it observes the owners' operations and writes a report. The legacy section names SCR-34 Partner list and SCR-35 Placement and allocation, which belong to S9 and its CON story; the harness neither builds nor reads them, and it asserts their data through the partner read and the instruction read.

| State | Read through | What the run asserts |
|---|---|---|
| ACTIVE, ON_NOTICE, SUSPENDED, EXITED (panel status) | rwb-partner partner read | The panel classification before the breach and SUSPENDED after it (DF-PRT-005) |
| SENT, ACCEPTED, IN_PROGRESS, DONE, DECLINED, RECALLED (instruction status) | rwb-partner instruction read | The status of each instruction before the breach, RECALLED after it, and unchanged after the forced failure (DF-PRT-014) |
| The sample of contacts and complaints | rwb-partner partner and instruction reads, and the result write | Each sampled contact or complaint is named with the instruction it belongs to, or reported as a gap in the evidence |
| The breach record | rwb-decision decision log, by rule and by period | One entry with its decision code, rule version and inputs reference, confirmed by the central ledger |
| The case state | rwb-case case read | The case is unchanged by the conduct check where the rule does not move it, and unchanged by the forced failure |
| PARTNER_RECALLED, NOTICE_BLOCKED, PLACEMENT_RECALLED, EXCEPTION_QUEUE | the rule rows and the owners' reads | The conduct, notice, placement and unlogged-action context the run reads at its edges, recorded by the owning services and never set by the harness |
| SCR-34 Partner list: empty, loading, error, no access | Screen Specifications v1, section SCR-34 | Not asserted; the harness renders no screen. Loading as the screen specification states it; empty, error and no access: Not specified in the source documents (CG-ALL-1233) |
| SCR-35 Placement and allocation: empty, loading, error, no access | Screen Specifications v1, section SCR-35 | Not asserted; the harness renders no screen. Loading as the screen specification states it; empty, error and no access: Not specified in the source documents (CG-ALL-1234) |

The environment, layout and retention of the run report, the fixture hook for the conduct trigger, the stub answer shapes, the sample size and method, and the pass or fail gate are Not specified in the source documents (GAP-0476; ASM-0668).

### 16. Test cases

| TC ID | Covers | Level | Data |
|---|---|---|---|
| TC-E7-016-01-ITG | AC1 (legacy); ITG AC1 | End to end | One partner on the panel with two instructions and a sampled result on each, the conduct check and the decision record live |
| TC-E7-016-02-ITG | Legacy AC2 not recorded stays with RWB-S9-E7016-APP; ITG AC4 | Integration | The decision-record library forced to fail on the conduct check |
| TC-E7-016-03-ITG | Access; ITG AC5 | Component | A caller holding Partner portal R and not U |
| TC-E7-016-04-ITG | Principle 5; ITG AC4 | Integration | A forced decision-record failure with the partner, instruction and case reads before and after |
| TC-E7-016-05-ITG | ITG AC3 | Integration | One partner upheld for a breach against the rule version in force, with its two instructions and the decision record live |
| TC-E7-016-06-ITG | ITG AC6 | Integration | One partner with its two instructions and the conduct check live, with the context rules read at the edge |
| TC-E7-016-07-ITG | ITG AC7 | Integration | The partner read forced to fail or not answer within the 2 s budget, with the instruction read live |

The Covers column names the legacy AC the copy derives from and the ITG AC it asserts, and the full legacy test, with its Given, When and Then, is in Recovery Workbench Test Cases v8.xlsx under the same legacy test case ID. Legacy AC2, the forced decision-log failure, stays with RWB-S9-E7016-APP and is asserted here at the conduct check through AC4.

### 17. Guardrails

- No business value in code: the partner, its type, its panel status, the contract end, the rule package version, the sample size and method, the sampled contacts and complaints and the report layout are data.
- No personal data in logs, events or reports: every key is synthetic, and the events carry IDs and facts only.
- ACE data only through the owner's contract or `v_ace_*` views: this run reads no ACE data at all, and the partner, instruction, decision and case rows are read only through their owners' contracts (DP-01).
- One hop and a 2 s budget per call, with a circuit breaker per downstream, so the harness fails where a screen would (DP-11, DP-13).
- A stub pass is never reported as a real pass: the report names the contract version and whether the hop was a stub or the owner, and the conduct trigger hop is named as a stub until the APP story lands.
- A sampled contact or complaint is evidenced or reported as a gap; it is never written up from a narrative.
- The breach is read against the rule version that was in force, never against the latest version, so R-UNI-38 is asserted and not assumed.
- No action proceeds unlogged: the forced failure of R-UNI-39 must leave the partner, its instructions and its case unchanged.
- The harness never runs against UAT or production, and it never writes a row by hand or sets a state it then asserts.
- A failing criterion is fixed in the owning service or raised as a gap; it is never waived in the script.

### 18. Traceability

| Item | Source | Where it lands |
|---|---|---|
| Legacy story RWB-E7-016 Check partner conduct | Recovery Workbench User Stories Epics 3 to 8 v4, lines 12800 to 12877 | Sections 1, 3, 8, 11, 14 and 19 of this file |
| Legacy AC1, verbatim | The same, lines 12819 to 12823 | Section 7, AC1, marked (legacy RWB-E7-016 AC1) |
| Legacy AC2, Not recorded, and its test case TC-E7-016-02 | The same, lines 12825 to 12828 and 12873 | AC4 asserts the same failure here; the legacy AC stays with RWB-S9-E7016-APP (section 19) |
| Legacy test cases TC-E7-016-01 to TC-E7-016-04 | The same, lines 12872 to 12875 | Copied as -ITG in section 16 |
| FEAT-PRM-13 Check partner conduct | Epics 3 to 8 Specification v3, line 146 | Sections 1, 2 and 3 |
| FEAT-PRM-08 Score partners monthly | Epics 3 to 8 Specification v3, line 141 | Sections 2 and 19: the scorecard is read as context and not built here |
| The S9 partner, instruction and result operations | Epics 3 to 8 Specification v3, lines 216 to 219; API Specification v5 `/partners`, `/partner/instructions`, `/partner/instructions/{instructionId}/results` | Section 12.2 |
| REQ-S9-001, REQ-S9-005 and REQ-S9-007 | Business Requirements Program v5, lines 430, 434 and 436 | Section 8, BR7 to BR9 |
| R-UNI-29, R-UNI-38, R-UNI-39 and R-UNI-44 | Business Rules and Routing Logic v4, lines 433, 442, 443 and 448 | Sections 2, 8 and 9 |
| R-LIT-22 and R-WO-34 | Business Rules and Routing Logic v4, lines 161 and 365 | Sections 2, 8 and 9 |
| S9 rwb-partner contract, InstructionWorkflow and the partner topic | Architecture v5 slides 17 and 41; slide 43 rows 20 and 21 | Sections 2, 12.2, 12.4 and 12.5 |
| DecisionRecorded and the central ledger | Architecture v5 slide 42 row 08; slides 27 and 29; Temporal and Drools design slide 26 | Sections 2, 12.4 and 13 |
| RulePackageInForce and JOB-20 | Architecture v5 slide 43 row 30 and slide 44 JOB-20; slide 27; Temporal and Drools design slide 15 | Sections 12.4, 12.6 and 13 |
| InstructionWorkflow SLA timers, chase then recall | Temporal and Drools design slide 25 | Sections 2, 8 and 12.5 |
| DF-PRT-001 to DF-PRT-007, DF-PRT-008 to DF-PRT-016, DF-DEC-001 to DF-DEC-018, DF-REF-001 to DF-REF-015 | Logical Data Model and Data Dictionary v9 | Section 11 |
| DP-03, DP-13 and DP-19 | Template and Rules v1 §R5.5 | Section 13, pattern application |
| ADR-015, ADR-020 and ADR-022 | Architecture Decision Records v4 | Sections 8 and 12: outbox and inbox on Kafka, contract-first REST with one hop and 2 s, local decision record plus central ledger |

### 19. Out of scope

- RWB-S9-E7016-CON and RWB-S9-E7016-APP: the contract, the conduct sampling, the breach, the allocation suspension and the recall.
- The S9 build: the partner, instruction and result tables, the panel status, InstructionWorkflow, the portal records the sample reads, and the partner portal rights.
- The sample size, the sampling method, the population period rule and the source of the contacts and complaints as products; this story carries them as fixture data and evidence fields.
- The monthly scorecard (FEAT-PRM-08) and the calculation of the score.
- The partner gateway and FAPI 2.0: partner users reach the portal through the DMZ gateway, which is the edge stories' own scope.
- The conduct stop and its lifting (R-UNI-44), the blocked notice (R-LIT-22) and the recalled placement (R-WO-34) as products: the harness reads the context, it does not build the transitions.
- The rule registry, the rule rows and the promote job (JOB-20), which are P7's.
- Platform deployment and configuration, and the platform H dependencies named in section 13.
- Any production change: the harness runs in the test environment only.

# RWB-P6-E1032-APP Automatic attach from the OCR intake

SCB Collections and Recovery. Henka Group, 22 November 2026.
(C) Siam Commercial Bank and Henka Pte Ltd

| Item | Value |
|---|---|
| Story key | RWB-P6-E1032-APP |
| Work type | APP (App development) |
| Suggested owner | TechX (suggested; any team may pick up this story) |
| Service | rwb-comms |
| Service epic | RWB-SVC-P6 |
| Wave | 1 |
| Business epic | EP01 |
| Release | 30 November 2026 (tentative) |
| Legacy key | RWB-E1-032 |
| Legacy disposition | Split (rework) |
| Build status | Not started |
| Patterns applied | DP01, DP03, DP05, DP06, DP07, DP09, DP10, DP11, DP15, DP19 |
| Parallel lane | L-P6-E |
| Ready to start | Day 1 |
| Depends on (build) | None |
| Contract dependencies | RWB-P5-E1032-CON |
| Integration dependencies | None |
| External dependencies | None |
| PRD reference | 03 Requirements and specifications/PRD/Recovery Workbench PRD P6 rwb-comms v1.md (no FR mapped to REQ-DCM-007, REQ-DRI-004, REQ-DCM-005) |
| Status | Draft (realignment v1) |

**Change log.** D-RCV-60, 22 November 2026: secondary slice of RWB-E1-032 for rwb-comms; fixes the letter copy that `NoticeDispatchWorkflow` generates, the handoff that puts it in front of the document hub, and the `rwb.comms.NoticeGenerated.v1` event, and leaves the intake, the matcher, the attach and the review queue to rwb-document. Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

**Change log.** D-RCV-60, 26 November 2026: fixes from the deterministic build-readiness checks (X20 RWB-P6-E1032-APP). Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

### 1. Story

As a **case owner (RW-CASEOWN)**, I want **the letter copy that rwb-comms generates in `NoticeDispatchWorkflow` to reach the document hub as an intake item that carries its notice, its case and the template version it was made from**, so that **the letter the bank sent is on its case without a person filing it, on the same attach path as a scan or a partner result, and no letter copy is ever left outside the hub**.

This story is the rwb-comms slice of legacy RWB-E1-032, and it is deliberately thin. The slice boundary is fixed by the integration story of the same key, which is the authority for who owns which part of the key: *"Two of the three intake sources are contracts of services that only exist in the target: the letter copy that P6 rwb-comms generates in `NoticeDispatchWorkflow` and the partner result file that S9 rwb-partner records from the partner gateway. They are why RWB-P6-E1032-APP and RWB-S9-E1032-APP sit in the chain"* (RWB-ITG-E1032-ITG, section 2). The event that carries it is stated there as well: *"rwb.comms.NoticeGenerated.v1 — the letter copy is generated and becomes an intake item"* (RWB-ITG-E1032-ITG, section 12.4).

**What rwb-comms owns in this key.** Only two things:

- the letter copy generated in `NoticeDispatchWorkflow`, built from a Legal-approved `template` version and its `merge_field` rows and handed to the document hub through the P5 rwb-document contract, and
- the `rwb.comms.NoticeGenerated.v1` event, written to the outbox in the same transaction as the notice row and published on `rwb.comms.events.v1`.

**What rwb-comms does not own and does not re-implement.** The intake item, its OCR, the classification, the case matching, the automatic attach, the duplicate-hash check and the held-item review queue are P5 rwb-document's (`RWB-P5-E1032-APP`, `RWB-P5-E1032-CON`, `RWB-P5-E1032-INF`, `RWB-P5-E1032-OPS`). The case directory and the case status the match reads are P3 rwb-case's (`RWB-P3-E1032-APP`). The partner result file is S9 rwb-partner's (`RWB-S9-E1032-APP`). The `DOCATT` record collection into the central ledger is P7 rwb-decision's (`RWB-P7-E1032-APP`). The end-to-end proof across the five owners is `RWB-ITG-E1032-ITG`. This story writes no `document_intake`, `document`, `document_text` or `decision_log_entry` row, names no P5 table in any statement, and serves no review queue.

**Where the criteria of the legacy key are owned.** The legacy key owns no acceptance criterion here. The integration story fixes that: *"This ITG story owns no legacy acceptance criterion. Legacy AC1 to AC15 sit at component level with RWB-P5-E1032-APP, and the access and the resilience criteria sit with the sibling APP stories … RWB-P6-E1032-APP …"* (RWB-ITG-E1032-ITG, section 2). The two legacy cases whose subject still lives in this service are carried as test cases: the access case `TC-E1-032-16` and the Principle 5 case `TC-E1-032-17`. Section 7 therefore writes six new criteria that test only the deliverable in the title — the generated letter copy and its handoff — and restates no legacy criterion (GAP-1201; ASM-2148).

### 2. Business rationale

Scans, partner files and letters arrive at the Workbench without a case link, and today a person reads each one and files it. The legacy story ends that for every document whose case ID or account number is readable, and holds the rest for a person who sees the OCR text and the candidate cases. Its automatic attach runs inside the Quartz job JOB-12, stores the matched file through `DocumentStore` and writes the `DOCATT` entry through `DecisionLogWriter`, all inside one monolith.

The target makes the letter a document source like any other. A notice letter is generated by rwb-comms from an approved template and the case facts, and in the monolith that generated PDF is simply a document on the case. In the 19-service target the generated letter copy travels to the document hub, which receives it as an intake item and puts it through the same path as a scan: the hub reads it, classifies nothing of its own, matches it to its case by the case ID the copy carries, and attaches it, and the `DOCATT` record is written locally in rwb_document and collected by rwb-decision. That is why the integration story names the letter copy as one of the three intake sources of the wave 1 proof, and why this story exists at all: without it, the scan path would be the only path proved and the letter copy would never appear in the evidence.

The service boundary is what this story delivers and all it delivers. rwb-comms must not become a second document hub: it holds no intake item, runs no OCR, owns no matcher and no review queue. It must not become a second decision ledger either: it writes its decision record locally and lets rwb-decision collect it. Its job is to make one letter copy, hand it over once, and say so on its own topic with IDs and facts only. It meets REQ-DCM-007 on its side of the boundary (a classified document attaches to its case without a person doing it), it supplies the document attachment record required from Epic 1 (REQ-DRI-004) through the decision record it writes before the handoff, and it honours REQ-DCM-005 by handing every copy over rather than deciding anything about type or confidence, which stay the hub's.

The change is also a change of mechanism, and each mechanism is one decoupling pattern: the tables stay in `rwb_comms` (DP-01), the decision record is local and on the shared topic (DP-03), the case facts are read through their owners' contracts (DP-05, DP-11), the values a business person may change are data rows (DP-06, DP-07), the event travels on the service's own topic through the outbox (DP-09), the letter is generated inside a workflow instead of a Quartz job (DP-10), the schema is the service's own Flyway sequence (DP-15), and the screen is reached through gateway-bff (DP-19).

### 3. Preconditions

- `RWB-P5-E1032-CON` is published: the OpenAPI 3.1 document of the rwb-document operation that accepts a generated document for a case and answers with the document it stored, the AsyncAPI schema of the intake item the hub creates from it, and the contract fake. The build runs against that fake from Day 1 (DP-11), and it is the only contract dependency of this story.
- The exact request and answer field names of that operation, and whether the hub answers with the intake item or only with the document it stored, are Not specified in the source documents (GAP-1199; ASM-2146). The story fixes what it sends and what it needs back — the document ID and the case — and derives the rest from the published P5 document.
- The platform contracts that the DP table attaches to DP-03, DP-06, DP-07, DP-09, DP-10, DP-15 and DP-19 (`RWB-PLT-E1027-CON`, `RWB-PLT-E1042-CON` and `RWB-P3-E1042-CON`, `RWB-PLT-E1043-CON` and `RWB-P3-E1043-CON`, `RWB-PLT-TE006-CON`, `RWB-PLT-E1071-CON`, `RWB-PLT-E1044-CON`, `RWB-PLT-N001-CON`) are absent from the plan's `Depends on (build)` and `Contract dependencies` rows for this story, which are `None` and `RWB-P5-E1032-CON`. The build goes against the platform release train and the published P3 documents, and the omission is carried as one combined gap (GAP-1198; ASM-2145).
- The workflow kit is available with its `Notify` template, on task queue `rwb-comms` in namespace `rwb-recovery`, so `NoticeDispatchWorkflow` is a kit workflow and not a hand-written one (Temporal and Drools Design v1, slide 12; Architecture v5 slide 17).
- `notice`, `template` and `merge_field` exist in `rwb_comms` from the per-service Flyway sequence, in the shape of TSD P6 v2 T3.1, and the notice baseline and the template and merge-field catalog arrive from `RWB-P6-E1052-APP` and `RWB-P6-E1046-APP` (DP-01, DP-15).
- A template version in force exists for the notice type and product group: for the fixtures of this story, template "DEMAND-SSME" language "TH" version 1, approved by Legal with a valid-from date (FSD P6 AC-EXC-P6-001-02; R-LIT-03).
- The case and the party facts a letter copy merges are read through rwb-case and rwb-source-data, never by SQL, and the recipient name and address are held only in the copy the hub stores (DP-05, DP-11).
- The values a business person may change are data rows: LOV-NOTICE, LOV-LANG, LOV-PRODUCT and LOV-CHANNEL through the P3 reference-data contract (DP-07). The notice parameters this story would read through the P3 parameters contract are Not specified in the source documents, because the P6 FSD and TSD name no notice parameter at all (GAP-1200; ASM-2147).
- The local decision-record library writes the service's decision record and publishes `DecisionRecorded` on `rwb.decision-record.v1` in the same transaction as the notice row and the outbox row (DP-03; Architecture v5 slide 20).
- The event catalogue fixes the topic and the consumer of `NoticeGenerated`: topic `rwb.comms.events.v1`, consumer rwb-decision (Architecture v5 slide 42, event 13). The hub is not a consumer of that event: it learns of the copy through the call of step 5. The two mechanisms are not reconciled by any source (GAP-1202; ASM-2149).
- No name of a person is read, stored, logged or published. A notice names a case, a party object and a template version, and the event carries IDs and facts only.
- The release date 30 November 2026 is tentative and is not a precondition of this story. The story has no build dependency, so it is Ready to start on Day 1 and builds against the P5 fake while the hub story is still in flight.

### 4. Flow

1. A caller with the Litigation create right on the case posts `POST /api/recovery/comms/v1/cases/{caseId}/notices` with the notice type, the template code, the language, the person key, the business date and an `Idempotency-Key` (API-P6-001).
2. The notice boundary of rwb-comms authorises the caller through the guard library and starts `NoticeDispatchWorkflow` on task queue `rwb-comms`, keyed by the notice ID and the case ID.
3. The workflow reads the case through `GET /api/recovery/case/v1/cases/{caseId}` for the case number, the product group, the status and the owner, and the party links through `GET /api/recovery/case/v1/cases/{caseId}/parties` for the recipient object.
4. The workflow reads the template version in force for the code, the language and the product group from `template` in `rwb_comms`, refuses a version that is not approved by Legal or is withdrawn (MSG-P6-003), and resolves each merge code of the template through `merge_field` to its source entity, source field and BR field ID. The recipient name and the postal address contact point arrive through the rwb-source-data data-product contract (DP-05), with the freshness stamp of that product.
5. The `GenerateLetterCopy` activity renders the letter copy from the template body and the merge values and hands it to the document hub through the P5 rwb-document operation for a generated document on the case, with source "GENERATED", the case, the template code and version and the notice ID (DP-11, one hop, 2 s). The hub stores the copy and creates the intake item for it; the workflow receives the document ID.
6. The `RecordAndApply` activity writes, in one transaction: the `notice` row with `case_id`, `notice_type`, `party_id`, `template_id` and `document_id` set to the ID the hub returned; the local decision record for decision D7 under rule R-LIT-03 with the classifier-independent facts of the notice (the template code and version, the notice type and the rule version); and the outbox row carrying `rwb.comms.NoticeGenerated.v1` (DP-01, DP-03, DP-09).
7. The outbox relay publishes `rwb.comms.NoticeGenerated.v1` on `rwb.comms.events.v1`, keyed by the case ID, carrying the notice ID, the case ID, the document ID, the notice type, the template code, the template version and the generation time, and nothing else.
8. The controller answers 201 with the notice, its state, its template version and the `document_id` of the copy. A repeat of the same request with the same `Idempotency-Key` returns the first answer and writes nothing further.
9. `GET /api/recovery/comms/v1/notices/{noticeId}` returns the notice with its `document_id`, its template code and version and its delivery facts, for a caller with the Litigation read right and the case in scope (API-P6-002). The read changes nothing.
10. The hub then does what it does with every intake item: it reads the copy, matches it to its case by the case ID the copy carries, attaches it, or holds it for a person with its OCR text and candidates, and writes the `DOCATT` record locally in `rwb_document`. None of that is this story's: this story asserts only that the copy arrived once and that the notice holds its ID.

### 5. Exception paths

| ID | Trigger | What happens | Message | Covered by |
|---|---|---|---|---|
| X1 | The template version in force is withdrawn, or no version of the code is approved by Legal | Generation is held before any copy is made; no document is handed over and no event is written | MSG-P6-003 | AC6 |
| X2 | A merge code of the template has no `merge_field` row, or its required source value is empty | Held with `hold_reason` naming the merge code; no copy and no event; the notice is not created | MSG-GEN-001 | AC6 |
| X3 | The local decision record cannot be written | The whole transaction rolls back: no notice row, no copy handed over, no event, an incident is raised under R-UNI-39 | MSG-P7-003 | AC4 |
| X4 | The hub refuses the copy, or does not answer inside the 2 s budget | The workflow retries under its policy; until the hub answers, no notice row and no event exist; after the policy is exhausted the caller receives 503 and an incident is raised | MSG-GEN-006 | AC6 |
| X5 | The hub stores the copy but its answer is lost | The workflow retries with the same idempotency key of the notice; the hub returns the document it already stored, so one copy and one `document` row exist | None | AC3 |
| X6 | The same request arrives twice on one `Idempotency-Key` | The first notice is returned; no second notice, no second copy and no second event | None | AC3 |
| X7 | The caller holds no Litigation create right, or the case is outside the scope | Refused before the workflow starts; nothing is generated and no copy is made | MSG-P4-002, MSG-P4-003 | AC5 |
| X8 | The caller holds no Litigation read right on the notice read | Refused; no notice, no document ID and no copy content is returned | MSG-P4-002 | AC5 |
| X9 | The case read or the party read does not answer inside the 2 s budget | The workflow waits and retries; a copy is never rendered from a partial case | MSG-GEN-006 | AC6 |
| X10 | The party of the notice is not on the case | Refused; no notice row, no copy and no event | MSG-P4-003 | AC5 |
| X11 | A `document_intake` row, a match status, a candidate list or a review decision is requested from rwb-comms | rwb-comms serves no such operation and holds no such row; the request is answered 404 and the caller is pointed at the P5 operations | None | AC1 |

X11 is the boundary of the split in one row: the intake item, its match status and its review queue exist only in rwb-document, so the only correct answer of this service is that it holds none (GAP-1201; ASM-2148).

### 6. INVEST check

| Test | Result |
|---|---|
| Independent | Builds against `RWB-P5-E1032-CON` and its fake, the `rwb_comms` tables of the notice stories and the workflow kit; the case, the party, the recipient data product, the reference lists and the hub are stubs on Day 1 |
| Negotiable | The template code, the notice type, the language and the merge codes are data; the shape of the handoff request and answer is settled with the P5 team and fixed in section 12.2 |
| Valuable | The letter the bank sent lands on its case with no person filing it, and rwb-comms stays a communications service rather than becoming a second document hub |
| Estimable | One workflow from the kit, two activities, one handoff client, one event, one read operation reused, no new table |
| Small | Fits one sprint as a secondary slice of a legacy key split across five services |
| Testable | Each criterion runs against the P5 fake and the case and data-product fakes, including the withdrawn template, the lost answer, the repeat key, the decision-record failure and the refusal paths |

### 7. Acceptance criteria

```gherkin
Feature: The letter copy generated by rwb-comms reaches the document hub

  Background:
    Given notice "N-0101" of type "DEMAND" for case "RC-2026-000321" is requested from template "DEMAND-SSME" language "TH" version 1
    Given the rwb-case contract mock returns case "RC-2026-000321" open with product group "SSME"
    Given the rwb-document contract mock returns document "DOC-0501" stored for case "RC-2026-000321"

  Scenario: AC1 The letter copy reaches the hub once and the notice holds its ID (new, D-RCV-60)
    Given the rwb-document contract mock returns document "DOC-0501" with source "GENERATED" for case "RC-2026-000321"
    When NoticeDispatchWorkflow runs for notice "N-0101"
    Then the hub receives one generated document for case "RC-2026-000321" from template "DEMAND-SSME" version 1
    Then notice "N-0101" holds document_id "DOC-0501" in field DF-LEG-017
    Then rwb-comms writes no document_intake row, no document row and no match status
    Then a request for an intake item on rwb-comms is answered 404

  Scenario: AC2 The event carries IDs and facts only (new, D-RCV-60)
    Given notice "N-0101" holds document_id "DOC-0501"
    When the outbox relay publishes the event of the notice
    Then one rwb.comms.NoticeGenerated.v1 is on rwb.comms.events.v1 with the case ID as its key
    Then the event carries notice "N-0101", case "RC-2026-000321", document "DOC-0501", notice type "DEMAND", template "DEMAND-SSME" and template version 1
    Then the event carries no recipient name, no address, no account number and no document content
    Then the consumer set is rwb-decision and no other service

  Scenario: AC3 A repeat request makes no second copy and no second event (new, D-RCV-60)
    Given a notice "N-0201" of type "RECALL" for case "RC-2026-000321" was requested with Idempotency-Key "a1b2c3d4-0001"
    When the same request is sent again with Idempotency-Key "a1b2c3d4-0001"
    Then the response is the first notice with status 201
    Then case "RC-2026-000321" has one RECALL notice, one letter copy and one rwb.comms.NoticeGenerated.v1
    When the hub answered the first call and the answer was lost, and the workflow retries the handoff
    Then the hub returns document "DOC-0501" and no second document is stored

  Scenario: AC4 A decision record that cannot be written hands nothing over (new, D-RCV-60)
    Given the local decision-record write is forced to fail by the test-only fault switch
    When NoticeDispatchWorkflow runs for notice "N-0101"
    Then nothing is stored: no notice row, no copy at the hub and no outbox row
    Then no rwb.comms.NoticeGenerated.v1 is published
    Then the caller receives 503 with MSG-P7-003 and an incident is raised under R-UNI-39

  Scenario: AC5 A role without the notice right is refused (new, D-RCV-60)
    Given the rwb-access contract mock returns RW-PLATADM with Documents R and no Litigation right
    When RW-PLATADM reads notice "N-0101" and asks for the letter copy it holds
    Then the response is status 403 with MSG-P4-002
    Then no notice, no document ID and no copy content is returned
    Then no call is made to the rwb-document read

  Scenario: AC6 A hub that refuses or is late hands nothing over (new, D-RCV-60)
    Given the rwb-document contract mock refuses the generated document for case "RC-2026-000321"
    When NoticeDispatchWorkflow runs for notice "N-0101"
    Then no notice row is created and no copy is held for the case
    Then no rwb.comms.NoticeGenerated.v1 is published
    Then the caller receives 503 with MSG-GEN-006 naming the document hub and an incident is raised
    When the hub answers on the retry with document "DOC-0501"
    Then one copy and one rwb.comms.NoticeGenerated.v1 exist and no second copy is created
    Given the rwb-document contract mock delays its answer beyond 2 s
    When NoticeDispatchWorkflow runs for notice "N-0101"
    Then the workflow retries under its policy and no copy is claimed as stored
```

All six criteria are new in the realignment and test only the deliverable in the title. The legacy criteria of RWB-E1-032 are not restated: the fifteen automatic-attach and reviewer-attach criteria (legacy AC1 to AC15) are owned by `RWB-P5-E1032-APP`, and the access and resilience cases are carried here as `TC-E1-032-16` and `TC-E1-032-17` (section 16). Every cross-service line above is the mock of an owner's published answer with the values the sources fix — the notice and template values come from FSD P6 v3 (notice "N-0101", case "RC-2026-000321", template "DEMAND-SSME" "TH" version 1, notice type "DEMAND" of LOV-NOTICE, the idempotency key "a1b2c3d4-0001" of its repeated-request case) and the field IDs come from TSD P6 v2 T3.1 — and no business value was added.

### 8. Business rules

| ID | Rule | Source |
|---|---|---|
| BR1 | A letter copy is generated only from a `template` version approved by Legal and in force for the notice type, the language and the product group; a withdrawn or unapproved version holds generation and no copy is made | R-LIT-03, R-LIT-04; FSD P6 VR-P6-001-1; MSG-P6-003 |
| BR2 | Each merge code of the template resolves through `merge_field` to a source entity and a source field, and a required value that is empty holds the notice instead of printing a blank | TSD P6 v2 T3.1 (DF-REF-252 to DF-REF-260); FSD P6 BR-P6-001 |
| BR3 | The letter copy is handed to the document hub through the P5 contract with source "GENERATED", and the notice stores the document ID the hub returns | DF-LEG-017; FSD P6 A2.7 (a generated document is stored with source "GENERATED") |
| BR4 | The hub owns the intake item, the OCR, the match, the attach and the review queue; rwb-comms writes no `document_intake`, `document` or `document_text` row and reads no P5 table | DP-01; Architecture v5 slide 41; RWB-ITG-E1032-ITG section 2 |
| BR5 | The local decision record is written before the copy is claimed as stored: a record that cannot be written rolls the transaction back, stores nothing and raises an incident | Principle 5; R-UNI-39; REQ-DRI-004; MSG-P7-003 |
| BR6 | `rwb.comms.NoticeGenerated.v1` is written to the outbox in the same transaction as the notice row and published on `rwb.comms.events.v1`, keyed by the case ID, with IDs and facts only | DP-09; Architecture v5 slides 20 and 42; ADR-015 |
| BR7 | A request repeated on the same `Idempotency-Key` returns the first notice, and one notice has one copy and one event | FSD P6 AC-EXC-P6-001-04; architecture slide 11 |
| BR8 | The notice read requires the Litigation read right and the case in scope; a role without it is refused and no copy content is returned | TSD P6 v2 T-A.2 (API-P6-002) and T6.1; MSG-P4-002 |
| BR9 | Notice types, languages, product groups and channels are LOV values read through the P3 reference-data contract; no code list is written in code | DP-07; TSD P6 v2 T3.2; FSD P6 BR-P6-001 |
| BR10 | Every consumed call is one hop with a 2 s timeout and a breaker; a hub that refuses or is late hands nothing over and never leaves a notice that points at a copy the hub does not hold | DP-11; ADR-020; MSG-GEN-006 |

### 9. State transitions

This story changes no case status and no case state machine; the case is rwb-case's and is only read. It changes no match status, no review status and no document state; those are rwb-document's and are only read through its contract. What it does change is one fact on the notice row and one fact on the hub item:

| Object | Owner | Transition | Meaning |
|---|---|---|---|
| notice | P6 (rwb_comms) | `document_id` empty, then set once to the hub document ID | The letter copy of this notice exists in the hub; the value is written once and never re-pointed |
| notice | P6 (rwb_comms) | `hold_reason` set when a template is withdrawn or a merge value is missing, then cleared when the value arrives | Generation is held; no copy exists while it is held |
| document_intake | P5 (rwb_document) | PENDING, MATCHED, or one of the held values of the P5 story | Read-only here: this story reads none of it and writes none of it |

`NoticeDispatchWorkflow` is a durable run per notice: it repeats the receive, record and apply sequence of the workflow model and survives a restart without making a second copy, because the handoff carries the notice's idempotency key (Temporal and Drools Design v1, slide 13; FSD P6 AC-EXC-P6-001-04).

### 10. Authority

The rights below are the TSD P6 v2 T6.1 rights of the capability areas this story touches, Documents and Litigation. The operation declares the right it needs and the guard library asks it of the rwb-access authorise contract, one hop with a 2 s budget. Neither the access contract nor the guard library is in this story's dependency lists, so the build runs against the published access document and its fake (GAP-1198; ASM-2145).

| Who | Documents (T6.1) | Litigation (T6.1) | What this story allows |
|---|---|---|---|
| RW-LITOFF, litigation officer | CRU | CRUA | Requests the notice and its letter copy for a case in scope; reads the notice and its document ID |
| RW-LEGAL, Legal counsel | CRUA | RA | Reads the notice and its document ID; approves the template version this story reads |
| RW-CASEOWN, case owner | CRU | R | Requests the notice and its letter copy for a case in scope; reads the notice and its document ID |
| RW-TEAMMGR, team manager | R | R | Reads the notice and its document ID for a case in scope; no request |
| RW-PLATADM, platform administrator | R | - | Refused the notice read with MSG-P4-002, because it holds no Litigation right |
| the rwb-comms service identity of `NoticeDispatchWorkflow` | - | - | Generates, hands over and records the copy, and writes the event; no person is behind it |

Every "who" above is a role code. No role grants itself a right, no path in this story reads `rwb_access` by SQL, and the service identity acts under the workflow's own identity and never as a person.

### 11. Data

| BR Field ID | Entity | Field | Owner | Read or write |
|---|---|---|---|---|
| DF-LEG-015 | notice | id | P6 (rwb_comms) | Write |
| DF-LEG-016 | notice | case_id | P6 (rwb_comms) | Write |
| DF-LEG-017 | notice | document_id | P6 (rwb_comms) | Write, once, from the ID the hub returns |
| DF-LEG-018 | notice | notice_type | P6 (rwb_comms) | Write, from LOV-NOTICE |
| DF-LEG-030 | notice | party_id | P6 (rwb_comms) | Write, from the party link the case read returns |
| DF-LEG-031 | notice | template_id | P6 (rwb_comms) | Write, from the template version in force |
| DF-LEG-032 | notice | hold_reason | P6 (rwb_comms) | Write and clear on the hold paths |
| DF-LEG-034 | notice | dispatch_attempts | P6 (rwb_comms) | Write on each attempt; the dispatch of the letter itself is RWB-P6-E2021-APP |
| DF-LEG-019 to DF-LEG-023 | notice | sent_date, barcode, callback_date, delivery_status, sent_type | P6 (rwb_comms) | Not written here: they arrive from WIN in RWB-P6-E1055-APP |
| DF-LEG-033 | notice | dispatch_file_id | P6 (rwb_comms) | Not written here: it belongs to the WIN file run |
| DF-REF-045 to DF-REF-051, DF-REF-063 to DF-REF-069 | template | all fields | P6 (rwb_comms) | Read: template code, version, language, product group, body reference, Legal approval and merge codes |
| DF-REF-252 to DF-REF-260 | merge_field | all fields | P6 (rwb_comms) | Read: merge code, source entity, source field, field ID, required flag, personal-data flag and catalog version |
| DF-DOC-001 to DF-DOC-011 | document | all fields | P5 (rwb_document) | Write through the P5 contract; the service stores no document row |
| DF-DOC-060, DF-DOC-061, DF-DOC-075 | document_intake | case_id, document_id, match_status | P5 (rwb_document) | Not read and not written: the hub's, asserted only through its contract |
| DF-CAS-001, DF-CAS-002, DF-CAS-005 | recovery_case | id, case_no, status | P3 (rwb_case) | Read through the P3 case read |
| DF-CAS-026 | case_account | account_key | P3 (rwb_case) | Not read: a letter copy needs no account number |
| the recipient name and the postal address contact point | the P1 rwb-source-data data product | the party and contact-point values the copy merges | P1 (rwb_source_data) | Read through the P1 data-product contract; the BR field IDs of that contract are Not specified in the source documents (GAP-1197; ASM-2144) |
| DF-DEC-001 to DF-DEC-018 | decision_log_entry | all fields | P7 (rwb_decision) | Written locally by the local decision-record library and collected by rwb-decision; never written into `rwb_decision` by this service |

No row of `document`, `document_intake`, `document_text`, `document_type`, `recovery_case`, `case_account`, `party_ext`, `contact_point_ext`, `parameter_catalog`, `parameter_value`, `lov_value` or `decision_log_entry` is read or written by SQL in this story, and no statement in it names a table of another schema (DP-01). The `outbox_event`, `outbox_delivery`, `processed_event` and `idempotency_key` objects are the platform library objects created in `rwb_comms` by the service migration (DP-09, PLT). Field IDs are those of the Logical Data Model and Data Dictionary.

### 12. Contract

#### 12.1 REST operations provided

Owner rwb-comms (P6); base `/api/recovery/comms/v1` (DP-13). This story adds no operation of its own: it reuses the two notice operations of the service and fixes the part of their answer that carries the letter copy.

| Method | Path | API ID | Request | Answer | Access | Idempotency |
|---|---|---|---|---|---|---|
| POST | `/cases/{caseId}/notices` | API-P6-001 | `NoticeRequest`: caseId, noticeType, templateCode, language, personKey, businessDate | 201 `Notice`: id, caseId, noticeType, state, templateCode, templateVersion, documentId, holdReason | Litigation C, scope applied | `Idempotency-Key` header |
| GET | `/notices/{noticeId}` | API-P6-002 | Path `noticeId` | 200 `Notice` with the fields above and the delivery facts | Litigation R, scope applied | Not applicable |

Errors: 401 no session or no role (MSG-P4-001); 403 the role lacks the right or the case is outside the scope (MSG-P4-002, MSG-P4-003); 404 an unknown notice, or a request for an intake item, a match status or a review decision, which this service does not serve (X11); 409 the case or the template is not in a state that allows generation; 422 a missing request field (MSG-GEN-001) or a withdrawn template (MSG-P6-003); 503 the local decision record or the hub did not answer (MSG-P7-003, MSG-GEN-006).

The operation list, the two identifiers and the access of each row are TSD P6 v2 T-A.1 and T-A.2, re-based on `/api/recovery/comms/v1`. The `documentId` of the answer is the letter copy this story hands over, and its field is DF-LEG-017. The operation that a hub-facing or screen-facing caller would use to read the intake item of that copy does not exist on this service, by design.

#### 12.2 REST operations consumed

| Call | Owner | Use in this story |
|---|---|---|
| `POST /api/recovery/document/v1/cases/{caseId}/generated-documents` | P5 rwb-document | Hand over the rendered letter copy with source "GENERATED", the case, the template code and version and the notice ID, and receive the document ID; the operation and the shape of its request and answer are Not specified in the source documents (GAP-1199; ASM-2146), so the client is built from the published P5 document and its fake |
| `GET /api/recovery/document/v1/documents/{documentId}` | P5 rwb-document | Read back the stored copy in the component tests, and prove that the ID the notice holds is the hub's |
| `GET /api/recovery/case/v1/cases/{caseId}` | P3 rwb-case | The case number, the product group, the status and the owner a letter copy merges |
| `GET /api/recovery/case/v1/cases/{caseId}/parties` | P3 rwb-case | The party links of the case, to resolve the recipient object and to refuse a person who is not on the case |
| `GET /api/recovery/case/v1/admin/lists/{listCode}` | P3 rwb-case | LOV-NOTICE, LOV-LANG, LOV-PRODUCT and LOV-CHANNEL, so no notice type, language, product group or channel is written in code (DP-07) |
| `GET /api/recovery/case/v1/admin/parameters` | P3 rwb-case | The parameters contract of DP-06; no notice parameter is named by the P6 sources, so this read is present and unconfigured until the register names one (GAP-1200; ASM-2147) |
| `GET /api/recovery/source-data/v1/data-products/{productCode}/records` | P1 rwb-source-data | The recipient name and the postal address contact point the copy merges (DP-05) |
| `GET /api/recovery/source-data/v1/data-products/freshness` | P1 rwb-source-data | The data date and the freshness stamp of the product the copy merges, carried onto the decision record |
| `GET /api/recovery/decision/v1/decision-log?caseId={caseId}` | P7 rwb-decision | Read back the D7 entry of the notice in the component tests; the write itself is local (DP-03) |

Every row is one hop with a 2 s timeout and a breaker, and a GET is retried once with jitter (DP-11, ADR-020). No path in this table writes a row of the owner: the only writes are the hub's own and they happen inside its operation.

#### 12.3 Events published

| Event | Topic | Key | Payload | Consumer |
|---|---|---|---|---|
| `rwb.comms.NoticeGenerated.v1` | `rwb.comms.events.v1` | caseId | notice ID, case ID, document ID, notice type, template code, template version, generation time; no recipient name, no address, no account number and no content | rwb-decision (Architecture v5 slide 42, event 13) |

The event is written to the outbox in the same transaction as the notice row and published by the outbox relay (DP-09, ADR-015). The topic carries two further events of the service, `rwb.comms.NoticeDispatched.v1` and `rwb.comms.NoticeDelivered.v1`, and this story publishes neither: they belong to the dispatch loop of `RWB-P6-E2021-APP` and the proof-of-delivery capture of `RWB-P6-E1055-APP`. The field names of the payload beyond the IDs and values named above are Not specified in the source documents (GAP-1197; ASM-2144), so the AsyncAPI schema is written from the event catalogue row and the field IDs of section 11.

#### 12.4 Events consumed

None. `NoticeDispatchWorkflow` is started by the notice request of API-P6-001 and not by a Kafka event of this story, and this story registers no consumer, no inbox group and no retry topic. The triggers of the dispatch loop — `CaseStateChanged`, `DeviationRaised` and `DeviationCleared` for a contact stop, `TreatmentApproved` and `PaymentMissed` — are the input of the dispatch stories of the service (`RWB-P6-E2021-APP`) and are not consumed here.

#### 12.5 Workflows and activities

| Workflow or activity | Owner | Task queue | Use in this story |
|---|---|---|---|
| `NoticeDispatchWorkflow` (workflow kit, `Notify` template) | P6 rwb-comms | rwb-comms | The durable run of one notice: reads the facts, renders the copy, hands it over, records and applies, waits |
| `GenerateLetterCopy` activity | P6 rwb-comms | rwb-comms | Resolves the template version and the merge codes, renders the copy and calls the P5 generated-document operation |
| `RecordAndApply` activity | P6 rwb-comms | rwb-comms | Writes the local decision record, the notice row and the outbox row in one transaction, and applies the state |
| Approval child workflow (workflow kit, on rwb-decision) | P7 rwb-decision | rwb-decision | Not built here: the approval of a notice is `RWB-P6-E2021-APP` and the decision centre |

The workflow is a kit workflow with no business terms in its interface (Temporal and Drools Design v1, slide 12), and its history is kept well below the Temporal limits by the stage-end `Continue-As-New` of the workflow model (slide 13).

#### 12.6 Schedules

None. The letter copy is generated on the notice request, not on a clock, and this story registers no Temporal Schedule. The daily WIN file window of JOB-10 at 16:00 belongs to the dispatch loop and the integration adapter (`RWB-P6-E2021-APP`, `RWB-P6-E1007-APP`; Architecture v5 slide 44), and the intake of the hub is started by its own event, not by this service.

#### 12.7 Tables owned

| Table | Owner | Contracted use |
|---|---|---|
| `notice` | P6 (rwb_comms) | Written: the notice row, its `document_id`, its `hold_reason` and its attempt count |
| `template` | P6 (rwb_comms) | Read: the version in force, its Legal approval, its body reference and its merge codes |
| `merge_field` | P6 (rwb_comms) | Read: the merge code to source entity, source field and field ID resolution |
| `outbox_event`, `outbox_delivery` | PLT library, created in rwb_comms | Written: the `NoticeGenerated` row and its relay delivery |
| `processed_event`, `idempotency_key` | PLT library, created in rwb_comms | Written and read: the idempotency record of the notice request |
| `document`, `document_intake`, `document_text`, `document_type`, `decision_log_entry` | P5 and P7 | Not owned, never created, never read directly |

No table of another service is created, read or joined. The tables of this story live in schema `rwb_comms` under the service's own login (DP-01, DP-02).

#### 12.8 Contract fakes

| Fake | Documented answer | Used by |
|---|---|---|
| rwb-document generated-document WireMock | Document "DOC-0501" stored for case "RC-2026-000321" with source "GENERATED"; a refusal; an answer delayed beyond 2 s; a repeated call answering the document already stored | AC1, AC3, AC6 |
| rwb-document document read WireMock | Document "DOC-0501" with its case, its type and its source | AC1, AC5 |
| rwb-case case WireMock | Case "RC-2026-000321" open with product group "SSME"; a case outside the scope; a case that does not answer inside 2 s | AC1, AC5, AC6 |
| rwb-case party WireMock | The party links of case "RC-2026-000321"; a party key that is not on the case | AC1, AC5 |
| rwb-case list WireMock | LOV-NOTICE with DEMAND, RECALL, STATUTORY_SALE_NOTICE and GUARANTOR_NOTICE; LOV-LANG with TH and EN; LOV-PRODUCT with MORTGAGE, HIRE_PURCHASE, SSME and UNSECURED | AC1, AC2 |
| rwb-case parameter WireMock | A healthy answer and an empty answer, because no notice parameter is named by the sources | AC1 |
| rwb-source-data data-product WireMock | The recipient name and the postal address contact point of the party, with the freshness stamp; a stale product | AC1, AC2 |
| rwb-access authorise WireMock | RW-LITOFF with Litigation CRUA; RW-PLATADM with Documents R and no Litigation right | AC5 |
| rwb-decision decision-log WireMock | The D7 entry of notice "N-0101" read back after the local write | AC4 |
| local decision-record fake | A healthy write and a forced failure, switched by the test-only fault switch | AC4 |

The fakes are derived from the published documents of their owners because the plan gives this story one contract dependency, and each is replaced by the real owner as the wave 1 stories land.

#### 12.9 Call-type summary

| Call type | Count | Detail |
|---|---|---|
| REST | 2 reused provided, 9 consumed | API-P6-001 and API-P6-002 reused; the nine rows of section 12.2 consumed, one hop each with a 2 s budget and a breaker |
| Kafka | 1 published, none consumed | `rwb.comms.NoticeGenerated.v1` on `rwb.comms.events.v1` through the outbox, keyed by case ID; `DecisionRecorded` on `rwb.decision-record.v1` written by the local library |
| Temporal | 1 workflow, 2 activities | `NoticeDispatchWorkflow` from the kit, with `GenerateLetterCopy` and `RecordAndApply`, on task queue `rwb-comms` |
| File | None | The copy is a stored document in the hub, not a file of this service; the WIN file is the dispatch loop's |

### 13. Solution plan

**Package.** `th.co.scb.ace.workbench.recovery.comms`, module `notice`, Java package `th.co.scb.ace.workbench.recovery.comms.notice`. Service base `/api/recovery/comms/v1`, schema `rwb_comms`, topic `rwb.comms.events.v1`, task queue `rwb-comms` in namespace `rwb-recovery`, per-service login (DP-02).

**Pattern application**

| DP | Legacy marker | Microservice pattern | Dependency added |
|---|---|---|---|
| DP-01 | `recovery.<table>` or "recovery schema" | Owner's schema `rwb_comms`; never read another service's tables | none |
| DP-03 | DecisionLogWriter, decision log | Local decision-record library and topic `rwb.decision-record.v1` | H RWB-PLT-E1027-CON |
| DP-05 | AceSourceQuery, `v_ace_*`, account_ext | Read through rwb-source-data's contract or the service's own ACE views | none |
| DP-06 | Parameters, casewf.config | Parameters contract of rwb-case and the client library | H RWB-PLT-E1042-CON; C RWB-P3-E1042-CON |
| DP-07 | Reference data, LOV | Reference-data contract of rwb-case | H RWB-PLT-E1043-CON; C RWB-P3-E1043-CON |
| DP-09 | Application event, EV-nn, outbox | Outbox and inbox library; Kafka topic of the owner; CloudEvents | H RWB-PLT-TE006-CON |
| DP-10 | Quartz, JOB-nn | Temporal Schedule or event-started workflow through the workflow kit | H RWB-PLT-E1071-CON |
| DP-11 | In-process call, published interface | REST contract with mock; one hop; 2 s timeout | none (C from the legacy dependency) |
| DP-15 | V0001 baseline, migration | Per-service Flyway sequence in the service's own schema | H RWB-PLT-E1044-CON |
| DP-19 | Screen, ace-web | gateway-bff composite route | H RWB-PLT-N001-CON |

The dependencies in the table are the ones the DP table attaches to each pattern; they are not in this story's `Depends on (build)` or `Contract dependencies` rows, which the plan fixed at `None` and `RWB-P5-E1032-CON` (GAP-1198; ASM-2145). The build therefore goes against the platform release train, the published P3 documents and the P5 published document. DP-05 applies on the read side only: the recipient and address the copy merges come from the P1 contract, and this service reads no ACE view of its own. DP-11 is the handoff and every other consumed call: one hop, 2 s, breaker, a GET retried once with jitter. DP-10 replaces the `matchStep` of the Quartz job JOB-12 with a durable workflow on the service's own queue, and DP-19 is the route by which the notice screens reach the two operations.

**Components**

| Component | Type | Responsibility |
|---|---|---|
| NoticeController | Controller | The two operations of section 12.1, request validation and the problem mapping for 401, 403, 404, 409, 422 and 503 |
| NoticeRequestService | Service | The guard check, the scope check, the idempotency record and the start of the workflow |
| NoticeDispatchWorkflow | Workflow (kit `Notify`) | One durable run per notice, from the request to the recorded copy |
| GenerateLetterCopy | Activity | Template and merge resolution, rendering, and the handoff to the P5 generated-document operation |
| RecordAndApply | Activity | The local decision record, the notice row and the outbox row in one transaction |
| TemplateResolver | Service | The template version in force for the code, the language and the product group, with the withdrawn and unapproved paths refused |
| MergeFieldResolver | Service | Merge code to source entity, source field and BR field ID, and the required-value check |
| CaseFactsClient | Client | The two rwb-case reads of section 12.2, one hop with the 2 s budget |
| RecipientFactsClient | Client | The rwb-source-data data-product read and the freshness read (DP-05) |
| DocumentHubClient | Client | The handoff and the read-back, one hop, 2 s, breaker, idempotent by the notice key |
| NoticeEventWriter | Outbox | The `NoticeGenerated` row and its payload, built from the field IDs and never from a value in code |
| AccessGuardClient | Client | The rwb-access authorise answer through the guard library |
| DegradedCallRecorder | Service | One entry per degraded call, with the target, the read at time and the outcome; no personal data |

**Database and migrations**

- `notice`, `template` and `merge_field` are read and written in `rwb_comms` in the shape of TSD P6 v2 T3.1; the notice baseline and the catalog arrive with `RWB-P6-E1052-APP` and `RWB-P6-E1046-APP` (DP-01, DP-15).
- One migration in the service's sequence, `V1032_1__comms_letter_copy.sql` by the convention of the service: one partial index on `notice` over `document_id` where it is not null, so a notice is found by the copy it holds. The migration adds no column, because DF-LEG-017 already carries the document ID, and it names no table of another schema. The index is the story's own design and not a source value.
- The outbox, inbox and idempotency objects are the library objects the service migration creates in `rwb_comms` (DP-09, PLT); this story writes into them and creates none itself.

**Configuration and reference data**

- LOV-NOTICE, LOV-LANG, LOV-PRODUCT and LOV-CHANNEL through the rwb-case reference-data contract, with their versions (DP-07).
- The template code, the language and the product group of each notice type are template rows and reference data, never constants (DP-06, DP-07). No notice parameter is named by the P6 sources, so the parameters read is wired and empty until the register names one (GAP-1200; ASM-2147).
- The handoff budget: one hop, 2 s, one retry with jitter, a breaker per target, and a workflow retry policy with a bounded attempt count (DP-11, ADR-020).
- The decision code D7 and the rule R-LIT-03 are read from the rule and decision rows the local library uses, not written into the activity.

**Build steps**

1. The two operations of section 12.1 over the notice tables, with the guard and the scope check first and the idempotency record behind them; test AC3 and AC5.
2. `TemplateResolver` and `MergeFieldResolver` against the template and merge-field fixtures, with the withdrawn, unapproved and missing-value paths refused and held; test X1 and X2.
3. `CaseFactsClient` and `RecipientFactsClient` against the P3 and P1 fakes, with the timeout and stale-product paths; test AC6.
4. `GenerateLetterCopy` against the P5 generated-document fake, carrying source "GENERATED", the case, the template code and version and the notice ID, and receiving the document ID; test AC1 and AC3.
5. `RecordAndApply` with the local decision record, the notice row and the outbox row in one transaction, and the forced-failure path through the test-only fault switch; test AC4.
6. `NoticeEventWriter` and its AsyncAPI schema, with the payload check that fails the build when a personal field appears; test AC2.
7. The workflow wiring from the kit `Notify` template, with the retry policy and the lost-answer path; test AC3 and AC6.
8. The gateway-bff route behind the notice panel, then the contract-fake run of every consumed answer in isolation, so the story builds before the hub and the dispatch loop are live in SIT.

**Feature flag.** `rwb.comms.letter-copy-v1`, read as a flag of the platform library: off means no letter copy is rendered and no `NoticeGenerated` is written, and the notice request answers 503 with MSG-GEN-006 rather than creating a notice without its copy.

**Done when.** The tests in section 16 pass, the event payload check proves that no personal value is published, and a SIT week shows every requested notice holding the document ID of one letter copy, one `NoticeGenerated` per notice, and the copy present once in the hub — including after a hub outage and a retried handoff.

### 14. Validation and messages

| ID | When | Message |
|---|---|---|
| MSG-P6-003 | The template version is withdrawn or no version is approved by Legal | The {template} template has been withdrawn. The notice is on hold until Legal approves a new version. |
| MSG-GEN-001 | A required request or merge value is missing | Enter {field}. |
| MSG-GEN-004 | The case or the template changed while the request was in flight | Someone else changed this record. Reload it to see their change. |
| MSG-GEN-006 | The document hub, the case read or the recipient read refuses or does not answer, or the feature flag is off | {system} is not available. Your request is queued and will be retried. |
| MSG-P7-003 | The local decision record cannot be written | The action was not taken because the decision could not be recorded. Try again in a few minutes. |
| MSG-P4-001 | No session or no Recovery Workbench role | You have no Recovery Workbench role. Ask your team manager to request one. |
| MSG-P4-002 | The role lacks the right the operation declares | You cannot {action} here. Your role does not include it. |
| MSG-P4-003 | The case or the party is outside the caller's scope | This case is not in your scope. |

The texts are copied unchanged from RWB-E1-032, FSD P6 v3 and the shared message set; no new message ID is added. Thai text for each message follows decision DL10.

### 15. Screens and states

This story builds no screen. It serves the two operations behind the notice panel of the case screens through a gateway-bff composite route (DP-19), and it lets the panel show the letter copy the notice holds.

| Screen | State | What the user sees and does |
|---|---|---|
| the notice panel of the case screens (its screen identifier is Not specified in the source documents (GAP-1197; ASM-2144)) | requested | The notice with its type, its template code and version, and the document ID of its letter copy |
| the notice panel of the case screens | held | The notice held with `hold_reason` and the message MSG-P6-003 or MSG-GEN-001 |
| the notice panel of the case screens | unavailable | MSG-GEN-006 while the hub or the feature flag is not answering; nothing is generated |
| SCR-30 Case documents | list | The letter copy appears on its case once the hub has attached it; the screen is P5's and is not built here |
| SCR-31 Document review queue | list | A copy the hub held for a person is reviewed there with its OCR text and candidates; the screen is P5's and is not built here |

The two document screens are read from the P5 story and are listed only so that the reader sees where the copy surfaces after the handoff; this story neither builds them nor reads their state.

### 16. Test cases

| TC ID | Covers | Level | Data |
|---|---|---|---|
| TC-E1-032-17 | AC4, Principle 5 | NFR | Local decision-record write forced to fail during the letter-copy handoff; nothing stored, no NoticeGenerated, MSG-P7-003, incident raised |
| TC-E1-032-16 | AC5, Access | Component | RW-PLATADM (Documents R, no Litigation right) reads notice "N-0101" and its letter copy; refused with MSG-P4-002 |
| TC-E1-032-01 | AC1, AC2 | End to end | Letter copy of notice "N-0101" for case "RC-2026-000321" from template "DEMAND-SSME" "TH" version 1; hub returns document "DOC-0501" |
| TC-E1-032-02 | AC6 | Component | Letter copy whose hub answer is a refusal, so no notice row and no copy exist and MSG-GEN-006 is returned |
| TC-E1-032-03 | AC1 | Component | Case "RW-2026-000321" and two candidates at the hub; the copy is handed over once and rwb-comms writes no candidate |
| TC-E1-032-04 | AC1, AC2 | End to end | Letter copy matched at the hub by an account number; the copy carries the notice and the case and no account number |
| TC-E1-032-05 | AC1 | Component | A copy whose case ID and account disagree at the hub; the handoff is unchanged and no match status is written here |
| TC-E1-032-06 | AC1 | Component | A copy naming case "RW-2026-999999"; the hub holds its item and rwb-comms records the notice as generated |
| TC-E1-032-07 | AC6 | Component | A copy for closed case "RW-2026-000789"; no document row is written and the hub holds nothing |
| TC-E1-032-08 | AC3 | Component | The same letter copy requested twice; one copy, one NoticeGenerated and no second document |
| TC-E1-032-09 | AC3 | End to end | Fifteen notices already generated; a repeat run writes no further copy and no second event for them |
| TC-E1-032-10 | AC1 | Component | Letter copy of a notice whose template version is in force; the copy is handed over with its template version and the notice carries no confidence value of its own |
| TC-E1-032-11 | AC1 | Component | A notice held with review reason UNKNOWN_TYPE at the hub; the copy exists once and rwb-comms holds no review reason |
| TC-E1-032-12 | AC1 | Component | A copy the hub holds for a reviewer; rwb-comms records the notice and the reviewer's attach changes no notice row |
| TC-E1-032-13 | AC5 | Component | A caller whose scope excludes case "RC-2026-000321"; refused with MSG-P4-003 and nothing is generated |
| TC-E1-032-14 | AC5 | Component | A notice type "PAYSLIP" that is not in LOV-NOTICE; refused with MSG-GEN-001 naming the notice type |
| TC-E1-032-15 | AC3 | Component | Two requests for one notice with different idempotency keys; one notice, one copy, one event and no second handoff |

The seventeen IDs, their order and their legacy data are kept. The Level follows the mapping used across the set: legacy System is Component or End to end, legacy Access is Component and legacy Resilience is NFR. Two rows are carried full: the access case `TC-E1-032-16` proves the notice-read refusal of this service, because the attach it proved in the monolith now belongs to P5 and the read is the right the P6 matrix grants; and the Principle 5 case `TC-E1-032-17` proves the decision-record failure on the letter-copy handoff, which is the same forced-failure row of the key on the P6 side. The other fifteen keep their legacy fixture and now prove the P6 side of the same case: the copy is handed over once whatever the hub decides about it, and rwb-comms stores no match status, no candidate and no review decision. The full test, with its Given, When and Then, is in Recovery Workbench Test Cases v8.xlsx, tab Story test cases, under the same test case ID.

### 17. Guardrails

- No business value in code: the notice type, language, product group and channel come from the P3 lists, the template code and version from the template rows, and the merge codes from the merge-field catalog; no pattern, threshold or code list is compiled into the activity (DP-06, DP-07).
- No personal data in events, workflow inputs, logs, tests or prompts: the recipient name and address live only in the copy the hub stores, the event carries IDs and facts only, and a degraded-call entry carries a target and a time. The payload check of AC2 fails the build when a personal field appears.
- No cross-schema read and no cross-service write: `notice`, `template` and `merge_field` are `rwb_comms`, the copy is stored by the hub inside its own operation, and no statement names another schema (DP-01).
- ACE data only through the owner's contract or the owner's `v_ace_*` views: the recipient facts are read through the P1 data-product contract, and this service reads no ACE view of its own (DP-05).
- The decision record is written before the copy is claimed, and a record that cannot be written stores nothing and raises an incident (R-UNI-39; Principle 5).
- One REST base, one hop and a 2 s timeout on every consumed call, with a breaker and one retry with jitter on a GET; a short answer never leaves a notice pointing at a copy the hub does not hold (DP-11, ADR-020).
- The hub is the only writer of the intake item, the match status and the review decision; this service holds no copy of them and serves no operation over them (X11).
- Synthetic data only: the fixtures use the case numbers, the accounts and the user roles of the harness `RWB-ITG-W1J01-ITG`, and no production connection is opened.

### 18. Traceability

| Requirement ID | Requirement (short) | BRD section | Feature | L3 process | Rules | Test cases |
|---|---|---|---|---|---|---|
| REQ-DCM-007 | A classified document attaches to its case without a person doing it | Business Requirements Program v5, section 5.5; Business Requirements Epic 1 v5, section 3.5 | FEAT-DCM-12 | 13 Manage documents and correspondence | R-LIT-03, R-UNI-40 | TC-E1-032-01, TC-E1-032-03, TC-E1-032-04, TC-E1-032-05, TC-E1-032-06, TC-E1-032-08, TC-E1-032-09, TC-E1-032-12, TC-E1-032-15 |
| REQ-DRI-004 | Records are written from Epic 1 for case creation, owner assignment, case transfer and document attachment | Business Requirements Program v5, section 6.4; Business Requirements Epic 1 v5, section 4.4 | FEAT-DRI-04 | 13 Manage documents and correspondence | R-UNI-39, R-LIT-03 | TC-E1-032-01, TC-E1-032-04, TC-E1-032-12, TC-E1-032-14, TC-E1-032-17 |
| REQ-DCM-005 | Inbound documents are classified into one of the agreed types with a confidence score, and anything below the threshold goes to a review queue | Business Requirements Program v5, section 5.5; Business Requirements Epic 1 v5, section 3.5 | FEAT-DCM-01 | 13 Manage documents and correspondence | R-UNI-40 | TC-E1-032-10, TC-E1-032-11 |
| RWB-E1-032 | The legacy key this story is split from; its automatic-attach criteria belong to RWB-P5-E1032-APP and only the access and Principle 5 cases are carried here | Legacy section 7 and section 16 | FEAT-DCM-12 | 13 Manage documents and correspondence | BR1 to BR10 of section 8 | TC-E1-032-16, TC-E1-032-17 |
| DP set | DP01, DP03, DP05, DP06, DP07, DP09, DP10, DP11, DP15, DP19 | Template and Rules v1 section R5.5 | - | - | - | TC-E1-032-01, TC-E1-032-09, TC-E1-032-17 |
| ADR-013 | 19 services inside ACE, each with its own schema and login | Architecture v5 slides 20 and 41 | - | - | - | TC-E1-032-01 |
| ADR-015 | Kafka with outbox, inbox and CloudEvents | Architecture v5 slides 20 and 42 | - | - | - | TC-E1-032-08, TC-E1-032-09 |
| ADR-020 | Contract-first REST, one hop, 2 s timeout | Template and Rules v1 section R5.5, DP-11 | - | - | - | TC-E1-032-02, TC-E1-032-04 |
| ADR-021 | Per-service Flyway and migration ownership | Template and Rules v1 section R5.5, DP-15 | - | - | - | TC-E1-032-01 |
| ADR-022 | Local decision record plus central ledger | Architecture v5 slide 28; R-UNI-39 | - | - | - | TC-E1-032-17 |

The three requirement IDs are the ones the WP fixes for this story; the BRD section numbers follow the requirement rows of the Program and Epic 1 extracts, and where the row carries no section number the extract's section of the requirement group is cited.

### 19. Out of scope

- The intake item, its OCR, the classification, the case match, the automatic attach, the duplicate-hash check and the held-item review queue: rwb-document, `RWB-P5-E1032-APP`, `RWB-P5-E1032-CON`, `RWB-P5-E1032-INF` and `RWB-P5-E1032-OPS`.
- The case directory, the case status and the party links: rwb-case, `RWB-P3-E1032-APP`.
- The partner result file as an intake source: rwb-partner, `RWB-S9-E1032-APP`.
- The `DOCATT` record collection into the central ledger: rwb-decision, `RWB-P7-E1032-APP`.
- The end-to-end proof across the five owners and the harness: `RWB-ITG-E1032-ITG`.
- The dispatch of the letter through WIN, the proof of delivery, the barcode, the sent date and the notice-period timer: `RWB-P6-E2021-APP` and `RWB-P6-E1055-APP`.
- The approval of a notice and its delegation-of-authority routing: `RWB-P6-E2013-APP` and the decision centre.
- The template and merge-field administration and the Legal approval of a version: `RWB-P6-E1046-APP`.
- Confirming or correcting the type and the fields of a document stored for review: `RWB-E1-054`.
- Source pickup from scanners, SFTP and mailboxes, and the intake item base record: `RWB-E1-057`.
- Moving an attached document to another case, and the attach of field app photos: Epic 2 and `RWB-E2-024`.
- The build of the screens and of the gateway-bff composite route itself: `RWB-PLT-N001-CON`.

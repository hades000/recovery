# RWB-P4-E2021-APP Letter dispatch loop with proof of delivery from WIN

SCB Collections and Recovery. Henka Group, 27 November 2026.
(C) Siam Commercial Bank and Henka Pte Ltd

| Item | Value |
|---|---|
| Story key | RWB-P4-E2021-APP |
| Work type | APP (App development) |
| Suggested owner | TechX (suggested; any team may pick up this story) |
| Service | rwb-access |
| Service epic | RWB-SVC-P4 |
| Wave | 2 |
| Business epic | EP02 |
| Release | 31 December 2026 (tentative) |
| Legacy key | RWB-E2-021 |
| Legacy disposition | Split (rework) |
| Build status | Not started |
| Patterns applied | DP01, DP03, DP05, DP07, DP09, DP10, DP11, DP13, DP18, DP19 |
| Parallel lane | L-P4-AN |
| Ready to start | Day 1 |
| Size | Not set; the squad sizes it at refinement; fit to a two-week iteration is Not specified in the source documents (DOR-RWB-P4-E2021-APP-15) |
| Depends on (build) | None on stories of this set; platform CON stories RWB-PLT-E1027-CON, RWB-PLT-E1043-CON, RWB-PLT-TE006-CON, RWB-PLT-E1071-CON, RWB-PLT-E1044-CON, RWB-PLT-N001-CON (Ready to start Day 1 holds) |
| Contract dependencies | RWB-P4-E1037-CON (operations in 12.1); RWB-P6-E2021-CON; RWB-P3-E1043-CON (rwb-case reference-data contract, read at the version carried by the record; the rwb-case baseline version is Not specified in the source documents (GAP-1277)); built against REST major version `v1` (path `/api/recovery/access/v1`); the contract version identifier is Not specified in the source documents (DOR-RWB-P4-E2021-APP-23) |
| Integration dependencies | INT-14 WIN daily dispatch file, consumed through RWB-P6-E2021-CON; the file layout is Not specified in the source documents (GAP-1602); the versioned interface definition is owned by `rwb-integration` and the dispatch is built against its fake until the layout is agreed |
| External dependencies | RWB-ACE-001 Section B view `v_ace_pod` for proof of delivery (DL43 open, GAP-1608): proof-of-delivery capture stays behind its feature flag until the view is available; fallback is proof entered by hand against the barcode, to be agreed before wave 2 |
| PRD reference | 03 Requirements and specifications/PRD/Recovery Workbench PRD P4 rwb-access v1.md (no FR mapped to REQ-OCC-003, REQ-OCC-005, REQ-OCC-006, REQ-ILG-010) |
| Status | Draft (directive resolutions) |
| Readiness decisions | RD-P1-007, RD-P1-041, RD-P1-064 |

**Version 3 changes.**

- Ledger and proof ownership restated per RD-P1-007: the P1 proof-of-delivery read writes nothing; `rwb-comms` appends the delivery entry over REST and `rwb-source-data` stores it (finding 1).
- The Case record C check on that append is named as a precondition; the permission row for the `rwb-comms` identity is added by RD-P1-064 rule 2, NEW-GAP-F10-01 closed (finding 2).
- RD-P1-041: this slice reads and writes no freshness stamp; no behaviour change.
- Finishing pass: the delivery entry reference is the WIN barcode, else the notice reference, and the `rwb-comms` append permission is settled (RD-P1-064); test case IDs of Test Cases v9 applied.
- Test case citations aligned to Test Cases v9: identifiers of this story replace the placeholders and the shared legacy identifiers that now hold another story's case (W2-tests mapping).

**Change log.** D-RCV-60, 27 November 2026: D-RCV-60 P1 developer readiness (RD-P1 register).

**Change log.** D-RCV-60, 22 November 2026: split from RWB-E2-021 for rwb-access. Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

**Change log.** D-RCV-60, 26 November 2026: fixes from the rulings workbook (X20 RWB-P4-E2021-APP). Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

**Change log.** D-RCV-60, 26 November 2026: directive resolutions under the programme directive (19 resolved, 40 cross-document, 6 not applied). Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

### 1. Story

As a **litigation officer (role `RW-LITOFF`) who requests a notice, reads it on SCR-18 and follows it through the WIN dispatch and the proof of delivery, and the recovery service identity that runs JOB-10 (role class `NON_HUMAN_ACTOR`, scope `ALL`; role code Not specified in the source documents (DOR-RWB-P4-E2021-APP-1; GAP-0948))**, I want **an access answer that says whether my role carries the Litigation right to request a notice and to read it with its dispatch and its proof, which scope and which policy versions that answer was taken from, and an access entry for every look at a notice that names the notice, the case and the personal fields as masked but never the addressee's address**, so that **the notice that starts the notice period is only requested and only read by a role that may do it, every hop of the dispatch loop is gated by the access service, and no name or address of an addressee reaches a log line, an event or a screen that did not ask for it**.

Inside `rwb-access` this is the access slice of legacy RWB-E2-021:

- Service `rwb-access`, schema `rwb_access`, REST base `/api/recovery/access/v1`, topic `rwb.access.events.v1` with event names `rwb.access.<Event>.v1`, Temporal task queue `rwb-access` in namespace `rwb-recovery`, Java package `th.co.scb.ace.workbench.recovery.access`.
- Three answers and one record, and nothing else: the authorise decision for capability area `LITIGATION` with right `C` on requesting a notice and right `R` on reading a notice, its dispatch and its proof; the resolved permission answer for the caller; the masking answer for the two personal fields the notice panel carries, `DF-PTY-007` and `DF-PTY-016`, the second of which is the addressee postal address over `v_ace_contact.contact_value`; and the access entry written as a decision-record entry of DP-03 on every allowed read (`AC-READ`) and every refusal (`AC-DENY`).
- The slice delivers no business behaviour of the legacy key. The conduct check, the WIN file, the notice state, the append of the delivery entry to the interaction ledger and the `NoticeDispatched` and `NoticeDelivered` events are `rwb-comms`'s (RWB-P6-E2021-APP, with the append under RWB-P6-E1055-APP); the proof read of `v_ace_pod` (`GET /api/recovery/source-data/v1/proof-of-delivery?businessDate=`, which writes nothing) and the ledger store are `rwb-source-data`'s (RD-P1-007 rules 1 and 7). The notice facts reach this slice through the published contract RWB-P6-E2021-CON and its fake, one hop, with the 2 s timeout of DP-11. This story neither holds a notice nor moves its state.
- JOB-10 (WIN notices, daily 16:00) runs in `rwb-comms` with `rwb-integration` (Architecture v5 slide 44) and is not this story's Schedule. What this story owns is the read the conduct check makes before JOB-10 selects a notice: the job asks for the service identity's Litigation R answer, and this service writes one `AC-READ` entry naming the notice, the case and the field markers, and never the address.
- The delegation of authority plays no part: the legacy authority table says that no approval level applies in this story, so this story answers no DoA question and reads no `delegation_limit` row, which stays RWB-P4-E2013-APP's.
- The slice builds no screen. The notice approval panel SCR-18 and the case timeline SCR-04 are served through the gateway-bff composite route of DP-19, the notice is `rwb-comms`'s, the case facts and the case ownership are `rwb-case`'s, and the central ledger entry of a decision is `rwb-decision`'s.
- Screen states of SCR-04 and SCR-18 served by the gateway-bff composite route: no access is the 403 answer with MSG-P4-002 (AC2) and the 404 answer with MSG-P4-003 (AC4); error is the 503 answer with MSG-P7-003 (AC10); empty and loading states are Not specified in the source documents (DOR-RWB-P4-E2021-APP-10).
- The policy pack is data: permission rows under matrix version `PM-2026.12`, masking rows under masking version `MASK-SIT-01`. The load path that writes those rows is this service's own and is out of this story (RWB-P4-AD002-APP, RWB-P4-AD004-APP).

The Litigation letters per role are Not specified in the source documents (GAP-0945; ASM-1672): the TSD P4 matrix tabulates only three capability areas and has no Litigation column, so the letters the legacy authority table names are carried as a policy pack assumption under `PM-2026.12`. The request and answer shape of the authorise call is Not specified in the source documents (GAP-0946; ASM-1673); no field of it is a business value and it is renamed at the contract review if the published contract differs. The masking version label in force in SIT and the field IDs and rendering of the addressee's postal address on the notice panel are Not specified in the source documents (GAP-0947; ASM-1674). The role code and scope of the service identity that runs JOB-10 are Not specified in the source documents (GAP-0948; ASM-1675); NFR-051 fixes only that such an identity passes the same checks as a person, and the role class is `NON_HUMAN_ACTOR` with scope `ALL`.

The rights carried from the legacy story are unchanged: `RW-LITOFF` holds Litigation `C` and `R`, `RW-ENFORCE` holds Litigation `CRU`, `RW-CASEOWN`, `RW-LEGAL`, `RW-HEADLIT` and the other roles with Litigation `R` read the notice and its dispatch and proof, a role with no `LITIGATION` row is refused, and internal audit reads with scope `ALL`.

### 2. Business rationale

A notice period counted from the print date can be challenged, and a letter sent while a contact stop is on is a conduct breach. The legacy story proved the dispatch loop; this slice proves who may enter it. Today the right to request and read a notice is spread over role documents and manual checks, and the addressee's address is copied into working files and log lines that no one reviews. Under Architecture v5 the authorise answer and the masking answer come from `rwb-access` as data, with the matrix version and the mask version naming the policy the answer was taken from, and every look at a notice is an append-only entry in the same ledger as the decisions.

This story carries controls CTL-15 (the notice period starts from proof of delivery) and CTL-16 (a contact stop blocks the contact) on the access side only, and the audit expectation behind NFR-042 (every read of the case store and the document store is logged) and NFR-051 (a service identity is subject to the same role checks as a person). It meets REQ-OCC-003, REQ-OCC-005, REQ-OCC-006 and REQ-ILG-010 on the access side and supports the measure notices with proof of delivery, target 100 percent, and the measure rule and limit changes made without a code release, target 100 percent.

The realignment changes the mechanism, not the business rule:

1. The permission rows and the masking rows of the monolith's recovery schema become `rwb-access`'s own tables in `rwb_access` (DP-01), versioned by matrix version and mask version, so a change of rights or of masking needs an approved load and no release.
2. The synchronous `RecoveryAccessGuard` call inside the monolith becomes the published authorise contract, cached, with one hop and a 2 s timeout (DP-11); the screen route and `rwb-comms` ask `rwb-access` and hold the answer for the life of the cache entry.
3. The decision-log writer inside the monolith becomes the local decision-record library of DP-03, so an `AC-READ` or an `AC-DENY` entry is hash-chained and published on `rwb.decision-record.v1` where `rwb-decision`'s ledger and the access audit query already read.
4. The access event that the monolith never sent becomes `rwb.access.AccessPolicyChanged.v1` on `rwb.access.events.v1`, and every holder of a cached answer refreshes on it, so a new masking version is in force at the next call with no deployment.
5. The ACE data behind the masked fields stays where it is: the address value is read through `rwb-source-data`'s contract by whoever displays it, and `rwb-access` answers only that the field is masked and under which version (DP-05).

### 3. Preconditions

| Precondition | What it gives this story |
|---|---|
| RWB-P6-E2021-CON | The published notice contract this slice is tested against: notice `N-0101` for case `RC-2026-000321` with notice type `DEMAND` and template `DEMAND-SSME` `TH` version 1 Approved, the dispatch read that returns barcode `RR223344556TH` with sent date 2026-12-15, the proof read with the result `DELIVERED`, `REFUSED`, `UNDELIVERABLE` or no proof inside the 7-day window, and the states `Held`, `Sent`, `Delivered` and `Unserved`, with its contract fakes. The request and answer shape of the authorise call itself is Not specified in the source documents (GAP-0946; ASM-1673) |
| Permission matrix `PM-2026.12` `IN_FORCE` | The rows this slice answers from, loaded by the policy pack path (RWB-P4-AD002-APP, RWB-P4-AD004-APP): `LITIGATION` `C` and `R` for `RW-LITOFF`, `LITIGATION` `CRU` for `RW-ENFORCE`, `LITIGATION` `R` for `RW-CASEOWN`, `RW-LEGAL` and `RW-HEADLIT`, every area `R` for `RW-AUDIT` with scope `ALL`, and no `LITIGATION` row for `RW-PHONECOL`, `RW-TEAMMGR` or `RW-PLATADM`. The TSD P4 matrix carries no Litigation column, so these letters are the assumption (GAP-0945; ASM-1672) |
| Masking version `MASK-SIT-01` in force | The rows for `DF-PTY-007` and `DF-PTY-016` covering `RW-LITOFF`, `RW-ENFORCE`, `RW-CASEOWN`, `RW-LEGAL`, `RW-HEADLIT` and the service identity that runs JOB-10 with `unmasked` false, so the addressee postal address and the party field are masked for every role that reaches the notice panel, and no row at all for a field outside the pack, which stays masked by default. The version label is assumed for SIT (GAP-0947; ASM-1674) |
| Test users in SIT | The litigation user reference `LIT-0101` holds `RW-LITOFF` (legacy AC10, AC11); `U-4101` holds `RW-CASEOWN`, `U-4103` holds `RW-TEAMMGR`, `U-4104` holds `RW-PLATADM` and `U-4106` holds only `RW-PHONECOL` (FSD P4 v3 A2.7 and A2.8) |
| The decision-record library and its topic | `rwb.decision-record.v1` and the local library of DP-03, so an access entry is written, chained and published in one transaction with the answer |
| gateway-bff composite route | The route of DP-19 that carries the screen's authorise, permission and masking calls to this base path, with the 2 s timeout of DP-11 |
| The ledger append of `rwb-source-data` (RWB-P1-E1066-CON) | `POST /api/recovery/source-data/v1/cases/{caseId}/interactions` checks Case record C of the caller's token before it appends. For a proof of delivery the one caller is `rwb-comms` (RD-P1-007 rules 5 and 7; RD-P1-064 rule 6). This slice answers no `CASE_RECORD` right and does not seed that row. The service-identity row "Case record C on rwb-source-data" for the `rwb-comms` workload identity is added to Users Roles and Permissions v6 and Role to System Access Matrix v4 (RD-P1-064 rule 2; NEW-GAP-F10-01 closed) |

Business preconditions carried from RWB-E2-021:

- The dispatch-eligible notice state is `APPROVED` (legacy `rwb.comms.dispatch.eligible-states`), the proof window is 7 days (R-LIT-08) and the statutory notice types are a reference list (LOV-NOTICE). All three are `rwb-comms`'s data and none of them changes the access answer.
- A notice carries no amount limit and no approval level from the delegation of authority applies to it; notice approval is RWB-E2-014, and the D7.1 approval of the same legacy family is RWB-P4-E2014-APP. No `delegation_limit` row is read on this path.
- Every refusal is answered with MSG-P4-002 naming the action and the capability area and carries no notice content (FSD P4 v3 A2.4 VR-P4-004-1). An object outside the caller's scope is answered with MSG-P4-003 (FSD P4 v3 A2.14 VR-P4-014-1, and legacy AC11 answers status 404).

### 4. Flow

1. Litigation officer (`LIT-0101`): requests a notice for case `RC-2026-000321` with notice type `DEMAND` through the P6 route `POST /cases/{caseId}/notices`; the composite route calls this service first with capability area `LITIGATION`, right `C`, the case as the object reference and the field list the panel will render.
2. `AuthoriseService`: reads the caller's permission rows for `LITIGATION` from `permission` in `rwb_access` under the matrix version in force, unions the letters of every role the caller holds, and answers `allowed` with right `C`, the roles that carry it, `matrixVersion` `PM-2026.12` and `maskingVersion` `MASK-SIT-01`.
3. The request itself is `rwb-comms`'s: the notice is created and reaches state Approved through RWB-E2-014. On this path this story writes an entry only when it refuses, which is an `AC-DENY` entry with the area, the right and the case reference.
4. JOB-10 at 16:00 (`rwb-comms` with `rwb-integration`): before it selects an Approved notice for the WIN file, its conduct check reads the notice and its case through RWB-P6-E2021-CON. That read is authorised by this service for the service identity that runs JOB-10, with area `LITIGATION`, right `R` and the notice and the case as the object reference.
5. `AuthoriseService` for the service identity: the role class is `NON_HUMAN_ACTOR` and the scope `ALL`, and the same checks apply as for a person (NFR-051). The answer is `allowed` with right `R`, the role it was taken from, `PM-2026.12` and `MASK-SIT-01`.
6. `AccessLogWriter`, in the same transaction as the answer of step 5: writes the decision-record entry of DP-03 with decision code `AC-READ`, the service identity as the actor, notice `N-0101`, case `RC-2026-000321`, area `LITIGATION`, right `R`, both policy versions and the field markers `DF-PTY-007` and `DF-PTY-016` marked masked, with no value of the address; publishes `rwb.decision.DecisionRecorded.v1` on `rwb.decision-record.v1` through the outbox.
7. `MaskingPolicyService`, for the same field list under the mask version in force: answers masked for the roles that reach the panel. Where no row covers a field for any of the caller's roles the answer is masked as well, so the default is refuse rather than show (FSD P4 v3 A2.5, AC-EXC-P4-004-05). No value of the address is read, echoed or cached by this service.
8. Litigation officer: reads the notice, its dispatch and its proof through the P6 read `GET /notices/{noticeId}` and on SCR-18. The composite route calls this service with right `R` for the same object and the panel's field list; the answer is served and one `AC-READ` entry is written per open, exactly as in step 6, and the panel renders the two fields masked with the mask version beside them.
9. SCR-04 Case timeline: the officer sees each ledger entry with its conduct check result. The timeline read is a case-record read and its entry is the timeline story's; this slice supplies only the `LITIGATION` `R` answer behind the dispatch and proof block. The delivery entry on that timeline is the one `rwb-comms` appends with `POST /api/recovery/source-data/v1/cases/{caseId}/interactions` (`eventCode` `LETTER`, with `deliveryStatus` and `externalRef` = the notice's WIN `barcode` of the row, else its `noticeRef`) once it has matched a row of the proof-of-delivery read; the read itself appends nothing (RD-P1-007 rule 7 as amended by RD-P1-064 rule 4).
10. A role without the right (`U-4101` holding `RW-CASEOWN` for the request, `U-4104` and `U-4106` for the read): the answer is refused with 403 and MSG-P4-002 for the action "request a notice" or "read a notice", and one `AC-DENY` entry is written with the actor, the area, the right and the object reference only.
11. A notice outside the caller's scope (`N-0200`): the answer is refused with 404 and MSG-P4-003, the shape legacy AC11 gives, and carries no case data, no notice field, no delivery status and no address value; one `AC-DENY` entry records the reason code.
12. A policy pack load by the service's own administration path commits new `permission` or `masking_rule` rows and writes the outbox row for `rwb.access.AccessPolicyChanged.v1` with the new matrix or masking version; the load itself is RWB-P4-AD002-APP and RWB-P4-AD004-APP.
13. The cache-refresh listener of this service reads that event from `rwb.access.events.v1` and replaces the cached answer for the affected roles; the next authorise call answers with the new version pair and a new mask answer, with no deployment and no restart, and the answer never mixes a matrix version with a mask version from a different policy load.

Every answer and its entry commit in one transaction (DP-03, R-UNI-39), so a call that cannot be logged is refused rather than answered (FSD P4 v3 AC-EXC-P4-007-03), and a repeated call with the same `Idempotency-Key` returns the first answer without a second entry.

### 5. Exception paths

| ID | Trigger | What happens | Message | Covered by |
|---|---|---|---|---|
| X1 | The caller holds no `LITIGATION` row at all | Refused with 403; one `AC-DENY` entry with area `LITIGATION` and the right asked; nothing shown | MSG-P4-002 | AC2, AC9 |
| X2 | The caller holds `LITIGATION` `R` and asks for right `C`, or holds `C` and asks for `R` | Refused with 403 for the named action; one `AC-DENY` entry with the right asked; the notice is unchanged | MSG-P4-002 | AC2 |
| X3 | The notice belongs to a case outside the caller's scope | Refused with 404 and no case data; one `AC-DENY` entry with the reason code and the object reference | MSG-P4-003 | AC4 |
| X4 | No masking row covers the field for any of the caller's roles | The field is answered masked under the mask version in force; the entry marks it masked; no value is read | None | AC6 |
| X5 | The notice is held or unserved by the conduct check of `rwb-comms` | The access answer is unchanged and the entry carries no hold reason and no delivery result | None (the notice messages are `rwb-comms`'s) | AC7 |
| X6 | A matrix version and a mask version arrive from two different policy loads, or the policy event does not parse | The cache refuses the mixed pair, keeps the versions it already holds and raises the mismatch; the caller gets the older consistent pair | None | AC8 |
| X7 | The decision record of the access entry cannot be written | The call returns 503, no answer and no data; the reason is logged; the cache is unchanged | MSG-P7-003 | AC10 |
| X8 | A second call arrives with the same `Idempotency-Key` | The first answer and its entry are returned; no second entry is written | None | AC11, AC12 |

An answer is never served without its entry and never without naming both policy versions; a call whose entry fails is an error, not a silent success. No exception path of this story changes a notice, a case or a task: those are `rwb-comms`'s and `rwb-case`'s.

### 6. INVEST check

| Test | Result |
|---|---|
| Independent | Builds against the published notice contract RWB-P6-E2021-CON and its fake; the notice content, the dispatch and the proof arrive in the request or in the fake, never as a table read |
| Negotiable | Letters, roles, areas, scopes, masking rows, mask formats and versions are data; the story fixes the answer shape and the entry only |
| Valuable | The notice cannot be requested or read without a current authorise answer, and the addressee's name and address never leave the owning service or enter a log |
| Estimable | Three endpoints, one cache, one masking answer, one entry writer, two index migrations |
| Small | Fits one week with its tests, because the notice, the dispatch, the proof, the ledger and the screens are other stories' |
| Testable | Every criterion below is one test case in section 16; the notice and dispatch facts are returned by the contract fake |

### 7. Acceptance criteria

```gherkin
Feature: Access decisions and access-log entries for the WIN letter dispatch loop

  Background:
    Given the environment is SIT
    Given permission matrix version "PM-2026.12" is in force and masking version "MASK-SIT-01" is in force
    Given test user "U-4101" holds RW-CASEOWN, test user "U-4103" holds RW-TEAMMGR, test user "U-4104" holds RW-PLATADM, test user "U-4106" holds RW-PHONECOL and the litigation user reference "LIT-0101" holds RW-LITOFF
    Given the rwb-comms contract mock returns notice "N-0101" for case "RC-2026-000321" with notice type "DEMAND" and template "DEMAND-SSME" "TH" version 1 Approved
    Given the rwb-comms contract mock returns the dispatch read of 2026-12-14 with barcode "RR223344556TH" and sent date 2026-12-15

  Scenario: AC1 Requesting a notice reads LITIGATION C from the matrix in force (new, D-RCV-60)
    Given the rwb-comms contract mock returns notice "N-0101" for case "RC-2026-000321" in state "Approved"
    When "LIT-0101" requests the notice and the composite route calls POST /api/recovery/access/v1/authorise with area "LITIGATION", right "C", case "RC-2026-000321" and the field list "DF-PTY-007", "DF-PTY-016"
    Then the answer is allowed with area "LITIGATION", right "C", the role "RW-LITOFF", matrix version "PM-2026.12" and masking version "MASK-SIT-01"
    Then the answer carries no value of the addressee address, no notice field and no template content
    Then no "AC-DENY" entry is written for that action and the notice itself is "rwb-comms"'s

  Scenario: AC2 A role without the Litigation letter is refused the request (new, D-RCV-60)
    Given test user "U-4101" holds RW-CASEOWN and no permission row of RW-CASEOWN holds the letter "C" for area "LITIGATION" under "PM-2026.12"
    When "U-4101" requests a notice for case "RC-2026-000321" and the route asks area "LITIGATION", right "C"
    Then the call is refused with status 403 and message MSG-P4-002 for the action "request a notice"
    Then one access-log entry exists with decision code "AC-DENY", actor "U-4101", area "LITIGATION", right "C" and case "RC-2026-000321"
    Then the entry holds no notice id, no template code and no value of the addressee address

  Scenario: AC3 Reading a notice, its dispatch and its proof reads LITIGATION R and keeps both fields masked (new, D-RCV-60)
    Given the rwb-comms contract mock returns notice "N-0101" for case "RC-2026-000321" in state "Sent" with barcode "RR223344556TH" and sent date 2026-12-15
    When "LIT-0101" opens SCR-18 and the composite route calls POST /api/recovery/access/v1/authorise with area "LITIGATION", right "R", notice "N-0101" and the field list "DF-PTY-007", "DF-PTY-016"
    Then the answer is allowed with area "LITIGATION", right "R", the role "RW-LITOFF", matrix version "PM-2026.12" and masking version "MASK-SIT-01"
    Then the answer marks "DF-PTY-007" and "DF-PTY-016" masked and carries no value of the addressee address
    Then one access-log entry exists with decision code "AC-READ", actor "LIT-0101", notice "N-0101", case "RC-2026-000321", area "LITIGATION", right "R" and the two field markers as masked
    Then the entry holds no addressee name, no postal address value and no template content

  Scenario: AC4 A notice outside the caller's scope is answered with MSG-P4-003 (new, D-RCV-60)
    Given notice "N-0200" belongs to a case outside the scope of "LIT-0101"
    When "LIT-0101" sends GET /notices/N-0200 and the composite route asks area "LITIGATION", right "R" for notice "N-0200"
    Then the call is refused with status 404 and message MSG-P4-003
    Then one access-log entry exists with decision code "AC-DENY", actor "LIT-0101", area "LITIGATION", right "R" and notice "N-0200"
    Then the answer holds no case number, no notice field, no delivery status, no barcode and no value of the addressee address

  Scenario: AC5 The service identity that runs JOB-10 gets the same checks (new, D-RCV-60)
    Given the role of the service identity that runs JOB-10 has role class "NON_HUMAN_ACTOR" and scope "ALL"
    When at 16:00 on 2026-12-14 the conduct check of JOB-10 asks for area "LITIGATION" and right "R" on notice "N-0101" of case "RC-2026-000321"
    Then the answer is allowed with right "R", role class "NON_HUMAN_ACTOR", scope "ALL", matrix version "PM-2026.12" and masking version "MASK-SIT-01"
    Then one access-log entry exists with the service identity as the actor, notice "N-0101", case "RC-2026-000321", area "LITIGATION" and the two field markers as masked
    Then the entry differs from a person's entry in the actor reference only and holds no value of the addressee address

  Scenario: AC6 A personal field with no masking row is masked by default (new, D-RCV-60)
    Given no masking row in "MASK-SIT-01" covers a field outside the policy pack for any role
    When "U-4103" asks GET /api/recovery/access/v1/masking-policies for that field
    Then the answer is masked under masking version "MASK-SIT-01"
    Then the answer carries no value and no format of the field

  Scenario: AC7 The conduct-check facts never change the access answer (new, D-RCV-60)
    Given case "RC-2026-000321" has an open deviation "X1" with contact stop on and a legal hold true, and template "DEMAND-SSME" "TH" version 1 was withdrawn on 2026-12-13
    When "LIT-0101" opens notice "N-0101" on SCR-18 at 16:00 on 2026-12-14 and the route asks area "LITIGATION", right "R"
    Then the answer is allowed and identical to the answer for a case with no stop, no hold and an Approved template, with matrix version "PM-2026.12" and masking version "MASK-SIT-01"
    Then the answer and the entry name no hold reason, no contact stop and no template state
    Then MSG-P6-001, MSG-P3-004 and MSG-P6-003 are produced by "rwb-comms" on its own path and this service produces none of them

  Scenario: AC8 A policy change reaches the cached answer with no deployment (new, D-RCV-60)
    Given the cached answer for "LIT-0101" holds masking version "MASK-SIT-01"
    When the policy pack load commits a masking row set under a masking version later than "MASK-SIT-01" and publishes rwb.access.AccessPolicyChanged.v1
    Then the next authorise call for "LIT-0101" answers with the later masking version and the mask answer of that version
    Then no deployment, restart or cache flush is performed and the matrix version in the answer stays "PM-2026.12"
    Then the answer never pairs the new masking version with a matrix version from a different load

  Scenario: AC9 A refusal names the action and the area and carries no notice content (new, D-RCV-60)
    Given the rwb-comms contract mock returns notice "N-0101" for case "RC-2026-000321" in state "Unserved" with the result "UNDELIVERABLE"
    When "U-4104" asks the authorise path for area "LITIGATION" and right "R" on notice "N-0101"
    Then the problem response names the action "read a notice" and the area "LITIGATION" and its messageId is MSG-P4-002
    Then the problem response holds no notice field, no case number, no delivery status, no barcode and no value of the addressee address
    Then the "AC-DENY" entry holds the actor, the area, the right and the notice reference only

  Scenario: AC10 A read that cannot be logged is refused and not answered (new, D-RCV-60)
    Given the decision-record write of the access entry is forced to fail
    When "LIT-0101" opens notice "N-0101" on SCR-18 and the route asks area "LITIGATION" and right "R"
    Then the call returns status 503 with message MSG-P7-003 and no answer
    Then the answer carries no field marker and no case or notice data
    Then no "AC-READ" entry exists for that call, the cache is unchanged and the notice is unchanged because its state is "rwb-comms"'s

  Scenario: AC11 A second call with the same Idempotency-Key returns the first answer and writes no second entry (new, D-RCV-60)
    Given "LIT-0101" has already received an allowed answer for notice "N-0101" under an Idempotency-Key
    When "LIT-0101" sends the same authorise call again with the same Idempotency-Key and area "LITIGATION" and right "R" on notice "N-0101"
    Then the first answer and its entry are returned unchanged and the idempotency_key row holds the stored answer
    Then no second "AC-READ" entry is written for that call

  Scenario: AC12 A repeated write with the same Idempotency-Key leaves one entry for that key (new, D-RCV-60)
    Given "LIT-0101" has already received an allowed answer for notice "N-0101" under an Idempotency-Key
    When "LIT-0101" repeats the authorise call with the same Idempotency-Key and the same body
    Then the first answer is returned unchanged and exactly one "AC-READ" entry exists for that key
    Then the repeated call writes no second "AC-READ" entry

  Scenario: AC13 The right, the mask default, the service identity and the version pair are read from data and never fixed in code (new, D-RCV-60)
    Given the permission rows of matrix version "PM-2026.12" and the masking rows of "MASK-SIT-01" are in force
    When the authorise path decides area "LITIGATION" with right "R" on notice "N-0101" for an actor with role class "NON_HUMAN_ACTOR" and scope "ALL" and a field with no masking row
    Then the right is the letter read from the permission row of the matrix version in force and the field is masked
    Then the service identity passes through the same role and scope checks as a person and the answer names matrix version "PM-2026.12" and masking version "MASK-SIT-01"
    Then the code holds no enum of areas, roles or letters, as shown by the boundary check of the build

  Scenario: AC14 A call with no valid session is refused with status 401 (new, D-RCV-60)
    Given "LIT-0101" holds no valid session
    When "LIT-0101" sends POST /api/recovery/access/v1/authorise with area "LITIGATION", right "R" and notice "N-0101"
    Then the call is refused with status 401 and no answer
    Then the answer carries no decision, no field marker and no case or notice data

  Scenario: AC15 A replayed refusal with the same Idempotency-Key returns the stored first answer (new, D-RCV-60)
    Given "U-4101" has already been refused a notice for case "RC-2026-000321" under an Idempotency-Key with area "LITIGATION" and right "C"
    When "U-4101" replays the same authorise call with the same Idempotency-Key
    Then the first refusal is returned unchanged and the idempotency_key row holds the stored answer
    Then no second "AC-DENY" entry is written for that call
```

The fifteen criteria above are the ones this story owns; the legacy AC1 to AC12 and the legacy test cases are carried by `rwb-comms` (RWB-P6-E2021-APP), by `rwb-source-data` (the ledger store and the proof read, which writes nothing; RD-P1-007) and by `rwb-decision` (the D7.1 entry), and the legacy test set is kept in section 16 against this slice's assertions. The authorise request and response shape used above — actor, roles, area, right, object reference and field list in, and allowed, roles, area, right, scope, matrix version, masking version, field markers and messageId out — is Not specified in the source documents (GAP-0946; ASM-1673).

### 8. Business rules

| ID | Rule | Source |
|---|---|---|
| BR1 | A right is taken from the permission rows of the matrix version in force, per role and capability area, with letters C, R, U, D and A; no letter, role or area is written in code | FSD P4 v3 A2.4; BR-P4-004; TSD P4 v3 T6.1 |
| BR2 | Requesting a notice needs `LITIGATION` `C`; reading the notice, its dispatch and its proof needs `LITIGATION` `R` | Legacy RWB-E2-021 section 10; FSD P4 v3 A2.4; TSD P4 v3 T3.2 LOV-CAPABILITY |
| BR3 | A role with no `LITIGATION` row is denied; the authorise path refuses by default and never falls back to a broader role or to a default letter | FSD P4 v3 A2.4 AC-EXC-P4-004-06; Architecture v5, deny by default |
| BR4 | A notice outside the caller's scope is answered with MSG-P4-003 and no case data; the scope is the role's default scope or the narrower scope the session resolved, from OWN, TEAM, REGION and ALL | FSD P4 v3 A2.14 VR-P4-014-1 and AC-EXC-P4-004-01; TSD P4 v3 T3.2 LOV-SCOPE |
| BR5 | A personal field is shown masked unless a masking row for the role and the field says unmasked, and a field with no covering row stays masked | FSD P4 v3 A2.5 AC-EXC-P4-004-05; BR-P4-005 |
| BR6 | A service identity is subject to the same role and scope checks as a person, and none of its answers is a bypass | NFR-051; TSD P4 v3 T6.2 |
| BR7 | Every allowed read of a notice writes one `AC-READ` entry and every refusal one `AC-DENY` entry, in one transaction with the answer; a call that cannot be logged is refused | FSD P4 v3 A2.7 AC-P4-007-01 and A2.8; DP-03; R-UNI-39 |
| BR8 | The entry carries the notice and case references, the field IDs and a masked marker, never a value; the addressee's name and address never reach an entry, an event or a log | Legacy RWB-E2-021 section 17; NFR-042; TSD P4 v3 T7 |
| BR9 | The access answer depends on the rights, the scope and the policy versions only; the conduct result, the contact stop, the legal hold, the template state, the delivery result and the proof window are `rwb-comms`'s checks and never change the answer | Legacy RWB-E2-021 BR1 to BR10 and section 5; FSD P4 v3 A2.4 VR-P4-004-1 |
| BR10 | An answer names the matrix version and the masking version it was decided under, and a policy change reaches the cached answer through `rwb.access.AccessPolicyChanged.v1` with no deployment | FSD P4 v3 A2.4 AC-P4-004-01; Architecture v5 slide 42 |

Coverage of BR1, BR5, BR6 and BR10 by the criteria of section 7: BR1 by AC1, BR5 by AC6, BR6 by AC5 and BR10 by AC8. AC13 is also the boundary criterion for BR1, BR5, BR6 and BR10.

Target-service statements that make the rules hold in `rwb-access`:

- BR1 is a read of `permission` in `rwb_access` under the matrix version in force; the capability areas are the LOV-CAPABILITY values read through the reference-data contract of DP-07, and the Java code holds no enum of areas, roles or letters.
- BR2 and BR3 are one check on the letter of the requested right in the area `LITIGATION`: `C` on the request of a notice and `R` on the read of a notice, its dispatch and its proof. A missing row is a refusal, never a default.
- BR4 is a scope predicate on the object reference the caller sends: the answer names the scope that was applied, and a notice outside it is a 404 with MSG-P4-003 and no case data, so the refusal cannot be used to test whether a notice exists.
- BR5 is the `masking_rule` read plus the default; the mask format is the one masking library every screen uses, because no source fixes a rendering for a postal address (GAP-0947; ASM-1674).
- BR6 is the `role_class` and `default_scope` read of the identity's role: `NON_HUMAN_ACTOR` with scope `ALL` passes through exactly the same check as a person's role, and the entry names the identity instead of a user reference.
- BR7 is one `RecordAndApply` transaction on the answer and the entry, with the idempotency key of DP-09.
- BR8 is a check on the entry writer: the field list it writes is the field ID and the masked flag, and a test asserts the entry text holds no part of the synthetic address.
- BR9 is the absence of any notice business field in the authorise request except the object reference and the field list: no conduct result, no hold reason, no template state and no delivery result is sent, so no check here can disagree with `rwb-comms`.
- BR10 is the version pair in the answer and the cache refresh on the service's own `AccessPolicyChanged`.

### 9. State transitions

| From | Event | Condition | To |
|---|---|---|---|
| No cached answer | Authorise call | The policy rows are in force | Allowed or denied, with the matrix and masking versions |
| Allowed | The answer is served | The `AC-READ` entry commits | Served, with the field markers and the scope |
| Denied | The refusal is served | The `AC-DENY` entry commits | Refused with 403 and MSG-P4-002, or 404 and MSG-P4-003 for a scope miss |
| Cached under `PM-2026.12` / `MASK-SIT-01` | `rwb.access.AccessPolicyChanged.v1` | A later policy load is in force | Cached under the new versions, served from the next call |
| Cached, mixed versions | Refresh | The event names a matrix version and a masking version from different loads | Unchanged, with the mismatch raised |

The notice states the answer gates but does not set, carried from legacy RWB-E2-021 section 9 and owned by `rwb-comms`:

| From | Event | Condition | To |
|---|---|---|---|
| `Approved` | JOB-10 runs and the conduct check passes | WIN acknowledges the file record | `Sent`, with the barcode `RR223344556TH` |
| `Approved` | JOB-10 runs and the conduct check blocks | A legal hold, a contact stop or a withdrawn template | `Held`, with the hold reason |
| `Sent` | The proof read returns `DELIVERED` | The result is inside the 7-day window | `Delivered`, with the callback date |
| `Sent` | The proof read returns `REFUSED` or `UNDELIVERABLE`, or the window expires | No proof inside the window | `Unserved` |

This story reads those states through RWB-P6-E2021-CON and changes none of them. Access entries have no lifecycle of their own: they are append-only and are read by `rwb-decision`'s decision-log query and by the access audit query of FSD P4 v3 A2.16.

### 10. Authority

| Who | What they may do in this story |
|---|---|
| RW-LITOFF Litigation officer | Requests a notice (`LITIGATION` C) and reads it with its dispatch and its proof (`LITIGATION` R) |
| RW-ENFORCE Enforcement owner | Requests and reads a notice (`LITIGATION` CRU) |
| RW-CASEOWN Case owner | Reads the notice of a case in its scope (`LITIGATION` R) and receives the unserved case in its queue; it may not request a notice |
| RW-LEGAL Legal counsel | Reads the notice, its dispatch and its proof (`LITIGATION` R) |
| RW-HEADLIT Head of Litigation | Reads the notice, its dispatch and its proof (`LITIGATION` R) |
| RW-AUDIT Internal audit | Reads the access and decision entries with scope `ALL`, and the policy versions they were decided under |
| RW-CONDUCT Conduct and QA officer | Reads blocked contacts on the ledger under a Case record right, which is answered for the case record and is not this story's `LITIGATION` answer |
| The service identity that runs JOB-10 | Reads the notice and its case before the conduct check selects it (`LITIGATION` R), with role class `NON_HUMAN_ACTOR` and scope `ALL`, under the same checks as a person (NFR-051) |
| SY-DECLOG, decision log writer | The service identity that writes the `AC-READ` and `AC-DENY` entries through the library |
| RW-PHONECOL, RW-TEAMMGR, RW-PLATADM and every role with no `LITIGATION` row | Refused by default, with an `AC-DENY` entry |

No approval level from the delegation of authority applies in this story, and no `delegation_limit` row is read: a notice carries no amount limit, notice approval is RWB-E2-014, and the D7.1 approval path is RWB-P4-E2014-APP. The role code of the service identity that runs JOB-10 is Not specified in the source documents (GAP-0948; ASM-1675).

### 11. Data

| BR Field ID | Table in `rwb_access` | Field | Read or write |
|---|---|---|---|
| DF-REF-034 to DF-REF-039 | `role` | role_code, role_name, role_class, default_scope | Read |
| DF-REF-040 to DF-REF-044 | `permission` | role_id, capability_area, letters, matrix_version | Read |
| DF-REF-198 to DF-REF-204 | `masking_rule` | role_code, field_id, unmasked, masking_version, valid_from, valid_to | Read |
| DF-REF-205 to DF-REF-211 | `role_conflict` | role_code, conflicts_with, conflict_version | Read, only to report a conflicting pair to the session that asks for permissions |
| DF-PTY-007, DF-PTY-016 | `contact_point` and the party record (owned by P1, read through the owner's contract of DP-05) | the party field and the addressee postal address over `v_ace_contact.contact_value` | Not read as values: the answer names the field and the masked marker only |
| DF-LEG-015, DF-LEG-016, DF-LEG-018, DF-LEG-019, DF-LEG-020 | `notice` (owned by P6) | id, case_id, notice_type, sent_date, barcode | Not read from the table: the values arrive in the object reference and in the contract fake |
| DF-DEC-001 to DF-DEC-018 | decision record (local library, DP-03) | the `AC-READ` or `AC-DENY` entry: decision code, actor, object reference, area, right, versions, field markers, time | Write |
| (inbox) | `processed_event` | event_id, consumer, processed_at | Write |
| (outbox) | outbox library table in `rwb_access` | the `AccessPolicyChanged` row and the record row | Write |
| (idempotency) | `idempotency_key` | the stored answer of an authorise call with its key | Write |

No `delegation_limit` row is read on this path: a notice carries no amount limit and the scope and the right, not a holder, are the check. The field IDs of the addressee's postal address and of the party field on the notice panel and their masked rendering are Not specified in the source documents (GAP-0947; ASM-1674); this story names `DF-PTY-016` for the postal address and `DF-PTY-007` for the second personal field of the same record, both marked masked on the case record view by FSD P4 v3 A2.7 AC-P4-007-01, and leaves the format to the one masking library every screen uses. Field IDs are those in the Logical Data Model and Data Dictionary v9.

### 12. Contract

#### 12.1 REST operations provided

None new. The decision is served through the operations of RWB-P4-E1037-CON on base `/api/recovery/access/v1`, owner P4 `rwb-access`; this slice adds no path, no query parameter and no response field, and decides the following behind them:

| Method | Path | Purpose | Authorization | Errors |
|---|---|---|---|---|
| POST | `/api/recovery/access/v1/authorise` | The role, scope and right decision for one capability area and right on a notice or a case, with the field markers | The caller's own session; the answer is the decision; `Idempotency-Key` header, a repeated key returns the first answer (TC-P4-E2021-APP-10) | 401; 403 MSG-P4-002; 404 MSG-P4-003; 422; 503 MSG-P7-003 |
| GET | `/api/recovery/access/v1/me/permissions` | The caller's resolved roles, letters per capability area, scope, matrix version and masking version | None beyond the session | 401; 503 |
| GET | `/api/recovery/access/v1/masking-policies` | The masking answer for a field and a role, with the mask version | None beyond the session | 401; 503 |

Architecture v5 slide 14 names `POST /authorise`, `GET /me/permissions`, `GET /doa-limits` and `/masking-policies`. The DoA operation is not used by this story, because a notice carries no amount limit. TSD P4 v3 names `GET /me/session` (API-P4-012) for the same resolved view, so the resolved view is answered behind `GET /me/permissions` under R-PREC and the session read keeps its own story and its own shape. The request and response shape of `POST /authorise` is Not specified in the source documents (GAP-0946; ASM-1673).

#### 12.2 REST operations consumed

None. The notice, its dispatch, its proof and the case facts are sent in the authorise request by the composite route and by `rwb-comms`, and the notice contract RWB-P6-E2021-CON is exercised by the contract fake; this service calls no other service on this path, so the call stays one hop with the 2 s timeout of DP-11 and a circuit breaker. In particular it calls neither the proof-of-delivery read nor the ledger append of `rwb-source-data`, and it reads and writes no freshness stamp (RD-P1-007, RD-P1-041).

#### 12.3 Events published

| Event | Topic | Owner | Key | Payload |
|---|---|---|---|---|
| `rwb.access.AccessPolicyChanged.v1` | `rwb.access.events.v1` | P4 `rwb-access` | matrix or mask version | the policy kind, the old and new version, validFrom, the affected capability areas or fields, the load reference |
| `rwb.decision.DecisionRecorded.v1` (EV-08) | `rwb.decision-record.v1` | PLT library; consumed by P7 | the entry ID | the hash-chained `AC-READ` or `AC-DENY` entry of DP-03 |

CloudEvents 1.0 envelope; neither payload carries personal data, and neither carries a notice field, a delivery result or a value of the addressee's address. `AccessPolicyChanged` is written by the policy load path of this service (RWB-P4-AD002-APP, RWB-P4-AD004-APP) in the same transaction as the rows, and this story's part is the refresh it triggers. `DoaLimitChanged` belongs to the delegation path and is not published by this story.

#### 12.4 Events consumed

None from another service. The cache refresh reads this service's own `rwb.access.AccessPolicyChanged.v1` from `rwb.access.events.v1` through an internal listener, which is not a cross-service subscription; no `rwb.comms.*`, `rwb.case.*` or `rwb.decision.*` event is read, so the dispatch and the proof reach this slice only through RWB-P6-E2021-CON. The refresh fails closed: a policy event that does not parse leaves the cache on the versions it already holds (X6).

#### 12.5 Workflows and activities

None. This story starts no workflow and registers no activity; the notice dispatch loop is `rwb-comms`'s `NoticeDispatchWorkflow` and JOB-10, and the case is `CaseWorkflow` in `rwb-case`.

#### 12.6 Schedules

None for this story. JOB-10 (WIN notices, daily 16:00) is `rwb-comms`'s with `rwb-integration` (Architecture v5 slide 44) and is not a Schedule of this service; the six-monthly access review list (JOB-18) is a Temporal Schedule of this service and belongs to its own story. The authorise path has no clock.

#### 12.7 Tables owned

| Table | Owner | Use in this story |
|---|---|---|
| `role` | P4 (`rwb_access`) | The roles the caller holds, their class and their default scope |
| `permission` | P4 (`rwb_access`) | The letters per capability area under the matrix version in force |
| `masking_rule` | P4 (`rwb_access`) | The unmasked flag per role and field under the mask version in force |
| `role_conflict` | P4 (`rwb_access`) | The conflicting pair reported to a session that asks for permissions |
| `delegation_limit` | P4 (`rwb_access`) | Not read here; a notice carries no amount limit |
| `outbox_event`, `processed_event`, `idempotency_key` | PLT library, created in `rwb_access` | Outbox, inbox and idempotency objects (DP-09) |

`notice`, `template`, `contact_point`, `recovery_case` and `decision_log_entry` are other services' and are not read: the field is named, the value stays with `rwb-source-data`, the notice and its states stay with `rwb-comms`, and the decision ledger entry is written through the library (DP-01).

#### 12.8 Contract fakes

| Fake | Serves | Stubs used by this story |
|---|---|---|
| rwb-comms notice WireMock | RWB-P6-E2021-CON | Notice `N-0101` for case `RC-2026-000321` with notice type `DEMAND` and template `DEMAND-SSME` `TH` version 1 Approved; barcode `RR223344556TH` with sent date 2026-12-15; the proofs `DELIVERED`, `REFUSED`, `UNDELIVERABLE` and no proof inside the 7-day window; the states `Held`, `Sent`, `Delivered` and `Unserved`; notice `N-0200` outside the caller's scope |
| decision-record fake | RWB-PLT-E1027-CON | The entry write and the publish on `rwb.decision-record.v1`, including a forced failure for X7 |
| guard and permission fakes | RWB-PLT-E1037-CON and RWB-P4-E1037-CON | The guard library that carries the answer to the caller, and this service's own authorise contract behind the three operations of 12.1 |
| reference-data fake | RWB-P3-E1043-CON | LOV-CAPABILITY (the area `LITIGATION`), LOV-SCOPE (OWN, TEAM, REGION, ALL) and LOV-NOTICE (the notice types, including `DEMAND` and `RECALL`) |
| gateway-bff route fake | RWB-PLT-N001-CON | The composite route behind SCR-18 and SCR-04, so the screen's own calls can be asserted |
| policy pack fixture | this story's own test data | The `PM-2026.12` permission rows and the `MASK-SIT-01` masking rows for `DF-PTY-007` and `DF-PTY-016`, and a later masking version for AC8 |

#### 12.9 Call-type summary

| Call type | Count in this story | Detail |
|---|---|---|
| REST | Provided 0 new (3 existing operations used), consumed 0 | The decisions are served on `/authorise`, `/me/permissions` and `/masking-policies` of RWB-P4-E1037-CON on `/api/recovery/access/v1` |
| Kafka | Published 2, consumed 0 from other services | `rwb.access.events.v1` and `rwb.decision-record.v1` published; the cache refresh reads this service's own topic |
| Temporal | 0 | No workflow, no activity, no task queue use; JOB-10 and its Schedule are `rwb-comms`'s |
| File | None | No file input or output; the WIN file and the INT-15 proof file are `rwb-comms`'s and ACE's |

### 13. Solution plan

**Package.** `th.co.scb.ace.workbench.recovery.access`, module `access/authorise`, Java package `th.co.scb.ace.workbench.recovery.access.authorise`.

**Pattern application**

| DP | Legacy marker | Microservice pattern | Dependency added |
|---|---|---|---|
| DP-01 | `recovery.<table>` or "recovery schema" | Owner's schema `rwb_<name>`; never read another service's tables | none |
| DP-03 | DecisionLogWriter, decision log | Local decision-record library and topic `rwb.decision-record.v1` | H RWB-PLT-E1027-CON |
| DP-05 | AceSourceQuery, `v_ace_*`, account_ext | Read through rwb-source-data's contract or the service's own ACE views | none |
| DP-07 | Reference data, LOV | Reference-data contract of rwb-case | H RWB-PLT-E1043-CON; C RWB-P3-E1043-CON |
| DP-09 | Application event, EV-nn, outbox | Outbox and inbox library; Kafka topic of the owner; CloudEvents | H RWB-PLT-TE006-CON |
| DP-10 | Quartz, JOB-nn | Temporal Schedule or event-started workflow through the workflow kit | H RWB-PLT-E1071-CON |
| DP-11 | In-process call, published interface | REST contract with mock; one hop; 2 s timeout | none (C from the legacy dependency) |
| DP-13 | `/api/recovery/v1` | `/api/recovery/<short>/v1` | none |
| DP-18 | Interaction ledger | Ledger owned by rwb-source-data | none |
| DP-19 | Screen, ace-web | gateway-bff composite route | H RWB-PLT-N001-CON |

Which patterns have an instance in this slice: DP-01 is the read of `permission`, `masking_rule` and `role` in `rwb_access`; DP-03 is the `AC-READ` and `AC-DENY` entry; DP-07 is the LOV-CAPABILITY area list, the LOV-SCOPE list and the LOV-NOTICE type list; DP-09 is the outbox, the inbox and the idempotency key; DP-11 is the notice contract with its mock and its 2 s timeout; DP-13 is the base path; DP-19 is the composite route of SCR-18 and SCR-04. DP-05 has an instance only as an absence — this service reads no `v_ace_*` view and names the field, and the value stays with `rwb-source-data`. DP-10 has no instance here: JOB-10 is `rwb-comms`'s and this story starts no Schedule, so the pattern is applied where the job lives and not in this slice.

Which DP work of the legacy key sits with another slice: DP-05 (the `v_ace_pod` proof read) is `rwb-source-data`'s and `rwb-comms`'s route; DP-09 (the outbox and `NoticeDelivered`) is `rwb-comms`'s; DP-10 (JOB-10 as a Schedule or an Airflow-triggered run on `rwb-comms`) is `rwb-comms`'s; DP-18 (the ledger) is `rwb-source-data`'s; DP-19 (SCR-18 and SCR-04) is served through the gateway route, and the screens themselves are the gateway's and the notice stories'. The libraries, the Flyway baseline, the outbox and the gateway route are already build dependencies of the P4 service's own stories — RWB-PLT-E1027-CON, RWB-PLT-E1043-CON, RWB-PLT-TE006-CON, RWB-PLT-E1071-CON, RWB-PLT-N001-CON and RWB-PLT-E1044-CON are pulled by the service baseline and by the policy pack path — so this secondary slice adds no H dependency of its own: metadata H is None, it is Day 1, and it builds against the published contract RWB-P6-E2021-CON.

**Components**

| Component | Type | Responsibility |
|---|---|---|
| AuthoriseController | REST controller | The three operations of 12.1, the problem responses with their message IDs, and the idempotency key |
| AuthoriseService | Service | Resolution of the caller's letters for one area and right, the `C` and `R` check on a notice, the scope predicate and the version pair in the answer |
| ScopeResolver | Service | The scope that applies to the object reference, from OWN, TEAM, REGION and ALL, and the 404 with MSG-P4-003 on a miss |
| MaskingPolicyService | Service | The `masking_rule` read per role and field, the masked default, and the mask version in the answer |
| PolicyVersionResolver | Service | The matrix version and the mask version in force, read once per refresh and held together |
| ServiceIdentityCheck | Service | The `role_class` and `default_scope` read of a service identity's role, so a job is checked like a person and not past the check |
| AccessLogWriter | Service | The `AC-READ` and `AC-DENY` entry of DP-03, with the masked field markers and no value, in the same transaction as the answer |
| PolicyChangeListener | Kafka consumer with the inbox | The service's own `AccessPolicyChanged`, deduplicated by event ID, refreshing the cache |

**Database and migrations**

- Reads `role`, `permission`, `masking_rule` and `role_conflict` in `rwb_access`; writes the decision-record entry through the library, and the inbox, outbox and idempotency rows.
- Index `ix_permission_role_area_version ON permission (role_id, capability_area, matrix_version)`, so the authorise read is one index scan in the cache-miss path.
- Index `ix_masking_field_version ON masking_rule (field_id, masking_version, role_code)`, so the mask answer for a field and a set of roles is one scan.
- No new table and no new column: the policy tables are the policy pack path's, and the access log is the decision-record entry (DP-03). No notice column is added, because the notice is `rwb-comms`'s.
- Migration in the per-service Flyway sequence of DP-15: `V2021_1__access_dispatch_read_indexes.sql`.

**Configuration and reference data**

- LOV-CAPABILITY, LOV-SCOPE and LOV-NOTICE through the reference-data contract of DP-07 (RWB-P3-E1043-CON); the area `LITIGATION` and the notice type `DEMAND` are values of those lists, never constants.
- The matrix version `PM-2026.12` and the masking version `MASK-SIT-01` in force are read from the rows, not configured; the SIT label is assumed (GAP-0947; ASM-1674).
- The access entry's decision codes `AC-READ` and `AC-DENY` follow the codes FSD P4 v3 A2.7 and A2.8 use, and the field markers come from the request (GAP-0946; ASM-1676).
- No switch of this slice's own: a notice that cannot be authorised must not be requested or read, so the authorise path has no off state. The legacy flag `rwb.comms.win-dispatch-loop` stays `rwb-comms`'s and is a legacy reference here.

**Build steps**

1. `AuthoriseController` and the problem responses, with the three operations and the idempotency key; tests for 401, 403, 404 and 503 shapes.
2. `PolicyVersionResolver` and the two index reads; test that a new matrix version is served as data with no code change.
3. `AuthoriseService` for right `C` and right `R` on `LITIGATION`, with the scope predicate; tests for AC1, AC2, AC3 and AC9.
4. `ScopeResolver` with the 404 and MSG-P4-003 and the no-case-data assertion; test for AC4 with notice `N-0200`.
5. `MaskingPolicyService` with the masked default and the mask version in the answer; tests for AC3 and AC6.
6. `ServiceIdentityCheck` with the `NON_HUMAN_ACTOR` and `ALL` read; test for AC5 through the JOB-10 read of the fake.
7. `AccessLogWriter` in the same transaction as the answer, with the masked markers and the no-value assertion; tests for AC3, AC5, AC7, AC9 and AC10.
8. `AuthoriseCache` and `PolicyChangeListener` with the version pair and the mixed-pair refusal; test for AC8 with a fixed clock.
9. The contract-fake run against RWB-P6-E2021-CON and the gateway-bff route fake, so the story builds before `rwb-comms` and the screens exist in the environment.

**Done when.** The tests in section 16 pass; every open of a notice on SCR-18 writes exactly one `AC-READ` entry naming the notice, the case, the actor, the area, the right and `DF-PTY-007` and `DF-PTY-016` as masked, with no name and no value of the address anywhere in the entry; the read the conduct check makes before JOB-10 selects a notice writes the same entry shape for the service identity; every refusal writes one `AC-DENY` entry with its area, right and object reference; every answer names the matrix version and the masking version it was decided under; and a masking policy change is served by the cache after `AccessPolicyChanged` with no deployment.

### 14. Validation and messages

| ID | When | Message | Where it is produced |
|---|---|---|---|
| MSG-P4-002 | The caller's role does not carry the right in the area | You cannot {action} here. Your role does not include it. | This story, on the authorise path |
| MSG-P4-003 | The notice is outside the caller's scope | This case is not in your scope. | This story, when the scope check fails |
| MSG-P7-003 | The access entry cannot be written | The action was not taken because the decision could not be recorded. Try again in a few minutes. | This story, on the entry writer |
| MSG-GEN-001 | A required field of the authorise request is missing | Enter {field}. | This story, on the request validation |
| MSG-P6-001 | A contact stop blocks the letter | Contact with this customer is stopped for {reason}. | `rwb-comms`, never this story |
| MSG-P3-004 | A legal hold or deviation blocks the letter | This case is on hold for {deviation}. The prescription date is still {date}. | `rwb-comms`, never this story |
| MSG-P6-003 | The template was withdrawn before dispatch | The {template} template has been withdrawn. The notice is on hold until Legal approves a new version. | `rwb-comms`, never this story |
| MSG-P6-008 | A notice is refused, undeliverable or has no proof in the window | {notice} for case {case} was not served: {reason}. The case is in your queue to choose another service method. | `rwb-comms`, never this story |

The {action} value in MSG-P4-002 names the action and nothing else — for this notice, "request a notice" or "read a notice" — and the problem response carries the capability area in its `detail` beside the message ID, so a refusal is diagnosable without any notice content. Every error is an RFC 9457 problem response with `messageId` set and `instance` naming the request.

### 15. Screens and states

No screen is built here. The screens are reached through the gateway-bff composite route of DP-19 (RWB-PLT-N001-CON) and drawn by the notice and timeline stories:

| Screen | State | What this story supplies |
|---|---|---|
| SCR-18 Notice approval | Approved, waiting for JOB-10 | The `LITIGATION` `R` answer per notice, and one `AC-READ` entry per open |
| SCR-18 Notice approval | Sent | The masked marker for `DF-PTY-016` and `DF-PTY-007` and the mask version the panel shows beside the field, beside the barcode and the sent date the panel reads from `rwb-comms` |
| SCR-18 Notice approval | Delivered | The same masked markers; the callback date and the notice period end date are `rwb-comms`'s and `rwb-case`'s |
| SCR-18 Notice approval | Unserved | The same masked markers; the result and MSG-P6-008 are `rwb-comms`'s |
| SCR-18 Notice approval | Held | The same masked markers; the hold reason and MSG-P6-001, MSG-P3-004 and MSG-P6-003 are `rwb-comms`'s |
| SCR-04 Case timeline | List | The `LITIGATION` `R` answer behind the dispatch and proof block, and the field markers that keep the addressee's address masked |
| SCR-04 Case timeline | Empty | Not specified in the source documents (CG-ALL-5281) |
| SCR-04 Case timeline | Loading | Not specified in the source documents (CG-ALL-5281) |
| SCR-04 Case timeline | Error | Not specified in the source documents (CG-ALL-5281) |
| SCR-04 Case timeline | No access | Not specified in the source documents (CG-ALL-5281) |
| SCR-18 Notice approval | Denied | The problem response of MSG-P4-002 or MSG-P4-003 with the action and the area, and the `AC-DENY` entry behind it |
| SCR-18 Notice approval | Empty | Not specified in the source documents (CG-ALL-5282) |
| SCR-18 Notice approval | Loading | Not specified in the source documents (CG-ALL-5282) |
| SCR-18 Notice approval | Error | Not specified in the source documents (CG-ALL-5282) |
| SCR-18 Notice approval | No access | Not specified in the source documents (CG-ALL-5282) |

The panel layout, the masked rendering, the field list the composite route carries for SCR-18 and SCR-04, and the request shape behind them are Not specified in the source documents (GAP-0947; ASM-1674); the screen stories are RWB-P6-E2021-APP and the gateway route, and this story changes no screen behaviour.

### 16. Test cases

| TC ID | Covers | Level | Data |
|---|---|---|---|
| TC-P4-E2021-APP-01 | AC1, AC3, BR2 | Contract | `N-0101` Approved for case `RC-2026-000321`; acknowledgment `RR223344556TH` with sent date 2026-12-15; the access answer and the entry are this story's assertion, the dispatch is the P6 fake |
| TC-P4-E2021-APP-02 | AC2 | Contract | The proof read returns `DELIVERED` with call-back `18122026`; the state change is `rwb-comms`'s and the entry names no address |
| TC-P4-E2021-APP-03 | AC3, AC7, BR9 | Contract | The proof read returns `UNDELIVERABLE`; the notice becomes `Unserved`; the access answer is unchanged |
| TC-P4-E2021-APP-04 | AC4 | Component | Open deviation `X1` with contact stop on; the answer is unchanged and MSG-P6-001 is `rwb-comms`'s |
| TC-P4-E2021-APP-05 | AC5 | Component | Postal contact point consent `WITHDRAWN` and notice type `DEMAND` statutory; the answer is unchanged |
| TC-P4-E2021-APP-06 | AC6 | Contract | `N-0102` sent 2026-12-15 and `N-0103` sent 2026-12-16, JOB-10 on 2026-12-22; MSG-P6-008 is `rwb-comms`'s and the answer is unchanged |
| TC-P4-E2021-APP-07 | AC7, BR9 | Component | Legal hold true on case `RC-2026-000321`; MSG-P3-004 is `rwb-comms`'s and the answer is unchanged |
| TC-P4-E2021-APP-08 | AC8 | Component | Template `DEMAND-SSME` `TH` version 1 withdrawn on 2026-12-13; MSG-P6-003 is `rwb-comms`'s and the answer is unchanged |
| TC-P4-E2021-APP-09 | AC9 | NFR | Open `X2` with contact stop; the decision-record write forced to fail; 503 with MSG-P7-003 and no answer |
| TC-P4-E2021-APP-10 | AC10 | Contract | The request repeated with one `Idempotency-Key`; the first answer is returned and no second entry is written |
| TC-P4-E2021-APP-11 | AC11 | Component | Notice `N-0200` outside the scope of `LIT-0101`; 404 with MSG-P4-003 and no case data |
| TC-P4-E2021-APP-12 | AC12 | Component | The request sent with no notice type; 422 with MSG-GEN-001 naming "notice type", refused before the handler runs |
| TC-E2-021-13 | AC2, AC9, BR2, BR3 | Component | Test user `U-4101` holding `RW-CASEOWN` requests a notice for `RC-2026-000321`; refused with MSG-P4-002 and one `AC-DENY` entry |
| TC-E2-021-14 | AC10, BR7, BR8 | NFR | The decision-record write forced to fail on 10 unserved results; no answer is served and no notice changes |
| TC-E2-021-15 | AC5 | Component | Service identity running JOB-10 with role class `NON_HUMAN_ACTOR` and scope `ALL`; `N-0101` of case `RC-2026-000321` at 16:00 on a date Not specified in the source documents (CG-ALL-5278); the answer and the entry are this story's assertion, the job is `rwb-comms`'s |
| TC-E2-021-16 | AC6 | Component | Field with no masking row in `MASK-SIT-01`; `U-4103` asks GET /api/recovery/access/v1/masking-policies for it; the answer is masked with no value and no format |
| TC-E2-021-17 | AC8 | Component | Cached answer for `LIT-0101` holds `MASK-SIT-01`; a later masking version is committed and `rwb.access.AccessPolicyChanged.v1` is published; the next authorise call answers with the later version and the matrix version stays `PM-2026.12` |
| TC-E2-021-18 | AC12, BR7 | Contract | The request repeated with one `Idempotency-Key` and the same body; the first answer is returned and exactly one `AC-READ` entry exists for that key |
| TC-E2-021-19 | AC13, BR1, BR5, BR6, BR10 | Component | Permission rows of `PM-2026.12` and masking rows of `MASK-SIT-01` in force; service identity with role class `NON_HUMAN_ACTOR` and scope `ALL`; a field with no masking row; the right, the mask and the version pair come from the data |
| TC-E2-021-20 | AC14 | Component | `LIT-0101` sends the authorise call with no valid session; 401 and no answer |
| TC-E2-021-21 | AC15, BR7 | Contract | Refused call of `U-4101` for case `RC-2026-000321` replayed with one `Idempotency-Key`; the first refusal is returned and no second `AC-DENY` entry is written |
| TC-E2-021-22 | Not specified in the source documents (ASM-3438) | Component | Not specified in the source documents (ASM-3438) |

The legacy level System maps to Contract or Component as the row shows, Access to Component and Resilience to NFR, and each case asserts only this slice's answer and entry; the rule that lives in `rwb-comms` is exercised at Level Contract through RWB-P6-E2021-CON and its fake. No case ID with the `-ITG` suffix is used here: the integration copy of the set belongs to the integration harness of this legacy key, which proves the same facts across `rwb-access`, `rwb-comms`, `rwb-source-data` and `rwb-case` with real services. The full test, with its Given, When and Then, is in Recovery Workbench Test Cases v9.xlsx, tab Story test cases, under the same test case ID.

Version 3: rows that cite `TC-P4-E2021-APP-` identifiers are this story's rows of Recovery Workbench Test Cases v9. Where a shared legacy identifier now names another story's case there, this story's identifier replaces it, and cases run by one identifier are joined in one row.

### 17. Guardrails

- No business value in code: the letters C, R, U, D and A, the capability areas, the roles, the scopes, the notice types, the masking rows and the matrix and mask versions are data rows; the Java code holds no letter, area, role, notice type or version literal (BR-P4-004, BR-P4-005).
- No personal data in logs, events, tests, workflow history or prompts: the access entry carries the actor reference, the notice and case references, the field IDs and a masked marker. Workflow history is not used because this story starts no workflow.
- No addressee name or address in an entry, an event or a log: the value is read through `rwb-source-data`'s contract by whoever displays it, this service answers the field ID and the masked flag only, and a test scans the entry text for any part of the synthetic address.
- ACE data only through the owner's contract or a `v_ace_*` view of this service; this story reads no ACE view at all, and the notice reaches it only through RWB-P6-E2021-CON.
- No business rule executed here: the conduct check, the contact stop, the legal hold, the template state, the consent rule, the proof window and the notice state are `rwb-comms`'s; this story answers the right, the scope and the mask, and a change of any business rule changes no line of it.
- No read of another service's tables and no cross-schema read (DP-01): `notice`, `template`, `recovery_case`, `contact_point`, `interaction` and `decision_log_entry` are never queried here.
- An answer is never served without its entry, and the answer and the entry commit in one transaction (R-UNI-39).
- The cache fails closed: an unparseable or mixed policy event leaves the versions in force, and a missing policy row is a refusal, never a default allow.
- The authorise path has no off switch, because a notice that cannot be authorised must not be requested or read; the legacy dispatch flag stays `rwb-comms`'s.

### 18. Traceability

| Requirement ID | Requirement (short) | BRD section | Feature | L3 process | Rules | Test cases |
|---|---|---|---|---|---|---|
| REQ-OCC-003 | Letters dispatched for print and post, proof of delivery returns | Business Requirements Epic 2, sections 3.6 and 4 | FEAT-OCC-02 | 13 Manage documents and correspondence | R-LIT-07, R-LIT-08, R-LIT-09 | TC-P4-E2021-APP-01, TC-P4-E2021-APP-02, TC-P4-E2021-APP-03, TC-P4-E2021-APP-06, TC-P4-E2021-APP-10, TC-E2-021-11, TC-E2-021-12 |
| REQ-OCC-005 | Every outbound contact carries a conduct check result | Business Requirements Epic 2, sections 3.6 and 4 | FEAT-OCC-05, FEAT-OCC-06 | 16 Manage risk, control and compliance | R-LIT-05, R-UNI-20, R-LIT-04, R-UNI-39 | TC-P4-E2021-APP-04, TC-P4-E2021-APP-07, TC-P4-E2021-APP-08, TC-P4-E2021-APP-09, TC-E2-021-14 |
| REQ-OCC-006 | Withdrawn consent stops the channel; statutory notices continue | Business Requirements Epic 2, sections 3.6 and 4 | FEAT-OCC-05 | 16 Manage risk, control and compliance | R-UNI-10 | TC-P4-E2021-APP-05 |
| REQ-ILG-010 | Dispatch results, including proof of delivery, written to the ledger | Business Requirements Epic 2, section 4 | FEAT-ILG-07 | 06 to 10 Recovery case processes | R-LIT-07, R-LIT-09 | TC-P4-E2021-APP-01, TC-P4-E2021-APP-02, TC-P4-E2021-APP-03, TC-E2-021-13 |

| Legacy reference | Where it is kept |
|---|---|
| Roles RW-LITOFF with Litigation C and R, RW-ENFORCE with CRU, and the reader roles with Litigation R | Metadata, sections 3, 7, 8, 10 |
| The conduct check, the WIN file, the proof read of `v_ace_pod` and the notice period, held by `rwb-comms` | Sections 1, 4, 7, 12, 19 |
| Notices `N-0101`, `N-0102`, `N-0103`, `N-0200`, cases `RC-2026-000321`, `RC-2026-000654`, `RC-2026-000655`, barcode `RR223344556TH`, template `DEMAND-SSME` `TH` version 1 | Background, AC1 to AC5, AC7, AC9, sections 3, 12.8, 16 |
| `LIT-0101` and the SIT test users `U-4101` to `U-4106` | Background, AC1 to AC4, AC9, section 3 |
| Matrix version `PM-2026.12` and masking version `MASK-SIT-01` | Sections 1, 3, 7, 9, 11, 13 |
| MSG-P4-002, MSG-P4-003, MSG-P7-003, MSG-GEN-001, MSG-P6-001, MSG-P6-003, MSG-P6-008, MSG-P3-004 | Section 14, exception paths |
| Masked addressee address and party field on the panel, and no name or address in the entry | Sections 4, 7, 11, 15, 17 |
| Controls CTL-15 and CTL-16, and NFR-042 and NFR-051 | Sections 2, 8, 17 |
| Legacy test set TC-E2-021-01 to TC-E2-021-14 | Section 16 |
| Legacy key RWB-E2-021, story RWB-P4-E2021-APP, contract RWB-P6-E2021-CON | Metadata, sections 3, 12 |

### 19. Out of scope

- The `rwb-comms` slice of this legacy key, RWB-P6-E2021-APP with RWB-P6-E2021-CON: the request and read of a notice, the WIN file, the conduct check, the proof read of `v_ace_pod`, the notice states `Held`, `Sent`, `Delivered` and `Unserved`, the `NoticeDispatched` and `NoticeDelivered` events, MSG-P6-001, MSG-P6-003, MSG-P6-008 and MSG-P3-004, and JOB-10 itself.
- The ledger entry of a dispatch and of a proof, which `rwb-source-data` stores under DP-18 and which `rwb-comms` appends over REST for a proof of delivery (RD-P1-007), and the decision entry of a held or unserved notice, which is `rwb-decision`'s under RWB-P4-E2014-APP and the D7.1 path.
- The notice approval of RWB-E2-014 and the access slice of its approval screen, RWB-P4-E2014-APP; the alternates service methods of R-LIT-10 and R-LIT-11 (Epic 5); SMS and LINE dispatch (RWB-E2-022).
- The policy pack load path of this service — the reference loads, their approval, verification and rollback, and the rows of `PM-2026.12` and `MASK-SIT-01` themselves (RWB-P4-AD002-APP, RWB-P4-AD004-APP).
- The delegation of authority table and its lookup (RWB-P4-E2013-APP), role, scope and sign-in administration, break-glass, and the six-monthly access review list (JOB-18).
- The screens SCR-18 and SCR-04 themselves, and the composite route's field list for them, which are the gateway-bff and the notice stories' (DP-19).
- The case facts, the case state, the owner queue and the transfer with reason `NOTICE_UNSERVED` (`rwb-case`, RWB-P3-E2021-APP), and the case timeline read.
- The integration harness of this legacy key and its `-ITG` copies of the test cases.
- The Helm chart, the Kafka subscription values, the metrics, the alerts and the runbook of the authorise path (an OPS story of this legacy key).

### 20. Remaining delivery steps

- Size the story at refinement (squad).
- Load the Case record C service-identity row of the `rwb-comms` workload identity from Users Roles and Permissions v6 (security administrator; RD-P1-064).
- RWB-P1-E1066-CON and RWB-P6-E2021-CON Done with published fakes and fixed versions (contract owners).
- Load the test data in SIT (test lead).

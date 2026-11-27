# RWB-P7-E2019-APP Partner identities through the external gateway

SCB Collections and Recovery. Henka Group, 22 November 2026.
(C) Siam Commercial Bank and Henka Pte Ltd

| Item | Value |
|---|---|
| Story key | RWB-P7-E2019-APP |
| Work type | APP (App development) |
| Suggested owner | TechX (suggested; any team may pick up this story) |
| Service | rwb-decision |
| Service epic | RWB-SVC-P7 |
| Wave | 2 |
| Business epic | EP02 |
| Release | 31 December 2026 (tentative) |
| Legacy key | RWB-E2-019 |
| Legacy disposition | Split (rework) |
| Build status | Not started |
| Patterns applied | DP01, DP03, DP05, DP06, DP07, DP08, DP11, DP13, DP15, DP19 |
| Parallel lane | L-P7-AB |
| Ready to start | Day 1 |
| Depends on (build) | None |
| Contract dependencies | RWB-P4-E2019-CON |
| Integration dependencies | None |
| External dependencies | None |
| PRD reference | 03 Requirements and specifications/PRD/Recovery Workbench PRD P7 rwb-decision v1.md (no FR mapped to REQ-ACA-012) |
| Status | Draft (realignment v1) |

**Change log.** D-RCV-60, 22 November 2026: split from RWB-E2-019 for rwb-decision — the partner access decision record in the central ledger, one chained appended entry per partner sign-in and per partner-role or firm change that rwb-access decides, plus the two decision-log reads filtered to partner access entries. Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

**Change log.** D-RCV-60, 26 November 2026: fixes from the deterministic build-readiness checks (X20 RWB-P7-E2019-APP). Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

### 1. Story

As an **agency manager (RW-AGENCYMG)** and an **internal audit reader (RW-AUDIT)**, I want **the partner access decision of every partner sign-in and of every partner-role or firm change recorded once in the central decision ledger of `rwb-decision` — one chained, append-only `decision_log_entry` carrying the partner firm reference, the partner role, the scope reference, the external gateway identity reference, the result and the refusal reason code, under the service identity and an idempotency key — with the two decision-log reads filtered to partner access entries**, so that **a firm that leaves the panel, an identity with no binding and a bank identity on the partner route all leave one entry that cannot be quietly changed, the agency manager and an auditor can read one entry and the entries of a firm in a date range, and no access answer stands where its record could not be appended**.

Inside `rwb-decision` this is the decision-record slice of the legacy story RWB-E2-019:

- Service `rwb-decision`, schema `rwb_decision`, REST base `/api/recovery/decision/v1`, topic `rwb.decision.events.v1` with event names `rwb.decision.<Event>.v1`, Temporal task queue `rwb-decision` in namespace `rwb-recovery`, Java package `th.co.scb.ace.workbench.recovery.decision`, and the shared topic `rwb.decision-record.v1` through the decision-record path of DP-03.
- One deliverable and nothing else: the partner access decision record, appended here through the decision-record path of DP-03 from the record that `rwb-access` publishes on the shared topic `rwb.decision-record.v1` — a library call inside the caller's transaction at `rwb-access`, not a REST operation of this service — hash chained and append only, with the partner firm reference, the partner role, the scope reference of type `PLACED`, the external gateway identity reference, the result, the reason code where the answer was refused, the requesting actor as the service identity `SY-DECLOG` and the record's idempotency key; plus the two reads so the agency manager and an auditor can read one entry and the entries of a firm in a date range.
- What stays with `rwb-access` (P4, RWB-P4-E2019-CON and RWB-P4-E2019-APP, RWB-P4-E1037-APP, RWB-P4-AD001-APP): the sign-in, the multi-factor authentication, the token, the resolve operation, the partner identity and its binding to one firm and one role, the partner role rows, the matrix and masking versions, firm scope on instructions, revocation and the same-day loss of access, and the access answer itself; the authorise call and the guard library are consumed through their contracts and fakes (DP-08, DP-11) and are not rebuilt here.
- What stays with `rwb-partner` (S9, RWB-S9-E2019-APP): `partner`, `partner_user` and `partner_instruction`, the panel, the panel status and contract end, the binding rows and the partner portal, with the partner gateway in the DMZ and `gateway-bff` under RWB-PLT-N007-INF and RWB-PLT-N001-CON; this story reads no S9 table, because the firm reference, the role code and the gateway identity reference arrive as fields of the record (DP-01). What stays with RWB-P4-E1039-APP is the general access log, the break-glass grant and the access-log read.
- The record and the access answer are one pair under DP-03: the decision is `rwb-access`'s and the record is this service's. A record that cannot be appended refuses the access answer — MSG-P7-003, no session, an incident under R-UNI-39 — and an entry is never appended for an answer that was not given. Where the sources read the append path differently the conflict is GAP-1273 and the reading applied is ASM-2241.
- The service records and exposes the decision; it holds no partner identity, token, session, role row, permission row or partner table, and answers no access question of its own (BR9). The database login is the per-service login of DP-02, whose name is Not specified in the source documents (GAP-1272; ASM-2243).

The legacy behaviour carried into the decision service is unchanged in meaning: one entry per partner access decision, the partner role and the firm of the session on that entry, refusal reasons that name why access ended, and no access answer without its record (legacy RWB-E2-019 AC1, AC3, AC4, AC9 and BR5).

### 2. Business rationale

Partners reach the Workbench only through the partner gateway in the DMZ (Architecture v5 slides 20 and 35), and `rwb-access` answers what a partner identity may do: one partner role, a `PLACED` scope carrying the firm, and the matrix and masking versions in force. That answer is a decision about access to bank data, and the legacy story already demanded a record of it — an `AC-SIGN` entry when a partner signs in, an `AC-DENY` entry with its reason when the firm is suspended, exited or past its contract end, when the identity has no active binding, and when a bank identity tries the partner route.

In the monolith the access module wrote those entries into the one decision log inside its own process, so the answer and the record could not drift apart. In the target the decision is `rwb-access`'s and the ledger is `rwb-decision`'s (slides 14, 28 and 41), so the record has to be appended in `rwb_decision`, chained and unchangeable, and read back by the agency manager who owns the panel relationship and by the auditor who later asks which firm could see what and from when. The realignment changes the mechanism, not the business rule:

1. The in-process decision-log write becomes the decision-record path of DP-03: `rwb-access` writes the partner access record through the library inside its own transaction, the library's outbox publishes `rwb.decision-record.DecisionRecorded.v1` on `rwb.decision-record.v1`, and this service consumes that fact and appends one entry, deduplicated by the record's idempotency key (slides 28 and 42, event 08).
2. The entry names the firm reference, the partner role, the scope reference, the gateway identity reference, the decision code, the result and the reason code; the firm's name, the person at the firm, the business e-mail, the instruction and the token stay with `rwb-partner` and the gateway (BR5, BR12).
3. The decision codes `AC-SIGN` and `AC-DENY` are values of LOV-DECISION read through the reference-data contract of `rwb-case` (DP-07), never literals (BR8); the partner role, the firm status, the binding and the scope stay their owners' and this story reads none of their tables (DP-01, DP-11).
4. The one decision-log read of the monolith becomes two operations on the service's own base (DP-13), and the data-lake copy of the log is retired with the data lake (DP-17) while JOB-13 stays continuous Kafka and JOB-14 keeps checking the chain at 02:00.
5. The entry is append only and hash chained, so a refused answer leaves no entry, a repeated record leaves one entry, and a break in the chain is a reportable event rather than a silent edit.

This story meets REQ-ACA-012 on the record side: it proves who could reach the Workbench from outside the bank, on which firm and which partner role, and that the answer is recorded before the session is used; and it carries control CTL-11 and the principle that no action proceeds unlogged (CTL-06, R-UNI-39). It puts the partner-access half of REQ-DRI-001, REQ-DRI-002, REQ-DRI-003, REQ-DRI-005 and REQ-DRI-012 in place and leaves the identity, the binding, the firm, the token, the access answer and the general access log where their owners have them. The values the criteria use are the legacy values unchanged: partner identities `P-5101`, `P-5102` and `P-5103`, test user `U-5105`, firms `LF-0012`, `LF-0019` and `VL-0004`, partner roles `PT-LAWFIRM`, `PT-VALUER` and `PT-AGENCY`, instruction `INS-2027-000431`, scope `PLACED`, matrix version `PM-2026.11`, masking version `MASK-SIT-01`, the refusal reasons `PARTNER_NOT_ACTIVE`, `NO_PARTNER_BINDING` and `BANK_IDENTITY_ON_PARTNER_ROUTE`, and the messages MSG-P4-001, MSG-P4-002, MSG-P4-003 and MSG-P4-008.

### 3. Preconditions

| Precondition | What it gives this story |
|---|---|
| RWB-P4-E2019-CON | The published contract of `rwb-access`: the resolve operation, the claim set, the answer with the roles, the `PLACED` scope and the two versions, the refusal vocabulary with its reasons (`BANK_IDENTITY_ON_PARTNER_ROUTE`, `NO_PARTNER_BINDING`, `ROLE_CONFLICT`, `PARTNER_NOT_ACTIVE`) and its fakes. Which fields of the record this service consumes is Not specified in the source documents (GAP-1272; ASM-2237) |
| RWB-PLT-E1027-CON | The decision-record path and the shared topic `rwb.decision-record.v1` (DP-03): the append, the chain position, the `prev_hash`, the `entry_hash`, the append-only rule and the idempotency key |
| RWB-PLT-E1042-CON, RWB-PLT-E1043-CON, RWB-P3-E1042-CON, RWB-P3-E1043-CON | The parameters and reference-data client libraries and the `rwb-case` contracts behind them (DP-06, DP-07): the page-size bound of the two reads, whose parameter name is Not specified in the source documents (GAP-1272; ASM-2239), and LOV-DECISION, which holds `AC-SIGN` and `AC-DENY`, at the version in force |
| RWB-PLT-E1037-CON, RWB-P4-E1037-CON | The guard library and the authorise contract of `rwb-access` (DP-08), behind the Decision log right R of the two reads |
| RWB-PLT-E1044-CON | The per-service Flyway sequence of `rwb_decision` (DP-15), in which this story adds two index steps and no table |
| RWB-PLT-N001-CON | The `gateway-bff` composite route (DP-19) through which SCR-38 Decision log query and the auditor's view reach the two reads |
| The `rwb-decision` decision-log store baseline | `decision_log_entry` with the columns of TSD P7 v2 T3.1, the append-only trigger `tr_declog_append_only`, the missing grant for UPDATE and DELETE, the unique key on the idempotency key and JOB-14 at 02:00. The baseline is the service's own earlier work and is in no H row: the dependency is carried in GAP-1273 and ASM-2241 |
| The authorise answer of `rwb-access` (P4) | `POST /api/recovery/access/v1/authorise` (slide 14) for the Decision log right R and the caller's firm or `ALL` scope behind the two reads; consumed, faked and in no C row (GAP-1272; ASM-2245) |

Business preconditions carried from RWB-E2-019: partner identity `P-5101` bound to firm `LF-0012` as a LAW_FIRM with panel status `ACTIVE` and contract end 30 June 2027, `P-5102` bound to `VL-0004` as a VALUER, and `P-5103` in the group of partner role `PT-LAWFIRM` with no active binding; `LF-0012` and `LF-0019` are LAW_FIRMs and `VL-0004` a VALUER, all with panel status `ACTIVE`, and `LF-0012` moves to `EXITED` at 11:00 on 4 January 2027; test user `U-5105` holds RW-LITOFF with a bank identity and is used on the partner route only to prove the refusal record; the partner role rows `PT-AGENCY`, `PT-LAWFIRM`, `PT-VALUER`, `PT-AUCTION`, `PT-BUYER` and `PT-RAMC` are loaded with role class `PARTNER_USER` at matrix version `PM-2026.11` and masking version `MASK-SIT-01` is in force, both `rwb-access`'s rows and named here only as the versions an entry carries; and the record under test is produced by the `rwb-access` contract fake and by the decision-record library fake on `rwb.decision-record.v1`, with the replay of AC9 delivering the same fact twice. No build dependency: Day 1, against RWB-P4-E2019-CON and its fakes.

### 4. Flow

1. A partner user opens the partner portal through the partner gateway in the DMZ and the gateway authenticates the identity with a second factor (`rwb-partner`, S9; RWB-PLT-N007-INF).
2. The gateway calls the resolve operation of `rwb-access` with the claims of the partner identity (RWB-P4-E2019-APP), and `rwb-access` decides: one partner role, a scope descriptor of type `PLACED` with the firm, the matrix version `PM-2026.11`, masking version `MASK-SIT-01`, or a refusal with its reason.
3. In the same transaction as its answer, `rwb-access` writes the partner access record through the decision-record library of DP-03 — a library call inside its own transaction and not a call to this service — with the decision code `AC-SIGN` or `AC-DENY`, the partner firm reference, the partner role, the scope reference `PLACED`, the external gateway identity reference, the result, the reason code where there is one, the claim-set reference with its two versions and the record's idempotency key; when the library cannot append, it hands 503 with MSG-P7-003 back to the caller and the access answer is refused (X2).
4. The library's outbox publishes `rwb.decision-record.DecisionRecorded.v1` on `rwb.decision-record.v1`, and `PartnerAccessRecordListener` reads the fact into the inbox of DP-09, deduplicates by event ID and by the idempotency key (R-UNI-40) and passes it to `PartnerAccessAppendService`, which appends the one entry of the resolution; a repeated delivery returns the first entry's ID (BR7).
5. `PartnerAccessRecordValidator` checks the record before any write: the decision code is a value of LOV-DECISION at the version in force, the result is a value of the service's result set, a refused result carries one of the reason codes, and the firm reference, the role code and the gateway identity reference are present where the legacy story names them. A record that fails is refused with MSG-P7-003, the field is named, and nothing is written (BR11).
6. `PartnerAccessAppendService`, one transaction in `rwb_decision`: takes the next `chain_seq`, computes `prev_hash` from the last entry's `entry_hash` (64 zeros for the first), computes `entry_hash` as the SHA-256 of the canonical form, writes the `decision_log_entry` row with the firm reference, the partner role, the scope reference and the gateway identity reference in `actions`, the claim-set reference and the two versions in `inputs_ref`, `SY-DECLOG` in `actor_user_id` and the idempotency key in `idempotency_key`, then writes the inbox row and the idempotency row. A failed append changes nothing (BR3, BR13).
7. A repeated record with the same idempotency key returns the first entry's ID, adds one to the repeat count for R-UNI-40 and appends nothing (BR7); a second append for the same resolution under a different key is refused with 409 and MSG-GEN-004, so one resolution has one entry (BR6).
8. An agency manager reads the entries of its own firm with `GET /api/recovery/decision/v1/decision-log` by `partnerId`, `decision`, `from`, `to`, `page` and `size`, and an auditor reads the same with scope `ALL`; each row holds `entryId`, `chainSeq`, the decision code, the firm reference, the partner role, the scope reference, the gateway identity reference, the reason code, `decidedAt`, `prevHash` and `entryHash` (BR10).
9. The same reader reads one entry with `GET /api/recovery/decision/v1/decision-log/{entryId}`, with the same fields and the claim-set reference, never a claim value and never a token; a caller without the Decision log right is refused with 403 and MSG-P4-002, and a firm outside its scope with 404 and MSG-P4-003 (BR10).
10. Nothing in this story resolves an identity, opens a session, reads an instruction, mints a token or changes a partner row: the entry is written beside the access answer and the readers keep their own state (BR9). JOB-14 at 02:00 and the daily seal cover these entries like any other and are the baseline's, not rebuilt here.

### 5. Exception paths

| ID | Trigger | What happens | Message | Covered by |
|---|---|---|---|---|
| X1 | The record names no decision code, a code outside LOV-DECISION, or a refused result with no reason code | The append is refused, the field is named, nothing is written and no chain position is used | MSG-P7-003 | AC9, AC10 |
| X2 | The decision log store is unavailable, or the chain position cannot be taken | The decision-record library at `rwb-access` cannot append and hands 503 with MSG-P7-003 back to the caller; the access answer is refused with no session, nothing is written and an incident is raised as in R-UNI-39 | MSG-P7-003 | AC6 |
| X3 | The same fact is redelivered or replayed from `rwb.decision-record.v1` | One entry exists; the inbox dedupe and the idempotency key hold, and the repeat is counted for R-UNI-40 | None | AC9 |
| X4 | A second append arrives for the same resolution under a different idempotency key | The second append is refused and the first entry stands | MSG-GEN-004 | AC9 |
| X5 | A partner-role or firm change is decided for an identity that already has an entry | A new `AC-SIGN` entry is appended beside the earlier one, which keeps its role, its firm and its `decidedAt` | None | AC5 |
| X6 | A correction of an entry is needed | A new entry is appended with `corrects_entry_id` naming it; the corrected entry is unchanged | None | AC10 |
| X7 | An UPDATE or a DELETE is attempted, through the service role or the schema owner | The statement is refused by the missing grant and by `tr_declog_append_only`; the entry is unchanged and the attempt is audited | None | AC10 |
| X8 | The caller holds no Decision log right, or asks for a firm outside its scope | 403 with MSG-P4-002, or 404 with MSG-P4-003; no entry is returned | MSG-P4-002, MSG-P4-003 | AC7 |
| X9 | The reference list or the parameters cannot be read at the version in force | The append or the read is refused rather than assumed and the record is retried; no entry is written from an assumed code or result | MSG-P7-003 | AC10 |
| X10 | The record carries a field this story may not keep: a personal name, a national id number, an e-mail address, a phone number, a token, a session identifier or the claims themselves | The field is rejected before any write, the request is logged with the field name only, and no entry is appended | None | AC8 |

An access answer is only ever recorded beside the decision that caused it: `rwb-access` writes the record through the decision-record path in the transaction of the answer and hands its failure back as 503, and this service appends the ledger entry from the fact in one transaction of its own — the entry, its chain position, its inbox row and its idempotency row — so a session never opens on an unwritten record and a record never exists for an answer that was not given (BR13).

### 6. INVEST check

| Test | Result |
|---|---|
| Independent | Builds against RWB-P4-E2019-CON, the decision-record path of DP-03, the reference-data and parameters libraries and the fakes; no sign-in, identity, binding, firm, token or guard behaviour is rebuilt here |
| Negotiable | The record-path operation, the entry's `actions` and `inputs_ref` composition, the result vocabulary and the query parameters are open until the contract review; the story fixes only the entry, the append-only rule, the chain and the two reads |
| Valuable | Every partner sign-in and every refusal, role change and firm change can be traced to one unchangeable entry, and the agency manager and the auditor can read it |
| Estimable | One listener, one validator, one appender with the chain, one query controller with two operations, two index steps and one fake set |
| Small | Fits one sprint with its tests; it is the decision-record slice of the legacy key |
| Testable | Each of the ten criteria in section 7 runs as one automated test against the contract fakes, with a fixed business date and a fixed chain |

### 7. Acceptance criteria

No legacy acceptance criterion is owned verbatim by this story: `acs` is empty for RWB-E2-019, and every legacy criterion of the key signs an identity in, refuses a session, returns or withholds an instruction, or refuses a bank screen, which belongs to RWB-P4-E2019-APP, RWB-P4-E2019-CON, RWB-S9-E2019-APP or RWB-ITG-E2019-ITG. The ten criteria below are new for the `rwb-decision` slice and test only the partner access entry and its two reads; each keeps the legacy values of RWB-E2-019 — the partner identities, the firms, the partner roles, the scope `PLACED`, the two policy versions, the three refusal reason codes and the messages MSG-P4-001, MSG-P4-002, MSG-P4-003 and MSG-P4-008 — and adds no business value.

```gherkin
Feature: The partner access decision record of rwb-decision

  Background:
    Given the environment is SIT
    Given the rwb-access contract mock returns partner identity "P-5101" resolved against firm "LF-0012" as a LAW_FIRM with panel status "ACTIVE" and contract end 30 June 2027, partner role "PT-LAWFIRM", scope "PLACED", matrix version "PM-2026.11", masking version "MASK-SIT-01" and the result allowed
    Given the rwb-access contract mock returns partner identity "P-5102" resolved against firm "VL-0004" as a VALUER with panel status "ACTIVE" and partner role "PT-VALUER"
    Given the rwb-access contract mock returns partner identity "P-5103" with no active binding
    Given the rwb-access contract mock returns test user "U-5105" holding RW-LITOFF with a bank identity on the partner route
    Given the decision-record library fake returns the append, the chain position, the append-only refusal and a forced failure

  Scenario: AC1 One chained AC-SIGN entry for a partner sign-in (new, D-RCV-60)
    Given the rwb-access contract mock returns the resolution of partner identity "P-5101" bound to firm "LF-0012" with partner role "PT-LAWFIRM", scope "PLACED" and the result allowed, under the resolution's idempotency key
    When this service appends the partner access decision record of that resolution at 09:15 on 4 January 2027
    Then one decision_log_entry exists with decision code "AC-SIGN", actor "SY-DECLOG", partner firm reference "LF-0012", partner role "PT-LAWFIRM", scope reference "PLACED", gateway identity reference "P-5101" and no refusal reason
    Then the entry carries chain_seq 1, the 64-zero prev_hash, an entry_hash equal to the SHA-256 of its canonical form, the idempotency key, the claim-set reference with "PM-2026.11" and "MASK-SIT-01", decidedAt 09:15 on 4 January 2027 and no case id
    Then GET /api/recovery/decision/v1/decision-log/{entryId} returns that entry with the same prevHash and entryHash

  Scenario: AC2 A firm that has left the panel leaves an AC-DENY entry (new, D-RCV-60)
    Given the rwb-access contract mock returns the resolution of partner identity "P-5101" bound to firm "LF-0012" refused with message MSG-P4-008 and reason "PARTNER_NOT_ACTIVE", because "LF-0012" moved to panel status "EXITED" at 11:00 on 4 January 2027
    When this service appends the partner access decision record of that resolution at 11:20
    Then one decision_log_entry exists with decision code "AC-DENY", reason "PARTNER_NOT_ACTIVE", partner firm reference "LF-0012", partner role "PT-LAWFIRM" and gateway identity reference "P-5101"
    Then the refusal stands with no session for "P-5101" at 11:20, the entry carries no partner instruction and no case id, and no incident is raised for the refusal itself

  Scenario: AC3 An identity with no binding leaves an AC-DENY entry with its reason (new, D-RCV-60)
    Given the rwb-access contract mock returns partner identity "P-5103" refused with message MSG-P4-001 and reason "NO_PARTNER_BINDING"
    When this service appends the partner access decision record of that refusal
    Then one decision_log_entry exists with decision code "AC-DENY", reason "NO_PARTNER_BINDING" and gateway identity reference "P-5103", with no partner firm reference and no partner role
    Then the entry carries the entry_hash of the entry before it as its prev_hash, or the 64-zero prev_hash where it is the first entry, and no value is invented for the firm or the role of "P-5103"

  Scenario: AC4 A bank identity on the partner route leaves an AC-DENY entry (new, D-RCV-60)
    Given the rwb-access contract mock returns test user "U-5105" holding RW-LITOFF refused with message MSG-P4-001 and reason "BANK_IDENTITY_ON_PARTNER_ROUTE"
    When this service appends the partner access decision record of that refusal
    Then one decision_log_entry exists with decision code "AC-DENY" and reason "BANK_IDENTITY_ON_PARTNER_ROUTE", carrying the gateway identity reference "U-5105"
    Then no role code "RW-LITOFF" and no role of class "BANK_USER" appears on the entry, and no bank session is opened

  Scenario: AC5 A partner-role and firm change is a new entry, not an edit (new, D-RCV-60)
    Given an AC-SIGN entry of partner identity "P-5102" for firm "VL-0004" with partner role "PT-VALUER" was appended at 10:00 on 3 December 2026
    Given the rwb-access contract mock returns the decision of the partner and agency manager "RW-AGENCYMG" that "P-5102" is bound to firm "LF-0012" with partner role "PT-AGENCY" and the result allowed
    When this service appends the partner access decision record of that change at 10:00 on 4 January 2027
    Then a second entry is appended with decision code "AC-SIGN", partner firm reference "LF-0012" and partner role "PT-AGENCY", and the entry of 3 December 2026 still names "VL-0004" and "PT-VALUER" with its decidedAt unchanged
    Then GET /api/recovery/decision/v1/decision-log?partnerId=LF-0012&from=2026-12-01&to=2027-01-31 returns the entry of 4 January 2027 only, and the same read for "VL-0004" returns the entry of 3 December 2026 only

  Scenario: AC6 A record that cannot be appended refuses the access answer (new, D-RCV-60)
    Given the partner access record path of rwb-access is unavailable and refuses the append at 09:14 on 4 January 2027
    Given the rwb-access contract mock holds the resolution of "P-5101" for firm "LF-0012" with partner role "PT-LAWFIRM" and the result allowed open in that transaction
    When "rwb-access" resolves the partner sign-in of "P-5101"
    Then the resolution answers status 503 with message MSG-P7-003 through the caller, no decision_log_entry exists for the resolution, no chain_seq is consumed and no session is issued for "P-5101"
    Then an incident is raised as in R-UNI-39
    When the same resolution is retried and the record path accepts the append
    Then one entry is appended and it takes the chain_seq the refused append did not use

  Scenario: AC7 The two reads answer one entry and the entries of a firm in a date range (new, D-RCV-60)
    Given the entries of AC1 and AC5 are appended
    Given the rwb-access contract mock returns the authorise answer allowing role RW-AGENCYMG the Decision log right R on firm "LF-0012", and refusing it on firm "VL-0004" with message MSG-P4-003
    When the agency manager reads GET /api/recovery/decision/v1/decision-log/{entryId} of the entry of AC1
    Then the response is 200 with decision code "AC-SIGN", partner firm reference "LF-0012", partner role "PT-LAWFIRM", scope reference "PLACED", gateway identity reference "P-5101", decidedAt, prevHash and entryHash
    When the agency manager reads GET /api/recovery/decision/v1/decision-log?partnerId=LF-0012&from=2026-12-01&to=2027-01-31 with page 1 and the page-size bound in force
    Then the page holds the entries of "LF-0012" in decidedAt order with the total count of the firm and no entry of "VL-0004"
    When the same caller reads GET /api/recovery/decision/v1/decision-log?partnerId=VL-0004
    Then the response is 404 with MSG-P4-003 and no entry of "VL-0004" is returned
    Given the rwb-access contract mock returns MSG-P4-002 for the Decision log right R of a role without it
    When that caller reads GET /api/recovery/decision/v1/decision-log
    Then the response is 403 with MSG-P4-002 and no entry is returned

  Scenario: AC8 The entry carries references and codes and no personal value (new, D-RCV-60)
    Given the rwb-access contract mock returns the resolution of "P-5101" for firm "LF-0012" with partner role "PT-LAWFIRM", the group "RWB-UAT-PT-LAWFIRM" and the result allowed
    When this service appends the partner access decision record
    Then the entry holds the gateway identity reference "P-5101", the firm reference "LF-0012", the role code "PT-LAWFIRM", the scope reference "PLACED", "PM-2026.11", "MASK-SIT-01" and the decision code "AC-SIGN", and nothing else of the caller
    Then the entry, its event payload, its audit line and the test data hold no personal name, no national id number, no e-mail address, no phone number, no bank role code and no Entra group name such as "RWB-UAT-PT-LAWFIRM"

  Scenario: AC9 A repeated record gives one entry and a duplicate is refused (new, D-RCV-60)
    Given the record of the resolution of AC1 was appended and its entry ID returned
    When the same record with the same idempotency key arrives again
    Then one entry exists for the resolution, the first entry ID is returned, the repeat count of R-UNI-40 is raised by one and no second chain position is written
    When a second append for the same resolution arrives under a different idempotency key
    Then the second append is refused with status 409 and message MSG-GEN-004 and the first entry stands

  Scenario: AC10 The ledger is append only and a correction is a new entry (new, D-RCV-60)
    Given an AC-SIGN entry of firm "LF-0012" with no refusal reason and chain_seq 1 is stored
    When an UPDATE setting the refusal reason to "PARTNER_NOT_ACTIVE" and a DELETE of the entry are attempted through the rwb-decision login and again through the schema owner role
    Then all four statements are refused: by the missing grant for the service role, and with "decision_log_entry is append only" from tr_declog_append_only for the schema owner
    Then the entry is unchanged and the refused attempts are written to the ACE audit log with the table, the operation and the entry ID
    When a correction of the entry is taken
    Then a new entry is appended with corrects_entry_id naming it and the corrected entry is still unchanged
```

The ten criteria are new and `acs` is empty for this story: no legacy criterion of RWB-E2-019 is owned verbatim here, because each of them signs an identity in, refuses a session, returns an instruction or refuses a bank screen and belongs to RWB-P4-E2019-APP, RWB-P4-E2019-CON, RWB-S9-E2019-APP or RWB-ITG-E2019-ITG. The values are the legacy values — partner identities `P-5101`, `P-5102` and `P-5103`, test user `U-5105` holding RW-LITOFF, firms `LF-0012`, `LF-0019` and `VL-0004`, partner roles `PT-LAWFIRM`, `PT-VALUER` and `PT-AGENCY`, instruction `INS-2027-000431`, scope `PLACED`, matrix version `PM-2026.11`, masking version `MASK-SIT-01`, panel status `ACTIVE` and `EXITED`, contract end 30 June 2027, the group `RWB-UAT-PT-LAWFIRM`, the decision codes `AC-SIGN` and `AC-DENY`, the reasons `PARTNER_NOT_ACTIVE`, `NO_PARTNER_BINDING` and `BANK_IDENTITY_ON_PARTNER_ROUTE`, and the messages MSG-P4-001, MSG-P4-002, MSG-P4-003, MSG-P4-008, MSG-P7-003 and MSG-GEN-004 — and no new business value is introduced. The record-path operation, the composition of `actions` and `inputs_ref`, the result vocabulary, the query parameters of the two reads, the database login name and the index names have no source and are carried in GAP-1272 with ASM-2236 to ASM-2239, ASM-2243 and ASM-2244; the reading of the append path is carried in GAP-1273 and ASM-2241. The `-ITG` copies of the test cases belong to RWB-ITG-E2019-ITG.

### 8. Business rules

| ID | Rule | Source |
|---|---|---|
| BR1 | One entry per partner access decision: a sign-in that is allowed leaves one `AC-SIGN` entry, and each refusal, partner-role change and firm change leaves one entry of its own | Legacy RWB-E2-019 AC1, AC3, AC4 and AC9; FSD P7 v3 A2.2; REQ-DRI-001 |
| BR2 | The entry carries the decision code `AC-SIGN` or `AC-DENY`, the partner firm reference, the partner role, the scope reference of type `PLACED`, the gateway identity reference, the result, the reason code and the idempotency key | Legacy RWB-E2-019 AC1, AC3, AC4 and AC9; TSD P7 v2 T3.1; ASM-2237 |
| BR3 | Every entry is hash chained: a `chain_seq`, a `prev_hash` equal to the previous `entry_hash` (64 zeros for the first) and an `entry_hash` equal to the SHA-256 of the canonical form; JOB-14 at 02:00 covers it | REQ-DRI-003; FSD P7 v3 AC-ALT-P7-001-01; Architecture v5 slide 28 |
| BR4 | The log is append only: an entry is never changed or deleted, and a correction is a new entry naming the one it corrects in `corrects_entry_id` | REQ-DRI-002; FSD P7 v3 AC-P7-001-01 and A2.1 |
| BR5 | The entry names references and codes only: never a personal name, a national id number, an e-mail address, a phone number, a token, a session identifier or a claim value | Legacy RWB-E2-019 section 17; DF-PTY-007; CTL-11; NFR-040; Architecture v5 slides 30 and 35 |
| BR6 | A decision is recorded whole or not at all: a refused answer leaves no entry, and a second append for the same resolution under a different key is refused | Legacy RWB-E2-019 BR5 and section 5; R-UNI-39 |
| BR7 | One entry under a repeated record: the inbox dedupe and the idempotency key make a second entry impossible, and the repeat is counted for R-UNI-40 | FSD P7 v3 AC-EXC-P7-002-03; R-UNI-40; Architecture v5 slide 42 |
| BR8 | The decision codes are values of LOV-DECISION at the version in force, read through the reference-data contract, never a literal in code | BR-P7-002; TSD P7 v2 T3.2; DP-07; TSD P4 v3 T3.2 |
| BR9 | The story records and exposes; it resolves no identity, opens no session, issues no token, reads no partner row, applies no scope and refuses no access of its own | Architecture v5 slides 14, 20, 35 and 41; DP-01 |
| BR10 | The two reads declare the Decision log right R with the caller's firm or `ALL` scope; a role without it is refused with MSG-P4-002 and a firm outside the scope with MSG-P4-003 | TSD P7 v2 T-A.1, T6.1 and T6.2; REQ-DRI-012; ASM-2245 |
| BR11 | A record that lacks its decision code, its result or, for a refused answer, its reason code is refused with MSG-P7-003 and appends nothing; no entry is written from an assumed value | FSD P7 v3 AC-EXC-P7-002-01, AC-EXC-P7-002-05 and AC-EXC-P7-002-02 read on this slice; REQ-DRI-001 |
| BR12 | No personal data in the entry, the claim-set reference, the event, the audit line, the tests or the logs; such a field is rejected before any write and the log names the field only | Architecture v5 slide 11; NFR-039; NFR-040; legacy RWB-E2-019 section 17 |
| BR13 | The entry, its chain position, its inbox row and its idempotency row commit in one transaction; a failed append leaves nothing and the access answer is refused with MSG-P7-003, no session and an incident under R-UNI-39 | Principle 5; R-UNI-39; FSD P7 v3 A2.5; DP-03 |
| BR14 | The ingest of `rwb.decision-record.v1` is continuous Kafka and the entries reach the ledger inside the completeness target of slide 28, with the chain checked daily and sealed to write-once storage by the baseline | Architecture v5 slides 28 and 44 (JOB-13); TSD P7 v2 T5.3 |
| BR15 | The ledger reads are one hop from the `gateway-bff` composite route and the service reads no table of another service: the firm, the role and the authorise answer arrive on their contracts or as fields of the record | Architecture v5 slides 13 and 41; DP-01; DP-11; DP-19 |

### 9. State transitions

None for a partner user, a firm, a partner role or a session: this story changes none of them, and the resolution answer's own states — resolved, refused, expired — are `rwb-access`'s (RWB-P4-E2019-APP). The states below are the states of an entry, which has no state column of its own: it is appended and then immutable.

| From | Event | Condition | To |
|---|---|---|---|
| Absent | The record of a partner access decision arrives with `AC-SIGN` or `AC-DENY` | The code is in LOV-DECISION, the result is in the service's result set, a refused result carries a reason code, and the chain head is known | Appended at the next `chain_seq`, with its `prev_hash`, `entry_hash`, inbox row and idempotency row in one transaction |
| Absent | The record arrives with a code outside the list, with no result, or with a refused result and no reason | The record fails the check of BR11 | Absent: refused with MSG-P7-003, no chain position used, the record retried |
| Absent | The store or the chain is unavailable | The append cannot commit | Absent: MSG-P7-003, nothing written, the access answer refused and an incident raised |
| Appended | The same record arrives again with the same idempotency key | The inbox or the idempotency key holds the entry | Unchanged: the first entry's ID is returned and the repeat is counted |
| Appended | A second append for the same resolution arrives under a different key | The first entry stands | Unchanged: the second append is refused with MSG-GEN-004 |
| Appended | A partner-role or firm change is decided for the same identity | The change is a new decision | A new entry is appended beside the earlier one, which keeps its role, its firm and its `decidedAt` |
| Appended | A correction is taken, or an UPDATE or a DELETE is attempted | The correction names its entry; any caller may attempt the other two | A correction is appended with `corrects_entry_id`; the UPDATE and the DELETE are refused and the entry stays unchanged |
| Appended | JOB-14 and the daily seal run | The baseline's check and seal | Sealed: the entry is unchanged and the chain is verified |

The partner session moves from resolved to ended when the firm's status or the binding ends, and that is the gateway's act on its next call (RWB-P4-E2019-APP, section 9); this story records the decision that ends it and never ends a session.

### 10. Authority

| Who | What they may do in this story |
|---|---|
| RW-AGENCYMG Partner and agency manager | Reads one entry and the entries of its own firm in a date range (Decision log R, firm scope), and decides a partner-role or firm change whose record this story appends |
| RW-AUDIT Internal audit | Reads the partner access entries of every firm by firm and date range, and one entry with its chain fields (Decision log R, scope ALL); changes nothing |
| RW-COMPLY Compliance and PDPA officer, RW-SECADM Security administrator, and every other role of TSD P7 v2 T6.1 | Read the entries they are scoped to and never a claim value; RW-SECADM also receives the conflict and refusal incidents and maintains the role rows and groups in `rwb-access`, not here |
| A role outside the matrix, or a firm out of the caller's scope | Refused with MSG-P4-002, or 404 with MSG-P4-003 |
| SY-DECLOG Decision log writer | The service identity under which the entry is appended; the append is never a person's act |
| The `rwb-decision` service identity | Reads its own `rwb_decision` rows, appends the entry, its inbox row and its idempotency row (DP-02) |
| `rwb-access` (P4) | Owns the sign-in, the identity, the binding, the roles, the scope, the versions and the answer, and writes the record through the decision-record path of DP-03 in its own transaction; this story holds no authority over any of them |
| `rwb-partner` (S9) | Owns the firm, the panel status, the contract end, the partner user and the instruction; this story names none of their rows |
| No delegation of authority level applies | A partner role, a firm status and a token are not a credit decision, and this story reads no `delegation_limit` row |

The authorisation decision behind the two reads is `rwb-access`'s role, permission and scope data, taken through the authorise answer the service already holds; this story adds no guard of its own and holds no role, permission or delegation row (ASM-2245). The database login is per service (DP-02) and its name is Not specified in the source documents (GAP-1272; ASM-2243); the story refers to "the rwb-decision login (DP-02)".

### 11. Data

| BR Field ID | Entity in `rwb_decision` | Field | Read or write |
|---|---|---|---|
| DF-DEC-001 | `decision_log_entry` | id | Write |
| DF-DEC-002 | `decision_log_entry` | case_id | Not written: a partner access decision belongs to a firm and never to a case (GAP-1272; ASM-2242) |
| DF-DEC-003 | `decision_log_entry` | decision_code (`AC-SIGN` or `AC-DENY`, values of LOV-DECISION) | Write |
| DF-DEC-004, DF-DEC-005 | `decision_log_entry` | rule_id, rule_version | Not written: no rule package fires on a partner access decision; the matrix version is in `inputs_ref` |
| DF-DEC-006, DF-DEC-007 | `decision_log_entry` | model_version, agent_version | Not written: no model and no agent takes part |
| DF-DEC-008 | `decision_log_entry` | inputs_ref (the claim-set reference with matrix version `PM-2026.11` and masking version `MASK-SIT-01`) | Write; the shape of the reference is Not specified in the source documents (GAP-1272; ASM-2240) |
| DF-DEC-009 | `decision_log_entry` | recommendation | Not written: an access decision proposes nothing |
| DF-DEC-010, DF-DEC-011 | `decision_log_entry` | approver_user_id, approval_level | Not written: the role owner's approval happens in the bank identity directory and the binding is `rwb-partner`'s |
| DF-DEC-012 | `decision_log_entry` | final_call (the result, `ALLOWED` or `REFUSED`) | Write; the value set is the service's own vocabulary and has no source (GAP-1272; ASM-2238) |
| DF-DEC-013 | `decision_log_entry` | override_reason | Not written: a partner access decision is not an override |
| DF-DEC-014 | `decision_log_entry` | actions (the partner firm reference, the partner role, the scope reference, the gateway identity reference and the reason code where the answer was refused) | Write; the container is TSD P7 v2 T3.1 and its content for this record is Not specified in the source documents (GAP-1272; ASM-2237) |
| DF-DEC-015 | `decision_log_entry` | outcome | Not written: a partner access decision changes nothing an outcome would name |
| DF-DEC-016, DF-DEC-017, DF-DEC-018 | `decision_log_entry` | decided_at, prev_hash, entry_hash | Write |
| DF-DEC-028 | `decision_log_entry` | chain_seq | Write |
| DF-DEC-029 | `decision_log_entry` | corrects_entry_id | Write on a correction only |
| DF-DEC-030 | `decision_log_entry` | actor_user_id (the service identity `SY-DECLOG`) | Write |
| DF-DEC-031 | `decision_log_entry` | idempotency_key (the resolution's key) | Write |
| DF-PRT-001, DF-PRT-004, DF-PRT-005, DF-PRT-006 | `partner` (S9) | id, partner_type, panel_status, contract_end | Named only, never read: the firm reference and the panel answer arrive on the `rwb-access` answer and as fields of the record |
| DF-REF-035, DF-REF-037, DF-REF-043, DF-REF-044 | `role`, `permission` (P4) | role_code, role_class, letters, matrix_version | Named only, never read: the role code arrives as a field of the record and the matrix version as a version of `inputs_ref` |
| DF-REF-213 to DF-REF-217 | `partner_user` (S9) | identity_ref, partner_id, role_code, valid_from, valid_to | Named only, never read: the gateway identity reference and the binding arrive as fields of the record |
| (reference lists, parameters) | reference data and `parameter_value` (P3) | LOV-DECISION with `AC-SIGN` and `AC-DENY`, and the page-size bound | Read through the contracts of DP-07 and DP-06, never a table |
| (inbox, outbox, idempotency) | `processed_event`, the outbox table of `rwb_decision`, `idempotency_key` | event_id, the outbox row of the append, the resolution's key and the first entry ID | Write |

No row of `partner`, `partner_user`, `partner_instruction`, `role`, `permission`, `masking_rule` or `lov_value` is copied into `rwb_decision`: the firm, the role, the scope and the gateway identity reference arrive as fields of the record, and the instruction, the token and the session never enter it (DP-01). The partner identities `P-5101`, `P-5102` and `P-5103`, test user `U-5105`, the firms `LF-0012`, `LF-0019` and `VL-0004` and instruction `INS-2027-000431` are named in this document as legacy values only and are written in no entry of this story (BR5). Field IDs are those of the Logical Data Model and Data Dictionary v9; the composition of `actions`, the shape of `inputs_ref` and the result vocabulary are the readings of ASM-2237, ASM-2238 and ASM-2240 and are Not specified in the source documents (GAP-1272; ASM-2237).

### 12. Contract

#### 12.1 REST operations provided

Owner `rwb-decision` (P7); base `/api/recovery/decision/v1`. The two decision-log paths are the ones TSD P7 v2 T-A.1 carries (API-P7-006 and API-P7-007) and the Ownership Map gives to P7, and they are the only operations this story provides. The append is the decision-record path of DP-03 and not a REST operation: TSD P7 v2 T-A.1 lists exactly API-P7-001 to API-P7-008 and none of them is a partner access record, so this service adds no API id and no path for it. The shape of a partner access entry and the query filter of the two reads are Not specified in the source documents (GAP-1272; ASM-2236).

| Method | Path | Purpose | Access | Idempotency |
|---|---|---|---|---|
| GET | `/api/recovery/decision/v1/decision-log` | API-P7-006: search the ledger filtered to partner access entries by `partnerId`, `decision`, `from`, `to`, `page` and `size`; 200 with the DecisionLogPage | Decision log, right R, firm or `ALL` scope applied | Not applicable, read only |
| GET | `/api/recovery/decision/v1/decision-log/{entryId}` | API-P7-007: read one partner access entry with its code, firm reference, partner role, scope reference, gateway identity reference, result, reason code, claim-set reference and chain fields; 200 with the DecisionLogEntry | Decision log, right R, firm or `ALL` scope applied | Not applicable, read only |

The DecisionLogEntry body carries `entryId`, `chainSeq`, `decisionCode`, `partnerId`, `partnerRole`, `scopeRef`, `partnerIdentityRef`, `finalCall`, `reasonCode`, `inputsRef`, `decidedAt`, `prevHash`, `entryHash`, `correctsEntryId` and `actorUserId`; the DecisionLogPage body carries `items`, `page`, `size` and `total`. The partner access field names and the query parameters are the reading of ASM-2236, ASM-2237 and ASM-2239. Errors: 401 no session on a read; 403 the role lacks the Decision log right (MSG-P4-002); 404 the entry or the firm is absent or outside the scope (MSG-P4-003); 422 a query value outside its list; 503 the ledger is unavailable. Every error is an RFC 9457 problem response with `messageId` set. API-P7-001 to API-P7-005 and API-P7-008 are operations of the decision centre and belong to the approval and recommendation stories of this service; this story declares none of them.

#### 12.2 REST operations consumed

| Method | Path | Owner | Use in this story |
|---|---|---|---|
| POST | `/api/recovery/access/v1/authorise` | P4 `rwb-access` (slide 14) | The cached role, firm or `ALL` scope and Decision log right R behind the two reads; consumed, faked, one hop with a 2 s timeout and a breaker (DP-11, DP-08), in no C row of this story (GAP-1272; ASM-2245) |
| GET | `/api/recovery/case/v1/admin/lists/{listCode}` | P3 `rwb-case` | LOV-DECISION, which holds `AC-SIGN` and `AC-DENY`, at the version in force (DP-07); faked |
| GET | `/api/recovery/case/v1/admin/parameters` | P3 `rwb-case` | The page-size bound of the two reads (DP-06); faked |

The fakes of this slice stand behind those rows and behind the record under test: the **rwb-access contract fake** (RWB-P4-E2019-CON) poses the resolution, the refusals and the authorise answer, the **decision-record library fake** (RWB-PLT-E1027-CON) supplies the append in the caller's transaction, the chain and the append-only refusal, the **central ledger fake** supplies the ledger reference, the replay of the same fact and the chain head, the **parameters and reference-data fakes** supply the page-size bound and LOV-DECISION, and the **partner gateway claim fake** supplies the claims the record's fields mirror. The record itself arrives on `rwb.decision-record.v1`. The contract dependency recorded on the story is RWB-P4-E2019-CON; the platform and published contracts the DP table adds are listed in section 13 and carried in GAP-1272 with ASM-2236, ASM-2241 and ASM-2245.

#### 12.3 Events published

None. This story publishes no event of its own on `rwb.decision.events.v1`: `ApprovalRequested`, `ApprovalDecided` and `RulePackageInForce` are the three events of the service and belong to the approval and rule-registry stories (slides 14 and 42). The partner access entry is read through 12.1, and `rwb.decision-record.DecisionRecorded.v1` on `rwb.decision-record.v1` is published by the owning service of each decision, which for a partner access decision is `rwb-access`.

#### 12.4 Events consumed

| Event | Topic | Owner | Handler |
|---|---|---|---|
| `rwb.decision-record.DecisionRecorded.v1` (EV-08) | `rwb.decision-record.v1` | P7 ledger and its shared topic; published by `rwb-access` for the partner access decisions | `PartnerAccessRecordListener`: inbox dedupe by event ID and by the idempotency key, then `PartnerAccessAppendService` for the code, the firm reference, the partner role, the scope reference, the gateway identity reference, the result, the reason code and the claim-set reference |

The fact carries IDs, codes and references only; no personal name, national id number, e-mail address, phone number, token or claim value travels on the topic (BR5, BR12). It is the only delivery of a partner access record: the same fact redelivered or replayed is deduplicated by event ID and by the idempotency key, so the ledger holds one entry (GAP-1273; ASM-2241). Which fields of the fact this service requires is Not specified in the source documents (GAP-1272; ASM-2237); the reading applied is that of ASM-2237.

#### 12.5 Workflows and activities

None. The append is a transactional write on the consumer path and not a workflow step; the handler is a Kafka consumer with the inbox of DP-09. This story registers no workflow and no activity on the `rwb-decision` queue and adds none to the workflow kit; the `ApprovalWorkflow` belongs to the approval stories and the chain check to the baseline.

#### 12.6 Schedules

None. The ingest of `rwb.decision-record.v1` is continuous Kafka, as JOB-13 states (slide 44), and JOB-14 at 02:00 and the daily seal are the decision-log baseline's and cover these entries like any other. This story creates no Temporal Schedule and starts nothing on a clock.

#### 12.7 Tables owned

| Table | Owner | Use in this story |
|---|---|---|
| `decision_log_entry` | P7 (`rwb_decision`) | The partner access entry with its firm reference, partner role, scope reference, gateway identity reference, result, reason code, claim-set reference and chain position; append only |
| `approval` | P7 (`rwb_decision`) | Not read and not written here: no approval is routed for a partner access decision |
| `rule_package`, `rule_package_version`, `rule_row`, `rule_test_case` | P7 (`rwb_decision`) | Not read: the partner access decision evaluates no rule package |
| decision record (local library) | P7 rows in `rwb_decision`, written through the decision-record path | The append of DP-03 and its hash chain |
| `outbox_event`, `processed_event`, `idempotency_key` | PLT library, created in `rwb_decision` | Outbox, inbox and idempotency objects (DP-09) |

Not owned and never read: `partner`, `partner_user` and `partner_instruction` (S9), `role`, `permission`, `masking_rule` and `delegation_limit` (P4), `recovery_case`, `lov_value`, `reference_row` and `parameter_value` (P3). No foreign key crosses a schema (DP-01).

#### 12.8 Contract fakes

| Fake | Serves | Stubs used by this story |
|---|---|---|
| rwb-access contract fake | RWB-P4-E2019-CON | The resolution of `P-5101` for `LF-0012` with `PT-LAWFIRM`, scope `PLACED`, `PM-2026.11` and `MASK-SIT-01` and the result allowed; the resolution of `P-5102` for `VL-0004` with `PT-VALUER`; the refusal of `P-5101` with MSG-P4-008 and reason `PARTNER_NOT_ACTIVE`; the refusal of `P-5103` with MSG-P4-001 and reason `NO_PARTNER_BINDING`; the refusal of `U-5105` with reason `BANK_IDENTITY_ON_PARTNER_ROUTE`; the change of `P-5102` to `LF-0012` and `PT-AGENCY`; the authorise answers for RW-AGENCYMG and RW-AUDIT, MSG-P4-002 for a role without the right and MSG-P4-003 for a firm outside the scope |
| decision-record library fake | RWB-PLT-E1027-CON | The append, the next `chain_seq`, the `prev_hash`, the `entry_hash` over the canonical form, the append-only refusal, the idempotency key and a forced failure for AC6 |
| central ledger fake | The ledger side of `rwb.decision-record.v1` | The ledger reference of the entry, the replay of the same fact, the duplicate append of AC9 and the chain head AC10 asserts against |
| Parameters fake (P3) | `GET /admin/parameters` | The page-size bound at version PAR-2026.11 |
| Reference-data fake (P3) | `GET /admin/lists/{listCode}` | LOV-DECISION with `AC-SIGN` and `AC-DENY` at version REF-2026.11 |
| Partner gateway claim fake | The claims the record's fields mirror | The gateway identity reference `P-5101`, the firm `LF-0012`, the partner role `PT-LAWFIRM`, the group `RWB-UAT-PT-LAWFIRM` and `amr` holding `pwd` and `mfa` |

Each fake is replaced by the real service as its own story lands, without a change to the scenarios.

#### 12.9 Call-type summary

| Call type | Count in this story | Detail |
|---|---|---|
| REST | Provided 2, consumed 3 | The two decision-log reads provided; the authorise answer and the two `rwb-case` reads consumed, one hop and 2 s with a breaker per downstream. The append is the decision-record path of DP-03 and is declared in no row of this table |
| Kafka | Published 0, consumed 1 | `rwb.decision-record.v1` consumed; no event published on `rwb.decision.events.v1` and no new topic |
| Temporal | None | No workflow, no activity and no Schedule; task queue `rwb-decision` in namespace `rwb-recovery` carries only other stories' work |
| File | None | No file input and no file output; no claim value and no token ever leaves the caller |

### 13. Solution plan

**Package.** `th.co.scb.ace.workbench.recovery.decision`, module `log/partner-access`, Java package `th.co.scb.ace.workbench.recovery.decision.partneraccess`.

**Pattern application**

| DP | Legacy marker | Microservice pattern | Dependency added |
|---|---|---|---|
| DP-01 | `recovery.<table>` or "recovery schema" | Owner's schema `rwb_<name>`; never read another service's tables | none |
| DP-03 | DecisionLogWriter, decision log | Local decision-record library and topic `rwb.decision-record.v1` | H RWB-PLT-E1027-CON |
| DP-05 | AceSourceQuery, `v_ace_*`, account_ext | Read through rwb-source-data's contract or the service's own ACE views | none |
| DP-06 | Parameters, casewf.config | Parameters contract of rwb-case and the client library | H RWB-PLT-E1042-CON; C RWB-P3-E1042-CON |
| DP-07 | Reference data, LOV | Reference-data contract of rwb-case | H RWB-PLT-E1043-CON; C RWB-P3-E1043-CON |
| DP-08 | RecoveryAccessGuard | Authorise contract of rwb-access and the guard library | H RWB-PLT-E1037-CON; C RWB-P4-E1037-CON |
| DP-11 | In-process call, published interface | REST contract with mock; one hop; 2 s timeout | none (C from the legacy dependency) |
| DP-13 | `/api/recovery/v1` | `/api/recovery/<short>/v1` | none |
| DP-15 | V0001 baseline, migration | Per-service Flyway sequence in the service's own schema | H RWB-PLT-E1044-CON |
| DP-19 | Screen, ace-web | gateway-bff composite route | H RWB-PLT-N001-CON |

Which pattern has an instance here: DP-03 is the record itself — the append through the decision-record path in the caller's transaction, the `prev_hash` and `entry_hash` chain, the append-only rule and the shared topic `rwb.decision-record.v1`, with its H RWB-PLT-E1027-CON. DP-01 is the boundary — the entry lives in `rwb_decision` and the partner, the partner user and the instruction are never read as tables. DP-06 is the page-size bound; DP-07 is LOV-DECISION with `AC-SIGN` and `AC-DENY`; DP-08 is the authorise answer behind the two reads; DP-11 is the one hop with a 2 s timeout and a breaker on the authorise call and the two `rwb-case` reads; DP-15 is the two index steps; DP-19 is the `gateway-bff` route through which SCR-38 and the auditor's view reach the two operations. DP-05 has an instance only as an absence: this service reads no `v_ace_*` view and no ACE table, and a partner identity is a reference of the external gateway and never an ACE party row.

The platform H dependencies — H RWB-PLT-E1027-CON, H RWB-PLT-E1042-CON, H RWB-PLT-E1043-CON, H RWB-PLT-E1037-CON, H RWB-PLT-E1044-CON and H RWB-PLT-N001-CON — and the C dependencies — C RWB-P3-E1042-CON, C RWB-P3-E1043-CON and C RWB-P4-E1037-CON — are not in the metadata rows of this story, which name None and RWB-P4-E2019-CON; they are the dependencies the DP table adds and they are recorded in GAP-1272 with ASM-2236 and ASM-2241, together with the decision-log store baseline and its JOB-14 check. None of them blocks the build beyond Day 1: they are platform and store contracts of waves 0 and 1 and the published contracts of `rwb-case` and `rwb-access`, built against their fakes.

**Components**

| Component | Type | Responsibility |
|---|---|---|
| `PartnerAccessRecordListener` | Kafka consumer with the inbox | Reads `DecisionRecorded` on `rwb.decision-record.v1`, deduplicates by event ID and by the idempotency key and hands the partner access facts to the appender |
| `PartnerAccessRecordValidator` | Service | Checks the code, the result, the reason code and the required references before any write, and rejects a personal field (BR11, BR12) |
| `PartnerAccessAppendService`, `ChainHasher` | Service | Writes the entry, its chain position, its inbox row and its idempotency row in one transaction; computes the canonical form and the `prev_hash` and `entry_hash` (BR2, BR3, BR13) |
| `DecisionLogQueryController`, `DecisionLogQueryService`, `DecisionLogRepository` | Controller, service, repository | The two operations of 12.1 with the declared right, the firm or `ALL` scope, the paging, the 401 to 503 mapping, the row shape and the insert-only write of `decision_log_entry` |
| `ReferenceListClient`, `ParameterClient`, `AuthoriseClient` | Client | LOV-DECISION and the page-size bound with the version in force, and the cached authorise answer, one hop with a 2 s timeout and a breaker (DP-06, DP-07, DP-08, DP-11) |

**Database and migrations.** Writes `decision_log_entry`, its inbox and idempotency rows and its outbox row in `rwb_decision` and reads no other schema (DP-01). The table, its columns of TSD P7 v2 T3.1, the trigger `tr_declog_append_only`, the missing grant for UPDATE and DELETE and the unique key on the idempotency key belong to the decision-log store baseline and are not rebuilt here (GAP-1273). Two steps in the Flyway sequence (DP-15): `V2026_2__decision_log_partner_access_index.sql` adds `ix_declog_partner_access ON decision_log_entry (decision_code, decided_at DESC)` and `ix_declog_partner_firm_gin ON decision_log_entry USING gin (actions jsonb_path_ops)`; the index names are Not specified in the source documents (GAP-1272; ASM-2244). No row of `partner`, `partner_user`, `role`, `permission` or `lov_value` is written here.

**Configuration and reference data.** LOV-DECISION holds `AC-SIGN` and `AC-DENY` and is read through DP-07 with the version in force, never as a literal (BR8). The page-size bound of the two reads is a parameter of DP-06 whose name is Not specified in the source documents (GAP-1272; ASM-2239), and the story holds no default. The result vocabulary is a reference row and not a constant; its value set has no source and the reading applied is `ALLOWED` and `REFUSED` (GAP-1272; ASM-2238). The claim-set reference is an opaque string carrying the business date and the hash of the claim set with the two versions in force, and this story never resolves the claims (GAP-1272; ASM-2240). The outbox retry policy and the inbox retention are the platform's (RWB-PLT-TE006-CON), used through DP-09 although it is not in the pattern set. No feature switch of this story's own is named by a source; the switch that stops a partner path in an environment is the parameter `rwb.access.partner-signin` of RWB-P4-E2019-APP (GAP-1272; ASM-2241).

**Build steps**

1. `DecisionLogRepository` and the two index steps; test the search by firm and date range and the single read (AC7).
2. `ChainHasher` and the canonical form: `chain_seq`, the first `prev_hash` of 64 zeros and `entry_hash` as the SHA-256 of the canonical form (AC1, AC10).
3. `PartnerAccessRecordValidator` with the code, the result, the reason code and the required references, and the rejection of a personal field (AC8, X1, X10).
4. `PartnerAccessAppendService` with the fail-closed transaction; test the failure of AC6 at the record path of the caller and the chain position the refused append does not use (AC6).
5. `PartnerAccessRecordListener` with the inbox dedupe and the idempotency rule; test the replay, the duplicate and the 409 (AC9).
6. The append-only rule: the trigger and the grant, with the four statements of AC10 refused and the audit line written.
7. `ReferenceListClient` and `ParameterClient` with the version in force, and the refusal rather than an assumed code or result (BR11, X9).
8. `DecisionLogQueryController` with the declared right, the firm or `ALL` scope, the paging and the problem mapping; tests for AC7, MSG-P4-002 and MSG-P4-003; then `AuthoriseClient` against the authorise fake and the whole-slice contract-fake run (AC1 to AC5).
9. The boundary test: no write to `rwb_access`, `rwb_partner` or `rwb_case`, no token and no personal value in any entry, event payload or log line, and one entry per resolution across a redelivery (AC8, BR5).

**Done when.** The tests of section 16 pass, the chain of a SIT day verifies from the first entry with no break, every partner access decision of the day leaves one entry with its firm, partner role, scope reference, gateway identity reference, result and reason code, a repeated record leaves one entry, a refused answer leaves none and does not consume a chain position, both reads answer inside the 2 s budget of the frame, and no partner row, session or token was read or written by this story.

### 14. Validation and messages

| ID | When | Message | Where it is produced |
|---|---|---|---|
| MSG-P7-003 | The partner access record cannot be appended, or lacks a field the entry requires | The action was not taken because the decision could not be recorded. Try again in a few minutes. | The decision-record path of DP-03, whose status the caller hands back; the access answer is refused with no session and an incident is raised |
| MSG-GEN-004 | A second append arrives for the same resolution under a different idempotency key | Someone else changed this record. Reload it to see their change. | This story, on the duplicate append of AC9 |
| MSG-P4-001 | The refusal of a partner identity with no role or no binding, or of a bank identity on the partner route | You have no Recovery Workbench role. Ask your team manager to request one. | `rwb-access`; this story records the answer and asserts the message, never rewrites it |
| MSG-P4-008 | The refusal of a firm that is suspended, exited or past its contract end | Your firm's access to the Recovery Workbench has ended. Contact your SCB partner manager. | `rwb-access`; this story records the answer and asserts the message |
| MSG-P4-002 | The caller holds no Decision log right on the two reads | You cannot {action} here. Your role does not include it. | This story, through the authorise answer of the read |
| MSG-P4-003 | The firm or the entry is outside the caller's scope | This case is not in your scope. | This story, through the authorise answer of the read |

MSG-P7-003, MSG-P4-001, MSG-P4-002, MSG-P4-003 and MSG-P4-008 are copied unchanged from RWB-E2-019 section 14 and the FSD P7 v3 message set, and MSG-GEN-004 from the platform set; MSG-P4-005 and MSG-P4-006 belong to the sign-in checks of `rwb-access` and appear in no entry of this story. Thai text for each message follows decision DL10. Every error is an RFC 9457 problem response with `messageId` set, `detail` carrying the text with its placeholders filled and `instance` naming the request; the status mapping is the legacy one — 403 with MSG-P4-002, 404 with MSG-P4-003, 409 with MSG-GEN-004 and 503 with MSG-P7-003 handed back on the decision-record path of DP-03.

### 15. Screens and states

No screen is built in this story. The two reads are consumed by SCR-38 Decision log query, which searches the log by firm, decision and date with export (FSD P7 v3 Screens), and by the auditor's view of the ledger; both are reached through the `gateway-bff` composite route of DP-19 and are another story's. The partner sign-in page and PRT-01 Partner home stay `rwb-partner`'s and the gateway's, and this story feeds neither.

| Where | State | What the reader sees |
|---|---|---|
| SCR-38 Decision log query (P7) | List | The partner access entries of a firm in decidedAt order, each with its decision code, partner role, scope reference, result and reason code |
| The entry read | One entry | The same row with its gateway identity reference, its claim-set reference, its `decidedAt`, its `prevHash` and its `entryHash` |
| The entry read | An entry with `correctsEntryId` | The correction beside the entry it corrects, and the corrected entry unchanged |
| The read | 403, or 404 | MSG-P4-002 for a caller without the right, MSG-P4-003 for a firm outside the scope; no row is returned |

A panel or screen id for showing a partner access entry beside the partner panel on SCR-34, and the field list of SCR-38, are Not specified in the source documents (GAP-1272; ASM-2245); the field list and the composite route specification belong to RWB-PLT-N001-CON and to the story that owns SCR-38.

### 16. Test cases

| TC ID | Covers | Level | Data |
|---|---|---|---|
| TC-E2-019-01 | AC1, BR1, BR2, BR3; legacy Covers "AC1, BR1, BR3" | Component | Synthetic firm LF-0012 with partner identity P-5101, partner role PT-LAWFIRM, scope PLACED, matrix version PM-2026.11 and masking version MASK-SIT-01 |
| TC-E2-019-02 | AC5, BR2, BR9; legacy Covers "AC2, BR4" | Unit | Partner identity P-5102 of firm VL-0004 with partner role PT-VALUER, and the change to firm LF-0012 with partner role PT-AGENCY |
| TC-E2-019-03 | AC2, BR6, BR13; legacy Covers "AC3, BR5" | Contract | Firm LF-0012 moved to panel status EXITED at 11:00 on 4 January 2027; MSG-P4-008 and reason PARTNER_NOT_ACTIVE |
| TC-E2-019-04 | AC3, BR2, BR6; legacy Covers "AC4, BR2" | Component | Partner identity P-5103 with no active binding; MSG-P4-001 and reason NO_PARTNER_BINDING |
| TC-E2-019-05 | AC4, BR5, BR12; legacy Covers "AC5, BR1" | Contract | Test user U-5105 holding RW-LITOFF on the partner route; MSG-P4-001 and reason BANK_IDENTITY_ON_PARTNER_ROUTE, with no bank role on the entry |
| TC-E2-019-06 | AC7, BR10; legacy Covers "AC6, BR3" | Component | The single entry read of the entry of AC1 by RW-AGENCYMG, and the entry of VL-0004 refused with MSG-P4-003 |
| TC-E2-019-07 | AC7, BR10; legacy Covers "AC7, BR2" | Component | The firm and date-range read of LF-0012 for 2026-12-01 to 2027-01-31, and the MSG-P4-002 refusal of a role without the right |
| TC-E2-019-08 | AC8, BR5, BR12; legacy Covers "AC8, BR6" | Component | The resolution of P-5101 with the group RWB-UAT-PT-LAWFIRM; a personal-field scan of the entry, the event payload, the audit line and the tests |
| TC-E2-019-09 | AC6, BR13; legacy Covers "AC9, BR1" | NFR | The decision-record library forced to fail every append during a partner sign-in; 503 with MSG-P7-003, no entry, no chain position, incident raised |
| TC-E2-019-10 | AC9, BR7; legacy Covers "Access" | Component | The same record twice under one idempotency key, and a second append for the same resolution under a different key; 409 with MSG-GEN-004 |
| TC-E2-019-11 | AC10, BR4; legacy Covers "Principle 5" | Component | An AC-SIGN entry at chain_seq 1; an UPDATE and a DELETE attempted through the service role and the schema owner, and one correction |

The eleven legacy test-case ids of RWB-E2-019 are kept in the order of the work package, and each is answered here on the record side: the entry, its firm, its partner role, its scope reference, its result and reason code, its chain and its two reads. The sign-in, the second factor, the role count, the firm status, the binding and the instruction read are the contract fakes' and their own services'. The legacy level System maps to Component, Contract or Unit as the row shows, Access to Component and Resilience to NFR. The `-ITG` copies of these cases belong to RWB-ITG-E2019-ITG, which runs the same values across the gateway, `rwb-access` and `rwb-partner`. The full test, with its Given, When and Then, is in Recovery Workbench Test Cases v8.xlsx, tab Story test cases, under the same test case ID.

### 17. Guardrails

- No business value in code: the decision codes, the result vocabulary, the reason codes, the page-size bound and the message ids are reference or parameter rows, and the partner roles and firms are facts of their owners; nothing of them is a constant here.
- No personal data in the entry, the claim-set reference, the event, the audit line, the tests or the logs: the firm reference, the partner role, the scope reference, the directory identity reference, the decision code, the result, the reason code, the hashes and the dates only. No personal name, national id number, e-mail address or phone number is read or written (BR5, BR12).
- No partner table and no partner row (DP-01): `partner`, `partner_user` and `partner_instruction` stay in `rwb_partner`, and the firm, the role and the gateway identity reference arrive as fields of the record.
- No token, session identifier, password, secret or private key is read, held, cached or logged; the entry names a directory identity reference and never a credential (ADR-010, slide 35).
- ACE data only through the owner's contract or `v_ace_*` views: this story reads no ACE data at all, and no ACE party is ever a partner identity.
- One recorder and no mover: this story resolves no identity, opens no session, issues no token and changes no partner row, so a partner access record can never open a partner path (BR9).
- No entry without its answer and no answer without its entry: the entry, its chain position, its inbox row and its idempotency row commit in one transaction, and an answer whose record cannot be appended is refused with an incident (BR13, R-UNI-39).
- Append only and hash chained, with one entry per resolution: no UPDATE and no DELETE on `decision_log_entry`, a correction is a new entry with `corrects_entry_id`, and the inbox dedupe, the idempotency key and the refusal of a duplicate append make a second entry impossible (BR3, BR4, BR6, BR7).
- One base and one topic: `/api/recovery/decision/v1` and `rwb.decision-record.v1` with `rwb-decision` in namespace `rwb-recovery`; no monolith base and no other service's base or topic is declared here as this service's own.
- One hop and 2 s with a breaker per downstream on the authorise call and the two `rwb-case` reads; an unreadable list or parameter refuses the append rather than writing an assumed value (DP-11).

### 18. Traceability

| Requirement ID | Requirement (short) | BRD section | Feature | L3 process | Rules | Test cases |
|---|---|---|---|---|---|---|
| REQ-ACA-012 | Partners only through the external gateway, with MFA, scoped to their own cases | Epic 2, 3.4; Program 5.4 | FEAT-OCC-13 | 12 Manage partners | BR1 to BR15 | TC-E2-019-01 to TC-E2-019-11 |

REQ-ACA-012 is carried on this story only for the partner access record and its two reads; the identity, the sign-in, the role, the scope, the firm and the instruction belong to RWB-P4-E2019-CON, RWB-P4-E2019-APP, RWB-S9-E2019-APP and RWB-ITG-E2019-ITG. The ledger controls are carried too: REQ-DRI-001 and REQ-DRI-002 for the one append-only entry, REQ-DRI-003 for the chain, REQ-DRI-005 for the answer that does not stand unrecorded, and REQ-DRI-012 for the two reads.

| Legacy reference | Where it is kept |
|---|---|
| One `AC-SIGN` entry for a partner sign-in, with the role, the firm and the partner identity | Sections 4, 7 (AC1), 8 (BR1, BR2), 11 |
| One `AC-DENY` entry with reason `PARTNER_NOT_ACTIVE` when the firm is suspended, exited or past its contract end | Sections 5 (X1), 7 (AC2), 8 (BR2, BR6), 11 |
| One `AC-DENY` entry with reason `NO_PARTNER_BINDING` for an identity with no binding | Sections 7 (AC3), 8 (BR2), 11 |
| One `AC-DENY` entry with reason `BANK_IDENTITY_ON_PARTNER_ROUTE` for a bank identity on the partner route | Sections 7 (AC4), 8 (BR2, BR5), 11, 17 |
| The partner role of the answer, the one role per partner type, and the scope `PLACED` with the firm and its instruction types | Sections 1, 4, 7 (AC1, AC5), 8 (BR2), 11 |
| The matrix version and the masking version in force at the resolution, and the rule that no claim value is copied | Sections 4, 7 (AC1, AC8), 11 |
| A record that cannot be written blocks the action, and the log is append only and hash chained | Sections 5 (X2), 7 (AC6, AC10), 8 (BR3, BR4, BR13), 9, 14, 17 |
| The identities P-5101, P-5102 and P-5103, test user U-5105, the firms LF-0012, LF-0019 and VL-0004, the roles PT-LAWFIRM, PT-VALUER and PT-AGENCY, the group RWB-UAT-PT-LAWFIRM and instruction INS-2027-000431 | Sections 3, 7, 11, 16 |
| Messages MSG-P4-001, MSG-P4-002, MSG-P4-003, MSG-P4-008, MSG-P7-003 and MSG-GEN-004, rules R-UNI-39 and R-UNI-40, and patterns DP01 to DP19 of the metadata row | Section 14, exception paths, sections 2, 5, 8, 13 |

The other slices of the key answer the rest: RWB-P4-E2019-CON the resolve operation, its claim set, its answer and its refusal vocabulary; RWB-P4-E2019-APP the resolver, the partner role rows, the `PLACED` scope and the two versions; RWB-P4-E2019-INF the DMZ plumbing; RWB-P4-E1037-APP and RWB-P4-AD001-APP the role matrix and the group mapping; RWB-S9-E2019-APP the firm, the partner user, the binding and the instruction; RWB-P4-E1039-APP the general access log; and RWB-ITG-E2019-ITG the cross-service harness and the `-ITG` copies.

### 19. Out of scope

- The sign-in, the multi-factor authentication, the token and the session: the partner gateway in the DMZ and `gateway-bff` (RWB-PLT-N007-INF, RWB-PLT-N001-CON), and RWB-P4-E1022-APP for the bank route.
- The partner identity, its resolution and the access answer: RWB-P4-E2019-CON and RWB-P4-E2019-APP, with the DMZ slice in RWB-P4-E2019-INF.
- The firm, the panel status, the contract end, the partner user, the binding, the instruction and the partner portal: `rwb-partner` (S9, RWB-S9-E2019-APP).
- One role per partner type, firm scope on instructions, revocation and the same-day loss of access: RWB-P4-E2019-APP, RWB-P4-E1037-APP and RWB-P4-AD001-APP; this story records the decision and ends no session.
- The authorise call and the guard library: consumed through RWB-P4-E1037-CON and RWB-PLT-E1037-CON with their fakes (DP-08, DP-11) and not rebuilt here. The general access log into the decision log, the break-glass grant and the access-log read are RWB-P4-E1039-APP's.
- The approval operations, the approval queue SCR-10, the decision screen SCR-11, the recommendation read and the rule registry: the other P7 stories of this service; this story evaluates no rule package and loads no Drools kit.
- The general ingest of every other decision code into the ledger, the append-only table itself, JOB-14 at 02:00 and the daily seal: the decision-log baseline of this service. The data-lake copy of the log, JOB-13 and lake retention are retired with the data lake (DP-17).
- SCR-38 Decision log query as a built screen, the partner panel SCR-34 and the composite route: the screen stories, RWB-S9-E2019-APP and RWB-PLT-N001-CON.
- The `-ITG` copies of the test cases and the cross-service harness: RWB-ITG-E2019-ITG. The Helm chart, the Kafka subscription values, the metrics, the alerts and the runbook: an OPS story of this legacy key.

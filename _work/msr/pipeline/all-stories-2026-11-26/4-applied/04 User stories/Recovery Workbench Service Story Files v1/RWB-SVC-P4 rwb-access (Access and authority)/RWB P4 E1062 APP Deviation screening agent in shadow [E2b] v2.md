# RWB-P4-E1062-APP Deviation screening agent in shadow [E2b]

SCB Collections and Recovery. Henka Group, 22 November 2026.
(C) Siam Commercial Bank and Henka Pte Ltd

| Item | Value |
|---|---|
| Story key | RWB-P4-E1062-APP |
| Work type | APP (App development) |
| Suggested owner | TechX (suggested; any team may pick up this story) |
| Service | rwb-access |
| Service epic | RWB-SVC-P4 |
| Wave | 1 |
| Business epic | EP01 |
| Release | 30 November 2026 (tentative) |
| Legacy key | RWB-E1-062 |
| Legacy disposition | Split (rework) |
| Build status | Not started |
| Patterns applied | DP01, DP04, DP06, DP07, DP09, DP13, DP15, DP18, DP19, DP20 |
| Parallel lane | L-P4-Y |
| Ready to start | Day 1 |
| Depends on (build) | None |
| Contract dependencies | RWB-P10-E1062-CON |
| Integration dependencies | None |
| External dependencies | None |
| PRD reference | 03 Requirements and specifications/PRD/Recovery Workbench PRD P4 rwb-access v1.md (no FR mapped to REQ-DVH-001, REQ-DVH-003, REQ-DVH-007) |
| Status | Draft (realignment v1) |

**Change log.** D-RCV-60, 22 November 2026: the rwb-access slice of RWB-E1-062. The shadow run of the deviation screening agent reads case data, call notes, documents and rule rows, and the legacy story answered "who may read this and what is masked" with an in-process access check of the monolith. In the target that answer is rwb-access's: this story fixes the agent-authority part of `POST /api/recovery/access/v1/authorise`, the non-human part of `GET /api/recovery/access/v1/me/session` and one access entry per answer, so a screening run passes the same role, scope and masking checks a person passes and every read it makes is logged with the policy version that allowed it. Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

**Change log.** D-RCV-60, 26 November 2026: fixes from the deterministic build-readiness checks (X20 RWB-P4-E1062-APP). Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

### 1. Story

As a **security administrator (RW-SECADM) and the service identity of the agent platform (SY-AGENT)**, I want **rwb-access to answer the authority question for one screening run: who the caller is and which role class it holds, which capability areas and letters the run's reads need at the matrix version in force, one marker per personal field the run presents at the masking version in force, the refusal with its reason, and one access entry per answer carrying the agent, its policy version and its autonomy mode**, so that **the shadow proposals of RWB-E1-062 start from reads that a person of the same role could also make, no clear personal value reaches the model, and an auditor can say which rule allowed which read on which day**.

This story is the authority slice of legacy RWB-E1-062 and nothing else. The legacy story asks for a deviation screening agent that reads "case data, call notes and documents" and proposes X1 to X7 in shadow (legacy sections 1 and 2), masks personal fields before the model call (legacy section 4 step 3), reads the owner role of each code from R-DEV-02 to R-DEV-06 (step 5), forbids a read of another module's table (legacy section 17) and refuses a role without the right with MSG-P4-002 (legacy section 5 X7, section 14). Two of those facts are rwb-access's: the decision that the run may read, and the masking of what it reads.

Inside `rwb-access` this is the agent-authority capability of the access service:

- Service `rwb-access`, schema `rwb_access`, REST base `/api/recovery/access/v1`, topic `rwb.access.events.v1`, Temporal task queue `rwb-access` in namespace `rwb-recovery`, Java package `th.co.scb.ace.workbench.recovery.access` (Architecture v5 slides 4, 8 and 13; context pack P4).
- Two deliverables. First, the **agent-authority part** of the service's existing `POST /api/recovery/access/v1/authorise`: the caller type `AGENT`, the agent code, the case, the trigger event, the policy version and the autonomy mode with the capability areas, the rights and the field IDs the run needs, answered with admitted or refused, the reason code, the role codes, the role class, the scope, the letters per area, the matrix version, the masking version and one marker per field ID. Second, the **non-human part** of `GET /api/recovery/access/v1/me/session`, which answers the caller's own profile.
- One **access entry per answer**, allowed or refused, appended before the answer leaves the service by the writer of RWB-P4-E1039-APP with decision code `AC-READ` or `AC-DENY`, and read back through the service's access-log search of RWB-P4-AD007-APP (API-P4-008).
- The rows are read, never written, here: `role` (DF-REF-034 to DF-REF-039), `permission` (DF-REF-040 to DF-REF-044) and `masking_rule` (DF-REF-198 to DF-REF-204) in `rwb_access`. The role catalogue and the matrix versions are RWB-P4-E1019-APP's, the masking profiles and their versions are RWB-P4-AD004-APP's, the enforcement point on every screen and every agent call is RWB-P4-E1037-APP's; this story composes their data into one answer for one run and adds no row of any of them.
- The values of the run are the agent contract's, not this service's: the run key "SCREENING:<caseId>:<eventId>", agent "SCREENING", policy "P1", mode "SHADOW", prompt "PR1" and the four read tools come from RWB-P10-E1062-CON and are carried as presented values on the request and on the entry. No agent row, no proposal and no confidence is stored here.

The rest of legacy RWB-E1-062 is owned elsewhere and is not answered here: the run, the orchestrator, the guardrails, the owner-role resolution and the evaluation are rwb-agent's (RWB-P10-E1062-APP against RWB-P10-E1062-CON); the documents and their extracted fields are rwb-document's (RWB-P5-E1062-APP); the interaction ledger, the call notes and the complaint notes are rwb-source-data's (DP-18); the deviation itself is rwb-deviation's; the cross-service proof is RWB-ITG-E1062-ITG, which consumes exactly the two operations this story extends.

### 2. Business rationale

A dispute, a death, a fraud sign or a lost contact found late means contact that should have stopped, or a case worked on the wrong route. The screening agent reads the case, the ledger and the documents and proposes deviations with reasons; in Epic 1 nothing is raised and the proposals are scored and shown to nobody (legacy section 2). A run that reads personal data and shows its output to no one is still a read of personal data, and the controls say so: party identifiers are masked at rest, on every screen and on every agent call, by role (NFR-039); each agent receives only the personal data it needs (NFR-040); every read of the case store and the document store is logged (NFR-042); and an agent runs under a service identity and is subject to the same role checks as a person (NFR-051, REQ-ACA-010).

In the monolith that rule was one access check inside the agent module, and the masker and the log were side effects of the same call. In the target the agent is a service of its own and the check is a contract. If the check stayed in rwb-agent, every other agent and every model would re-implement it, and the one property an audit relies on - that a non-human reader is authorised exactly as a person is, and that its read is recorded - would become a property of the caller.

Three target facts shape the slice.

1. **Identity.** The caller of the authority question is the calling service's identity; the subject is the agent service identity `SY-AGENT`, resolved through the `role` row at the matrix version in force, with role class `NON_HUMAN_ACTOR` and no partner and no break-glass state. Only a role of that class may be the subject of a run, so a person's token cannot drive the agent path.
2. **Least privilege.** The agent holds the letter `R` and only `R` in the two areas rwb-access governs for it: Rules and parameters and Reference data (TSD P4 v3 T6.1, `SY-AGENT Agent platform | R | R | -`). Those are exactly the two reads the legacy run makes for its codes and its owner roles. A `C`, `U`, `D` or `A` letter is refused with MSG-P4-002 and the reason code, with no bypass for a non-human caller.
3. **Disclosure.** The masking answer is default deny: a field is `clear` only where a `masking_rule` row for one of the subject's roles, that field ID and the masking version in force says `unmasked` true, and `masked` otherwise, including where no row exists. The legacy marks two of the run's fields masked outright (the ledger summary DF-INT-011 and the stored document field value DF-DOC-015), so the agent's input carries references, codes and confidences and no clear personal value.

It serves REQ-DVH-001, REQ-DVH-003 and REQ-DVH-007 by making the run's evidence reachable under control: the codes it detects, the owner it routes to and the contact it names are all read from records whose access is decided here and recorded here. It changes no business rule of the agent and no rule of the access service's own catalogue.

Three values no source fixes are carried as placeholders and not as invented values: the request and answer element set of the agent-authority part - Not specified in the source documents (GAP-2326; ASM-3867); the reason-code vocabulary and the status of each code - Not specified in the source documents (GAP-2327; ASM-3868); and which of the run's fields are personal for a non-human actor, with the mask format served to an agent - Not specified in the source documents (GAP-2328; ASM-3869). The default scope of the agent identity (GAP-2329; ASM-3870) and the access-entry element set of an agent read (GAP-2330; ASM-3871) are carried the same way.

### 3. Preconditions

| Precondition | What it gives this story |
|---|---|
| RWB-P4-E1037-CON (same service, its own contract story) | The authorise contract itself: `POST /api/recovery/access/v1/authorise` and `GET /api/recovery/access/v1/me/session` on base `/api/recovery/access/v1`, the request and answer envelopes, the RFC 9457 problem shape and the guard library of DP-08. This story fixes a part of two existing operations and adds no path |
| RWB-P4-E1037-APP (same service, the enforcement point) | The `rwb_access` baseline - `role`, `permission` and `masking_rule` with their dictionary rows and the per-service login of DP-02 - and the masking answer this story composes rather than restates |
| RWB-P4-E1019-APP (same service) | The role rows, the permission rows and the matrix version in force: `PM-2026.11` at go-live and `PM-2026.12` from 1 December 2026, with `SY-AGENT` of class `NON_HUMAN_ACTOR` and letters `R` in `RULES_AND_PARAMETERS` and `R` in `REFERENCE_DATA` (TSD P4 v3 T6.1) |
| RWB-P4-AD004-APP (same service) | The `masking_rule` versions and the version in force, `MASK-SIT-01`; the mask formats `XXXXXXXXX1234`, `XXXXXX5678` and `XXXX-XX-XX`; the masked-by-default rule including the field with no rule |
| RWB-P4-E1039-APP (same service) | The access-entry writer: the append through the local decision-record path, the hash chain, the outbox row and its forced-failure behaviour. This story supplies the entry and the reason code and adds no second writer |
| RWB-P4-AD007-APP (same service) | The access-log search `GET /api/recovery/access/v1/admin/access-log` (API-P4-008) that reads back the entries of AC6; this story adds no query parameter to it |
| RWB-P10-E1062-CON | The rwb-agent contract of this legacy key: the run key "SCREENING:<caseId>:<eventId>", agent "SCREENING", policy "P1", mode "SHADOW", prompt "PR1", the four read tools and the two trigger events. The agent is the subject of this answer and the consumer of it; the story builds against its fake |
| RWB-P3-E1043-CON and RWB-P3-E1042-CON | The reference-data and parameters contracts of rwb-case (DP-07, DP-06) through their client libraries: LOV-CAPABILITY, LOV-SCOPE, LOV-ROLE-CLASS, and the retention window and the feature switch of the answer |
| RWB-PLT-TE006-CON, RWB-PLT-E1044-CON, RWB-PLT-N001-CON | The outbox library of the entry (DP-09), the per-service Flyway sequence (DP-15) and the gateway-bff route of the admin reads (DP-19). They arrive with the service baseline and are not new build dependencies of this slice |

Business preconditions carried from RWB-E1-062:

- Agent "SCREENING" has approved policy "P1": mode SHADOW, timeout 60 seconds, confidence floor 0.80, allowed tools read_case, read_interactions, read_documents and read_document_fields, and output schema "screening-v1" with codes from LOV-DEVIATION (X1 to X7). Prompt "PR1" is approved. Both are the agent's rows; this story reads neither.
- Rule rows R-DEV-02 to R-DEV-06 are loaded in the rwb-decision registry and are in force, so the owner role of each code is data. They are never read by this service (DP-04 as a prohibition, section 13).
- Labelled sample "SCREEN-S1" version 1, the 200 cases, the counts 18, 2 and 6 and the precisions 0.9000 and 0.7500 are the agent's fixtures; this story needs only the case identifiers RW-2026-000401 to RW-2026-000404 as presented values.
- Matrix version `PM-2026.11` and masking version `MASK-SIT-01` are the labels in force at go-live and in SIT; both are rows and neither is a constant in code.
- Every user, service identity, case, document and reference in the tests is synthetic; no production case, call note or document value is copied into a test, a fixture or a prompt, and no name of a person appears anywhere.
- No approval is required to build against a Draft contract: the service baseline is Draft (realignment v1) and this part is frozen when the agent contract's contract tests pass.
- The release date 30 November 2026 is tentative and is copied unchanged.

### 4. Flow

1. The agent platform's tool gateway, running under the `rwb-agent` service identity, is about to start or continue one screening run for case `RW-2026-000401` and trigger event `DocumentStored`, and calls `POST /api/recovery/access/v1/authorise` with caller type `AGENT`, agent code `SCREENING`, the case, the trigger event, policy version `P1`, autonomy mode `SHADOW`, the capability areas and rights the run needs, and the field IDs it will present.
2. `AgentAuthorityController` reads the calling identity from the token; the guard library of DP-08 answers the calling service's own right to the operation with 403 and MSG-P4-002 before any row is read. That is the caller's right, not the subject's.
3. `AgentSubjectResolver` resolves the subject: the service identity presented for the agent is matched to a `role` row at the matrix version in force and its role class is read. No role, or a role class other than `NON_HUMAN_ACTOR`, is a refusal with reason code `CALLER_KIND` (BR2).
4. `MatrixVersionResolver` fixes the matrix version in force for the day of the call, and `MaskingVersionResolver` fixes the masking version, so one answer names one version of each and never a mixture of two (BR8).
5. `PermissionReader` reads the letters of the subject's roles in each requested capability area. A requested letter that the rows do not hold is a refusal with reason code `RIGHT_NOT_HELD`, and the answer names the area, the letter asked and the matrix version (BR3).
6. `AgentScopeService` reads `role.default_scope`. A scope of `ALL` carries no restriction in this answer; a narrower scope cannot be resolved, because no table of `rwb_access` binds a role to a list of teams or regions, and the refusal is `SCOPE_NOT_ALL` (BR4; GAP-2329; ASM-3870).
7. `AgentRequestValidator` checks the presented values against the contract of this key: a required member missing, a capability area outside LOV-CAPABILITY at the version in force or a field ID that is not a personal field id of the dictionary is 422 with MSG-GEN-001 naming the member (BR6).
8. `MaskingAnswerService` composes the masking answer from the enforcement point of RWB-P4-E1037-APP and the profiles of RWB-P4-AD004-APP: one marker per presented field ID at the masking version in force, `clear` only where a `masking_rule` row for one of the subject's roles, that field and that version says `unmasked` true, `masked` otherwise including where no row exists (BR5).
9. The answer is 200 with `admitted` true, the caller type, the agent code, the role codes, the role class, the scope, the letters per requested area, the matrix version, the masking version, the policy version, the autonomy mode and the field markers. It carries no case status, no owner, no ledger entry, no document, no document field value, no rule row, no proposal and no confidence (BR9).
10. A refusal is 403 with an RFC 9457 problem response, `messageId` MSG-P4-002, a `reasonCode`, and only the values that make the refusal legible: the area, the right asked, the matrix version and the scope. No field value, no case fact and no other subject's data is returned (BR10).
11. `AccessEntryWriter` of RWB-P4-E1039-APP appends one access entry before the answer leaves the service, with decision code `AC-READ` for an admission and `AC-DENY` for a refusal, and the values of BR7. The entry carries no name, no e-mail address, no call note, no document value and no proposal.
12. Where the entry cannot be written the answer is withheld: the call fails with 503 and MSG-P7-003, because an access entry that is missing cannot be reconstructed and no admission may proceed unlogged (FSD P4 v3 AC-EXC-P4-007-03; BR7).
13. The same subject reading `GET /api/recovery/access/v1/me/session` is answered from the same readers, so a profile read and an authority answer never disagree, and the profile carries no partner identity and no break-glass grant because a non-human actor holds neither.
14. Nothing of the run itself is written here: no run row, no proposal, no deviation and no ledger entry. The agent writes its run in `rwb_agent`; this service answers and records the access, one hop each way.

### 5. Exception paths

| ID | Trigger | What happens | Message | Covered by |
|---|---|---|---|---|
| X1 | The calling service identity holds no right to the authority operation | 403 before any row is read; nothing is answered | MSG-P4-002 | AC1 |
| X2 | The subject does not resolve to a role at the matrix version in force | Refused with reason code `CALLER_KIND`; no letter, no field marker and no version label in the answer | MSG-P4-002 | AC4 |
| X3 | The subject resolves to a role whose class is `BANK_USER` or `PARTNER_USER` | Refused with reason code `CALLER_KIND`: a person's identity cannot drive the agent path | MSG-P4-002 | AC4 |
| X4 | The subject's roles hold no `R` letter in a requested area | Refused with reason code `RIGHT_NOT_HELD`, naming the area, the letter and the matrix version | MSG-P4-002 | AC2 |
| X5 | The subject's roles hold the letter but not in the requested write form (`C`, `U`, `D` or `A`) | Refused with reason code `RIGHT_NOT_HELD`; no bypass for a non-human caller | MSG-P4-002 | AC2 |
| X6 | The subject's default scope is narrower than `ALL` | Refused with reason code `SCOPE_NOT_ALL`; no team or region list is named, because none exists in the schema | MSG-P4-002 | TC-E1-062-10 |
| X7 | A presented field ID has no `masking_rule` row for any of the subject's roles | The marker is `masked`: default deny, never an error and never `clear` | None | AC5 |
| X8 | A required request member is missing, or a capability area or a field ID is outside its list | 422 naming the member; nothing is admitted and no entry beyond the refusal | MSG-GEN-001 | AC1, AC2 |
| X9 | The access entry cannot be written | 503 and no answer; the admission is not given and nothing else is written | MSG-P7-003 | AC8 |

No exception path of this story changes a case, a run, a proposal or a deviation: this service answers and records, and the states of the run are the agent's.

### 6. INVEST check

| Test | Result |
|---|---|
| Independent | Answers from `rwb_access` alone, builds against the rwb-agent contract fake RWB-P10-E1062-CON, the reference-data and parameters client libraries and the `rwb_access` baseline; no case, ledger, document, deviation or agent row is read, and no build dependency of its own is added |
| Negotiable | The matrix version, the letters, the scope, the role class, the masking rows, the field list and the reason codes are data or contract values; the internal order of the readers is design |
| Valuable | One authority answer makes a screening run pass the checks a person passes and one access entry makes every read of the run auditable before a proposal exists |
| Estimable | Two extended operations, one subject resolver, one permission reader, one masking composition, one validator and one entry appender |
| Small | Fits one sprint as a secondary slice of the legacy key; there is no screen, no workflow, no business event and no table of its own |
| Testable | Every criterion in section 7 is one automated test over synthetic role, permission and masking rows, with the agent contract, the reference data and the entry writer stubbed |

### 7. Acceptance criteria

```gherkin
Feature: The authority answer of rwb-access for the deviation screening agent in shadow

  Background:
    Given the rwb-access base path is /api/recovery/access/v1 and the schema is rwb_access
    Given the rwb-agent contract mock returns the run key "SCREENING:<caseId>:<eventId>", agent "SCREENING", policy version "P1", mode "SHADOW", prompt "PR1" and the four reads read_case, read_interactions, read_documents and read_document_fields
    Given the rwb-case reference-data contract mock returns LOV-CAPABILITY with "RULES_AND_PARAMETERS" and "REFERENCE_DATA", LOV-ROLE-CLASS with "NON_HUMAN_ACTOR" and LOV-SCOPE with "ALL"
    Given matrix version "PM-2026.11" is in force on 30 November 2026 and gives the service identity "SY-AGENT" the letter "R" in "RULES_AND_PARAMETERS" and "R" in "REFERENCE_DATA"
    Given the "role" row of "SY-AGENT" carries role class "NON_HUMAN_ACTOR" and default scope "ALL"
    Given masking version "MASK-SIT-01" is in force and holds no "unmasked" row for the roles of "SY-AGENT"

  Scenario: AC1 One answer for one screening run names the roles, the areas, the letters and the two versions (new, D-RCV-60)
    When the rwb-agent service identity calls POST /api/recovery/access/v1/authorise for callerType "AGENT", callerCode "SCREENING", caseId "RW-2026-000401", triggerEvent "DocumentStored", policyVersion "P1", autonomyMode "SHADOW", capabilityArea "RULES_AND_PARAMETERS" and right "R"
    Then the response is 200 with admitted true, roleCodes "SY-AGENT", roleClass "NON_HUMAN_ACTOR", scope "ALL", matrixVersion "PM-2026.11" and maskingVersion "MASK-SIT-01"
    Then the answer names the capability area "RULES_AND_PARAMETERS" and the letter "R" that admitted the read
    Then the same call for the area "REFERENCE_DATA" and the right "R" is admitted on the same two version labels
    Then the answer carries no case status, no owner, no queue, no ledger entry, no document, no rule row, no proposal and no confidence

  Scenario: AC2 The same check a person passes refuses the agent the write it does not hold (new, D-RCV-60)
    When the rwb-agent service identity asks for the area "RULES_AND_PARAMETERS" and the right "C"
    Then the response is 403 with message MSG-P4-002, reasonCode "RIGHT_NOT_HELD", capabilityArea "RULES_AND_PARAMETERS", right "C" and matrixVersion "PM-2026.11"
    Then when a user holding "RW-COE", whose letters are "CRUD" in that area, asks for the same right the call is admitted, so no non-human path exists that a person does not pass
    Then one access entry is appended with decision code "AC-DENY" and the reason code, and nothing is admitted
    Then a request with no capabilityArea member is answered 422 with message MSG-GEN-001 naming the member

  Scenario: AC3 The agent's own profile names its class, its areas, its scope and the two versions (new, D-RCV-60)
    When the rwb-agent service identity calls GET /api/recovery/access/v1/me/session
    Then the response is 200 with roleCodes "SY-AGENT", roleClass "NON_HUMAN_ACTOR", scope "ALL", matrixVersion "PM-2026.11", maskingVersion "MASK-SIT-01" and the letters of each capability area in force
    Then the answer carries no partner identity and no break-glass grant, because a non-human actor holds neither
    Then a caller whose role class is "BANK_USER" is answered 403 with message MSG-P4-002 and no profile

  Scenario: AC4 A person's identity cannot drive the agent path (new, D-RCV-60)
    Given the rwb-agent contract mock returns the same run for user reference "U-6100", whose role "RW-CASEOWN" carries role class "BANK_USER"
    When that identity asks the authority question with callerType "AGENT"
    Then the response is 403 with message MSG-P4-002 and reasonCode "CALLER_KIND"
    Then no letter is read, no field marker is answered and no matrix version is named
    Then the run of that event holds no admission, and the run the contract mock answers for "SY-AGENT" is unaffected

  Scenario: AC5 Every personal field the run presents is answered masked (new, D-RCV-60)
    When the authority question presents fieldIds "DF-INT-011", "DF-DOC-015" and "DF-PTY-007"
    Then the answer carries maskingVersion "MASK-SIT-01" and the marker "masked" for all three field IDs
    Then a field ID with no "masking_rule" row in the version in force is answered "masked", as the date of birth of the legacy case is
    Then a marker is "clear" only where a "masking_rule" row for one of "SY-AGENT"'s roles, that field and "MASK-SIT-01" says "unmasked" true, and no such row exists for the agent
    Then the answer carries no field value, no rendering and no last four digits

  Scenario: AC6 Every answer leaves one access entry with the agent, its policy and its mode (new, D-RCV-60)
    When one run is admitted on the letter "R" and one is refused with reasonCode "RIGHT_NOT_HELD"
    Then two entries are appended, the first with decision code "AC-READ" and the second with "AC-DENY"
    Then each entry carries actor "SY-AGENT", callerType "AGENT", callerCode "SCREENING", policyVersion "P1", autonomyMode "SHADOW", caseId "RW-2026-000401", triggerEvent "DocumentStored", the field IDs with their markers, matrixVersion "PM-2026.11", maskingVersion "MASK-SIT-01" and the time
    Then the access-log search of RWB-P4-AD007-APP, filtered by actor "SY-AGENT" and the day, returns both entries in time order
    Then neither entry carries a name, an e-mail address, a call note, a document value or a proposal

  Scenario: AC7 A new matrix or masking version is answered without a deployment (new, D-RCV-60)
    Given matrix version "PM-2026.11" is in force on 30 November 2026
    When the authority question is asked on that date the answer names "PM-2026.11"
    Then when version "PM-2026.12" is loaded and takes effect on 1 December 2026 the same question asked on 2 December 2026 names "PM-2026.12" with no deployment
    Then a masking version "MASK-SIT-02" in force from its own date is answered the same way
    Then a read never mixes two versions: it answers one of each whole, the one in force on the day of the call

  Scenario: AC8 An answer that cannot be recorded is not given (new, D-RCV-60)
    Given the access-entry writer of RWB-P4-E1039-APP is forced to fail
    When the authority question is asked for case "RW-2026-000402"
    Then the response is 503 with message MSG-P7-003 and no authority answer
    Then no admission exists for that run, and the rwb-agent contract mock records no proposal for the case and event

  Scenario: AC9 The authority names no table of another service (new, D-RCV-60)
    Given case "RW-2026-000403", its outbound call of 2026-11-25, document "D-1001" and the open deviations of the case exist in rwb-case, rwb-source-data, rwb-document and rwb-deviation
    When the authority question is asked with that case, that document reference and that interaction reference
    Then the answer is given on the values presented with the request and no query of the package names recovery_case, interaction, document, deviation, agent_run or any recovery.v_ace_* view
    Then an unknown case or document is not refused here: that refusal is its owner's 404
    Then the rule rows R-DEV-02 to R-DEV-06 stay the agent's and this service loads no rule package for the run
```

The nine criteria above are new and test only this slice: the authority answer of one screening run, its masking markers, its profile read, its refusal forms, its two version labels and its one access entry per answer. The legacy criteria AC1 to AC9 of RWB-E1-062 are owned by RWB-P10-E1062-APP (the shadow flags, the precision and recall, the run start, the owner role, the preceding contact, the review marker, the repeated event, the code outside the list and the timeout) and are not copied here, because this story owns no legacy AC.

The cross-service facts are read from the contract mocks named in the Background: the rwb-agent contract of RWB-P10-E1062-CON returns the run key, the agent code, the policy version, the mode and the four reads, and the rwb-case reference-data contract returns the four lists with the version in force. The reference to the run is a presented value and never a call: this service never calls rwb-agent, and the agent is the caller of the two operations of section 12.1. The requested-area and field-ID element names of the agent-authority part are Not specified in the source documents (GAP-2326; ASM-3867) and the three reason codes are this story's enumeration (GAP-2327; ASM-3868).

### 8. Business rules

| ID | Rule | Source |
|---|---|---|
| BR1 | A screening run reads only what rwb-access admits: one authority answer per run, asked by the calling service identity, with the case, the trigger event, the policy version, the mode, the areas, the rights and the field IDs | NFR-051; REQ-ACA-010; legacy RWB-E1-062 sections 10 and 17 |
| BR2 | Only a role of class `NON_HUMAN_ACTOR` may be the subject of this answer: a role of class `BANK_USER` or `PARTNER_USER` is refused with reason code `CALLER_KIND`, so a person's identity cannot drive the agent path | LOV-ROLE-CLASS; NFR-051; legacy section 10 |
| BR3 | The subject passes the same permission check a person passes: the letter asked, in the area asked, from `permission` at the matrix version in force; the agent holds `R` in Rules and parameters and `R` in Reference data and holds no `C`, `U`, `D` or `A` letter for this key | TSD P4 v3 T6.1; REQ-ACA-010; legacy section 10 |
| BR4 | The scope follows `role.default_scope`: `ALL` carries no restriction in this answer, and a narrower scope is refused with reason code `SCOPE_NOT_ALL`, because no table of `rwb_access` binds a role to a list of teams or regions | TSD P4 v3 T3.1; GAP-2329; ASM-3870 |
| BR5 | Masking is default deny: a field ID is answered `clear` only where a `masking_rule` row for one of the subject's roles, that field and the masking version in force says `unmasked` true, and `masked` otherwise, including where no row exists; no field value is answered | NFR-039; NFR-040; FSD P4 v3 AC-EXC-P4-004-05; TSD P4 v3 T3.1 masking_rule |
| BR6 | The presented values keep the shape of the two contracts: a required member missing, a capability area outside LOV-CAPABILITY or a field ID that is not a personal field id of the dictionary is 422 with MSG-GEN-001 naming the member, and no business value is checked in code | DP-06; DP-07; FSD P4 v3 VR-P4-004-1 |
| BR7 | Every answer, allowed or refused, appends one access entry before the answer leaves the service, with the actor, the caller type, the agent code, the policy version, the autonomy mode, the case, the trigger event, the field IDs with their markers, the two version labels and the time, and no personal value; an entry that cannot be written withholds the answer with 503 | NFR-042; FSD P4 v3 A2.7 and AC-EXC-P4-007-03; GAP-2330; ASM-3871 |
| BR8 | One answer names one matrix version and one masking version whole: each is resolved once per call from its effective date, and a read never mixes two versions | FSD P4 v3 A2.4 and A2.5; DP-15 |
| BR9 | The answer carries policy only: no case status, no owner, no queue, no ledger entry, no document, no document field value, no rule row, no proposal and no confidence is read or answered | Architecture v5 slides 13 and 41; DP-01; DP-18; DP-20 |
| BR10 | A refusal names the reason code, the area, the right asked, the matrix version and the scope, and nothing else; it returns no limit, no field value, no case fact and no other subject's data | FSD P4 v3 VR-P4-004-1; CTL-09 pattern of the service baseline |
| BR11 | The legacy refusal of the key is kept: a role without the right is refused with 403 and MSG-P4-002, and the run of the case and event proceeds only with the reads it was admitted | Legacy RWB-E1-062 section 5 X7 and section 14; FSD P4 v3 AC-EXC-P4-001-05 |

The rules hold in `rwb_access` as follows. BR2 is one read of `role.role_class` at the matrix version in force. BR3 is one read of `permission` for the subject's roles keyed on the area and the letter; there is no second path for an agent and no exemption. BR4 is the `default_scope` value alone, and the narrower-scope refusal is explicit rather than silent. BR5 is the masking answer of RWB-P4-E1037-APP composed from the profiles of RWB-P4-AD004-APP with the default-deny default; the two fields the legacy marks masked (DF-INT-011 and DF-DOC-015) have no `unmasked` row for the agent. BR6 puts the areas, the scopes, the role classes and the personal field ids in reference data and the dictionary rather than in a Java enumeration. BR7 is the entry appender of RWB-P4-E1039-APP inside the transaction that produces the answer, and `rwb_access` holds no access-log table of its own: the access log and the decision log are one append-only chain (FSD P4 v3 A2.8, FEAT-ACA-08). BR8 is the two resolvers, called once each. BR9 is the boundary rule: the package names no case, ledger, document, deviation or agent table and calls no other service. BR10 is the problem-response mapper. BR11 keeps the legacy message id and status of the key.

### 9. State transitions

This service holds no case, run, proposal or deviation state. What it holds is the outcome of one authority answer and the lifecycle of the two versions it reads, which RWB-P4-E1019-APP and RWB-P4-AD004-APP write.

| From | Event | Condition | To |
|---|---|---|---|
| No answer | The authority question is asked | The subject is a `NON_HUMAN_ACTOR` with the letter asked and scope `ALL` | `ADMITTED`, decision code `AC-READ`, and one entry appended |
| No answer | The authority question is asked | No letter, or a role class other than `NON_HUMAN_ACTOR`, or a scope narrower than `ALL` | `REFUSED` 403 with the reason code, decision code `AC-DENY`, and one entry appended |
| No answer | The authority question is asked | A required member is missing or a value is outside its list | 422, no answer, no entry beyond the refusal |
| No answer | The authority question is asked | The entry cannot be written | 503 with MSG-P7-003, no answer, nothing admitted |
| Matrix version in force | A new version takes effect on its date | A call is dated on or after that date | The new version answers; the older rows stay readable for their own dates |
| Masking version in force | A new version takes effect on its date | A call is dated on or after that date | The new masking version answers and its markers follow it |
| Answer given | The same question is asked again for the same run | None | The same answer and a second entry: an authority answer is a read of the policy and not a state change |

The states of the run itself - PENDING, ANSWERED, GUARDRAIL_FAILED, TIMED_OUT, COMPLETED and the review marker of a low-confidence proposal - are rwb-agent's rows and rwb-agent's transitions (RWB-P10-E1062-APP), and no state of them is written here.

### 10. Authority

| Who | What they may do in this story |
|---|---|
| `SY-AGENT`, agent platform | Is the subject of an authority answer: reads its own profile, and reads through this answer only the areas, letters and field markers it is granted. Holds `R` in Rules and parameters and `R` in Reference data and no other letter for this key (TSD P4 v3 T6.1) |
| The calling `rwb-agent` service identity | Calls the authority question and the profile read and reads nothing else; its own right to the operation is answered by the guard library of DP-08. Its login name is DP-02's and is not named here |
| RW-COE, center of excellence analyst | Loads the sample and starts the evaluation (Rules and parameters CRUD), reads the run metadata (Platform administration R); this story grants it nothing beyond those rows |
| RW-RISK, risk and model risk officer | Approves the policy and prompt versions and reads the scores (Rules and parameters R and A) |
| RW-CONDUCT, conduct and QA officer | Reads the scores (Rules and parameters R) |
| RW-PLATADM, RW-AUDIT, RW-COMPLY, RW-DATASTEW, RW-SECADM | Read the run metadata through the admin read (Platform administration R); RW-SECADM owns the matrix and the masking versions this answer reads |
| RW-SECADM | Writes the `role`, `permission` and `masking_rule` versions this story reads (RWB-P4-E1019-APP, RWB-P4-AD004-APP); it holds no write path here |
| `rwb-access` itself | Reads `role`, `permission` and `masking_rule` in `rwb_access` and writes no row of any of them; it appends the access entry of an answer |
| No role | Reads a case, a ledger entry, a document, a deviation or an agent run through this service, or receives a clear personal value it holds no `unmasked` row for |

The refusal shape is 403 with an RFC 9457 problem response, `messageId` MSG-P4-002 and a `reasonCode`. The service login is the per-service login of the baseline (DP-02) and is not named here.

### 11. Data

| BR Field ID | Table in `rwb_access` | Field | Read or write |
|---|---|---|---|
| DF-REF-034 to DF-REF-039 | `role` | id, role_code, role_name, role_class, default_scope, entra_group | Read: the subject's role code, class and default scope |
| DF-REF-040 to DF-REF-044 | `permission` | id, role_id, capability_area, letters, matrix_version | Read: the letters of the subject's roles in the areas asked, at the matrix version in force |
| DF-REF-198 to DF-REF-204 | `masking_rule` | id, role_code, field_id, unmasked, masking_version, valid_from, valid_to | Read: the one marker per presented field ID at the masking version in force |
| DF-REF-027 to DF-REF-033 | `lov_value` (reference rows of rwb-case, DP-07) | lov_code, value_code, label_en, label_th, sort_order, valid_from | Read: LOV-CAPABILITY, LOV-SCOPE, LOV-ROLE-CLASS through the reference-data contract. TSD P4 v3 T3.1 gives `lov_value` to the module; in the target it is rwb-case's under the default ruling of section R3 |
| (entry) | access entry of the append-only chain, written by RWB-P4-E1039-APP | the members of BR7 | Write: one entry per answer. The member names are Not specified in the source documents (GAP-2330; ASM-3871) |
| (outbox) | `outbox_event` in `rwb_access` | the outbox row of the entry (DP-09) | Write |
| (inbox) | `processed_event` in `rwb_access` | none | None: this story consumes no event |
| (idempotency) | `idempotency_key` in `rwb_access` | none | None: an authority answer is a read of the policy and stores no answer |

No row of `recovery_case`, `interaction`, `document`, `document_field`, `deviation`, `agent_run` or `rule_row` is read or written: those tables are rwb-case's, rwb-source-data's, rwb-document's, rwb-deviation's, rwb-agent's and rwb-decision's, and the case, the trigger event, the document reference and the interaction reference arrive on the request as presented values (DP-01, DP-18, DP-20). No `recovery.v_ace_*` view is named: the personal values the agent reads are served masked by their owners and re-marked here, and this service reads no ACE data of its own. Nothing of `decision_log_entry` is written: that table is P7's, and the chain this story appends to is the service's own access and decision entry of RWB-P4-E1039-APP. Field IDs are those of the Logical Data Model and Data Dictionary v9 and of TSD P4 v3 T3.1.

### 12. Contract

#### 12.1 REST operations provided

Base `/api/recovery/access/v1`; owner P4 `rwb-access`. Both operations are the service baseline's and are published by RWB-P4-E1037-CON; this story fixes the agent-authority part of the first and the non-human part of the second, and adds no path (DP-13).

| Operation | Path | Request | Response | Errors | Authorization | Idempotency |
|---|---|---|---|---|---|---|
| POST | `/api/recovery/access/v1/authorise` | Body: `callerType` (`AGENT`), `callerCode` (`SCREENING`), `caseId`, `triggerEvent`, `policyVersion`, `autonomyMode`, `capabilityArea`, `right`, `fieldIds[]`, and no case fact beyond the case reference | `admitted`, `reasonCode`, `callerType`, `callerCode`, `roleCodes[]`, `roleClass`, `scope`, `capabilityArea`, `right`, `letters`, `matrixVersion`, `maskingVersion`, `policyVersion`, `autonomyMode`, `fieldMarkers[]` | 401 MSG-P4-001; 403 MSG-P4-002 with `reasonCode`; 422 MSG-GEN-001; 503 MSG-P7-003 | The calling service identity's right to the operation (DP-08), then the subject's letters in the area asked | Not applicable, a read of the policy; each call writes one access entry and no `Idempotency-Key` is stored |
| GET | `/api/recovery/access/v1/me/session` | None | `roleCodes[]`, `roleClass`, `scope`, `letters[]` per capability area, `matrixVersion`, `maskingVersion`, and no partner identity and no break-glass grant for a non-human actor | 401 MSG-P4-001; 403 MSG-P4-002; 503 MSG-P7-003 | The same guard right; the read answers the caller's own profile only | Not applicable, read only |

The shape of `GET /me/session` is API-P4-012 of TSD P4 v3 T-A.2, which already names `roleClass`, the matrix version and the conflict version. No source names the agent-authority part of `POST /authorise` or its request and answer element set: Architecture v5 slide 14 names the operation only and TSD P4 v3 T-A holds no row for it (GAP-2326; ASM-3867). The two operations change nothing of the service's other operations: the role catalogue read `GET /admin/roles` (API-P4-007), the access-log search `GET /admin/access-log` (API-P4-008, owned by RWB-P4-AD007-APP) and the break-glass grant `POST /admin/break-glass-grants` (API-P4-013) keep the shapes their own stories publish.

#### 12.2 REST operations consumed

None at run time. This story calls no other service: the matrix, the masking rows and the entry are in `rwb_access`, and the rest of the run's facts are presented values.

Three contracts are consumed as shapes and fixtures:

| Contract | What is consumed | Note |
|---|---|---|
| RWB-P10-E1062-CON | The run key "SCREENING:<caseId>:<eventId>", agent "SCREENING", policy "P1", mode "SHADOW", prompt "PR1", the four read tools and the two trigger events | The agent is the caller of 12.1 and the subject of the answer; the contract fixes the values this story records and tests. Its element names are Not specified in the source documents (GAP-2326; ASM-3867) |
| rwb-case reference data (DP-07, C RWB-P3-E1043-CON) | LOV-CAPABILITY, LOV-SCOPE and LOV-ROLE-CLASS at the version in force | Read through the reference-data client library; no area, scope value or role class is a literal in code |
| rwb-case parameters (DP-06, C RWB-P3-E1042-CON) | The retention window of an access entry and the feature switch `rwb.access.agent-authority` | Read through the parameters client library; no window and no switch is a constant in code |

#### 12.3 Events published

| Event | Topic | Owner | Key | Payload |
|---|---|---|---|---|
| None of its own | `rwb.access.events.v1` | P4 | None | This story adds no event type to the service's topic: the ownership rows give `rwb-access` no business event, and the matrix and masking versions stay the load stories' |
| The access entry, through the local chain | `rwb.decision-record.v1` (the shared topic of section R4) | The decision-record library, written by RWB-P4-E1039-APP | the entry ID | the members of BR7: the actor, the caller type, the agent code, the policy version, the mode, the case, the trigger event, the field IDs with their markers, the two version labels and the time |

CloudEvents 1.0 envelope; neither payload carries a name, an e-mail address, a call note, a document value or a proposal. The entry is inserted in the outbox in the same transaction as the answer and relayed by the outbox library, so an entry exists exactly when an answer exists (DP-09; BR7). The entry and its chain are the writer's of RWB-P4-E1039-APP; this story fixes the values it carries and adds no topic.

#### 12.4 Events consumed

None. Architecture v5 slide 14 gives `rwb-access` no inbound event ("none: reference data owner"), and this story adds no subscription and writes no inbox row. The agent's run events of `rwb.agent.events.v1` are consumed by rwb-reporting and rwb-case, not here.

#### 12.5 Workflows and activities

None. The authority answer is a synchronous answer of one REST request in the caller's thread, one hop, inside the 2 s client budget. `AgentRunWorkflow` and its activities are rwb-agent's on the queue `rwb-agent`; this story starts none, signals none and registers no activity on `rwb-access`.

#### 12.6 Schedules

None for this story. The six-monthly access review list (JOB-18) is a Schedule of `rwb-access` and belongs to the service's own administration story; this slice adds no Schedule and no timer.

#### 12.7 Tables owned

| Table | Owner | Use in this story |
|---|---|---|
| `role` | P4 (`rwb_access`) | Read only: the subject's role code, role class and default scope |
| `permission` | P4 (`rwb_access`) | Read only: the letters per capability area at the matrix version in force |
| `masking_rule` | P4 (`rwb_access`) | Read only: the marker per field ID at the masking version in force |
| `outbox_event` | PLT library, created in `rwb_access` | The outbox row of the access entry (DP-09) |
| `processed_event` | PLT library, created in `rwb_access` | Not used: this story consumes no event |
| `idempotency_key` | PLT library, created in `rwb_access` | Not used: this story stores no answer |
| access entry of the append-only chain | PLT library, created in `rwb_access`, written by RWB-P4-E1039-APP | The entry of an admission and of a refusal (BR7) |

`recovery_case`, `interaction`, `document`, `document_field`, `deviation`, `agent_run` and `rule_row` are never named by a query of this story, and no foreign key crosses a schema (DP-01). `masking_rule`, `role` and `permission` are read through a repository that exposes no save, update or delete, so an answer can never change a policy row.

#### 12.8 Contract fakes

| Fake | Serves | Stubs used by this story |
|---|---|---|
| RWB-P10-E1062-CON fake | The agent contract of this legacy key | The run key "SCREENING:<caseId>:<eventId>", agent "SCREENING", policy "P1", mode "SHADOW", prompt "PR1", the four read tools, and a run for a user reference of class `BANK_USER` (AC4) |
| rwb-case reference-data fake | DP-07, RWB-P3-E1043-CON | LOV-CAPABILITY with the 14 areas including `RULES_AND_PARAMETERS` and `REFERENCE_DATA`, LOV-SCOPE with `OWN`, `TEAM`, `REGION` and `ALL`, LOV-ROLE-CLASS with `BANK_USER`, `PARTNER_USER` and `NON_HUMAN_ACTOR`, each with a version in force, and an area that is absent (AC2) |
| rwb-case parameters fake | DP-06, RWB-P3-E1042-CON | The retention window of an access entry and the switch `rwb.access.agent-authority` on and off (AC6, AC8) |
| matrix and masking fixtures | RWB-P4-E1019-APP, RWB-P4-AD004-APP | `PM-2026.11` with `R` for `SY-AGENT` and `CRUD` for `RW-COE`; `PM-2026.12` effective 1 December 2026; scope `ALL` and scope `TEAM`; `MASK-SIT-01` with no `unmasked` row for the agent, `MASK-SIT-02` effective on its own date, and one field id with no row at all |
| access-entry writer double | RWB-P4-E1039-APP | The append, the hash chain check, and the forced failure of AC8 |
| gateway-bff route stub | DP-19, RWB-PLT-N001-CON | A pass-through route in front of the two operations, one hop, preserving the query and the media type |

Every fixture is synthetic; no production case, call note, document or party record is copied into a fake.

#### 12.9 Call-type summary

| Call type | Count | Detail |
|---|---|---|
| REST | 2 provided, 0 consumed | `POST /authorise` and `GET /me/session` on `/api/recovery/access/v1`, each one hop; the access-log search of API-P4-008 is read in AC6 and is RWB-P4-AD007-APP's |
| Kafka | 0 of its own, 0 consumed; 1 entry through the library | The access entry of the answer on `rwb.decision-record.v1` through the writer of RWB-P4-E1039-APP; `rwb.access.events.v1` is not extended |
| Temporal | None | No workflow, no activity and no Schedule in this slice |
| File | None | No file is read or written |

### 13. Solution plan

**Package.** `th.co.scb.ace.workbench.recovery.access`, module `access/agentauthority`, Java package `th.co.scb.ace.workbench.recovery.access.agentauthority`.

**Pattern application**

| DP | Legacy marker | Microservice pattern | Dependency added |
|---|---|---|---|
| DP-01 | `recovery.<table>` or "recovery schema" | Owner's schema `rwb_<name>`; never read another service's tables | none |
| DP-04 | RuleEvaluator, Drools | Embedded Drools kit; rule packages from rwb-decision | H RWB-PLT-E1072-CON; C RWB-P7-E1073-CON |
| DP-06 | Parameters, casewf.config | Parameters contract of rwb-case and the client library | H RWB-PLT-E1042-CON; C RWB-P3-E1042-CON |
| DP-07 | Reference data, LOV | Reference-data contract of rwb-case | H RWB-PLT-E1043-CON; C RWB-P3-E1043-CON |
| DP-09 | Application event, EV-nn, outbox | Outbox and inbox library; Kafka topic of the owner; CloudEvents | H RWB-PLT-TE006-CON |
| DP-13 | `/api/recovery/v1` | `/api/recovery/<short>/v1` | none |
| DP-15 | V0001 baseline, migration | Per-service Flyway sequence in the service's own schema | H RWB-PLT-E1044-CON |
| DP-18 | Interaction ledger | Ledger owned by rwb-source-data (default ruling) | none |
| DP-19 | Screen, ace-web | gateway-bff composite route | H RWB-PLT-N001-CON |
| DP-20 | Agent client | rwb-agent contract | C RWB-P10-TE013-CON |

This is a secondary slice: metadata "Depends on (build)" stays `None` and "Contract dependencies" stays `RWB-P10-E1062-CON` exactly as the Work Package fixes them. The H rows of the table are the platform contract libraries of the service baseline and arrive with it; the C rows are contracts this story builds against its fakes and adds no build of (ASM-3872).

- **DP-01** keeps the whole answer inside `rwb_access`: `role`, `permission` and `masking_rule` are this service's own, and no case, ledger, document, deviation, rule or agent table is read. The case, the trigger event, the document reference and the interaction reference are presented values.
- **DP-04** applies as a prohibition: the owner role of each proposed code is evaluated by the agent in the embedded kit from the rule package of rwb-decision, so this story loads no Drools kernel, no DRL and no workbook, and reads no rule row.
- **DP-06** is the parameter read: the retention window of an access entry and the switch `rwb.access.agent-authority` come from the parameters contract and client library of rwb-case, cached, so neither is a constant of the module.
- **DP-07** is the list read: the 14 capability areas, the four scopes and the three role classes are taken at the version in force that the reference-data route reports, so no area, scope or class is an enumeration of the module.
- **DP-09** is the outbox: the access entry's outbox row is written by the writer of RWB-P4-E1039-APP in the transaction that produces the answer, and the relay publishes it; a failed entry withholds the answer.
- **DP-13** gives the two operations their base `/api/recovery/access/v1`, so the agent's tool gateway calls one owner and never a monolith path.
- **DP-15** puts any index or view this slice needs in the per-service Flyway sequence of `rwb_access`, and this slice creates no table of its own.
- **DP-18** applies as a prohibition: the interaction ledger is rwb-source-data's, so the run's call notes and complaint notes are read there, and this service holds neither a ledger row nor a copy of one.
- **DP-19** is the gateway-bff composite route: the profile read and the access-log search of a screen are reached there, one hop, and no route calls a service that calls another.
- **DP-20** is the rwb-agent contract of this key: the agent is the caller and the subject, and this service imports only the contract shape of RWB-P10-E1062-CON as its fake; it never calls rwb-agent.

**Components**

| Component | Type | Responsibility |
|---|---|---|
| AgentAuthorityController | Controller | The agent-authority part of `POST /authorise` and the non-human part of `GET /me/session`: request validation, error mapping to RFC 9457 problems, the `reasonCode` of a refusal |
| AgentSubjectResolver | Service | BR2: the presented service identity to a `role` row at the matrix version in force, its role class and its role codes |
| PermissionReader | Service | BR3: the letters of those roles in the areas asked, and the letter that admits the read |
| AgentScopeService | Service | BR4: `default_scope` and its one consequence, with no team or region list |
| MatrixVersionResolver, MaskingVersionResolver | Service | BR8: the two version labels in force for the day of the call, resolved once each |
| MaskingAnswerService | Service | BR5: composed from the enforcement point of RWB-P4-E1037-APP and the profiles of RWB-P4-AD004-APP; one marker per field ID, default deny |
| AgentRequestValidator | Service | BR6: the required members, the areas against LOV-CAPABILITY and the field IDs against the dictionary, with 422 |
| AgentProfileService | Service | The `/me/session` answer for a non-human actor: roles, class, scope, letters, two versions, no partner state and no break-glass |
| AccessEntryWriter | Client of RWB-P4-E1039-APP | BR7: one entry per answer, in the transaction that produces the answer |
| LevelCatalog | Client of DP-07 | The three lists through the reference-data contract; no Java enum of areas, scopes or classes |

**Database and migrations**

- This story creates no table and owns no Flyway version of its own. `role`, `permission` and `masking_rule` are created by the service baseline of RWB-P4-E1037-APP in the per-service sequence of DP-15, and their rows are loaded by RWB-P4-E1019-APP and RWB-P4-AD004-APP; this story reads them through the repository.
- The read predicates are `role.role_code`, `role.role_class`, `role.default_scope`, `permission.role_id`, `permission.capability_area`, `permission.matrix_version` and the `masking_rule` keys `role_code`, `field_id` and `masking_version` with their date window. An index this slice needs is added to the creating story's migration, not to a new one here.
- No write statement exists in the repository for any of the three tables, so an answer can never change a permission or a masking row.
- The access entry and its outbox row commit in one transaction with nothing else to write; a failure rolls them back and the answer is not returned.

**Configuration and reference data**

- The matrix version in force and the masking version in force are data, resolved from their own effective dates; neither label is a constant.
- LOV-CAPABILITY (the 14 areas including `RULES_AND_PARAMETERS` and `REFERENCE_DATA`), LOV-SCOPE (`OWN`, `TEAM`, `REGION`, `ALL`) and LOV-ROLE-CLASS (`BANK_USER`, `PARTNER_USER`, `NON_HUMAN_ACTOR`) are read through the reference-data contract of DP-07 with the version in force.
- The reason codes of BR10 are the one enumeration of this story; they are fixed in the contract document, not spread through the classes, and every refusal carries exactly one (GAP-2327; ASM-3868).
- The feature switch `rwb.access.agent-authority` is a parameter of rwb-case read through DP-06: off means the agent-authority part answers 403 to an `AGENT` caller and writes no `AC-READ` entry, while the profile read and every other operation of the service are unchanged.
- The values of the run - run key, agent code, policy version, mode and the four tools - are the agent contract's and are never copied into the module's configuration.

**Build steps**

1. `AgentSubjectResolver` and `PermissionReader` over `role` and `permission`, with the two version resolvers; tests for AC1, AC2 and AC7.
2. `AgentScopeService` with the `ALL` rule and the `SCOPE_NOT_ALL` refusal, and the negative test that no team list is read (AC1, X6).
3. `AgentRequestValidator` with the required members, the area list and the field-ID check; tests for AC1 and X8.
4. `MaskingAnswerService` with default deny, the three masked field IDs and a field with no row at all; tests for AC5, including a marker that would be `clear` for another role only.
5. `AgentProfileService` on `GET /me/session`, including the `BANK_USER` refusal and the absence of partner and break-glass state; tests for AC3 and AC4.
6. `AccessEntryWriter` with the entry and its outbox row in one transaction; tests for AC6 and for the 503 of AC8.
7. The boundary test: the package names no case, ledger, document, deviation, rule or agent table, no `recovery.v_ace_*` view, and no Drools dependency; test for AC9.
8. The contract-fake run of RWB-P10-E1062-CON, the reference data and the parameters, so the slice builds and proves every criterion before the agent is live in DEV.

**Done when.** The tests in section 16 pass; an `AGENT` caller under `SY-AGENT` is admitted on `R` in both areas with `PM-2026.11` and `MASK-SIT-01`; a `C` request is refused with MSG-P4-002 and `RIGHT_NOT_HELD`; a `BANK_USER` subject is refused with `CALLER_KIND`; no field ID is answered `clear` for the agent; every answer leaves exactly one access entry with the agent, the policy version and the mode; the entry cannot be skipped, as AC8 proves; and the boundary test names no table of another service.

### 14. Validation and messages

| ID | When | Message | Where it is produced |
|---|---|---|---|
| MSG-P4-001 | The caller presents no valid session or workload token | You have no Recovery Workbench role. Ask your team manager to request one. | The service baseline, before any row is read |
| MSG-P4-002 | The calling identity holds no right to the operation, or the subject holds no letter, or the role class is not `NON_HUMAN_ACTOR`, or the scope is not `ALL` | You cannot {action} here. Your role does not include it. | This story, with `reasonCode` `RIGHT_NOT_HELD`, `CALLER_KIND` or `SCOPE_NOT_ALL` |
| MSG-GEN-001 | A required member is missing, or a capability area is outside LOV-CAPABILITY at the version in force, or a field ID is not a personal field id of the dictionary | Enter {field}. | This story, on the authority question |
| MSG-P7-003 | The access entry cannot be written | The action was not taken because the decision could not be recorded. Try again in a few minutes. | This story, on both operations |
| MSG-P10-002, MSG-P10-003 | The empty sample and the evaluation already running | The legacy texts, unchanged | Not produced here: they are RWB-P10-E1062-APP's, and this story adds no message to them |

Every error is an RFC 9457 problem response with `messageId` set, `detail` carrying the text with its placeholders filled and `instance` naming the request. A 403 also carries `reasonCode` and only the values that make the refusal legible: the area, the right asked, the matrix version and the scope (BR10). For MSG-P4-002 in this story, {action} names the action the caller tried, for example "read the rule and parameter values for this run", and never a case fact, a field value or a role name.

### 15. Screens and states

No screen is built in this story. The two operations are consumed by the agent's tool gateway and by the access screens of the service; no person is in the loop of a screening run.

| Screen | State | Where it is |
|---|---|---|
| SCR-43 Roles and access | List, access log, refused entry | `rwb-access` (RWB-P4-AD007-APP and RWB-P4-E1039-APP); it reads the entries this story writes |
| SCR-47 Personal data | Masked and unmasked states of a field | `rwb-access` (RWB-P4-AD004-APP); it shows the rows this story marks |
| Run metadata of agent "SCREENING" | List, detail | `rwb-agent` (RWB-P10-E1062-APP); this story serves it nothing and holds no state of it |

The gateway-bff composite route of DP-19 is the only path on which a screen reaches these reads, one hop, and the route specification and the field-level masking of the composite route are RWB-PLT-N001-CON's.

### 16. Test cases

| TC ID | Covers | Level | Data |
|---|---|---|---|
| TC-E1-062-10 | Access: the authority answer of AC1, AC2 and AC4. A role without the right is refused with MSG-P4-002, and a `C` request by the agent is refused the same way | Component | `SY-AGENT` under `PM-2026.11` with `R` only; `RW-COE` admitted on `C`; a subject of class `BANK_USER` refused with `CALLER_KIND` |
| TC-E1-062-01 | AC1, AC5 and AC9 for the authority and the masking of the run; the shadow flags themselves belong to RWB-P10-E1062-APP | Contract | 200 synthetic cases with call notes and documents; the run of case `RW-2026-000401` admitted on `R` with the two masked field IDs |
| TC-E1-062-02 | No criterion here; the comparison with the labels and the 0.9000 and 0.7500 of X6 belong to RWB-P10-E1062-APP | Component | Sample SCREEN-S1 version 1; X6 counts 18, 2, 6 |
| TC-E1-062-03 | AC1 and AC6: the run started by `EV-16 DocumentStored` names the trigger event on its entry; the run itself is the agent's | Contract | Case RW-2026-000401, document D-1001 of type DEATH_CERTIFICATE, trigger `DocumentStored` |
| TC-E1-062-04 | No criterion here; the owner role read from R-DEV-02 to R-DEV-06 is the agent's, and this service loads no rule package (AC9) | Component | X4 proposal on case RW-2026-000402; one unmapped code |
| TC-E1-062-05 | AC9: the interaction reference of the contact before the complaint is a presented value and no ledger row is read | Component | Call 2026-11-25, complaint note 2026-11-27 |
| TC-E1-062-06 | No criterion here; the review marker of a low-confidence proposal belongs to RWB-P10-E1062-APP | Component | X2 proposal with confidence 0.72 |
| TC-E1-062-07 | AC6: two answers for the same case and event append two entries, because an authority answer is a read of the policy | Component | The same question asked twice for case RW-2026-000401 and event `DocumentStored` |
| TC-E1-062-08 | No criterion here; the code guardrail belongs to RWB-P10-E1062-APP | Component | Model stub returns code X9 |
| TC-E1-062-09 | No criterion here for the model timeout; the 2 s budget and the 503 of AC8 are the ones this slice answers | NFR | Model stub silent 61 seconds; the entry writer forced to fail |

The full test, with its Given, When and Then, is in Recovery Workbench Test Cases v8.xlsx, tab Story test cases, under the same test case ID. Legacy level System maps to Component or Contract as the row shows, Access to Component, and the model stub and the timeout case to Component or NFR. Every legacy test case of the key is listed with the slice of behaviour this story answers, and no criterion is claimed for the cases whose behaviour is the agent's or the deviation's. The `-ITG` copies are not here: they belong to RWB-ITG-E1062-ITG, which proves the same values across rwb-agent, rwb-access, rwb-document, rwb-source-data and rwb-deviation end to end.

### 17. Guardrails

- No business value in code: the matrix version, the letters, the scope, the role class, the capability areas, the masking rows and the retention window are data of their owners, and only the three reason codes are fixed here (BR10, BR6). A test proves that a new matrix version, masking version or area needs no build.
- No personal data anywhere: the answer carries a caller code, a case reference, a field ID and a marker; the entry carries the same and no name, e-mail address, call note, document value or last four digits. No test data, fixture or prompt holds a personal value, and the two fields the legacy marks masked are the two the agent never receives in clear.
- Masking before the value is served: the marker is decided here and applied by the owner of the value, so a `masked` marker means no clear value reaches the model, the log or the trace.
- No read of another service's tables (DP-01, DP-18, DP-20): `recovery_case`, `interaction`, `document`, `deviation`, `agent_run` and `rule_row` are their owners', and no foreign key crosses a schema.
- ACE data only through the owner's contract or its own `v_ace_*` views: this story reads no ACE data at all, and the group-to-role mapping is the service's own concern in its own story.
- One authority path for a person, a model and an agent: there is no agent-only operation, no exemption from the letter check and no second scope rule, which is what NFR-051 and REQ-ACA-010 rely on.
- No answer without its entry: the entry commits with the answer, and the answer is withheld with MSG-P7-003 when it cannot be written (BR7).
- An answer is repeatable and unrecorded as an idempotent one: a retry answers the same and appends a second entry, as a read of policy must.
- The run, the proposal and the deviation stay with their owners: this service answers authority, records the entry and never starts, retries or advances a run.

### 18. Traceability

| Requirement ID | Requirement (short) | BRD section | Feature | L3 process | Rules | Test cases |
|---|---|---|---|---|---|---|
| REQ-DVH-001 | X1 to X7 detected from case data, call notes, documents and flags | Business Requirements Program, section 5.15 | FEAT-DVH-01, FEAT-AGT-08 | 11 Handle customer care and deviations | None | TC-E1-062-01, TC-E1-062-03, TC-E1-062-10 (the reads the detection starts from are admitted and logged here; the detection is the agent's) |
| REQ-DVH-003 | Each code routes to its named owner; an unmapped code goes to the team manager | Business Requirements Program, section 5.15 | FEAT-DVH-04 | 11 Handle customer care and deviations | R-DEV-02 to R-DEV-06 (the agent's) | TC-E1-062-04 (the rule registry read is the agent's; this service records that the run was admitted to read it) |
| REQ-DVH-007 | A complaint is matched to the contact before it | Business Requirements Program, section 5.15 | FEAT-DVH-08 | 11 Handle customer care and deviations | None | TC-E1-062-05 (the ledger is rwb-source-data's; this service admits and logs the read) |
| NFR-039 | Party identifiers are masked at rest, on every screen and every agent call, by role | Non-functional, security | FEAT-ACA-05 | All recovery processes | BR5 | TC-E1-062-01 |
| NFR-040 | Each screen and each agent receives only the personal data it needs | Non-functional, security | FEAT-ACA-05 | All recovery processes | BR5 | TC-E1-062-01 |
| NFR-042 | Every read of the case store and the document store is logged | Non-functional, audit | FEAT-ACA-07 | All recovery processes | BR7 | TC-E1-062-10, TC-E1-062-07 |
| NFR-051 | Agents run under service identities and are subject to the same role checks as people | Non-functional, security | FEAT-ACA-04 | All recovery processes | BR1, BR2, BR3 | TC-E1-062-10 |
| REQ-ACA-010 | A model or agent identity passes the same role and scope checks as a person | Epic 1 | FEAT-ACA-01, FEAT-ACA-04 | All recovery processes | BR2, BR3 | TC-E1-062-10 |

| Legacy reference | Where it is kept |
|---|---|
| Legacy story RWB-E1-062 - the authority of the run and the masking of what it reads (sections 4, 10, 14, 17; X7) | Sections 1, 2, 4, 8, 10, 14 |
| Agent "SCREENING", policy "P1", mode "SHADOW", prompt "PR1", the four read tools, the run key | Sections 1, 3, 4, 7, 12.2, 12.8 |
| MSG-P4-002 and the refusal of a role without the right | Sections 5, 7, 14 |
| The masked ledger summary and the masked document field value | Sections 2, 7, 8, 11, 17 |
| Field IDs DF-REF-034 to DF-REF-044 and DF-REF-198 to DF-REF-204 | Section 11 |
| TC-E1-062-01 to TC-E1-062-10 | Section 16 |
| Legacy key RWB-E1-062, story RWB-P4-E1062-APP, contract RWB-P10-E1062-CON, harness RWB-ITG-E1062-ITG | Metadata, sections 1, 3, 12, 19 |

The access and masking features this slice answers for one key are FEAT-ACA-04 (role to permission matrix as data), FEAT-ACA-05 (mask PDPA fields by role), FEAT-ACA-07 (access events to the access log) and FEAT-ACA-08 (the access log into the decision log), which the FSD P4 module pairs with its own requirements in RWB-E1-037, RWB-E1-039 and RWB-E1-022; this slice changes none of their designs and adds no feature of its own.

### 19. Out of scope

- The run, the orchestrator, the model call, the output schema, the guardrails, the owner-role resolution, the evaluation and the run states: RWB-P10-E1062-APP and the contract RWB-P10-E1062-CON.
- The masked document and extracted-field read the agent makes, and the `DocumentStored` event that starts a run: RWB-P5-E1062-APP.
- The interaction ledger, the call notes and the complaint notes: rwb-source-data (P1) under DP-18.
- The deviation itself - registration, pause, handling, routing and clearing: rwb-deviation (S8).
- The role catalogue and the matrix versions as rows: RWB-P4-E1019-APP. The masking profiles and their versions: RWB-P4-AD004-APP. The enforcement point on every screen and every agent call: RWB-P4-E1037-APP.
- The access-log search, its filters and its export: RWB-P4-AD007-APP (API-P4-008), read here only to prove AC6. The break-glass grant: RWB-P4-E1039-APP and RWB-P4-AD006-APP.
- The six-monthly access review list (JOB-18) and the delegation of authority table (RWB-P4-E1038-APP): no approval level and no review cadence applies to a shadow read.
- The gateway-bff composite route, the edge stories and the route specification of DP-19: RWB-PLT-N001-CON and the edge epic.
- The end-to-end proof of these values across the five services: RWB-ITG-E1062-ITG and its `-ITG` test cases.
- The `rwb_access` schema baseline, the service login, the metrics, the alerts and the runbook of this capability: the service baseline and an OPS story of this legacy key.

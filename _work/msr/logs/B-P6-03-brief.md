# Brief B-P6-03 — RWB-SVC-P6 rwb-comms, five legacy keys

Scratch brief written by the WP B-P6-03 lead for the five fan-out workers. Decision D-RCV-60.
Workspace root: the folder that holds `04 User stories`, `22 Microservice Realignment` and `_work`.

## 1. What every worker must read first

1. `22 Microservice Realignment/Recovery Workbench Microservice Story Template and Rules v1.md` — read fully (§R5.5 DP table, §R5.7 lanes, §R7.1 metadata rows, §R7.2 the 19 sections, §R7.3 fill order, §R9 gap and assumption rows).
2. `_work/msr/wp/B-P6-03.md` — your JSON line(s) are the only stories you write. Copy every metadata value from that line character for character.
3. `_work/msr/plan/ownership.json` — table, API, event and workflow owners. Owners come from here only.
4. `22 Microservice Realignment/Recovery Workbench Architecture v5 Text Extract v1.md` — slides 17 (P6 contract), 41 (service catalogue), 42 (event catalogue), 44 (job map).
5. `_work/msr/extract/Recovery Workbench Functional Specifications by Module v6/Recovery Workbench FSD P6 Communications v3.md` — A1.2, A2.19, A2.20, A2.21 and "Requirements served".
6. `_work/msr/extract/Recovery Workbench Technical Specifications by Module v5/Recovery Workbench TSD P6 Communications v2.md` — T3.1, T3.2, T5, T6.1, appendix T-A.
7. Your legacy story: `04 User stories/Recovery Workbench User Stories Epics 3 to 8 v3.md` for RWB-E4-040, RWB-E4-041 and RWB-E4-042 (headings at lines ~13476, ~13562, ~13647); `04 User stories/Recovery Workbench Administration Stories v3.md` for RWB-AD-017; `04 User stories/Recovery Workbench User Stories Epic 1 Story Files v7/RWB E1 034 Letter template management v1.md` for RWB-E1-034.
8. `_work/msr/extract/Recovery Workbench Business Rules and Routing Logic v4.md` — R-LIT-04, R-LIT-06, R-UNI-20, R-UNI-39, R-WO-47, R-WO-48.
9. `_work/msr/extract/Recovery Workbench Business Requirements Program v4.md` — REQ-DCM-010, -016, -017, -018, -019, -020 and NFR-028, NFR-074.
10. Format model: `04 User stories/Recovery Workbench Service Story Files v1/RWB-SVC-P6 rwb-comms (Communications)/RWB P6 E2021 APP Letter dispatch loop with proof of delivery from WIN v1.md` and its `... - contract v1.md` twin. Copy their structure, table shapes, tone and level of detail. Do not copy their content, their ids, their dependencies or their gap ids.

## 2. Hard rules for every file

- First line: `# <story id> <title>`. Then the two header lines, exactly:
  `SCB Collections and Recovery. Henka Group, 22 November 2026.`
  `(C) Siam Commercial Bank and Henka Pte Ltd`
- Then the metadata table `| Item | Value |` with the 20 rows of §R7.1 in order, no row removed, values copied from the WP JSON: Story key, Work type (`APP (App development)` / `CON (Contract)`), Suggested owner `TechX (suggested; any team may pick up this story)`, Service `rwb-comms`, Service epic `RWB-SVC-P6`, Wave, Business epic, Release (`<date> (tentative)`), Legacy key, Legacy disposition, Build status, Patterns applied (comma list of the WP patterns), Parallel lane, Ready to start, Depends on (build) (= H joined with `, `, or `None`), Contract dependencies (= C or `None`), Integration dependencies (= I or `None`), External dependencies (= X or `None`), PRD reference `Pending (C1)`, Status `Draft (realignment v1)`.
- Then one line: `**Change log.** D-RCV-60, 22 November 2026: <what this story is>. Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.`
- Then `### 1. Story` … `### 19. Out of scope`, the 19 names of §R7.2 in order, spelled exactly: Story, Business rationale, Preconditions, Flow, Exception paths, INVEST check, Acceptance criteria, Business rules, State transitions, Authority, Data, Contract, Solution plan, Validation and messages, Screens and states, Test cases, Guardrails, Traceability, Out of scope.
- §7 is a ```gherkin block. Every `Scenario:` line is `Scenario: ACn <title> (legacy RWB-… ACn)` or `Scenario: ACn <title> (new, D-RCV-60)`. No scenario line may lack its tag.
- §12 has subsections `#### 12.1 REST operations provided` … `#### 12.9 Call-type summary`, in that order, `None` where the element is empty.
- §16 table columns exactly `| TC ID | Covers | Level | Data |`; Level is one of Unit, Component, Contract, Integration, End to end, NFR.
- Names fixed once for this service and never varied: schema `rwb_comms`, REST base `/api/recovery/comms/v1`, topic `rwb.comms.events.v1` (plus retry and `.dlt`), events `rwb.comms.<Event>.v1`, task queue `rwb-comms` in namespace `rwb-recovery`, Java package `th.co.scb.ace.workbench.recovery.comms`.
- Never write the string `/api/recovery/v1/` and never name a monolith base as this service's own. Operations of this service are the `/api/recovery/comms/v1` paths.
- Owners only from the Ownership Map. Never declare another service's operation as provided.
- No personal data in events, logs, workflow inputs, tests or prompts: ids, codes, dates, amounts only.
- No names of people anywhere (roles and synthetic user ids such as `LIT-0101`, `LEG-0001` only). No email address. No mention of the issue tracker or of any tracker product.
- Never edit an existing file; never touch a master or a legacy story; never write a file outside your own list.

## 3. Facts you may rely on (do not re-derive, do not contradict)

**Service P6 rwb-comms.** Owns `notice`, `template`, `merge_field` (Ownership Map). Not owned and never read: `document`, `document_custody`, `document_text`, `document_intake`, `document_field`, `document_type`, `document_checklist_item`, `document_hub_parameter`, `signature_request`, `retention_rule`, `retention_action`, `case_document_check` (all P5); `recovery_case`, `task`, `timer`, `queue`, `assignment` (P3); `decision_log_entry`, `rule_row`, `rule_package*`, `approval` (P7); `interaction`, `efs_ledger_outcome`, `case_list_row` (P1); `outbound_item`, `interface_config`, `job_catalog` (P2); `deviation` (S8). `outbox_event`, `processed_event`, `idempotency_key` are the platform library objects created in `rwb_comms`.

**Operations of this service in the TSD (appendix T-A.1).** API-P6-001 POST /cases/{caseId}/notices · API-P6-002 GET /notices/{noticeId} · API-P6-003 GET /admin/templates · API-P6-004 POST /admin/templates · API-P6-005 GET /admin/templates/{templateId}/content · API-P6-006 POST /admin/templates/{templateId}/approve · API-P6-007 POST /admin/templates/{templateId}/withdraw · API-P6-008 POST /cases/{caseId}/messages · API-P6-009 POST /treatments/{treatmentId}/signature-requests · API-P6-010 GET /treatments/{treatmentId}/signature-requests · API-P6-011 POST /signature-requests/{requestId}/result. There is no custody, document-request or retention operation in any source: where a story needs one, the contract story fixes the path under the service base and records the gap.

**Events (Arch v5 slide 42).** On `rwb.comms.events.v1`: EV-13 NoticeGenerated (consumer rwb-decision), EV-14 NoticeDispatched (rwb-reporting), EV-15 NoticeDelivered (rwb-litigation, rwb-guarantee, rwb-case). Consumed by rwb-comms: EV-05 CaseStateChanged (rwb.case.events.v1), EV-06 DeviationRaised and EV-07 DeviationCleared (rwb.deviation.events.v1), EV-10 TreatmentApproved (rwb.treatment.events.v1), EV-12 PaymentMissed (rwb.payment.events.v1). EV-08 DecisionRecorded is on the shared `rwb.decision-record.v1` and is published by the local decision-record library (DP-03), never by a new event of this service. No custody, document-request or retention event exists in the catalogue: do not invent one.

**Jobs.** JOB-10 WIN notices is rwb-comms plus rwb-integration (Airflow file window plus workers); JOB-11 outbox relay is the platform's; JOB-17 retention is rwb-document's. Nothing in these five keys owns a new job in the catalogue.

**Roles and rights (TSD P6 T6.1).** RW-LITOFF Litigation CRUA · RW-LEGAL Litigation RA and Documents CRUA · RW-ENFORCE Litigation CRU · RW-CASEOWN Documents CRU and Litigation R · RW-TEAMMGR R · RW-AUDIT Internal audit R and R · RW-COMPLY Compliance and PDPA officer Documents RU and Litigation R · RW-PLATADM R · RW-CONDUCT R. Use only these.

**Rules.** R-LIT-04 withdrawn template holds generation and raises a task to the litigation officer · R-LIT-06 a new approved version resumes generation · R-UNI-20 legal hold stops every outbound action and automated decision · R-UNI-39 incident on an unrecorded decision · R-WO-47 case closes when the retention timer expires and every document carries a retention class · R-WO-48 a document with no retention class holds closure and raises a Document Hub task (5 working days).

**Requirements (Program BRD).** REQ-DCM-010 every document carries a retention class · REQ-DCM-016 legal hold overrides the retention class · REQ-DCM-017 an electronic discovery request produces every document for a named population with metadata and version history · REQ-DCM-018 a produced document carries origin, entry date, alteration flag and readers · REQ-DCM-019 retention runs by class and disposal or extension is a recorded decision · REQ-DCM-020 the records management position · NFR-028 retention classes per type, periods not set (DL26) · NFR-074 a document at the end of its period is disposed of or extended by a recorded decision.

## 4. Gap and assumption rows (both files, one row per topic)

- Ids are per legacy key: `CG-B-P6-03-<key>-<n>` and `ASM-B-P6-03-<key>-<n>`, where `<key>` is `E4040`, `E4041`, `E4042`, `AD017` or `E1034`, `n` starting at 1 and increasing. Every gap has exactly one paired assumption with the same `n`.
- In a story, a missing value reads: `Not specified in the source documents (CG-B-P6-03-<key>-<n>; ASM-B-P6-03-<key>-<n>)`. Where the same missing topic recurs in the same story, cite the same pair again; do not open a second pair for it.
- Gap row keys, all present: `id, title, source, section, description, evidence, type, area, severity, needed_by_wave, legacy_ref, owner_role, asm, proposed, wp`. `type` is one of Missing, Conflict, Ambiguous, Outdated, ID collision; `severity` P1, P2 or P3 (a thin story with no rule is P2, documentation-only is P3); `wp` is `B-P6-03`; `asm` is the paired assumption id.
- Assumption row keys, all present: `id, text, why, read, gap, applied_in, confidence, confirm, impact, wp`. `confidence` is High, Medium or Low; `gap` is the paired gap id; `applied_in` names the story sections where it is used.
- Write the rows with a single append per file, after checking which of your ids are already there, e.g.
  `python -I -c "import json,os;p=r'_work/msr/gaps/B-P6-03.jsonl';rows=[...];have=set();import io;\nimport pathlib;\ntxt=pathlib.Path(p).read_text(encoding='utf-8') if pathlib.Path(p).exists() else '';\nrows=[r for r in rows if r['id'] not in txt];data=''.join(json.dumps(r,ensure_ascii=False)+'\n' for r in rows);fd=os.open(p,os.O_WRONLY|os.O_CREAT|os.O_APPEND|os.O_BINARY);os.write(fd,data.encode('utf-8'));os.close(fd)"`
  Do not rewrite or reorder rows another worker already wrote. Then read the file back and confirm every one of your ids is present.

## 5. Fragment

`_work/msr/fragments/<id>.json`, UTF-8, valid JSON, keys: `id, epic, service, wt, lane, ready, owner, business_epic, wave, release, legacy, disposition, H, C, I, X, acs, tcs, reqs, ops_provided, ops_consumed, events_published, events_consumed, workflows, prd_ref, gaps, assumptions, file`.
`release` is the bare plan date without `(tentative)`. `acs` is a list of `{"id","origin","text_first_line"}` where `text_first_line` is the scenario line text without the origin tag. `gaps` and `assumptions` list every id you opened for that story. `file` is the ROOT-relative path with forward slashes. `reqs` is `[]` unless the WP JSON gives requirements.

## 6. Content brief per legacy key

### 6.1 RWB-E4-040 — Record a custody movement of a document (APP + CON)

Legacy: `RWB-E4-040` in Epics 3 to 8 v3, module P6, FEAT-COM-06, depends FEAT-DCM-19, screen SCR-33, TCs TC-E4-040-01..04, two ACs (AC1 record, AC2 decision log not written). FSD A2.19 adds: integration point the Workbench document hub, prerequisite FEAT-DCM-19, primary actor "None; runs unattended", also Legal counsel. TSD T3.1 has no custody table, and the Ownership Map gives `document_custody` to P5.

Target shape for both files: the physical document is rwb-document's (`document`, `document_custody`); rwb-comms owns the notice and keeps the movement reference on its side, records the movement through the rwb-document contract, writes the decision record through the local library, and serves the movement on its own contract. Patterns applied: DP03, DP13, DP19 only — no DP01, so this service declares no custody table; say so and make it a rule.
- CON baseline fixes two operations under `/api/recovery/comms/v1`: `POST /notices/{noticeId}/custody-movements` (record one movement, 201) and `GET /notices/{noticeId}/custody-movements` (list them, 200), with the movement fields the legacy data names — `document_id`, `moved_at`, `from_location`, `to_location`, `held_by` — and the seventh `document_custody` field as the placeholder. Record that no source names a custody operation.
- APP story: the officer records the movement, the service refuses a movement on a notice that is not in an allowed state or whose document is missing, writes the decision record before the change (DP-03) and answers on the read. The decision code and rule id of a custody movement are not stated in any source: fix that as a gap and an assumption, never invent a code.
- AC1 of the legacy story is kept verbatim; add one `Given the rwb-document contract mock returns …` line for the cross-service part. AC2 is kept verbatim. Do not add business values.
- Expected gaps: (1) module versus owner conflict on `document_custody` and the absence of a C row for the P5 document contract; (2) no custody operation in the API specification; (3) the seventh `document_custody` field and the movement field types; (4) the decision code and rule id of a custody movement; (5) whether a movement is allowed on a closed case and on which notice states (legacy and FSD say nothing). Four to five gaps is right.

### 6.2 RWB-E4-041 — Answer a legal or audit document request (APP + CON)

Legacy: `RWB-E4-041`, module P6, FEAT-COM-07, depends FEAT-DCM-06, screen SCR-33, TCs TC-E4-041-01..04, two ACs (AC1 answer, AC2 decision log not written). FSD A2.20: primary actor Legal counsel, also Internal audit and Compliance and PDPA officer, integration point the Workbench document hub, prerequisite FEAT-DCM-06.

Target shape: the answer is assembled on the rwb-comms side from its notices (the index entries: notice id, case id, document id, notice type, sent date, barcode, callback date, delivery status — the TSD T3.1 fields) and from the documents rwb-document produces on its discovery contract (REQ-DCM-017, REQ-DCM-018). Patterns DP03, DP13, DP19 only.
- CON fixes `POST /cases/{caseId}/document-requests` (open and answer, 201 with the answer) and `GET /document-requests/{requestId}` (read the answer with its index entries), and records that no source names a document-request operation.
- Expected gaps: (1) no C row for the rwb-document discovery contract although the documents and their version history are P5's; (2) no operation in the API specification and no answer shape; (3) the selector conflict — REQ-DCM-017 asks for "a named population", the legacy story asks per request on a case; (4) the legacy screen SCR-33 Template approval is named for a document request, which is a different screen; (5) whether the answer is a file or a JSON list and how a produced document is protected (REQ-DCM-018 fields). Four to five gaps.

### 6.3 RWB-E4-042 — Apply retention on case closure (APP + CON)

Legacy: `RWB-E4-042`, module P6, FEAT-COM-08, depends FEAT-DCM-17, screen SCR-33, TCs TC-E4-042-01..04, two ACs (AC1 apply retention, AC2 decision log not written). FSD A2.21: primary actor "None; runs unattended", also Compliance and PDPA officer, integration points the Workbench document hub and Blob storage, prerequisite FEAT-DCM-17. Ownership Map: `retention_rule` and `retention_action` are P5's, JOB-17 is rwb-document's.

Target shape: rwb-comms consumes `rwb.case.CaseStateChanged.v1` (EV-05, the catalogue names rwb-comms as a consumer), and on closure checks every notice document of the case through the rwb-document contract for its retention class, writes the decision record with the rule version, and where a class is missing raises the Document Hub task and asks rwb-case to hold closure under R-WO-48. It never sets the class itself: the class and its period are P5's reference data (NFR-028, DL26). Patterns DP03, DP13, DP19 only, and no new workflow and no Schedule: the trigger is the event, not a Temporal Schedule.
- CON fixes `GET /cases/{caseId}/retention-coverage` (read, 200, the notice documents with class present or absent), records that no source names the operation, and fixes the consumed event element.
- Expected gaps: (1) module versus owner conflict and no C row for the P5 retention contract; (2) no operation and no answer shape; (3) the case-hold fact this service may send to rwb-case on R-WO-48 is not specified (operation, reason code); (4) the retention classes and periods are unset (NFR-028, DL26) and are not this service's data; (5) the legacy screen SCR-33 does not fit a retention run. Four to five gaps.

### 6.4 RWB-AD-017 — Manage letter and notice templates (APP + CON)

Legacy: `RWB-AD-017` in Administration Stories v3, module P6, FEAT none, depends RWB-E1-034, decision DL28, screen SCR-33, TCs TC-AD-017-01..04, two ACs (AC1 approve, AC2 withdraw and hold). Ownership Map: `template` is P6's; the operations are API-P6-003..007 on `/api/recovery/comms/v1`.

Target shape: this is the Epic 8 administration surface on top of `RWB-P6-E1034-APP` — list by code, language and state with paging, upload, download the body, approve with valid from, withdraw with a reason, and raise the litigation officer task on a withdrawn template under R-LIT-04. E1034 keeps the Epic 1 upload-and-approve core unchanged (rule U2 and §R6): say so and do not re-plan E1034. Patterns DP03, DP05, DP13, DP19: DP-05 applies as the prohibition (no `v_ace_*` read and no ACE row by this service; ACE facts arrive on the owner's contract), and the value sets of TSD T3.2 are read with the version in force.
- Expected gaps: (1) the two legacy stories overlap (E1-034 and AD-017 both approve and withdraw) and the split of the surface is not stated — record the split as an assumption; (2) no C row for the reference-data read of the product group, channel and notice type lists; (3) the legacy ACs carry no values (no valid-from rule, no reason rule), and the messages MSG-P6-005, MSG-P6-003 and MSG-GEN-004 come from E1034's contract; (4) the withdrawn-template task target and how the held generation resumes under R-LIT-06 are not specified for this story; (5) no template event exists in the catalogue. Four to five gaps.

### 6.5 RWB-E1-034 — Letter template management (APP only, disposition Moved (no impact))

The legacy file is already a full 19-section story with AC1..AC10 and TCs TC-E1-034-01..11. Keep its content: sections 1–11, 14, 15, 17, 18 and 19 stay as the legacy text, with only these changes:
- the metadata table of §R7.1 replaces the legacy table, values from the WP JSON (wave 1, release 30 November 2026, H = RWB-PLT-E1043-CON, RWB-PLT-N001-CON, RWB-P6-E1046-APP; C = RWB-P3-E1043-CON, RWB-P1-E1015-CON; legacy dependencies RWB-E1-046 becomes `RWB-P6-E1046-APP`, RWB-E1-015 becomes the freshness read of `RWB-P1-E1015-CON`);
- §7 keeps all ten scenarios word for word and adds the tag `(legacy RWB-E1-034 ACn)` to each scenario line, plus the Background kept as is;
- §12 is rewritten into 12.1–12.9 on base `/api/recovery/comms/v1` with the five operations as the TSD names them (`/admin/templates`, `/admin/templates/{templateId}/content`, `/admin/templates/{templateId}/approve`, `/admin/templates/{templateId}/withdraw`), the legacy `/templates` paths recorded as the legacy names and the disagreement recorded as a gap;
- §13 is rewritten for the target: package `th.co.scb.ace.workbench.recovery.comms`, schema `rwb_comms`, per-service Flyway, the platform naming and library rows, the same build steps and the same feature switch `rwb.comms.template-admin`;
- §16 keeps TC-E1-034-01..11 with the Level column (legacy System maps to End to end, Access to Component) and adds the contract test the contract tables need if the story carries them;
- §12.1 must also say that "set current" of legacy AC2 is not an operation: the current version is the Approved version with the latest valid from (assumption, because the target has no set-current operation).
- Patterns DP01, DP07, DP13, DP19. `reqs` is `["REQ-OCC-002"]`.
- Expected gaps: (1) the `/templates` versus `/admin/templates` disagreement between the legacy story and the TSD; (2) "set current" has no target operation; (3) the legacy property values `rwb.comms.template.allowed-types` = DOCX and `rwb.comms.template.max-size-mb` = 10 are marked "assumed" in the legacy text; (4) whether the template body is a P5 document-hub object or the service's own container (the legacy stores `body_ref` and the target gives file custody to P5). Three to four gaps.

## 7. Reply to the lead

State: the files written, the ids of your gap and assumption rows, the legacy AC ids you copied with their tags, the legacy TC ids you carried, and any conflict you hit. Do not run the checks; the lead runs them.

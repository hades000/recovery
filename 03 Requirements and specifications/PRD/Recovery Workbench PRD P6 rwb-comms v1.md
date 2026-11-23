SCB Collections and Recovery. Henka Group, 22 November 2026.
(C) Siam Commercial Bank and Henka Pte Ltd

---
title: Recovery Workbench PRD P6 rwb-comms v1
description: Product requirements for the Recovery Workbench communications service (P6 rwb-comms) in the 19-service realignment; capabilities, functional and non-functional requirements, data and integration requirements, release slices by wave and acceptance criteria.
status: Draft
brd: 03 Requirements and specifications/Recovery Workbench Business Requirements Program v5.md; 03 Requirements and specifications/Recovery Workbench Business Requirements Epic 1 v5.md; 03 Requirements and specifications/Recovery Workbench Business Requirements Epic 2 v3.md
fsd: 03 Requirements and specifications/Recovery Workbench Functional Specifications by Module v6/Recovery Workbench FSD P6 Communications v3.md
service: P6 rwb-comms
epic: RWB-SVC-P6
wave: 1
decision: D-RCV-60
---

# Recovery Workbench PRD P6 rwb-comms v1

# 1. Document control and change log

## 1.1 Document control

| Attribute | Value |
|---|---|
| Document title | Recovery Workbench PRD P6 rwb-comms |
| Document ID | P6-RWB-PRD-v1 |
| Version | 1 |
| Status | Draft |
| Classification | Confidential |
| Date | 22 November 2026 |
| Service | P6 rwb-comms |
| Service epic | RWB-SVC-P6 |
| Wave | 1 |
| Business epics | EP01 (Epic 1, wave 1); EP02 (Epic 2, wave 2); EP04 and EP05 (wave 3) |
| Schema | `rwb_comms` |
| REST base | `/api/recovery/comms/v1` |
| Topic | `rwb.comms.events.v1` |
| Temporal task queue | `rwb-comms` |
| Java package | `th.co.scb.ace.workbench.recovery.comms` |
| Product owner role | Product owner (section 13) |
| Requirement owner role | Litigation business owner, with the conduct and QA officer and Compliance |
| Decision | D-RCV-60 (microservice realignment); inherits D-RCV-35 and ADR-010 |
| Upstream artifacts | Business Requirements Program v5; Business Requirements Epic 1 v5; Business Requirements Epic 2 v3; FSD P6 Communications v3; Architecture v5; Microservice Ownership Map v1 |
| Upstream requirement IDs | REQ-OCC-001 to REQ-OCC-011; REQ-ILG-010; REQ-DRI-006, REQ-DRI-007; REQ-APD-006; REQ-ACA-005, REQ-ACA-006; NFR-004, NFR-008, NFR-011, NFR-020, NFR-021, NFR-022, NFR-023, NFR-025, NFR-026, NFR-027, NFR-028, NFR-030, NFR-031, NFR-033, NFR-034, NFR-035, NFR-038, NFR-039, NFR-040, NFR-042, NFR-044, NFR-046, NFR-047, NFR-049, NFR-051, NFR-052, NFR-053, NFR-054, NFR-058, NFR-059, NFR-064, NFR-067, NFR-068, NFR-075, NFR-077 |
| Upstream acceptance criteria | AC-P6-001-01, AC-ALT-P6-001-01 to -02, AC-EXC-P6-001-01 to -07; AC-P6-002-01, AC-ALT-P6-002-01 to -02, AC-EXC-P6-002-01 to -07; AC-P6-003-01, AC-ALT-P6-003-01 to -02, AC-EXC-P6-003-01 to -09; AC-P6-004-01, AC-ALT-P6-004-01 to -02, AC-EXC-P6-004-01 to -09; AC-P6-005-01 to AC-EXC-P6-007-18 (document generation); AC-P6-008-01, AC-ALT-P6-008-01 to -02, AC-EXC-P6-008-01 to -06; AC-P6-009-01 to AC-EXC-P6-009-06; AC-EXC-P6-014-01 to -02; AC-EXC-P6-018-01 to -02; AC-BG-P6-001-01 to AC-BG-P6-021-01 |
| Upstream feature IDs | FEAT-OCC-01 to FEAT-OCC-13; FEAT-COM-01 to FEAT-COM-08 |
| Upstream API IDs | API-P6-001 to API-P6-011 |
| Upstream event IDs | EV-05, EV-06, EV-07, EV-10, EV-12, EV-13, EV-14, EV-15 |
| Upstream interface IDs | INT-14 (WIN), INT-17 (NSS), INT-18 (LINE OA) |
| Upstream job | JOB-10 (WIN notices, 16:00) |
| Generated IDs | CAP-P6-001 to CAP-P6-013; FR-P6-001 to FR-P6-038; NFR-P6-001 to NFR-P6-024; AC-P6-001 to AC-P6-034; ROL-P6-01 to ROL-P6-10; JRN-P6-01 to JRN-P6-05; OQ-P6-01 to OQ-P6-10 |
| Run ID, branch, commit, pull request | Not applicable. This run writes documents only: no repository branch, commit or pull request is created, and no issue tracker is read or updated (rule 3, U6) |
| Source baseline | FSD P6 Communications v3 (15 November 2026) and the BRD Program v5 / Epic 1 v5 / Epic 2 v3, realigned to Architecture v5 under D-RCV-60 |

## 1.2 Change log

| Version | Date | Change | Tool |
|---|---|---|---|
| 1 | 22 November 2026 | D-RCV-60 microservice realignment | T3 Code / OpenCode / DeepSeek v4.1 Flash |

This is version 1 of the PRD P6 family: the folder holds no earlier PRD for this service, so there is no earlier version to supersede (ASM-2744).

## 1.3 Inherited history and ID continuity

The product baseline is FSD P6 Communications v3. Its history and ID set are carried unchanged; the microservice realignment changes the owner of the dispatch, the read path for the contact data and the proof of delivery, and the delivery wave, not the requirement substance.

| Version | Date | Change carried from the FSD |
|---|---|---|
| 1 | Before 28 October 2026 | The module was written inside the monolith: letters and notices prepared by hand, proof of delivery chased by phone. |
| 2 | 28 October 2026 | The module was restated as 21 features FEAT-OCC-01 to FEAT-OCC-13 and FEAT-COM-01 to FEAT-COM-08, with the notification path, the document hub and the decision log reached through their own interfaces. |
| 3 | 15 November 2026 | Re-based on the ACE database under D-RCV-35 (ADR-010): source data is read only through `recovery.v_ace_*` views and lands through ACE ingestion; no inbound load, load run or data quality exception in the Workbench. Payment acceptance criteria read `v_ace_payment`, proof of delivery reads `v_ace_pod`, collateral comes from ACE views, and contact points come from `v_ace_contact` plus `contact_point_ext`. Everything else unchanged from v2. |
| 1 (PRD) | 22 November 2026 | First PRD of this family. CAP, FR, NFR, AC, ROL, JRN and OQ IDs are new; the FSD requirement IDs (REQ-OCC-001 to REQ-OCC-011), the feature IDs (FEAT-OCC-01 to -13, FEAT-COM-01 to -08), the acceptance criteria IDs (AC-P6-xxx, AC-ALT-P6-xxx, AC-EXC-P6-xxx, AC-BG-P6-xxx), the API IDs (API-P6-001 to API-P6-011), the interface IDs (INT-14, INT-17, INT-18), the job ID (JOB-10), the event IDs (EV-13, EV-14, EV-15), the lists of values (LOV-NOTICE, LOV-DELIVERY, LOV-SENT-TYPE, LOV-SIGN-METHOD, LOV-SIGN-STATUS, LOV-SIGNATURE-BASIS, LOV-CHANNEL, LOV-LANG, LOV-PRODUCT), the rule references (VR-P6-nnn-n, BR-P6-nnn, R-LIT-04, R-LIT-09, R-UNI-34, R-UNI-39, R-UNI-40) and the message IDs (MSG-P6-001, MSG-P6-002, MSG-P6-003, MSG-P6-008, MSG-P6-009, MSG-P1-001, MSG-P4-002, MSG-P7-003, MSG-GEN-001, MSG-GEN-004, MSG-GEN-006, MSG-P5-002, MSG-P5-009, MSG-P5-010, MSG-P5-011, MSG-P5-013, MSG-P5-014) are preserved character for character |

## 1.4 Documents this PRD is read against

| Document | Type | Relationship |
|---|---|---|
| Recovery Workbench Business Requirements Program v5 | BRD | Source of the business requirements REQ-OCC-001 to REQ-OCC-011 and the non-functional requirements |
| Recovery Workbench Business Requirements Epic 1 v5 | BRD | Source of RWB-E1-034, RWB-E1-046, RWB-E1-052 and RWB-E1-055, the template and notice work of wave 1 |
| Recovery Workbench Business Requirements Epic 2 v3 | BRD | Source of RWB-E2-018, RWB-E2-021 and RWB-E2-022, the dispatch, proof-of-delivery and e-signature work of wave 2, and of DL28 and DL30 |
| Recovery Workbench Functional Specifications by Module v6, FSD P6 Communications v3 | FSD | Pair: the functional baseline this PRD re-expresses as product behaviour |
| Recovery Workbench Technical Specifications by Module v5, TSD P6 Communications v2 | TSD | Pair: object and field definitions, the lists of values, INT-14, INT-17 and INT-18, and the API inventory API-P6-001 to API-P6-011 |
| Recovery Workbench Architecture v5 | Architecture | Constraint: 19 services, one schema and login per service, Kafka, Temporal, the edge and gateway, no data lake |
| Recovery Workbench Temporal and Drools Design v1 | Design | Constraint: task queue, workflow kit, rules governed centrally and evaluated in the owning service |
| Recovery Workbench Microservice Ownership Map v1 | Ownership | Owner of every table, operation, event, job and workflow |
| Recovery Workbench Non Functional Specification v3 | Non-functional | Source of the numeric targets |
| Recovery Workbench Microservice Story Template and Rules v1 | Rules | Header, versioning, placeholder and register rules |

# 2. Product overview and relationship to ACE

## 2.1 Purpose

rwb-comms (P6) is the recovery module's one place where a customer is told something. It turns "letters and notices are prepared by hand and proof of delivery is chased by phone" into a product: a versioned template catalog that only Legal can approve, a notice generated from case facts without re-keying, a daily dispatch window to the registered-mail printer, a proof of delivery that returns to the case and starts the notice period, a message on the channel the customer actually uses, a conduct check and a consent rule that are applied before anything leaves, and an electronic signature request that returns the signed agreement to the case. It is the service that makes the notice period countable from proof rather than from printing.

## 2.2 What is new in this release

| New | What it is | Business reason |
|---|---|---|
| The service rwb-comms | One deployable with its own API and worker, schema `rwb_comms`, login, topic `rwb.comms.events.v1`, task queue `rwb-comms` and lifecycle | Letters, notices and messages become one owned contract instead of a module inside a single deployable |
| The template and merge-field catalog as a product | Versioned template rows with a Legal approval per version, and a merge-field catalog that states which field supplies which merge code | A template change is a data release approved by Legal, not a code release |
| The daily dispatch window as a product behaviour | One file per business date, written in the 16:00 window (JOB-10) and delivered by rwb-integration | Notice periods start from a dispatch that can be evidenced |
| Proof of delivery back on the case | Barcode, callback date and delivery status on the notice, and the notice period counted from delivery | The notice period is counted from proof, not from printing |
| The conduct and consent gate | A conduct check result on every outbound contact, a contact stop that holds every channel, and statutory notices that continue when consent is withdrawn | A contact the bank should not make is not made, and a statutory notice is still served |
| The notice and message events | NoticeGenerated, NoticeDispatched and NoticeDelivered on `rwb.comms.events.v1` | The case, litigation, guarantee and reporting act on a notice without reading this service's tables |
| The e-signature request flow in the owning service | One request per document with the signature basis applied, and the signed copy returned to the case | A settlement completes without paper where the law allows |

## 2.3 What is reused, and what leaves the service

| Capability | Verdict | Owner in v5 |
|---|---|---|
| ACE common sign-in, access check, audit and PII logging | REUSE | ACE common; P4 rwb-access for roles, scope and masking policy |
| The ACE notification path to NSS and LINE OA (SMS and LINE) | REUSE, called by this service | ACE common (INT-17, INT-18) |
| Contact points, consent state and their verification | REUSE, read and written through one contract | P1 rwb-source-data (`v_ace_contact`, `contact_point_ext`) |
| Case, case state, queues, transfer and timers | REUSE | P3 rwb-case |
| Document generation, the document store and the signature record | REUSE | P5 rwb-document |
| Decision record, approval routing and the central ledger | REUSE | P7 rwb-decision |
| Rule governance for the conduct and consent rules | REUSE | P7 rwb-decision, evaluated in this service |
| The WIN file window and the file transport | REUSE | Bank Airflow opens the window; P2 rwb-integration delivers the file |
| The customer screen, the partner portal and the batch edge | REUSE | gateway-bff and the partner gateway (ADR-019); P3, S9 |
| Match a payment to the plan (FEAT-OCC-10) and raise the plan payment missed event (FEAT-OCC-11) | MOVED | P8 rwb-payment (it publishes PaymentMissed) |
| Publish the steering dashboard (FEAT-OCC-12) | MOVED | P9 rwb-reporting |
| Give partners identities through the external gateway (FEAT-OCC-13) | MOVED | S9 rwb-partner with P4 rwb-access, on the partner gateway |
| Maintain the contact repository (FEAT-COM-05) | SPLIT: enforcement stays here, the data is P1's | P1 rwb-source-data for the contact point and its consent state |
| Record a custody movement (FEAT-COM-06), answer a legal or audit document request (FEAT-COM-07), apply retention on case closure (FEAT-COM-08) | MOVED | P5 rwb-document |
| View the offer, accept it, pay and raise a dispute in self-service (FEAT-COM-01 to FEAT-COM-04) | SPLIT: the message that carries the offer stays here | S2 rwb-treatment, P8 rwb-payment, P3 rwb-case and S8 rwb-deviation, through gateway-bff |

## 2.4 Constraints confirmed in Architecture v5 that bound the product

1. One ACE PostgreSQL server; a schema and a login per service; only rwb-source-data reads the `recovery.v_ace_*` views, so this service reads contact and proof data through that contract (ADR-010, ADR-014, DP-05).
2. The service writes only schema `rwb_comms`; no cross-schema join and no foreign key into another schema (ADR-014, DP-01).
3. REST is one hop from gateway-bff with a 2 s timeout; anything longer is a workflow (ADR-020, DP-11).
4. Events are CloudEvents on Kafka with outbox and inbox; topic `rwb.comms.events.v1`; retry and `.dlt` topics (ADR-015, DP-09, DP-14).
5. Temporal namespace `rwb-recovery`, task queue `rwb-comms`; `NoticeDispatchWorkflow` is a kit template; a schedule replaces a Quartz job and the shared Quartz tables are not used (ADR-016, DP-10).
6. Rules are governed in rwb-decision and evaluated in this service with the embedded rule kit; a decision record is written locally and sealed in the central ledger (ADR-017, ADR-022).
7. Personal data stays out of events, workflow inputs and logs; the notice and the message are personal data at rest and are masked by role on every read (Arch v5 slide 45, NFR-039, NFR-040).
8. The service has no data lake and no dashboard connection; the dispatch and delivery facts reach reporting as events (ADR-018, DP-17).

# 3. Personas and roles

Roles only; no person is named anywhere in this document.

| ID | Persona | What they need from this product | Primary journeys |
|---|---|---|---|
| ROL-P6-01 | Litigation officer | A demand or recall notice generated from an approved template, approved, dispatched and proved, with the notice period counted from proof | JRN-P6-02, JRN-P6-03 |
| ROL-P6-02 | Litigation officer team | A held notice with its reason and a task, so a withdrawn template does not stop the file silently | JRN-P6-02, JRN-P6-03 |
| ROL-P6-03 | Case owner | To reach the customer on the channel they use, and to see every contact with its result and conduct state on the case | JRN-P6-04, JRN-P6-05 |
| ROL-P6-04 | Conduct and QA officer | A conduct check result on every outbound contact, and a blocked contact that leaves a record | JRN-P6-04 |
| ROL-P6-05 | Compliance and PDPA officer | Consent applied per channel, statutory notices that continue, masking by role, and a retention class on every record | JRN-P6-04 |
| ROL-P6-06 | Legal counsel | Wording approved per template version and recorded against it, and a wet-ink requirement that overrides an electronic signature | JRN-P6-01, JRN-P6-05 |
| ROL-P6-07 | Restructuring officer (FCR) | The deed in lieu document set generated from templates and sent for signature, with the signed copy back on the case | JRN-P6-05 |
| ROL-P6-08 | Customer (borrower) | The offer and the signature on LINE and the web, in their own language, and no contact on a channel they have withdrawn from | JRN-P6-04, JRN-P6-05 |
| ROL-P6-09 | Platform administrator | A dispatch window that runs, an exception queue with a named owner, and an alert when the window or a send fails | JRN-P6-03 |
| ROL-P6-10 | Product owner | Capabilities, requirements and acceptance criteria that can be approved, and one owner for each behaviour | All |

Non-human actors: the bank scheduler (Airflow) that opens the WIN file window; `NoticeDispatchWorkflow` on the `rwb-comms` task queue; the outbox relay; the notification path to NSS and LINE OA; the consumers of the three published events. The bank Airflow sits outside the 19 services and calls no schema (Arch v5 slides 32 and 44).

# 4. User journeys

## 4.1 Current state (as recorded in the sources)

1. Letters and notices are prepared by hand, and proof of delivery is chased by phone (FSD P6 A1.3).
2. A template is uploaded and Legal approval recorded through a screen this epic adds, so today a template change is not a data release (Epic 1 RWB-E1-034; Epic 2 DL28).
3. The notice period is counted from printing rather than from proof, which is the outcome Epic 2 RWB-E2-021 changes ("the notice period is counted from proof, not from printing").
4. A conduct check result on every outbound contact is a requirement of this release (REQ-OCC-005), set by the conduct and QA officer.
5. Consent per channel and the statutory exception are requirements of this release (REQ-OCC-006), and the contact point that carries them is a source-data record (`v_ace_contact` with `contact_point_ext`).

Consequence: the notice period is counted from printing, not from proof (Epic 2 RWB-E2-021), and a contact that should have been held has no recorded result to show for it (REQ-OCC-005).

## 4.2 Target state (this product)

### JRN-P6-01 Template approved and made current (Legal counsel, per template change)

1. The template maintainer uploads a new version of a template code with its language, product group, channel, notice type and signature basis; the version starts in DRAFT.
2. The merge codes the template uses are checked against the merge-field catalog version in force; a merge code that is not in the catalog is refused whole with its message.
3. Legal counsel approves the version; the approval is recorded against the version with the approver role, the date and a decision record, and the version becomes the current one from its valid-from date.
4. A later version supersedes it without a code release; the superseded version stays readable, and a document already generated keeps the version it was generated from.
5. Legal counsel may withdraw a version; from that moment no notice is generated from it and any notice already created from it is held.

### JRN-P6-02 Notice generated and approved (litigation officer, on the case)

1. The officer requests a notice on the case with a notice type (DEMAND, RECALL, STATUTORY_SALE_NOTICE or GUARANTOR_NOTICE) and the template the rule proposed.
2. The service merges the case facts through the case service, the customer and contact facts through the source-data service, and asks the document hub to generate the letter; a required merge field with no value refuses the request whole.
3. The notice is created with its state and the template code and version it used; a repeat of the same request returns the first notice and creates nothing.
4. The notice is approved through the approval path; the approval and the rule that proposed the notice are on the decision record.
5. A notice whose template was withdrawn after approval is HELD with the reason `TEMPLATE_WITHDRAWN`, kept out of the file, and a task is raised to the litigation officer team.
6. A notice held because the data behind it is stale names the data product and its business date, and clears only when the data is current.

### JRN-P6-03 Letter dispatched at 16:00 and proof of delivery returns (unattended, daily)

1. At 16:00 on the business date, the dispatch workflow collects every APPROVED notice of the date and writes one file in the window the bank Airflow opens; a rerun for the same date replaces the file and duplicates no notice.
2. The file is delivered to WIN by rwb-integration; every letter in it carries a conduct check result of PASSED, and the ledger entry for the letter names the barcode once WIN acknowledges it.
3. The notice records the sent date, the barcode and the dispatch file; a notice that cannot be written because a layout field is missing is held with its reason.
4. The proof of delivery for the business date is read by barcode and applied: DELIVERED sets the notice to Delivered with the callback date and publishes NoticeDelivered, which starts the notice period timer on the case; UNDELIVERABLE sets it to Unserved, writes the decision record D7.1 under rule R-LIT-09, transfers the case to the owner's queue with reason `NOTICE_UNSERVED`, and starts no timer.
5. A proof of delivery that matches no notice is listed for the operations queue and never creates a notice.

### JRN-P6-04 Customer reached on SMS or LINE under the conduct and consent rules (case owner)

1. The case owner sends a message on SMS or LINE from an approved template, in the customer's language, to a verified contact point.
2. The conduct check runs before anything leaves; a contact stop that is in force refuses the send, and so does a channel the customer has withdrawn consent from, each with its own message and a BLOCKED record.
3. A statutory notice still goes out on the postal channel when consent is withdrawn, marked as such, because a statutory notice is not a marketing contact.
4. A successful send returns its result; the delivery state (DELIVERED, READ or FAILED) and the channel reference are recorded, and a failure raises the contact point's failed count.
5. A channel that is unavailable queues the send and retries it; after the retry limit the item sits in the exception queue with a task for a named owner.

### JRN-P6-05 Agreement signed electronically or on paper (restructuring officer, Legal counsel)

1. The officer generates the deed in lieu document set from approved templates; a set is stored whole or not at all, and a template version that Legal has not approved refuses the set.
2. The officer sends the reviewed documents for signature; a document whose signature basis is `WET_INK_REQUIRED` refuses an electronic signature with its message.
3. The customer signs on the bank's signing channel or on paper at a branch; the result returns to the request, and the signed copy is stored as a write-once version on the case.
4. The treatment records signed or not signed once; a repeat of the same result changes nothing and is counted.
5. An offer that expires cancels the request; a result that arrives after expiry stays on the exception queue and is not applied.

# 5. Capabilities and features

Each capability is one releasable slice of product behaviour. Priorities follow the BRD: Must is needed for the epic to release; Should is planned in the epic.

| CAP ID | Capability | What changes for the user | BR IDs | MoSCoW | Wave | FSD features |
|---|---|---|---|---|---|---|
| CAP-P6-001 | Versioned template catalog with a Legal approval per version | A template change is a data release Legal has approved, and every letter states the version it used | REQ-OCC-001, REQ-OCC-002 | Must | 1 | FEAT-OCC-01 (A2.1), FEAT-OCC-07 (A2.7) |
| CAP-P6-002 | Notice generation from an approved template with case facts merged | A demand, recall, statutory sale or guarantor notice is produced without re-keying | REQ-OCC-001 | Must | 1 | FEAT-OCC-01 (A2.1) |
| CAP-P6-003 | Template and data gate on a notice | A notice from a withdrawn template, or on stale data, is held and seen, never sent silently | REQ-OCC-001, REQ-OCC-002 | Must | 1 and 2 | FEAT-OCC-01 (A2.1), FEAT-OCC-02 (A2.2) |
| CAP-P6-004 | Daily dispatch window to WIN | Every approved notice of the business date leaves in one evidenced file at 16:00 | REQ-OCC-003, REQ-DRI-006, REQ-DRI-007 | Must | 2 | FEAT-OCC-02 (A2.2) |
| CAP-P6-005 | Proof of delivery on the notice and the notice period | The notice period is counted from proof, and an unserved notice moves the case | REQ-OCC-003, REQ-ILG-010 | Must | 2 | FEAT-OCC-02 (A2.2) |
| CAP-P6-006 | SMS and LINE dispatch through the bank's notification path | The customer is reached on the channel they use, with the result on the case | REQ-OCC-004, REQ-ILG-010 | Must | 2 | FEAT-OCC-03 (A2.3), FEAT-OCC-04 (A2.4) |
| CAP-P6-007 | Conduct check on every outbound contact | A contact that fails the check is held, and every contact carries its result | REQ-OCC-005 | Must | 2 | FEAT-OCC-05 (A2.5) |
| CAP-P6-008 | Contact stop and consent per channel, statutory notices excepted | A customer who withdraws consent stops receiving on that channel, and a statutory notice is still served | REQ-OCC-006 | Must | 2 | FEAT-OCC-06 (A2.6) |
| CAP-P6-009 | E-signature request and signature result | An agreement is signed on the bank's channel where Legal allows, and the signed copy is on the case | REQ-OCC-009 | Must | 2 | FEAT-OCC-08 (A2.8), FEAT-OCC-09 (A2.9) |
| CAP-P6-010 | Notice and message block of the case record view | The notices and messages of a case, with their states, are on the case record | REQ-OCC-007 | Must | 1 | FEAT-OCC-01 (A2.1), FEAT-OCC-03 (A2.3) |
| CAP-P6-011 | Notice and message history in order | A reader sees what was sent, on which channel, when, and with what result | REQ-OCC-008 | Must | 2 | FEAT-OCC-02 (A2.2), FEAT-OCC-03 (A2.3) |
| CAP-P6-012 | Verified contact point clears a lost contact | A contact point the customer confirms is trusted, and the lost-contact deviation clears | REQ-OCC-010 | Must | 2 | FEAT-COM-05 (A2.18) |
| CAP-P6-013 | Self-service offer link on the digital channels | The customer reaches the offer on LINE and the web from a message the bank can evidence | REQ-OCC-011 | Should | 3 | FEAT-COM-01 to FEAT-COM-04 (A2.14 to A2.17) |

## 5.1 Capabilities not carried into the product

| Capability | Status | Later home |
|---|---|---|
| Match a payment to the plan (FEAT-OCC-10) | Moved | P8 rwb-payment (GAP-1607; ASM-2739) |
| Raise the plan payment missed event (FEAT-OCC-11) | Moved | P8 rwb-payment, which publishes PaymentMissed (EV-12) |
| Publish the steering dashboard (FEAT-OCC-12) | Moved | P9 rwb-reporting |
| Give partners identities through the external gateway (FEAT-OCC-13) | Moved | S9 rwb-partner with P4 rwb-access, on the partner gateway in the DMZ |
| Record a custody movement of a document (FEAT-COM-06) | Moved | P5 rwb-document |
| Answer a legal or audit document request (FEAT-COM-07) | Moved | P5 rwb-document |
| Apply retention on case closure (FEAT-COM-08) | Moved, with the class declared here | P5 rwb-document applies the archive and disposal (GAP-1604; ASM-2736) |
| Maintain the contact repository as a store (FEAT-COM-05) | Split | The contact point and its consent state are P1's; the enforcement is here (GAP-1605; ASM-2737) |
| View the offer, accept it, pay and raise a dispute in self-service (FEAT-COM-01 to FEAT-COM-04) | Split | The offer and its acceptance are S2's, the payment P8's, the dispute P3's and S8's; the message that carries the offer is here |
| The case record view and the case timeline as products (REQ-OCC-007, REQ-OCC-008) | Split | P3 rwb-case owns the view and the timeline; this service serves the notice and message block and its history (GAP-1598; ASM-2730) |

# 6. Functional requirements

Every requirement is specific and testable. The FSD REQ column keeps the trace to the source requirement, and the FSD feature column to its section. Priorities follow the BRD.

| FR ID | Requirement | CAP | BR | FSD REQ | FSD feature | Priority | Wave |
|---|---|---|---|---|---|---|---|
| FR-P6-001 | The service SHALL hold one template version row per template code and version, carrying the template code, the version, the language (LOV-LANG), the product group (LOV-PRODUCT), the channel (LOV-CHANNEL), the notice type (LOV-NOTICE), the signature basis (LOV-SIGNATURE-BASIS), the body reference, the merge codes, the state, the Legal approval flag, the approver role, the approval time and the valid-from date, and SHALL never overwrite an approved version. | CAP-P6-001 | REQ-OCC-002 | REQ-OCC-002 | FEAT-OCC-01 (A2.1); TSD T3.1 template | Must | 1 |
| FR-P6-002 | The service SHALL move a template version from DRAFT to APPROVED only on an approval recorded by Legal, SHALL record that approval as a decision record through rwb-decision with the approver role and the time, and SHALL move it to WITHDRAWN only with a reason and a record; a version that is not APPROVED SHALL generate no notice. | CAP-P6-001 | REQ-OCC-002 | REQ-OCC-002 | FEAT-OCC-01 (A2.1); FEAT-COM-05 (A2.18) | Must | 1 |
| FR-P6-003 | The service SHALL hold a versioned merge-field catalog in which each row carries the merge code, the source entity, the source field, the field ID, the required flag, the personal-data flag, the catalog version and the valid-from date, and SHALL refuse a template that uses a merge code not in the catalog version in force, naming the code. | CAP-P6-001 | REQ-OCC-001, REQ-OCC-002 | REQ-OCC-001 | FEAT-OCC-01 (A2.1); TSD T3.1 merge_field | Must | 1 |
| FR-P6-004 | The service SHALL keep exactly one current version of a template code, language, product group and channel at any date, SHALL refuse a load in which two versions claim the same current date window whole, and SHALL keep the version in force readable, including a withdrawn version for audit. | CAP-P6-001 | REQ-OCC-002 | REQ-OCC-002 | FEAT-OCC-01 (A2.1); AC-ALT-P6-007-01 | Must | 1 |
| FR-P6-005 | The service SHALL list template versions by code, language and state with paging, SHALL return the content of an APPROVED or WITHDRAWN version to a role that holds the template read right, and SHALL return the content of a DRAFT version only to a role that holds the template maintain right. | CAP-P6-001 | REQ-OCC-001, REQ-OCC-002 | REQ-OCC-001 | FEAT-OCC-01 (A2.1); API-P6-003, API-P6-005 | Must | 1 |
| FR-P6-006 | The service SHALL create one notice from the template version in force at the request date for a notice type of DEMAND, RECALL, STATUTORY_SALE_NOTICE or GUARANTOR_NOTICE, SHALL require the notice type and answer 422 with MSG-GEN-001 naming "notice type" when it is missing, and SHALL store the template code and the template version the notice used. | CAP-P6-002 | REQ-OCC-001 | REQ-OCC-001 | FEAT-OCC-01 (A2.1); AC-P6-007-01, AC-EXC-P6-001-05 | Must | 1 |
| FR-P6-007 | The service SHALL merge every value in the notice from the owner of that value through its contract — case facts through rwb-case, customer and contact facts through rwb-source-data, collateral and title facts through rwb-source-data — and SHALL refuse the whole request with 422 naming the template and the field when a required merge field has no value, storing no notice, no file and no decision record. | CAP-P6-002 | REQ-OCC-001 | REQ-OCC-001 | FEAT-OCC-01 (A2.1); FEAT-OCC-07 (A2.7); AC-EXC-P6-007-01 | Must | 1 |
| FR-P6-008 | The service SHALL obtain the letter from rwb-document through the generate-letter activity and SHALL hold only the document reference on the notice; a generation that fails SHALL store no notice and SHALL write no decision record, so that a set is stored whole or not at all. | CAP-P6-002 | REQ-OCC-001 | REQ-OCC-001 | FEAT-OCC-01 (A2.1); AC-EXC-P6-007-09 | Must | 1 |
| FR-P6-009 | The service SHALL treat a notice request as idempotent on the Idempotency-Key header: a repeat of the same key SHALL return the first notice with status 201 and SHALL create no second notice and no second decision record. | CAP-P6-002 | REQ-OCC-001 | REQ-OCC-001 | FEAT-OCC-01 (A2.1); AC-EXC-P6-001-04 | Must | 1 |
| FR-P6-010 | The service SHALL write one decision record for every notice generation, carrying the decision code and the rule reference that proposed the notice, and SHALL publish NoticeGenerated (EV-13) on `rwb.comms.events.v1` in the same transaction as the notice row through its outbox. | CAP-P6-002 | REQ-OCC-001, REQ-ILG-010 | REQ-OCC-001 | FEAT-OCC-01 (A2.1); EV-13 | Must | 1 |
| FR-P6-011 | The service SHALL return one notice by its identifier with the notice type, the template code and version, the state, the sent date, the barcode, the callback date, the delivery status and the sent type, masked by role, and SHALL answer 404 when the notice does not exist and 403 when the role's scope does not cover the case. | CAP-P6-002 | REQ-OCC-001, REQ-OCC-008 | REQ-OCC-001 | FEAT-OCC-01 (A2.1); API-P6-002 | Must | 1 |
| FR-P6-012 | The service SHALL hold a notice whose template version was withdrawn after the notice was created in the state Held with the hold reason `TEMPLATE_WITHDRAWN`, SHALL keep it out of the dispatch file, and SHALL raise one task to the litigation officer team with MSG-P6-003 naming the template. | CAP-P6-003 | REQ-OCC-002 | REQ-OCC-001 | FEAT-OCC-01 (A2.1); AC-EXC-P6-001-02 | Must | 1 |
| FR-P6-013 | The service SHALL refuse to dispatch a notice while the data product that supplies its merge values is STALE, SHALL hold the notice with the product and its business date, and SHALL show MSG-P1-001 to the role that asks for it. | CAP-P6-003 | REQ-OCC-001, REQ-OCC-003 | REQ-OCC-001 | FEAT-OCC-02 (A2.2); VR-P6-002-1; MSG-P1-001 | Must | 2 |
| FR-P6-014 | The service SHALL release or cancel a held notice only on a recorded approval decision taken through rwb-decision after an approved template version exists, and SHALL write one decision record for the release or the cancellation naming the person's role and the rule. | CAP-P6-003 | REQ-OCC-001, REQ-OCC-002 | REQ-OCC-001 | FEAT-OCC-01 (A2.1); AC-EXC-P6-001-03 | Must | 1 |
| FR-P6-015 | The service SHALL write every APPROVED notice of the business date into one dispatch file in the 16:00 window (JOB-10), SHALL hand the file to rwb-integration for delivery to WIN, and SHALL make the run idempotent on the business date so that a rerun replaces the file of that date and duplicates no notice. | CAP-P6-004 | REQ-OCC-003, REQ-DRI-007 | REQ-OCC-003 | FEAT-OCC-02 (A2.2); AC-BG-P6-001-01; JOB-10 | Must | 2 |
| FR-P6-016 | The service SHALL record the dispatch file reference and the dispatch attempt count on every notice it writes, and SHALL never place one notice in two dispatch files for the same business date. | CAP-P6-004 | REQ-OCC-003 | REQ-OCC-003 | FEAT-OCC-02 (A2.2); TSD T3.1 notice (dispatch_file_id, dispatch_attempts) | Must | 2 |
| FR-P6-017 | The service SHALL write the dispatch file against the versioned WIN interface definition, and SHALL hold, with its reason, a notice that lacks a value the layout requires rather than write an incomplete record into the file. | CAP-P6-004 | REQ-OCC-003, REQ-DRI-006 | REQ-OCC-003 | FEAT-OCC-02 (A2.2); INT-14; GAP-1602; ASM-2734 | Must | 2 |
| FR-P6-018 | The service SHALL place no letter in the dispatch file without a conduct check result of PASSED, and SHALL record the result PASSED and the summary "Statutory notice, consent withdrawn" on a statutory notice sent on the postal channel after consent was withdrawn. | CAP-P6-004 | REQ-OCC-003, REQ-OCC-005, REQ-OCC-006 | REQ-OCC-003 | FEAT-OCC-02 (A2.2); AC-EXC-P6-001-01 | Must | 2 |
| FR-P6-019 | The service SHALL read the proof-of-delivery rows for the business date through rwb-source-data's contract, SHALL apply a proof to the notice whose barcode it carries for the result DELIVERED, REFUSED, UNDELIVERABLE or PENDING together with the callback date, and SHALL list a proof that matches no notice for the operations queue without creating a notice. | CAP-P6-005 | REQ-OCC-003 | REQ-OCC-003 | FEAT-OCC-02 (A2.2); AC-ALT-P6-001-01 to -02; v_ace_pod | Must | 2 |
| FR-P6-020 | The service SHALL set a DELIVERED notice to Delivered with the callback date and publish NoticeDelivered (EV-15) so that rwb-case starts the `NOTICE_PERIOD` timer from the callback date; for UNDELIVERABLE it SHALL set the notice to Unserved, write one decision record with decision code D7.1 and rule R-LIT-09, call rwb-case's transfer operation with reason `NOTICE_UNSERVED`, show MSG-P6-008 naming the notice type and the delivery status, and start no timer. | CAP-P6-005 | REQ-OCC-003, REQ-ILG-010 | REQ-OCC-003 | FEAT-OCC-02 (A2.2); AC-ALT-P6-001-01 to -02; EV-15 | Must | 2 |
| FR-P6-021 | The service SHALL apply a proof of delivery once: the same barcode with the same result applied twice SHALL change nothing and SHALL be counted as a repeat rather than written twice. | CAP-P6-005 | REQ-OCC-003 | REQ-OCC-003 | FEAT-OCC-02 (A2.2); TSD T3.1 notice | Must | 2 |
| FR-P6-022 | The service SHALL write one interaction ledger entry through rwb-source-data's contract for every dispatch and every proof-of-delivery outcome, and SHALL raise an incident rather than discard an entry when the ledger write fails. | CAP-P6-005 | REQ-ILG-010 | REQ-ILG-010 | FEAT-OCC-02 (A2.2); NFR-077 | Must | 2 |
| FR-P6-023 | The service SHALL send one message on SMS or LINE through the ACE notification path for a request that names the channel, the template, the language and the party, SHALL answer 202 with the interaction, and SHALL answer 422 with MSG-GEN-001 naming "channel" when the channel is missing. | CAP-P6-006 | REQ-OCC-004 | REQ-OCC-004 | FEAT-OCC-03 (A2.3), FEAT-OCC-04 (A2.4); AC-P6-003-01; AC-EXC-P6-003-07 | Must | 2 |
| FR-P6-024 | The service SHALL record the channel result code and the delivery state (DELIVERED, READ or FAILED) with the channel reference on the interaction, and SHALL increment the contact point's failed count through rwb-source-data's contract when the result is FAILED. | CAP-P6-006 | REQ-OCC-004 | REQ-OCC-004 | FEAT-OCC-03 (A2.3); AC-EXC-P6-003-04 | Must | 2 |
| FR-P6-025 | The service SHALL treat a message request as idempotent on the Idempotency-Key header, so that a repeat returns the first response and exactly one message reaches NSS or LINE OA. | CAP-P6-006 | REQ-OCC-004 | REQ-OCC-004 | FEAT-OCC-03 (A2.3); AC-EXC-P6-003-05 | Must | 2 |
| FR-P6-026 | The service SHALL answer 202 with MSG-GEN-006 naming the channel when the notification path is unavailable, SHALL queue the send and retry it on the platform schedule, and SHALL place the send in the exception queue with delivery state FAILED and a task for a named owner once the retry limit is reached. | CAP-P6-006 | REQ-OCC-004 | REQ-OCC-004 | FEAT-OCC-03 (A2.3); AC-EXC-P6-003-03; NFR-026; GAP-1601; ASM-2733 | Must | 2 |
| FR-P6-027 | The service SHALL test every outbound contact — letter, SMS, LINE and signature invitation — against the conduct and consent rule package in force from rwb-decision before anything leaves, evaluated in this service with the embedded rule kit, and SHALL write the rule package version that was applied on the interaction and the decision record. | CAP-P6-007 | REQ-OCC-005 | REQ-OCC-005 | FEAT-OCC-05 (A2.5); VR-P6-005-1 to -2; BR-P6-005 | Must | 2 |
| FR-P6-028 | The service SHALL send no contact that carries no conduct check result, SHALL block a contact that fails the check with nothing sent, SHALL answer 409 with MSG-P6-001 for a contact stop and MSG-P6-002 for a channel without consent, and SHALL write one interaction marked BLOCKED with the reason. | CAP-P6-007 | REQ-OCC-005 | REQ-OCC-005 | FEAT-OCC-05 (A2.5); AC-EXC-P6-003-01 | Must | 2 |
| FR-P6-029 | The service SHALL read the consent state of the contact point per channel through rwb-source-data's contract, SHALL refuse a send on a channel whose consent is WITHDRAWN with 409 and MSG-P6-002 naming the channel, and SHALL write the BLOCKED interaction. | CAP-P6-008 | REQ-OCC-006 | REQ-OCC-006 | FEAT-OCC-06 (A2.6); AC-EXC-P6-003-01 | Must | 2 |
| FR-P6-030 | The service SHALL block every outbound contact on a case while a contact stop is in force, from the DeviationRaised event (EV-06) until the DeviationCleared event (EV-07), SHALL name the deviation code and the reason in MSG-P6-001, and SHALL release the block only on the matching clear event. | CAP-P6-008 | REQ-OCC-006 | REQ-OCC-006 | FEAT-OCC-06 (A2.6); AC-ALT-P6-003-02; EV-06, EV-07 | Must | 2 |
| FR-P6-031 | The service SHALL mark a notice type as statutory or not as versioned reference data, SHALL continue a statutory notice on the postal channel after consent was withdrawn, and SHALL record the conduct result PASSED with the summary "Statutory notice, consent withdrawn" for that send. | CAP-P6-008 | REQ-OCC-006 | REQ-OCC-006 | FEAT-OCC-06 (A2.6); AC-EXC-P6-001-01; NFR-044 | Must | 2 |
| FR-P6-032 | The service SHALL create one signature request for a generated document with method E_SIGNATURE, BRANCH or PAPER through rwb-document's contract, SHALL refuse E_SIGNATURE with 409 and MSG-P6-009 naming the template when the document's signature basis is `WET_INK_REQUIRED`, and SHALL send no request to the signing channel in that case. | CAP-P6-009 | REQ-OCC-009 | REQ-OCC-009 | FEAT-OCC-08 (A2.8); AC-EXC-P6-008-01 | Must | 2 |
| FR-P6-033 | The service SHALL apply a signing result within 60 seconds of its arrival: it SHALL return the signed copy as a write-once version linked to the case, SHALL set the request status SIGNED or DECLINED with the signed time, SHALL call the treatment service's signature record once, and SHALL count a repeated result without applying it twice; a result for an EXPIRED request SHALL stay on the exception queue and SHALL not be applied. | CAP-P6-009 | REQ-OCC-009 | REQ-OCC-009 | FEAT-OCC-09 (A2.9); AC-P6-008-01; AC-EXC-P6-008-02, AC-EXC-P6-008-04 | Must | 2 |
| FR-P6-034 | The service SHALL cancel the open signature request of a treatment when the offer expires, SHALL keep the request status EXPIRED, and SHALL answer 201 with status QUEUED and MSG-GEN-006 naming the signing channel when that channel is unavailable, retrying on the platform schedule. | CAP-P6-009 | REQ-OCC-009 | REQ-OCC-009 | FEAT-OCC-08 (A2.8); AC-EXC-P6-008-03 | Must | 2 |
| FR-P6-035 | The service SHALL return the notices of a case in time order with the notice type, the template code and version, the state, the sent date, the barcode, the callback date and the delivery status, masked by role, so that the case record view can show the notice block through this contract; the case record view itself belongs to rwb-case. | CAP-P6-010 | REQ-OCC-007 | REQ-OCC-007 | FEAT-OCC-01 (A2.1); API-P6-002 | Must | 1 |
| FR-P6-036 | The service SHALL serve the notice and message history of a case in time order with the channel, the state change, the outcome and the conduct result, so that the case timeline shows it through rwb-case's contract and the interaction ledger, and SHALL not build a second history store. | CAP-P6-011 | REQ-OCC-008 | REQ-OCC-008 | FEAT-OCC-02 (A2.2), FEAT-OCC-03 (A2.3); API-P6-002 | Must | 2 |
| FR-P6-037 | The service SHALL record a verified contact point through rwb-source-data's contract with its consent state, the verification time, the verifying role and its source, and SHALL clear the lost-contact deviation X6 through rwb-deviation's contract with one decision record naming the verification. | CAP-P6-012 | REQ-OCC-010 | REQ-OCC-010 | FEAT-COM-05 (A2.18); AC-P6-018-01 | Must | 2 |
| FR-P6-038 | The service SHALL send the outbound message that carries the offer reference to LINE or the web through the SMS and LINE capability, with the offer reference in the merge and its delivery recorded, and SHALL treat the viewing, acceptance, payment and dispute of the offer as the products of S2 rwb-treatment, P8 rwb-payment, P3 rwb-case and S8 rwb-deviation reached through gateway-bff. | CAP-P6-013 | REQ-OCC-011 | REQ-OCC-011 | FEAT-COM-01 to FEAT-COM-04 (A2.14 to A2.17) | Should | 3 |

# 7. Non-functional requirements

Targets are copied from the Non Functional Specification v3, the BRDs and the FSD. A target marked open is carried as an open question, never as a value.

| NFR ID | Requirement | Target | BR | Priority | Test |
|---|---|---|---|---|---|
| NFR-P6-001 | A notice request and a notice read answer inside the user's wait under the busiest-hour load, including the merge from the case and the contact contract. | Under 2 seconds at the 95th percentile | NFR-008 | Must | Performance test in SIT |
| NFR-P6-002 | A message request is accepted inside the user's wait and its result is recorded when the channel returns it. | 202 under 2 seconds; result recorded on arrival | NFR-008, NFR-025 | Must | Performance test with the channel stub |
| NFR-P6-003 | A conduct rule evaluation completes inside the user's wait before a contact leaves. | Under 300 milliseconds per evaluation at the 95th percentile | NFR-011 | Must | Component test with the rule package in force |
| NFR-P6-004 | The dispatch file of a business date holds every approved notice of that date and is complete inside the window. | Complete by 16:00 on the business date | NFR-067, NFR-021 | Must | Dispatch window drill with a seeded hold |
| NFR-P6-005 | A signing result is applied and a signed copy is on the case inside one minute of the result. | Within 60 seconds | NFR-025 | Must | Integration test with the signing stub |
| NFR-P6-006 | Every outbound contact carries a conduct check result. | 100 percent of contacts | NFR-038 | Must | Ledger reconciliation against the sent records |
| NFR-P6-007 | The consent state per channel is applied on every send, and a statutory notice continues when consent is withdrawn. | Applied on every send | NFR-044 | Must | Consent matrix test across channels and notice types |
| NFR-P6-008 | A notification-path or signing-channel outage queues the outbound action and loses none. | Queue and retry, nothing lost | NFR-025 | Must | Failure injection on the channel stub |
| NFR-P6-009 | An item that fails after the retry limit is in the exception queue with a task for a named owner. | Three retries, then the exception queue | NFR-026 | Must | Failure injection to the limit (GAP-1600; ASM-2732) |
| NFR-P6-010 | The service is available in business hours and outside them, when the dispatch window runs. | 99.9 percent in business hours; 99.5 percent outside business hours excluding the change window | NFR-020, NFR-021 | Must | Availability read monthly from monitoring |
| NFR-P6-011 | The service inherits the ACE recovery point and recovery time. | The ACE recovery point objective and recovery time objective | NFR-022, NFR-023 | Must | Failover and restore test before the first release |
| NFR-P6-012 | The service carries the letter, SMS, LINE and proof-of-delivery volume of the collections estate in the volume test. | No notice or message count is stated in the sources; the test uses the document volume of about 860,000 in 2027 as the upper bound for letters (GAP-1603; ASM-2735) | NFR-004, NFR-001 | Must | Volume test at the stated volume |
| NFR-P6-013 | Every notice decision is reproducible from the log, including the rule and the template version applied. | Every decision reproducible | NFR-033, NFR-034 | Must | Decision record inspection |
| NFR-P6-014 | The decision log of this service is append-only and hash-chained, and a break is reported the day it is found. | Daily check, same-day report | NFR-033, NFR-035 | Must | Chain break drill |
| NFR-P6-015 | A failed interaction ledger write raises an incident and no entry is discarded. | No silent gaps | NFR-077, NFR-075 | Must | Write failure drill |
| NFR-P6-016 | Personal data is masked by role on every read, and no personal data appears in an event, a workflow input or a log. | Masked by default; identifiers and facts only in events | NFR-039, NFR-040 | Must | Masking matrix test and event payload review |
| NFR-P6-017 | Every read of a personal field is written to the access log. | 100 percent of personal field reads | NFR-042, REQ-ACA-006 | Must | Access log reconciliation against reads |
| NFR-P6-018 | Staff authenticate with single sign-on and multi-factor; the service uses its own identity; data is encrypted in transit and at rest; secrets live in the key store. | Entra ID single sign-on with multi-factor; encrypted; no secret in code or configuration | NFR-049, NFR-051, NFR-052, NFR-053 | Must | Sign-in, identity and secret scan |
| NFR-P6-019 | The build blocks a change that carries a secret, personal data in code, tests or logs, or an unapproved dependency. | Pipeline checks pass | NFR-054 | Must | Pipeline run with a seeded violation |
| NFR-P6-020 | Workbench data stays in the bank's cloud tenancy in the agreed region, and every record carries a data classification that sets its handling. | SCB Azure, Southeast Asia; classification applied per record | NFR-046, NFR-047 | Must | Tenancy and classification review |
| NFR-P6-021 | Notices and messages are produced in the customer's language, and labels and messages served with this service's operations are available in Thai and English. | Thai by default, English where the customer chose it; every label and message in both languages | NFR-058, NFR-059 | Must | Language matrix review |
| NFR-P6-022 | Logs, traces and metrics are produced for template approval, notice generation, the dispatch window, every send and every proof of delivery, and every schedule has a run book and an alert. | Every flow covered; alert within 15 minutes to a named owner | NFR-064, NFR-067, NFR-068 | Must | Observability review and alert drill |
| NFR-P6-023 | A production release rolls back by redeploying the previous tag, and the service carries its own migration sequence in its own schema. | Rollback by previous tag; per-service migration | NFR-027 | Must | Rollback rehearsal |
| NFR-P6-024 | The notice record, the template version and the merge-field catalog each carry a retention class that sets their handling, with the period set by Compliance. | A class per record; periods open under DL26 (GAP-1604; ASM-2736) | NFR-028, NFR-030, NFR-031 | Must | Retention class review |

# 8. Data requirements

## 8.1 Entities owned by the service

Schema `rwb_comms`. Every table carries the seven standard record columns of the platform library. Retention is stated by class; the periods are open (GAP-1604; ASM-2736). The three tables are the ones the Ownership Map gives P6 (GAP-1595, GAP-1599; ASM-2727, ASM-2731).

| Entity | Kind | Key fields | Classification | Source | Retention |
|---|---|---|---|---|---|
| `template` | Versioned reference | `template_code`, `template_version`, `language` (LOV-LANG), `product_group` (LOV-PRODUCT), `channel` (LOV-CHANNEL), `notice_type` (LOV-NOTICE), `signature_basis` (LOV-SIGNATURE-BASIS), `body_ref`, `merge_codes`, state, `approved_by_legal`, `approved_by` (role), `approved_at`, `valid_from` | [CONFIDENTIAL] | Workbench reference data; the body file is held by rwb-document | Versioned; every superseded and withdrawn version kept and readable |
| `merge_field` | Versioned reference | `merge_code`, `source_entity`, `source_field`, `field_id`, `is_required`, `personal_data`, `catalog_version`, `valid_from` | [CONFIDENTIAL] | Workbench reference data | Versioned by catalog version |
| `notice` | Transaction, and the record of a dispatch and its proof of delivery | `case_id` (business key, no foreign key), `document_id`, `party_id`, `template_id`, `notice_type` (LOV-NOTICE), `sent_date`, `barcode`, `callback_date`, `delivery_status` (LOV-DELIVERY), `sent_type` (LOV-SENT-TYPE), `hold_reason`, `dispatch_file_id`, `dispatch_attempts`, state | [PII] | Workbench, with the dispatch and proof fields sourced from WIN | Workbench record class; archived by rwb-document |

The field IDs of the source are kept: DF-LEG-015 to DF-LEG-023, DF-LEG-030 to DF-LEG-034 on `notice`; DF-REF-045 to DF-REF-051 and DF-REF-063 to DF-REF-069 on `template`; DF-REF-252 to DF-REF-260 on `merge_field`.

Not carried: `signature_request`. It is a P5 rwb-document table under the Ownership Map ruling (GAP-1596; ASM-2728). Not carried either: any message, interaction or dispatch-history table, because the interaction ledger is rwb-source-data's and the dispatch facts sit on the notice (GAP-1599; ASM-2731).

## 8.2 Data read but not owned

| Entity or contract | Owner | What is read | Classification |
|---|---|---|---|
| `v_ace_contact`, `contact_point_ext` (through the source-data contract) | P1 rwb-source-data | Contact value, contact type, consent state per channel, verification time, failed count | [PII] |
| `v_ace_customer`, `v_ace_account`, `v_ace_collateral`, `v_ace_collateral_detail` (through the source-data contract) | P1 rwb-source-data | Merge values: name, address, account number, balance, title and collateral references | [PII], [SENSITIVE_FINANCIAL] |
| `v_ace_pod` (through the source-data contract) | P1 rwb-source-data | The proof-of-delivery row: barcode, result, callback date (GAP-1597, GAP-1608; ASM-2729, ASM-2740) | [PII] |
| Case facts, case state, queue and owner | P3 rwb-case | Merge values and the transfer on a non-delivered notice | [PII], [SENSITIVE_FINANCIAL] |
| Document, generated letter, signature request and signed copy | P5 rwb-document | Document references and the signature request status | [PII], [CONFIDENTIAL] |
| Decision record, approval decision and the conduct rule package | P7 rwb-decision | The approval decision, the rule package version and the decision reference | [CONFIDENTIAL] |
| Roles, scope and masking policy | P4 rwb-access | The authorisation answer and the masking rows for the role | [CONFIDENTIAL] |
| Deviation X1 to X7, including the contact stop | S8 rwb-deviation | The open deviation code, the contact stop and its clear | [CONFIDENTIAL] |
| Treatment and its signature result | S2 rwb-treatment | The treatment reference and the signature record call | [SENSITIVE_FINANCIAL] |
| The outbound file item and its delivery result | P2 rwb-integration | The file reference and the delivery result of the WIN file | [CONFIDENTIAL] |

## 8.3 Field-level requirements for personal and financial data

| Field | Meaning | Classification | Requirement |
|---|---|---|---|
| `notice.party_id`, `notice.case_id` | The party served and the case | [PII] | Masked by role on every read; the party identifier is a business key with no foreign key |
| `notice.barcode`, `notice.callback_date`, `notice.delivery_status` | Proof of delivery | [PII] | Read by a role with the notice read right; never in an event payload |
| `notice.sent_date`, `notice.sent_type` | When the notice was served and whether before or after NPL | [CONFIDENTIAL] | Read by role; carried in an event as identifiers and dates only |
| The merged customer name and postal address in the letter body | The content of the letter | [PII] | Generated into a document held by rwb-document; never stored on the notice row and never logged |
| The message content and the contact value it was sent to | SMS or LINE content | [PII] | Held on the ledger entry and masked by role; never in an event or a workflow input |
| `merge_field.personal_data` and `merge_field.source_field` | Which merge code carries personal data and where it comes from | [CONFIDENTIAL] | Drives the masking check at generation; a merge code marked personal is not written to a log |
| Account and balance values merged into a notice | Arrears shown to the customer | [SENSITIVE_FINANCIAL] | Read through the source-data contract; no financial value in an event |

## 8.4 Data rules

1. A value a business person may change — a template, a merge code, a notice type, a statutory flag, a retry limit — is a versioned data row read at run time, never a constant in code (BR-P6-001 to BR-P6-021; principle 1).
2. A link to a case, a party, a document or a treatment is a business-key column of type `varchar(255)` or `uuid` with no foreign key into another schema (DP-01).
3. The notice holds the dispatch and proof facts; it does not hold the letter body, which is a document.
4. A personal field is not returned when the access log cannot be written.
5. The proof of delivery is applied by barcode and is never inferred from a sent date.
6. A notice is the unit of evidence: one notice, one dispatch file reference, one proof outcome.

# 9. Integration points

Paths and call types are the confirmed v5 constraints. Nothing here is a design decision of this document.

| System or consumer | Direction | Protocol and call | Owner | Notes |
|---|---|---|---|---|
| gateway-bff | In | REST composite route, one hop, 2 s timeout | Platform edge (RWB-PLT-EDGE) | The notice and message requests and reads reach this service through the edge (ADR-019, DP-19) |
| rwb-case (P3) | In and out | REST and Temporal activity | P3 | Case facts for the merge, the transfer on a non-delivered notice, and the timer started from NoticeDelivered (GAP-1609; ASM-2741) |
| rwb-source-data (P1) | Out | REST, read and write through the published contract | P1 | Contact points and consent, customer and account merge values, collateral and title, the proof-of-delivery row, and the interaction ledger (DP-05, DP-18) |
| rwb-document (P5) | Out | Temporal activity for generate letter; REST for the document and the signature request | P5 | The letter is generated there; the signature request and the signed copy are stored there (GAP-1596; ASM-2728) |
| rwb-decision (P7) | Out and in | Temporal child workflow for approval; REST for the rule package in force; Kafka on `rwb.decision-record.v1` | P7 | The notice approval, the conduct and consent rule package, and one decision record per decision (DP-03, DP-04) |
| rwb-access (P4) | Out | REST, cached | P4 | Authorise, role scope and field masking policy (DP-08) |
| rwb-deviation (S8) | In and out | Kafka in; REST to clear the lost-contact deviation | S8 | DeviationRaised and DeviationCleared carry the contact stop (EV-06, EV-07); a verified contact point clears X6 |
| rwb-treatment (S2) | In and out | Kafka in for TreatmentApproved; REST to record the signature result | S2 | TreatmentApproved (EV-10) and the signature record call |
| rwb-payment (P8) | In | Kafka | P8 | PaymentMissed (EV-12) is a trigger for a reminder notice, consumed on the `rwb-comms` group |
| rwb-integration (P2) | Out | Temporal activity deliverFile | P2 | Delivers the WIN dispatch file of the 16:00 window (JOB-10, INT-14) (GAP-1602; ASM-2734) |
| ACE notification path, NSS (INT-17) | Out | REST | ACE common | SMS through the bank's path; the result code and the delivery state return on the same path |
| ACE notification path, LINE OA (INT-18) | Out | REST | ACE common | LINE message through the bank's official account |
| The signing channel (EasyApp) | Out and in | REST through the ACE path | ACE common | The signature request goes out and the result comes back; no direct call from this service to a system of record (REQ-DRI-006) |
| Bank scheduler (Airflow) | In | File window | Bank platform team | Opens the WIN file window that JOB-10 writes into (Arch v5 slides 32 and 44) |
| Kafka topic `rwb.comms.events.v1` | Out | CloudEvents 1.0, AsyncAPI contract, retry and `.dlt` topics, keyed by case | This service | NoticeGenerated (EV-13), NoticeDispatched (EV-14), NoticeDelivered (EV-15) |
| ACE audit and PII logging path (Kafka to the SOC) | Out | Kafka through the ACE path | ACE common | Every audit and personal-data access entry |

## 9.1 Integration questions

| Question | Owner role | Why it blocks |
|---|---|---|
| What is the record layout, field order, naming and encoding of the WIN registered-mail file, and how are the barcode and the sent date returned? | Solution architect with rwb-integration | No dispatch can be built or accepted without it (GAP-1602; ASM-2734) |
| Does the WIN return land in ACE and reach this service through the source-data contract, or does this service receive the return directly? | Solution architect with the ACE team | It decides the proof-of-delivery read path and whether the feature can start before RWB-ACE-001 lands (GAP-1597, GAP-1608) |
| Which channel result codes map to DELIVERED, READ, REFUSED and UNDELIVERABLE for NSS and for LINE OA? | Platform administrator with the ACE team | The delivery status shown on the case depends on the mapping |
| Is the signing channel reached through the ACE path or through rwb-integration, given that this service calls no system of record directly? | Solution architect | It decides the call type on the signature-request path |

# 10. Release slicing proposal

The service is wave 1: it is created with Epic 1 (release 30 November 2026 (tentative)) and grows through waves 2 and 3 (ASM-2745). Each slice is a list of capabilities, not stories.

## 10.1 Wave 0 — platform prerequisites (no product capability of its own)

The service consumes platform contracts before its own work starts: the service template and repositories, the shared libraries including the outbox and inbox library, the Temporal workflow kit with `NoticeDispatchWorkflow`, the schema and login provision in the ACE database, the Kafka event platform and naming library, the edge and gateway route, and observability. These belong to the platform epics and are not capabilities of this product.

## 10.2 Wave 1 — Epic 1 (release 30 November 2026 (tentative))

| Slice | Capabilities | Why now |
|---|---|---|
| 1.1 Template catalog and merge fields | CAP-P6-001 | Nothing can be generated until a version exists and Legal has approved it; the template and merge-field catalog is a wave-1 story (RWB-E1-046) |
| 1.2 Notice generation and hold | CAP-P6-002, CAP-P6-003 | The demand, recall and guarantor notice generated from case data is the Epic 1 outcome the litigation team is waiting for (RWB-E1-052) |
| 1.3 Notice block on the case record | CAP-P6-010 | The read-only case record view is a wave-1 outcome, and it shows no notice until this block exists |

Rationale: the wave-1 slice is the smallest set that lets a notice be produced from an approved template and read on the case. The dispatch window, the messages and the proof of delivery are wave 2 because the Epic 2 release is where the business takes letters with proof and SMS and LINE.

## 10.3 Wave 2 — Epic 2 (release 31 December 2026 (tentative))

| Slice | Capabilities | Why now |
|---|---|---|
| 2.1 Dispatch window and proof of delivery | CAP-P6-004, CAP-P6-005 | The notice period is counted from proof, which is the Epic 2 promise (RWB-E2-021) |
| 2.2 SMS and LINE dispatch | CAP-P6-006 | The customer is reached on the channel they use, with the result on the case (RWB-E2-022) |
| 2.3 Conduct and consent gate | CAP-P6-007, CAP-P6-008 | A contact is not made before the check, and a statutory notice still leaves |
| 2.4 E-signature | CAP-P6-009 | The deed in lieu wave-1 document set is signed without paper where Legal allows (RWB-E2-018) |
| 2.5 Notice and message history | CAP-P6-011 | The full history on one screen is an Epic 2 outcome |
| 2.6 Verified contact point | CAP-P6-012 | A lost-contact deviation clears only when a contact point is verified |

Rationale: Epic 2 puts one owner and a timer on every case and needs the notice period to run from proof. The dispatch, the proof, the channels and the conduct gate are one release because a dispatch without a conduct result cannot be accepted (NFR-038).

## 10.4 Wave 3 — Epic 4 and Epic 5 (release 28 February 2027 and 31 March 2027 (tentative))

| Slice | Capabilities | Why now |
|---|---|---|
| 3.1 Self-service offer link | CAP-P6-013 | Self-service is a Should requirement of Epic 4 (REQ-OCC-011); this service supplies the message and the evidence of delivery, the offer itself is S2's |
| 3.2 Proof of delivery on a notice at full scope (RWB-E5-002) | CAP-P6-005 | Litigation in Epic 5 needs the proof on the notice for every statutory notice type |

Rationale: both slices need a service that already dispatches and already holds proof; nothing here is a precondition for wave 2.

## 10.5 Later increments and not carried

| Increment | What unlocks it |
|---|---|
| Proof-of-delivery capture from ACE | RWB-ACE-001 accepted and `v_ace_pod` delivered (DL43; GAP-1608) |
| Guarantor notices at full scope | S3 rwb-guarantee (wave 3) and its notice types |
| Litigation notices for every action | S4 rwb-litigation (wave 3) |
| Customer letters for a debt sale and a write-off | S6 rwb-debtsale and S7 rwb-writeoff (waves 3 and 4) |
| Payment matching, the plan-missed event, the steering dashboard, partner identities, custody, the legal or audit document request and retention on closure | Not this service: P8, P9, S9 with P4, and P5 (GAP-1607; ASM-2739) |
| A retention period for the notice record and the template version | Compliance under DL26 (GAP-1604) |

# 11. Acceptance criteria and validation evidence

Each criterion is written GIVEN/WHEN/THEN. The evidence column points at the source acceptance criterion that proves it, so a criterion is never invented where the source has one. Every criterion is verified in SIT against synthetic data; no production data is used.

## 11.1 Acceptance criteria

| AC ID | Covers | GIVEN | WHEN | THEN | Evidence |
|---|---|---|---|---|---|
| AC-P6-001 | FR-P6-001, FR-P6-004, NFR-P6-024 | two versions of template "DIL-CONTRACT", version 2 approved and version 3 approved by Legal and valid from 2026-12-15 | each version is read and the current version is resolved for a date | version 2 stays readable with its own content and version 3 is current from its valid-from date; no approved version is overwritten; each version carries its state and its approval | AC-ALT-P6-007-01 |
| AC-P6-002 | FR-P6-002 | a template version in DRAFT and Legal's approval | the approval is recorded and the version is later withdrawn with a reason | the version moves DRAFT to APPROVED with the approver role and the time and one decision record; on withdrawal it moves to WITHDRAWN with the reason and stays readable; a version that is not APPROVED generates no notice | FSD P6 A2.1 VR-P6-001-1; AC-EXC-P6-001-02 |
| AC-P6-003 | FR-P6-003 | a template that uses merge code "transfer_price" and a catalog version in force that does not hold it | the template is uploaded | the upload is refused whole with the message naming the code and nothing is stored | TSD P6 T3.1 merge_field; MSG-GEN-001 |
| AC-P6-004 | FR-P6-004 | two versions of one template code, language, product group and channel claiming the same current window | the load is validated | the load is refused whole and the version in force keeps its rows and stays current | FSD P6 A2.1; AC-ALT-P6-007-01 |
| AC-P6-005 | FR-P6-006, FR-P6-008 | case "RC-2026-000321" in scope, template "DEMAND-SSME" TH version 2 approved, and the case facts that fill its merge fields | a litigation officer requests a DEMAND notice | one notice exists with notice type DEMAND, the state after approval and template code "DEMAND-SSME" with version 2, linked to the generated document; the letter is held by the document hub and the notice holds only its reference | AC-P6-007-01 |
| AC-P6-006 | FR-P6-006 | a user holding the notice-create right and a case in scope | POST /cases/RC-2026-000321/notices is sent with no notice type | the response is 422 with MSG-GEN-001 naming "notice type" and no notice is stored | AC-EXC-P6-001-05 |
| AC-P6-007 | FR-P6-007, FR-P6-012 | a template "DIL-CONTRACT" whose required merge field "title_doc_no" has no value on the case | the notice is requested | the response is 422 naming the template and the field; no notice, no file and no decision record is stored | AC-EXC-P6-007-01 |
| AC-P6-008 | FR-P6-009 | a notice request with Idempotency-Key "a1b2c3d4-0001" that returned a RECALL notice | the same request is sent again with the same key | the response is the first notice with status 201 and the case has one RECALL notice, with one decision record | AC-EXC-P6-001-04 |
| AC-P6-009 | FR-P6-010, NFR-P6-013, NFR-P6-014 | an approved template and a case in scope | a notice is generated | one decision record carries the decision code, the rule reference and the template version, NoticeGenerated is in the outbox with the case identifier as its key and no personal data in the payload, and the daily chain check reports the record as intact | EV-13; Arch v5 slide 42 |
| AC-P6-010 | FR-P6-011, NFR-P6-016, NFR-P6-017, NFR-P6-020 | a notice for party "P-0077" and a role without the unmasked masking row | the role reads the notice | the party and the contact value are masked, no response field holds the clear value, one access log entry is written, and the notice record carries its data classification | REQ-ACA-005, REQ-ACA-006; NFR-039, NFR-047 |
| AC-P6-011 | FR-P6-012 | template "DEMAND-SSME" TH version 1 withdrawn on 2026-12-13 and a notice created from it | the 16:00 window runs on 2026-12-14 | the notice is Held with hold reason `TEMPLATE_WITHDRAWN` and is not in the file, and a task is raised to the litigation officer team with MSG-P6-003 naming the template | AC-EXC-P6-001-02 |
| AC-P6-012 | FR-P6-013 | the data product that supplies the merge values is STALE with a business date behind the run date | the dispatch step runs | the notice is held with the product and its business date and MSG-P1-001 is shown; no incomplete record enters the file | VR-P6-002-1; MSG-P1-001 |
| AC-P6-013 | FR-P6-014, FR-P6-001 | a notice Held for `TEMPLATE_WITHDRAWN` and a later version approved by Legal | the approval decision to release is recorded | the notice leaves Held, the release carries one decision record with the approver role, and the notice is eligible for the next window; a cancel leaves it out of every file | FSD P6 A2.1; Arch v5 slide 17 (child approval) |
| AC-P6-014 | FR-P6-015, FR-P6-016, FR-P6-017, NFR-P6-004 | approved notices for business date 2026-12-14 and the 16:00 window open | JOB-10 runs twice for the same date | one file exists for the date and holds each notice once; each notice carries the file reference and one attempt per run; a notice missing a layout field is held with its reason rather than written | AC-BG-P6-001-01; AC-P6-001-01 |
| AC-P6-015 | FR-P6-018, FR-P6-027, NFR-P6-003, NFR-P6-006 | a notice whose conduct check passed and WIN acknowledging contract "CT-88001" with barcode "RR223344556TH" and sent date 15122026 | the dispatch runs | the notice is Sent with barcode "RR223344556TH" and sent date 2026-12-15, and the ledger entry for the letter carries conduct check PASSED and names the barcode, with the rule package version applied | AC-P6-001-01 |
| AC-P6-016 | FR-P6-019, FR-P6-020, FR-P6-021 | notice "N-0101" is Sent on 2026-12-15 | the proof of delivery for business date 2026-12-21 returns barcode "RR223344556TH" with result DELIVERED and callback date 18122026 | the notice is Delivered with callback date 2026-12-18, the ledger has a Delivered entry for case "RC-2026-000321" on 2026-12-18, NoticeDelivered is published, and the case has a running `NOTICE_PERIOD` timer started on 2026-12-18; the same proof applied again changes nothing and is counted as a repeat | AC-ALT-P6-001-01 |
| AC-P6-017 | FR-P6-020 | notice "N-0101" is Sent on 2026-12-15 | the proof returns barcode "RR223344556TH" with result UNDELIVERABLE | the notice is Unserved with delivery status UNDELIVERABLE, one decision record exists with decision code D7.1 and rule R-LIT-09, the case is transferred to its owner's queue with reason `NOTICE_UNSERVED`, the owner sees MSG-P6-008 naming DEMAND and UNDELIVERABLE, and no timer is started | AC-ALT-P6-001-02 |
| AC-P6-018 | FR-P6-031, FR-P6-018, NFR-P6-007 | the borrower's postal contact point has consent status WITHDRAWN and notice type DEMAND is statutory | JOB-10 runs on 2026-12-14 | the notice is written to the file and its ledger entry carries conduct check PASSED and the summary "Statutory notice, consent withdrawn" | AC-EXC-P6-001-01 |
| AC-P6-019 | FR-P6-022, NFR-P6-015 | a case with an open deviation X2 and a contact stop, and a decision log store that refuses writes | JOB-10 runs on 2026-12-14 | the notice stays Approved and is not in the file, the job record shows MSG-P7-003 for the notice, an incident is raised under rule R-UNI-39, and no decision or ledger entry is discarded | AC-EXC-P6-001-03 |
| AC-P6-020 | FR-P6-023, FR-P6-024, FR-P6-025, NFR-P6-002, NFR-P6-021 | party "P-0077" with a verified MOBILE contact point and consent GIVEN | a message is sent with channel SMS, template "SMS-REMIND", language TH and party "P-0077", and the same request is sent again with the same Idempotency-Key | the response is 202 with an interaction of channel SMS, direction OUTBOUND and conduct check PASSED; the interaction carries delivery status DELIVERED and reference "NSS-7781"; NSS received one message for the two requests; the message text is in the customer's language and the labels and messages are served in Thai and English | AC-P6-003-01, AC-EXC-P6-003-05 |
| AC-P6-021 | FR-P6-023, FR-P6-024 | party "P-0077" with a verified LINE contact point and consent GIVEN | a message is sent with channel LINE and template "LINE-REMIND" | the interaction carries channel LINE, conduct check PASSED and delivery status READ, and LINE OA received one message | AC-ALT-P6-003-01 |
| AC-P6-022 | FR-P6-028, FR-P6-030 | case "RC-2026-000777" has an open deviation X6, lost contact | a message is sent with channel SMS | the response is 409 with MSG-P6-001 naming "X6 Lost contact", nothing is sent to NSS, an interaction with conduct check BLOCKED is written, and one decision record exists with decision code X6 and the final call "contact refused" | AC-ALT-P6-003-02 |
| AC-P6-023 | FR-P6-029 | party "P-0077" has a MOBILE contact point with consent WITHDRAWN | a message is sent with channel SMS | the response is 409 with MSG-P6-002 naming SMS, nothing is sent to NSS, and a BLOCKED interaction is written | AC-EXC-P6-003-01 |
| AC-P6-024 | FR-P6-026, NFR-P6-008, NFR-P6-009 | the ACE notification path returns "unavailable" for NSS | a message is sent with channel SMS | the response is 202 with MSG-GEN-006 naming NSS, the send is queued and retried on the platform schedule, and after the retry limit it is in the exception queue with delivery status FAILED and a task for a named owner | AC-EXC-P6-003-03; GAP-1600 |
| AC-P6-025 | FR-P6-024 | party "P-0077" has a verified MOBILE contact point with consent GIVEN and failed count 0 | NSS returns result FAILED for the message | the interaction carries delivery status FAILED and the contact point has failed count 1 | AC-EXC-P6-003-04 |
| AC-P6-026 | FR-P6-032, FR-P6-033, NFR-P6-005 | signature request "RS-0301" sent for document "D-0601" to party "P-0088" on 2026-12-10 | the signing channel returns SIGNED with the bank signature applied at 2026-12-11 10:15:00 | within 60 seconds version 2 of "D-0601" holding the signed PDF is stored on case "RC-2026-000888" with write-once true, the request is SIGNED at 2026-12-11 10:15:00, and the treatment's signature record is called once with signed true and method E_SIGNATURE | AC-P6-008-01 |
| AC-P6-027 | FR-P6-032 | document "D-0701" has signature basis `WET_INK_REQUIRED` | a signature request is sent with method E_SIGNATURE | the response is 409 with MSG-P6-009 naming the template and no request is sent to the signing channel | AC-EXC-P6-008-01 |
| AC-P6-028 | FR-P6-033, FR-P6-034 | document "D-0601" was sent on 2026-12-10, the offer expired on 2026-12-21 and the open request was cancelled, so its status is EXPIRED | the signing channel returns SIGNED for that request on 2026-12-21 | the request keeps status EXPIRED, the result is held on the exception queue, the treatment's signature record is not called, and a later send for the same treatment reaches the signing channel once | AC-EXC-P6-008-02, AC-EXC-P6-008-03 |
| AC-P6-029 | FR-P6-035, FR-P6-036 | a case with notices on DEMAND and RECALL and messages on SMS and LINE | the case record block and the history are read | the notices come back in time order with type, template version, state, sent date, barcode and delivery status masked by role, and the history shows each contact with its channel, state change, outcome and conduct result in one order | AC-P6-001-01; API-P6-002 |
| AC-P6-030 | FR-P6-037 | a party confirms a MOBILE contact point and the case has an open deviation X6 lost contact | the verification is recorded with its consent state and the verifying role | the contact point carries the verification time and the verifying role, one decision record names the verification, and X6 is cleared through the deviation service | FSD P6 A2.18; REQ-OCC-010 |
| AC-P6-031 | FR-P6-005, FR-P6-028, NFR-P6-017, NFR-P6-018 | a user without the right in the capability area | the user tries a template or message action | the action is refused with MSG-P4-002, nothing changes, the refusal is written to the access log, and the call is authenticated by single sign-on with multi-factor on this service's own identity | AC-EXC-P6-001-06, AC-EXC-P6-003-08 |
| AC-P6-032 | FR-P6-038 | a treatment offer for case "RC-2026-000888" with an offer reference and a verified LINE contact point | the offer message is sent on LINE | the message carries the offer reference, reaches LINE OA once, and its delivery state is recorded; the offer itself is read from S2 through gateway-bff | AC-ALT-P6-003-01; REQ-OCC-011 |
| AC-P6-033 | NFR-P6-001, NFR-P6-002, NFR-P6-003, NFR-P6-012, NFR-P6-022 | the service at the volume stated in NFR-P6-012, with every flow instrumented | the performance and volume test runs and an alert drill is fired | a notice request and a notice read answer under 2 seconds at the 95th percentile, a message request is accepted under 2 seconds, a conduct evaluation completes under 300 milliseconds, and the alert for a failed dispatch window or a failed send reaches the named owner inside 15 minutes | NFR-008, NFR-011, NFR-067, NFR-068 |
| AC-P6-034 | NFR-P6-010, NFR-P6-011, NFR-P6-019, NFR-P6-023 | the previous release tag, a migration in `rwb_comms` and a pipeline run with a seeded secret and an unapproved dependency | the release is rolled back, the service is failed over, and the pipeline runs | the rollback redeploys the previous tag without touching another schema, the service meets its recovery point and recovery time in the failover test, and the pipeline fails on the seeded secret and the unapproved dependency | NFR-020 to NFR-023, NFR-027, NFR-054 |

## 11.2 Requirement trace summary

| BR | Capability | Functional requirement | Non-functional requirement | Acceptance criteria |
|---|---|---|---|---|
| REQ-OCC-001 | CAP-P6-001, CAP-P6-002, CAP-P6-003 | FR-P6-003, FR-P6-005, FR-P6-006, FR-P6-007, FR-P6-008, FR-P6-009, FR-P6-010, FR-P6-011, FR-P6-013, FR-P6-014 | NFR-P6-001, NFR-P6-013, NFR-P6-016 | AC-P6-003, AC-P6-005, AC-P6-006, AC-P6-007, AC-P6-008, AC-P6-009, AC-P6-010, AC-P6-013, AC-P6-029 |
| REQ-OCC-002 | CAP-P6-001, CAP-P6-003 | FR-P6-001, FR-P6-002, FR-P6-003, FR-P6-004, FR-P6-005, FR-P6-012, FR-P6-014 | NFR-P6-013, NFR-P6-024 | AC-P6-001, AC-P6-002, AC-P6-004, AC-P6-011, AC-P6-013 |
| REQ-OCC-003 | CAP-P6-004, CAP-P6-005 | FR-P6-015, FR-P6-016, FR-P6-017, FR-P6-018, FR-P6-019, FR-P6-020, FR-P6-021 | NFR-P6-004, NFR-P6-006, NFR-P6-012 | AC-P6-014, AC-P6-015, AC-P6-016, AC-P6-017 |
| REQ-OCC-004 | CAP-P6-006 | FR-P6-023, FR-P6-024, FR-P6-025, FR-P6-026 | NFR-P6-002, NFR-P6-008, NFR-P6-009 | AC-P6-020, AC-P6-021, AC-P6-024, AC-P6-025 |
| REQ-OCC-005 | CAP-P6-007 | FR-P6-027, FR-P6-028 | NFR-P6-003, NFR-P6-006 | AC-P6-015, AC-P6-022 |
| REQ-OCC-006 | CAP-P6-008 | FR-P6-029, FR-P6-030, FR-P6-031 | NFR-P6-007 | AC-P6-018, AC-P6-022, AC-P6-023 |
| REQ-OCC-007 | CAP-P6-010 | FR-P6-035 | NFR-P6-016, NFR-P6-017 | AC-P6-010, AC-P6-029 |
| REQ-OCC-008 | CAP-P6-011 | FR-P6-011, FR-P6-036 | NFR-P6-015 | AC-P6-029 |
| REQ-OCC-009 | CAP-P6-009 | FR-P6-032, FR-P6-033, FR-P6-034 | NFR-P6-005, NFR-P6-008 | AC-P6-026, AC-P6-027, AC-P6-028 |
| REQ-OCC-010 | CAP-P6-012 | FR-P6-037 | NFR-P6-024 | AC-P6-030 |
| REQ-OCC-011 | CAP-P6-013 | FR-P6-038 | NFR-P6-021 | AC-P6-032 |
| REQ-ILG-010 | CAP-P6-005, CAP-P6-006, CAP-P6-011 | FR-P6-010, FR-P6-020, FR-P6-022, FR-P6-036 | NFR-P6-015 | AC-P6-009, AC-P6-016, AC-P6-019, AC-P6-029 |
| REQ-DRI-006 | CAP-P6-004 | FR-P6-017, FR-P6-023 | NFR-P6-018 | AC-P6-014, AC-P6-020 |
| REQ-DRI-007 | CAP-P6-004 | FR-P6-015, FR-P6-016 | NFR-P6-004, NFR-P6-022 | AC-P6-014, AC-P6-024 |
| REQ-APD-006 | CAP-P6-002, CAP-P6-003 | FR-P6-014 | NFR-P6-013 | AC-P6-013, AC-P6-019 |
| REQ-ACA-005, REQ-ACA-006 | CAP-P6-002, CAP-P6-010 | FR-P6-011, FR-P6-035 | NFR-P6-016, NFR-P6-017 | AC-P6-010, AC-P6-031 |
| Non-functional work (every capability) | All capabilities | None; delivered as non-functional work in the service epic and the platform epics | NFR-P6-001 to NFR-P6-003, NFR-P6-010 to NFR-P6-014, NFR-P6-018 to NFR-P6-023 | AC-P6-033, AC-P6-034 |

BR coverage: all 11 P6 program requirements (REQ-OCC-001 to REQ-OCC-011) are covered by at least one functional requirement. Two of them are covered as this service's contribution rather than as ownership of the whole behaviour: REQ-OCC-007 and REQ-OCC-008 describe the case record view and the case timeline, which belong to rwb-case (GAP-1598; ASM-2730). REQ-OCC-010 is covered with the contact data held by rwb-source-data (GAP-1605; ASM-2737). The seven features that v5 places elsewhere carry no functional requirement here by design (GAP-1607; ASM-2739).

## 11.3 Validation evidence expected before approval

| Evidence | What it proves | Owner role |
|---|---|---|
| Template catalog walk-through: version, Legal approval, withdrawal, current version | FR-P6-001 to FR-P6-005, NFR-P6-024 | Legal counsel with the product owner |
| Notice generation run with a withdrawn template and with stale data | FR-P6-006 to FR-P6-014, NFR-P6-001 | Litigation officer with the QA team |
| Dispatch window drill: two runs for one date, one file, one record per notice | FR-P6-015 to FR-P6-018, NFR-P6-004 | Platform administrator with the QA team |
| Proof-of-delivery drill on DELIVERED and UNDELIVERABLE, with the timer and the transfer | FR-P6-019 to FR-P6-022 | Litigation officer with P3 |
| Conduct and consent matrix across channels and notice types, including the statutory exception | FR-P6-027 to FR-P6-031, NFR-P6-006, NFR-P6-007 | Conduct and QA officer with Compliance |
| SMS and LINE send, failure and retry drill to the exception queue | FR-P6-023 to FR-P6-026, NFR-P6-008, NFR-P6-009 | Platform administrator |
| E-signature flow: SIGNED within 60 seconds, wet-ink refusal, expired result | FR-P6-032 to FR-P6-034, NFR-P6-005 | Restructuring officer with P5 |
| Masking matrix, access log reconciliation and event payload review | FR-P6-011, FR-P6-035, NFR-P6-016, NFR-P6-017 | Compliance and PDPA officer |
| Volume and performance test at the stated volume | NFR-P6-001, NFR-P6-002, NFR-P6-012 | QA team |

# 12. Open questions

The FSD carries no open question of its own for this module; the questions below are product-level and are raised here, with the gap and assumption rows that stand in for an answer. No question is answered by invention.

| ID | Question | Owner role | Needed by | Blocks | Source |
|---|---|---|---|---|---|
| OQ-P6-01 | What is the record layout of the WIN registered-mail file, and how are the barcode and the sent date returned to the case? | Solution architect with rwb-integration | Before wave 2 system test | CAP-P6-004, CAP-P6-005 | GAP-1602; ASM-2734; INT-14 |
| OQ-P6-02 | Does the WIN return land in ACE and reach this service through the source-data contract, and does proof-of-delivery capture wait for RWB-ACE-001? | ACE team lead with the solution architect | Before wave 2 release | CAP-P6-005 | GAP-1597, GAP-1608; ASM-2729, ASM-2740; DL43 |
| OQ-P6-03 | Who owns the letter templates and the merge fields: the answer recorded in DL28, or rwb-comms as Architecture v5 and the Ownership Map state? | Product owner | Before wave 1 release | CAP-P6-001 | GAP-1595; ASM-2727; DL28 |
| OQ-P6-04 | Is the Legal approval taken on the template version, on the generated notice, or on both, and which path records each? | Product owner with Legal counsel | Before wave 1 release | CAP-P6-001, CAP-P6-002, CAP-P6-003 | GAP-1606; ASM-2738; REQ-APD-006 |
| OQ-P6-05 | Where is the record of a sent message and its delivery status held, given that the service has no message table in Architecture v5? | Solution architect | Before wave 2 system test | CAP-P6-006, CAP-P6-011 | GAP-1599; ASM-2731 |
| OQ-P6-06 | Which rule identifiers make up the conduct and consent rule package, and who approves its first version? | Conduct and QA officer with rwb-decision | Before wave 2 release | CAP-P6-007, CAP-P6-008 | GAP-1610; ASM-2742 |
| OQ-P6-07 | How many notices, letters, SMS, LINE messages and returned proofs a month are expected, so that the volume test can be sized? | Business lead with the data lead | Before wave 2 performance test | CAP-P6-004, CAP-P6-006, NFR-P6-012 | GAP-1603; ASM-2735 |
| OQ-P6-08 | Which retry limit applies to a failed send: three as NFR-026 states, or five as two acceptance criteria state? | Solution architect | Before wave 2 system test | CAP-P6-006, CAP-P6-009 | GAP-1600; ASM-2732; NFR-026 |
| OQ-P6-09 | Which retention class and period apply to a notice record, a template version and the merge-field catalog? | Compliance with Legal | Before wave 3 | CAP-P6-001, CAP-P6-005 | GAP-1604; ASM-2736; DL26 |
| OQ-P6-10 | Where does the signature record live, and who shows the request status on the case: this service, the document hub, or the case service? | Solution architect with P5 and P3 | Before wave 2 release | CAP-P6-009 | GAP-1596; ASM-2728 |

# 13. Approval

The approval table is deliberately empty: this version is Draft and no approval is recorded in this run. A missing approval is carried as an assumption, not as an answer (GAP-1611; ASM-2743).

| Role | Name | Decision | Date | Notes |
|---|---|---|---|---|
| Product Owner | | | | |
| FDA | | | | |

# Appendix A. Sources and evidence

| Source | Sections used |
|---|---|
| Recovery Workbench Business Requirements Program v5 | 5.6 (P6 requirements, REQ-OCC-001 to REQ-OCC-011), 5.7 (REQ-ILG-010), 5.2 (REQ-DRI-006, REQ-DRI-007), 5.7 (REQ-APD-006), 5.4 (REQ-ACA-005, REQ-ACA-006), 6.1 to 6.12 (NFR-001 to NFR-078), 7 (constraints), 8 (release plan), 9 (open decisions, DL26 and DL43), 10 (delivery model), 11 (requirement to service epic trace) |
| Recovery Workbench Business Requirements Epic 1 v5 | 3.6 (P6 requirements at development detail, RWB-E1-034, RWB-E1-046, RWB-E1-052, RWB-E1-055), 9 (requirement to service epic trace) |
| Recovery Workbench Business Requirements Epic 2 v3 | 3.6 (RWB-E2-018, RWB-E2-021, RWB-E2-022), 4 (REQ-OCC-003 to REQ-OCC-006, REQ-OCC-008 to REQ-OCC-010), 7 (DL28, DL30), 9 (traceability), 10.6 (personal data) |
| Recovery Workbench FSD P6 Communications v3 | Document control, existing capability check, A1.1 to A1.4, A2.1 to A2.21 (functional decomposition, rules, acceptance criteria), Requirements served, Screens (SCR-33), Appendix A and Appendix B |
| Recovery Workbench TSD P6 Communications v2 | T3.0 to T3.3 (objects, fields, lists of values, relationships), T5.1 to T5.3 (interfaces INT-14, INT-17, INT-18 and the events), T6 (RBAC), T7 (non-functional), Appendix T-A.1 and T-A.2 (API-P6-001 to API-P6-011), Appendix T-B |
| Recovery Workbench Architecture v5 | Slides 13 to 20 (service contracts, including P6 on slide 17), 20 and 31 and 32 (outbox, overnight chain, bank scheduler), 37 (no data lake), 41 (service catalogue), 42 (event catalogue), 44 (job map, JOB-10), 45 (architect questions) |
| Recovery Workbench Temporal and Drools Design v1 | Task queue, workflow kit, rules governed centrally and evaluated in the owning service, the saga steps of the long paths |
| Recovery Workbench Microservice Ownership Map v1 | Services, tables (template, merge_field, notice), operations (API-P6-001 to API-P6-011), events (EV-13 to EV-15), jobs (JOB-10), workflows (NoticeDispatchWorkflow), and the rulings on signature_request, JOB-10 and JOB-11 |
| Recovery Workbench Non Functional Specification v3 | 1 (targets on one page), 2 (volumes and concurrency), 3.1 to 3.12 (requirements by quality characteristic) |
| Recovery Workbench Microservice Story Template and Rules v1 | R1 (user decisions), R3 (source precedence and default rulings), R4 (services and naming), R5 (target structure and waves), R8 (outputs), R9 (gaps and assumptions) |

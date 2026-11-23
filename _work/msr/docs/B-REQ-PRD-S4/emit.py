import json, io, os

WP = "B-REQ-PRD-S4"
G = "CG-B-REQ-PRD-S4-"
A = "ASM-B-REQ-PRD-S4-"
FSD = ("Recovery Workbench FSD S4 Litigation and enforcement v3 (03 Requirements and specifications/"
       "Recovery Workbench Functional Specifications by Module v6)")
ARCH = "Recovery Workbench Architecture v5 Text Extract v1"
TMP = "Recovery Workbench Temporal and Drools Design Text Extract v1"
OM = "Recovery Workbench Microservice Ownership Map v1"
RULES = "Recovery Workbench Microservice Story Template and Rules v1"
BRDE38 = "Recovery Workbench Business Requirements Epics 3 to 8 v1"
BRDPROG = "Recovery Workbench Business Requirements Program v5"

gaps = []


def gap(n, title, source, section, description, evidence, typ, area, sev, wave, legacy, owner, proposed):
    gaps.append({
        "id": G + str(n), "title": title, "source": source, "section": section,
        "description": description, "evidence": evidence, "type": typ, "area": area,
        "severity": sev, "needed_by_wave": wave, "legacy_ref": legacy,
        "owner_role": owner, "asm": A + str(n), "proposed": proposed, "wp": WP})


gap(1,
    "FSD S4 reads the ACE views and the batch-status view directly, while Architecture v5 allows only rwb-source-data to read them and the connection matrix gives S4 no cell to P1",
    FSD + "; " + ARCH + " slides 13, 37 and 45; " + OM + "; " + RULES + " DP-05 and DP-13",
    "A1.1 constraints; A2.1 to A2.22 integration points and VR-S4-001-1 to VR-S4-022-1; A2.11 integration point",
    "The FSD is explicit that source data is read only from the ACE database through the SELECT-only recovery.v_ace_* views, and seventeen of the twenty-two features carry validation rule VR-S4-00n-1 against v_ace_batch_status. A2.11 reads the LIT hearings through ACE and A2.17 reads the NCB. Architecture v5 slide 37 changes '30 views read by any module (ADR-010)' to views read only by rwb-source-data, slide 45 answers 'who reads ACE data' with rwb-source-data alone plus REST or a Temporal activity for everyone else, and slide 13 gives the S4 row a T to P7, a T and E to P6 and a T and E to S9 and no cell to P1 at all. The whole read path of this service is therefore undefined, and the FSD's own rule wording contradicts the platform it is being realigned to.",
    "FSD S4 A1.1 Constraints; VR-S4-001-1, VR-S4-002-1, VR-S4-004-1, VR-S4-008-1, VR-S4-009-1, VR-S4-011-1, VR-S4-012-1, VR-S4-015-1, VR-S4-016-1, VR-S4-017-1, VR-S4-019-1 and VR-S4-022-1; A2.11.2 'Integration points. LIT, Partner portal' and A2.17.2 'Integration points. NCB, Model gateway'. " + ARCH + " slide 37, slide 45 (only rwb-source-data reads the 30 views), slide 13 (S4 row: T to P7; T E to P6; T E to S9; no P1 cell). Rules DP-05, DP-10, DP-13.",
    "Conflict", "Data read path", "P1", "2",
    "RWB-E5-001 to RWB-E5-022",
    "Solution architect",
    "Carry the FSD's field names as the source field names that the rwb-source-data contract returns, and build every step on that contract; no view and no ACE table is read by this service. Confirm the contract fields, the LIT view names and the freshness response with P1 before the wave 2 notice test.")

gap(2,
    "The connection matrix gives S4 no cell to rwb-document, rwb-payment or rwb-agent, while the FSD names the document hub, ALS and GL and the model gateway",
    FSD + "; " + ARCH + " slides 13 and 19; " + OM + " endpoints",
    "A2.4, A2.6, A2.10 field catalogs; A2.6 and A2.4 integration points; A2.15 integration point; A2.12 integration point; A2.22 integration point",
    "The FSD's integration points name 'the Workbench document hub' for the pack and the missing document, 'ALS and GL' for the court fee and the legal expense, 'ALS and GL, LED portal' for the enforcement proceeds match, and 'Model gateway' for the next litigation step. Architecture v5 slide 19 gives the S4 contract Temporal edges to Partner (issueInstruction), Comms (demand notice child) and Decision (approval child) and no other edge, and slide 13 gives the S4 row no cell to P5, P8 or P10. The Ownership Map lists only the five S4 REST paths, so no document, payment or agent contract is recorded for this service anywhere in the sources read.",
    "FSD S4 A2.4.2 and A2.6.2 integration points (the Workbench document hub, CCMS); A2.12.2 ('Workbench, Model gateway'); A2.15.2 ('Partner portal, ALS and GL'); A2.22.2 ('ALS and GL, LED portal'). " + ARCH + " slide 19 (S4 IN and OUT) and slide 13 (the S4 row). " + OM + " Endpoints: five paths with owner S4, none to P5, P8 or P10.",
    "Conflict", "Integration", "P1", "3",
    "RWB-E5-004, RWB-E5-006, RWB-E5-010, RWB-E5-012, RWB-E5-015, RWB-E5-022",
    "Solution architect",
    "Carry the three edges as contract dependencies on the P5, P8 and P10 contract stories and build this service against their published fakes, with the pack, the fee and the agent call behind the contract that the contract story fixes. No direct call and no second writer is introduced by this document.")

gap(3,
    "The Ownership Map gives rwb-litigation two tables, while Architecture v5 gives the schema judgments, enforcement and the LED auction ladder and the FSD holds notice, pack and deferral state",
    ARCH + " slides 19, 30 and 41; " + OM + " tables; " + FSD + " field catalog",
    "A2.1 to A2.3 (notice state and served result); A2.16 (judgment); A2.18 to A2.21 (enforcement, ladder, deferral, petition); A2.22 (proceeds)",
    "Architecture v5 slide 19 states that rwb-litigation 'writes schema rwb_litigation: legal actions, hearings, judgments, enforcement, LED auction ladder' and slide 41 repeats the same list as what the service owns. The Ownership Map Tables sheet has exactly two rows with owner S4, legal_action and hearing, plus the four platform library objects, and no row for a judgment, an enforcement record, an auction round, a pack, a notice state, a deferral or a decision record. The FSD's field catalog for all twenty-two features repeats the same eight legal_action columns, so the table set the DB story is written from does not exist for six of the eight things the schema is said to hold.",
    ARCH + " slide 19 (DB writes schema rwb_litigation: legal actions, hearings, judgments, enforcement, LED auction ladder) and slide 41 (S4 owns legal actions, hearings, judgments, enforcement, LED auction ladder). " + OM + " Tables: legal_action (S4), hearing (S4); no other S4 row. FSD S4 A2.6.3.2, A2.7.3.2, A2.10.3.2, A2.13.3.2, A2.14.3.2, A2.18.3.2, A2.20.3.2 and A2.21.3.2 field catalog: the same eight legal_action columns.",
    "Missing", "Data model", "P2", "3",
    "RWB-E5-001 to RWB-E5-022",
    "Data architect",
    "State the six missing entity groups and their key fields as product requirements and fix no physical table name beyond the two the map already holds; the table set and the physical schema are written when the S4 DB story is picked up, and the missing rows are added to the Ownership Map in the same change.")

gap(4,
    "legal_action.case_id is a uuid in the FSD, while ADR-014 and DP-01 forbid a cross-schema foreign key and require a varchar(255) business key",
    FSD + " field catalog; " + ARCH + " slides 20 and 45; " + RULES + " DP-01 and DP-15",
    "A2.6.3.2, A2.7.3.2, A2.10.3.2, A2.13.3.2, A2.14.3.2, A2.18.3.2, A2.20.3.2, A2.21.3.2 field catalog",
    "Every field catalog of the FSD types legal_action.case_id as uuid with the meaning 'The recovery_case this record belongs to' and the required flag Yes, and lists no foreign key. Under Architecture v5 the case lives in schema rwb_case and this service writes only schema rwb_litigation, so a uuid column carrying a cross-schema reference is exactly what DP-01 forbids; the platform pattern is a business-key column of type varchar(255) with no foreign key. The same column is the key of almost every entity in this schema, so the DB story cannot start until it is settled.",
    "FSD S4 A2.6.3.2 to A2.21.3.2 field catalog row 'legal_action.case_id | The recovery_case this record belongs to | uuid | Yes | None | No'. " + ARCH + " slide 20 (schema and login per service) and slide 45. " + RULES + " DP-01 (never read another service's tables) and DP-15 (per-service Flyway in the service's own schema). ADR-014.",
    "Conflict", "Data model", "P2", "3",
    "RWB-E5-004, RWB-E5-005, RWB-E5-007, RWB-E5-010, RWB-E5-013 to RWB-E5-022",
    "Data architect",
    "Use a business-key column of type varchar(255) with no foreign key, keeping the FSD's field name; the case number is the business key and no identifier of another schema is stored as a foreign key.")

gap(5,
    "The notice and its proof of delivery sit in S4 in the FSD and in rwb-comms in Architecture v5 and the Ownership Map, and the three notice paths are split across the two services",
    FSD + " A2.1 to A2.3; " + ARCH + " slide 41; " + OM + " endpoints and services",
    "A2.1, A2.2, A2.3 (generation, proof of delivery, notice period); Screens SCR-18",
    "The FSD gives module S4 the demand and recall notice, its approval, the proof of delivery and the notice period, and its own integration points name WIN for dispatch. Architecture v5 slide 41 gives rwb-comms 'notices, templates, merge fields, proof of delivery', and the Ownership Map therefore puts POST /cases/{caseId}/notices and GET /notices/{noticeId} on P6 while POST /notices/{noticeId}/approve is x-module S4, on the same resource. Two services appear to own the notice, its state and its served result, and the notice period cannot start from a proof of delivery that this service does not hold.",
    "FSD S4 A1.2 FEAT-LIT-01 to FEAT-LIT-03; A2.1.2 integration point 'WIN, Workbench'; A2.2.2 integration point 'WIN'; A2.2.3.1 R-LIT-07, R-LIT-08, R-LIT-09; Screens SCR-18 notice approval, first in E2. " + ARCH + " slide 41 (rwb-comms owns notices, templates, merge fields, proof of delivery). " + OM + " Endpoints: POST /cases/{caseId}/notices (P6), GET /notices/{noticeId} (P6), POST /notices/{noticeId}/approve (S4).",
    "Ambiguous", "Capability ownership", "P1", "2",
    "RWB-E5-001, RWB-E5-002, RWB-E5-003",
    "Solution architect",
    "This service decides that a notice is due, approves it and owns the notice period; rwb-comms owns the template, the merge fields, the delivery and the proof of delivery, and returns the served result as NoticeDelivered. The notice period starts from the delivered_at that rwb-comms returns, and the notice state on the case is written by this service only.")

gap(6,
    "The notice capability is first needed in Epic 2 (wave 2, 31 December 2026 (tentative)) while the service is created in wave 3",
    FSD + " module table and Screens; " + BRDPROG + " section 8 and 10.2; " + RULES + " R5.6",
    "Document control module table; Screens SCR-18",
    "The FSD's module table reads 'S4 | Litigation and enforcement | E2 notices; E5' and its screens list gives SCR-18 notice approval the first-in E2. The Program BRD release plan puts E2 at 31 December 2026 (tentative) and E5 at 31 March 2027 (tentative), and section 10.2 puts RWB-SVC-S4 in wave 3. The wave map in R5.6 puts EP02 in wave 2 and EP05 in wave 3, and R5.6 also says a story whose wave map wave is earlier than its service's wave keeps the wave map wave, so notice work is due one wave before the service that owns it exists.",
    "FSD S4 document control module table ('S4 | Litigation and enforcement | E2 notices; E5') and Screens ('SCR-18 Notice approval | Generated demand and recall notices for approval before dispatch | E2'). " + BRDPROG + " section 8 (E2 31 Dec 2026 (tentative), E5 31 Mar 2027 (tentative)) and section 10.2 (RWB-SVC-S4, wave 3). " + RULES + " R5.6 wave map and the conflict rule.",
    "Conflict", "Release sequencing", "P1", "2",
    "RWB-E5-001, RWB-E5-002, RWB-E5-003",
    "Solution architect",
    "Publish the notice contract, its fake and its schema as slice 2.1 before wave 3, let the notice stories keep the EP02 wave 2 that R5.6 gives them, and build the rest of the capability in wave 3 against the same contract.")

gap(7,
    "Thirty-two of the seventy-nine R-LIT rules are named in the FSD and the litigation rule package is Phase 2",
    FSD + " A2.1 to A2.22 rule tables; " + TMP + " slide 20 and slide 48; " + BRDE38 + " BR-034 source column",
    "A2.1.3.1 to A2.22.3.1; slide 20 of the Drools design",
    "The FSD's rule tables name R-LIT-03, 04, 07, 08, 09, 11, 15, 16, 18, 21, 23, 24, 26, 27, 28, 30, 31, 32, 36, 37, 38, 44, 45, 50, 51, 52, 54, 55, 58, 65, 67 and 70, thirty-two of the seventy-nine the BRD cites as R-LIT-01 to R-LIT-79. The remaining forty-seven (R-LIT-01, 02, 05, 06, 10, 12, 13, 14, 17, 19, 20, 22, 25, 29, 33, 34, 35, 39 to 43, 46 to 49, 53, 56, 57, 59 to 64, 66, 68, 69 and 71 to 79) are named in no FSD section, including the two the design relies on for the prescription escalation (R-LIT-20) and the broken settlement (R-LIT-40 is named only in the Drools design). The Drools design says the litigation set is 79 rules and the package is Phase 2, so the rule base the requirements are tested against does not exist yet.",
    "FSD S4 A2.1.3.1 to A2.22.3.1 rule ID column; the twelve distinct rules repeated across features. " + TMP + " slide 20 ('Litigation route set, 79 rules (package Phase 2)', 'R-LIT-63 to 67', 'R-LIT-11/20', 'R-LIT-57', 'R-LIT-40') and the Phase 2 open point (Drools packages for S1 and S3 to S9). " + BRDE38 + " BR-034 source column ('R-LIT-01 to R-LIT-79').",
    "Missing", "Business rules", "P1", "3",
    "RWB-E5-001 to RWB-E5-022",
    "Center of excellence analyst",
    "Take the thirty-two rules the FSD names as the requirement set of this PRD, treat the other forty-seven as authoring work for the package, and require the package code, its version label and its owner in rwb-decision before the wave 3 release. No rule is restated here and no value is invented.")

gap(8,
    "Every FSD acceptance criterion is the same generic sentence and there is no alternate flow and no background event for any of the twenty-two features",
    FSD + " A2.1.4 to A2.22.4",
    "A2.1.4.1 to A2.22.4.1, A2.1.4.2 to A2.22.4.2, A2.1.4.4 to A2.22.4.4",
    "Each of the twenty-two main-success criteria reads 'The data and rules it needs are in place / The trigger arrives / The result is recorded with its rule version', and the two exception criteria of each feature read 'Refused with MSG-P4-002; nothing changes' and 'Nothing changes; MSG-P7-003; incident raised'. Every alternate-flow table says 'No alternate path' and every system-background-event table says 'No background event', although A2.3 is a timer, A2.11 tracks a court calendar and A2.19 follows an auction ladder. The consequence is that no source criterion states a business outcome, so the criteria in this PRD are written from the rules each feature names and each one cites the FSD row it comes from.",
    "FSD S4 A2.1.4.1 to A2.22.4.1 (main success flow, the identical three-column statement), A2.1.4.2 to A2.22.4.2 ('None | No alternate path') and A2.1.4.4 to A2.22.4.4 ('None | No background event').",
    "Ambiguous", "Acceptance criteria", "P2", "2",
    "RWB-E5-001 to RWB-E5-022",
    "Business analyst, S4",
    "Read each FSD row as one criterion per feature and write the step-specific criterion from the rules that feature names, with the FSD row cited as its evidence. The story-level scenarios are written in the story files with their origin tag, as R7.2 requires.")

gap(9,
    "LawsuitFiled, JudgmentRecorded and AuctionResult have no EV number and no catalogue row",
    ARCH + " slides 19, 42 and 43; " + OM + " events",
    "Slide 19 S4 OUT; slides 42 and 43 event catalogue",
    "Architecture v5 slide 19 gives the S4 OUT contract 'rwb.litigation.events.v1: LawsuitFiled, JudgmentRecorded, AuctionResult', but the event catalogue on slides 42 and 43 has no numbered row for any of the three: JudgmentRecorded and AuctionResult appear only as the unnumbered '+' row at the end of slide 43, and LawsuitFiled appears on slide 19 alone. The Ownership Map events sheet holds none of the three, so a consumer cannot be wired to a contract row and the reporting read model cannot subscribe by name.",
    ARCH + " slide 19 (OUT: rwb.litigation.events.v1: LawsuitFiled, JudgmentRecorded, AuctionResult); slide 43 (the last row is '| + | JudgmentRecorded, AuctionResult | rwb-litigation | rwb.litigation.events.v1 | rwb-asset, rwb-case |'). " + OM + " Events: no row with owner S4.",
    "Missing", "Event contract", "P2", "3",
    "RWB-E5-010, RWB-E5-016, RWB-E5-019, RWB-E5-022",
    "Solution architect",
    "Carry the three event names, the topic and the consumers as the contract, keyed by the case, and leave the EV numbers to the event catalogue change. No EV id is asserted here.")

gap(10,
    "R-LIT-01 starts litigation on route R4 while the case journeys call R4 the guarantee claim and R5 litigation",
    TMP + " slide 20 and open points; " + FSD + " A1.1",
    "S4 open point; the route the legal action starts from",
    "The Drools design says 'R-LIT-01 starts litigation on route = R4' and, in the same document's open points, that 'Case Journeys v3 calls R4 the guarantee claim and R5 litigation'. The FSD's S4 scope begins at the notices and never names a route number, so the route a legal action starts from is stated one way in the design and another way in the case journeys. The route number drives the route decision that starts LitigationWorkflow, so the trigger of the whole service is ambiguous.",
    TMP + " slide 20 notes ('Starts when litigation route approved (R-LIT-01), or a restructure or settlement plan breaks (R-LIT-02)') and the open point 'Route numbering: R-LIT-01 starts litigation on route = R4; Case Journeys v3 calls R4 the guarantee claim and R5 litigation'. FSD S4 A1.1 scope.",
    "Conflict", "Business rules", "P2", "3",
    "RWB-E5-001",
    "Business analyst, S4",
    "Name no route number in this document: the legal action starts when the route decision names litigation or when a restructure or settlement plan breaks (R-LIT-01, R-LIT-02), and the numbering is settled in rwb-decision as reference data.")

gap(11,
    "REQ-S4-009 (prescription warnings) has no BRD requirement row, and BR-038 and BR-042 carry no program requirement ID",
    BRDPROG + " section 5.11; " + BRDE38 + " section 8.3; " + FSD + " Requirements served",
    "Program BRD 5.11; Epics 3 to 8 BR-034 to BR-043",
    "The program BRD states ten requirements for S4, REQ-S4-001 to REQ-S4-010, all Must. The E5 requirement set maps them as REQ-S4-001 to BR-034, REQ-S4-002 to BR-035, REQ-S4-003 to BR-036, REQ-S4-004 to BR-037, REQ-S4-005 to BR-039, REQ-S4-006 to BR-040, REQ-S4-007 and REQ-S4-008 to BR-041 and REQ-S4-010 to BR-043. REQ-S4-009, 'Prescription warnings force a litigation review ahead of every other open action on the case', has no row; its rule family appears only inside BR-034's source column. In the other direction BR-038 (court filing and receipt matched to the LIT lawsuit) and BR-042 (asset trace, writ, ladder and bankruptcy petition) carry no program requirement ID. A reader cannot tell whether the BRD lost a requirement or the mapping did.",
    BRDPROG + " section 5.11 (REQ-S4-001 to REQ-S4-010). " + BRDE38 + " section 8.3 BR-034 (sources REQ-S4-001, REQ-APD-006), BR-035, BR-036, BR-037, BR-038 (no REQ), BR-039 (REQ-S4-005), BR-040 (REQ-S4-006), BR-041 (REQ-S4-007, REQ-S4-008), BR-042 (no REQ), BR-043 (REQ-S4-010).",
    "Missing", "Requirements traceability", "P2", "3",
    "RWB-E5-003, RWB-E5-010, RWB-E5-017 to RWB-E5-021",
    "Product Owner",
    "Carry REQ-S4-009 into this PRD as FR-S4-051 and FR-S4-052 under BR-034, the requirement that owns the statutory clock, and record the gap so the E5 BRD can add the row. Carry BR-038 and BR-042 from the FSD features and the RWB-E5 story keys. Nothing is dropped and no requirement is merged.")

gap(12,
    "The three S4 screens have no owner cell in the v5 screen matrix, and SCR-18's first-in is Epic 2",
    FSD + " Screens; " + ARCH + " slide 41 and the edge slides; " + OM + " endpoints",
    "Screens SCR-18, SCR-19, SCR-20",
    "The FSD lists three screens for this module: SCR-18 notice approval (first in E2), SCR-19 litigation workspace and SCR-20 enforcement workspace (first in E5). Architecture v5 slide 41 gives the service catalogue and the edge and gateway design gives composite routes, but neither states which service each screen belongs to, and the Ownership Map lists the API paths only. The composite route that serves a screen joins more than one service here, because SCR-19 shows the pack from rwb-document, the court dates from this service and the case party from rwb-case.",
    "FSD S4 Screens: SCR-18 notice approval (E2), SCR-19 litigation workspace (E5), SCR-20 enforcement workspace (E5). " + ARCH + " slide 41 (edge and gateway) and the gateway-bff composite route; " + RULES + " DP-19.",
    "Missing", "Screens", "P3", "2",
    "RWB-E5-001 to RWB-E5-022",
    "Solution architect",
    "Serve the three screens from gateway-bff composite routes and let this service answer the legal-action part of each; the screen owner cell is recorded with the edge work and is not decided here.")

gap(13,
    "The message wording and the Thai and English versions of the S4 messages are not in the FSD",
    FSD + " A2.1.3.1 to A2.22.3.1; " + BRDPROG + " DL10 and DL59",
    "Every validation rule row that names a message",
    "The FSD names MSG-P1-001, MSG-P4-002, MSG-P7-003, MSG-GEN-001, MSG-S4-001 and MSG-S4-002 and gives one English wording for each, but gives no Thai wording, no field-level text for MSG-GEN-001 and no owner for the wording. The Program BRD leaves the Thai name of every field, label and message to DL10, and NFR-059 requires every label and message in Thai and in English. The two messages that carry a business meaning here, MSG-S4-001 'The pack is missing {item}.' and MSG-S4-002 'The claim on this case expires on {date}.', decide what the officer reads at the moment of filing.",
    "FSD S4 A2.5.3.1 VR-S4-005-1 (MSG-S4-001), A2.3.3.1 VR-S4-003-1 (MSG-S4-002), A2.14.3.1 VR-S4-014-1 (MSG-GEN-001), A2.1.3.1 VR-S4-001-1 (MSG-P1-001), A2.6.3.1 VR-S4-006-2 (MSG-P4-002), A2.1.4.3 AC-EXC-S4-001-02 (MSG-P7-003). " + BRDPROG + " DL10; NFR-059.",
    "Missing", "Messages", "P2", "2",
    "RWB-E5-002, RWB-E5-005, RWB-E5-007, RWB-E5-013, RWB-E5-020",
    "Business analyst, S4",
    "Preserve the message IDs and the English wording of the FSD character for character, and leave the Thai wording, the field-level text and the approver to the message work DL10 names.")

gap(14,
    "The sources state no litigation, hearing or enforcement volume for this module, and no release date other than the program release plan",
    FSD + " A1.2 and A2.1.1 to A2.22.1; " + BRDPROG + " section 8; Non Functional Specification v3 sections 2 and 3",
    "A2.1.1 to A2.22.1 metric tables; NFR-001, NFR-002, NFR-003",
    "Every one of the twenty-two features carries the same single metric, 'Litigation turnaround | 21 days | 6 days' (the FSD writes the target as 6 days), and no feature states a case count, a hearing count, a filing count or an enforcement count. The non-functional specification gives the case store volume (about 23,600 open cases at go-live), the staff population (about 370 of 914 online) and the partner population (about 50 of about 320 online, across 11 to 12 law firms), none of which is split by module. A performance target for this service therefore has no module-specific volume behind it, and the release date used in this document is the program release plan date and nothing else.",
    "FSD S4 A2.1.1 to A2.22.1 metric table ('Litigation turnaround | 6 days'). Non Functional Specification v3 NFR-001, NFR-002, NFR-003, NFR-007. " + BRDPROG + " section 8 release plan (E2 31 Dec 2026 (tentative), E5 31 Mar 2027 (tentative)).",
    "Missing", "Non-functional", "P3", "3",
    "RWB-E5-001 to RWB-E5-022",
    "Solution architect",
    "Use the population figures the non-functional specification states, mark the litigation share as open, and copy every release date unchanged and tentative. No volume and no date is invented here.")

os.makedirs("_work/msr/gaps", exist_ok=True)
with io.open("_work/msr/gaps/" + WP + ".jsonl", "w", encoding="utf-8", newline="\n") as f:
    for r in gaps:
        f.write(json.dumps(r, ensure_ascii=False) + "\n")

asms = []


def asm(n, text, why, read, confidence, confirm, impact, applied):
    asms.append({
        "id": A + str(n), "text": text, "why": why, "read": read,
        "gap": G + str(n) if n <= 14 else "", "applied_in": applied,
        "confidence": confidence, "confirm": confirm, "impact": impact, "wp": WP})


asm(1,
    "This service reads lawsuit, hearing, balance and batch-status facts only through the rwb-source-data contract, publishes nothing it read from a view, and keeps the FSD's field names as the source field names that contract returns.",
    "Architecture v5 is higher in precedence than the FSD and makes the 30 views readable by rwb-source-data alone; the connection matrix gives the S4 row no cell to P1, so the edge is carried as a contract dependency.",
    "The FSD's integration points and its seventeen stale-data validation rows as a statement of which facts each step needs, not of how they are read.",
    "High", "Solution architect with P1, before the wave 2 notice test",
    "If a view stays readable by this service, the boundary test and the freshness guarantee both need a second owner.",
    "Section 2.4 constraint 11; Section 5.1; Section 6 FR-S4-053; Section 8.2; Section 8.4 rule 2; Section 9")

asm(2,
    "The pack, the court fee and the next-step agent reach this service as contract dependencies on the P5, P8 and P10 contract stories, built against their published fakes, with no direct call and no second writer.",
    "The FSD names the document hub, ALS and GL and the model gateway while the connection matrix gives the S4 row no cell to P5, P8 or P10.",
    "The FSD's integration points as the set of external capabilities a step needs, with the call type left to the contract of the owning service.",
    "Medium", "Solution architect with P5, P8 and P10, before the S4 contract story closes",
    "A wrong carrier puts a second REST hop inside a business step, which ADR-020 forbids.",
    "Section 2.3; Section 5.1; Section 9; Section 9.1; Section 12 OQ-S4-02")

asm(3,
    "This service owns eight entity groups in schema rwb_litigation: the two tables the Ownership Map names (legal_action, hearing) and six groups named as Architecture v5 names them (judgment, enforcement, auction round, pack, notice state, decision record). No physical table name is stated for the six.",
    "Architecture v5 slides 19 and 41 give the schema and its content; the Ownership Map has two S4 table rows and the FSD field catalog repeats the legal_action columns only.",
    "Architecture v5's list of what the schema holds as the entity set, with the physical names left to the DB story.",
    "Medium", "Data architect, before the S4 DB story",
    "The migration and the boundary test cannot be written until the table set exists; no story is blocked by it.",
    "Section 8.1; Section 10.4; Section 12 OQ-S4-03")

asm(4,
    "A link to the case is a business-key column of type varchar(255) with no foreign key, and legal_action.case_id keeps its FSD name and takes the case number rather than a uuid from another schema.",
    "ADR-014 and DP-01 forbid a cross-schema reference and the platform pattern is a varchar(255) business key; the FSD types the column as uuid.",
    "The FSD's column as the name and the meaning of the link, not as its physical type.",
    "High", "Data architect, before the S4 DB story",
    "A uuid foreign key into rwb_case is a boundary breach the conformance check would reject.",
    "Section 8.1; Section 8.4 rule 3; Section 12 OQ-S4-04")

asm(5,
    "This service decides that a notice is due, approves it and owns the notice period; rwb-comms owns the template, the merge fields, the delivery and the proof of delivery, and returns the served result as NoticeDelivered. The notice period starts from the delivered_at that rwb-comms returns.",
    "Architecture v5 slide 41 gives notices, templates, merge fields and proof of delivery to rwb-comms, and the Ownership Map gives two of the three notice paths to P6 and the approval path to S4.",
    "FSD A2.1 to A2.3 as the notice requirement set, with the content and the delivery read as the comms service's and the decision and the clock as this service's.",
    "Medium", "Solution architect with P6, before the wave 2 notice test",
    "Two writers of the served result would leave the notice period starting from a date neither service owns.",
    "Section 2.3; Section 5.1; Section 6 FR-S4-003; Section 9; Section 12 OQ-S4-05")

asm(6,
    "The notice slice keeps the wave 2 that R5.6's wave map gives EP02 and is published as a contract with its fake before wave 3; the remaining capability is built in wave 3 against the same contract.",
    "The FSD puts the notice in E2 and the service in wave 3, and R5.6 keeps the wave map wave when it is earlier than the service wave.",
    "The FSD's module table and screen list as the statement of when the notice is first needed, with the delivery read through the contract rule of R5.6 and R5.7.",
    "Medium", "Solution architect with the programme manager, before E2 system test",
    "If the notice waits for wave 3, the E2 release loses the notice approval screen and the notice period.",
    "Section 5 CAP-S4-001 to CAP-S4-003 (wave 2); Section 6 FR-S4-001 to FR-S4-009; Section 10.2; Section 12 OQ-S4-06")

asm(7,
    "The thirty-two R-LIT rules the FSD names are the requirement set of this PRD and the other forty-seven are authoring work for the litigation package in rwb-decision, whose code, version label and owner must exist before the wave 3 release.",
    "The FSD names 32 of the 79 rules the BRD cites and the Drools design says the litigation package is Phase 2.",
    "The FSD rule tables as the rules the requirements are written from, with the remaining rule numbers read as the package authoring list.",
    "Medium", "Center of excellence analyst with P7, before the wave 3 release",
    "A requirement tested against a rule that is not in force is a requirement that cannot be signed off.",
    "Section 5.1; Section 10.4; Section 12 OQ-S4-07")

asm(8,
    "Each FSD acceptance criterion row is read as one criterion per feature, and the step-specific criteria in this PRD are written from the rules each feature names, with the FSD row cited as their evidence.",
    "All forty-four main and exception criteria of the FSD are the same generic sentences and there is no alternate flow and no background event for any feature.",
    "The FSD's criteria as a coverage statement rather than as a testable outcome.",
    "Medium", "Business analyst, S4, before the story files are written",
    "Without step-specific criteria the story scenarios would repeat the generic sentence and prove nothing.",
    "Section 11.1; Section 12 OQ-S4-08")

asm(9,
    "LawsuitFiled, JudgmentRecorded and AuctionResult are carried as the topic's contract, keyed by the case, with rwb-asset and rwb-case as consumers, and no EV number is asserted for any of them.",
    "Architecture v5 slide 19 names the three events and slide 43 lists two of them on an unnumbered '+' row; the Ownership Map has no S4 event row.",
    "Slide 19's OUT contract as the event requirement, with the catalogue id left to the event catalogue change.",
    "Medium", "Solution architect, before the wave 3 system test",
    "A consumer cannot be wired to a contract row that does not exist, so the reporting and asset subscriptions would be built on a name only.",
    "Section 5.1; Section 6 FR-S4-040 and FR-S4-050; Section 9; Section 10.4; Section 12 OQ-S4-09")

asm(10,
    "No route number is asserted in this document: the legal action starts when the route decision names litigation or when a restructure or settlement plan breaks, and the route numbering is settled in rwb-decision as reference data.",
    "The Drools design says R-LIT-01 starts litigation on R4 while the case journeys call R4 the guarantee claim and R5 litigation.",
    "The FSD's scope as starting at the notices, with the trigger read from the rule IDs R-LIT-01 and R-LIT-02 and no route number.",
    "Low", "Business analyst, S4 with P7, before the wave 3 system test",
    "A wrong route number starts the legal action on the wrong decision and leaves the real litigation case unstarted.",
    "Section 12 OQ-S4-10")

asm(11,
    "REQ-S4-009 is carried under BR-034, the requirement that owns the statutory clock, through FR-S4-051 and FR-S4-052; BR-038 and BR-042 are traced from the FSD features FEAT-LIT-10 and FEAT-LIT-17 to FEAT-LIT-21 and the RWB-E5 story keys.",
    "The E5 requirement set has no row for REQ-S4-009 and BR-038 and BR-042 carry no program requirement ID.",
    "The program requirement set and the E5 requirement set as two views of one need, with the missing link recorded rather than invented.",
    "Medium", "Product Owner with the business analyst, before the wave 3 release",
    "A requirement with no BR row cannot be prioritised in the BRD, and a BR with no program ID cannot be reported against.",
    "Section 11.2; Section 12 OQ-S4-11")

asm(12,
    "The three screens are served from gateway-bff composite routes and this service answers the legal-action part of each; the screen owner cell and the route are recorded with the edge work.",
    "The FSD lists three screens and neither Architecture v5 nor the Ownership Map states which service owns a screen.",
    "FSD Screens as the screen requirement, with the route read as the edge pattern of DP-19.",
    "Medium", "Solution architect, before the wave 3 release",
    "A screen without a route owner cannot be built, and a composite route that joins the wrong services shows the officer a different case.",
    "Section 2.3; Section 9; Section 12 OQ-S4-12")

asm(13,
    "The message IDs and the English wording of the FSD are preserved character for character, and the Thai wording, the field-level text of MSG-GEN-001 and the approver are left to the message work DL10 names.",
    "The FSD gives one English wording per message, no Thai wording and no approver, and DL10 and NFR-059 require both languages and an approver.",
    "The FSD's message column as the ID set and the English text, with the rest read as the message work.",
    "Medium", "Business analyst, S4 with Legal counsel and Compliance, before the wave 2 release",
    "A message without an approved Thai wording fails the label review and cannot be shown on a live case.",
    "Section 12 OQ-S4-17")

asm(14,
    "No litigation, hearing or enforcement volume is asserted: NFR-S4-005 uses the population figures the non-functional specification states and marks the module split as open, and every release date is copied unchanged and tentative.",
    "The FSD states one metric per feature and no volume, and the non-functional specification's volumes are not split by module.",
    "The non-functional specification's population figures as the sizing base, with the module share left to the solution architect.",
    "Medium", "Solution architect with Risk, before the wave 3 release",
    "A volume target invented per module would be either unachievable or too loose to test.",
    "Section 7 NFR-S4-005; Section 11 AC-S4-039; Section 12 OQ-S4-16")

asm(15,
    "This PRD stays at status Draft and the Product Owner and FDA approval is not recorded in this run; the approval table is deliberately empty.",
    "D-RCV-60 runs without a human verification stop (U8) and the run records missing approval as an assumption rather than waiting for it.",
    "The PRD Builder contract's requirements-approval gate as satisfied by the assumption, with the decision itself left to the Product Owner and the FDA.",
    "High", "Product Owner and FDA, before the requirement is baselined",
    "The requirements cannot be baselined, and no later stage may treat this document as approved.",
    "Section 1.1 Status; Section 13")

asm(16,
    "The BRD is read as approved for this run: Business Requirements Program v5 and Business Requirements Epics 3 to 8 v1 are treated as the approved baseline, and the missing governance decision is carried as this assumption.",
    "The PRD Builder precondition asks for an Approved BRD with a Product Owner decision, and the run is not allowed to stop for a missing approval (D-RCV-60 overlay).",
    "The BRD requirement text, priorities and owners as the approved baseline for this PRD, with the governance entry read as pending.",
    "Medium", "Product Owner, before the requirement is baselined",
    "If the BRD changes at approval, the BR references in this PRD must be re-checked against the approved version.",
    "Section 1.1 Status")

asm(17,
    "The service wave (3) and the business epic wave of EP05 (3) are the same, so no wave conflict is raised for Epic 5; the only wave conflict in this document is the Epic 2 notice slice.",
    "R5.6's wave map puts EP04 and EP05 in wave 3 and the Arch v5 wave table puts S4 in wave 3.",
    "The two wave tables as one statement for Epic 5, with the conflict rule applied only where the waves differ.",
    "High", "Solution architect, before the wave 3 release",
    "An unnecessary conflict gap would send a sequencing question to the programme manager that the sources already answer.",
    "Section 10.3; Section 12 OQ-S4-06")

asm(18,
    "Every release date in this document is copied unchanged from the Program BRD release plan and marked (tentative): E2 31 December 2026 and E5 31 March 2027.",
    "U7 and DL48 keep the dates as they are and treat them as tentative, and a date is never raised as a gap.",
    "The Program BRD section 8 release plan as the only date source, with no date recomputed from a duration.",
    "High", "Programme manager, at each release review",
    "A date presented as fixed would be committed to before the programme's own review.",
    "Section 1.1 Release; Section 10; Section 11.3")

asm(19,
    "Every owner, approver and persona in this document is a role and no person is named anywhere, including in the approval table and the sources appendix.",
    "U3 and DL46 name owners by team type only, and check C12 rejects a person name taken from the issue-tracker export.",
    "The FSD's role tables and the BRD's owner column as role names, with no named individual anywhere.",
    "High", "Product Owner, before the requirement is baselined",
    "A named individual in a document that is circulated outside the bank is a personal-data exposure.",
    "Section 3; Section 13")

asm(20,
    "The CAP, FR, NFR, AC, JRN, ROL and OQ identifiers of this document are new and exist only here; the FSD's requirement, feature, rule, message, list and screen identifiers are preserved character for character, and no identifier of this document is reused from another module.",
    "The PRD Builder creates its own identifier families and the realignment must keep the source identifiers stable so the story files and the traceability matrix can be read against both.",
    "The S1 PRD's identifier scheme as the family pattern, with the module letter changed to S4.",
    "High", "Business analyst, S4, before the story files are written",
    "A colliding identifier would make a traceability row point at two different requirements.",
    "Section 1.3; the whole document")

with io.open("_work/msr/assumptions/" + WP + ".jsonl", "w", encoding="utf-8", newline="\n") as f:
    for r in asms:
        f.write(json.dumps(r, ensure_ascii=False) + "\n")

print("gaps", len(gaps), "asms", len(asms))
for p in ("_work/msr/gaps/" + WP + ".jsonl", "_work/msr/assumptions/" + WP + ".jsonl"):
    for i, line in enumerate(io.open(p, encoding="utf-8"), 1):
        json.loads(line)
    print("ok", p)

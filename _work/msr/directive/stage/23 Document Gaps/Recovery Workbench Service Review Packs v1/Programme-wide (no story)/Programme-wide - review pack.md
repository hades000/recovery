# Programme-wide (no story) - review pack

Decision: D-RCV-60. Date: 26 November 2026. Status: Draft (directive resolutions). Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

Directive run result for this service: every gap and assumption was resolved with the recommended resolution, except business decisions. Review this pack, then the staged story files it lists. Row IDs (ruling R-, item GAP-/ASM-/CG-, CDC-) match the master registers in 23 Document Gaps.

## 1. Summary

| Measure | Count |
|---|---|
| Stories | 0 |
| Resolved in the stories | 0 |
| Cross-document (pending in another document) | 136 |
| Not applied (value not in the sources) | 0 |
| Open business decisions | 247 |
| Register gaps linked | 451 |
| Unconfirmed assumptions | 176 |
| Lint findings | 0 |

## 3. Open business decisions (not resolved; owner decides)

| Story | Ruling | Item | Kind | Owner role | Title | Proposed resolution |
|---|---|---|---|---|---|---|
| - | R-09156 | GAP-0010 | Register gap | Compliance and IT risk | BOT approval route under FPG 19/2560 clause 5.5 | Confirm the route in wave 0 and place the submission date in the programme plan |
| - | R-09158 | GAP-0304 | Register gap | Programme governance | The BOT approval under FPG 19/2560 clause 5.5 is not in the cutover plan and its submission date is not stated | Confirm with Compliance whether the change is significant under clause 5.5, name the submission date and the owner, and record both in section 9 before the Wave 1 rehearsal. |
| - | R-09160 | GAP-1592 | Register gap | Product Owner | The BRDs carry no status field and no approval record, so the requirements approval gate has no recorded baseline | The PRD is issued as Draft with an empty approval table and the gate stays open. The BRD next versions add a Status row and the Product Owner decision. |
| - | R-09162 | GAP-1863 | Register gap | IT lead with Operational Risk | Recovery point objective not stated for the 19 services | Confirm one recovery point objective for the 19 Recovery schemas on the ACE PostgreSQL server, with the ACE platform tier as the floor, and replace the target of NFR-022 with it at the next NFR baseline; the value belongs to the failover and restore test of section 3.4 |
| - | R-09163 | GAP-1864 | Register gap | IT lead with Operational Risk | Recovery time objective not stated for the 19 services | Confirm one recovery time objective with a tier per service wave (0 to 4) and replace the target of NFR-023 with it at the next NFR baseline; the value drives the failover and restore test and the 99.9 percent target of NFR-020 |
| - | R-09165 | GAP-3185 | Register gap | Product owner with the integration lead | RWB-E2-023 has no row in the plan, so it has no service, lane or new stories | Add a slice set for RWB-E2-023 with rwb-integration as primary service, register it in the plan, and re-run the story split for wave 2. |
| - | R-09166 | GAP-3235 | Register gap | ACE team with Enterprise Architecture; Platform team; Risk and Internal Audit; Compliance and IT Risk | Five of the six Wave 0 platform dependencies of Architecture v5 slide 39 have no row in the external dependency table | Record the five on the Dependency classes sheet exactly as slide 39 states them and create no new DEP ID in this version; the next version of the Risks Assumptions Issues and Dependencies document takes them as DEP-37 to DEP-41 with the slide 39 owner roles. |
| - | R-09169 | GAP-3255 | Register gap | Compliance | 29 of 32 regulatory obligations not confirmed | Compliance and Legal confirm each obligation in scope |
| - | R-21677 | GAP-0178 | Register gap | Compliance with P7 rwb-decision | The decision log archive rule keeps a copy in the data lake | Keep the 10-year period and replace the archive rule with the central decision ledger of rwb_decision, the local decision record and the rwb.decision-record.v1 topic. |
| - | R-21679 | GAP-0180 | Register gap | Compliance | No retention period for tables that carry no data-product row | State the placeholder in the three schema rows that hold only such tables and leave the period to the bank retention schedule when Compliance issues it under DL26. |
| - | R-21680 | GAP-0181 | Register gap | Legal counsel with P3 rwb-case and P5 rwb-document | A legal hold on a party or a document has no field in the target | Record the hold on the case and have the P5 retention job exclude every document of a held case, as the P5 acceptance criteria already assume. |
| - | R-21685 | GAP-0196 | Register gap | Reporting and BI analyst; Compliance | The reporting and outbound leg of REG-15 and REG-27 is covered by no control | Add a control on P9 rwb-reporting for the BOT repossessed-vehicle and loss-on-sale report and for the credit-bureau correction file, or extend the Controls cells of REG-15 and REG-27 to name the P2 outbound item, and reissue the map. |
| - | R-21686 | GAP-0197 | Register gap | Compliance and PDPA officer | The personal data breach notification of REG-25 has no owning service | Add the incident and breach process to the Ownership Map (an incident record and an event in P9 rwb-reporting or P4 rwb-access), add a control for the breach notification and its time limit, then reissue this map with the new owner service. |
| - | R-21703 | GAP-0309 | Register gap | Programme governance | No source names a service owner for the run of any of the 19 services | Name one service owner role for each of the 19 services, record it on the Services sheet of the Ownership Map next to the work-type suggestion, and close DL02 at the same time. |
| - | R-21704 | GAP-0310 | Register gap | Programme governance | The tier 2 and tier 3 roles of version 2 are not defined per service now that there are 19 services | State, for each tier, the role that serves each service, for example one platform administrator per wave, and print that role on the service's run book page. |
| - | R-21707 | GAP-0320 | Register gap | Product owner with the two tech leads and the program manager | Two recovery squads and fourteen source module names do not map one to one onto nineteen services | Keep the squad and module words of version 2, and put the service, the source module and the squad side by side on the Services and squads sheet. Record the story slices and legacy stories per service from the plan. The per-service headcount stays open. |
| - | R-21708 | GAP-0321 | Register gap | Product owner with the two tech leads | Six services have no source module and no squad in the resource plan | Carry the R9 placeholder for the squad of the six services on the Services and squads sheet, and let the first daily review assign them as the Structure sheet says. |
| - | R-21711 | GAP-1453 | Register gap | Product owner | RWB-E1-014 is live in the BRD but retired by D-RCV-60 | Business owner confirms the retirement and the later home (reporting read model from events) at the next BRD review; the BRD text is then re-worded in a later version, not in this one. |
| - | R-21712 | GAP-1454 | Register gap | Product owner | RWB-E1-029 is live in the BRD but was cancelled before this run | Business owner confirms whether the cancellation stands; if it does, the requirement is marked Removed in a later BRD version with its later home named. |
| - | R-21713 | GAP-1455 | Register gap | Product owner | RWB-E1-048 is live in the BRD but was cancelled before this run | Business owner confirms whether the cancellation stands; if it does, the requirement is marked Removed in a later BRD version with its later home named. |
| - | R-21714 | GAP-1459 | Register gap | Product owner with the data product owner | RWB-E2-023 Automated EFS file load has no legacy story and no slice in the plan | Add a slice set for RWB-E2-023 with rwb-integration as primary service and register it in the plan before the wave 2 build starts. |
| - | R-21715 | GAP-1498 | Register gap | Product owner | No requirement section for P8 payment, P9 reporting or P10 agent | Add the three service epics to the delivery model with no requirement row, and let the service PRD carry their requirements until a later version adds the sections. |
| - | R-21716 | GAP-1550 | Register gap | Product owner | BRD and FSD approval status is not evidenced in the source documents | Record the Product Owner and FDA decisions on the BRD, then on this PRD. |
| - | R-21717 | GAP-1555 | Register gap | Compliance | No retention period is set for any case record class | Set the period per record class under DL26 before the wave 4 closure feature is built. |
| - | R-21723 | GAP-1655 | Register gap | Compliance and PDPA officer | No retention class or retention period is set for a snapshot, an extract or a run record | Declare a class per entity now, and apply the periods from DL26 when they are set |
| - | R-21724 | GAP-1725 | Register gap | Risk with the product heads | The release of a guarantor and of a TCG guarantee have approval authorities but no requirement | Deliver the release through the approval path in rwb-decision with the level read from the delegation table, state the behaviour as a capability of this product, and keep the limits out of this document until DL18 answers them. |
| - | R-21725 | GAP-1729 | Register gap | Compliance and PDPA officer | The retention class and the masking rules of the claim record are not set | Apply a record class to the claim and to the guarantor record, hold the period as reference data, and mask the party fields by role once DL26 answers; no period is stated in this document. |
| - | R-21726 | GAP-1734 | Register gap | Business lead | The number of claims a month and the number of guarantors a case are not stated | State the volume target as the program case volume that this service inherits and carry the claim share as an open question until the business lead sets it. |
| - | R-21730 | GAP-1867 | Register gap | Business lead | Concurrency and named-user figures disagree between section 2, NFR-002 and NFR-003 and Architecture v5 | Confirm one concurrent-user figure per population for the busiest hour and use it in NFR-002, NFR-003 and the load test; the named-user total of 1,234 stays |
| - | R-21770 | GAP-3260 | Register gap | Business lead | 20 business measures have a To set baseline or target | Measure owners set each value |
| - | R-28136 | GAP-0020 | Register gap | Compliance | Regulatory source dates and coverage | Compliance confirms the three citations before the wave 1 gate |
| - | R-28144 | GAP-0084 | Register gap | Model Risk | The monitoring rows name governance roles only, with no service owner for the data | Keep the three roles word for word and add the data owner of each measure from the Ownership Map: score coverage P1, drift P10 and P7, outcome P1 and P7. |
| - | R-28159 | GAP-0117 | Register gap | Programme governance | Owner labels in the Decision Log name individuals, not roles | Confirm the role that owns each of the fifteen open decisions named here and record the role, not the individual, in the Decision Log and in every document that quotes these rows. |
| - | R-28160 | GAP-0119 | Register gap | Programme governance | The version date in the Decision Log header is earlier than its last decision | State which date the header carries: the issue date of the version or the date the sheet text was last edited. The date is kept unchanged in v11 either way. |
| - | R-28185 | GAP-0175 | Register gap | Programme governance | No approval of version 4 is recorded | Record the approval of the Controls Catalog v4 by the control owner and the programme governance forum, and carry the approved status in the Read me sheet. |
| - | R-28187 | GAP-0177 | Register gap | Compliance | The metadata table reads version 1 while the file name reads v2 | Take the file name as the family version, so this version is 3, and keep the source reading in a Source version row of the metadata table and in the change log. |
| - | R-28188 | GAP-0183 | Register gap | Compliance with P4 rwb-access | The access-log period refers to a bank standard that is not in the run sources | Keep the period and the archive rule as written, name rwb-access as the owner, and leave the store and the standard to the security design and the bank retention schedule. |
| - | R-28191 | GAP-0186 | Register gap | Compliance | Version 2 document stamps itself Version 1 | Treat the file name as the version of record; issue this next version as v3 with the source version named in the metadata table. |
| - | R-28193 | GAP-0189 | Register gap | Compliance | Version 2 records no approval or document status | Issue v3 as Draft and leave the approval to the programme governance step after the run. |
| - | R-28195 | GAP-0192 | Register gap | Compliance | Data subject access retrieval across 19 services | Retrieve through each owning service's contract under the Compliance role and scope, with rwb-case (P3) supplying the case ID and case view; no new service is added. |
| - | R-28196 | GAP-0194 | Register gap | Programme governance | The source workbook states no version date and records no approval | Record the issue date of version 2 and the approval of version 3 from the document register in the Read me sheet, and keep the draft status until that approval exists. |
| - | R-28197 | GAP-0195 | Register gap | Compliance; service owner | The obligations map names no service owner | Confirm the owner service of each of the 32 obligations with Compliance, Legal and the service owners, and keep the basis column as the record of the ruling. |
| - | R-28198 | GAP-0198 | Register gap | Compliance; data steward | The map and the Controls Catalog disagree on which controls answer four obligations | Reconcile the two documents in one pass: either add CTL-43 and CTL-44 to the Controls cells of REG-11, REG-22, REG-27 and REG-32, or remove them from the Controls Catalog Obligations column, and record the ruling in the Change Register. |
| - | R-28199 | GAP-0199 | Register gap | Compliance; conduct and QA | Two obligations rest on the conduct sample whose owner service is itself an assumption | Confirm P9 rwb-reporting as owner of the conduct sample in the Ownership Map before E8; this map then follows without change. |
| - | R-28201 | GAP-0201 | Register gap | Compliance; programme governance | The Owner column and the new Owner service column can be read as one owner | Confirm that both columns are wanted in the next version, and consider renaming column G to Business owner so the two are not read as alternatives. |
| - | R-28207 | GAP-0290 | Register gap | Programme governance | No approval of version 6 is recorded and the source carries no Status row | Record the approval of version 6 by the solution architect, the ACE team and the programme, with a date, and keep a Status row with the approver role in every later version. |
| - | R-28211 | GAP-0297 | Register gap | Programme governance | Version 5 carries no approval and the source records no status | Record the approval of version 5 by the programme and the delivery lead with a date, and keep a Status row in every later version. |
| - | R-28213 | GAP-0307 | Register gap | Business lead | The tracker retirement names the six teams but no service, so the replacement case list per team is not stated | Name the screen or report each of the six teams uses in the retirement week, and record it in the six-team report filed on 26 November 2026. |
| - | R-28214 | GAP-0308 | Register gap | Programme governance | The source carries no Status or approval row, and no approval of this version is recorded | Record the approval of version 4 by the release owner, the ACE team and the programme, with a date, and keep a Status row with the approver role in every later version. |
| - | R-28217 | GAP-0315 | Register gap | Programme governance | No approval of version 3 is recorded and the source deck carries no status | Record the approval of version 3 by the programme, the solution architect and the ACE team, with a date, and keep a status line on the cover and in the change log of every later version. |
| - | R-28225 | GAP-0328 | Register gap | Product owner with the Collection squad and P3 rwb-case | The shared Epic 2 items of DL30 are not identified per service | Keep the shared items with the Collection squad as the source says and list them per service when the Epic 2 BRD names them. |
| - | R-28226 | GAP-0329 | Register gap | Program manager with the business lead | No approval of the resource plan is recorded | Issue version 3 as Draft and record the missing approval as an assumption, as AGENTS.md rule 9 requires. |
| - | R-28244 | GAP-1458 | Register gap | Business lead | Four open-decision rows name people in the owner column and no owner role | Business lead states the owner role for each of the four decisions; the cell then carries the role. |
| - | R-28245 | GAP-1460 | Register gap | Product owner | Two open decisions name individuals as owners and the source states no role for either | Name the role that holds DL03 and DL09 when each decision is answered, and keep the role in place of the individual in every future version. |
| - | R-28246 | GAP-1461 | Register gap | Product owner | The document control block says Version 1 and 28 October 2026 while the source file is v2 and this version is 3 | Correct the metadata table at the next human edit so the version and the date match the file name. |
| - | R-28247 | GAP-1462 | Register gap | Product owner with the business lead | Ten Epic 2 legacy keys in the plan have no requirement row in this BRD | Name the source document of each key in the traceability file, or add the requirement to the next version of this BRD. |
| - | R-28248 | GAP-1491 | Register gap | Programme governance | Section 9 names persons as decision owners | Confirm the role that owns each of DL06, DL12, DL13 and DL20 and record the role, not the person, in the decision log. |
| - | R-28256 | GAP-1556 | Register gap | Solution architect with Risk | Non-functional target values are open under DL11 | Adopt the ACE values for RPO and RTO and record them under DL11. |
| - | R-28258 | GAP-1611 | Register gap | Product owner with the FDA | The business requirements document carries no approval for this service and this PRD is issued as Draft | Issue this PRD as Draft with an empty approval table and record the missing business approval as an assumption; the Product Owner and the FDA approve the PRD when the business requirements documents are approved. |
| - | R-28259 | GAP-1642 | Register gap | Product Owner | No approval is recorded for this product baseline | Keep the status at Draft and the approval table empty, and record the missing approval as an assumption; the Product Owner and the FDA approve the baseline and this PRD together. |
| - | R-28261 | GAP-1661 | Register gap | Product Owner | No approval is recorded for this PRD | Record the Product Owner and FDA decision before wave 1 build starts |
| - | R-28262 | GAP-1665 | Register gap | Product owner | No predecessor PRD exists in the PLT family | Treat this file as the family baseline v1 and version from it. |
| - | R-28265 | GAP-1765 | Register gap | Product Owner | No approval is recorded for the requirements this PRD states | Hold the document at Draft, leave the approval table empty, and record the Product Owner and FDA approval as the next step after this run. |
| - | R-28273 | GAP-1978 | Register gap | Programme governance | Owner labels in the open points name individuals, not roles | Confirm the role that owns each of the six open points and record the role, not the individual, in section 8 and in every document that quotes these rows. |
| - | R-28274 | GAP-1979 | Register gap | Programme governance | Version 4 carries the version 3 approval statuses and no approval of the 19-service decision | Record the approval of version 4 by SCB CTO and SCB IT architecture, and decide whether the replacing ADRs of 22 November 2026 are accepted with it, so that the status column and section 9 can carry an approved state. |
| - | R-28310 | GAP-2117 | Register gap | Programme governance | No approval of the new version is recorded and the source has no Status row | Record the approval of version 3 by the test lead and the programme, with a date, and add a Status row with the approver role to the metadata table of every later version. |
| - | R-28318 | GAP-2129 | Register gap | Business lead | Accessibility is 'each screen' and no screen inventory exists | Section 9 keeps 'Each screen' as a gate on every screen of every service, and section 6 names no screen; the screens are read from each service's REST base and its tabs. |
| - | R-28323 | GAP-2142 | Register gap | Product owner; service owner | No owner per service is stated, and no owner table exists | Confirm table 1.1 as the owner reference of every story and keep the roles of section 1 and section 5 for the gate approval itself. |
| - | R-28326 | GAP-2149 | Register gap | Product owner; service owner; DevOps lead | No owner and no approval path are stated for contract publication or for the boundary test | Confirm the two added rows and the four-eyes review path for a contract version. |
| - | R-28391 | GAP-3237 | Register gap | Programme governance | Version 3 carries no approval record and no status, so version 4 has no approved baseline | Record the approval of version 4 when the programme approves it, and state the approved version in the title block at the next issue. |
| - | R-28398 | GAP-3267 | Register gap | Business lead | DL09 owner differs between the epic BRDs | Confirm the DL09 owner in the Decision Log |
| - | R-33469 | ASM-0011 | Register assumption |  | The release dates carried in the v2 context stay unchanged and tentative; Arch v5 waves 0-4 are not mapped to them in this run. | Product Owner |
| - | R-33471 | ASM-0013 | Register assumption |  | The decision record is written locally in one transaction with the state change and sealed in the central ledger; strict mode applies at the four points of no return. | RW-RISK and Internal Audit |
| - | R-33474 | ASM-0016 | Register assumption |  | Phase 1 packages stay in XLS decision-table format; DMN 1.6 conversion is table by table on the same Drools runtime. | RW-COE and RW-RISK |
| - | R-33478 | ASM-0020 | Register assumption |  | The move to 19 services is treated as a significant change for FPG 19/2560 clause 5.5 until Compliance says otherwise, and the 30 business day lead time is planned. | Compliance and IT risk |
| - | R-33483 | ASM-0025 | Register assumption |  | RPO and RTO stay unset in this baseline; no target is claimed. | Compliance and Product Owner |
| - | R-33488 | ASM-0030 | Register assumption |  | The three regulatory citations are used as the architecture source states them and Compliance confirms them before the wave 1 gate. | Compliance |
| - | R-33581 | ASM-0144 | Register assumption |  | The three monitoring owner roles of version 2 are kept word for word, and the data each measure reads is attributed to its owner in the Ownership Map: score coverage to rwb-source-data (P1), drift to rwb-agent (P10) and rwb-decision (P7), outcome to rwb-source-data (P1) and rwb-decision (P7). | Model Risk and the data owners |
| - | R-33627 | ASM-0191 | Register assumption |  | The header date of v10, 15 November 2026, is read as the date the sheet text was last edited, not as the issue date of the version, and is carried into v11 unchanged. | Programme governance |
| - | R-33680 | ASM-0246 | Register assumption |  | The DoA limit amounts stay in the Delegation of Authority Matrix and in the versioned DoA rule package; delegation_limit in rwb_access holds them and GET /doa-limits serves them. | Product head (Mortgage, HP, SSME) |
| - | R-33692 | ASM-0259 | Register assumption |  | Version 4 is issued as Draft because no approval of it is recorded in any source, and the catalog carries no approval row in version 3 either. | Record the approval of version 4 by the control owner and the programme governance forum. |
| - | R-33694 | ASM-0261 | Register assumption |  | The file name gives the family version, so this document is version 3; the source reading of Version 1 and Date 28 October 2026 is kept in a Source version row and in the change log. |  |
| - | R-33695 | ASM-0262 | Register assumption |  | The decision log is kept in rwb_decision, in the append-only decision_log_entry table and the central ledger, with the local decision record of the owning service; no copy goes to a data lake. |  |
| - | R-33697 | ASM-0265 | Register assumption |  | A legal hold on a party or on a document is recorded on the case in recovery_case.legal_hold and applied by the P5 retention job, which excludes the documents of a held case. |  |
| - | R-33699 | ASM-0267 | Register assumption |  | The access-log period stays per the bank security standard and its archive rule stays; the store behind GET /admin/access-log belongs to P4 rwb-access and is not in the Physical Schema v6. |  |
| - | R-33707 | ASM-0276 | Register assumption |  | The file name is the version of record, so the source is version 2 and this document is version 3; the internal stamp of 1 is kept as a source fact and named in the metadata table. | Compliance |
| - | R-33710 | ASM-0279 | Register assumption |  | This version is issued as Draft because no approval or document status is recorded in version 2. | Compliance |
| - | R-33713 | ASM-0282 | Register assumption |  | A data subject request is served by reading each owning service's contract under the Compliance role and scope, joined on the case ID from rwb-case; no new retrieval service is added. | Compliance |
| - | R-33715 | ASM-0284 | Register assumption |  | Version 2 of the regulatory requirements map is treated as the baseline immediately before version 3. Its issue date is written as the placeholder of Template and Rules R9 because no sheet states one, and version 3 is issued as Draft because no approval is recorded in any source of this run. | Programme governance |
| - | R-33716 | ASM-0285 | Register assumption |  | The 32 obligations keep every cell of columns A to H word for word, and one owner service with its basis is added per obligation, taken from the controls in column F through the Ownership Map v1 and the Controls Catalog v4. | Compliance; service owners |
| - | R-33717 | ASM-0286 | Register assumption |  | The owner service in column I is taken only from the controls the Controls cell names. Where a reporting or outbound-file leg of an obligation belongs to another service - P9 rwb-reporting for REG-15 and P2 rwb-integration for REG-27 - that service is named in the basis column and not in the owner service column, so column I stays a direct read of the controls. | Reporting and BI analyst; Compliance |
| - | R-33718 | ASM-0287 | Register assumption |  | REG-25 keeps S9 rwb-partner as its owner service because CTL-37 is the only control the row names, and the breach-notification step itself is recorded as having no owning object in the Ownership Map rather than being assigned to a service by guesswork. | Compliance and PDPA officer |
| - | R-33719 | ASM-0288 | Register assumption |  | Where the Controls Catalog v4 and this map disagree on which controls answer an obligation, the Controls cell of this map is kept word for word, the difference is stated in the basis column, and the owner service follows this map's Controls cell. | Compliance; data steward |
| - | R-33720 | ASM-0289 | Register assumption |  | REG-02 and REG-08 keep P9 rwb-reporting as owner service, carried from CTL-39 and from the ruling recorded in the Controls Catalog v4 (ASM-B-CTRL-32-4), and the dependency on that ruling is named in the row. | Compliance; conduct and QA |
| - | R-33722 | ASM-0291 | Register assumption |  | Column G Owner, the business role, and column I Owner service, the service that holds the control evidence, are both kept, and the Read me states that they are different dimensions. | Compliance; programme governance |
| - | R-33743 | ASM-0312 | Register assumption |  | Column D keeps its stewardship owner, and the service that loads and serves the list is read from the appended 'Owning service (D-RCV-60)' and 'Owning schema (D-RCV-60)' columns; the Key sheet gains both terms. | Data steward and data product owner confirms at the wave 1 document review that the two columns are read as stewardship and service ownership. |
| - | R-33808 | ASM-0380 | Register assumption |  | Version 6 is issued as Draft with no recorded approval, and the approval is carried as an open gap and this assumption. | Programme governance |
| - | R-33815 | ASM-0387 | Register assumption |  | Version 5 is issued as Draft with no recorded approval; the per-epic status words of the source stay as they stand (E1 and E2 Confirmed, E3 to E8 Proposed). | Programme governance |
| - | R-33823 | ASM-0395 | Register assumption |  | BOT approval under FPG 19/2560 clause 5.5 is treated as required before the Wave 1 cutover, with the submission date open, and it is carried as a gate in section 10.2 step 1 and as an open decision in section 9. | Programme governance with Compliance |
| - | R-33826 | ASM-0398 | Register assumption |  | The tracker retirement stays a team procedure run by the six team managers against the Wave 1 case list of rwb-case, with the data steward recording the fields no data product carries; no service is named as the owner of a tracker or of the retirement report. | Business lead with the six team managers and the data steward |
| - | R-33827 | ASM-0399 | Register assumption |  | Version 4 is issued as Draft with no recorded approval, and the approval is carried as an open gap and this assumption. | Programme governance |
| - | R-33829 | ASM-0401 | Register assumption |  | The owner of a service is its service code in the Ownership Map v1, with TechX as the suggested team for every service, and the run-time service owner stays open until one role is named per service. | Programme governance with the solution architect |
| - | R-33830 | ASM-0402 | Register assumption |  | The tier 2 and tier 3 roles of version 2 keep serving all 19 services as one pool until the per-service role is stated, and each service's run book page is read by that pool. | Programme governance with the ACE team |
| - | R-33835 | ASM-0407 | Register assumption |  | Version 3 is issued as Draft with no recorded approval, and the approval is carried as an open gap and this assumption. | Programme governance |
| - | R-33840 | ASM-0412 | Register assumption |  | The fourteen source module names are read as the service mapping of thirteen services: squad 1 carries P1 rwb-source-data (data engine), P3 rwb-case (case and workflow), the rules component of every service (the embedded Drools kit, DP-04), P4 rwb-access, S1 rwb-valuation, S5 rwb-asset and S8 rwb-deviation; squad 2 carries P5 rwb-document, P6 rwb-comms, P7 rwb-decision, S2 rwb-treatment, S4 rwb-litigation, S6 rwb-debtsale and S7 rwb-writeoff. Per-service headcount is not derived and is left open. | Product owner with the two tech leads |
| - | R-33841 | ASM-0413 | Register assumption |  | The six services with no source module (P2, P8, P9, P10, S3, S9) are left at the R9 placeholder for the squad and are assigned at the first daily review, as the Structure sheet says the split is agreed there. | Product owner with the two tech leads |
| - | R-33848 | ASM-0420 | Register assumption |  | The shared Epic 2 items stay with the Collection squad as version 2 says, and are not split across the nineteen services in this version. | Product owner with the Collection squad |
| - | R-33849 | ASM-0421 | Register assumption |  | Version 3 is issued as Draft because no approval is recorded for the source or for this realignment, and the run overlay of D-RCV-60 asks for a record instead of a stop. | Program manager with the business lead |
| - | R-33993 | ASM-2169 | Register assumption |  | REQ-DRI-009 is read as the reporting requirement it describes and not as a requirement on rwb-comms: the daily agent measures are available from the P9 rwb-reporting read model with the row counts matched against the P10 source, and the notification of a cost breach is the only part of the legacy story that remains with rwb-comms. The requirement identifier and its owner are unchanged and no date is changed. | Data steward and data product owner |
| - | R-34005 | ASM-2332 | Register assumption |  | The model version of agent INTAKE is a P10 fact that arrives inside the record; the fixtures of this story carry a synthetic model version and the criteria assert that the value is present and travels unchanged, never a particular value. | P10 agent runtime business analyst with the model risk officer, at the agent policy approval |
| - | R-34104 | ASM-2555 | Register assumption |  | The requirement text of RWB-E1-014, RWB-E1-029 and RWB-E1-048 is unchanged; their realignment position appears only in section 8.5, section 9 and the gap register. | Product owner confirms the three positions |
| - | R-34113 | ASM-2565 | Register assumption |  | RWB-E2-023 is read as module P2 Integration from its section heading, which is the only source that places it. | Product owner and the rwb-integration service owner |
| - | R-34116 | ASM-2570 | Register assumption |  | The settlement range and the floor price are read per product from versioned reference rows. Only a documented test version is used in SIT, and the production version is approved by the product head like the treatment policy. | Product head (Mortgage, HP, SSME) with Risk |
| - | R-34117 | ASM-2571 | Register assumption |  | The offer validity of 14 days stated in the rule rows is the documented test value. The cure period, the maximum number of breaks and the queue and approval service levels are parameters with no value until DL22 and DL23 are loaded. | Business lead before the E3 release |
| - | R-34118 | ASM-2572 | Register assumption |  | Notice periods and prescription periods are read from the legal periods table that Epic 1 already holds, and the litigation step service levels are read from the service level reference data. No period is restated in this document. | Legal counsel before the E5 release |
| - | R-34121 | ASM-2575 | Register assumption |  | The write-off exception loop is owned by the write-off team, escalates to its team manager when the time limit passes, and is recorded as an unmapped owner until the operating model names the role. | Head of recovery |
| - | R-34122 | ASM-2576 | Register assumption |  | Enforcement after judgment is held by the enforcement owner role the rules already name, and an eviction is held by the sale officer with Legal counsel named on the case. The assignment is recorded as an assumption until the operating model names the holder. | Head of Litigation with Legal counsel |
| - | R-34123 | ASM-2577 | Register assumption |  | The non performing asset stock position is owned per case by the NPA and asset manager, and the monthly stock report goes to the head of NPA. | Head of NPA |
| - | R-34124 | ASM-2578 | Register assumption |  | The 54 percent figure is the debt sale cap in force at the release, held as a versioned policy parameter whose version label carries the basis and the period, and headroom is computed against the population the policy names. | Head of Asset Liquidity with Risk |
| - | R-34125 | ASM-2579 | Register assumption |  | Buyer qualification uses the bank's existing KYC and licensing checks, with the accepted licence types and their validity held as reference data, and the debt sale officer may bar a buyer with Compliance confirming the reason. | Compliance and PDPA officer |
| - | R-34126 | ASM-2580 | Register assumption |  | A retention class and a masking rule per record class and role are versioned reference data applied at creation, and a disposal that would breach a period not yet set is recorded as a decision rather than carried out. | Compliance and PDPA officer with Legal counsel |
| - | R-34128 | ASM-2582 | Register assumption |  | An autonomy level stays at its current setting until the risk owner loads a measure, a threshold and an approval level per agent and per decision as a versioned row; no step-up is taken on a threshold this document invented. | Risk and model risk officer |
| - | R-34129 | ASM-2583 | Register assumption |  | The deceased customer capability is read as the E7 deviation flow RWB-E7-003 and is recorded in the E3 scope as delivered in E7, with the E3 program requirement served through it. | Product Owner |
| - | R-34134 | ASM-2588 | Register assumption |  | Benefit realisation reports the eight program measures of the program requirements until the benefit model is supplied, and the report is labelled as the program measure set. | Finance and CFO delegate |
| - | R-34143 | ASM-2597 | Register assumption |  | The debt sale turnaround is measured from lot selection to award and transfer, and the 45 day target stands until a baseline is measured on the first lot. | Head of Asset Liquidity |
| - | R-34147 | ASM-2601 | Register assumption |  | Agent acceptance, override rate, latency and cost are reported per agent and per decision from the agent run record, with no target until the model risk owner sets one. | Risk and model risk officer |
| - | R-34159 | ASM-2615 | Register assumption |  | P8 payment, P9 reporting and P10 agent have no requirement section in this BRD, and their service epics appear in the delivery model with no requirement row. | Product owner |
| - | R-34162 | ASM-2618 | Register assumption |  | The retention class per data product and recovery table is declared here as versioned data, the archive rule table and the monthly archive run belong to rwb-document, and ACE retains ACE data. | Compliance and PDPA officer, before wave 1 release |
| - | R-34163 | ASM-2619 | Register assumption |  | Role-level read access per data product is held here; field-level masking rules are held by rwb-access and applied here, and a personal field with no masking row for the role is returned masked. | Compliance and PDPA officer, before wave 1 release |
| - | R-34164 | ASM-2620 | Register assumption |  | This service builds and publishes the case list rows and holds their publication status; the case list screen and its filters are served by rwb-case over those rows. | Product owner, at the Epic 1 story review |
| - | R-34172 | ASM-2628 | Register assumption |  | The four-label classification in this PRD is read from the personal-data markers in the field catalogues: personal fields and the party and contact extension rows as personal data, balances, amounts, offers, debt sale and money as sensitive financial data, case, legal, collateral, documents and metadata as confidential, and no data product as public. | Compliance with Security, when DL26 closes |
| - | R-34187 | ASM-2643 | Register assumption |  | Because the FSD P10 requirement table is empty, every functional requirement of this PRD is mapped to the FSD section and to the acceptance criteria it serves, and to the feature code FEAT-AGT-nn where the feature overview carries one; no FSD requirement ID is invented. | Business analyst, P10 |
| - | R-34191 | ASM-2647 | Register assumption |  | Every target the source does not state is written with the R9 placeholder and carried as an open question; the only numeric targets stated in the source set are the 60 second agent target and the fallback rate below 10 percent, and both are carried as stated. | Solution architect with Risk |
| - | R-34192 | ASM-2648 | Register assumption |  | The run, the guardrail result, the feedback, the sample, the evaluation and the alert are retained for the period set for them, are answerable to audit before a purge and are never removed silently; the period is written with the R9 placeholder until DL26 is answered. | Compliance |
| - | R-34197 | ASM-2653 | Register assumption |  | RWB-E2-028, RWB-E2-029 and RWB-E2-030 are read as the legacy story keys of the feedback, the screening rejection and the legal document pack, even though BRD Epic 2 v3 holds no requirement row for them. | Product owner with the backlog builder |
| - | R-34202 | ASM-2658 | Register assumption |  | The message codes MSG-P10-001 to MSG-P10-008 are referenced with the behaviour the source states and with no invented wording; the wording is taken from the Error and Message Standard at build time, and where the source does not say which service owns a message the PRD leaves that to the screen owner. | Business lead with the centre of excellence |
| - | R-34204 | ASM-2660 | Register assumption |  | SCR-46 Agent monitor is described by what it shows and by the filter it applies (agent, policy version, prompt version, business date); its layout, components and states follow the Design System and Component Library and are not fixed by this PRD. | Business lead |
| - | R-34214 | ASM-2670 | Register assumption |  | The PRD covers the requirements rwb-integration owns (REQ-DRI-006, REQ-DRI-007, REQ-DRI-008 and REQ-DRI-013) and the one wave-2 orchestration step those requirements and the FSD carry; the consumer-side compositions assigned to the service in later wave story slices are not restated as P2 product requirements and are carried as open question Q-P2-06. | Product Owner with the solution architect |
| - | R-34217 | ASM-2673 | Register assumption |  | The debt buyer tape carries only the fields that the approved sale terms and the approved mask list allow, the mask list is a reference-data row owned by Compliance, and no field-level rule is fixed by this PRD. | Compliance with Legal |
| - | R-34223 | ASM-2679 | Register assumption |  | The retention period of an outbound item, a delivery record, a manifest and a transmission acknowledgement is open under DL26; the PRD requires only that the record of a send, an exception and a resend outlives the retention period of the case it belongs to. | Compliance with Legal |
| - | R-34224 | ASM-2680 | Register assumption |  | The BRD and this PRD are treated as not yet approved; the PRD is issued as Draft with an empty approval table. | Product owner |
| - | R-34231 | ASM-2687 | Register assumption |  | The recovery point and recovery time objectives adopt the ACE values; the value of each is left open until DL11 is answered. | IT lead with Operational risk |
| - | R-34236 | ASM-2692 | Register assumption |  | The queue write interface for models and agents is built dark in wave 2 and switched on only when a consumer is approved. | AI product owner |
| - | R-34238 | ASM-2694 | Register assumption |  | No retention period is stated: the case record classes are carried as DL26 open, and the PRD states the requirement and the variable, not a period. | Compliance |
| - | R-34239 | ASM-2695 | Register assumption |  | The three slices with no requirement row (encumbrance check, proof of delivery, committee routing) stay in the later waves as delivery items and are not given an FR in this PRD. | Product owner |
| - | R-34243 | ASM-2699 | Register assumption |  | rwb-access keeps identity and session, roles, permissions, scope, masking, the delegation of authority table, the access log and break-glass. The reference-data load surface, the rule package registry and its six operations, the platform smoke workflow, the case record view, the list of values and the partner identity rows are outside this service and are recorded as dependencies only. | Solution architect and the owners of rwb-case, rwb-decision, rwb-partner and the platform library |
| - | R-34245 | ASM-2701 | Register assumption |  | The masking answer names a personal field ID with a masked or clear marker and never a rendering, the client renders the masked form of the field, and a masked caller never causes a clear value to be retrieved from the ACE PII path. A personal field with no masking row for any role is masked for every role. | Compliance with the solution architect at the masking policy review |
| - | R-34252 | ASM-2710 | Register assumption |  | The third object of REQ-ACA-006, written as 'the data lake copy', is read as 'a data product', because Architecture v5 removes the data lake and the reporting read model is built from events into rwb-reporting. Nothing else in the requirement changes. | Compliance with the solution architect when REQ-ACA-006 is re-issued |
| - | R-34253 | ASM-2711 | Register assumption |  | BRD Program v4, BRD Epic 1 v4 and BRD Epic 2 v2 are taken as the approved business baseline for this PRD even though none of them carries a status field or an approval record, so the PRD is issued as Draft with an empty approval table and the requirements approval gate stays open. | Product Owner and FDA at the requirements approval gate |
| - | R-34256 | ASM-2714 | Register assumption |  | Legal hold is a product behaviour of this service, driven by the hold that rwb-case records, and it is released in wave 4 with RWB-AD-021 even though REQ-DCM-016 is an Epic 1 Must; the retention class and the virus scan that the hold overlays are released in wave 1. | Solution architect with Legal counsel |
| - | R-34257 | ASM-2715 | Register assumption |  | E-discovery production and court-ready evidence are in scope of this PRD and are released in wave 2, with the discovery response target left open until Legal counsel sets one. | Legal counsel |
| - | R-34258 | ASM-2717 | Register assumption |  | The retention classes named in the FSD acceptance criteria (GENERAL05Y, LEGAL10Y, DOCTYPE-2026.11 and RET-2026.11) are read as examples taken from a reference-table version, not as approved periods; the period behind each class stays open and the retention rule table is read as the versioned table that carries it. | Compliance and PDPA officer |
| - | R-34259 | ASM-2718 | Register assumption |  | The 26 extracted fields are read as the union of the per-type field definitions delivered in the signed reference load; this PRD requires the count to reconcile with 26 and the two named types to keep their four fields each, and does not enumerate the remaining four types. | Business lead with Legal counsel and the Head of NPA |
| - | R-34260 | ASM-2719 | Register assumption |  | OCR, document classification and field extraction are reached through a contract owned outside this service, either as an AgentRunCompleted event or as a Temporal child run on queue rwb-document, and malware scanning is a platform security service; P5 owns the intake, the text, the confidence, the review queue, the index and the decision record that carries the versions. | Solution architect with the AI product owner |
| - | R-34265 | ASM-2724 | Register assumption |  | Every read of a document and of its extracted fields through this service is logged; the data lake clause of NFR-042 is not carried because no lake copy of the document store exists in the target. | Compliance and PDPA officer |
| - | R-34270 | ASM-2730 | Register assumption |  | REQ-OCC-007 and REQ-OCC-008 are read as this service's contribution to the case record view and the case timeline: the notice and message block with its states and the ordered notice and message history. The view and the timeline are rwb-case's product. | Product owner with the solution architect, before wave 1 release |
| - | R-34275 | ASM-2735 | Register assumption |  | The volume test is sized on the document volume of about 860,000 in 2027 as the upper bound for letters and on the interaction volume for messages, until the business lead states the notice and message counts. | Business lead with the data lead, before wave 2 performance test |
| - | R-34276 | ASM-2736 | Register assumption |  | A retention class is declared on the notice record, the template version and the merge-field catalog as versioned data; the periods stay open under DL26 and rwb-document applies the archive and disposal. | Compliance with Legal, before wave 3 |
| - | R-34278 | ASM-2738 | Register assumption |  | The Legal approval is recorded on the template version as a decision record written through rwb-decision, and the approval of a demand or recall notice is taken on the generated notice through the approval workflow. | Product owner with Legal counsel, before wave 1 release |
| - | R-34279 | ASM-2739 | Register assumption |  | The seven features that v5 places elsewhere (payment matching and the plan-payment-missed event, the steering dashboard, partner identities, custody movement, the legal or audit document request and retention on closure) are kept in the source with their identifiers and are not built in this service. | Product owner, before wave 2 |
| - | R-34283 | ASM-2743 | Register assumption |  | This PRD is issued as Draft with an empty approval table because the business requirements documents it rests on are Draft in this run; the Product Owner and the FDA approve it when they approve the business requirements. | Product owner with the FDA, at the requirements approval gate |
| - | R-34290 | ASM-2750 | Register assumption |  | Notice generation, letter template management, the template catalog with merge fields and proof of delivery from WIN belong to rwb-comms, with rwb-document for the document and rwb-integration for the WIN file. This service keeps only the approval of a D7.1 notice and the recording of the template version on the approval. | Business lead with Legal counsel and the rwb-comms owner |
| - | R-34292 | ASM-2752 | Register assumption |  | The delegation of authority table is rwb-access's. This service reads a limit through the access contract at the moment of the decision, records the delegation row ID and the limit version on the approval, and loads and approves no limit file. | Risk and model risk officer with the rwb-access owner |
| - | R-34294 | ASM-2754 | Register assumption |  | A retention class is required for every decision record class and every ledger entry class, and the periods themselves stay open under DL26. The service runs no archive of its own and keeps the seal for the class period once set. | Compliance and PDPA officer |
| - | R-34298 | ASM-2758 | Register assumption |  | Committee members present and their votes are carried in the approval terms structure until the field list is agreed, and the decision-log entry records the committee's outcome and its approver. | Business lead with the center of excellence analyst before Epic 4 |
| - | R-34306 | ASM-2766 | Register assumption |  | The posting file holds one line per posting with case, account key, entry type, amount, value date, business date and posting reference, is delivered by rwb-integration with a manifest that states the count and a checksum, and has no personal data on any line. | Finance and CFO delegate with the solution architect, before wave 3 |
| - | R-34308 | ASM-2768 | Register assumption |  | A payment reversal is out of scope for this release; the behaviour is specified nowhere in the FSD and is carried as an open question, and the case reopens only through rwb-case when a reversal is reported to it. | Business lead with Credit Administration, before wave 3 |
| - | R-34309 | ASM-2769 | Register assumption |  | Fee rates, caps and bases are versioned rows in a fee table owned by Finance, read at run time; until the table and its owner are named, no fee is calculated by the service. | Finance and CFO delegate, before wave 3 |
| - | R-34312 | ASM-2772 | Register assumption |  | The order in which a receipt is applied to the balance is a versioned row set with an owner and a valid-from date; the sequence itself is a Finance decision and is not written here. | Finance and CFO delegate, before wave 3 |
| - | R-34314 | ASM-2774 | Register assumption |  | The measure 'receipts matched the same day' is read from the decision log per match, counted on the business date of the run against the receipt date, until the product owner sets a baseline, a target and the definition. | Product owner with the Tribe lead, before wave 2 release |
| - | R-34317 | ASM-2778 | Register assumption |  | This document stays at status Draft with an empty approval table; the missing Product Owner and FDA approval is carried as an assumption, not as an answer. | Product Owner and the FDA, after this run |
| - | R-34324 | ASM-2785 | Register assumption |  | This PRD stays in Draft and records no approval. | Product Owner and FDA |
| - | R-34326 | ASM-2787 | Register assumption |  | The service is created in wave 1 and serves EP02, EP06 and EP08 from the same read model. | Solution architect |
| - | R-34332 | ASM-2793 | Register assumption |  | The reconciliation result and the break rows are read from rwb-source-data's contract, and the break view and its closure live in this service. | Data steward and data product owner with P1 |
| - | R-34336 | ASM-2797 | Register assumption |  | Every reporting entity declares a retention class now and takes its period from DL26 when it is set. | Compliance and PDPA officer |
| - | R-34337 | ASM-2798 | Register assumption |  | Benefit realisation reports each measured value against the frozen baseline and states where the benefit model sets no measure or no target. | Finance and CFO delegate |
| - | R-34340 | ASM-2801 | Register assumption |  | Agent acceptance and override are counted from the decision record, which carries the agent and prompt version, the recommendation, the approval and the outcome. | Solution architect with the AI product owner |
| - | R-34342 | ASM-2803 | Register assumption |  | Agent acceptance and override are published per agent and version with no threshold, and an agent with no recommendations shows 'No runs'. | Risk and model risk officer |
| - | R-34347 | ASM-2808 | Register assumption |  | There is no predecessor PRD in the PLT family, so this document is version 1. | Product owner |
| - | R-34358 | ASM-2819 | Register assumption |  | A target the source does not state is held open with the placeholder and is never invented: the recovery point and time, the namespace quotas, the key rotation period, the retention of the platform rows and telemetry, and the stored idempotent answer period. | Compliance |
| - | R-34360 | ASM-2821 | Register assumption |  | Telemetry carries identifiers and facts only: party identifiers, names, addresses and document content are scrubbed before export, and the field list is open under DL26. | Compliance |
| - | R-34378 | ASM-2840 | Register assumption |  | The valuation record, the route decision and the route agent output carry a classification from the working labels of this document and a retention class whose period stays open under DL26. | Compliance and PDPA officer, before wave 3 release |
| - | R-34379 | ASM-2841 | Register assumption |  | This document stays at status Draft with an empty approval table, and the missing requirements approval is carried as an assumption. | Product Owner, after this run |
| - | R-34400 | ASM-2864 | Register assumption |  | The treatment, the agreements and the plan timers carry a classification from the working labels of this document (SENSITIVE_FINANCIAL for the terms and the agreements, CONFIDENTIAL for the references), and the retention period is stated as open. | Compliance and PDPA officer, before wave 3 release |
| - | R-34403 | ASM-2867 | Register assumption |  | This document stays at status Draft with an empty approval table, and the missing requirements approval is treated as an assumption rather than as an answer. | Product Owner and FDA, after this run |
| - | R-34418 | ASM-2882 | Register assumption |  | The insurance claim is delivered as the Must behaviour of BR-025 and traced through REQ-S3-002 for the claim status it records on the case, and a program requirement for the collateral event is raised when the program requirement set is next versioned. | Product Owner, before wave 3 release |
| - | R-34422 | ASM-2887 | Register assumption |  | The claim is classified [SENSITIVE_FINANCIAL] and the guarantor party fields [PII], the periods are held as reference data by record class, and no period is stated in this document. | Compliance and PDPA officer, before wave 3 release |
| - | R-34427 | ASM-2892 | Register assumption |  | The volume target of this service is the program case volume it inherits and the number of claims a month, of guarantors a case and of notices a demand are carried as open, with no count recomputed here. | Business lead, before wave 3 release |
| - | R-34443 | ASM-2908 | Register assumption |  | REQ-S4-009 is carried under BR-034, the requirement that owns the statutory clock, through FR-S4-051 and FR-S4-052; BR-038 and BR-042 are traced from the FSD features FEAT-LIT-10 and FEAT-LIT-17 to FEAT-LIT-21 and the RWB-E5 story keys. | Product Owner with the business analyst, before the wave 3 release |
| - | R-34463 | ASM-2928 | Register assumption |  | The route recommendation and the price proposal are decisions of the disposal rule set; where an agent proposes, it is reached only through the rwb-agent contract, waits at most 60 s, falls back to the rule result and leaves a run record. | Solution architect with the model risk officer, before wave 2 system test |
| - | R-34465 | ASM-2930 | Register assumption |  | The stock balance owner is the NPA and asset manager role held as versioned reference data until Q-009 answers, and the monthly balance is refused where no owner role is in force. | Head of NPA, before wave 2 release |
| - | R-34466 | ASM-2931 | Register assumption |  | Every floor limit and approval level is read at run time from the versioned delegation table of rwb-access, the three amounts and the three percentages of the design slide are carried as stated, and the direction of the test is held open until DL18 and Q-001 answer. | Risk with the product heads, before wave 2 release |
| - | R-34467 | ASM-2932 | Register assumption |  | Sale prices, values, floors and cost amounts are [SENSITIVE_FINANCIAL], bidder and customer identity are [PII], vendor and partner data are [CONFIDENTIAL], and the retention periods stay open. | Compliance and PDPA officer, before wave 2 release |
| - | R-34468 | ASM-2933 | Register assumption |  | This document stays at status Draft with an empty approval table; the missing Product Owner and FDA approval is carried as an assumption and not as an answer. | Product Owner and FDA, after this run |
| - | R-34472 | ASM-2937 | Register assumption |  | The service is sized on the case volume and the NPA book of NFR-001 until the asset, round and holding cost volumes are given, and the missing volume blocks the performance test only. | Solution architect with the data product owner, before wave 2 release |
| - | R-34483 | ASM-2948 | Register assumption |  | The KYC result, the licence expiry and the panel status of a buyer are held as data on the buyer record, the panel is read through the S9 contract, and the evidence the officer accepted is recorded with the admission. | Compliance and PDPA officer, before wave 4 release |
| - | R-34484 | ASM-2949 | Register assumption |  | The debt sale cap, its denominator and its period are one versioned reference-data row owned by the Head of Asset Liquidity, and the version applied is recorded at the selection, the award and the headroom report. | Head of Asset Liquidity, before wave 4 release |
| - | R-34485 | ASM-2950 | Register assumption |  | The lot approval and the award are routed through P7's approval child on the P4 delegation table, with the secured and unsecured bands of design slide 22 held as versioned reference data and the level applied and the approving role recorded on the award. | Risk with the product heads, before wave 4 release |
| - | R-34493 | ASM-2958 | Register assumption |  | borrower_code and account_key are personal data in use: they are masked on every screen and on the tape and the transfer file by role, and the is_personal flag is corrected in the next version of the Logical Data Model and the physical schema. | Compliance and PDPA officer, before wave 3 system test |
| - | R-34497 | ASM-2962 | Register assumption |  | Every record this service holds carries a data classification and a retention class, the periods are held as reference data from DL26, and the tape and the transfer file inherit the class of the record they are derived from. | Compliance and PDPA officer, before wave 3 release |
| - | R-34498 | ASM-2963 | Register assumption |  | The put-back claim window, the buyer remediation window and the settlement term are versioned reference-data values with valid-from dates, held from DL22, and the value in force at the business date of the lot is applied and recorded. | Head of Asset Liquidity, before wave 4 release |
| - | R-34515 | ASM-2980 | Register assumption |  | The write-off exception loop is owned by the write-off team role until a named owner is decided, and it carries one time limit as a data row rather than a code constant. | Head of recovery, before wave 4 release |
| - | R-34516 | ASM-2981 | Register assumption |  | No write-off cap value, basis or period is asserted, and the population is reported against the cap only once the cap exists; the committee limit of R-WO-11 and R-WO-12 is the only limit this release enforces. | Head of Asset Liquidity with Risk, before wave 4 release |
| - | R-34517 | ASM-2982 | Register assumption |  | The committee approval is taken through the approval workflow on rwb-decision, the limit is read from the delegation table at run time, and the level applied and the approver role are recorded; the level values are loaded from the regulation under DL18 and the committee composition is taken as open under Q-001. | Risk with the product heads, before wave 4 release |
| - | R-34519 | ASM-2984 | Register assumption |  | A retention class and a retention period are held as data on every document and every record this service closes on, the closure is held when a class is missing, and the periods themselves stay open under DL26 and Q-012. | Compliance and PDPA officer, before wave 4 release |
| - | R-34526 | ASM-2991 | Register assumption |  | This version is Draft and its approval table stays empty: no Product Owner decision and no FDA decision exists for the BRD or the FSD this PRD is built from, so no approval is claimed. | Product Owner, before the requirements gate |
| - | R-34538 | ASM-3003 | Register assumption |  | The deceased customer slice lands twice on purpose: the contact stop, the heir and estate notification and the insurance claim path as the E3 slice in wave 2, and the full X3 flow with its approver and return point in wave 4. | Product Owner, answering Q-015 |
| - | R-34540 | ASM-3005 | Register assumption |  | The deviation service level, the ten working day escalation and the thirty day skip trace window are versioned reference data read at run time; no number is asserted in this document. | Business lead, setting DL22 |
| - | R-34541 | ASM-3006 | Register assumption |  | The confidence threshold that sends a flag to a person and the autonomy policy that permits L1 on a segment are held as versioned reference data by rwb-agent and rwb-decision; this service reads them and asserts no value. | Risk and model risk officer with the P10 owner, before the L1 run |
| - | R-34542 | ASM-3007 | Register assumption |  | The deviation record, the screening run and the breach record are confidential records attached to a case; the staff identifier of the handler is confidential rather than personal customer data, and no retention period is stated. | Compliance and PDPA officer, closing DL26 and Q-012 |
| - | R-34569 | ASM-3034 | Register assumption |  | The three partner tables carry the Workbench record class, and the periods stay open until DL26 answers; the partner, its instructions and its results stay readable after an exit. | Compliance and PDPA officer, before wave 4 release |
| - | R-34571 | ASM-3036 | Register assumption |  | The four reused messages keep their published wording, and the module's own refusals, holds, differences and breach notices are authored with the story from the Error and Message Standard in Thai and English. | Business analyst, S9 with Legal counsel and Compliance, before wave 4 release |
| - | R-34589 | ASM-3054 | Register assumption |  | Until the recovery point objective is confirmed, no RPO value is tested. NFR-022 stays Open under DL11, the recovery test is run against the ACE platform tier, and the section R9 placeholder stands in its owning service cell. | IT lead with Operational Risk states the RPO in the failover and restore test plan |
| - | R-34590 | ASM-3055 | Register assumption |  | Until the recovery time objective is confirmed, no RTO value is tested. NFR-023 stays Open under DL11, the recovery test is run against the ACE platform tier, and the section R9 placeholder stands in its owning service cell. | IT lead with Operational Risk states the RTO per service wave in the failover and restore test plan |
| - | R-34593 | ASM-3058 | Register assumption |  | Where the concurrency figures differ, Architecture v5 slide 48 is used for the load test: 414 concurrent staff, 48 concurrent partners and about 21 requests a second. The requirement text keeps its own figures, including the named-user total of 1,234. | Business lead confirms one concurrent-user figure per population at the next NFR baseline |
| - | R-34640 | ASM-3141 | Register assumption |  | The former owner is represented by the sale officer acting on the case, and enters this story only as a party key the owner's contract answers. No customer or borrower role, no customer screen and no external edge is added, and the buy-back is signed by the approver the limit names and not by the former owner inside the Workbench. | The owner of rwb-access with the sales business owner |
| - | R-34689 | ASM-3200 | Register assumption |  | Version 4 carries the version 3 approval statuses unchanged in section 9, gives the four replaced decision rows the Proposed status of the record that replaces them, and is issued as Draft. | Record the approval of version 4 and of the replacing ADRs by SCB CTO and SCB IT architecture. |
| - | R-34766 | ASM-3277 | Register assumption |  | Masking is applied twice and both controls stay: rwb-source-data masks in v_ace_customer and v_ace_contact and in its contract, and every service re-applies the masking_rule rows of rwb-access at its own API before the response leaves. | Compliance confirms that masking in the owning service at the API is the primary PDPA control and that the view mask is a second control. |
| - | R-34781 | ASM-3292 | Register assumption |  | The decision log is measured twice: the local decision record of each service in its own schema, and the central ledger of P7 rwb-decision that collects rwb.decision-record.v1 within 5 minutes and runs the chain check as JOB-14 at 02:00. | Risk and Internal Audit accept the local record plus central ledger model (ADR-022). |
| - | R-34782 | ASM-3293 | Register assumption |  | The six recipient names of version 3 are kept character for character and read as role names, not as persons; only RW-PLATADM and RW-COE appear in the source as role codes, and no mapping of the other names to a role code is invented here. | P4 rwb-access confirms the role codes and the recipient mapping before the alert rules are built. |
| - | R-34785 | ASM-3296 | Register assumption |  | The hash chain alert is raised on the local chain of each service and once on the central ledger of P7 rwb-decision, and a break is attributed to the service whose chain fails, with the daily check as JOB-14 at 02:00. | P7 rwb-decision and Internal Audit confirm the check and the attribution in the run book. |
| - | R-34796 | ASM-3307 | Register assumption |  | No recovery point objective and no recovery time objective is set for any store or any service. Every store row and every service statement carries the placeholder 'Not specified in the source documents (CG-B-TECH-11-2; ASM-B-TECH-11-2)'; no tier, no number of minutes and no number of hours is taken from the proposed tiers that Architecture v5 mentions. | SCB IT infrastructure with Operations and Compliance set the ACE value and the per-store tier before the first production release. |
| - | R-34810 | ASM-3321 | Register assumption |  | The file name gives the version of the family and the metadata table gives the document's own issue number. The source is therefore version 2 of the family and version 1 of its own table, and this document is version 3. The source values are kept in a 'Source version' row as 1, 28 October 2026. | The document owner confirms the version numbering of the family. |
| - | R-34817 | ASM-3328 | Register assumption |  | Every retention period of the source is kept as written under DL26. Where each period is held and which job enforces it is left open: the retention tables of the map are rwb-document (P5) and JOB-17 is document retention, so the ledger and access-log periods need their own rows, owned by P7, P1 and P4. | Compliance states where the three periods are held and which job enforces them. |
| - | R-34819 | ASM-3330 | Register assumption |  | The approver of a decision is stored as an identifier, never as a name. The identifier is masked in every export under the masking rows of rwb-access and every read of the field is recorded in the PII log. | Compliance and Information Security confirm the protection of the column and the mask. |
| - | R-34844 | ASM-3355 | Register assumption |  | DL10 is read as answered on 5 November 2026 with answer A, 'Thai field names'. The source row and its fallback answer are kept word for word, section 6.1 records the answer, and this document adds no Thai wording. | The business lead with Legal and Compliance confirms the DL10 answer applies to notices. |
| - | R-34845 | ASM-3356 | Register assumption |  | Templates and merge fields are owned by P6 rwb-comms in rwb_comms, following Architecture v5 slide 41 and the Ownership Map v1. The DL28 answer of 13 November 2026, which gives them to the document module, is recorded as a conflict and is not applied. | The product owner reaffirms or amends DL28 before RWB-P6-AD017 is Done. |
| - | R-34847 | ASM-3358 | Register assumption |  | The verified contact point and its consent state are held by P1 rwb-source-data in contact_point_ext and are read and maintained through a P1 contract. The P6 screen maintains them through that contract and never writes rwb_source_data directly. | The P1 and P6 service owners agree the contract, and the P1 API specification publishes the contact-point operation. |
| - | R-34848 | ASM-3359 | Register assumption |  | A contact stop is read as X1 to X3, following the Temporal and Drools design, so a death (X3) holds messages and letters except statutory notices where the law requires service. The wider reading is applied and R-LIT-05 is flagged for correction. | The business lead corrects R-LIT-05 or confirms the X1 to X3 reading. |
| - | R-34853 | ASM-3364 | Register assumption |  | Contact times and frequency are reference data of P3 rwb-case, read through the reference-data contract (H RWB-PLT-E1043-CON; C RWB-P3-E1043-CON), and are not held by P4. Roles and DoA stay with P4. | The P3 and P4 service owners confirm the split. |
| - | R-34854 | ASM-3365 | Register assumption |  | The Compliance approval of customer wording is recorded as a second approval of P7 rwb-decision with the template as its source, while approved_by_legal, approved_by and approved_at on the template row record the Legal approval that POST /admin/templates/{templateId}/approve writes. | Compliance and Legal confirm the second approval and where it is recorded. |
| - | R-34890 | ASM-3402 | Register assumption |  | Version 3 carries Status Draft in the metadata table, states in the opening note that no approval is recorded, and is issued without an approval round. | Record the approval of version 3 by the test lead and the programme, with a date. |
| - | R-34905 | ASM-3417 | Register assumption |  | The accessibility gate 'Each screen' is read as every screen of every service, reached through that service's REST base, and no screen list is added because no source names one. | The business lead confirms the screen list per service when SIT starts. |
| - | R-34908 | ASM-3420 | Register assumption |  | Until NFR-022 and NFR-023 are set under DL11, every restore test runs against the ACE recovery objectives recorded under DL11 and is re-run when a target is set; NFR-071 stays Open under DL27. | The IT lead with Operational Risk sets NFR-022 and NFR-023. |
| - | R-34916 | ASM-3428 | Register assumption |  | rwb-access (P4) holds the approved masking version as masking_rule; rwb-source-data (P1) applies the mask at the 30 recovery.v_ace_* views; the service that owns a personal field applies display masking at its API under the same version. | Compliance |
| - | R-34924 | ASM-3436 | Register assumption |  | Every owner named in the document is read from the Ownership Map v1: the 19 services of sheet Services with their wave, schema and REST base, and the owner team of each kind of work from R5.3. The roles of the Checked by column and of section 5 stay as the approvers of the gate itself. | Confirm table 1.1 as the owner reference of every story. |
| - | R-34931 | ASM-3443 | Register assumption |  | Contract publication is owned by the owning service team from its contract story and changes only through a new published version after a four-eyes review; the boundary test is owned by the owning service team with the DevOps team on the golden pipeline and changes only with platform approval. | Confirm the two rows and the review path for a contract version. |
| - | R-35094 | ASM-3829 | Register assumption |  | A field whose is_personal is true needs at least one masking_rule row at the masking version in force, and a personal field with no row is masked for every role and reported as a coverage failure of the load; the count of personal fields among the 1,366 is not stated by any source, so the register reports the count it finds and no criterion asserts a fixed number. | Compliance and PDPA officer with the pack owner |
| - | R-35173 | ASM-4719 | Register assumption |  | Both stories stay at Status Draft (realignment v1) and the missing approval of the FSD S5 and the TSD S5 is recorded rather than awaited. | Solution architect and the business owner of S5 |
| - | R-35234 | ASM-5570 | Register assumption |  | The INT-19 extract and the data lake are removed, and rwb-reporting publishes the measure rows and events the data set reads. | Reporting and BI lead |
| - | R-35242 | ASM-5578 | Register assumption |  | The primary service of a story is the primary the plan gives its legacy key, and RWB-E2-023, which has no plan row, takes its primary service from the source module line, its wave from the EP02 W-MAP rule and its release from the catalogue rows of the same epic. | Programme office with the solution architect |
| - | R-35244 | ASM-5580 | Register assumption |  | The story set of this document is the 42 stories of the source version, which is one more than the 41 plan keys because RWB-E2-023 is in the source and not in the plan. | Programme office |
| - | R-35277 | ASM-5614 | Register assumption |  | A requirement named in a PRD as an upstream ID but carried by no functional requirement is flagged, not mapped to a nearby FR. | Product owner confirms or withdraws each flagged requirement. |
| - | R-35313 | ASM-5650 | Register assumption |  | The five Wave 0 dependencies of Architecture v5 slide 39 stay on the Dependency classes sheet exactly as slide 39 states them, and no new DEP ID is created in this version. | Program manager with the solution architect |
| - | R-35320 | ASM-5657 | Register assumption |  | Version 4 is issued as Draft with no recorded approval, and the approval is carried as an open row. | Programme governance |
| - | R-35348 | ASM-5685 | Register assumption |  | The regulatory, audit, control and report rows are copied unchanged from their workbooks, with the owner service the workbook names | Compliance and Audit confirm the rows |
| - | R-35349 | ASM-5686 | Register assumption |  | A measure value of To set is copied as written and means the value is not set | Measure owners set the values |

## 4. Not applied (the value is not in the source documents)

None.

## 5. Cross-document changes (pending in the target document)


### 05 Technical architecture/Recovery Workbench Environment and Deployment Design v5.docx (10)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-20376 |  | GAP-0134 |  | write failed: WRITE FAILED (nothing was written): N001-F1: paragraph found 0 time(s), expected 1 |
| CDC-20377 |  | GAP-2009 |  | write failed: WRITE FAILED (nothing was written): N001-F1: paragraph found 0 time(s), expected 1 |
| CDC-20378 |  | GAP-2121 |  | write failed: WRITE FAILED (nothing was written): N001-F1: paragraph found 0 time(s), expected 1 |
| CDC-20379 |  | GAP-0306 |  | write failed: WRITE FAILED (nothing was written): N001-F1: paragraph found 0 time(s), expected 1 |
| CDC-20380 |  | GAP-1988 |  | write failed: WRITE FAILED (nothing was written): N001-F1: paragraph found 0 time(s), expected 1 |
| CDC-20381 |  | GAP-2010 |  | write failed: WRITE FAILED (nothing was written): N001-F1: paragraph found 0 time(s), expected 1 |
| CDC-20382 |  | GAP-2012 |  | write failed: WRITE FAILED (nothing was written): N001-F1: paragraph found 0 time(s), expected 1 |
| CDC-20383 |  | GAP-2011 |  | write failed: WRITE FAILED (nothing was written): N001-F1: paragraph found 0 time(s), expected 1 |
| CDC-20384 |  | GAP-2013 |  | write failed: WRITE FAILED (nothing was written): N001-F1: paragraph found 0 time(s), expected 1 |
| CDC-20385 |  | GAP-0287 |  | write failed: WRITE FAILED (nothing was written): N001-F1: paragraph found 0 time(s), expected 1 |

### 05 Technical architecture/Recovery Workbench Batch and Scheduling Design v5.xlsx (9)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-20358 |  | GAP-0008 |  | JOB-16 in Jobs and the map: Temporal Schedule, rwb-writeoff, monthly 3rd working day, gated on AceDataReady. Checked against the v5 build script, not the live file. |
| CDC-20359 |  | GAP-0031 |  | JOB-01 is retired, no new story, read through the rwb-source-data ACE view contract. Checked against the v5 build script, not the live file. |
| CDC-20360 |  | GAP-0033 |  | JOB-09 is retired, no new story, read through the v_ace_* views owned by rwb-source-data. Checked against the v5 build script, not the live file. |
| CDC-20361 |  | GAP-0034 |  | JOB-10 note: rwb-comms owns the notice, window and Schedule; rwb-integration performs deliverFile. Checked against the v5 build script. |
| CDC-20362 |  | GAP-0043 |  | JOB-10 is owned by P6 rwb-comms, with deliverFile in rwb-integration. Checked against the v5 build script, not the live file. |
| CDC-20363 |  | GAP-0044 |  | JOB-13: continuous DecisionRecorded ingest in P7 rwb-decision, no data-lake copy, no Schedule. Checked against the v5 build script. |
| CDC-20364 |  | GAP-0045 |  | JOB-15: Airflow-triggered buildRegulatoryExtract in P9 rwb-reporting, no data lake. Checked against the v5 build script. |
| CDC-20365 |  | GAP-0046 |  | JOB-16: Temporal Schedule write-off scan in S7 rwb-writeoff on the 3rd working day. Checked against the v5 build script. |
| CDC-20366 |  | GAP-0142 |  | Needs Schedule IDs, cron, catch-up duration and pause rule no source gives. SKIP, Asia/Bangkok, ID placeholder and JOB-16 AceDataReady gate are already in the design. |

### 05 Technical architecture/Recovery Workbench Document Management Design v3.docx (8)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-20386 |  | GAP-2078 |  | Section 2 and 9.3 record GET /cases/{caseId} of rwb-case: REST, one hop, 2 s timeout, fake, class C. |
| CDC-20387 |  | GAP-2079 |  | Section 7: hold recorded by rwb-case, checked before an expiry is proposed; retention_rule and retention_action stay in rwb_document. |
| CDC-20388 |  | GAP-2077 |  | Document is version 3; '1, 28 October 2026' shows in the Source version row and the change log. |
| CDC-20389 |  | GAP-2080 |  | Section 7: e-Discovery is served by GET /documents with case, type and date filters, returning metadata and version list. |
| CDC-20390 |  | GAP-2081 |  | Sections 3 and 9.6: type list and checklist sit in rwb_document (P5), read through P5, with no copy in another service. |
| CDC-20391 |  | GAP-2082 |  | Sections 1, 2 and 9.5: JOB-12 starts DocumentIntakeWorkflow every 15 minutes with KEDA workers on the intake queue. |
| CDC-20392 |  | GAP-2085 |  | Sections 1 and 2 name Azure Blob (WORM), claim-check and 2.8 TB by 2031; DL27 stays open. |
| CDC-20393 |  | GAP-2086 |  | Section 5: task raised through the rwb-case task contract, MSG-P5-004 on the case, custody row in rwb_document. |

### 09 Testing and quality/Recovery Workbench Definition of Ready and Done v4.docx (8)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-20404 |  | GAP-2145 |  | write failed: WRITE FAILED (nothing was written): N001-F6: old text found 0 time(s) in paragraphs, expected 1 |
| CDC-20405 |  | GAP-2144 |  | write failed: WRITE FAILED (nothing was written): N001-F6: old text found 0 time(s) in paragraphs, expected 1 |
| CDC-20406 |  | GAP-2143 |  | write failed: WRITE FAILED (nothing was written): N001-F6: old text found 0 time(s) in paragraphs, expected 1 |
| CDC-20407 |  | GAP-2118 |  | write failed: WRITE FAILED (nothing was written): N001-F6: old text found 0 time(s) in paragraphs, expected 1 |
| CDC-20408 |  | GAP-2119 |  | write failed: WRITE FAILED (nothing was written): N001-F6: old text found 0 time(s) in paragraphs, expected 1 |
| CDC-20409 |  | GAP-2141 |  | write failed: WRITE FAILED (nothing was written): N001-F6: old text found 0 time(s) in paragraphs, expected 1 |
| CDC-20410 |  | GAP-2146 |  | write failed: WRITE FAILED (nothing was written): N001-F6: old text found 0 time(s) in paragraphs, expected 1 |
| CDC-20411 |  | GAP-2147 |  | write failed: WRITE FAILED (nothing was written): N001-F6: old text found 0 time(s) in paragraphs, expected 1 |

### 04 User stories/Recovery Workbench Service Story Catalog v1.xlsx (6)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-20394 |  | GAP-0153 |  | Feature List v4 rows stay unchanged. The rwb-reporting read model and JOB-15 schedule apply at story stage, in the P9 and P1 story files. |
| CDC-20395 |  | GAP-3212 |  | Requirement-to-story assignment is for the next story pass (Service Story Files section 18; v7 traceability matrix flags orphans). The catalog has no requirement column. |
| CDC-20396 |  | GAP-1553 |  | Needs a business decision: raise a wave 4 story or retire REQ-WKM-010. A new catalog row would need an invented story ID and attributes. |
| CDC-20397 |  | GAP-2003 |  | INT-14 owner/executor split goes into the P6 and P2 contract story files (and Interface Specifications, row INT-14). |
| CDC-20398 |  | GAP-2004 |  | INT-25 owner/executor split goes into the S6 and P2 contract story files (and Interface Specifications, row INT-25). |
| CDC-20399 |  | GAP-3198 |  | First option taken: derived epic scope and owner stay in 04 User stories/Recovery Workbench Service Epics v1.md, which already records them. No new catalog columns. |

### 09 Testing and quality/Recovery Workbench Test Cases v8.xlsx (6)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-20424 |  | GAP-3153 |  | -ITG rows with own IDs exist, but some story files give them Component, Contract or NFR. Choosing Integration or End to end per row needs a QA decision. RTM part belongs in the RTM. |
| CDC-20425 |  | GAP-3219 |  | v8 keeps Level and has a Test level column on both case sheets; the C3-TC log records the mapping as an assumption. Cells not re-read. |
| CDC-20426 |  | GAP-3221 |  | Rule test cases has a Service column and no story key column; the C3-TC log records services from Architecture v5 slide 3. Cells not re-read. |
| CDC-20427 |  | GAP-3222 |  | Both case sheets of v8 have a Service column; the C3-TC log records it as filled from the Ownership Map. The Regression Suite is a separate document. |
| CDC-20428 |  | GAP-3223 |  | Per the C3-TC log and build script, the 20 cases are marked retired in Service. Status stays Live; no evidence read that replacement stories are tested. |
| CDC-20429 |  | GAP-3224 |  | C3-TC log records 987 -ITG rows added to v8. Having the Integration Test Plan count from the workbook belongs in that plan. Cells not re-read. |

### 05 Technical architecture/Recovery Workbench Technical Specifications by Module v6/Recovery Workbench TSD P2 Integration v4.md (6)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-20895 |  | GAP-1164 |  | INT-14 record layout and claim-check store belong to the P6 outbound file story (B-P6-04). The P2 table rows are unchanged here. |
| CDC-20896 |  | GAP-0739 |  | Case-side outbound outcome seam belongs to the P3 story files (RWB-P3-E1007-APP). Not a change to this document. |
| CDC-20897 |  | GAP-0808 |  | Bank IAM removal request path, shape and failure contract are not in the source documents. Not written here; no value invented. |
| CDC-20898 |  | GAP-0657 |  | Item text not re-read in this run, so no fix was written. Not verified against this document. |
| CDC-20900 |  | GAP-1074 |  | Item text not re-read in this run, so no fix was written. Not verified against this document. |
| CDC-20902 |  | GAP-0651 |  | Item text not re-read in this run, so no fix was written. Not verified against this document. |

### 05 Technical architecture/Recovery Workbench Event and Messaging Design v5.xlsx (5)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-20367 |  | GAP-0030 |  | Events v5 EV-18 and Realignment change 7: TimerDue retired, no event type and no topic. |
| CDC-20368 |  | GAP-0038 |  | EV-08 owner P7 on rwb.decision-record.v1; 'Decision record' rule has local records and the central ledger. |
| CDC-20369 |  | GAP-0039 |  | EV-18 owner PLT, retired; Realignment change 7 states a durable Temporal timer. |
| CDC-20370 |  | GAP-0040 |  | EV-21 published by rwb-partner (S9); Realignment change 8. |
| CDC-20371 |  | GAP-0041 |  | EV-26 published by rwb-source-data (P1); Realignment change 9. |

### 09 Testing and quality/Recovery Workbench Test Data Plan v4.docx (5)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-20445 |  | GAP-2135 |  | write failed: WRITE FAILED (nothing was written): N001-F7: paragraph found 0 time(s), expected 1 |
| CDC-20446 |  | GAP-3220 |  | write failed: WRITE FAILED (nothing was written): N001-F7: paragraph found 0 time(s), expected 1 |
| CDC-20447 |  | GAP-2138 |  | write failed: WRITE FAILED (nothing was written): N001-F7: paragraph found 0 time(s), expected 1 |
| CDC-20448 |  | GAP-2139 |  | write failed: WRITE FAILED (nothing was written): N001-F7: paragraph found 0 time(s), expected 1 |
| CDC-20449 |  | GAP-3226 |  | write failed: WRITE FAILED (nothing was written): N001-F7: paragraph found 0 time(s), expected 1 |

### 22 Microservice Realignment/Recovery Workbench Microservice Ownership Map v1.xlsx (4)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-20372 |  | GAP-0204 |  | Conflicts with GAP-0132/GAP-1995: staged Tables sheet already gives S1 the valuation table. 'S1 owns no entity' not written; needs reconciling in the Gap Register. |
| CDC-20373 |  | GAP-0286 |  | No repository names or source-control group found in the item or searches; adding them would invent values. Provisioning is a DevOps action. |
| CDC-20374 |  | GAP-0289 |  | Staged Tables sheet already has valuation (owner S1, rwb_valuation). The rwb_valuation.sql change belongs to the Physical Schema. |
| CDC-20375 |  | GAP-1995 |  | valuation (S1) already staged; valuation_ext stays P1. Route decision table has no name in TSD S1 T3.1; the staged GAP-0132 ruling records this. |

### 11 Delivery and operations/Recovery Workbench Resource Plan and Team Structure v3.xlsx (4)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-20400 |  | GAP-0323 |  | DevOps row records 0 FTE and no row, with a gap reference. Adding FTE or assigning pipeline work to TechX remains an IT lead decision. |
| CDC-20401 |  | GAP-0319 |  | Read me holds the R8.1 header, tool line, and change log with the v2 row marked as not stated in the source workbook. |
| CDC-20402 |  | GAP-0325 |  | Team types and resources QA row: served by the QA engineers of both squads, with the W1J01 harness and NFR stories against it. |
| CDC-20403 |  | GAP-0326 |  | Team types and resources TechX row reads Recovery squad 1 and 2 as TechX and keeps both names. |

### 05 Technical architecture/Recovery Workbench Interface Specifications v4.xlsx (4)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-20412 |  | GAP-2000 |  | Needs a business decision: REST/file interface or second Kafka consumer, and who serves COLLINS model learning. The resolution recommends neither, so no new interface ID is added. |
| CDC-20413 |  | GAP-2112 |  | INT-06 and its Data product column are in System Disposition and Integration Inventory v3, sheet Interfaces. This workbook has neither. |
| CDC-20414 |  | GAP-0082 |  | INT-08 is kept: ACE ingestion read through v_ace_score, owner ACE team, owning service P1 rwb-source-data. The register names an owner, so no placeholder is needed. |
| CDC-20415 |  | GAP-2007 |  | PARTLY: Key repointed to v9. Field mapping row 2 still says 'LDM v7' (title cell, no fix format reaches it; change to v9 by hand). DF-* IDs not checked in v9. |

### 09 Testing and quality/Recovery Workbench Integration Test Plan v1.docx (4)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-20418 |  | GAP-2151 |  | Version 1, 22 November 2026, Supersedes 'None (first version)', and the section 18 row states no earlier version exists. |
| CDC-20419 |  | GAP-2152 |  | Section 11 wave gates use the SIT exit wording (all journey cases pass, no open severity 1 or 2) and invent no pass rate. |
| CDC-20420 |  | GAP-2153 |  | Section 11 fixes one cycle per wave closing the gate before the first release date, with no further window; dates stay tentative. |
| CDC-20421 |  | GAP-2157 |  | Section 9 reads integration evidence as the two RWB-ITG-NFR stories, NFT-J rows and journey NFR cases; the rest stays with the NFT plan. |

### 22 Microservice Realignment/Recovery Workbench Microservice Change Register v1.md (4)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-20431 |  | GAP-0171 |  | Needs a business decision: run CTL-36 from wave 3 on S9 contract and fake, or move its first release to E6. The resolution picks neither, so no ruling is recorded. |
| CDC-20432 |  | GAP-1861 |  | Functional Specifications by Module, next FSD baseline. This register already shows RWB-E1-014 as retired. |
| CDC-20433 |  | GAP-1862 |  | Functional Specifications by Module, next FSD baseline. This register already shows RWB-TE-007 as retired. |
| CDC-20434 |  | GAP-3165 |  | RWB-E1-014 row already reads Retired (D-RCV-60), new stories None, with the reason that Arch v5 has no data lake. |

### 03 Requirements and specifications/Recovery Workbench Business Requirements Program v5.md (4)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-20435 |  | GAP-3262 |  | Needs a business decision: write requirements or rule 18.1 and 18.2 out of scope. Section 4 puts process 18 in the Workbench, and the item does not pick an option. |
| CDC-20436 |  | GAP-3263 |  | Needs a business decision: write requirements or rule 14.3 out of scope. REG-04 traces to 14.3, and the item does not pick an option. |
| CDC-20437 |  | GAP-1496 |  | Sections 10.5, 10.6 and 11 keep the IDs under P7, deliver the ledger under RWB-SVC-P1 and note the split. |
| CDC-20438 |  | GAP-1497 |  | Sections 10.5 and 10.6 state P7 delivers approvals against P4's authority table. The API contract part belongs in that contract, not checked. |

### 04 User stories/Recovery Workbench How To Read The Acceptance Criteria v2.docx (4)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-20439 |  | GAP-3201 |  | v2 has the metadata table dated 22 November 2026 and a change log; version 1 is recorded as having no date in the source. |
| CDC-20440 |  | GAP-3202 |  | How the set is sliced and Reading the slices of one legacy story are in v2; the existing sections are kept. |
| CDC-20441 |  | GAP-3203 |  | The four new sections are in English and Where to read more states the Thai gap. Thai wording awaits the message standard owner. |
| CDC-20442 |  | GAP-3204 |  | How the set is sliced holds the key part table and the work type table with suggested owner phrases. |

### 09 Testing and quality/Recovery Workbench Non Functional Test Plan v3.docx (4)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-20450 |  | GAP-2125 |  | Section 5 states the NFT ID convention; sections 6 to 8 hold the rows. Checked in the v3 round-trip .md copy, not the .docx (no shell to run docview). |
| CDC-20451 |  | GAP-2124 |  | Version 3, 22 November 2026, Supersedes row (v2, 28 October 2026) and change-log row noting the stated Version 1 are there. Checked in the round-trip .md copy. |
| CDC-20452 |  | GAP-2126 |  | Section 2 keeps 410 as the test load and lists 370, 50, 48 and about 420 with their sources. Checked in the round-trip .md copy. |
| CDC-20453 |  | GAP-2128 |  | Section 5 reads E1 to E8 as EP01 to EP08; section 9 orders waves from the Ownership Map. Checked in the round-trip .md copy. |

### 11 Delivery and operations/Recovery Workbench Story Build Order v4.docx (4)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-20461 |  | GAP-3238 |  | Change-log table exists with the v3 source row and v4 row (D-RCV-60, tool line). No v1/v2 source history was supplied, so no rows are added for them. |
| CDC-20462 |  | GAP-3242 |  | How to use it keeps the v3 board limit and marks the team-type limit as not specified (CG-C4-SBO-6). No programme limit is given to record. |
| CDC-20463 |  | GAP-3243 |  | Epic release statement kept and marked tentative (CG-C4-SBO-7). The item gives no agreed release calendar or per-window release date to add. |
| CDC-20464 |  | GAP-3245 |  | How this version is read keeps Waits on word for word and reads realigned waits from Ready to start and lane (CG-C4-SBO-9). |

### 09 Testing and quality/Recovery Workbench Requirements Traceability Matrix v7.xlsx (3)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-20456 |  | GAP-3210 |  | v7 RTM has the realigned Owner column and keeps the v6 Module column; the Coverage sheet records the 14 differences. |
| CDC-20457 |  | GAP-3214 |  | v7 Legacy keys cells read 'None - no legacy key in the v6 matrix'; Coverage records the 97 requirements with no v6 story. |
| CDC-20458 |  | GAP-3215 |  | v7 Coverage sheet keeps the v6 block as history and has the D-RCV-60 realignment block below it. |

### 11 Delivery and operations/Recovery Workbench Run Operating Model v3.pptx (3)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-20465 |  | GAP-0312 |  | Slides 15-16 keep rota and tier roles as 'Not specified'. No source gives rota or tier 1 hand-off point; needs a DevOps decision. Also, docwriter.py has no .pptx writer. |
| CDC-20466 |  | GAP-0313 |  | Slide 19 has a change log with a v2 row. No v1 row; its date and content are not given, and file properties/release record were not checked. No .pptx writer. |
| CDC-20467 |  | GAP-0314 |  | Slides 10-13 give a run book row per service. Missing: keep beside contract story, review at start of service's wave. Add by hand to slide 8; no .pptx writer. |

### 05 Technical architecture/Recovery Workbench System Disposition and Integration Inventory v4.xlsx (2)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-20416 |  | GAP-2108 |  | By route counts are calculated in v4 (20 In, 12 Out, 4 Both, 36 Total). Route vocabulary confirmation stays for the owner's next review. |
| CDC-20417 |  | GAP-2113 |  | Needs a decision between S4 and S9 for INT-33, and a standard from the partner gateway contract; the resolution gives neither. |

### 08 AI and agents/Recovery Workbench Agent Catalog and Specifications v3.xlsx (2)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-20422 |  | GAP-0086 |  | Agents v3 holds the owning service and P10 runtime host for all 12 agents. Tagging agent stories and contract dependencies belongs in the story files. |
| CDC-20423 |  | GAP-0089 |  | v3 Read me carries Status Draft and the D-RCV-60 change-log row, with no approval claimed (per build script and edit log). |

### 05 Technical architecture/Recovery Workbench Availability Performance and Recovery Design v3.docx (2)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-20443 |  | GAP-2059 |  | Section 3 bullet 2 already names the rwb-reporting read model, not the 19 live schemas, no data lake (ADR-018, DP-17). Checked in the roundtrip .md extract. |
| CDC-20444 |  | GAP-2057 |  | Version is 3; the 'Source version' row keeps both 2 (file name) and 1 (source table). Change log has 3 plus a source row 2. Checked in the roundtrip .md extract. |

### 05 Technical architecture/Recovery Workbench ACE Architecture Decision v4.docx (2)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-20459 |  | GAP-1981 |  | Sections 3.2, 3.4 and 6 already state the shared cluster, Schedules, repository and pipeline per service, shared release train and flags. |
| CDC-20460 |  | GAP-1982 |  | Needs a squad assignment per service for Waves 1 to 4; no source gives it. Section 6 already says the number of squads is not restated. |

### 01 Decisions and governance/Recovery Workbench Decision Log v11.xlsx (2)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-20468 |  | GAP-0298 |  | Needs a Solution architect choice: S4 creation moves to Wave 2, or E2 notice approval moves to E5. No choice found in the sources searched; then record it against DL44 and DL48. |
| CDC-20469 |  | GAP-0023 |  | The v11 extract already uses D-RCV-60: Read me states it and Decisions taken holds the D-RCV-60 row. |

### 11 Delivery and operations/Recovery Workbench Risks Assumptions Issues and Dependencies v5.xlsx (2)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-20470 |  | GAP-0317 |  | R-19 to R-27, Read me mapping and Risks cover row seen in the v5 check render, not the workbook itself (no shell). |
| CDC-20471 |  | GAP-0318 |  | Read me note 2 and bracketed service codes in Owner cells seen in the v5 check render and fix_book.py; workbook not read directly. |

### 05 Technical architecture/Recovery Workbench Target Architecture v7.pptx (2)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-20476 |  | GAP-1987 |  | v7 text extract keeps the 'What each epic adds' slide and states each service's wave is the Ownership Map's, which governs over v6 slide 15. .pptx not opened. |
| CDC-20477 |  | GAP-1997 |  | Correction is for the Architecture v5 pack; published per-service OpenAPI files are the contract. No cited paths found in v7 text extract. .pptx not opened. |

### 11 Delivery and operations/Recovery Workbench Cutover and Go Live Plan v4.docx (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-20430 |  | GAP-0299 |  | v4 metadata reads Version 4, matching the file name; the v3 lag is recorded in section 12 (CG-B-DELIVDOC-46-1). |

### 08 AI and agents/Recovery Workbench Model Integration Design v3.docx (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-20454 |  | GAP-0079 |  | Version row reads 3, the 28 October 2026 date is kept, and the title block notes it is the version 2 text date. |

### 05 Technical architecture/Recovery Workbench Temporal Workflow and Activity Catalog v1.xlsx (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-20455 |  | GAP-0145 |  | Needs names, inputs, outputs and re-run behaviour the item does not give. Some story files use differing names, so an architect must choose. |

### 05 Technical architecture/Recovery Workbench Kafka Topic and Event Catalog v1.xlsx (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-20472 |  | GAP-0097 |  | ReportPublished, GuaranteeClaimFiled, GuaranteeClaimSettled and TreatmentClosed already have topics on sheets Topics and Events. |

### 03 Requirements and specifications/Recovery Workbench Functional Specifications by Module v7/Recovery Workbench FSD P3 Case and workflow v5.md (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-20473 |  | GAP-1551 |  | v5 file already states Document ID P3-RWB-FSD-v5 and Version 5, matching the file name. |

### 03 Requirements and specifications/PRD/Recovery Workbench PRD P9 rwb-reporting v1.md (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-20474 |  | GAP-1645 |  | Sections 1.5 and 6 already trace to FSD feature and AC IDs. Some FR rows cite only Arch, job, NFR or BR sources; none added. Adding REQ IDs would be an FSD P9 change. |

### 05 Technical architecture/Recovery Workbench Service Contract Catalog v1.md (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-20475 |  | GAP-0099 |  | Document is version 1, status Draft, and its change log starts with the D-RCV-60 row; section 11 records the point. |

### 11 Delivery and operations/Recovery Workbench Build Sequence Epic 1 and Epic 2 v7.xlsx (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-20478 |  | GAP-3231 |  | Per v7 build script and edit log: Module (v6) kept, sheet 'By service and lane' reports the load, and the 'By module' note points to it. Workbook cells not read directly. |

### 06 Data/Recovery Workbench Physical Schema v7/rwb_source_data.sql (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-20479 |  | GAP-0188 |  | contact_point_ext already has consent_given (boolean) and consent_at (DF-EXT-015/016). The Data Protection Design v2 s.3 citation and P1 stories can use these names. |

### 06 Data/Recovery Workbench Data Classification and Personal Data Inventory v5.xlsx (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-20480 |  | GAP-0266 |  | v5 has the Fields and Identifiers rule columns, six new Handling rows and PII controls with owners. Checked in the cached v5 text; docview was not run (no shell). |

### 05 Technical architecture/Recovery Workbench Information Flow v6.pptx (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-20481 |  | GAP-2100 |  | No .pptx fix op or writer. Edit slides 13 and 22 by hand: 'O05 is out of scope until the model owner confirms COLLINS needs it after wave 1'. Checked v6 build text only. |

### 10 Policy, controls and compliance/Recovery Workbench Regulatory Requirements Map v3.xlsx (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-20482 |  | GAP-3254 |  | No obligation-to-requirement-ID mapping found in sources searched; assigning IDs needs Business analyst judgement. v3 workbook not opened (no shell); checked via BRD v6 section 13 copy. |

### 10 Policy, controls and compliance/Recovery Workbench Audit Findings Response Map v2.xlsx (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-20483 |  | GAP-3256 |  | No finding-to-requirement mapping found in sources searched; BA must decide it. Findings sheet has no requirement ID column, and the fix formats cannot add one. |

### 05 Technical architecture/Recovery Workbench Audit and Logging Design v3.docx (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-20484 |  | GAP-2071 |  | Checked in the v3 build-source .md, not the .docx (no shell): sections 1, 4, 8 cover lake removal, JOB-13/14, WORM seal, RWB-E1-014. Batch design job text belongs to that document. |

### 06 Data/Recovery Workbench Physical Schema v7/README.md (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-20485 |  | GAP-2140 |  | README sections 2 and 6 and the SQL already place 4 objects in all 19 schemas, 2 flag tables in rwb_integration. Seed treatment belongs in the test data plan. |

### 04 User stories/Recovery Workbench Acceptance Criteria Glossary v2.xlsx (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-20486 |  | GAP-3150 |  | No confirmed Thai wording is available, so adding it would mean inventing it. English stays authoritative meanwhile. v2 placeholders not checked: no shell tool to run docview. |

### 09 Testing and quality/Recovery Workbench Regression Suite v7.xlsx (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-20487 |  | GAP-3225 |  | v7 build script (C3-TC/build.py:390) writes this into Read me, row 'Growth'; Growth rows unchanged. Workbook not opened: no shell to run docview. |

## 6. Register gaps linked to this service (Gap Register v2 status)

| GAP ID | Title | Owner role | Status |
|---|---|---|---|
| GAP-0005 | Route numbering R4 and R5 conflict | Business analyst | Resolved (directive) |
| GAP-0008 | JOB-16 write-off scan trigger | Platform team and S7 owner | Accepted (directive); resolution in progress |
| GAP-0009 | Airflow role and ownership undecided | Enterprise Architecture and bank platform team | Resolved (directive) |
| GAP-0010 | BOT approval route under FPG 19/2560 clause 5.5 | Compliance and IT risk | Open (business decision) |
| GAP-0018 | Platform task queue rwb-platform is not one of the 19 services | Platform team | Resolved (directive) |
| GAP-0019 | The canonical context files remain at v2 | Context Builder and Context Updater | Accepted (directive); resolution in progress |
| GAP-0020 | Regulatory source dates and coverage | Compliance | Open (business decision) |
| GAP-0023 | Decision ID D-RCV-53 already used | Delivery lead | Accepted (directive); resolution in progress |
| GAP-0024 | Interaction ledger endpoint ownership | Solution architect | Resolved (directive) |
| GAP-0025 | Feature flag endpoint ownership | Solution architect | Resolved (directive) |
| GAP-0026 | Rule package registry endpoint ownership | Solution architect | Resolved (directive) |
| GAP-0027 | Reference data endpoint ownership | Solution architect | Resolved (directive) |
| GAP-0028 | Platform smoke endpoint ownership | Solution architect | Resolved (directive) |
| GAP-0029 | Asset valuation endpoint ownership | Solution architect | Resolved (directive) |
| GAP-0030 | TimerDue event retired but still listed with an owner | Solution architect | Accepted (directive); resolution in progress |
| GAP-0031 | COLLINS load check job retired but still in the job list | Solution architect | Accepted (directive); resolution in progress |
| GAP-0032 | Timer check job has no single owner and is retired | Solution architect | Resolved (directive) |
| GAP-0033 | File load job retired but still in the job list | Solution architect | Accepted (directive); resolution in progress |
| GAP-0034 | WIN notice job names two owners | Solution architect | Accepted (directive); resolution in progress |
| GAP-0035 | Outbox sender runs in every service | Solution architect | Resolved (directive) |
| GAP-0036 | Decision log copy to the data lake disagrees with Arch v5 | Solution architect | Resolved (directive) |
| GAP-0037 | Reporting extract to the data lake disagrees with Arch v5 | Solution architect | Resolved (directive) |
| GAP-0038 | DecisionRecorded producer is 'all 19' but the event type and ledger have one owner | Solution architect | Accepted (directive); resolution in progress |
| GAP-0039 | TimerDue producer is a durable timer, not a rwb-case event | Solution architect | Accepted (directive); resolution in progress |
| GAP-0040 | PartnerResultSubmitted direction and owner | Solution architect | Accepted (directive); resolution in progress |
| GAP-0041 | AceDataReady direction and owner | Solution architect | Accepted (directive); resolution in progress |
| GAP-0042 | Timer check retired, but the decision log keeps Quartz and the TimerScheduler | Solution architect | Resolved (directive) |
| GAP-0043 | WIN notices have two owners in the job map | Solution architect | Accepted (directive); resolution in progress |
| GAP-0044 | Decision log copy: continuous Kafka ingest versus the nightly data-lake job | Solution architect | Accepted (directive); resolution in progress |
| GAP-0045 | Reporting extract: Airflow trigger versus the 01:30 Schedule and the data lake | Solution architect | Accepted (directive); resolution in progress |
| GAP-0046 | Write-off scan: Temporal Schedule versus the ACE batch trigger and Quartz | Solution architect | Accepted (directive); resolution in progress |
| GAP-0047 | Interaction ledger owner | Solution architect | Resolved (directive) |
| GAP-0048 | Case list row owner | Solution architect | Resolved (directive) |
| GAP-0049 | Rule registry owner | Solution architect | Resolved (directive) |
| GAP-0050 | DoA table owner | Solution architect | Resolved (directive) |
| GAP-0051 | List of values owner | Solution architect | Resolved (directive) |
| GAP-0052 | Partner user owner | Solution architect | Resolved (directive) |
| GAP-0053 | Feature flag owner | Solution architect | Resolved (directive) |
| GAP-0054 | Outbox, inbox and idempotency table owner | Solution architect | Resolved (directive) |
| GAP-0055 | Job catalogue owner | Solution architect | Resolved (directive) |
| GAP-0056 | Retention rule owner | Solution architect | Resolved (directive) |
| GAP-0057 | Signature request owner | Solution architect | Resolved (directive) |
| GAP-0058 | Timer table versus durable timers | Solution architect | Resolved (directive) |
| GAP-0059 | Data lake watermark owner | Solution architect | Resolved (directive) |
| GAP-0060 | DP04 copy owner | Solution architect | Resolved (directive) |
| GAP-0061 | Writer of the appraisal extension | Solution architect | Resolved (directive) |
| GAP-0069 | The autonomy levels let an agent act, while the architecture says AI only suggests and a person approves | Solution architect | Resolved (directive) |
| GAP-0070 | The model endpoint of DL33 is 'a private endpoint in the SCB tenant'; Architecture v5 names INT-23 and no approval path | Enterprise AI team and solution architect | Resolved (directive) |
| GAP-0071 | Nine of the twelve agents have no service row that starts the run | Solution architect | Resolved (directive) |
| GAP-0074 | The rule result used on a fallback is named for two agents only | P7 rwb-decision | Resolved (directive) |
| GAP-0075 | Who may change a prompt or a policy: the centre of excellence owns them, the admin endpoints are P10's | Center of excellence and P10 rwb-agent | Resolved (directive) |
| GAP-0076 | The 60 seconds: the whole run or the model call | P10 rwb-agent | Resolved (directive) |
| GAP-0077 | The model output is 'read from the daily load', but only rwb-source-data may read ACE data | P1 rwb-source-data | Resolved (directive) |
| GAP-0079 | Internal Version row says 1 while the file family is at version 2 | Architecture | Accepted (directive); resolution in progress |
| GAP-0082 | INT-08 is not carried in Architecture v5 or the interface set | Architecture | Accepted (directive); resolution in progress |
| GAP-0084 | The monitoring rows name governance roles only, with no service owner for the data | Model Risk | Open (business decision) |
| GAP-0085 | D5.1 and D5.2 are not defined and no owning service is assigned | TechX | Resolved (directive) |
| GAP-0086 | No owning service per agent in the agent catalog | Solution architect with the agent platform owner | Accepted (directive); resolution in progress |
| GAP-0087 | Owning service of the Valuation agent is not named | Solution architect with the valuation and route module owner | Resolved (directive) |
| GAP-0088 | Owning service of the Tracing agent is not named | Solution architect with the partner management owner | Resolved (directive) |
| GAP-0089 | Agent catalog v2 records no status or approval | Document owner with the strategy and model committee secretariat | Accepted (directive); resolution in progress |
| GAP-0090 | D-RCV-36 T1 and T2 text is not in the source documents read for this work package | Solution architect | Resolved (directive) |
| GAP-0091 | Three Temporal release positions disagree: 1.28.1 in ADR-011, 1.29.7 in the design stack note, 1.30+ required for Nexus and Worker Versioning | Platform team | Resolved (directive) |
| GAP-0092 | The Kafka platform for Recovery business events is not confirmed by Enterprise Architecture and the ACE platform team | Enterprise Architecture | Resolved (directive) |
| GAP-0095 | PLT owns five v4 operations but the split has no PLT service document | Solution architect | Resolved (directive) |
| GAP-0096 | Event payload property types, formats and required flags are not specified in any source | Solution architect | Resolved (directive) |
| GAP-0097 | No event is catalogued for rwb-reporting, and two catalogue rows give no topic | Solution architect | Accepted (directive); resolution in progress |
| GAP-0098 | Seven component schemas of API Specification v4 are referenced by no operation | TechX | Resolved (directive) |
| GAP-0099 | No earlier Service Contract Catalog exists | Delivery lead | Accepted (directive); resolution in progress |
| GAP-0101 | Activity contract jar coordinates are not specified | Tech lead | Resolved (directive) |
| GAP-0102 | Consumers of two events are not named | Solution architect | Accepted (directive); resolution in progress |
| GAP-0103 | Schema registry product is not specified | Platform architect | Accepted (directive); resolution in progress |
| GAP-0104 | Route-services-through-Temporal rule meets REST cells to rwb-source-data | Solution architect | Resolved (directive) |
| GAP-0105 | Enterprise AI endpoint contract is not specified | Solution architect | Accepted (directive); resolution in progress |
| GAP-0106 | Matrix cell S5 to P6 has no named interface | Solution architect | Accepted (directive); resolution in progress |
| GAP-0117 | Owner labels in the Decision Log name individuals, not roles | Programme governance | Open (business decision) |
| GAP-0119 | The version date in the Decision Log header is earlier than its last decision | Programme governance | Open (business decision) |
| GAP-0120 | EV-18 TimerDue changes direction and owner between Event and Messaging Design v4 and Architecture v5 | Solution architect | Accepted (directive); resolution in progress |
| GAP-0121 | EV-21 PartnerResultSubmitted is consumed in v4 and published by rwb-partner in Architecture v5 | Solution architect | Accepted (directive); resolution in progress |
| GAP-0122 | EV-26 AceDataReady is consumed in v4 and published by rwb-source-data in Architecture v5 | Solution architect | Accepted (directive); resolution in progress |
| GAP-0126 | The v4 failure rule sends a failed event to an exception queue, the target sends it to a dead-letter topic | Solution architect | Accepted (directive); resolution in progress |
| GAP-0127 | The 15 event types named only in the Architecture v5 service catalogue have no payload | Solution architect | Resolved (directive) |
| GAP-0128 | No consumer is given for ApprovalDecided, ReportPublished or LawsuitFiled | Solution architect | Accepted (directive); resolution in progress |
| GAP-0131 | The idempotency key of an event is required but its derivation is not stated | Solution architect | Accepted (directive); resolution in progress |
| GAP-0132 | The Ownership Map v1 has no table for rwb-valuation although Architecture v5 names valuations, the D6 route decision and the route agent output | Solution architect | Resolved (directive) |
| GAP-0133 | The Ownership Map v1 holds only proceeds for rwb-payment although Architecture v5 names fees, bookings and posting files | Solution architect | Resolved (directive) |
| GAP-0134 | The stack versions of the service template are not pinned in any source read for this work package | Platform team | Accepted (directive); not applied: value not in the source documents |
| GAP-0135 | The repository name and location for a service are not fixed by any source | Platform team | Accepted (directive); resolution in progress |
| GAP-0136 | The Helm chart name, the release naming and the container registry are not fixed | Platform team | Accepted (directive); resolution in progress |
| GAP-0137 | The event catalogue does not name the consumers of ApprovalDecided or ReportPublished | Solution architect | Accepted (directive); resolution in progress |
| GAP-0138 | Architecture v5 names a decision_record table in every service schema; the Ownership Map v1 has no row for it | Solution architect | Resolved (directive) |
| GAP-0139 | The pipeline tool and its stage names are not fixed by any source | DevOps team | Accepted (directive); resolution in progress |
| GAP-0140 | No earlier Service Catalog or Service Template Specification exists in the document set | Delivery lead | Accepted (directive); resolution in progress |
| GAP-0142 | Temporal Schedule identifiers, calendars and overlap values are not defined | Platform team | Accepted (directive); not applied: value not in the source documents |
| GAP-0143 | Activity timeouts, heartbeat intervals and task-queue limits are not specified | Solution architect | Resolved (directive) |
| GAP-0144 | The event-started payment workflow of JOB-07 and JOB-08 has no name | Solution architect | Resolved (directive) |
| GAP-0145 | The work started by six Schedules and three workflows is not named | Solution architect | Accepted (directive); not applied: value not in the source documents |
| GAP-0146 | DailyCaseRun is described both as a Schedule and as an event-started workflow | Solution architect | Accepted (directive); resolution in progress |
| GAP-0147 | The rwb-platform task queue has no service definition | Platform team | Accepted (directive); resolution in progress |
| GAP-0148 | The case workflow ID is written two ways | Solution architect | Accepted (directive); resolution in progress |
| GAP-0149 | The Feature List keys every feature on one of 19 modules, and 13 of the module names differ from the Arch v5 service names | Business architect and the platform solution architect | Accepted (directive); resolution in progress |
| GAP-0151 | Ten interaction-ledger features are listed in module P7 while the Ownership Map and DP-18 place the ledger with P1 rwb-source-data | Solution architect of P1 rwb-source-data and of P7 rwb-decision | Resolved (directive) |
| GAP-0153 | Seven live features name the Data lake and Power BI as their systems, and INT-19 and INT-20 are removed | Reporting lead of P9 rwb-reporting and the solution architect of P1 rwb-source-data | Accepted (directive); resolution in progress |
| GAP-0155 | The workbook carries no wave column, and for 141 of the 378 features the service wave and the business-epic wave differ | Programme planner and the platform solution architect | Accepted (directive); resolution in progress |
| GAP-0156 | Two features govern feature flags in module P3 while the default ruling puts the flag store in the platform library | Platform library lead and the solution architect of P3 rwb-case | Accepted (directive); resolution in progress |
| GAP-0157 | No rwb-valuation table in the Ownership Map for the route decision | Architecture owner | Accepted (directive); resolution in progress |
| GAP-0158 | CCMS collateral has no target service in the Ownership Map | Architecture owner | Accepted (directive); resolution in progress |
| GAP-0167 | The Counts tab is blank and the release column holds values that are not releases | Security administrator | Accepted (directive); resolution in progress |
| GAP-0169 | No approval and no status is recorded for the document | Application owner | Accepted (directive); resolution in progress |
| GAP-0170 | Control owner service is not stated in the controls catalog | Control owner; service owner | Accepted (directive); resolution in progress |
| GAP-0171 | CTL-36 first runs in E5 while its owner service rwb-partner is wave 4 | Programme delivery lead | Accepted (directive); not applied: value not in the source documents |
| GAP-0172 | Five controls check work that two services own | Control owner | Accepted (directive); resolution in progress |
| GAP-0173 | The conduct sample control has no owner in the Ownership Map | Control owner; conduct and QA | Resolved (directive) |
| GAP-0174 | Control rows still name monolith components and monolith messages | Control owner | Accepted (directive); resolution in progress |
| GAP-0175 | No approval of version 4 is recorded | Programme governance | Open (business decision) |
| GAP-0176 | No calendar release date is stated for any control | Programme delivery lead | Accepted (directive); resolution in progress |
| GAP-0177 | The metadata table reads version 1 while the file name reads v2 | Compliance | Open (business decision) |
| GAP-0178 | The decision log archive rule keeps a copy in the data lake | Compliance with P7 rwb-decision | Open (business decision) |
| GAP-0179 | Scores (DP11) have no owning schema and no table | Data owner with P1 rwb-source-data | Resolved (directive) |
| GAP-0180 | No retention period for tables that carry no data-product row | Compliance | Open (business decision) |
| GAP-0181 | A legal hold on a party or a document has no field in the target | Legal counsel with P3 rwb-case and P5 rwb-document | Open (business decision) |
| GAP-0182 | No operation or event lets the retention job act on another service's schema | Solution architect with P5 rwb-document | Resolved (directive) |
| GAP-0183 | The access-log period refers to a bank standard that is not in the run sources | Compliance with P4 rwb-access | Open (business decision) |
| GAP-0184 | The retention class LAKE_COPY has no target without the data lake | P5 rwb-document | Accepted (directive); resolution in progress |
| GAP-0185 | No source maps a data product to a service schema | Data architect | Accepted (directive); resolution in progress |
| GAP-0186 | Version 2 document stamps itself Version 1 | Compliance | Open (business decision) |
| GAP-0187 | No service owner for any personal data category or control | Data owner | Accepted (directive); resolution in progress |
| GAP-0188 | Consent state table and column name in the target schema | Data owner | Accepted (directive); resolution in progress |
| GAP-0189 | Version 2 records no approval or document status | Compliance | Open (business decision) |
| GAP-0190 | Debt sale tape masking check has no owner and no field list | Data owner | Resolved (directive) |
| GAP-0191 | PII read log has no event contract | Security operations | Accepted (directive); resolution in progress |
| GAP-0192 | Data subject access retrieval across 19 services | Compliance | Open (business decision) |
| GAP-0193 | Tokenization point and token format are not stated | Data owner | Resolved (directive) |
| GAP-0194 | The source workbook states no version date and records no approval | Programme governance | Open (business decision) |
| GAP-0195 | The obligations map names no service owner | Compliance; service owner | Open (business decision) |
| GAP-0196 | The reporting and outbound leg of REG-15 and REG-27 is covered by no control | Reporting and BI analyst; Compliance | Open (business decision) |
| GAP-0197 | The personal data breach notification of REG-25 has no owning service | Compliance and PDPA officer | Open (business decision) |
| GAP-0198 | The map and the Controls Catalog disagree on which controls answer four obligations | Compliance; data steward | Open (business decision) |
| GAP-0199 | Two obligations rest on the conduct sample whose owner service is itself an assumption | Compliance; conduct and QA | Open (business decision) |
| GAP-0200 | An obligation states no release, wave or date | Programme delivery lead | Accepted (directive); resolution in progress |
| GAP-0201 | The Owner column and the new Owner service column can be read as one owner | Compliance; programme governance | Open (business decision) |
| GAP-0204 | No entity is owned by S1 rwb-valuation, although Architecture v5 gives S1 the valuations and the route decision | Solution architect | Accepted (directive); not applied: value not in the source documents |
| GAP-0207 | The four platform library tables have schema 'platform' in the map but are created in every service schema | Data architecture team | Accepted (directive); resolution in progress |
| GAP-0208 | Feature flags are 'Workbench' as system of record in the model but owned by the platform library | Solution architect | Accepted (directive); resolution in progress |
| GAP-0209 | The Key sheet has no term for the five realignment concepts the new columns use | Data architecture team | Accepted (directive); resolution in progress |
| GAP-0261 | lake_copy_watermark is still an entity of the inventory although the data lake is removed | Data architecture team | Accepted (directive); resolution in progress |
| GAP-0266 | The inventory has no rule for events, workflow inputs or logs | Solution architecture team | Accepted (directive); resolution in progress |
| GAP-0284 | Version 5 states one ACE service, one repository, one recovery module and one schema, which Architecture v5 replaces with 19 services | Solution architect | Accepted (directive); resolution in progress |
| GAP-0286 | No source names the 19 service repositories, their source-control group or the way an empty repository is provisioned | DevOps team | Accepted (directive); not applied: value not in the source documents |
| GAP-0287 | The four DEV and two SIT deployment slots of version 5 are not stated per service now that there are 19 services with an api and a worker each | SCB IT infrastructure | Accepted (directive); not applied: value not in the source documents |
| GAP-0288 | No source states who approves a published contract version or where the contract artefact is held for its consumers | Solution architect | Resolved (directive) |
| GAP-0289 | The Ownership Map v1 gives rwb-valuation no table, so its schema and its first migration have no listed content | ACE DB team | Accepted (directive); resolution in progress |
| GAP-0290 | No approval of version 6 is recorded and the source carries no Status row | Programme governance | Open (business decision) |
| GAP-0291 | The source carries no change log and no tool line | Business analyst | Accepted (directive); resolution in progress |
| GAP-0292 | Version 4 has no delivery wave, and Architecture v5 puts Epics 2 and 3 in one wave while the plan gives each epic its own monthly release | Delivery lead | Resolved (directive) |
| GAP-0293 | The plan has no Wave 0 row and no platform release, so nothing states when the platform enablers are complete | Delivery lead | Resolved (directive) |
| GAP-0294 | No source states who approves a published contract or that a release gate covers contract publication | Solution architect | Resolved (directive) |
| GAP-0295 | The Features and Stories counts, and the 'Delivered in' text, are monolith-era and are not restated per service | Business analyst | Resolved (directive) |
| GAP-0296 | The plan names no owner per release, and no source states which team owns a wave's release readiness | Delivery lead | Resolved (directive) |
| GAP-0297 | Version 5 carries no approval and the source records no status | Programme governance | Open (business decision) |
| GAP-0298 | Version 4 gives S4 rwb-litigation notice approval in E2 while Architecture v5 creates S4 in Wave 3 | Solution architect | Accepted (directive); not applied: value not in the source documents |
| GAP-0299 | The file is version 3 while its metadata table states Version 2 | Business analyst | Accepted (directive); resolution in progress |
| GAP-0300 | Only the first release date is named; the Wave 2, 3 and 4 release dates and the wave to release mapping are not stated | Release owner | Resolved (directive) |
| GAP-0301 | No source states that one wave goes live per release or how a wave maps to a release | Release owner | Resolved (directive) |
| GAP-0302 | The first-release scope is written per capability, not per service, so the Wave 1 service that delivers each capability is not stated | Solution architect | Resolved (directive) |
| GAP-0303 | The rollback of version 3 switches one set of feature flags and redeploys one tag, and has no per-service rollback, no Worker Versioning statement and no rule package rollback | DevOps team | Resolved (directive) |
| GAP-0304 | The BOT approval under FPG 19/2560 clause 5.5 is not in the cutover plan and its submission date is not stated | Programme governance | Open (business decision) |
| GAP-0305 | Version 3 has the release read the 30 views under a recovery role, while Architecture v5 gives the views to rwb-source-data only, one login per service | ACE DB team | Resolved (directive) |
| GAP-0306 | No source states the production capacity or the deployment slot model for a wave of up to nine services | SCB IT infrastructure | Accepted (directive); not applied: value not in the source documents |
| GAP-0307 | The tracker retirement names the six teams but no service, so the replacement case list per team is not stated | Business lead | Open (business decision) |
| GAP-0308 | The source carries no Status or approval row, and no approval of this version is recorded | Programme governance | Open (business decision) |
| GAP-0309 | No source names a service owner for the run of any of the 19 services | Programme governance | Open (business decision) |
| GAP-0310 | The tier 2 and tier 3 roles of version 2 are not defined per service now that there are 19 services | Programme governance | Open (business decision) |
| GAP-0311 | Version 2 gives four severity bands but no alert threshold, no SLO and no dashboard per service | SCB IT infrastructure | Resolved (directive) |
| GAP-0312 | No source gives an on-call rota per service or the hand-off from the tier roles to the 19 services | DevOps team | Accepted (directive); not applied: value not in the source documents |
| GAP-0313 | The source deck carries no change log, no version history and no tool line | Business analyst | Accepted (directive); not applied: value not in the source documents |
| GAP-0314 | The source deck has no run book per service, although the target has 19 services | Solution architect | Accepted (directive); not applied: value not in the source documents |
| GAP-0315 | No approval of version 3 is recorded and the source deck carries no status | Programme governance | Open (business decision) |
| GAP-0316 | Review-by date for the nine realignment risks | Program manager | Resolved (directive) |
| GAP-0317 | Numbering of the nine realignment risks | Program manager | Accepted (directive); resolution in progress |
| GAP-0318 | Owner vocabulary for risks, assumptions and dependencies after the realignment | Architecture | Accepted (directive); resolution in progress |
| GAP-0319 | The source workbook records no version, version date, change log or tool line | Program manager | Accepted (directive); resolution in progress |
| GAP-0320 | Two recovery squads and fourteen source module names do not map one to one onto nineteen services | Product owner with the two tech leads and the program manager | Open (business decision) |
| GAP-0321 | Six services have no source module and no squad in the resource plan | Product owner with the two tech leads | Open (business decision) |
| GAP-0322 | The wave 0 platform epics have no team, no full-time equivalent and no accountable role | IT lead with the platform team | Resolved (directive) |
| GAP-0323 | The DevOps team type has no full-time equivalent in the resource plan | IT lead | Accepted (directive); resolution in progress |
| GAP-0324 | SCB IT infrastructure has no full-time equivalent and appears only as a shared supporting team | IT lead | Resolved (directive) |
| GAP-0325 | The QA team type is staffed inside the TechX squads and has no separate capacity line | QA lead with the program manager | Accepted (directive); resolution in progress |
| GAP-0326 | The phrase 'TechX' and the source rows 'Recovery squad 1 and 2 (Organization TechX)' use two vocabularies | Program manager | Accepted (directive); resolution in progress |
| GAP-0327 | The accountability text is module based and names the recovery module that no longer exists as one unit | Solution architect | Resolved (directive) |
| GAP-0328 | The shared Epic 2 items of DL30 are not identified per service | Product owner with the Collection squad and P3 rwb-case | Open (business decision) |
| GAP-0329 | No approval of the resource plan is recorded | Program manager with the business lead | Open (business decision) |
| GAP-0525 | Gap cited in B2-P1-003 | Tech lead | Accepted (directive); resolution in progress |
| GAP-0539 | Gap cited in B2-P1-008 | Tech lead | Accepted (directive); resolution in progress |
| GAP-0545 | Gap cited in B2-P1-010 | Tech lead | Accepted (directive); resolution in progress |
| GAP-0605 | Gap cited in B2-P1-016 | Tech lead | Accepted (directive); resolution in progress |
| GAP-0632 | Gap cited in B2-P10-001 | Tech lead | Accepted (directive); resolution in progress |
| GAP-0733 | Gap cited in B2-P3-007 | Tech lead | Accepted (directive); resolution in progress |
| GAP-0768 | Gap cited in B-P3-09 | Tech lead | Accepted (directive); resolution in progress |
| GAP-0800 | Gap cited in B2-P4-001 | Tech lead | Accepted (directive); resolution in progress |
| GAP-0865 | Gap cited in B2-P4-006 | Tech lead | Accepted (directive); resolution in progress |
| GAP-0866 | Gap cited in B2-P4-009 | Tech lead | Accepted (directive); resolution in progress |
| GAP-0894 | Gap cited in B-P4-07 | Tech lead | Accepted (directive); resolution in progress |
| GAP-1042 | Gap cited in B-P5-04 | Tech lead | Accepted (directive); resolution in progress |
| GAP-1136 | Gap cited in B-P6-02 | Tech lead | Accepted (directive); resolution in progress |
| GAP-1321 | Gap cited in B2-P7-008 | Tech lead | Accepted (directive); resolution in progress |
| GAP-1322 | Gap cited in B2-P7-009 | Tech lead | Accepted (directive); resolution in progress |
| GAP-1345 | Gap cited in B2-P7-016 | Tech lead | Accepted (directive); resolution in progress |
| GAP-1383 | Gap cited in B2-P8-001 | Tech lead | Accepted (directive); resolution in progress |
| GAP-1453 | RWB-E1-014 is live in the BRD but retired by D-RCV-60 | Product owner | Open (business decision) |
| GAP-1454 | RWB-E1-029 is live in the BRD but was cancelled before this run | Product owner | Open (business decision) |
| GAP-1455 | RWB-E1-048 is live in the BRD but was cancelled before this run | Product owner | Open (business decision) |
| GAP-1458 | Four open-decision rows name people in the owner column and no owner role | Business lead | Open (business decision) |
| GAP-1459 | RWB-E2-023 Automated EFS file load has no legacy story and no slice in the plan | Product owner with the data product owner | Open (business decision) |
| GAP-1460 | Two open decisions name individuals as owners and the source states no role for either | Product owner | Open (business decision) |
| GAP-1461 | The document control block says Version 1 and 28 October 2026 while the source file is v2 and this version is 3 | Product owner | Open (business decision) |
| GAP-1462 | Ten Epic 2 legacy keys in the plan have no requirement row in this BRD | Product owner with the business lead | Open (business decision) |
| GAP-1491 | Section 9 names persons as decision owners | Programme governance | Open (business decision) |
| GAP-1492 | One requirement prefix, REQ-DRI, is used by two modules | Solution architect | Resolved (directive) |
| GAP-1493 | No delivery model or service-epic mapping in version 4 | Programme manager | Closed |
| GAP-1494 | Business epic codes EP01 to EP08 are not defined in this document | Programme manager | Resolved (directive) |
| GAP-1495 | Three constraints in section 7 contradict the target architecture | Solution architect | Closed |
| GAP-1496 | Interaction ledger requirements sit under P7 but the ledger is P1's | Solution architect | Accepted (directive); resolution in progress |
| GAP-1497 | Approval requirements sit under P7 but the authority table is P4's | Solution architect | Accepted (directive); resolution in progress |
| GAP-1498 | No requirement section for P8 payment, P9 reporting or P10 agent | Product owner | Open (business decision) |
| GAP-1515 | No approval status is recorded for the business requirements in this run | Product owner | Duplicate of GAP-1592 |
| GAP-1526 | The BRD carries no status field and no approval record for the requirements approval gate | Product Owner | Duplicate of GAP-1592 |
| GAP-1543 | Neither BRD carries an approval record or a document status | Product Owner | Duplicate of GAP-1592 |
| GAP-1550 | BRD and FSD approval status is not evidenced in the source documents | Product owner | Open (business decision) |
| GAP-1551 | FSD P3 file name is v4 while the document states version 3 | Business analyst, P3 | Accepted (directive); resolution in progress |
| GAP-1552 | The FSD carries no requirement identifiers, so FR mapping uses the BRD REQ IDs and the FSD FEAT, BR and AC codes | Business analyst, P3 | Resolved (directive) |
| GAP-1553 | REQ-WKM-010 capacity view is assigned to rwb-case but has no story in the wave plan | Capacity and workforce planner | Accepted (directive); not applied: value not in the source documents |
| GAP-1555 | No retention period is set for any case record class | Compliance | Open (business decision) |
| GAP-1556 | Non-functional target values are open under DL11 | Solution architect with Risk | Open (business decision) |
| GAP-1561 | Duplicate case merge has no feature or acceptance criteria in the FSD | Case owner | Resolved (directive) |
| GAP-1592 | The BRDs carry no status field and no approval record, so the requirements approval gate has no recorded baseline | Product Owner | Open (business decision) |
| GAP-1611 | The business requirements document carries no approval for this service and this PRD is issued as Draft | Product owner with the FDA | Open (business decision) |
| GAP-1613 | The daily copy of the decision log to the data lake and its row-count reconciliation have no target under Architecture v5 | Solution architect with the reporting and BI analyst | Resolved (directive) |
| GAP-1642 | No approval is recorded for this product baseline | Product Owner | Open (business decision) |
| GAP-1645 | FSD P9 has no requirement IDs, so FR rows cannot map to FSD REQ IDs | Business analyst, P9 | Accepted (directive); resolution in progress |
| GAP-1647 | JOB-15 is described both as a Temporal Schedule at 01:30 and as an Airflow trigger | Solution architect with the bank platform team | Resolved (directive) |
| GAP-1648 | The report resource path differs between the architecture and the ownership map | Solution architect | Resolved (directive) |
| GAP-1650 | RWB-E1-014 is retired but the operations reporting of P9 is built on the copy it produced | Solution architect | Resolved (directive) |
| GAP-1654 | No field catalog exists for the snapshot, the publication, the report definition, the run record or the projections | Data architect | Resolved (directive) |
| GAP-1655 | No retention class or retention period is set for a snapshot, an extract or a run record | Compliance and PDPA officer | Open (business decision) |
| GAP-1660 | Message IDs from other modules are reused by P9's validation rules | Business analyst, P9 | Resolved (directive) |
| GAP-1661 | No approval is recorded for this PRD | Product Owner | Open (business decision) |
| GAP-1665 | No predecessor PRD exists in the PLT family | Product owner | Open (business decision) |
| GAP-1671 | The BRD carries no approval record and no status field | Product owner | Duplicate of GAP-1592 |
| GAP-1725 | The release of a guarantor and of a TCG guarantee have approval authorities but no requirement | Risk with the product heads | Open (business decision) |
| GAP-1727 | TSD S3 publishes no event, while Architecture v5 gives two claim events and the catalogue numbers neither | Solution architect | Resolved (directive) |
| GAP-1729 | The retention class and the masking rules of the claim record are not set | Compliance and PDPA officer | Open (business decision) |
| GAP-1734 | The number of claims a month and the number of guarantors a case are not stated | Business lead | Open (business decision) |
| GAP-1735 | The dates and change notes of FSD S3 v1 and v2 are not in the sources read | Business analyst, S3 | Resolved (directive) |
| GAP-1765 | No approval is recorded for the requirements this PRD states | Product Owner | Open (business decision) |
| GAP-1766 | The history of FSD S5 versions 1 and 2 is not in the sources read | Business analyst, S5 | Resolved (directive) |
| GAP-1860 | The FSD modules are written against one recovery schema and one login and carry no per-service ownership | Data architect | Accepted (directive); resolution in progress |
| GAP-1861 | Seven module specifications still send extracts and copies to a data lake that Architecture v5 removes | Solution architect | Accepted (directive); resolution in progress |
| GAP-1862 | Five module specifications name the Quartz scheduler as their scheduling mechanism | Solution architect | Accepted (directive); resolution in progress |
| GAP-1863 | Recovery point objective not stated for the 19 services | IT lead with Operational Risk | Open (business decision) |
| GAP-1864 | Recovery time objective not stated for the 19 services | IT lead with Operational Risk | Open (business decision) |
| GAP-1865 | 'Weeks' versus '28 days' wording for the same period | Business analyst | Resolved (directive) |
| GAP-1866 | NFR-042 logs reads of a data lake copy that Architecture v5 removes | Solution architect | Resolved (directive) |
| GAP-1867 | Concurrency and named-user figures disagree between section 2, NFR-002 and NFR-003 and Architecture v5 | Business lead | Open (business decision) |
| GAP-1868 | Owning service not derivable from the Ownership Map for NFR-032 | Solution architect | Resolved (directive) |
| GAP-1884 | Gap cited in B2-S4-011 | Tech lead | Accepted (directive); resolution in progress |
| GAP-1945 | Gap cited in B2-S5-023 | Tech lead | Accepted (directive); resolution in progress |
| GAP-1977 | Gap cited in B2-S6-001 | Tech lead | Accepted (directive); resolution in progress |
| GAP-1978 | Owner labels in the open points name individuals, not roles | Programme governance | Open (business decision) |
| GAP-1979 | Version 4 carries the version 3 approval statuses and no approval of the 19-service decision | Programme governance | Open (business decision) |
| GAP-1980 | The option 3 cells of the workflow comparison are written as not-now and no source restates them | Solution architect | Resolved (directive) |
| GAP-1981 | Statements about one repository, no extra runtime, Quartz and Spring Batch are not restated for 19 services | Solution architect | Accepted (directive); resolution in progress |
| GAP-1982 | The number of squads that release the 19 services is not stated | TechX delivery lead | Accepted (directive); not applied: value not in the source documents |
| GAP-1983 | Table counts per schema are not stated in any source | Solution architect | Resolved (directive) |
| GAP-1985 | The shared topic rwb.decision-record.v1 has no topic settings | Solution architect | Resolved (directive) |
| GAP-1987 | A service's first epic in version 6 differs from its wave in Architecture v5 | Solution architect | Accepted (directive); resolution in progress |
| GAP-1988 | No source sizes the deployment slots for 38 deployments across four environments | SCB IT infrastructure | Accepted (directive); not applied: value not in the source documents |
| GAP-1989 | The repository model for the 19 services is not stated | DevOps team | Resolved (directive) |
| GAP-1990 | The Temporal cluster, namespace and workflow kit are owned by a role, not by an owner code | Platform team | Resolved (directive) |
| GAP-1995 | S1 owns the valuations but has no table in the Ownership Map | Solution architect | Accepted (directive); resolution in progress |
| GAP-1996 | Eleven business events have no number in the catalogue and three have no contract | Solution architect | Resolved (directive) |
| GAP-1997 | The Arch v5 contract paths and the published OpenAPI files differ | Solution architect | Accepted (directive); resolution in progress |
| GAP-1998 | Every module specification is still In review and no approval is recorded | Design authority | Accepted (directive); resolution in progress |
| GAP-1999 | No squad is named per service | Delivery lead | Accepted (directive); resolution in progress |
| GAP-2000 | No interface carries the reporting output after INT-19 and INT-20 are removed | Solution architect | Accepted (directive); not applied: value not in the source documents |
| GAP-2002 | INT-34 (ACE Common) has five consumers and no single owning service | Solution architect | Resolved (directive) |
| GAP-2003 | INT-14 (WIN registered mail) has three different owners in the sources | Solution architect | Accepted (directive); resolution in progress |
| GAP-2004 | INT-25 (debt-buyer data tape) is owned by the Workbench in v3 and by two services in the target | Solution architect | Accepted (directive); resolution in progress |
| GAP-2005 | INT-24 is screen-based through the external gateway in v3 and gateway-based around rwb-partner in Architecture v5 | Solution architect | Resolved (directive) |
| GAP-2006 | No PII topic, schema or sender library is named for INT-22, the audit and PII path | Platform architect | Resolved (directive) |
| GAP-2007 | Field mapping and Key cite Logical Data Model and Data Dictionary v7 while v8 is the latest in the set | Data architect | Accepted (directive); not applied: value not in the source documents |
| GAP-2009 | Environment names for per-service deployment | SCB IT infrastructure lead | Accepted (directive); not applied: value not in the source documents |
| GAP-2010 | Kubernetes namespace of the 19 services against the namespace of the Temporal release | SCB IT infrastructure lead | Accepted (directive); not applied: value not in the source documents |
| GAP-2011 | Temporal server is pinned at 1.28.1 but Nexus and Worker Versioning need 1.30 or later | SCB IT architecture | Accepted (directive); not applied: value not in the source documents |
| GAP-2012 | The 19 database logins and the per-service connection budget are not named | ACE team, DBA | Accepted (directive); not applied: value not in the source documents |
| GAP-2013 | Per-service CPU, memory and autoscaling thresholds are not stated | SCB IT infrastructure lead | Accepted (directive); not applied: value not in the source documents |
| GAP-2014 | Kafka cluster ownership, sizing and the Event Hubs fallback are not decided | SCB IT infrastructure lead | Resolved (directive) |
| GAP-2015 | The shared Quartz tables are either kept by Epic 1 and Epic 2 or no longer used | Solution architect | Resolved (directive) |
| GAP-2052 | Retry-topic and dead-letter topic names are not specified | Tech lead | Resolved (directive) |
| GAP-2054 | No message ID for a REST hop timeout or a dead-lettered event | Tech lead | Resolved (directive) |
| GAP-2055 | Role that replays a dead-lettered event is not named | Platform administrator | Resolved (directive) |
| GAP-2056 | The 2 s REST timeout equals the 2 s screen target | Tech lead | Resolved (directive) |
| GAP-2057 | The source file is v2 in its name and Version 1 in its own table, with the date 28 October 2026 | Technical documentation with the architecture team | Accepted (directive); resolution in progress |
| GAP-2059 | The source sends report queries to the data lake copy, and the target architecture removes the data lake | P9 rwb-reporting with P1 rwb-source-data | Accepted (directive); resolution in progress |
| GAP-2071 | The nightly copy to the data lake survives in the source and in the v4 batch design | Service owner P7 rwb-decision | Accepted (directive); resolution in progress |
| GAP-2077 | The source metadata table says Version 1 while the file family is v2 | P5 rwb-document | Accepted (directive); resolution in progress |
| GAP-2078 | The case match of an intake item has no consumed contract in Architecture v5 | P5 rwb-document | Accepted (directive); resolution in progress |
| GAP-2079 | The legal hold is a case operation in the Ownership Map and a hub rule in the source design | P3 rwb-case | Accepted (directive); resolution in progress |
| GAP-2080 | e-Discovery is described with no operation in the Ownership Map | P5 rwb-document | Accepted (directive); resolution in progress |
| GAP-2081 | Document types and checklists are reference data in the source and P5 tables in the Ownership Map | P5 rwb-document | Accepted (directive); resolution in progress |
| GAP-2082 | The intake job has no mechanism or frequency in the source design | P5 rwb-document | Accepted (directive); resolution in progress |
| GAP-2083 | The search index and the masking rows sit with different owners | P5 rwb-document | Resolved (directive) |
| GAP-2084 | E-signature is named in the type table and nowhere else | P5 rwb-document | Resolved (directive) |
| GAP-2085 | The storage is 'Blob storage' in the source and Azure Blob with a WORM container in Architecture v5 | P5 rwb-document | Accepted (directive); resolution in progress |
| GAP-2086 | The overdue-original task has no owner queue | P3 rwb-case | Accepted (directive); resolution in progress |
| GAP-2100 | O05, decisions and outcomes for model learning, has no path once the data lake is removed | Solution architect | Accepted (directive); not applied: value not in the source documents |
| GAP-2108 | The By route counts are blank in v2 and v3 although the sheet says they are calculated | Solution architect | Accepted (directive); resolution in progress |
| GAP-2109 | The data lake row and INT-19 and INT-20 are kept while Architecture v5 removes them | Solution architect | Resolved (directive) |
| GAP-2110 | Four services own no row of the disposition or the interface inventory | Solution architect | Resolved (directive) |
| GAP-2111 | No source names an owning service for any system or interface | Solution architect | Resolved (directive) |
| GAP-2112 | The data product of INT-06 (AAL) reads To confirm | Data architect | Accepted (directive); resolution in progress |
| GAP-2113 | INT-33 (Legal Execution Department and courts) has no standard and two candidate services | Solution architect | Accepted (directive); not applied: value not in the source documents |
| GAP-2114 | Three statements of v3 read as outdated and are kept word for word | Solution architect | Resolved (directive) |
| GAP-2115 | The partner portal row keeps the wording of the external gateway | Solution architect | Resolved (directive) |
| GAP-2116 | The source file is named v2 while its metadata table gives Version 1, and it carries no change-log row | Business analyst | Resolved (directive) |
| GAP-2117 | No approval of the new version is recorded and the source has no Status row | Programme governance | Open (business decision) |
| GAP-2118 | The nine levels of version 2 describe one deployable and state no criteria for contract, component or wave integration testing | Test lead | Accepted (directive); not applied: value not in the source documents |
| GAP-2119 | No source names the owner of a contract test or of a contract fake | Test lead | Accepted (directive); not applied: value not in the source documents |
| GAP-2120 | How SIT is composed while a later-wave service does not exist is not stated | Test lead | Resolved (directive) |
| GAP-2121 | The environments are counted but never named in any source | SCB IT infrastructure | Accepted (directive); not applied: value not in the source documents |
| GAP-2124 | Document control states Version 1 while the file is the second version | Document owner | Accepted (directive); resolution in progress |
| GAP-2125 | The plan names no test ID and no per-service test | QA lead | Accepted (directive); resolution in progress |
| GAP-2126 | User concurrency is written four ways across the sources | Solution architect | Accepted (directive); resolution in progress |
| GAP-2128 | The release names E1 to E8 are not mapped to waves or epics | Delivery lead | Accepted (directive); resolution in progress |
| GAP-2129 | Accessibility is 'each screen' and no screen inventory exists | Business lead | Open (business decision) |
| GAP-2135 | The source does not say how the data in a fake relates to the sandbox seed | QA | Accepted (directive); not applied: value not in the source documents |
| GAP-2138 | Events that the event catalogue does not number cannot be named by an EV ID in a fake | TechX | Accepted (directive); not applied: value not in the source documents |
| GAP-2139 | The daily journey smoke workflow has no data set in the plan | DEVOPS | Accepted (directive); not applied: value not in the source documents |
| GAP-2140 | The map gives six tables to the platform library but does not say which schema holds them | TechX | Accepted (directive); resolution in progress |
| GAP-2141 | The metadata Version row reads 2 while the file family reads v3 | Document owner | Accepted (directive); not applied: value not in the source documents |
| GAP-2142 | No owner per service is stated, and no owner table exists | Product owner; service owner | Open (business decision) |
| GAP-2143 | The definition of ready does not require a published contract | Tech lead; QA lead | Accepted (directive); not applied: value not in the source documents |
| GAP-2144 | The definition of done names no boundary test and no contract test result | Tech lead; QA lead | Accepted (directive); not applied: value not in the source documents |
| GAP-2145 | No contract version, compatibility or withdrawal rule is stated | Enterprise architecture | Accepted (directive); not applied: value not in the source documents |
| GAP-2146 | One module means the monolith module in the source and a service and schema after the split | Tech lead; enterprise architecture | Accepted (directive); not applied: value not in the source documents |
| GAP-2147 | A tracker record is named in the definition of done while tracker work is out of scope | Delivery lead | Accepted (directive); not applied: value not in the source documents |
| GAP-2149 | No owner and no approval path are stated for contract publication or for the boundary test | Product owner; service owner; DevOps lead | Open (business decision) |
| GAP-2151 | The document family has no source file, so no version, section, ID or date can be carried forward | Document owner | Accepted (directive); resolution in progress |
| GAP-2152 | No source states an integration-level exit threshold | QA lead | Accepted (directive); resolution in progress |
| GAP-2153 | The number and calendar of integration test cycles per wave are not stated | Delivery lead | Accepted (directive); resolution in progress |
| GAP-2156 | How SIT is composed while a later-wave service is not deployed is not stated | Integration lead | Resolved (directive) |
| GAP-2157 | Which non-functional requirements are proven at the integration level is not stated | Solution architect | Accepted (directive); resolution in progress |
| GAP-2195 | Gap cited in B2-P10-003 | Tech lead | Accepted (directive); resolution in progress |
| GAP-2231 | Gap cited in B2-P3-013 | Tech lead | Accepted (directive); resolution in progress |
| GAP-2268 | Gap cited in B2-P4-003 | Tech lead | Accepted (directive); resolution in progress |
| GAP-2279 | Gap cited in B2-P4-010 | Tech lead | Accepted (directive); resolution in progress |
| GAP-2287 | Gap cited in B2-P4-013 | Tech lead | Accepted (directive); resolution in progress |
| GAP-2292 | Gap cited in B2-P4-014 | Tech lead | Accepted (directive); resolution in progress |
| GAP-2297 | Gap cited in B2-P4-015 | Tech lead | Accepted (directive); resolution in progress |
| GAP-2310 | Gap cited in B2-P4-020 | Tech lead | Accepted (directive); resolution in progress |
| GAP-2315 | Gap cited in B2-P4-021 | Tech lead | Accepted (directive); resolution in progress |
| GAP-2331 | Gap cited in B2-P4-026 | Tech lead | Accepted (directive); resolution in progress |
| GAP-2383 | Gap cited in B2-P6-006 | Tech lead | Accepted (directive); resolution in progress |
| GAP-2451 | Gap cited in B2-P7-011 | Tech lead | Accepted (directive); resolution in progress |
| GAP-2477 | Gap cited in B2-P7-019 | Tech lead | Accepted (directive); resolution in progress |
| GAP-2499 | Gap cited in B2-P7-022 | Tech lead | Accepted (directive); resolution in progress |
| GAP-2509 | Gap cited in B2-P8-002 | Tech lead | Accepted (directive); resolution in progress |
| GAP-2581 | Gap cited in B2-P9-003 | Tech lead | Accepted (directive); resolution in progress |
| GAP-2608 | Gap cited in B2-S1-004 | Tech lead | Accepted (directive); resolution in progress |
| GAP-2660 | Gap cited in B2-S2-002 | Tech lead | Accepted (directive); resolution in progress |
| GAP-2686 | Gap cited in B2-S2-013 | Tech lead | Accepted (directive); resolution in progress |
| GAP-2694 | Gap cited in B2-S2-017 | Tech lead | Accepted (directive); resolution in progress |
| GAP-2704 | Gap cited in B2-S2-021 | Tech lead | Accepted (directive); resolution in progress |
| GAP-2707 | Gap cited in B2-S2-023 | Tech lead | Accepted (directive); resolution in progress |
| GAP-2710 | Gap cited in B2-S3-001 | Tech lead | Accepted (directive); resolution in progress |
| GAP-2713 | Gap cited in B2-S3-002 | Tech lead | Accepted (directive); resolution in progress |
| GAP-2727 | Gap cited in B2-S3-005 | Tech lead | Accepted (directive); resolution in progress |
| GAP-2741 | Gap cited in B2-S3-009 | Tech lead | Accepted (directive); resolution in progress |
| GAP-2772 | Gap cited in B2-S4-007 | Tech lead | Accepted (directive); resolution in progress |
| GAP-2780 | Gap cited in B2-S4-008 | Tech lead | Accepted (directive); resolution in progress |
| GAP-2859 | Gap cited in B2-S5-005 | Tech lead | Accepted (directive); resolution in progress |
| GAP-2979 | Gap cited in B2-S6-003 | Tech lead | Accepted (directive); resolution in progress |
| GAP-3003 | Gap cited in B2-S6-009 | Tech lead | Accepted (directive); resolution in progress |
| GAP-3020 | Gap cited in B2-S7-002 | Tech lead | Accepted (directive); resolution in progress |
| GAP-3045 | Gap cited in B2-S7-014 | Tech lead | Accepted (directive); resolution in progress |
| GAP-3065 | Gap cited in B2-S8-007 | Tech lead | Accepted (directive); resolution in progress |
| GAP-3105 | Gap cited in B2-S9-001 | Tech lead | Accepted (directive); resolution in progress |
| GAP-3116 | Gap cited in B2-S9-006 | Tech lead | Accepted (directive); resolution in progress |
| GAP-3150 | Thai wording for the three rows that D-RCV-60 adds to the glossary | TechX | Accepted (directive); not applied: value not in the source documents |
| GAP-3152 | Name, version and location of a contract fake | TechX | Resolved (directive) |
| GAP-3153 | Level and register place of an -ITG copy of a test case | QA team | Accepted (directive); not applied: value not in the source documents |
| GAP-3165 | The data lake copy note remains in the build notes although the decision retires it | Solution architect | Accepted (directive); resolution in progress |
| GAP-3185 | RWB-E2-023 has no row in the plan, so it has no service, lane or new stories | Product owner with the integration lead | Open (business decision) |
| GAP-3195 | Open defects of retired and cancelled keys have no target story | Delivery lead | Resolved (directive) |
| GAP-3196 | Two v4 rows carry narrative defect labels that do not match a register number | Delivery lead | Resolved (directive) |
| GAP-3197 | No source states the replacement timing rule for the retired Quartz job behind row 93 | Recovery tech lead | Resolved (directive) |
| GAP-3198 | The Service Story Catalog has no epic-level scope or suggested-owner column | Delivery lead | Accepted (directive); resolution in progress |
| GAP-3200 | Epic lane counts add to 547 while the programme has 510 distinct lanes | Delivery lead | Resolved (directive) |
| GAP-3201 | The source guide carries no version, date or status in its body | Delivery lead | Accepted (directive); resolution in progress |
| GAP-3202 | The guide describes one story per legacy key and gives no way to read a split story | Delivery lead | Accepted (directive); resolution in progress |
| GAP-3203 | No Thai wording is specified for the four new sections | Delivery lead | Accepted (directive); resolution in progress |
| GAP-3204 | The work types and the story key pattern do not appear in the guide | Delivery lead | Accepted (directive); resolution in progress |
| GAP-3205 | The project hub and the glossary are described without their state after the realignment | Delivery lead | Resolved (directive) |
| GAP-3210 | The v6 Module column names a different service from the realigned owner | Solution architect | Accepted (directive); resolution in progress |
| GAP-3212 | Requirements that no realigned story cites | Business analyst | Accepted (directive); resolution in progress |
| GAP-3214 | No legacy key for requirements written before the realignment | Business analyst | Accepted (directive); resolution in progress |
| GAP-3215 | The v6 coverage statement no longer describes the story position | Test manager | Accepted (directive); resolution in progress |
| GAP-3216 | No issue-tracker, branch, commit or pull-request metadata | Delivery lead | Accepted (directive); resolution in progress |
| GAP-3217 | Every realigned artifact is Draft with no approval | Delivery lead | Accepted (directive); resolution in progress |
| GAP-3218 | Test cases of RWB-E2-023 have no story in the realignment plan | Test lead | Resolved (directive) |
| GAP-3219 | Level vocabulary of Test Cases v7 is not the Template and Rules R7.2 vocabulary | Test lead | Accepted (directive); resolution in progress |
| GAP-3220 | Test Cases v7 covers 147 legacy keys of the 358 in the plan | Test lead | Accepted (directive); not applied: value not in the source documents |
| GAP-3221 | A rule case names a route set, not the story or service that owns the rule set | Test lead | Accepted (directive); resolution in progress |
| GAP-3222 | Neither workbook states the owner of a case | Test lead | Accepted (directive); resolution in progress |
| GAP-3223 | Two retired stories keep 20 live cases with no owning service | Test lead | Accepted (directive); resolution in progress |
| GAP-3224 | Integration test case count of the Integration Test Plan is not held in Test Cases v7 | Test lead | Accepted (directive); resolution in progress |
| GAP-3225 | Regression Suite Growth sheet stops at release E6 | Test lead | Accepted (directive); resolution in progress |
| GAP-3226 | No environment or pipeline stage is stated for the platform cases | Test lead | Accepted (directive); not applied: value not in the source documents |
| GAP-3229 | Window dates end in January 2027 while the new stories release through June 2027 | Delivery lead | Resolved (directive) |
| GAP-3231 | The v6 module column cannot show who builds a split row | Delivery lead | Accepted (directive); resolution in progress |
| GAP-3235 | Five of the six Wave 0 platform dependencies of Architecture v5 slide 39 have no row in the external dependency table | ACE team with Enterprise Architecture; Platform team; Risk and Internal Audit; Compliance and IT Risk | Open (business decision) |
| GAP-3236 | 124 non-CON stories carry no dependency row, 31 of them application stories | TechX | Resolved (directive) |
| GAP-3237 | Version 3 carries no approval record and no status, so version 4 has no approved baseline | Programme governance | Open (business decision) |
| GAP-3238 | Version 3 carries no change log and no tool line | Delivery lead | Accepted (directive); resolution in progress |
| GAP-3242 | No source states the board limit of a team type, or how many stories one team type may hold at once | Delivery lead | Accepted (directive); resolution in progress |
| GAP-3243 | Version 3 names no release date for an item beyond the epic its window releases in | Delivery lead | Accepted (directive); resolution in progress |
| GAP-3245 | The waits-on column of version 3 names legacy keys, and the stories that now carry those keys are different work items | Solution architect | Accepted (directive); resolution in progress |
| GAP-3246 | RPO and RTO per service not stated | Solution architect | Resolved (directive) |
| GAP-3247 | 'Weeks' versus '28 days' retention wording | Business analyst | Accepted (directive); resolution in progress |
| GAP-3248 | Kafka cluster ownership and sizing | SCB IT infrastructure lead | Resolved (directive) |
| GAP-3249 | Temporal namespace and codec key ownership | SCB IT infrastructure lead | Accepted (directive); resolution in progress |
| GAP-3250 | Schema registry product | Solution architect | Accepted (directive); resolution in progress |
| GAP-3252 | Partner gateway hosting (DMZ) | SCB IT infrastructure lead | Accepted (directive); resolution in progress |
| GAP-3253 | Issue tracker status of Epic 1 not readable in this run | Delivery lead | Accepted (directive); resolution in progress |
| GAP-3254 | Regulatory obligations not traced to business requirement IDs | Business analyst | Accepted (directive); not applied: value not in the source documents |
| GAP-3255 | 29 of 32 regulatory obligations not confirmed | Compliance | Open (business decision) |
| GAP-3256 | Audit findings not traced to business requirement IDs | Business analyst | Accepted (directive); not applied: value not in the source documents |
| GAP-3257 | Controls not in the BRD | Business analyst | Closed |
| GAP-3258 | NFR-079 and NFR-080 missing from the BRD | Solution architect | Closed |
| GAP-3259 | 19 business measures missing from the BRD | Business analyst | Closed |
| GAP-3260 | 20 business measures have a To set baseline or target \| | Business lead | Open (business decision) |
| GAP-3261 | Reports not in the BRD | Business analyst | Closed |
| GAP-3262 | Processes 18.1 and 18.2 have no business requirement | Shared operations | Accepted (directive); not applied: value not in the source documents |
| GAP-3263 | Process 14.3 has no business requirement | Center of excellence | Accepted (directive); not applied: value not in the source documents |
| GAP-3264 | Process 15.2 has no program requirement | Business analyst | Resolved (directive) |
| GAP-3265 | Open decisions missing from section 9 | Business analyst | Closed |
| GAP-3266 | Backlog story codes used as requirement keys | Business analyst | Closed |
| GAP-3267 | DL09 owner differs between the epic BRDs | Business lead | Open (business decision) |
| GAP-3268 | Program section 12 printed candidate IDs | Business analyst | Closed |
| GAP-3269 | Epics 3 to 8 BRD traced to Program v4 | Business analyst | Closed |
| GAP-3270 | Duplicate gaps for BRD approval status | Business analyst | Closed |

## 7. Unconfirmed assumptions (tied to a business decision)

| ASM ID | Assumption | Status |
|---|---|---|
| ASM-0011 | The release dates carried in the v2 context stay unchanged and tentative; Arch v5 waves 0-4 are not mapped to them in this run. | Unconfirmed (business decision pending) |
| ASM-0013 | The decision record is written locally in one transaction with the state change and sealed in the central ledger; strict mode applies at the four points of no return. | Unconfirmed (business decision pending) |
| ASM-0016 | Phase 1 packages stay in XLS decision-table format; DMN 1.6 conversion is table by table on the same Drools runtime. | Unconfirmed (business decision pending) |
| ASM-0020 | The move to 19 services is treated as a significant change for FPG 19/2560 clause 5.5 until Compliance says otherwise, and the 30 business day lead time is planned. | Unconfirmed (business decision pending) |
| ASM-0025 | RPO and RTO stay unset in this baseline; no target is claimed. | Unconfirmed (business decision pending) |
| ASM-0030 | The three regulatory citations are used as the architecture source states them and Compliance confirms them before the wave 1 gate. | Unconfirmed (business decision pending) |
| ASM-0144 | The three monitoring owner roles of version 2 are kept word for word, and the data each measure reads is attributed to its owner in the Ownership Map: score coverage to rwb-source-data (P1), drift to rwb-agent (P10) and rwb-decision (P7), outcome to rwb-source-data (P1) and rwb-decision (P7). | Unconfirmed (business decision pending) |
| ASM-0191 | The header date of v10, 15 November 2026, is read as the date the sheet text was last edited, not as the issue date of the version, and is carried into v11 unchanged. | Unconfirmed (business decision pending) |
| ASM-0246 | The DoA limit amounts stay in the Delegation of Authority Matrix and in the versioned DoA rule package; delegation_limit in rwb_access holds them and GET /doa-limits serves them. | Unconfirmed (business decision pending) |
| ASM-0259 | Version 4 is issued as Draft because no approval of it is recorded in any source, and the catalog carries no approval row in version 3 either. | Unconfirmed (business decision pending) |
| ASM-0261 | The file name gives the family version, so this document is version 3; the source reading of Version 1 and Date 28 October 2026 is kept in a Source version row and in the change log. | Unconfirmed (business decision pending) |
| ASM-0262 | The decision log is kept in rwb_decision, in the append-only decision_log_entry table and the central ledger, with the local decision record of the owning service; no copy goes to a data lake. | Unconfirmed (business decision pending) |
| ASM-0265 | A legal hold on a party or on a document is recorded on the case in recovery_case.legal_hold and applied by the P5 retention job, which excludes the documents of a held case. | Unconfirmed (business decision pending) |
| ASM-0267 | The access-log period stays per the bank security standard and its archive rule stays; the store behind GET /admin/access-log belongs to P4 rwb-access and is not in the Physical Schema v6. | Unconfirmed (business decision pending) |
| ASM-0276 | The file name is the version of record, so the source is version 2 and this document is version 3; the internal stamp of 1 is kept as a source fact and named in the metadata table. | Unconfirmed (business decision pending) |
| ASM-0279 | This version is issued as Draft because no approval or document status is recorded in version 2. | Unconfirmed (business decision pending) |
| ASM-0282 | A data subject request is served by reading each owning service's contract under the Compliance role and scope, joined on the case ID from rwb-case; no new retrieval service is added. | Unconfirmed (business decision pending) |
| ASM-0284 | Version 2 of the regulatory requirements map is treated as the baseline immediately before version 3. Its issue date is written as the placeholder of Template and Rules R9 because no sheet states one, and version 3 is issued as Draft because no approval is recorded in any source of this run. | Unconfirmed (business decision pending) |
| ASM-0285 | The 32 obligations keep every cell of columns A to H word for word, and one owner service with its basis is added per obligation, taken from the controls in column F through the Ownership Map v1 and the Controls Catalog v4. | Unconfirmed (business decision pending) |
| ASM-0286 | The owner service in column I is taken only from the controls the Controls cell names. Where a reporting or outbound-file leg of an obligation belongs to another service - P9 rwb-reporting for REG-15 and P2 rwb-integration for REG-27 - that service is named in the basis column and not in the owner service column, so column I stays a direct read of the controls. | Unconfirmed (business decision pending) |
| ASM-0287 | REG-25 keeps S9 rwb-partner as its owner service because CTL-37 is the only control the row names, and the breach-notification step itself is recorded as having no owning object in the Ownership Map rather than being assigned to a service by guesswork. | Unconfirmed (business decision pending) |
| ASM-0288 | Where the Controls Catalog v4 and this map disagree on which controls answer an obligation, the Controls cell of this map is kept word for word, the difference is stated in the basis column, and the owner service follows this map's Controls cell. | Unconfirmed (business decision pending) |
| ASM-0289 | REG-02 and REG-08 keep P9 rwb-reporting as owner service, carried from CTL-39 and from the ruling recorded in the Controls Catalog v4 (ASM-B-CTRL-32-4), and the dependency on that ruling is named in the row. | Unconfirmed (business decision pending) |
| ASM-0291 | Column G Owner, the business role, and column I Owner service, the service that holds the control evidence, are both kept, and the Read me states that they are different dimensions. | Unconfirmed (business decision pending) |
| ASM-0312 | Column D keeps its stewardship owner, and the service that loads and serves the list is read from the appended 'Owning service (D-RCV-60)' and 'Owning schema (D-RCV-60)' columns; the Key sheet gains both terms. | Unconfirmed (business decision pending) |
| ASM-0380 | Version 6 is issued as Draft with no recorded approval, and the approval is carried as an open gap and this assumption. | Unconfirmed (business decision pending) |
| ASM-0387 | Version 5 is issued as Draft with no recorded approval; the per-epic status words of the source stay as they stand (E1 and E2 Confirmed, E3 to E8 Proposed). | Unconfirmed (business decision pending) |
| ASM-0395 | BOT approval under FPG 19/2560 clause 5.5 is treated as required before the Wave 1 cutover, with the submission date open, and it is carried as a gate in section 10.2 step 1 and as an open decision in section 9. | Unconfirmed (business decision pending) |
| ASM-0398 | The tracker retirement stays a team procedure run by the six team managers against the Wave 1 case list of rwb-case, with the data steward recording the fields no data product carries; no service is named as the owner of a tracker or of the retirement report. | Unconfirmed (business decision pending) |
| ASM-0399 | Version 4 is issued as Draft with no recorded approval, and the approval is carried as an open gap and this assumption. | Unconfirmed (business decision pending) |
| ASM-0401 | The owner of a service is its service code in the Ownership Map v1, with TechX as the suggested team for every service, and the run-time service owner stays open until one role is named per service. | Unconfirmed (business decision pending) |
| ASM-0402 | The tier 2 and tier 3 roles of version 2 keep serving all 19 services as one pool until the per-service role is stated, and each service's run book page is read by that pool. | Unconfirmed (business decision pending) |
| ASM-0407 | Version 3 is issued as Draft with no recorded approval, and the approval is carried as an open gap and this assumption. | Unconfirmed (business decision pending) |
| ASM-0412 | The fourteen source module names are read as the service mapping of thirteen services: squad 1 carries P1 rwb-source-data (data engine), P3 rwb-case (case and workflow), the rules component of every service (the embedded Drools kit, DP-04), P4 rwb-access, S1 rwb-valuation, S5 rwb-asset and S8 rwb-deviation; squad 2 carries P5 rwb-document, P6 rwb-comms, P7 rwb-decision, S2 rwb-treatment, S4 rwb-litigation, S6 rwb-debtsale and S7 rwb-writeoff. Per-service headcount is not derived and is left open. | Unconfirmed (business decision pending) |
| ASM-0413 | The six services with no source module (P2, P8, P9, P10, S3, S9) are left at the R9 placeholder for the squad and are assigned at the first daily review, as the Structure sheet says the split is agreed there. | Unconfirmed (business decision pending) |
| ASM-0420 | The shared Epic 2 items stay with the Collection squad as version 2 says, and are not split across the nineteen services in this version. | Unconfirmed (business decision pending) |
| ASM-0421 | Version 3 is issued as Draft because no approval is recorded for the source or for this realignment, and the run overlay of D-RCV-60 asks for a record instead of a stop. | Unconfirmed (business decision pending) |
| ASM-2169 | REQ-DRI-009 is read as the reporting requirement it describes and not as a requirement on rwb-comms: the daily agent measures are available from the P9 rwb-reporting read model with the row counts matched against the P10 source, and the notification of a cost breach is the only part of the legacy story that remains with rwb-comms. The requirement identifier and its owner are unchanged and no date is changed. | Unconfirmed (business decision pending) |
| ASM-2332 | The model version of agent INTAKE is a P10 fact that arrives inside the record; the fixtures of this story carry a synthetic model version and the criteria assert that the value is present and travels unchanged, never a particular value. | Unconfirmed (business decision pending) |
| ASM-2555 | The requirement text of RWB-E1-014, RWB-E1-029 and RWB-E1-048 is unchanged; their realignment position appears only in section 8.5, section 9 and the gap register. | Unconfirmed (business decision pending) |
| ASM-2565 | RWB-E2-023 is read as module P2 Integration from its section heading, which is the only source that places it. | Unconfirmed (business decision pending) |
| ASM-2570 | The settlement range and the floor price are read per product from versioned reference rows. Only a documented test version is used in SIT, and the production version is approved by the product head like the treatment policy. | Unconfirmed (business decision pending) |
| ASM-2571 | The offer validity of 14 days stated in the rule rows is the documented test value. The cure period, the maximum number of breaks and the queue and approval service levels are parameters with no value until DL22 and DL23 are loaded. | Unconfirmed (business decision pending) |
| ASM-2572 | Notice periods and prescription periods are read from the legal periods table that Epic 1 already holds, and the litigation step service levels are read from the service level reference data. No period is restated in this document. | Unconfirmed (business decision pending) |
| ASM-2575 | The write-off exception loop is owned by the write-off team, escalates to its team manager when the time limit passes, and is recorded as an unmapped owner until the operating model names the role. | Unconfirmed (business decision pending) |
| ASM-2576 | Enforcement after judgment is held by the enforcement owner role the rules already name, and an eviction is held by the sale officer with Legal counsel named on the case. The assignment is recorded as an assumption until the operating model names the holder. | Unconfirmed (business decision pending) |
| ASM-2577 | The non performing asset stock position is owned per case by the NPA and asset manager, and the monthly stock report goes to the head of NPA. | Unconfirmed (business decision pending) |
| ASM-2578 | The 54 percent figure is the debt sale cap in force at the release, held as a versioned policy parameter whose version label carries the basis and the period, and headroom is computed against the population the policy names. | Unconfirmed (business decision pending) |
| ASM-2579 | Buyer qualification uses the bank's existing KYC and licensing checks, with the accepted licence types and their validity held as reference data, and the debt sale officer may bar a buyer with Compliance confirming the reason. | Unconfirmed (business decision pending) |
| ASM-2580 | A retention class and a masking rule per record class and role are versioned reference data applied at creation, and a disposal that would breach a period not yet set is recorded as a decision rather than carried out. | Unconfirmed (business decision pending) |
| ASM-2582 | An autonomy level stays at its current setting until the risk owner loads a measure, a threshold and an approval level per agent and per decision as a versioned row; no step-up is taken on a threshold this document invented. | Unconfirmed (business decision pending) |
| ASM-2583 | The deceased customer capability is read as the E7 deviation flow RWB-E7-003 and is recorded in the E3 scope as delivered in E7, with the E3 program requirement served through it. | Unconfirmed (business decision pending) |
| ASM-2588 | Benefit realisation reports the eight program measures of the program requirements until the benefit model is supplied, and the report is labelled as the program measure set. | Unconfirmed (business decision pending) |
| ASM-2597 | The debt sale turnaround is measured from lot selection to award and transfer, and the 45 day target stands until a baseline is measured on the first lot. | Unconfirmed (business decision pending) |
| ASM-2601 | Agent acceptance, override rate, latency and cost are reported per agent and per decision from the agent run record, with no target until the model risk owner sets one. | Unconfirmed (business decision pending) |
| ASM-2615 | P8 payment, P9 reporting and P10 agent have no requirement section in this BRD, and their service epics appear in the delivery model with no requirement row. | Unconfirmed (business decision pending) |
| ASM-2618 | The retention class per data product and recovery table is declared here as versioned data, the archive rule table and the monthly archive run belong to rwb-document, and ACE retains ACE data. | Unconfirmed (business decision pending) |
| ASM-2619 | Role-level read access per data product is held here; field-level masking rules are held by rwb-access and applied here, and a personal field with no masking row for the role is returned masked. | Unconfirmed (business decision pending) |
| ASM-2620 | This service builds and publishes the case list rows and holds their publication status; the case list screen and its filters are served by rwb-case over those rows. | Unconfirmed (business decision pending) |
| ASM-2628 | The four-label classification in this PRD is read from the personal-data markers in the field catalogues: personal fields and the party and contact extension rows as personal data, balances, amounts, offers, debt sale and money as sensitive financial data, case, legal, collateral, documents and metadata as confidential, and no data product as public. | Unconfirmed (business decision pending) |
| ASM-2643 | Because the FSD P10 requirement table is empty, every functional requirement of this PRD is mapped to the FSD section and to the acceptance criteria it serves, and to the feature code FEAT-AGT-nn where the feature overview carries one; no FSD requirement ID is invented. | Unconfirmed (business decision pending) |
| ASM-2647 | Every target the source does not state is written with the R9 placeholder and carried as an open question; the only numeric targets stated in the source set are the 60 second agent target and the fallback rate below 10 percent, and both are carried as stated. | Unconfirmed (business decision pending) |
| ASM-2648 | The run, the guardrail result, the feedback, the sample, the evaluation and the alert are retained for the period set for them, are answerable to audit before a purge and are never removed silently; the period is written with the R9 placeholder until DL26 is answered. | Unconfirmed (business decision pending) |
| ASM-2653 | RWB-E2-028, RWB-E2-029 and RWB-E2-030 are read as the legacy story keys of the feedback, the screening rejection and the legal document pack, even though BRD Epic 2 v3 holds no requirement row for them. | Unconfirmed (business decision pending) |
| ASM-2658 | The message codes MSG-P10-001 to MSG-P10-008 are referenced with the behaviour the source states and with no invented wording; the wording is taken from the Error and Message Standard at build time, and where the source does not say which service owns a message the PRD leaves that to the screen owner. | Unconfirmed (business decision pending) |
| ASM-2660 | SCR-46 Agent monitor is described by what it shows and by the filter it applies (agent, policy version, prompt version, business date); its layout, components and states follow the Design System and Component Library and are not fixed by this PRD. | Unconfirmed (business decision pending) |
| ASM-2670 | The PRD covers the requirements rwb-integration owns (REQ-DRI-006, REQ-DRI-007, REQ-DRI-008 and REQ-DRI-013) and the one wave-2 orchestration step those requirements and the FSD carry; the consumer-side compositions assigned to the service in later wave story slices are not restated as P2 product requirements and are carried as open question Q-P2-06. | Unconfirmed (business decision pending) |
| ASM-2673 | The debt buyer tape carries only the fields that the approved sale terms and the approved mask list allow, the mask list is a reference-data row owned by Compliance, and no field-level rule is fixed by this PRD. | Unconfirmed (business decision pending) |
| ASM-2679 | The retention period of an outbound item, a delivery record, a manifest and a transmission acknowledgement is open under DL26; the PRD requires only that the record of a send, an exception and a resend outlives the retention period of the case it belongs to. | Unconfirmed (business decision pending) |
| ASM-2680 | The BRD and this PRD are treated as not yet approved; the PRD is issued as Draft with an empty approval table. | Unconfirmed (business decision pending) |
| ASM-2687 | The recovery point and recovery time objectives adopt the ACE values; the value of each is left open until DL11 is answered. | Unconfirmed (business decision pending) |
| ASM-2692 | The queue write interface for models and agents is built dark in wave 2 and switched on only when a consumer is approved. | Unconfirmed (business decision pending) |
| ASM-2694 | No retention period is stated: the case record classes are carried as DL26 open, and the PRD states the requirement and the variable, not a period. | Unconfirmed (business decision pending) |
| ASM-2695 | The three slices with no requirement row (encumbrance check, proof of delivery, committee routing) stay in the later waves as delivery items and are not given an FR in this PRD. | Unconfirmed (business decision pending) |
| ASM-2699 | rwb-access keeps identity and session, roles, permissions, scope, masking, the delegation of authority table, the access log and break-glass. The reference-data load surface, the rule package registry and its six operations, the platform smoke workflow, the case record view, the list of values and the partner identity rows are outside this service and are recorded as dependencies only. | Unconfirmed (business decision pending) |
| ASM-2701 | The masking answer names a personal field ID with a masked or clear marker and never a rendering, the client renders the masked form of the field, and a masked caller never causes a clear value to be retrieved from the ACE PII path. A personal field with no masking row for any role is masked for every role. | Unconfirmed (business decision pending) |
| ASM-2710 | The third object of REQ-ACA-006, written as 'the data lake copy', is read as 'a data product', because Architecture v5 removes the data lake and the reporting read model is built from events into rwb-reporting. Nothing else in the requirement changes. | Unconfirmed (business decision pending) |
| ASM-2711 | BRD Program v4, BRD Epic 1 v4 and BRD Epic 2 v2 are taken as the approved business baseline for this PRD even though none of them carries a status field or an approval record, so the PRD is issued as Draft with an empty approval table and the requirements approval gate stays open. | Unconfirmed (business decision pending) |
| ASM-2714 | Legal hold is a product behaviour of this service, driven by the hold that rwb-case records, and it is released in wave 4 with RWB-AD-021 even though REQ-DCM-016 is an Epic 1 Must; the retention class and the virus scan that the hold overlays are released in wave 1. | Unconfirmed (business decision pending) |
| ASM-2715 | E-discovery production and court-ready evidence are in scope of this PRD and are released in wave 2, with the discovery response target left open until Legal counsel sets one. | Unconfirmed (business decision pending) |
| ASM-2717 | The retention classes named in the FSD acceptance criteria (GENERAL05Y, LEGAL10Y, DOCTYPE-2026.11 and RET-2026.11) are read as examples taken from a reference-table version, not as approved periods; the period behind each class stays open and the retention rule table is read as the versioned table that carries it. | Unconfirmed (business decision pending) |
| ASM-2718 | The 26 extracted fields are read as the union of the per-type field definitions delivered in the signed reference load; this PRD requires the count to reconcile with 26 and the two named types to keep their four fields each, and does not enumerate the remaining four types. | Unconfirmed (business decision pending) |
| ASM-2719 | OCR, document classification and field extraction are reached through a contract owned outside this service, either as an AgentRunCompleted event or as a Temporal child run on queue rwb-document, and malware scanning is a platform security service; P5 owns the intake, the text, the confidence, the review queue, the index and the decision record that carries the versions. | Unconfirmed (business decision pending) |
| ASM-2724 | Every read of a document and of its extracted fields through this service is logged; the data lake clause of NFR-042 is not carried because no lake copy of the document store exists in the target. | Unconfirmed (business decision pending) |
| ASM-2730 | REQ-OCC-007 and REQ-OCC-008 are read as this service's contribution to the case record view and the case timeline: the notice and message block with its states and the ordered notice and message history. The view and the timeline are rwb-case's product. | Unconfirmed (business decision pending) |
| ASM-2735 | The volume test is sized on the document volume of about 860,000 in 2027 as the upper bound for letters and on the interaction volume for messages, until the business lead states the notice and message counts. | Unconfirmed (business decision pending) |
| ASM-2736 | A retention class is declared on the notice record, the template version and the merge-field catalog as versioned data; the periods stay open under DL26 and rwb-document applies the archive and disposal. | Unconfirmed (business decision pending) |
| ASM-2738 | The Legal approval is recorded on the template version as a decision record written through rwb-decision, and the approval of a demand or recall notice is taken on the generated notice through the approval workflow. | Unconfirmed (business decision pending) |
| ASM-2739 | The seven features that v5 places elsewhere (payment matching and the plan-payment-missed event, the steering dashboard, partner identities, custody movement, the legal or audit document request and retention on closure) are kept in the source with their identifiers and are not built in this service. | Unconfirmed (business decision pending) |
| ASM-2743 | This PRD is issued as Draft with an empty approval table because the business requirements documents it rests on are Draft in this run; the Product Owner and the FDA approve it when they approve the business requirements. | Unconfirmed (business decision pending) |
| ASM-2750 | Notice generation, letter template management, the template catalog with merge fields and proof of delivery from WIN belong to rwb-comms, with rwb-document for the document and rwb-integration for the WIN file. This service keeps only the approval of a D7.1 notice and the recording of the template version on the approval. | Unconfirmed (business decision pending) |
| ASM-2752 | The delegation of authority table is rwb-access's. This service reads a limit through the access contract at the moment of the decision, records the delegation row ID and the limit version on the approval, and loads and approves no limit file. | Unconfirmed (business decision pending) |
| ASM-2754 | A retention class is required for every decision record class and every ledger entry class, and the periods themselves stay open under DL26. The service runs no archive of its own and keeps the seal for the class period once set. | Unconfirmed (business decision pending) |
| ASM-2758 | Committee members present and their votes are carried in the approval terms structure until the field list is agreed, and the decision-log entry records the committee's outcome and its approver. | Unconfirmed (business decision pending) |
| ASM-2766 | The posting file holds one line per posting with case, account key, entry type, amount, value date, business date and posting reference, is delivered by rwb-integration with a manifest that states the count and a checksum, and has no personal data on any line. | Unconfirmed (business decision pending) |
| ASM-2768 | A payment reversal is out of scope for this release; the behaviour is specified nowhere in the FSD and is carried as an open question, and the case reopens only through rwb-case when a reversal is reported to it. | Unconfirmed (business decision pending) |
| ASM-2769 | Fee rates, caps and bases are versioned rows in a fee table owned by Finance, read at run time; until the table and its owner are named, no fee is calculated by the service. | Unconfirmed (business decision pending) |
| ASM-2772 | The order in which a receipt is applied to the balance is a versioned row set with an owner and a valid-from date; the sequence itself is a Finance decision and is not written here. | Unconfirmed (business decision pending) |
| ASM-2774 | The measure 'receipts matched the same day' is read from the decision log per match, counted on the business date of the run against the receipt date, until the product owner sets a baseline, a target and the definition. | Unconfirmed (business decision pending) |
| ASM-2778 | This document stays at status Draft with an empty approval table; the missing Product Owner and FDA approval is carried as an assumption, not as an answer. | Unconfirmed (business decision pending) |
| ASM-2785 | This PRD stays in Draft and records no approval. | Unconfirmed (business decision pending) |
| ASM-2787 | The service is created in wave 1 and serves EP02, EP06 and EP08 from the same read model. | Unconfirmed (business decision pending) |
| ASM-2793 | The reconciliation result and the break rows are read from rwb-source-data's contract, and the break view and its closure live in this service. | Unconfirmed (business decision pending) |
| ASM-2797 | Every reporting entity declares a retention class now and takes its period from DL26 when it is set. | Unconfirmed (business decision pending) |
| ASM-2798 | Benefit realisation reports each measured value against the frozen baseline and states where the benefit model sets no measure or no target. | Unconfirmed (business decision pending) |
| ASM-2801 | Agent acceptance and override are counted from the decision record, which carries the agent and prompt version, the recommendation, the approval and the outcome. | Unconfirmed (business decision pending) |
| ASM-2803 | Agent acceptance and override are published per agent and version with no threshold, and an agent with no recommendations shows 'No runs'. | Unconfirmed (business decision pending) |
| ASM-2808 | There is no predecessor PRD in the PLT family, so this document is version 1. | Unconfirmed (business decision pending) |
| ASM-2819 | A target the source does not state is held open with the placeholder and is never invented: the recovery point and time, the namespace quotas, the key rotation period, the retention of the platform rows and telemetry, and the stored idempotent answer period. | Unconfirmed (business decision pending) |
| ASM-2821 | Telemetry carries identifiers and facts only: party identifiers, names, addresses and document content are scrubbed before export, and the field list is open under DL26. | Unconfirmed (business decision pending) |
| ASM-2840 | The valuation record, the route decision and the route agent output carry a classification from the working labels of this document and a retention class whose period stays open under DL26. | Unconfirmed (business decision pending) |
| ASM-2841 | This document stays at status Draft with an empty approval table, and the missing requirements approval is carried as an assumption. | Unconfirmed (business decision pending) |
| ASM-2864 | The treatment, the agreements and the plan timers carry a classification from the working labels of this document (SENSITIVE_FINANCIAL for the terms and the agreements, CONFIDENTIAL for the references), and the retention period is stated as open. | Unconfirmed (business decision pending) |
| ASM-2867 | This document stays at status Draft with an empty approval table, and the missing requirements approval is treated as an assumption rather than as an answer. | Unconfirmed (business decision pending) |
| ASM-2882 | The insurance claim is delivered as the Must behaviour of BR-025 and traced through REQ-S3-002 for the claim status it records on the case, and a program requirement for the collateral event is raised when the program requirement set is next versioned. | Unconfirmed (business decision pending) |
| ASM-2887 | The claim is classified [SENSITIVE_FINANCIAL] and the guarantor party fields [PII], the periods are held as reference data by record class, and no period is stated in this document. | Unconfirmed (business decision pending) |
| ASM-2892 | The volume target of this service is the program case volume it inherits and the number of claims a month, of guarantors a case and of notices a demand are carried as open, with no count recomputed here. | Unconfirmed (business decision pending) |
| ASM-2908 | REQ-S4-009 is carried under BR-034, the requirement that owns the statutory clock, through FR-S4-051 and FR-S4-052; BR-038 and BR-042 are traced from the FSD features FEAT-LIT-10 and FEAT-LIT-17 to FEAT-LIT-21 and the RWB-E5 story keys. | Unconfirmed (business decision pending) |
| ASM-2928 | The route recommendation and the price proposal are decisions of the disposal rule set; where an agent proposes, it is reached only through the rwb-agent contract, waits at most 60 s, falls back to the rule result and leaves a run record. | Unconfirmed (business decision pending) |
| ASM-2930 | The stock balance owner is the NPA and asset manager role held as versioned reference data until Q-009 answers, and the monthly balance is refused where no owner role is in force. | Unconfirmed (business decision pending) |
| ASM-2931 | Every floor limit and approval level is read at run time from the versioned delegation table of rwb-access, the three amounts and the three percentages of the design slide are carried as stated, and the direction of the test is held open until DL18 and Q-001 answer. | Unconfirmed (business decision pending) |
| ASM-2932 | Sale prices, values, floors and cost amounts are [SENSITIVE_FINANCIAL], bidder and customer identity are [PII], vendor and partner data are [CONFIDENTIAL], and the retention periods stay open. | Unconfirmed (business decision pending) |
| ASM-2933 | This document stays at status Draft with an empty approval table; the missing Product Owner and FDA approval is carried as an assumption and not as an answer. | Unconfirmed (business decision pending) |
| ASM-2937 | The service is sized on the case volume and the NPA book of NFR-001 until the asset, round and holding cost volumes are given, and the missing volume blocks the performance test only. | Unconfirmed (business decision pending) |
| ASM-2948 | The KYC result, the licence expiry and the panel status of a buyer are held as data on the buyer record, the panel is read through the S9 contract, and the evidence the officer accepted is recorded with the admission. | Unconfirmed (business decision pending) |
| ASM-2949 | The debt sale cap, its denominator and its period are one versioned reference-data row owned by the Head of Asset Liquidity, and the version applied is recorded at the selection, the award and the headroom report. | Unconfirmed (business decision pending) |
| ASM-2950 | The lot approval and the award are routed through P7's approval child on the P4 delegation table, with the secured and unsecured bands of design slide 22 held as versioned reference data and the level applied and the approving role recorded on the award. | Unconfirmed (business decision pending) |
| ASM-2958 | borrower_code and account_key are personal data in use: they are masked on every screen and on the tape and the transfer file by role, and the is_personal flag is corrected in the next version of the Logical Data Model and the physical schema. | Unconfirmed (business decision pending) |
| ASM-2962 | Every record this service holds carries a data classification and a retention class, the periods are held as reference data from DL26, and the tape and the transfer file inherit the class of the record they are derived from. | Unconfirmed (business decision pending) |
| ASM-2963 | The put-back claim window, the buyer remediation window and the settlement term are versioned reference-data values with valid-from dates, held from DL22, and the value in force at the business date of the lot is applied and recorded. | Unconfirmed (business decision pending) |
| ASM-2980 | The write-off exception loop is owned by the write-off team role until a named owner is decided, and it carries one time limit as a data row rather than a code constant. | Unconfirmed (business decision pending) |
| ASM-2981 | No write-off cap value, basis or period is asserted, and the population is reported against the cap only once the cap exists; the committee limit of R-WO-11 and R-WO-12 is the only limit this release enforces. | Unconfirmed (business decision pending) |
| ASM-2982 | The committee approval is taken through the approval workflow on rwb-decision, the limit is read from the delegation table at run time, and the level applied and the approver role are recorded; the level values are loaded from the regulation under DL18 and the committee composition is taken as open under Q-001. | Unconfirmed (business decision pending) |
| ASM-2984 | A retention class and a retention period are held as data on every document and every record this service closes on, the closure is held when a class is missing, and the periods themselves stay open under DL26 and Q-012. | Unconfirmed (business decision pending) |
| ASM-2991 | This version is Draft and its approval table stays empty: no Product Owner decision and no FDA decision exists for the BRD or the FSD this PRD is built from, so no approval is claimed. | Unconfirmed (business decision pending) |
| ASM-3003 | The deceased customer slice lands twice on purpose: the contact stop, the heir and estate notification and the insurance claim path as the E3 slice in wave 2, and the full X3 flow with its approver and return point in wave 4. | Unconfirmed (business decision pending) |
| ASM-3005 | The deviation service level, the ten working day escalation and the thirty day skip trace window are versioned reference data read at run time; no number is asserted in this document. | Unconfirmed (business decision pending) |
| ASM-3006 | The confidence threshold that sends a flag to a person and the autonomy policy that permits L1 on a segment are held as versioned reference data by rwb-agent and rwb-decision; this service reads them and asserts no value. | Unconfirmed (business decision pending) |
| ASM-3007 | The deviation record, the screening run and the breach record are confidential records attached to a case; the staff identifier of the handler is confidential rather than personal customer data, and no retention period is stated. | Unconfirmed (business decision pending) |
| ASM-3034 | The three partner tables carry the Workbench record class, and the periods stay open until DL26 answers; the partner, its instructions and its results stay readable after an exit. | Unconfirmed (business decision pending) |
| ASM-3036 | The four reused messages keep their published wording, and the module's own refusals, holds, differences and breach notices are authored with the story from the Error and Message Standard in Thai and English. | Unconfirmed (business decision pending) |
| ASM-3054 | Until the recovery point objective is confirmed, no RPO value is tested. NFR-022 stays Open under DL11, the recovery test is run against the ACE platform tier, and the section R9 placeholder stands in its owning service cell. | Unconfirmed (business decision pending) |
| ASM-3055 | Until the recovery time objective is confirmed, no RTO value is tested. NFR-023 stays Open under DL11, the recovery test is run against the ACE platform tier, and the section R9 placeholder stands in its owning service cell. | Unconfirmed (business decision pending) |
| ASM-3058 | Where the concurrency figures differ, Architecture v5 slide 48 is used for the load test: 414 concurrent staff, 48 concurrent partners and about 21 requests a second. The requirement text keeps its own figures, including the named-user total of 1,234. | Unconfirmed (business decision pending) |
| ASM-3141 | The former owner is represented by the sale officer acting on the case, and enters this story only as a party key the owner's contract answers. No customer or borrower role, no customer screen and no external edge is added, and the buy-back is signed by the approver the limit names and not by the former owner inside the Workbench. | Unconfirmed (business decision pending) |
| ASM-3200 | Version 4 carries the version 3 approval statuses unchanged in section 9, gives the four replaced decision rows the Proposed status of the record that replaces them, and is issued as Draft. | Unconfirmed (business decision pending) |
| ASM-3277 | Masking is applied twice and both controls stay: rwb-source-data masks in v_ace_customer and v_ace_contact and in its contract, and every service re-applies the masking_rule rows of rwb-access at its own API before the response leaves. | Unconfirmed (business decision pending) |
| ASM-3292 | The decision log is measured twice: the local decision record of each service in its own schema, and the central ledger of P7 rwb-decision that collects rwb.decision-record.v1 within 5 minutes and runs the chain check as JOB-14 at 02:00. | Unconfirmed (business decision pending) |
| ASM-3293 | The six recipient names of version 3 are kept character for character and read as role names, not as persons; only RW-PLATADM and RW-COE appear in the source as role codes, and no mapping of the other names to a role code is invented here. | Unconfirmed (business decision pending) |
| ASM-3296 | The hash chain alert is raised on the local chain of each service and once on the central ledger of P7 rwb-decision, and a break is attributed to the service whose chain fails, with the daily check as JOB-14 at 02:00. | Unconfirmed (business decision pending) |
| ASM-3307 | No recovery point objective and no recovery time objective is set for any store or any service. Every store row and every service statement carries the placeholder 'Not specified in the source documents (CG-B-TECH-11-2; ASM-B-TECH-11-2)'; no tier, no number of minutes and no number of hours is taken from the proposed tiers that Architecture v5 mentions. | Unconfirmed (business decision pending) |
| ASM-3321 | The file name gives the version of the family and the metadata table gives the document's own issue number. The source is therefore version 2 of the family and version 1 of its own table, and this document is version 3. The source values are kept in a 'Source version' row as 1, 28 October 2026. | Unconfirmed (business decision pending) |
| ASM-3328 | Every retention period of the source is kept as written under DL26. Where each period is held and which job enforces it is left open: the retention tables of the map are rwb-document (P5) and JOB-17 is document retention, so the ledger and access-log periods need their own rows, owned by P7, P1 and P4. | Unconfirmed (business decision pending) |
| ASM-3330 | The approver of a decision is stored as an identifier, never as a name. The identifier is masked in every export under the masking rows of rwb-access and every read of the field is recorded in the PII log. | Unconfirmed (business decision pending) |
| ASM-3355 | DL10 is read as answered on 5 November 2026 with answer A, 'Thai field names'. The source row and its fallback answer are kept word for word, section 6.1 records the answer, and this document adds no Thai wording. | Unconfirmed (business decision pending) |
| ASM-3356 | Templates and merge fields are owned by P6 rwb-comms in rwb_comms, following Architecture v5 slide 41 and the Ownership Map v1. The DL28 answer of 13 November 2026, which gives them to the document module, is recorded as a conflict and is not applied. | Unconfirmed (business decision pending) |
| ASM-3358 | The verified contact point and its consent state are held by P1 rwb-source-data in contact_point_ext and are read and maintained through a P1 contract. The P6 screen maintains them through that contract and never writes rwb_source_data directly. | Unconfirmed (business decision pending) |
| ASM-3359 | A contact stop is read as X1 to X3, following the Temporal and Drools design, so a death (X3) holds messages and letters except statutory notices where the law requires service. The wider reading is applied and R-LIT-05 is flagged for correction. | Unconfirmed (business decision pending) |
| ASM-3364 | Contact times and frequency are reference data of P3 rwb-case, read through the reference-data contract (H RWB-PLT-E1043-CON; C RWB-P3-E1043-CON), and are not held by P4. Roles and DoA stay with P4. | Unconfirmed (business decision pending) |
| ASM-3365 | The Compliance approval of customer wording is recorded as a second approval of P7 rwb-decision with the template as its source, while approved_by_legal, approved_by and approved_at on the template row record the Legal approval that POST /admin/templates/{templateId}/approve writes. | Unconfirmed (business decision pending) |
| ASM-3402 | Version 3 carries Status Draft in the metadata table, states in the opening note that no approval is recorded, and is issued without an approval round. | Unconfirmed (business decision pending) |
| ASM-3417 | The accessibility gate 'Each screen' is read as every screen of every service, reached through that service's REST base, and no screen list is added because no source names one. | Unconfirmed (business decision pending) |
| ASM-3420 | Until NFR-022 and NFR-023 are set under DL11, every restore test runs against the ACE recovery objectives recorded under DL11 and is re-run when a target is set; NFR-071 stays Open under DL27. | Unconfirmed (business decision pending) |
| ASM-3428 | rwb-access (P4) holds the approved masking version as masking_rule; rwb-source-data (P1) applies the mask at the 30 recovery.v_ace_* views; the service that owns a personal field applies display masking at its API under the same version. | Unconfirmed (business decision pending) |
| ASM-3436 | Every owner named in the document is read from the Ownership Map v1: the 19 services of sheet Services with their wave, schema and REST base, and the owner team of each kind of work from R5.3. The roles of the Checked by column and of section 5 stay as the approvers of the gate itself. | Unconfirmed (business decision pending) |
| ASM-3443 | Contract publication is owned by the owning service team from its contract story and changes only through a new published version after a four-eyes review; the boundary test is owned by the owning service team with the DevOps team on the golden pipeline and changes only with platform approval. | Unconfirmed (business decision pending) |
| ASM-3829 | A field whose is_personal is true needs at least one masking_rule row at the masking version in force, and a personal field with no row is masked for every role and reported as a coverage failure of the load; the count of personal fields among the 1,366 is not stated by any source, so the register reports the count it finds and no criterion asserts a fixed number. | Unconfirmed (business decision pending) |
| ASM-4719 | Both stories stay at Status Draft (realignment v1) and the missing approval of the FSD S5 and the TSD S5 is recorded rather than awaited. | Unconfirmed (business decision pending) |
| ASM-5570 | The INT-19 extract and the data lake are removed, and rwb-reporting publishes the measure rows and events the data set reads. | Unconfirmed (business decision pending) |
| ASM-5578 | The primary service of a story is the primary the plan gives its legacy key, and RWB-E2-023, which has no plan row, takes its primary service from the source module line, its wave from the EP02 W-MAP rule and its release from the catalogue rows of the same epic. | Unconfirmed (business decision pending) |
| ASM-5580 | The story set of this document is the 42 stories of the source version, which is one more than the 41 plan keys because RWB-E2-023 is in the source and not in the plan. | Unconfirmed (business decision pending) |
| ASM-5614 | A requirement named in a PRD as an upstream ID but carried by no functional requirement is flagged, not mapped to a nearby FR. | Unconfirmed (business decision pending) |
| ASM-5650 | The five Wave 0 dependencies of Architecture v5 slide 39 stay on the Dependency classes sheet exactly as slide 39 states them, and no new DEP ID is created in this version. | Unconfirmed (business decision pending) |
| ASM-5657 | Version 4 is issued as Draft with no recorded approval, and the approval is carried as an open row. | Unconfirmed (business decision pending) |
| ASM-5685 | The regulatory, audit, control and report rows are copied unchanged from their workbooks, with the owner service the workbook names | Unconfirmed (business decision pending) |
| ASM-5686 | A measure value of To set is copied as written and means the value is not set | Unconfirmed (business decision pending) |

## 8. Lint findings on the staged stories

None.

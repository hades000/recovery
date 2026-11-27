# RWB-PLT-LIB Shared libraries - review pack, part 1 of 4 (RWB-PLT-E1027-APP to RWB-PLT-E1037-APP)

Decision: D-RCV-60. Date: 26 November 2026. Status: Draft (directive resolutions). Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

Directive run result for this service: every gap and assumption was resolved with the recommended resolution, except business decisions. Review this pack, then the staged story files it lists. Row IDs (ruling R-, item GAP-/ASM-/CG-, CDC-) match the master registers in 23 Document Gaps.

## 1. Summary

| Measure | Count |
|---|---|
| Stories | 3 |
| Resolved in the stories | 49 |
| Cross-document (pending in another document) | 203 |
| Not applied (value not in the sources) | 17 |
| Open business decisions | 22 |
| Register gaps linked | 177 |
| Unconfirmed assumptions | 0 |
| Lint findings | 0 |

## 2. Stories (staged next version)

| Story | Resolved | Cross-document | Not applied | File |
|---|---|---|---|---|
| RWB-PLT-E1027-APP | 10 | 31 | 1 | 04 User stories/Recovery Workbench Service Story Files v2/RWB-PLT-LIB Shared libraries/RWB PLT E1027 APP Decision log writer v1 v2.md |
| RWB-PLT-E1027-CON | 28 | 131 | 9 | 04 User stories/Recovery Workbench Service Story Files v2/RWB-PLT-LIB Shared libraries/RWB PLT E1027 CON Decision log writer v1 - contract v2.md |
| RWB-PLT-E1037-APP | 11 | 40 | 7 | 04 User stories/Recovery Workbench Service Story Files v2/RWB-PLT-LIB Shared libraries/RWB PLT E1037 APP Role to permission matrix as data and PDPA field masking by role v2.md |

## 3. Open business decisions (not resolved; owner decides)

| Story | Ruling | Item | Kind | Owner role | Title | Proposed resolution |
|---|---|---|---|---|---|---|
| RWB-PLT-E1027-APP | R-11584 | CG-ALL-1293 | Script gap | Compliance | Fields classed as personal data where the story says none is carried | State the handling rule of Data Classification v5 for each field (codec, masking) or drop the field. |
| RWB-PLT-E1037-APP | R-11594 | CG-ALL-1308 | Script gap | Compliance | Fields classed as personal data where the story says none is carried | State the handling rule of Data Classification v5 for each field (codec, masking) or drop the field. |
| RWB-ITG-E1011-ITG, RWB-PLT-N001-APP, RWB-PLT-N001-CON, RWB-PLT-E1027-CON, RWB-PLT-E1042-CON, RWB-PLT-E1043-CON, RWB-PLT-E1047-CON, RWB-PLT-E1044-CON, RWB-PLT-E1071-CON, RWB-P1-E1011-APP, RWB-P1-E1011-CON, RWB-P1-E1011-OPS, RWB-P3-E1011-APP, RWB-P3-E1042-CON, RWB-P3-E1043-CON, RWB-P6-E1011-APP, RWB-S5-E1011-APP | R-21929 | GAP-2972 | Register gap | TechX and the data steward and data product owner | RWB-S5-E1011-APP: the asset slice of RWB-E1-011 has no source for its dependency lists, its ACE-side read, its quality objects, its rights, its run cadence and the owning row of the asset table, and the data-lake and Power BI target of the legacy key is removed | Confirm at the wave-1 design gate: the platform release train as the source of the seven platform CONs; the rwb-source-data contract as the only ACE-side read, with the FSD S5 view names read as the product behind it; the three quality tables, check names and read operations as the service design; the two quality reads in Platform administration right R; the asset table as an S5 object read in rwb_asset; and a daily Schedule with a cron and alert groups set as configuration. |
| RWB-ITG-E1017-ITG, RWB-PLT-N001-APP, RWB-PLT-N001-CON, RWB-PLT-E1027-CON, RWB-PLT-E1043-CON, RWB-PLT-E1044-CON, RWB-PLT-TE012-APP, RWB-PLT-E1071-CON, RWB-P1-E1017-APP, RWB-P1-E1017-CON, RWB-P1-E1017-OPS, RWB-P5-AD021-CON, RWB-P5-E1017-APP, RWB-P7-E1017-APP | R-21974 | GAP-1029 | Register gap | Solution architect, with the Compliance and PDPA officer and the platform storage owner | The P5 retention slice has no source value for its retention periods, its document age basis, its retention-load and run-read paths, its archive container name and its login, and the three contracts it consumes at run time are not in its contract-dependency list | Build the P5 slice on the recorded defaults: RET-2026.11 at 24 months for DP10 documents on created_at with end action ARCHIVE until Compliance supplies the bank schedule (DL26); the shared retention contract shape of RWB-P5-AD021-CON for the retention-class and document-retention reads, with the four admin operations on /api/recovery/document/v1; the write-once container rwb-docs-archive of RWB-PLT-TE012-APP with a manifest of row count and SHA-256 per file; the phrase 'the rwb-document login (DP-02)'; and the P3 case, P3 reference-data and P7 decision-record contracts named in 12.2 and 12.8 with their fakes. When Compliance supplies the schedule, load it as a new rule version with no code change; when the platform and contract owners publish, add the five H rows and the three consumed contracts to the plan, re-run the dependency check and swap each fake for the real contract in the same iteration. |
| RWB-ITG-E1027-ITG, RWB-ITG-E1037-ITG, RWB-PLT-E1027-APP, RWB-PLT-E1027-CON, RWB-PLT-E1037-APP, RWB-PLT-E1037-CON, RWB-P4-E1037-APP, RWB-P4-E1037-CON, RWB-P7-E1027-APP, RWB-P7-E1027-CON | R-22037 | GAP-2073 | Register gap | Service owner P7 rwb-decision with P4 rwb-access and Compliance | The approver identifier is personal data under a rule that forbids personal data in records | Store the identifier, never a name; mask it in every export under the masking rows of rwb-access (P4) and record the read in the PII log. The protection of the column itself is a decision for Compliance and Information Security. |
| RWB-ITG-E1037-ITG, RWB-PLT-E1037-APP, RWB-PLT-E1037-CON, RWB-P4-AD004-APP, RWB-P4-AD004-CON, RWB-P4-E1037-APP, RWB-P4-E1037-CON | R-22094 | GAP-1575 | Register gap | Compliance with the solution architect | The personal field list the masking policy must cover and the content of a masking version are not enumerated in any source | Produce the personal field register with its field IDs and its masked form per data type, the per-role unmasked list and a masking version label that names the register it belongs to, as the seed of the masking policy, and answer DL26 for it, so FR-P4-016 and FR-P4-017 are testable beyond the five fields the FSD names. |
| RWB-ITG-E1037-ITG, RWB-PLT-E1037-APP, RWB-PLT-E1037-CON, RWB-P4-E1037-APP, RWB-P4-E1037-CON | R-22104 | GAP-2037 | Register gap | Architecture with Compliance | Two sources disagree on who applies the mask: rwb-source-data or each service | Both controls are kept and written as defence in depth: rwb-source-data masks in the view and in its contract, and each service re-applies the masking_rule rows of rwb-access before the response leaves. The story RWB-P4-E1037-APP owns the profile; the P1 story owns the view mask. |
| RWB-ITG-E1037-ITG, RWB-PLT-E1037-APP, RWB-PLT-E1037-CON, RWB-P4-E1037-APP, RWB-P4-E1037-CON | R-22105 | GAP-2136 | Register gap | Compliance | The plan does not say which service applies the mask once the masking rules are rwb-access data | rwb-access holds the approved masking version; rwb-source-data applies the mask at the 30 views; display masking at the API is applied by the service that owns the field, under the same version. |
| RWB-PLT-N001-APP, RWB-PLT-N001-CON, RWB-PLT-E1027-CON, RWB-PLT-E1072-CON, RWB-PLT-TE006-CON, RWB-PLT-E1071-CON, RWB-S7-E6020-APP, RWB-S7-E6020-CON | R-23236 | GAP-3031 | Register gap | Solution architect; business lead | RWB-S7-E6020-APP: the review date has no property, field ID, column or list, the legacy timer table is not S7's, R-WO-17's owner conflicts with the FSD role and the permission table, the plan's C row is empty while the step consumes four contracts, DP-04, DP-09 and DP-10 are absent, and no source publishes a rule, a message or a state for a date in the past or a second decision at DEFERRED | Keep the plan's H, C, I and X rows as they stand; carry the review date as an additive request property recorded in the decision record and the case move, with no column and no field ID until the business lead and rwb-case confirm them; set the review timer as a durable workflow timer and let rwb-case own the timer row; map R-WO-17's owner to the roles that hold right A for the act and to the write-off team for the return; declare the four consumed rows in sections 12.2 and 12.8 and record the absent DP-04, DP-09 and DP-10 rows; leave a second decision at DEFERRED and a past review date unpublished and tracked |
| RWB-PLT-N001-APP, RWB-PLT-N001-CON, RWB-PLT-E1027-CON, RWB-PLT-E1072-CON, RWB-PLT-TE006-CON, RWB-S7-E6019-APP, RWB-S7-E6019-CON | R-23240 | GAP-3029 | Register gap | Solution architect; business lead | RWB-S7-E6019-APP: the reject reason and the decision code have no field, column or list, R-WO-16's owner conflicts with the FSD role and the permission table, the plan's C row is empty while the step consumes three contracts, DP-04 and DP-09 are absent, and no published row moves a case out of RETURNED_TO_PURSUE | Keep the plan's H, C, I and X rows as they stand; record the reason and the decision code as request and record inputs with a placeholder until the business lead confirms them; map R-WO-16's owner to the four roles that hold right A in TSD S7 T6.1; declare the three consumed rows in sections 12.2 and 12.8 and record the absent DP-04 and DP-09 rows; leave the onward path of RETURNED_TO_PURSUE to the case owner and raise it in the next planning cut; keep committee_date and every other write_off column out of the reject slice |
| RWB-PLT-N001-APP, RWB-PLT-N001-CON, RWB-PLT-E1027-CON, RWB-PLT-E1072-CON, RWB-PLT-TE006-CON, RWB-S9-E6034-APP, RWB-S9-E6034-CON | R-23241 | GAP-3117 | Register gap | Solution architect; business lead; access owner in rwb-access | RWB-S9-E6034-APP: the legacy story names two read endpoints and no operation that places the account, partner_instruction carries no rule-version or decision column, S9 owns no route set so the placement rule is only expressible as the D9 rows R-WO-29 to R-WO-32, the legacy permission table gives the Partner portal right R while the issue needs C and the FSD also-uses role has no matrix row, both screens are list states with no placement form, the plan C row is empty while the case and the rule package are consumed, DP-04 and DP-09 are absent, the EV-20 consumer set and payload are not published, and no requirement row traces to FEAT-PRM-06 | Keep the plan H, C, I and X rows as they stand; issue the placement through API-S9-002 and never through a new path; record the rule version and the picked agency on the local decision record and add no column to partner_instruction; read the placement rows from rwb-decision as data and record the absent DP-04 rows; read the case on the rwb-case contract and record the absent C rows; authorise the issue on the Partner portal right C the matrix gives and record the legacy right R and the missing also-uses row as conflicts; serve the placement from the list state of SCR-35 through the composite route and carry the form as a placeholder; publish EV-20 with IDs only and record the absent DP-09 row; let the trace rest on the legacy key and the feature row until the E6 BRD and the PRD publish a requirement |
| RWB-PLT-N001-APP, RWB-PLT-N001-CON, RWB-PLT-E1027-CON, RWB-PLT-E1072-CON, RWB-S6-E6005-APP, RWB-S6-E6012-APP | R-23244 | GAP-3015 | Register gap | Solution architect with the owners of rwb-case (P3), rwb-decision (P7), rwb-access (P4) and rwb-source-data (P1), and the business owner of the debt sale cap | RWB-S6-E6012-APP: the cap slice has no plan row for the five consumed contracts, no cap parameter row, no cap route rule, no published trigger, no headroom column and no service contract baseline | Publish the five consumed operations with their fake; add C rows for rwb-case, rwb-decision, rwb-access and rwb-source-data; add the DP-04, DP-06, DP-07, DP-08 and DP-09 rows the tables need; name the cap row, its version, its basis and its owner; publish one route rule for the cap or confirm that R-DS-19 and R-DS-23 are its only test and which story owns them; publish the trigger or confirm the call from the lot build and award steps; add the cap-position and headroom fields or confirm the decision record as their only home; create the service contract baseline for this legacy key; and carry REQ-S6-001 and BR-050 in the plan |
| RWB-PLT-N001-APP, RWB-PLT-N001-CON, RWB-PLT-E1027-CON, RWB-S8-E7009-APP, RWB-S8-E7009-CON | R-23272 | GAP-3068 | Register gap | Solution architect; business lead; access owner in rwb-access | RWB-S8-E7009-APP: neither deviation nor any other owned table carries a complaint or contact reference, no published rule row expresses the match, no requirement row traces to FEAT-DVF-09, the Conduct and QA officer holds R only while the feature needs U, the plan's C row is empty while two contracts are consumed, DP-04, DP-05, DP-09 and DP-18 are absent, and no event carries the match to rwb-reporting | Keep the plan's H, C, I and X rows as they stand; carry the complaint and contact references and the match outcome as request inputs recorded on the local decision record until the business lead confirms their names, formats and value set; declare the two consumed rows in sections 12.2 and 12.8 and record the absent DP-04, DP-05, DP-09 and DP-18 rows; read the contact through rwb-source-data as the connection matrix gives it and never through EFS; authorise the match on the case-record right U the permission table gives and record the matrix row as the conflict; let the trace rest on the legacy key and the feature row until the E7 BRD and the PRD publish a requirement; leave the conduct measure on the decision-record ledger until an event exists |
| RWB-ITG-E1008-ITG, RWB-ITG-E1027-ITG, RWB-PLT-E1027-APP, RWB-PLT-E1027-CON, RWB-P4-E1008-APP, RWB-P7-E1008-APP, RWB-P7-E1008-CON, RWB-P7-E1008-DB, RWB-P7-E1008-OPS, RWB-P7-E1027-APP, RWB-P7-E1027-CON | R-28460 | GAP-2067 | Register gap | Document owner of the audit and logging design | The source reads version 1 in its metadata table and v2 in its file name | Take the file name as the family version, so this document becomes version 3, and keep the source values in a 'Source version' row: 1, 28 October 2026. The change log carries both readings. |
| RWB-ITG-E1037-ITG, RWB-PLT-E1037-APP, RWB-PLT-E1037-CON, RWB-P4-E1037-APP, RWB-P4-E1037-CON | R-28578 | GAP-0162 | Register gap | Product head (Mortgage, HP, SSME) | The DoA limit amounts are not in this document | v5 names the owner (P4), the table (delegation_limit) and the two operations that serve it; the amounts stay in the Delegation of Authority Matrix and the DoA rule package and no amount is copied into this document. |
| RWB-ITG-E1037-ITG, RWB-PLT-E1037-APP, RWB-PLT-E1037-CON, RWB-P4-E1037-APP, RWB-P4-E1037-CON | R-28579 | GAP-0163 | Register gap | Compliance and PDPA officer | The masking rules per role, area and field group are not in this document | v5 names P4 as owner of masking_rule and GET /masking-policies as the contract; the rule values stay with Compliance and are loaded as a versioned reference data set. |
| RWB-ITG-E1037-ITG, RWB-PLT-E1037-APP, RWB-PLT-E1037-CON, RWB-P4-E1037-APP, RWB-P4-E1037-CON | R-28585 | GAP-2048 | Register gap | P4 rwb-access with Compliance | The alert recipient roles of version 3 are not mapped to role codes in rwb-access | The six recipient names are kept as they are and read as role names; the role codes are settled with the rwb-access role model before the per-service alert rules are built, and no code is invented here. |
| RWB-ITG-E1037-ITG, RWB-PLT-E1037-APP, RWB-PLT-E1037-CON, RWB-P4-E1037-APP, RWB-P4-E1037-CON, RWB-P4-E1038-APP | R-28587 | GAP-1579 | Register gap | Solution architect with Risk | No performance target covers the authorise answer, although every request passes one, and the nearest targets belong to other objects | Set one target for the authorise answer at the busiest hour, with the cache hit and the miss stated separately, and record it under DL11 beside the screen and rule-evaluation targets, so NFR-P4-001 becomes a testable number. |
| RWB-ITG-E2036-ITG, RWB-PLT-E1027-CON, RWB-P2-E2036-APP, RWB-P2-E2036-CON, RWB-P3-E2036-APP, RWB-P4-AD007-APP, RWB-P4-E2036-APP, RWB-P7-E2036-APP, RWB-S8-E2036-APP | R-28854 | GAP-0961 | Register gap | Internal audit | rwb-access queue-write authority: the decision code of the access entry for a placement admission and the entry fields beyond the standard record columns are fixed by no source | Use AC-READ for an admission and AC-DENY for a refusal, keep D6 for the adapter's own admission record where RWB-P2-E2036-CON already uses it, and leave the column set to RWB-PLT-E1027-CON; confirm with Internal audit at the access-log story (RWB-P4-AD007-APP) that a placement admission reads as an access entry and not as a business decision. |
| RWB-ITG-E1008-ITG, RWB-ITG-E1023-ITG, RWB-ITG-E1025-ITG, RWB-ITG-E1031-ITG, RWB-ITG-E1037-ITG, RWB-ITG-E1050-ITG, RWB-ITG-E1054-ITG, RWB-ITG-E1057-ITG, RWB-ITG-TE004-ITG, RWB-ITG-E2003-ITG, RWB-ITG-E2016-ITG, RWB-ITG-E2024-ITG, RWB-ITG-E2025-ITG, RWB-ITG-E2026-ITG, RWB-ITG-E2034-ITG, RWB-ITG-E6025-ITG, RWB-PLT-E1037-APP, RWB-PLT-E1037-CON, RWB-PLT-E1042-APP, RWB-PLT-E1042-CON, RWB-PLT-E1042-OPS, RWB-PLT-TE004-APP, RWB-PLT-TE011-APP, RWB-PLT-TE012-APP, RWB-PLT-E2039-APP, RWB-PLT-E2039-CON, RWB-P1-E1016-APP, RWB-P1-E1016-DB, RWB-P1-E1017-APP, RWB-P1-E1068-APP, RWB-P1-E2034-APP, RWB-P2-E2003-APP, RWB-P2-E2034-APP, RWB-P3-E1023-APP, RWB-P3-E1031-APP, RWB-P3-E1031-CON, RWB-P3-E1035-APP, RWB-P3-E1042-APP, RWB-P3-E1042-CON, RWB-P3-E2016-APP, RWB-P3-E2016-CON, RWB-P3-E2024-APP, RWB-P3-E6025-APP, RWB-P4-AD004-APP, RWB-P4-AD004-CON, RWB-P4-AD006-DB, RWB-P4-E1008-APP, RWB-P4-E1016-APP, RWB-P4-E1037-APP, RWB-P4-E1037-CON, RWB-P4-E1039-DB, RWB-P4-E1064-APP, RWB-P4-E2003-APP, RWB-P4-E2019-APP, RWB-P4-E2026-APP, RWB-P4-E8016-APP, RWB-P4-E8016-CON, RWB-P5-AD021-APP, RWB-P5-AD021-CON, RWB-P5-E1016-APP, RWB-P5-E1017-APP, RWB-P5-E1025-APP, RWB-P5-E1033-APP, RWB-P5-E1041-APP, RWB-P5-E1041-CON, RWB-P5-E1046-APP, RWB-P5-E1050-APP, RWB-P5-E1050-CON, RWB-P5-E1050-OPS, RWB-P5-E1053-APP, RWB-P5-E1054-APP, RWB-P5-E1057-APP, RWB-P5-E1062-APP, RWB-P5-E1065-APP, RWB-P5-E2016-APP, RWB-P5-E2018-APP, RWB-P5-E2024-APP, RWB-P5-E2025-APP, RWB-P5-E2025-OPS, RWB-P5-E2026-APP, RWB-P6-E2026-APP, RWB-P6-E4042-APP, RWB-P6-E4042-CON, RWB-P7-E1008-APP, RWB-P7-E1008-CON, RWB-P7-E1008-DB, RWB-P7-E1008-OPS, RWB-P7-E1017-APP, RWB-P7-E2005-APP, RWB-P7-E2017-APP, RWB-P7-E2024-APP, RWB-P7-E2025-APP, RWB-P7-E2026-APP, RWB-S2-E2025-APP, RWB-S2-E2026-APP, RWB-S4-E2025-APP, RWB-S7-E6025-APP, RWB-S7-E6025-CON, RWB-S8-E1023-APP, RWB-S9-E1057-APP | R-35380 | ASM-0247 | Register assumption |  | Masking rules are held in rwb_access.masking_rule, owned by P4, set by Compliance under DL26 and served by GET /masking-policies; v5 copies no rule. | Compliance and PDPA officer |
| RWB-ITG-E1008-ITG, RWB-ITG-E1023-ITG, RWB-ITG-E1025-ITG, RWB-ITG-E1031-ITG, RWB-ITG-E1037-ITG, RWB-ITG-E1050-ITG, RWB-ITG-E1054-ITG, RWB-ITG-E1057-ITG, RWB-ITG-TE004-ITG, RWB-ITG-E2003-ITG, RWB-ITG-E2016-ITG, RWB-ITG-E2024-ITG, RWB-ITG-E2025-ITG, RWB-ITG-E2026-ITG, RWB-ITG-E2034-ITG, RWB-ITG-E6025-ITG, RWB-PLT-E1037-APP, RWB-PLT-E1037-CON, RWB-PLT-E1042-APP, RWB-PLT-E1042-CON, RWB-PLT-E1042-OPS, RWB-PLT-TE004-APP, RWB-PLT-TE011-APP, RWB-PLT-TE012-APP, RWB-PLT-E2039-APP, RWB-PLT-E2039-CON, RWB-P1-E1016-APP, RWB-P1-E1016-DB, RWB-P1-E1017-APP, RWB-P1-E1068-APP, RWB-P1-E2034-APP, RWB-P2-E2003-APP, RWB-P2-E2034-APP, RWB-P3-E1023-APP, RWB-P3-E1031-APP, RWB-P3-E1031-CON, RWB-P3-E1035-APP, RWB-P3-E1042-APP, RWB-P3-E1042-CON, RWB-P3-E2016-APP, RWB-P3-E2016-CON, RWB-P3-E2024-APP, RWB-P3-E6025-APP, RWB-P4-AD004-APP, RWB-P4-AD004-CON, RWB-P4-AD006-DB, RWB-P4-E1008-APP, RWB-P4-E1016-APP, RWB-P4-E1037-APP, RWB-P4-E1037-CON, RWB-P4-E1039-DB, RWB-P4-E1064-APP, RWB-P4-E2003-APP, RWB-P4-E2019-APP, RWB-P4-E2026-APP, RWB-P4-E8016-APP, RWB-P4-E8016-CON, RWB-P5-AD021-APP, RWB-P5-AD021-CON, RWB-P5-E1016-APP, RWB-P5-E1017-APP, RWB-P5-E1025-APP, RWB-P5-E1033-APP, RWB-P5-E1041-APP, RWB-P5-E1041-CON, RWB-P5-E1046-APP, RWB-P5-E1050-APP, RWB-P5-E1050-CON, RWB-P5-E1050-OPS, RWB-P5-E1053-APP, RWB-P5-E1054-APP, RWB-P5-E1057-APP, RWB-P5-E1062-APP, RWB-P5-E1065-APP, RWB-P5-E2016-APP, RWB-P5-E2018-APP, RWB-P5-E2024-APP, RWB-P5-E2025-APP, RWB-P5-E2025-OPS, RWB-P5-E2026-APP, RWB-P6-E2026-APP, RWB-P6-E4042-APP, RWB-P6-E4042-CON, RWB-P7-E1008-APP, RWB-P7-E1008-CON, RWB-P7-E1008-DB, RWB-P7-E1008-OPS, RWB-P7-E1017-APP, RWB-P7-E2005-APP, RWB-P7-E2017-APP, RWB-P7-E2024-APP, RWB-P7-E2025-APP, RWB-P7-E2026-APP, RWB-S2-E2025-APP, RWB-S2-E2026-APP, RWB-S4-E2025-APP, RWB-S7-E6025-APP, RWB-S7-E6025-CON, RWB-S8-E1023-APP, RWB-S9-E1057-APP | R-35381 | ASM-0264 | Register assumption |  | Tables with no data-product row keep no retention period in this version; the source schedule covers data products and document types only, as DL26 asks. |  |
| RWB-ITG-E1008-ITG, RWB-ITG-E1023-ITG, RWB-ITG-E1025-ITG, RWB-ITG-E1031-ITG, RWB-ITG-E1037-ITG, RWB-ITG-E1050-ITG, RWB-ITG-E1054-ITG, RWB-ITG-E1057-ITG, RWB-ITG-TE004-ITG, RWB-ITG-E2003-ITG, RWB-ITG-E2016-ITG, RWB-ITG-E2024-ITG, RWB-ITG-E2025-ITG, RWB-ITG-E2026-ITG, RWB-ITG-E2034-ITG, RWB-ITG-E6025-ITG, RWB-PLT-E1037-APP, RWB-PLT-E1037-CON, RWB-PLT-E1042-APP, RWB-PLT-E1042-CON, RWB-PLT-E1042-OPS, RWB-PLT-TE004-APP, RWB-PLT-TE011-APP, RWB-PLT-TE012-APP, RWB-PLT-E2039-APP, RWB-PLT-E2039-CON, RWB-P1-E1016-APP, RWB-P1-E1016-DB, RWB-P1-E1017-APP, RWB-P1-E1068-APP, RWB-P1-E2034-APP, RWB-P2-E2003-APP, RWB-P2-E2034-APP, RWB-P3-E1023-APP, RWB-P3-E1031-APP, RWB-P3-E1031-CON, RWB-P3-E1035-APP, RWB-P3-E1042-APP, RWB-P3-E1042-CON, RWB-P3-E2016-APP, RWB-P3-E2016-CON, RWB-P3-E2024-APP, RWB-P3-E6025-APP, RWB-P4-AD004-APP, RWB-P4-AD004-CON, RWB-P4-AD006-DB, RWB-P4-E1008-APP, RWB-P4-E1016-APP, RWB-P4-E1037-APP, RWB-P4-E1037-CON, RWB-P4-E1039-DB, RWB-P4-E1064-APP, RWB-P4-E2003-APP, RWB-P4-E2019-APP, RWB-P4-E2026-APP, RWB-P4-E8016-APP, RWB-P4-E8016-CON, RWB-P5-AD021-APP, RWB-P5-AD021-CON, RWB-P5-E1016-APP, RWB-P5-E1017-APP, RWB-P5-E1025-APP, RWB-P5-E1033-APP, RWB-P5-E1041-APP, RWB-P5-E1041-CON, RWB-P5-E1046-APP, RWB-P5-E1050-APP, RWB-P5-E1050-CON, RWB-P5-E1050-OPS, RWB-P5-E1053-APP, RWB-P5-E1054-APP, RWB-P5-E1057-APP, RWB-P5-E1062-APP, RWB-P5-E1065-APP, RWB-P5-E2016-APP, RWB-P5-E2018-APP, RWB-P5-E2024-APP, RWB-P5-E2025-APP, RWB-P5-E2025-OPS, RWB-P5-E2026-APP, RWB-P6-E2026-APP, RWB-P6-E4042-APP, RWB-P6-E4042-CON, RWB-P7-E1008-APP, RWB-P7-E1008-CON, RWB-P7-E1008-DB, RWB-P7-E1008-OPS, RWB-P7-E1017-APP, RWB-P7-E2005-APP, RWB-P7-E2017-APP, RWB-P7-E2024-APP, RWB-P7-E2025-APP, RWB-P7-E2026-APP, RWB-S2-E2025-APP, RWB-S2-E2026-APP, RWB-S4-E2025-APP, RWB-S7-E6025-APP, RWB-S7-E6025-CON, RWB-S8-E1023-APP, RWB-S9-E1057-APP | R-35383 | ASM-0355 | Register assumption |  | The masking policy is P4 rwb-access data (masking_rule), enforced in each service and applied by rwb-source-data on every ACE field it serves; the content of the rule stays with Compliance under DL26. | Compliance team issues the rule content and P4 confirms the masking_rule rows in the next release. |

## 4. Not applied (the value is not in the source documents)

| Story | Ruling | Item | Section | Title | Reason |
|---|---|---|---|---|---|
| RWB-PLT-E1027-APP | R-18521 | DOR-RWB-PLT-E1027-APP-11 | 12 | Definition of Ready item 11 Guardrails: Partial | Field named: actor_user_id (DF-DEC-030, Data Classification v5, personal Yes). The 'No personal data' sentence is outside this chunk; its text is needed to edit it. |
| RWB-PLT-E1027-CON | R-18529 | DOR-RWB-PLT-E1027-CON-18 | find it | Definition of Ready item 18 Open decisions: Partial | DL10 open-decisions text is not in the chunk, only the header and headings. No exact old text to copy, so no edit. Needs the current section text. |
| RWB-PLT-E1027-CON | R-21895 | GAP-2068 | find it | The local decision record has no table, no DDL and no case or trace column | Decision-record table text is not in the chunk, only the header and headings. No exact old text to copy, so no edit. Needs the current section text. |
| RWB-PLT-E1027-CON | R-21896 | GAP-2074 | find it | One chain or 19 chains plus the ledger chain | Chain-scope section text is not in the chunk, only the header and headings. No exact old text to copy, so no edit. Needs the current section text. |
| RWB-PLT-E1027-CON | R-22007 | GAP-2441 | 12 | How the business date, the queue identifier and the owner identifier travel in the decision record is not in the sources | Section 12 envelope and actions text is not in the chunk, only the header and headings. No exact old text to copy, so no edit. Needs the current section text. |
| RWB-PLT-E1027-CON | R-22039 | GAP-1238 | 12.3 | Two ce_type values are published for DecisionRecorded | Section 12.3 ce_type text is not in the chunk, only the header and headings. No exact old text to copy, so no edit. Needs the current section text. |
| RWB-PLT-E1027-CON | R-22040 | GAP-0352 | 16 | E1027 decision codes and reference data move to P3 while the writer and the ledger are PLT and P7 | Section 16 test-case text and its lake and P3 rows are not in the chunk, only the header and headings. No exact old text to copy, so no edit. |
| RWB-PLT-E1027-CON | R-22045 | GAP-1403 | find it | Local decision-record contract: record schema, table shape, shared-topic envelope and message catalogue | Record schema, DDL and envelope text is not in the chunk, only the header and headings. No exact old text to copy, so no edit. Needs the current section text. |
| RWB-PLT-E1027-CON | R-22075 | GAP-2448 | 13 | The metadata dependency rows name only the P5 contract, while the DP table adds platform and rwb-case and rwb-access contracts | Section 13 text is not in the chunk, only the header and headings. Header metadata row is already kept as fixed. No exact old text to copy, so no edit. |
| RWB-PLT-E1027-CON | R-28465 | GAP-0984 |  | rwb-access local decision-record store: the column set behind the five named columns, the canonical form, the genesis value, the verifier behaviour on write and read, the DECISION_LOG letters per role and the per-service login are not specified | Decision_record column set, physical types and canonical form appear in no source; publishing them would invent values. RBAC and login parts belong to other documents. |
| RWB-PLT-E1037-APP | R-07156 | DOR-RWB-PLT-E1037-APP-14 |  | Definition of Ready item 14 Epic design: Fail | No signed epic design record found in the source set (Grep for sign-off wording hit only working files). Sign-off cannot be confirmed from the story. |
| RWB-PLT-E1037-APP | R-07159 | DOR-RWB-PLT-E1037-APP-22 |  | Definition of Ready item 22 Fake published: Fail | No published contract fake library version found in the source set (Grep hits were working files). Recording a version would invent one. |
| RWB-PLT-E1037-APP | R-18535 | DOR-RWB-PLT-E1037-APP-10 |  | Definition of Ready item 10 Screens and states: Partial | Empty, loading, error and no-access state definitions for SCR-43 and SCR-47 are not in the chunk's story parts. Adding them would invent content. |
| RWB-PLT-E1037-APP | R-18536 | DOR-RWB-PLT-E1037-APP-11 |  | Definition of Ready item 11 Guardrails: Partial | The personal-data fields the detcheck finding names are not in the chunk's story parts. Classifying them would invent field names. |
| RWB-PLT-E1037-APP | R-18538 | DOR-RWB-PLT-E1037-APP-18 |  | Definition of Ready item 18 Open decisions: Partial | DL10, DL26 and DL38 are business decisions that stay open. The directive confirms assumptions but does not close decisions. No edit. |
| RWB-PLT-E1037-APP | R-18540 | DOR-RWB-PLT-E1037-APP-4 | 8 | Definition of Ready item 4 Business rules: Partial | Sections 7 and 16 are not in this chunk, so there is no anchor to add AC9-AC11 or their test rows for BR10, BR12 and BR14. Needs next chunk. |
| RWB-PLT-E1037-APP | R-31741 | AC14: §8 BR10, BR12, BR14 (these rules have no criterion and no test; a rule that is an architecture constraint may belong in a guardrail or boundary test instead) | 7 | AC14: §8 BR10, BR12, BR14 (these rules have no criterion and no test; a rule that is an architecture constraint may belong in a guardrail or boundary test instead) | Section 7 and 16 text for BR10, BR12, BR14 is not in this chunk; needs next chunk, consistent with DOR item 4 (R-18540). |

## 5. Cross-document changes (pending in the target document)


### 11 Delivery and operations/Recovery Workbench Dependency Map v5.xlsx (13)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-13721 | RWB-PLT-E1027-CON | GAP-1343 | header | Publish the six DP-added dependencies with this story as consumer; confirm RWB-P4-E1037-CON as a contract dependency in the wave 2 contract review. |
| CDC-13724 | RWB-PLT-E1027-CON | GAP-2501 | header | Record the DP-added H and C contracts as non-blocking platform and published contracts built against fakes; keep the metadata rows as the plan gives them. |
| CDC-13728 | RWB-PLT-E1027-CON | GAP-1291 | header | Record the DP-added H and C contracts as non-blocking platform and published contracts built against fakes; keep metadata rows; keep DP-04 and DP-14 contracts visible in section 13. |
| CDC-13730 | RWB-PLT-E1027-CON | GAP-2317 | header | Add the five rows: H RWB-PLT-E1027-CON, RWB-PLT-E1043-CON, RWB-PLT-E1044-CON, RWB-PLT-N001-CON and C RWB-P3-E1043-CON. Keep Work Package metadata unchanged. |
| CDC-13738 | RWB-PLT-E1027-CON | GAP-1312 | n/a | Add H rows RWB-PLT-E1027-CON and RWB-PLT-N001-CON and the four consumed contracts to the Dependency Map as non-blocking. |
| CDC-13751 | RWB-PLT-E1027-CON | GAP-1885 |  | Add non-blocking consumed rows: RWB-P7-E2013-CON as C of wave 2; case and partner contracts as published contracts built on fakes; RWB-P3-E1043-CON as C; DP-08 edge and guard rule for declared rights. |
| CDC-13752 | RWB-PLT-E1027-CON | GAP-2751 |  | Add non-blocking rows for API-P5-002, API-P5-008 and API-P3-002 built on fakes; RWB-P3-E1043-CON as C; DP-08 edge and guard rule; name the case-state announcement and task raise in the P3 case contract. |
| CDC-13763 | RWB-PLT-E1027-CON | GAP-2797 |  | Declare the LITIGATION package as a non-blocking consumed contract from rwb-decision at its version in force, with its fake; add no rule row, package or rule version to the consumers. |
| CDC-13806 | RWB-PLT-E1027-CON | GAP-2468 | story line and dependency map | Carry the six platform CON H rows of DP-03, DP-06, DP-07, DP-09, DP-10 and DP-19 (IDs Not specified in the source documents (GAP-2468)) and RWB-P7-E2005-CON in the dependency map. Keep the lane at Day 1. |
| CDC-13807 | RWB-PLT-E1027-CON | GAP-1335 | 13 | Carry RWB-PLT-E1027-CON, RWB-PLT-E1042-CON, RWB-P3-E1042-CON, RWB-PLT-E1043-CON, RWB-P3-E1043-CON, RWB-PLT-TE006-CON, RWB-PLT-E1071-CON and RWB-PLT-N001-CON as sequencing rows. |
| CDC-13808 | RWB-PLT-E1027-CON | GAP-1337 | 13 | Carry RWB-PLT-E1027-CON, RWB-PLT-E1072-CON, RWB-P7-E1073-CON, RWB-PLT-E1042-CON, RWB-P3-E1042-CON, RWB-PLT-E1043-CON, RWB-P3-E1043-CON, RWB-PLT-TE006-CON, RWB-PLT-E1071-CON, RWB-PLT-E1044-CON and RWB-PLT-N001-CON as sequencing rows. |
| CDC-13812 | RWB-PLT-E1027-CON | GAP-1277 | 13 | Carry six platform H dependencies, one published C dependency and two service baselines as DP-added rows; correct metadata at next version. |
| CDC-13813 | RWB-PLT-E1027-CON | GAP-1282 | 13 | Carry six platform H dependencies and three published C dependencies as DP-added rows; correct metadata at next version. |

### 03 Requirements and specifications/PRD/Recovery Workbench PRD PLT Platform v1.md (11)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-13674 | RWB-PLT-E1027-APP | CG-ALL-1294 | header | Renumber the duplicate FR-PLT-014 (the one for the local decision record in the transaction) in the next PRD version. |
| CDC-13675 | RWB-PLT-E1027-APP | CG-ALL-1295 | header | Renumber the duplicate FR-PLT-015 (the daily hash-chain check) in the next PRD version. |
| CDC-13677 | RWB-PLT-E1027-APP | DOR-RWB-PLT-E1027-APP-2 | 18 | Give FR-PLT-014 and FR-PLT-015 one meaning each in the PRD. |
| CDC-13695 | RWB-PLT-E1027-CON | CG-ALL-1302 | none | Renumber the duplicate FR-PLT-014 in the PRD's next version so each ID has one meaning. |
| CDC-13696 | RWB-PLT-E1027-CON | CG-ALL-1303 | none | Renumber the duplicate FR-PLT-015 in the PRD's next version so each ID has one meaning. |
| CDC-13699 | RWB-PLT-E1027-CON | DOR-RWB-PLT-E1027-CON-2 | 18 | Give FR-PLT-014 and FR-PLT-015 one meaning each in the PRD |
| CDC-13830 | RWB-PLT-E1037-APP | CG-ALL-1309 | header | Renumber the duplicate FR-PLT-008 in the PRD's next version so each ID has one meaning. |
| CDC-13831 | RWB-PLT-E1037-APP | CG-ALL-1310 | header | Renumber the duplicate FR-PLT-019 in the PRD's next version so each ID has one meaning. |
| CDC-13832 | RWB-PLT-E1037-APP | CG-ALL-1311 | header | Renumber the duplicate FR-PLT-026 in the PRD's next version so each ID has one meaning. |
| CDC-13833 | RWB-PLT-E1037-APP | CG-ALL-1312 | header | Renumber the duplicate FR-PLT-033 in the PRD's next version so each ID has one meaning. |
| CDC-13836 | RWB-PLT-E1037-APP | DOR-RWB-PLT-E1037-APP-2 | 18 | Renumber the duplicate FR-PLT-008, FR-PLT-019, FR-PLT-026 and FR-PLT-033 in the PRD's next version so each ID has one meaning. |

### 22 Microservice Realignment/Recovery Workbench Microservice Ownership Map v1.xlsx (9)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-13681 | RWB-PLT-E1027-APP | GAP-1235 |  | Record the decision-record append as a local operation on task queue rwb-decision under DP-03, with no REST write row for decision-log. |
| CDC-13708 | RWB-PLT-E1027-CON | GAP-1235 |  | Add a local-operation row for the decision-record append on task queue rwb-decision under DP-03. Add no POST or PUT path for decision-log. |
| CDC-13745 | RWB-PLT-E1027-CON | GAP-3129 | header | Publish a contract-end operation or confirm a workflow command; define open for an instruction; publish case-side re-selection command; publish the partner_user field list. |
| CDC-13841 | RWB-PLT-E1037-APP | GAP-1245 | find it | Name the scope predicate in the rwb-access authorise answer and the case-scope read of rwb-case; name the Compliance incident queue as platform configuration; confirm with the P4 access owner and P3 case owner. |
| CDC-13842 | RWB-PLT-E1037-APP | GAP-0358 | 13 | Name matrix table load and approval under P4 rwb-access; name parameters and LOV load under P3 rwb-case; platform library publishes guard and annotations. |
| CDC-13843 | RWB-PLT-E1037-APP | GAP-1564 | 2 | At RWB-P3 reference-data contract review, confirm load, approve, verify and rollback of the permission matrix and DoA tables stay with rwb-case; record the ruling on the Ownership Map. |
| CDC-13846 | RWB-PLT-E1037-APP | GAP-0164 | 2 | Record that PT role rows and their letters stay with P4, partner user stays with S9, and S9 calls POST /authorise with the PT role code and holds the user-to-role link. |
| CDC-13857 | RWB-PLT-E1037-APP | GAP-2039 | n/a | Add an access_log row owned by P4 rwb-access with the ACE DBA, in schema rwb_access, with its own DB story in RWB-SVC-P4 at the next revision. |
| CDC-13862 | RWB-PLT-E1037-APP | GAP-2063 | 5 | Add a row for gateway-bff owned by RWB-PLT-EDGE for screen composition, and read the partner gateway as RWB-PLT-EDGE with S9 rwb-partner behind it. |

### 06 Data/Recovery Workbench Logical Data Model and Data Dictionary v9.xlsx; 06 Data/Recovery Workbench Data Classification and Personal Data Inventory v5.xlsx (8)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-13667 | RWB-PLT-E1027-APP | CG-ALL-1284 | 12.3 | Record ce_specversion as a CloudEvents 1.0 binary-mode transport attribute, or add a dictionary name for it. |
| CDC-13668 | RWB-PLT-E1027-APP | CG-ALL-1285 | 12.3 | Record ce_id as a CloudEvents 1.0 binary-mode transport attribute, or add a dictionary name for it. |
| CDC-13669 | RWB-PLT-E1027-APP | CG-ALL-1286 | 12.3 | Record ce_type as a CloudEvents 1.0 binary-mode transport attribute, or add a dictionary name for it. |
| CDC-13670 | RWB-PLT-E1027-APP | CG-ALL-1287 | 12.3 | Record ce_source as a CloudEvents 1.0 binary-mode transport attribute, or add a dictionary name for it. |
| CDC-13671 | RWB-PLT-E1027-APP | CG-ALL-1288 | 12.3 | Record ce_subject as a CloudEvents 1.0 binary-mode transport attribute, or add a dictionary name for it. |
| CDC-13672 | RWB-PLT-E1027-APP | CG-ALL-1289 | 12.3 | Record ce_time as a CloudEvents 1.0 binary-mode transport attribute, or add a dictionary name for it. |
| CDC-13678 | RWB-PLT-E1027-APP | DOR-RWB-PLT-E1027-APP-7 | 11 | Add decision_record as a local library object in each service schema and outbox_event with their section 11 fields; treat ce_specversion, ce_id and decision_log_repeats_total as envelope and metric names. |
| CDC-13700 | RWB-PLT-E1027-CON | DOR-RWB-PLT-E1027-CON-7 | 11 | Add decision_record, ce_type and ce_subject as fields or entities in LDM v9 or Data Classification v5 |

### RWB-PLT-E1027-CON (5)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-13663 | RWB-PLT-E1027-APP | DOR-RWB-PLT-E1027-APP-21 | Header | Build status must reach Done (published) before this story can rely on the contract; currently 'Not started'. |
| CDC-13664 | RWB-PLT-E1027-APP | DOR-RWB-PLT-E1027-APP-22 | Header | Record the published contract fake library version that this story builds against. |
| CDC-13680 | RWB-PLT-E1027-APP | GAP-1238 | 12.3 | Story keeps ce_type rwb.decision.DecisionRecorded.v1; the second published value is not in the sources, so the contract must settle which type is published. |
| CDC-13683 | RWB-PLT-E1027-APP | GAP-1237 |  | Freeze the canonical form: ordered field list, UTF-8, no whitespace, null as empty string, 64 lowercase hex; publish one cross-language fixture. |
| CDC-13685 | RWB-PLT-E1027-APP | GAP-1403 |  | Publish the record schema, DDL template and CloudEvents envelope as major version 1; freeze them when consuming stories pass contract tests. |

### 05 Technical architecture/Recovery Workbench Event and Messaging Design v5.xlsx (4)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-13687 | RWB-PLT-E1027-APP | GAP-1622 |  | Add a contract version to the DecisionRecorded event, record it on the ledger entry, and send unknown versions to the dead-letter topic. |
| CDC-13767 | RWB-PLT-E1027-CON | GAP-2669 |  | Confirm the stage report as the event REQ-S2-009 means, or allocate rwb.treatment.PlanBroken.v1 with DP-09 and outbox rows in both stories and the wave 2 catalogue. |
| CDC-13794 | RWB-PLT-E1027-CON | GAP-1622 | n/a | Add a contract version to DecisionRecorded and record it on the ledger entry; consumer accepts a known version set and sends an unknown version to the dead-letter topic. |
| CDC-13852 | RWB-PLT-E1037-APP | GAP-1569 | n/a | Add AccessPolicyChanged and DoaLimitChanged on topic rwb.access.events.v1 with CloudEvents type, key, payload, versioning, cache refresh window and missed-event fallback; change T5.3 from None to the two events. |

### 06 Data/Recovery Workbench Logical Data Model and Data Dictionary v9.xlsx (3)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-13665 | RWB-PLT-E1027-APP | CG-ALL-1282 | Header | Record decision_record as a platform library object created per service schema by the DDL template (PLT), so the name resolves in the owning document. |
| CDC-13666 | RWB-PLT-E1027-APP | CG-ALL-1283 | 14 | Record decision_log_repeats_total as a metric object exported by the platform library (defined in section 14), not a data field. |
| CDC-13694 | RWB-PLT-E1027-CON | CG-ALL-1296 | none | Add decision_record as the PLT-published local decision-record table (DDL template, Resource DecisionRecordDdlTemplate in RWB-PLT-E1027-CON section 13), or record it as the dictionary name. |

### 09 Testing and quality/Recovery Workbench Test Cases v8.xlsx (3)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-13673 | RWB-PLT-E1027-APP | CG-ALL-1291 | 16 | Add rows TC-PLT-E1027-APP-01 to TC-PLT-E1027-APP-06 to Story test cases, with Given, When and Then copied from the criteria they cover. |
| CDC-13792 | RWB-PLT-E1027-CON | CG-ALL-1300 | 16 | Add rows for TC-PLT-E1027-CON-01 to TC-PLT-E1027-CON-05 with Given, When and Then copied from the criteria they cover. |
| CDC-13829 | RWB-PLT-E1037-APP | CG-ALL-1306 | 16 | Add rows TC-PLT-E1037-APP-01 to TC-PLT-E1037-APP-07 under Story test cases, with Given, When and Then copied from the criteria they cover. |

### 09 Testing and quality/Recovery Workbench Requirements Traceability Matrix v7.xlsx (3)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-13686 | RWB-PLT-E1027-APP | CG-ALL-1292 | 18 | Align the REQ-DRI-004 and REQ-DRI-005 test lists in section 18 and RTM v7 in their next versions. |
| CDC-13793 | RWB-PLT-E1027-CON | CG-ALL-1301 | 18 | Align the REQ-DRI-004 and REQ-DRI-005 test lists with section 18 of RWB-PLT-E1027-CON in the next RTM version. |
| CDC-13854 | RWB-PLT-E1037-APP | CG-ALL-1307 | 18 | Align the test case list for REQ-ACA-003, REQ-ACA-005 and the four other differing requirements with RWB-PLT-E1037-APP section 18 in the next RTM version. |

### 04 User stories/Recovery Workbench Service Story Catalog v1.xlsx (3)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-13692 | RWB-PLT-E1027-APP | GAP-3232 |  | Use the catalog as the source of the v5 graph. State the template baseline once on the Dependency classes sheet. Record the 75-row difference (64 H, 11 C) across the ten listed stories. |
| CDC-13809 | RWB-PLT-E1027-CON | GAP-2484 | 13 | Give GET /cases/{caseId}/recommendation read to the P7 story serving the decision screen; treat four platform contracts as published before Day 1. |
| CDC-13863 | RWB-PLT-E1037-APP | GAP-3232 | 3 | Use the catalog as the source of the v5 graph and state the template baseline once on the Dependency classes sheet; story files keep their rows. |

### 22 Microservice Realignment/Recovery Workbench Architecture v5 Text Extract v1.md (3)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-13747 | RWB-PLT-E1027-CON | GAP-0637 | header | Fix the three /admin/agent-configs operations as the contract; relabel slide 16 summary; fix kind value set as POLICY and PROMPT; take approval instant from updated_at. |
| CDC-13827 | RWB-PLT-E1037-APP | GAP-0013 | find it | Version each of the six ACE Common contracts and run contract tests on both sides from wave 1 (owner: ACE team). |
| CDC-13845 | RWB-PLT-E1037-APP | GAP-0161 | 2 | Record fail-closed reading, refresh on AccessPolicyChanged and DoaLimitChanged, and the 5 minute membership refresh; cache lifetime stays a placeholder until RWB-P4-E1037-CON. |

### 05 Technical architecture/Recovery Workbench Kafka Topic and Event Catalog v1.xlsx (3)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-13824 | RWB-PLT-E1037-APP | CG-ALL-1305 | 12.4 | Add rwb.access.DoALimitChanged.v1 to the Events sheet, or align the story to a catalogued event type. |
| CDC-13826 | RWB-PLT-E1037-APP | DOR-RWB-PLT-E1037-APP-8 | 12.4 | Add platform as consumer of rwb.access.AccessPolicyChanged.v1, and add rwb.access.DoALimitChanged.v1 to the Events sheet. |
| CDC-13828 | RWB-PLT-E1037-APP | CG-ALL-1304 | 12.4 | Add platform as a consumer of rwb.access.AccessPolicyChanged.v1 and its ACL, or drop the handler. |

### RWB-PLT-E1037-CON (3)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-13825 | RWB-PLT-E1037-APP | DOR-RWB-PLT-E1037-APP-21 | find it | Set build status to Done once the contract is published. |
| CDC-13849 | RWB-PLT-E1037-APP | GAP-1404 | 2 | Publish library artefact at a platform coordinate with major version 1; hold cache lifetime in a parameter; publish authorise and masking-policy payloads and the decide-or-mask split. |
| CDC-13850 | RWB-PLT-E1037-APP | GAP-1405 | 2 | Publish guard, scope guard, mask applier and annotation shapes; fix audit record as case id, field id and clear or masked flag; map access-owner failures to 503 with no business data. |

### RWB-P4-E1037-CON (3)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-13844 | RWB-PLT-E1037-APP | GAP-0159 | 2 | Publish operation IDs, request and response bodies, status codes and error model for POST /authorise, GET /me/permissions, GET /doa-limits and GET /masking-policies. |
| CDC-13848 | RWB-PLT-E1037-APP | GAP-0778 | 2 | Fix role roster and row count from the approved file; publish AccessPolicyChanged payload with change kind, version label and effective date; confirm rwb_access baseline as V0001. |
| CDC-13851 | RWB-PLT-E1037-APP | GAP-2036 | 2 | Write the four operations with owner P4 and guard library owner platform; record that request and response shapes are open until the contract is written. |

### 09 Testing and quality/Recovery Workbench Test Cases v8.xlsx; 09 Testing and quality/Recovery Workbench Requirements Traceability Matrix v7.xlsx (2)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-13676 | RWB-PLT-E1027-APP | DOR-RWB-PLT-E1027-APP-12 | 16 | Add TC-PLT-E1027-APP-01 to -07 under the same ids in Test Cases v8; align the section 18 test lists with RTM v7. |
| CDC-13698 | RWB-PLT-E1027-CON | DOR-RWB-PLT-E1027-CON-12 | 12.7, 16, 18 | Add TC-PLT-E1027-CON-01 to -07 to Test Cases v8; align RTM v7 test lists with story §18 |

### RWB-P7-E2032-APP (2)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-13679 | RWB-PLT-E1027-APP | GAP-2404 | 13 | Read the H list as None plus the five platform contracts the DP table names; read the C list as RWB-P10-E2032-CON plus C RWB-P3-E1042-CON, C RWB-P3-E1043-CON and the published P4 authorise contract. |
| CDC-13707 | RWB-PLT-E1027-CON | GAP-2404 | unknown | Read H as None plus the five platform contracts; C as RWB-P10-E2032-CON plus RWB-P3-E1042-CON, RWB-P3-E1043-CON and the published P4 authorise contract; add DP-08 to patterns applied |

### parameter-catalog.csv (2)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-13688 | RWB-PLT-E1027-APP | GAP-1617 |  | Add the completeness target and gap alert threshold as five-minute reference-data rows; the strict-mode wait bound stays open. |
| CDC-13795 | RWB-PLT-E1027-CON | GAP-1617 | n/a | Add completeness target and gap alert threshold as reference-data keys at five minutes. Strict-mode wait bound key: Not specified in the source documents (GAP-1617) until Risk sign-off. |

### 02 Business architecture and process/Recovery Workbench Users Roles and Permissions v5.xlsx (2)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-13697 | RWB-PLT-E1027-CON | DOR-RWB-PLT-E1027-CON-1 | 1 | Add the role 'platform contract owner' with its role code to Users Roles and Permissions v5 so the section 1 role resolves; story text unchanged |
| CDC-13834 | RWB-PLT-E1037-APP | DOR-RWB-PLT-E1037-APP-1 | 1 | Add 'service developer' as a role code or role name, or the section 1 role must be changed to a role already listed there. |

### OTHER:Gap register (2)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-13701 | RWB-PLT-E1027-CON | GAP-0542 | find it | Close GAP-0542 with the proposed fix: P1 emits chain-order entries via the local library; P1 writes no decision_log_entry row |
| CDC-13702 | RWB-PLT-E1027-CON | GAP-2176 | find it | Close GAP-2176 with the proposed fix: P1 emits each entry with chain_seq, prev_hash and entry_hash; rwb-decision seals; P1 holds no grant on rwb_decision |

### 05 Technical architecture/Recovery Workbench Service Contract Catalog v1.md (2)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-13716 | RWB-PLT-E1027-CON | GAP-0672 | find it | Record the eight DP H rows as wave-0 platform prerequisites and publish the model fetch (path, request, response fields) in RWB-P7-E1073-CON. |
| CDC-13804 | RWB-PLT-E1027-CON | GAP-2455 |  | Confirm rwb-decision appends every DecisionRecorded fact to decision_log_entry; the producer's local record is the working record and the ledger entry is the record of record; platform contracts are wave-0/1 baseline outside H. |

### RWB-P7-E1073-CON (2)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-13719 | RWB-PLT-E1027-CON | GAP-1336 | find it | Fix the model answer, the inputs snapshot and the announcement payload in the registry contract; name the plan-status section of the decision log screen with the gateway-bff route owner; publish the per-service login with the database platform story before wave 2 build. |
| CDC-13720 | RWB-PLT-E1027-CON | GAP-1339 | find it | Fix the model and catalogue answer in the OpenAPI, and the envelope field names in RWB-PLT-E1027-CON, before wave 2 contract tests. Take MSG-P7-009 and MSG-P7-012 wording from the Error and Message Standard. Name the SCR-38 and SCR-03 panel in RWB-P7-E2005-APP. State in build order that DP-added platform dependencies are held by platform stories. |

### RWB-S6-E6002-APP (2)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-13780 | RWB-PLT-E1027-CON | GAP-2984 | n/a | Keep plan H, C, I and X rows; declare rwb-partner as class C with placeholder name and 2 s budget; model package as rwb-decision activity and case move as child stage outcome; raise bid table for DB story; adopt REQ-S6-004. |
| CDC-13784 | RWB-PLT-E1027-CON | GAP-1969 | n/a | Keep metadata rows; declare four consumed contracts and authorise call as class C rows; name REQ-S6-004 as requirement; confirm three operation names with owners before baseline tag. |

### Epic design record; OTHER:EP01) (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-13662 | RWB-PLT-E1027-APP | DOR-RWB-PLT-E1027-APP-14 | Header | Record the signed epic design sign-off for this story's epic; the story cannot state a sign-off that the source documents do not contain. |

### 06 Data/Recovery Workbench Physical Schema v7 (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-13682 | RWB-PLT-E1027-APP | GAP-1236 |  | Fix the physical column list, the data-date column, the inputs digest and the MSG-P7-009 and MSG-P7-003 catalogue entry format. |

### OTHER:Platform decision-record library baseline (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-13684 | RWB-PLT-E1027-APP | GAP-1402 |  | Publish the artefact coordinates, the entry-id key for records with no case, one chain per service schema shared with P7, and incident routing through each service's alerting. |

### RWB-P7-E1027-APP (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-13689 | RWB-PLT-E1027-APP | GAP-2075 |  | Audit search reads the ledger only and shows unsealed entries until JOB-13 collects them; strict mode waits for ledger acknowledgement of its own record. |

### OTHER:Batch and Scheduling next version (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-13690 | RWB-PLT-E1027-APP | GAP-1240 |  | Keep the ledger ingest continuous from Kafka, keep JOB-14 as the only P7 Schedule, and mark JOB-13 retired. |

### OTHER:FSD P7 module specification (P7 A2.6; OTHER:AC-P7-006-01 to AC-EXC-P7-006-04) (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-13691 | RWB-PLT-E1027-APP | GAP-1239 |  | Delete A2.6 and its acceptance criteria AC-P7-006-01 to AC-EXC-P7-006-04 (partitions, manifest, watermark, REC-08). Move the reporting need to the rwb-reporting projection from events. |

### Epic design record (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-13693 | RWB-PLT-E1027-CON | DOR-RWB-PLT-E1027-CON-14 | none | Record the signed epic design sign-off for RWB-PLT-LIB. No signed epic design is named in the story or source documents. |

### 05 Technical architecture/Recovery Workbench Service Contract Catalog v1.md; OTHER:gap register (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-13703 | RWB-PLT-E1027-CON | GAP-0673 | find it | Mark INT-03 superseded for legacy key RWB-E4-046 with date and decision; load ALS interface_config row per environment after interface owner agrees values |

### RWB-S5-E1011-APP (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-13704 | RWB-PLT-E1027-CON | GAP-1946 | unknown | Keep H and C at None; record nine platform and rwb-case CONs as wave-0 prerequisites and fakes; drop the two extracts and INT-19 path; serve quality facts from the GET /api/recovery/asset/v1 quality endpoints; declare the ACE read as the DP06 rwb-source-data contract |

### RWB-P6-E1011-APP (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-13705 | RWB-PLT-E1027-CON | GAP-1167 | unknown | Keep H at None; record the seven platform CONs as wave-0 build prerequisites that arrive with the platform release train; add them to the dependency map as platform prerequisites, not lane dependencies |

### RWB-S8-E1021-APP (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-13706 | RWB-PLT-E1027-CON | GAP-3075 | unknown | State the eight platform H rows and two C rows in pattern application; keep H empty and C as RWB-P3-E1021-CON; start Day 1 against published baselines and fakes |

### 06 Data/Recovery Workbench Physical Schema v7; OTHER:contract baseline; OTHER:platform message catalogue (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-13709 | RWB-PLT-E1027-CON | GAP-1236 |  | Fix the physical column list, the data-date column and the inputs digest in rwb_decision.sql and the contract baseline. Publish the catalogue entry format for MSG-P7-009 and MSG-P7-003. |

### OTHER:contract baseline (canonical form of the entry hash) (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-13710 | RWB-PLT-E1027-CON | GAP-1237 |  | Freeze the canonical form: ordered field list, UTF-8, no whitespace, null as empty string, 64 lowercase hex. Publish one cross-language fixture for writers and the verifier. |

### OTHER:platform decision-record library baseline (RWB-PLT-LIB) (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-13711 | RWB-PLT-E1027-CON | GAP-1402 |  | Publish the artefact coordinates, the entry-id key for records with no case, one chain per service schema sharing the P7 algorithm, and incident routing through each service's alerting. |

### RWB-P6-E1032-APP; 11 Delivery and operations/Recovery Workbench Dependency Map v5.xlsx (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-13712 | RWB-PLT-E1027-CON | GAP-1198 |  | Add H RWB-PLT-E1027-CON, RWB-PLT-E1042-CON, RWB-PLT-E1043-CON, RWB-PLT-TE006-CON, RWB-PLT-E1071-CON, RWB-PLT-E1044-CON and RWB-PLT-N001-CON, and C RWB-P3-E1042-CON and RWB-P3-E1043-CON. |

### RWB-P7-E2041-APP (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-13713 | RWB-PLT-E1027-CON | GAP-2414 |  | Set H to None plus the eight platform contracts the DP table names. Set C to RWB-P3-E2041-CON plus RWB-P7-E1073-CON, RWB-P3-E1042-CON, RWB-P3-E1043-CON and RWB-P4-E1037-CON. |

### RWB-P4-E1039-CON (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-13714 | RWB-PLT-E1027-CON | GAP-1250 |  | Confirm P4 reads the relayed rwb.decision-record.v1 events for its access-log view. P4 keeps the break-glass path and role model, and no write path from this service calls P4. |

### OTHER:RWB-E1-065 section 11 (decision code of seeded records) (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-13715 | RWB-PLT-E1027-CON | GAP-2252 |  | Name decision code RWB-P3-E1018-APP for the creation seed and RWB-P3-E1019-APP or the exclusion rule for seeded exclusions. Confirm both at contract review. |

### OTHER:AsyncAPI document rwb.decision-record.v1 (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-13717 | RWB-PLT-E1027-CON | GAP-1332 | find it | Fix the DecisionRecorded payload element names (business date, queue and owner identifiers, hand-over reference, actions) and the inputs snapshot shape with the composite idempotency key; confirm with the hand-over contract owner before wave 2 build. |

### RWB-P7-E2005-CON (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-13718 | RWB-PLT-E1027-CON | GAP-2462 | find it | Add the element list of decision_log_entry.actions and outcome to the DecisionLogEntry resource, and the record shape to RWB-PLT-E1027-CON, at contract review. Until then tests assert counts, source system and action codes. |

### RWB-P8-E2008-CON (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-13722 | RWB-PLT-E1027-CON | GAP-1347 | header | Publish the three event schemas with the data fields the legacy story names per event and the platform CloudEvents envelope; require a new schema version for any added business field. |

### RWB-S8-E2009-APP (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-13723 | RWB-PLT-E1027-CON | GAP-3087 | header | Record the slice as secondary serving of the steering data set in S8; publish seven consumed operation names with owners before tagging; confirm the load-time edge with P9 and S8 owners. |

### RWB-P6-E2013-APP; 11 Delivery and operations/Recovery Workbench Dependency Map v5.xlsx (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-13725 | RWB-PLT-E1027-CON | GAP-1223 | header | Read the H list as None plus the DP-named platform contracts and the C list as RWB-P7-E2013-CON plus the three published contracts; story stays Day 1. |

### 22 Microservice Realignment/Recovery Workbench Microservice Ownership Map v1.xlsx; OTHER:S4 context pack; OTHER:PRD EP05 and P6 and P3 contract stories (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-13726 | RWB-PLT-E1027-CON | GAP-2742 | header | Add non-blocking C rows for the P6 notice call and the rwb-case stage answer; record notice and template rows as P6's or correct S4; name the operations; add REQ-S4-001; decide D7.1 approval in EP05 PRD. |

### RWB-P6-E2018-APP (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-13727 | RWB-PLT-E1027-CON | GAP-1196 | header | Add DP-03 to the pattern set and H RWB-PLT-E1027-CON to the build list, or confirm the platform release train delivers the decision-record library. |

### RWB-P7-E2028-APP; 11 Delivery and operations/Recovery Workbench Dependency Map v5.xlsx (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-13729 | RWB-PLT-E1027-CON | GAP-1295 | header | Read the H list as None plus six platform contracts and the C list as RWB-P10-E2028-CON plus C RWB-P3-E1043-CON and the P3 read and P4 authorise contracts; story stays Day 1. |

### RWB-P2-E2036-CON (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-13731 | RWB-PLT-E1027-CON | GAP-2412 | n/a | Publish the rwb.decision-record.DecisionRecorded.v1 element names, key and envelope, plus the P3 case-read and P4 authorise shapes and the reference-data operation. |

### OTHER:RWB-S5-E3026 story file (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-13732 | RWB-PLT-E1027-CON | GAP-2869 | n/a | Add planned dependency rows for the four consumed contracts and the Schedule library RWB-PLT-E1071-CON; trace both slices to REQ-S5-003. |

### OTHER:Legacy RWB-E4-046 contract baseline (TSD P8 v2 and P8 contract story) (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-13733 | RWB-PLT-E1027-CON | GAP-2548 | n/a | Allocate a contract baseline publishing rwb.payment.TreatmentBooked.v1 and the deliverFile manifest; publish ALS values and the data product code. |

### RWB-S6-E6008-APP (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-13734 | RWB-PLT-E1027-CON | GAP-3006 | n/a | Record the four reads and the interface call as class C dependencies; add REQ-S6-008; carry posting result in the decision record and case state. |

### RWB-S7-E6017-APP (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-13735 | RWB-PLT-E1027-CON | GAP-3025 | n/a | Record five consumed rows as class C, add RWB-PLT-E1072-CON, RWB-P7-E1073-CON and RWB-PLT-TE006-CON, and add a routing requirement row. |

### RWB-S7-E6021-APP (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-13736 | RWB-PLT-E1027-CON | GAP-3033 | n/a | Record four consumed rows as class C; treat DP-05 as consumed on rwb-source-data; add REQ-S7-002 and REQ-S7-005 at D1. |

### RWB-S7-E6025-APP (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-13737 | RWB-PLT-E1027-CON | GAP-3041 | n/a | Record five consumed rows as class C; add RWB-PLT-E1072-CON, RWB-P7-E1073-CON and RWB-PLT-TE006-CON as tracked dependencies; read the scheduler marker as the workflow timer. |

### RWB-S8-E7001-APP (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-13739 | RWB-PLT-E1027-CON | GAP-3051 | n/a | Add C rows for the document and source-data reads; name EV-06 and EV-07 as DeviationRaised and DeviationCleared; add RWB-PLT-TE006-CON; add AC for the happy path. |

### RWB-S8-E7002-APP (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-13740 | RWB-PLT-E1027-CON | GAP-3053 | n/a | Add class C rows for four consumed contracts; add RWB-PLT-TE006-CON, RWB-PLT-E1072-CON and RWB-P7-E1073-CON; adopt REQ-S8-002, REQ-DVH-005, REQ-S8-004. |

### RWB-S8-E7003-APP; RWB-S8-E7003-CON (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-13741 | RWB-PLT-E1027-CON | GAP-3055 | header | Record rwb-source-data, rwb-case, rwb-access and rwb-decision rows as class C in fact; add DP-04, DP-09 and DP-10 rows; record the escalation level in the rule row. |

### RWB-S8-E7004-APP (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-13742 | RWB-PLT-E1027-CON | GAP-3057 | header | Record the two rwb-case rows and two rwb-decision rows as class C in fact; add DP-04, DP-05 and DP-09 rows; publish a list of values for the deviation state. |

### 02 Business architecture and process/Recovery Workbench Business Rules and Routing Logic v4.xlsx (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-13743 | RWB-PLT-E1027-CON | GAP-3059 | header | Carry claim deadline, SLA and Legal route as versioned reference rows with placeholders; trace both slices to FEAT-DVF-05. |

### RWB-S8-E7006-APP (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-13744 | RWB-PLT-E1027-CON | GAP-3061 | header | Record the four consumed rows as class C in fact with placeholders and fakes; record absent DP-05, DP-09, DP-14 and DP-20 rows in the registers. |

### 22 Microservice Realignment/Recovery Workbench Microservice Change Register v1.md (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-13746 | RWB-PLT-E1027-CON | GAP-0152 | header | Record the retirement of RWB-E1-014 with no new story; keep FEAT-RDF-20, FEAT-DRI-06 and FEAT-RPT-04 rows unchanged; drop E1-014 dependencies. |

### OTHER:Legacy step RWB-E4-043 story (data table) and DP-05 pattern (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-13748 | RWB-PLT-E1027-CON | GAP-1365 | header | Read receipts on the rwb-source-data contract, treatment on S2 GET /treatments/{treatmentId}, case on rwb-case contract, and write the decision record locally through RWB-PLT-E1027-CON. |

### 11 Delivery and operations/Recovery Workbench Dependency Map v5.xlsx; OTHER:S4 rwb-litigation) (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-13749 | RWB-PLT-E1027-CON | GAP-2760 | header | Carry rwb-document checklist read, case document page read and case-move answer as non-blocking consumed contracts; name the two document reads after the P5 stories. |

### OTHER:Legacy RWB-E4-040 story and the P5 rwb-document story (not in this chunk) (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-13750 | RWB-PLT-E1027-CON | GAP-1156 |  | Make document and document_custody P5 rwb-document rows; rwb-comms declares no custody table or cross-schema key and uses the P5 custody operation with a 2 s budget. Add the P5 custody contract C row to both stories. |

### OTHER:Appeal slices of the litigation plan (not in this chunk) (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-13753 | RWB-PLT-E1027-CON | GAP-2801 |  | Add non-blocking rows for the D7.4 approval (C of its wave), the case and partner contracts built on fakes, RWB-P3-E1043-CON as C, and DP-08 edge and guard rules. |

### OTHER:Batch and Scheduling Design v4; RWB-P4-E8015-APP; 22 Microservice Realignment/Recovery Workbench Architecture v5 Text Extract v1.md (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-13754 | RWB-PLT-E1027-CON | GAP-2296 |  | Add a JOB-nn row for the daily rwb-access chain check; add RWB-PLT-E1071-CON to the H list of RWB-P4-E8015-APP in the dependency map and plan. |

### RWB-S6-E5025-APP (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-13755 | RWB-PLT-E1027-CON | GAP-3014 |  | Keep H, C, I and X rows; carry six consumed rows in 12.2 and fakes in 12.8; hold tape reference and check result in the decision record; record PII service as unmapped; trace REQ-S6-003. |

### RWB-S6-E6007-APP (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-13756 | RWB-PLT-E1027-CON | GAP-3004 |  | Add six consumed rows and RWB-PLT-TE006-CON, RWB-PLT-E1047-CON, RWB-P2-E1007-CON as dependencies; add DP-09 outbox for AccountsTransferred; record transfer on lot status and decision record; split R-DS-25 into one saga. |

### RWB-P4-AD008-APP (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-13757 | RWB-PLT-E1027-CON | GAP-0807 |  | Add RWB-PLT-E1071-CON to Depends on (build) and DP-10 to the pattern row of RWB-P4-AD008-APP. Set the Schedule cron as deployment configuration under the DL38 six-monthly placeholder. Create the Schedule in the operations story of RWB-P4-AD008. |

### RWB-S7-E6015-APP; OTHER:FSD requirement REQ-S7-002 and TSD T8 row (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-13758 | RWB-PLT-E1027-CON | GAP-3021 |  | Keep the H, C, I and X rows. Record the seven consumed contracts as class C in fact with placeholders. Add C RWB-P10-TE013-CON (agent client, DP-20), RWB-PLT-TE006-CON (wave 0 library), RWB-PLT-E1072-CON and RWB-P7-E1073-CON (rule kit). Adopt REQ-S7-002 in the FSD and correct the TSD T8 row. Confirm the SCR-27 read with the Ownership Map owner. |

### RWB-S7-E6013-APP (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-13759 | RWB-PLT-E1027-CON | GAP-3016 |  | Keep the H, C, I and X rows. Record rwb-case, rwb-source-data and rwb-decision as class C in fact with placeholders. Add RWB-PLT-E1072-CON with RWB-P7-E1073-CON (rule kit), RWB-PLT-TE006-CON (outbox and inbox library) and RWB-PLT-E1071-CON (Scheduled job kit). Declare the JOB-16 Schedule and ACE data-ready trigger in the story without registering them. |

### RWB-S6-E5023-APP (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-13760 | RWB-PLT-E1027-CON | GAP-2973 |  | Add C rows for rwb-case, rwb-source-data and rwb-decision; add RWB-PLT-TE006-CON to H; add DP-04 (H RWB-PLT-E1072-CON, C RWB-P7-E1073-CON) and DP-09; adopt REQ-S6-001. |

### RWB-S6-E6011-APP (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-13761 | RWB-PLT-E1027-CON | GAP-3012 |  | Add C rows for the six consumed contracts; add RWB-PLT-TE006-CON to H for DP-09; add DP-04 with its rule kit row and C row RWB-P7-E1073-CON; record the settlement stamp and GL prerequisite. |

### RWB-S7-E6016-APP (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-13762 | RWB-PLT-E1027-CON | GAP-3023 |  | Add the removal operation with placeholder path; add removal_reason field and list placeholder; add C rows for the three consumed contracts; add requirement id; add DP-09 and DP-04 rows. |

### OTHER:RWB-S6-E5023 story (APP and CON slices) (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-13764 | RWB-PLT-E1027-CON | GAP-1947 |  | Keep plan metadata rows as stated; declare the four consumed rows in 12.2 with operation-name placeholders and fakes from 12.8; read DEBTSALE package as data; trace REQ-S6-001. |

### RWB-S6-E5024-APP (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-13765 | RWB-PLT-E1027-CON | GAP-2975 |  | Add C rows for rwb-case, rwb-source-data, rwb-agent and rwb-decision; add RWB-P10-TE013-CON and RWB-PLT-TE006-CON to H; add DP-04 rows; adopt REQ-S6-002. |

### RWB-S7-E6023-APP (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-13766 | RWB-PLT-E1027-CON | GAP-3037 |  | Fix the posting product and its event on the rwb-source-data contract with a matching cross-reference; hold three consumed rows as class C; record no provided operation or Schedule; trace REQ-S7-005. |

### RWB-S5-E3019-APP (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-13768 | RWB-PLT-E1027-CON | GAP-2837 |  | Add C rows for rwb-source-data and rwb-case; add RWB-PLT-TE006-CON to H; add the asset row to the Ownership Map; adopt REQ-S5-001; state that only RWB-S5-E3023-APP runs the R-DIS-06 clocks. |

### OTHER:RWB-S5-E3021 split plan slices (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-13769 | RWB-PLT-E1027-CON | GAP-2847 |  | Keep H, C, I and X rows as stated; declare AuctionResult event and three consumed REST rows with Day 1 fakes; record RWB-PLT-TE006-CON as the wave 0 outbox and inbox library. |

### RWB-S6-E6004-APP (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-13770 | RWB-PLT-E1027-CON | GAP-2988 |  | Record the five consumed rows as class C with placeholders; add RWB-PLT-TE006-CON as the wave 0 library; fix API-S6-005 as this key's operation; keep one writer per rule (R-DS-18 here, R-DS-34 claim in RWB-S6-E6009-APP); hold bid amount, time and reference until the column set is added. |

### RWB-S7-E6018-APP (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-13771 | RWB-PLT-E1027-CON | GAP-3027 |  | Record the five consumed rows as class C with placeholders; read delegation_limit as reference data on the rwb-case contract; record approver and limit in the local decision record; carry R-WO-13 and R-WO-14 out of scope; claim EV-24 for the approved path; add RWB-PLT-TE006-CON as the library. |

### RWB-S1-E4007-APP (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-13772 | RWB-PLT-E1027-CON | GAP-2624 |  | Service owner or delivery lead confirms whether RWB-S1-E4005-APP and RWB-S1-E4006-APP are build dependencies; if confirmed, add them to the H row and set ready-to-start to 'After RWB-S1-E4005-APP, RWB-S1-E4006-APP'. |

### RWB-S4-E5008-APP (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-13773 | RWB-PLT-E1027-CON | GAP-2773 |  | Name the rwb-partner panel and instruction reads and the rwb-case case-move answer as consumed rows of both stories; build against published documents and fakes with a 2 s budget and a breaker; step D1 decides the C row and partner contract story. |

### OTHER:Deferral step story lines (both stories) (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-13774 | RWB-PLT-E1027-CON | GAP-2829 |  | Declare the rwb-case read, the rwb-case answer with stage move, queue placement and task request, and the rwb-decision package read as consumed rows in 12.2; fake them on Day 1; keep metadata rows; add C rows when owners publish operation names. |

### RWB-S5-E3024-APP (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-13775 | RWB-PLT-E1027-CON | GAP-2860 |  | Define the figure as the count of asset rows with book_value and holding_cost_to_date totals per holding_status for LOV-SEGMENT and an as-at date; serve it as AssetStockBalance on GET /assets; owner role RW-NPAMGR; R-DIS-01 and R-DIS-02 sit with RWB-S5-E3019-APP and RWB-S5-E3020-APP. |

### RWB-S5-E3019-APP; RWB-S5-E3019-CON (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-13776 | RWB-PLT-E1027-CON | GAP-1906 |  | Keep the H, C, I and X rows; add the rwb-source-data, rwb-case and DP-09 rows as dependencies; declare AssetTakenOn from the outbox on rwb.asset.events.v1; read the case move as the workflow stage outcome; read REQ-S5-001 with a note that the plan carries no requirement id. |

### RWB-S6-E5024-APP; RWB-S6-E5024-CON (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-13777 | RWB-PLT-E1027-CON | GAP-1952 |  | Keep the H, C, I and X rows; record the rwb-source-data, rwb-agent, rwb-case and rwb-decision rows as class C dependencies; fake each on Day 1; read the case move as the workflow stage outcome; keep the DP-04 and DP-09 rows in this register. |

### RWB-S6-E5026-APP (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-13778 | RWB-PLT-E1027-CON | GAP-2977 |  | Keep the H, C, I and X rows; record rwb-document, rwb-partner and rwb-case as class C dependencies with placeholders and fakes; record the partner DMZ channel as an edge dependency with no plan row; reference the tape and never build it; write no lot status of the opening; adopt REQ-S6-003 and FEAT-DBS-04. |

### RWB-S6-E5026-APP; RWB-S6-E5026-CON (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-13779 | RWB-PLT-E1027-CON | GAP-1958 |  | Declare the rwb-document tape read, rwb-partner panel read and rwb-case case-move answer as class C dependencies; build against their published documents and fakes on Day 1; keep the C row as the plan states it; trace REQ-S6-003 from the programme and the FSD. |

### RWB-S6-E6003-APP (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-13781 | RWB-PLT-E1027-CON | GAP-2986 | n/a | Keep H row; build against six contract fakes with 2 s budget and breaker; declare no provided operation; carry three placeholders; delegate re-offer to R-DS-28 at RWB-S6-E5005-APP; record wave conflict once. |

### RWB-S6-E6009-APP (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-13782 | RWB-PLT-E1027-CON | GAP-3008 | n/a | Keep plan rows; record five consumed rows as class C with placeholders; declare no provided operation; read claim window as versioned parameter with placeholder; hold realized recovery on account selling_price and closed lot. |

### RWB-S6-E6001-APP (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-13783 | RWB-PLT-E1027-CON | GAP-1963 | n/a | Add five C rows (P7 approval chain, P7 rule-package read, P4 delegation_limit, P3 case state read, P3 case-move answer) and the rwb-decision queue dependency to the dependency map. |

### RWB-S6-E6005-APP (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-13785 | RWB-PLT-E1027-CON | GAP-2990 | n/a | Declare six consumed rows in 12.2 with owners, budget and placeholder; fake them for build; keep metadata C row as the plan states it. |

### RWB-S6-E6010-APP (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-13786 | RWB-PLT-E1027-CON | GAP-3010 | n/a | Keep plan rows; record rwb-case, rwb-access and rwb-decision rows as class C with placeholders; declare no provided operation; name API-S6-003 of RWB-S6-E6005-APP as start signal; run unattended step under rwb-debtsale identity. |

### RWB-S6-E6006-APP (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-13787 | RWB-PLT-E1027-CON | GAP-2996 | n/a | Build against plan H row and owners' fakes; declare six rows in 12.2 with placeholders and in 12.8 with fakes; add C rows of P5, P6, P1, P3 and P7 to the plan key. |

### RWB-S7-E6022-APP (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-13788 | RWB-PLT-E1027-CON | GAP-3035 | n/a | Keep plan rows; record four reads and feed call as class C with placeholders; declare no provided operation; name API-S7-001 and API-S7-002; carry feed status and references in decision record and case state; hold with MSG-S7-001. |

### RWB-S7-E6024-APP (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-13789 | RWB-PLT-E1027-CON | GAP-3039 | n/a | Add correction operation on write-off base with placeholder path and elements; take vocabulary from three rule events; read retry count from posting step and limit from WO package; carry R-WO-41 and R-WO-43 as other entries. |

### RWB-S7-E6027-APP (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-13790 | RWB-PLT-E1027-CON | GAP-3046 | n/a | Declare the recovery act event-driven with no own operation; consume the P8 payment event with a placeholder name and payload; read ACE facts and the fee reference as proposed; raise the reporting gap; fill the plan C row. |

### OTHER:FSD S8; OTHER:TSD S8; OTHER:UNIVERSAL rule set, rwb-access and rwb-source-data contracts (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-13791 | RWB-PLT-E1027-CON | GAP-3070 | n/a | Publish a UNIVERSAL rule row for a contact sent under a contact stop; decide breach storage on deviation; publish the interaction-ledger read and SCR-08 breach read; correct RW-CONDUCT right; settle service level with DL22. |

### OTHER:Service owner P7 rwb-decision: audit search specification (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-13796 | RWB-PLT-E1027-CON | GAP-2075 | n/a | Audit search reads the ledger only and shows a committed entry as not yet sealed until JOB-13 collects it; strict mode waits for ledger acknowledgement of its own record. |

### OTHER:Story whose metadata carries the eight patterns and Depends on (build) empty (key not in chunk; RWB-PLT-E1027-CON (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-13797 | RWB-PLT-E1027-CON | GAP-2429 |  | Keep the metadata rows as the WP fixes them. Name the five H rows (RWB-PLT-E1027-CON, RWB-PLT-E1043-CON, RWB-PLT-E1071-CON, RWB-PLT-E1044-CON, RWB-PLT-N001-CON), C row RWB-P3-E1043-CON and the DP-11 authorise contract in its pattern table and the fakes of section 12.8. Build against fakes from Day 1; step D1 decides the dependency map. |

### RWB-S8-E1023-APP (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-13798 | RWB-PLT-E1027-CON | GAP-3082 |  | Keep the service, lane, C row RWB-P3-E1023-CON and empty H row. Record the slice as secondary serving of the page with its own deviation block and assembly, and the case header consumed from RWB-P3-E1023-CON. Declare RWB-PLT-E1027-CON, RWB-PLT-E1042-CON, RWB-PLT-E1043-CON, RWB-PLT-E1037-CON, RWB-PLT-E1047-CON, RWB-PLT-E1044-CON and RWB-PLT-N001-CON as build prerequisites and fakes. Keep wave 1 by R5.6 with release tentative. |

### OTHER:Batch and Scheduling (next version) (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-13799 | RWB-PLT-E1027-CON | GAP-1240 |  | Mark JOB-13 as retired; keep the continuous ingest in RWB-P7-E1008-APP and JOB-14 (02:00 hash-chain check) as the only P7 Schedule. |

### OTHER:FSD P7 module specification (next version) (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-13800 | RWB-PLT-E1027-CON | GAP-1239 |  | Delete A2.6 (FEAT-DRI-06) and its criteria AC-P7-006-01 to AC-EXC-P7-006-04; move the reporting need to the rwb-reporting projection from events. |

### RWB-S9-E1032-APP (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-13801 | RWB-PLT-E1027-CON | GAP-3140 |  | Keep the H list as the WP fixes it. Record the DP-03, DP-06, DP-07, DP-09, DP-10, DP-15 and DP-19 platform rows (RWB-PLT-E1027-CON, RWB-PLT-E1042-CON, RWB-PLT-E1043-CON, RWB-PLT-TE006-CON, RWB-PLT-E1071-CON, RWB-PLT-E1044-CON, RWB-PLT-N001-CON) as the wave 0 shared baseline. |

### RWB-P3-E1050-APP (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-13802 | RWB-PLT-E1027-CON | GAP-0767 |  | Write the decision record as a local row in the rwb_case decision-record table from the service baseline. Publish no DecisionRecorded event and claim no platform dependency. If the ledger is required, add DP-03 and RWB-PLT-E1027-CON to this story. |

### RWB-P3-E1052-APP (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-13803 | RWB-PLT-E1027-CON | GAP-0754 | metadata and pattern table | Keep the metadata rows as the work package gives them (H empty). Hold the platform contract dependencies RWB-PLT-E1027-CON, RWB-PLT-E1043-CON, RWB-PLT-TE006-CON, RWB-PLT-E1044-CON and RWB-PLT-N001-CON in the pattern table and preconditions. Keep Ready to start Day 1. |

### RWB-P6-E1073-APP (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-13805 | RWB-PLT-E1027-CON | GAP-1218 | H list and lane document | Add RWB-PLT-E1027-CON, RWB-PLT-E1072-CON, RWB-PLT-E1042-CON, RWB-PLT-E1043-CON, RWB-PLT-E1071-CON, RWB-PLT-E1047-CON, RWB-PLT-E1044-CON and RWB-PLT-N001-CON to the H list. Keep Ready to start Day 1. |

### RWB-S8-E2012-APP (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-13810 | RWB-PLT-E1027-CON | GAP-3091 | 13 | No plan change: keep Depends on (build) None and Day 1; track the eight platform H rows in section 13 of the owning story. |

### RWB-P6-E2014-APP (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-13811 | RWB-PLT-E1027-CON | GAP-2389 | 13 | Keep H empty; add six platform contracts and two rwb-case contracts to the C list at next plan revision. |

### OTHER:Work Package B2-P4-021 line (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-13814 | RWB-PLT-E1027-CON | GAP-2312 | 13 | Keep H [] and C [RWB-P8-E2027-CON] as fixed; confirm at the wave 2 planning gate that no H chain is missing from the lane. |

### OTHER:Work Package build sequence (document not named in the item) (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-13815 | RWB-PLT-E1027-CON | GAP-2410 | header | Record that a secondary slice builds against platform contracts and published fakes and reads same-service wave-1 rows through its own schema. |

### RWB-P7-E2042-APP (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-13816 | RWB-PLT-E1027-CON | GAP-1296 | header | Keep metadata as written; carry the eight H and three C DP-added dependencies in its dependency map; Ready to start stays Day 1. |

### RWB-P6-E5002-APP (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-13817 | RWB-PLT-E1027-CON | GAP-1190 | header | Add RWB-PLT-E1027-CON and RWB-PLT-N001-CON to the build list of RWB-P6-E5002-APP when the plan is regenerated; seams build against fakes meanwhile. |

### OTHER:TSD P4 v3 T6.3 and the rwb-access rule-version approval story (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-13818 | RWB-PLT-E1027-CON | GAP-0830 | 13 | Write one approval entry with a decision code from the DP-03 decision-code list, carrying the package, version label, status change and outcome, in the local transaction before the registry call. |

### RWB-P6-E4035-APP (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-13819 | RWB-PLT-E1027-CON | GAP-2368 |  | Add the S2 and P1 contract stories to the C list and the S8 event rows to the I list when planned; keep the drift test as the guard until then. |

### OTHER:Work Package plan: wp/B-P4-04.md and wp/B2-P4-010.md (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-13820 | RWB-PLT-E1027-CON | GAP-2278 |  | Keep one owner for legacy RWB-AD-016 on rwb-access; number CG and ASM rows once; add a plan-uniqueness check to checks/run_all.py. |

### RWB-S5-E4030-APP (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-13821 | RWB-PLT-E1027-CON | GAP-2953 |  | Declare inbox and outbox as platform capabilities, add no new H row this wave, and raise the platform build dependency question at next plan revision. |

### RWB-S3-E4015-APP (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-13822 | RWB-PLT-E1027-CON | GAP-2716 |  | Add contract rows for the P7 rwb-decision GUARANTEE package and the P3 rwb-case reference data at next plan revision, or declare both as template capabilities. |

### OTHER:split_plan.json entry for RWB-S4-E5011 (WP legacy record) (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-13823 | RWB-PLT-E1027-CON | GAP-2790 |  | Add dependency rows for DP-04, DP-06 and DP-07 centrally at plan revision; name the rule package read and reference-data ride on the 12.2 contract rows. |

### 09 Testing and quality/Recovery Workbench Requirements Traceability Matrix v7.xlsx; 09 Testing and quality/Recovery Workbench Test Cases v8.xlsx (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-13835 | RWB-PLT-E1037-APP | DOR-RWB-PLT-E1037-APP-12 | 16, 18 | Add TC-PLT-E1037-APP-01 to TC-PLT-E1037-APP-07 to Test Cases v8, and align the section 18 test lists to RTM v7. |

### OTHER:Technical Specification P1 v3 (TSD P1) T3.6 (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-13837 | RWB-PLT-E1037-APP | GAP-0481 | 3 | Remove masking_rule from the P1 schema and the masking step from P1; keep data_product_access only; P1 takes the answer from POST /api/recovery/access/v1/authorise and FieldMasker of RWB-P4-E1037-CON. |

### API:(service not named); OTHER:T3.1 (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-13838 | RWB-PLT-E1037-APP | GAP-1568 | find it | Publish POST /authorise, GET /me/permissions, GET /doa-limits and /masking-policies with request and answer schemas, refusal and not-found codes, version fields and masking marker vocabulary; state group-to-role resolution and session behaviour on role retirement in T3.1. |

### OTHER:P3 rwb-case export story (RWB-E1-031 split) (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-13839 | RWB-PLT-E1037-APP | GAP-0355 | find it | Read the export entry back through the P4 access-log contract with AC-EXPT, filters and row count; apply P4 masking rules over P1 masked columns; keep owner display names synthetic in SIT. |

### OTHER:TSD P3 v3 (API-P3-001; RWB-P4-E1039-CON (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-13840 | RWB-PLT-E1037-APP | GAP-2208 | find it | Add team as an additive optional filter on GET /cases; name the rwb-access access-log operation with AC-EXPT fields in RWB-P4-E1039-CON; record that masking rules travel in the authorise answer. |

### OTHER:v4 data dictionary (Fields sheet; OTHER:DF-DOC-089 and DF-DOC-015) (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-13847 | RWB-PLT-E1037-APP | GAP-0262 | 2 | Data steward to decide classification; apply Restricted handling meanwhile: never in an event, workflow input or log; page id only in a log. |

### API:(service not named) (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-13853 | RWB-PLT-E1037-APP | GAP-0779 | n/a | Keep load and approve on /api/recovery/access/v1 for rwb-access tables, with lists and other reference data on rwb-case; publish /api/recovery/access/v1/masking-policies (Reference data R); publish AccessPolicyChanged with change kind, version and effective date, no personal value; one matrix-read contract. |

### OTHER:Security and Access Design v5 (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-13855 | RWB-PLT-E1037-APP | GAP-2035 | n/a | Write section 7 per service: one login rwb_<short name> per service with grants on own schema only; rwb_source_data sole holder of the view grant on the v_ace_* views; replace the recovery_svc isolation row with a service login row; state the change in the realignment table. |

### OTHER:TSD P4 v3 T3.1 and the reference data source (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-13856 | RWB-PLT-E1037-APP | GAP-1574 | n/a | Publish the approved role conflict list with its version label and effective dates; add matrix version effective-date columns to T3.1 or state the date lives on the load; confirm the role and permission row counts of the version in force. |

### OTHER:Security and Access Design v4 (access log, section 1) (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-13858 | RWB-PLT-E1037-APP | GAP-2076 | n/a | The access row records the version the owning service applied at the event time; the rwb-decision registry stays the source of the version and its effective date; owners P4 rwb-access and P7 rwb-decision. |

### RWB-P4-E1037-CON; 02 Business architecture and process/Recovery Workbench Users Roles and Permissions v5.xlsx (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-13859 | RWB-PLT-E1037-APP | GAP-0166 | n/a | State that the six SY actors resolve through POST /authorise with their SY role code and managed identity as subject; the credential type is left to the P4 contract story. |

### OTHER:RWB-P1 and RWB-P4 CON stories (rwb-source-data, rwb-access) (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-13860 | RWB-PLT-E1037-APP | GAP-0248 | 8 | State that the masking function stays in the recovery view schema with the views, the policy rows stay in rwb_access, and rwb-source-data applies the mask in the view and in its responses. |

### OTHER:RWB-S9 rwb-partner and RWB-P4 rwb-access stories (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-13861 | RWB-PLT-E1037-APP | GAP-2041 | 8 | Name the S9 rwb-partner administrator as creator and ender of partner users, with roles held as P4 role rows granted by the P4 role owner, both written to the access log. |

### 05 Technical architecture/Recovery Workbench API Specification v5/asyncapi/rwb.decision-record.v1.asyncapi.yaml (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-20853 | RWB-PLT-E1027-CON | R-22320 |  | GAP-1332: element names and inputs snapshot shape are in no source and need the hand-over contract owner. Not invented. |

## 6. Register gaps linked to this service (Gap Register v2 status)

| GAP ID | Title | Owner role | Status |
|---|---|---|---|
| GAP-0013 | ACE Common contracts are not versioned or scheduled | ACE team | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-0152 | Three live features carry story key A14, whose legacy story RWB-E1-014 D-RCV-60 retires with no new story | Solution architect of P7 rwb-decision and the reporting lead of P9 rwb-reporting | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-0159 | The four authorise operations have no request, response or error schema in any source | TechX | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-0160 | The sign-in permission read has two names, /me/permissions and /me/session | TechX | Resolved (directive) |
| GAP-0161 | No cache lifetime and no rule for a failed authorise call | TechX | Resolved (directive) |
| GAP-0164 | Partner roles sit in the roles table while the partner user is owned by S9 | Partner and agency manager | Resolved (directive) |
| GAP-0166 | How the six non-human actors authenticate is not stated | Security administrator | Resolved (directive) |
| GAP-0168 | The Key tab scope values do not include REGION, which the access story uses | TechX | Resolved (directive) |
| GAP-0248 | The masking function and the masking policy have no stated home after the schema split | Security architect | Resolved (directive) |
| GAP-0262 | OCR text is classified Not personal while the same content at field level is Restricted | Data steward | Resolved (directive) |
| GAP-0264 | The PII log path is named PII Kafka with no owner and no separation from the business topics | Security team | Resolved (directive) |
| GAP-0352 | E1027 decision codes and reference data move to P3 while the writer and the ledger are PLT and P7 | Solution architect | Resolved (directive) |
| GAP-0355 | Export access entry, masking source and owner display name path are not named for the target | Tech lead | Resolved (directive) |
| GAP-0358 | Matrix load owner, masking read path and the platform library boundary are not named for the target | Solution architect | Resolved (directive) |
| GAP-0481 | The masking rules stay in P1 in the TSD while the Ownership Map rules the table to rwb-access (P4) | Solution architect | Resolved (directive) |
| GAP-0542 | decision_log_entry is P7's and the target writes a local decision record plus the shared topic, while no source says whether the migrated legacy entries are published as records or handed over as a file, or who continues the hash chain | Solution architect | Resolved (directive) |
| GAP-0584 | Two sources give the masking of a ledger field to two different services | Tech lead | Resolved (directive) |
| GAP-0637 | The operation path of a configuration change, the record payload members, the approval instant, the kind value set and the state mapping are not fixed by one source | Solution architect with the service owner of rwb-agent and the owners of rwb-decision and rwb-access | Resolved (directive) |
| GAP-0672 | rwb-integration rule copy: the H and C rows, the model-fetch surface, the assigned package, the local copy table, the event consumers and the login are not settled by any one source | Solution architect | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-0673 | rwb-integration ALS settlement booking: the interface itself, the modelling of INT-03, the field mapping, the metadata rows and the login are not settled by any one source | Solution architect | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-0754 | The platform contract dependencies of the pattern table are not carried in the metadata rows | RW-COE | Resolved (directive) |
| GAP-0767 | The decision record is written here although DP-03 and its library story are not applied | Solution architect | Resolved (directive) |
| GAP-0778 | Missing and conflicting values in the rwb-access matrix and masking slice (RWB-P4-E1037-APP) | Solution architect | Resolved (directive) |
| GAP-0779 | The load, approve and masking-policy contract of rwb-access has a missing path and a conflicting owner (RWB-P4-E1037-CON) | Solution architect | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-0807 | rwb-access access review list: JOB-18 is a Temporal Schedule but the story metadata carries no workflow-kit dependency and no cron | Solution architect and the platform workflow owner | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-0830 | rwb-access rule-version approval: the decision code and the entry fields of an approval record are not specified | Solution architect | Resolved (directive) |
| GAP-0984 | rwb-access local decision-record store: the column set behind the five named columns, the canonical form, the genesis value, the verifier behaviour on write and read, the DECISION_LOG letters per role and the per-service login are not specified | Solution architect | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-1156 | document_custody is a P6 module table in the legacy story and a P5 rwb-document table in the target, and the P5 custody contract has no C row and no contract story | solution architect with the P5 rwb-document owner | Resolved (directive) |
| GAP-1161 | The dependencies DP-03, DP-07, DP-09, DP-10 and DP-19 add are absent from this story's build and contract lists, and no fake is named for the reference data or the decision record | Solution architect | Resolved (directive) |
| GAP-1167 | RWB-P6-E1011-APP: the seven platform CONs added by DP-03, DP-06, DP-07, DP-10, DP-14, DP-15 and DP-19 are missing from the story's H list | Solution architect | Resolved (directive) |
| GAP-1190 | The platform contract rows that DP-03 and DP-19 add are not in this story's build list | Tech lead | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-1196 | DP-03 and its decision-record library are missing from the pattern set and the build list of the e-signature key | Solution architect | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-1198 | The DP-added platform and P3 contracts are missing from the story dependency rows | Release manager | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-1218 | RWB-P6-E1073-APP: the platform H dependencies that DP-03, DP-04, DP-06, DP-07, DP-10, DP-14, DP-15 and DP-19 add are absent from the story's H list | Tech lead | Resolved (directive) |
| GAP-1223 | The plan's H and C lists for this story name None and RWB-P7-E2013-CON, and omit the platform and published contracts that the DP table adds | Delivery lead | Resolved (directive) |
| GAP-1235 | The decision-record write operation is absent from the Ownership Map | Solution architect | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-1236 | The full record shape, the data-date column, the inputs digest and the message catalogue entry format are not specified | Data steward | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-1237 | The canonical form of the entry hash is not specified | Solution architect | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-1238 | Two ce_type values are published for DecisionRecorded | Solution architect | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-1239 | The decision-log stream to the data lake is retired but still specified | Business analyst | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-1240 | JOB-13 is a 01:00 copy job in the specifications and a continuous ingest in the target | Solution architect | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-1245 | Scope predicate and Compliance incident queue of the audit read have no owner document | Solution architect, with the P4 access owner and the P3 case owner | Resolved (directive) |
| GAP-1250 | Access record of a query: local decision record or the rwb-access access log | Solution architect, with the P4 access owner | Resolved (directive) |
| GAP-1277 | The DP table adds platform and published dependencies, and two service baselines, that the metadata rows of the story do not carry | Solution architect, P7 rwb-decision, with the platform team and the rwb-case team | Resolved (directive) |
| GAP-1279 | rwb-decision login, migration file and sequence, constraint and index names, standard-column Field IDs, the dictionary handover and the platform-contract carriage are not fixed by any source | Solution architect | Resolved (directive) |
| GAP-1282 | The DP table adds platform and published dependencies that the metadata rows of the story do not carry | Solution architect, P7 rwb-decision, with the platform team, the rwb-case team and the rwb-access team | Resolved (directive) |
| GAP-1286 | The DP table adds platform and published dependencies that the metadata rows of the story do not carry | Solution architect, P7 rwb-decision, with the platform team and the rwb-case team | Resolved (directive) |
| GAP-1288 | The DP table and the service baseline add platform, store and published dependencies that the metadata rows do not carry | Solution architect, P7 rwb-decision, with the platform team, the rwb-case team and the rwb-access team | Resolved (directive) |
| GAP-1291 | The DP table adds platform and published contracts that the metadata rows do not carry | Delivery lead, with the platform contract owners | Resolved (directive) |
| GAP-1295 | The metadata rows name no build dependency and the agent contract only, while the DP table of the story adds six platform contracts and one rwb-case contract and the story consumes two further operations | Delivery lead | Resolved (directive) |
| GAP-1296 | The DP-added H and C dependencies of RWB-P7-E2042-APP are absent from the metadata rows | Solution architect | Resolved (directive) |
| GAP-1308 | The DP table adds platform and published dependencies that the metadata rows of the story do not carry | Solution architect with the platform team, the rwb-case team and the rwb-access team | Resolved (directive) |
| GAP-1312 | The DP table adds two platform contracts and the story consumes three operations that its metadata rows do not carry | Solution architect, P7 rwb-decision, with the platform team and the rwb-access team | Resolved (directive) |
| GAP-1319 | The DP table adds platform and published dependencies that the metadata rows of the story do not carry | Solution architect, P7 rwb-decision, with the platform team and the rwb-case and rwb-access teams | Resolved (directive) |
| GAP-1328 | RWB-P7-E1073-APP: the DP table adds eight platform H rows, one C row and one PLT object set that the metadata rows of the plan do not carry, and DP-04 points its C row at this service's own contract story | Solution architect with the platform library owner and the rwb-decision service owner | Resolved (directive) |
| GAP-1332 | Envelope and payload element names of DecisionRecorded, and the shape of the inputs snapshot | Solution architect | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-1335 | Platform and published dependencies added by the patterns but not carried in the metadata rows | Delivery lead | Resolved (directive) |
| GAP-1336 | Shape of the model answer, of the inputs snapshot and of the announcement, with the carrier names of the plan-status move | Solution architect | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-1337 | Platform and published dependencies added by the patterns but not carried in the metadata rows | Delivery lead | Resolved (directive) |
| GAP-1338 | One ledger entry per route move or per case and business date, for a move that runs two rules | Solution architect | Resolved (directive) |
| GAP-1339 | Values of the RESTRUCTURE catalogue and plan-timer ledger slice that no source fixes | Solution architect | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-1340 | DP-added platform and published dependencies are not carried in the metadata rows | Solution architect | Resolved (directive) |
| GAP-1343 | The platform and published dependencies this slice adds through the decoupling patterns are not carried by the empty metadata rows | Solution architect | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-1347 | RWB-E2-008: the three event payloads and the decision-record element are not fixed by any source | Solution architect | Resolved (directive) |
| GAP-1365 | The legacy step reads v_ace_payment and four other modules tables in process | Solution architect | Resolved (directive) |
| GAP-1402 | Local decision-record library: artefact coordinates, no-case publish path, chain scope and incident routing | Solution architect | Resolved (directive) |
| GAP-1403 | Local decision-record contract: record schema, table shape, shared-topic envelope and message catalogue | Solution architect | Resolved (directive) |
| GAP-1404 | Library artefact coordinates, the policy cache time to live, the authorise payload and the split of the masking read between P4's policy and P1's read are not specified | Platform library architect with the P4 rwb-access owner and the P1 rwb-source-data owner | Resolved (directive) |
| GAP-1405 | The contract shapes of the guard and masker, the /masking-policies path, the audit record shape and the failure mapping are not specified | Platform library contract owner with the P4 rwb-access contract owner | Resolved (directive) |
| GAP-1564 | The load, verify, approve and rollback surface of the permission matrix and the delegation of authority table is rwb-case's under the Ownership Map, while the tables and every validation rule that decides a refusal are rwb-access's | Solution architect with the rwb-case contract owner | Resolved (directive) |
| GAP-1568 | The four operations Architecture v5 gives rwb-access first (authorise, /me/permissions, /doa-limits, /masking-policies) have no request or answer schema in the API Specification v4 or the P4 appendix, and the group-to-role mapping has no stated read path | Solution architect | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-1569 | AccessPolicyChanged and DoaLimitChanged are published by rwb-access in Architecture v5 but have no row, payload, key or refresh window in the event design | Solution architect with the platform event owner | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-1574 | No source holds the full role conflict list, the role and permission row counts of a version, or the effective-date column of a matrix version | Security administrator with the reference data administrator | Resolved (directive) |
| GAP-1617 | The ledger completeness target, the gap alert threshold and the strict-mode wait bound have no value in the BRD or the FSD | Solution architect with the platform administrator | Resolved (directive) |
| GAP-1622 | The decision record is published by 19 services on one topic with no schema version field in the field list | Platform event library owner | Resolved (directive) |
| GAP-1885 | Three consumed contracts and two platform reads of the petition have no dependency row, and two of the three operation names exist in no source | Solution architect, S4 rwb-litigation, with the P7 rwb-decision, P3 rwb-case and S9 rwb-partner architects and the platform team | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-1906 | RWB-S5-E3019: the take-on slice has no source for its dependency rows, its event, its case move, its requirement id and the duplicated R-DIS-06 criterion | Solution architect | Resolved (directive) |
| GAP-1946 | RWB-S5-E1011-APP: the asset slice of RWB-E1-011 has no source for its dependency lists, its ACE-side read, its quality objects, its rights and its run cadence, and the data-lake and Power BI target of the legacy key is removed | Solution architect | Resolved (directive) |
| GAP-1947 | RWB-S6-E5023: the eligibility slice has no C row for its four consumed rows, no DP-04 row and no requirement id | Solution architect | Resolved (directive) |
| GAP-1952 | RWB-S6-E5024: the lot build and price step needs rwb-source-data, rwb-agent, rwb-case and rwb-decision while the plan's C row is empty | Solution architect | Resolved (directive) |
| GAP-1958 | RWB-S6-E5026: the data-room slice carries an empty C row although it needs rwb-document, rwb-partner and rwb-case, and the plan holds no requirement id | Solution architect | Resolved (directive) |
| GAP-1963 | RWB-S6-E6001: the plan gives this step an empty C row while it consumes rwb-decision, rwb-access and rwb-case, and two of the consumed operations have no published name | Solution architect | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-1969 | RWB-S6-E6002: the qualification slice has no C row, no requirement id and no case-move or authorise operation although it needs rwb-partner, rwb-case, rwb-decision and rwb-access | Solution architect | Resolved (directive) |
| GAP-2035 | The source keeps one recovery schema and one recovery_svc login; Architecture v5 has 19 schemas and 19 logins | Architecture with the ACE DBA | Resolved (directive) |
| GAP-2036 | The authorise contract has no request or response shape in any source | TechX with P4 rwb-access | Resolved (directive) |
| GAP-2039 | The access log is named as an rwb_access object but has no row in the Ownership Map | P4 rwb-access with the ACE DBA | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-2041 | Partner users moved to S9 rwb-partner, while the approving role owner stays in P4 | S9 rwb-partner with P4 rwb-access | Resolved (directive) |
| GAP-2063 | The edge components have no owner row in the Ownership Map, and section 5 needs one | Platform (RWB-PLT-EDGE) with S9 rwb-partner | Resolved (directive) |
| GAP-2068 | The local decision record has no table, no DDL and no case or trace column | Service owners of the 19 services with P7 rwb-decision | Resolved (directive) |
| GAP-2074 | One chain or 19 chains plus the ledger chain | Service owner P7 rwb-decision with the 19 service owners | Resolved (directive) |
| GAP-2075 | The record that governs while the central ledger lags by up to five minutes | Service owner P7 rwb-decision | Resolved (directive) |
| GAP-2076 | The versions in force in the access log come from two services | Service owners P4 rwb-access and P7 rwb-decision | Resolved (directive) |
| GAP-2176 | decision_log_entry is P7's, the record is local and the ledger is central, and no source says whether the migrated legacy entries are published as records or handed over as a file, nor who continues the hash chain | Solution architect | Resolved (directive) |
| GAP-2208 | Four target-side facts of the case list and its export are not fixed by any source, and the sources disagree on the team filter | Solution architect | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-2252 | The decision code and the payload of the decision records the seed writes are not in the sources | TechX and the rwb-decision contract owner | Resolved (directive) |
| GAP-2261 | Depends on (build) is empty while the DP table adds platform H dependencies | TechX | Resolved (directive) |
| GAP-2278 | Two Work Packages write the same two story files and the same two fragments for legacy RWB-AD-016 on rwb-access | Delivery lead | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-2296 | The daily chain check has no job row in the Batch and Scheduling Design and the workflow kit dependency is absent from the Work Package | Solution architect with the platform workflow owner | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-2312 | DP-added platform and published contracts are not in the metadata dependency rows | Solution architect, P4 | Resolved (directive) |
| GAP-2317 | The four platform contracts and the reference-data contract that the DP table adds are absent from the Work Package dependency lists | Solution architect | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-2368 | The two contracts and the contact-stop events the view depends on carry no C row and no source shape in this key's plan | Solution architect | Resolved (directive) |
| GAP-2389 | The plan records no build row for the platform contracts that the patterns of this slice add | Delivery lead | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-2398 | The DP table adds eight H rows and three C rows that the Work Package dependency rows do not carry | Tech lead | Resolved (directive) |
| GAP-2404 | The metadata rows name no build dependency and the agent contract only, while the DP table of the story adds five platform contracts and two rwb-case contracts and the story consumes a further authorise operation | Delivery lead | Resolved (directive) |
| GAP-2410 | A secondary registry slice carries no build dependency while the DP rows add seven platform contracts and four published contracts | Delivery lead | Resolved (directive) |
| GAP-2412 | Placement record slice: element names of the decision-record fact, the case read and the authorise call, the reference-data operation, the MSG-P7-009 text, the per-service login name and the platform contract rows are not in any source this story may read | Solution architect, rwb-decision, with the rwb-integration and rwb-case contract owners | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-2414 | The metadata rows name no build dependency and the P3 contract only, while the DP table adds eight platform contracts and four published contracts, and the registry operations this story amends sit in another lane of the same service | Delivery lead | Resolved (directive) |
| GAP-2419 | The platform build dependencies, the authorise answer and the agent contract that the patterns add are not in the metadata rows, and RWB-P10-TE013-CON is not written | Solution architect | Resolved (directive) |
| GAP-2429 | The eight patterns add five platform build dependencies, one reference-data contract and one authorise contract that the metadata rows of a secondary slice do not carry | Solution architect, with the delivery lead | Resolved (directive) |
| GAP-2441 | How the business date, the queue identifier and the owner identifier travel in the decision record is not in the sources | P7 and P3 contract owners | Resolved (directive) |
| GAP-2448 | The metadata dependency rows name only the P5 contract, while the DP table adds platform and rwb-case and rwb-access contracts | Solution architect, P7 | Resolved (directive) |
| GAP-2455 | No source states which service appends the D7.1 generation record to the central ledger | TechX | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-2462 | The inner shape of the actions and outcome columns of a hand-over decision entry is not in any source | Solution architect with the data steward | Resolved (directive) |
| GAP-2468 | The story line carries one C row and no H row while the pattern table adds six platform H rows and the guard | Coordinator of the realignment with the P7 solution architect | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-2470 | RWB-P7-E2002-APP: the DP table adds six platform H rows, two C rows and one PLT object set that the metadata rows of the plan do not carry | Solution architect with the platform library owner and the rwb-decision service owner | Resolved (directive) |
| GAP-2475 | RWB-P7-E2004-APP: the DP table adds eight platform H rows, three C rows and a workflow-kit dependency that the metadata rows of a secondary slice do not carry | Solution architect with the platform library owner and the rwb-decision service owner | Resolved (directive) |
| GAP-2484 | The platform contracts the DP table adds are not in the metadata build row, and one provided operation has no story | P7 solution architect and the story-catalogue owner | Resolved (directive) |
| GAP-2488 | The eleven patterns add seven platform build dependencies and four consumed contracts that the metadata rows of a secondary slice do not carry | Solution architect, with the delivery lead | Resolved (directive) |
| GAP-2496 | The twelve patterns add eight platform build dependencies and four consumed contracts that the metadata rows of a secondary slice do not carry | Solution architect, with the delivery lead | Resolved (directive) |
| GAP-2501 | The DP table adds platform and published contracts that the metadata rows do not carry | Delivery lead, with the platform contract owners | Resolved (directive) |
| GAP-2540 | The plan gives this story no H row, while its migration needs the schema, the login and the Flyway pipeline of the service | Solution architect | Resolved (directive) |
| GAP-2548 | No contract story is allocated to this legacy key, and the outbound manifest, the event payload, the data product code and the ALS interface values are unpublished | P8 solution architect, the P2 integration owner and the event catalogue owner | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-2624 | FEAT-VAL-05 and FEAT-VAL-06 are prerequisites of the feature but their stories are not in the build dependency row | S1 rwb-valuation service owner with the delivery lead of wave 3 | Resolved (directive) |
| GAP-2669 | REQ-S2-009 says a broken plan raises an event, and the ownership rows and the plan give this legacy key no event to raise | Solution architect with the owner of the Kafka event platform and the business analyst of module S2 | Resolved (directive) |
| GAP-2716 | The GUARANTEE rule package and the two claim lists are consumed with no dependency row in this slice | P7 rwb-decision owner with the P3 rwb-case owner | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-2742 | The notice step of RWB-E5-001 has no declared owner for the notice and template rows, no operation name for the two consumed calls, no case-move operation, no requirement id, and one conflict between "no person in the path" and the built D7.1 approval | Solution architect, S4 rwb-litigation, with the P6 rwb-comms, P3 rwb-case and P7 rwb-decision architects and the reference-data owner | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-2751 | The four consumed reads and the two handed-over operations of the pack carry no dependency row, and two of the operations have no published name | Solution architect, S4 rwb-litigation, with the P5 rwb-document, P3 rwb-case and P4 rwb-access architects and the platform team | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-2760 | Three consumed contracts of the pack-recovery step have no dependency row, and the plan gives the two stories no contract or integration dependency | Solution architect, S4 rwb-litigation, with the P5 rwb-document and P3 rwb-case architects | Resolved (directive) |
| GAP-2773 | The panel read, the decline read and the case-move answer are consumed by both stories, have no contract story in the plan and no C row | Solution architect | Resolved (directive) |
| GAP-2790 | The rule package read and the reference values carry no dependency row, and DP-04, DP-06 and DP-07 are outside the pattern set | Solution architect, S4 rwb-litigation, with the P7 rwb-decision and P3 rwb-case architects | Resolved (directive) |
| GAP-2797 | The rule package that decides the three rules is a consumed contract of another service with no dependency row and no pattern in the set | P7 rwb-decision architect with the solution architect of S4 | Resolved (directive) |
| GAP-2801 | Four consumed surfaces of the appeal have no dependency row, and the plan carries no contract, integration or external dependency for either slice | Solution architect, S4 rwb-litigation, with the P7 rwb-decision, P3 rwb-case, S9 rwb-partner architects and the platform team | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-2829 | Three consumed owner contracts of the deferral step have no dependency row, and the plan gives both stories no contract or integration dependency | Solution architect with the P3 and P7 owners | Resolved (directive) |
| GAP-2837 | RWB-S5-E3019-APP: the take-on slice has no plan row for its cross-service reads, its outbox library, its requirement id or the duplicated R-DIS-06 criterion | Solution architect | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-2847 | RWB-S5-E3021: the take-on step consumes and publishes an event and reads four owner contracts, while the plan carries no C or I row and its pattern set omits DP-09 | Solution architect | Resolved (directive) |
| GAP-2860 | RWB-S5-E3024-APP: the stock balance has no figure definition, no write operation for its confirmation, no object in the TSD, no requirement id, and its two take-on rules are owned by sibling stories | Business analyst S5 with the solution architect and the rwb-access owner | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-2869 | RWB-S5-E3026: the cycle slice has no planned dependency row for its four consumed contracts or its Schedule library, and neither the plan nor the module model holds the re-appraisal record, the requirement id or the AC3 evidence | Solution architect | Resolved (directive) |
| GAP-2953 | The slice consumes an event and evaluates a rule package, while DP-09 and DP-04 are outside its pattern set and no platform build row is carried | S5 rwb-asset service owner with the platform event and workflow owners | Resolved (directive) |
| GAP-2973 | RWB-S6-E5023-APP: the eligibility slice has no plan row for its four consumed contracts, its outbox library, its rule kit, the 54 percent cap criterion or the two eligibility inputs | Solution architect | Resolved (directive) |
| GAP-2975 | RWB-S6-E5024-APP: the lot build and price slice has no plan row for its four consumed contracts, its agent contract, the R-DS-04 criterion split, the rules that carry no value or the outbox library | Solution architect | Resolved (directive) |
| GAP-2977 | RWB-S6-E5026-APP: the data-room slice has no plan row for its three consumed contracts, its partner channel or the lot status of the opening | Solution architect | Resolved (directive) |
| GAP-2984 | RWB-S6-E6002-APP: the qualification step has no operation, no bid table, no published names for the buyer read, the case move and the package, and no partner arrow in the connection matrix | Solution architect | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-2986 | RWB-S6-E6003-APP: the bar slice has no plan row for its six consumed contracts, no published bar operation, no panel or lot-status vocabulary, no next-bidder field and no window row | Solution architect with the owners of rwb-partner, rwb-case, rwb-access and rwb-decision | Resolved (directive) |
| GAP-2988 | RWB-S6-E6004-APP: the take-bids slice has no plan row for its five consumed contracts, its guard and outbox libraries, the publish-first story of API-S6-005, the bid and realised-recovery columns, the two rules it shares with sibling keys, the reporting destination of R-DS-34, its wave or its requirement id | Solution architect | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-2990 | RWB-S6-E6005: the award step carries an empty C row although it consumes rwb-case, rwb-decision, rwb-access and rwb-source-data, and three consumed operations have no published name | Solution architect | Resolved (directive) |
| GAP-2996 | RWB-S6-E6006: the agreement-and-notices step carries an empty C row although it consumes rwb-document, rwb-comms, rwb-source-data, rwb-case and rwb-decision, and five consumed operations have no published name | Solution architect | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-3004 | RWB-S6-E6007-APP: the transfer slice has no plan row for its five consumed contracts or the buyer-file delivery, no outbox row although it publishes AccountsTransferred, no transfer operation and no column set to record the transfer | Solution architect | Resolved (directive) |
| GAP-3006 | RWB-S6-E6008-APP: the derecognition and posting slice has no plan row for its four consumed contracts and its interface call, no posting column, no published operation names and no requirement id | Solution architect | Resolved (directive) |
| GAP-3008 | RWB-S6-E6009-APP: the put-back review has no published operation, its claim window, claim reason and realized-recovery figure have no field, column or event, its consumed contracts have no plan row, and two of its four criteria execute rules owned by sibling stories | Solution architect | Resolved (directive) |
| GAP-3010 | RWB-S6-E6010-APP: the closure slice has no plan row for its four consumed contracts, no published closure operation, an open-action set no source enumerates, no right for an unattended step and an ALS and GL integration point it does not own | Solution architect | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-3012 | RWB-S6-E6011-APP: the settle-and-cancel slice has no plan row for its six consumed contracts, its inbox library, its rule kit, its settlement stamp, its GL prerequisite or its EP06 wave | Solution architect | Resolved (directive) |
| GAP-3014 | RWB-S6-E5025: the masking rule set, the tape layout, the tape's storage reference, the PII service mapping and the six consumed contracts are given by no source and sit outside the plan's empty C row | Solution architect | Resolved (directive) |
| GAP-3016 | RWB-S7-E6013-APP: the scan slice has no plan row for its four consumed contracts, its rule kit, its ACE read, its inbox and its schedule, and no table or list of values holds the scan | Solution architect | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-3021 | RWB-S7-E6015-APP: the pack slice has no plan row for its seven consumed contracts, its agent, outbox and rule-kit dependencies, its pack columns, its requirement id or its screen read | Solution architect | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-3023 | RWB-S7-E6016-APP: the removal slice has no published operation, no field or list for the removal reason, no plan row for its three consumed contracts, and no requirement id | Solution architect | Resolved (directive) |
| GAP-3025 | RWB-S7-E6017-APP: the routing slice has no plan row for its five consumed contracts, its rule kit, its event library, its meeting calendar, the operation it provides or the requirement it serves | Solution architect | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-3027 | RWB-S7-E6018-APP: the delegation table and its owner, the approver and the limit applied have no column, the credit committee outcome is claimed by no story, and the plan's C row is empty while five rows are consumed | Solution architect | Resolved (directive) |
| GAP-3033 | RWB-S7-E6021-APP: the plan holds no C or X row for the four consumed contracts of the pack-prepared step, no dependency row for DP-05, no interface for the ALS and general-ledger crossing, and no separate story for the shared pack rule R-WO-05 | Solution architect with the rwb-writeoff tech lead, the rwb-source-data, rwb-case and rwb-decision owners and the wave 4 integration lead | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-3035 | RWB-S7-E6022-APP: the Finance feed slice provides no operation while four consumed surfaces and one external feed have no plan row, no column carries the feed result, and the feed transport, layouts and codes are unpublished | Solution architect | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-3037 | RWB-S7-E6023-APP: the reconciliation step has no published operation, no posting-product operation or event name, no matching cross-reference, no plan C row for its three consumed services, no job or Schedule for its monthly trigger and no requirement row | Solution architect | Resolved (directive) |
| GAP-3039 | RWB-S7-E6024-APP: no source publishes the correction operation or its elements, the loop's owner and time limit that REQ-S7-004 requires are unconfirmed, the retry count has no column, the other two entries to WRITEOFF_EXCEPTION have no feature, and SCR-27 has no exception state | Solution architect | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-3041 | RWB-S7-E6025-APP: the closure slice has no plan row for its five consumed contracts, its rule kit, its event library, its scheduler marker, the retention period, the placement record or the closing amounts | Solution architect | Resolved (directive) |
| GAP-3046 | RWB-S7-E6027-APP: the post charge-off recovery has no REST operation, no published event name, no fee column and no screen state, and the plan's C row is empty while two rows and one event are consumed | Solution architect | Resolved (directive) |
| GAP-3051 | RWB-S8-E7001-APP: the X1 slice has no plan row for its two cross-service reads, no event names, no complaint service level and no published case-clock boundary, and its happy path has no acceptance criterion | Solution architect | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-3053 | RWB-S8-E7002-APP: the X2 slice has no plan row for its four consumed contracts, its outbox library, its EFS touch, its requirement ids, its work-management owners or its screen read | Solution architect | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-3055 | RWB-S8-E7003-APP: the X3 branch has no plan row for its four consumed contracts, its rule read, its outbox and its workflow, and no source names the claim reference, the heir notification or the escalation level | Solution architect | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-3057 | RWB-S8-E7004-APP: the X4 slice has no plan row for its five consumed contracts, its rule kit, its ACE read, its outbox and inbox, its Aric route or its state vocabulary, and its legacy success criterion is owned by the harness | Solution architect | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-3059 | Seven values of the X5 deviation have no source: the claim deadline, the Legal handler route, the case contract and its two event families, the platform outbox, the legal counsel's right, the requirement identifier and the sign-off | Solution architect | Resolved (directive) |
| GAP-3061 | RWB-S8-E7006-APP: the X6 slice has no plan row for its consumed contracts, its skip-trace sources, its events, its agent dispatch, its 30-day clock or the deviation service level | Solution architect | Resolved (directive) |
| GAP-3070 | RWB-S8-E7010-APP: the contact-breach path has no rule row, no column, no published ledger read, no operation of its own, no event and no write right for its primary role | Center of excellence with the solution architect, the rwb-decision rule owner, the rwb-source-data owner and the rwb-access owner | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-3075 | The plan gives this slice no build dependency while the DP table adds eight platform contract rows and two further contract rows | Platform owner for the TPL, LIB, WF, DB, EVT and EDGE epics with the S8 service owner | Resolved (directive) |
| GAP-3082 | RWB-S8-E1023-APP: a P3 Case and workflow module story is placed in rwb-deviation with an empty build row, and the plan gives the slice no platform dependency although seven pattern rows add one | Solution architect | Resolved (directive) |
| GAP-3087 | RWB-S8-E2009-APP: a P9 Reporting story is placed in rwb-deviation with one C row and an empty build row, and the seven owner reads, the matrix edge and the platform prerequisites are unpublished | Solution architect | Resolved (directive) |
| GAP-3091 | Plan build list is empty for RWB-S8-E2012-APP although the DP table adds eight platform contract rows | Platform architect | Resolved (directive) |
| GAP-3129 | RWB-S9-E7015-APP: the contract end has no operation, the recall has no event, "open" has no definition, the partner service level sits on no PRM rule row and the case-side re-selection has no published boundary | Solution architect with the rwb-case owner, the rwb-decision rule owner and the center of excellence | Resolved (directive) |
| GAP-3140 | The DP table names platform H rows that the plan's H list does not carry | Tech lead | Resolved (directive) |
| GAP-3232 | The story catalog carries 2,534 dependency rows while the story files carry 2,609 for the same 1,034 stories | Solution architect | Accepted (directive); change listed in the Cross-document Change Register v1 |

## 7. Unconfirmed assumptions (tied to a business decision)

None.

## 8. Lint findings on the staged stories

None.

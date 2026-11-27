# RWB-PLT-EDGE Edge and gateway - review pack, part 1 of 2 (RWB-PLT-N001-APP to RWB-PLT-N001-APP)

Decision: D-RCV-60. Date: 26 November 2026. Status: Draft (directive resolutions). Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

Directive run result for this service: every gap and assumption was resolved with the recommended resolution, except business decisions. Review this pack, then the staged story files it lists. Row IDs (ruling R-, item GAP-/ASM-/CG-, CDC-) match the master registers in 23 Document Gaps.

## 1. Summary

| Measure | Count |
|---|---|
| Stories | 1 |
| Resolved in the stories | 12 |
| Cross-document (pending in another document) | 186 |
| Not applied (value not in the sources) | 1 |
| Open business decisions | 8 |
| Register gaps linked | 185 |
| Unconfirmed assumptions | 0 |
| Lint findings | 0 |

## 2. Stories (staged next version)

| Story | Resolved | Cross-document | Not applied | File |
|---|---|---|---|---|
| RWB-PLT-N001-APP | 12 | 186 | 1 | 04 User stories/Recovery Workbench Service Story Files v2/RWB-PLT-EDGE Edge and gateway/RWB PLT N001 APP gateway-bff routes and composite screens v2.md |

## 3. Open business decisions (not resolved; owner decides)

| Story | Ruling | Item | Kind | Owner role | Title | Proposed resolution |
|---|---|---|---|---|---|---|
| RWB-ITG-E1011-ITG, RWB-PLT-N001-APP, RWB-PLT-N001-CON, RWB-PLT-E1027-CON, RWB-PLT-E1042-CON, RWB-PLT-E1043-CON, RWB-PLT-E1047-CON, RWB-PLT-E1044-CON, RWB-PLT-E1071-CON, RWB-P1-E1011-APP, RWB-P1-E1011-CON, RWB-P1-E1011-OPS, RWB-P3-E1011-APP, RWB-P3-E1042-CON, RWB-P3-E1043-CON, RWB-P6-E1011-APP, RWB-S5-E1011-APP | R-21929 | GAP-2972 | Register gap | TechX and the data steward and data product owner | RWB-S5-E1011-APP: the asset slice of RWB-E1-011 has no source for its dependency lists, its ACE-side read, its quality objects, its rights, its run cadence and the owning row of the asset table, and the data-lake and Power BI target of the legacy key is removed | Confirm at the wave-1 design gate: the platform release train as the source of the seven platform CONs; the rwb-source-data contract as the only ACE-side read, with the FSD S5 view names read as the product behind it; the three quality tables, check names and read operations as the service design; the two quality reads in Platform administration right R; the asset table as an S5 object read in rwb_asset; and a daily Schedule with a cron and alert groups set as configuration. |
| RWB-ITG-E1017-ITG, RWB-PLT-N001-APP, RWB-PLT-N001-CON, RWB-PLT-E1027-CON, RWB-PLT-E1043-CON, RWB-PLT-E1044-CON, RWB-PLT-TE012-APP, RWB-PLT-E1071-CON, RWB-P1-E1017-APP, RWB-P1-E1017-CON, RWB-P1-E1017-OPS, RWB-P5-AD021-CON, RWB-P5-E1017-APP, RWB-P7-E1017-APP | R-21974 | GAP-1029 | Register gap | Solution architect, with the Compliance and PDPA officer and the platform storage owner | The P5 retention slice has no source value for its retention periods, its document age basis, its retention-load and run-read paths, its archive container name and its login, and the three contracts it consumes at run time are not in its contract-dependency list | Build the P5 slice on the recorded defaults: RET-2026.11 at 24 months for DP10 documents on created_at with end action ARCHIVE until Compliance supplies the bank schedule (DL26); the shared retention contract shape of RWB-P5-AD021-CON for the retention-class and document-retention reads, with the four admin operations on /api/recovery/document/v1; the write-once container rwb-docs-archive of RWB-PLT-TE012-APP with a manifest of row count and SHA-256 per file; the phrase 'the rwb-document login (DP-02)'; and the P3 case, P3 reference-data and P7 decision-record contracts named in 12.2 and 12.8 with their fakes. When Compliance supplies the schedule, load it as a new rule version with no code change; when the platform and contract owners publish, add the five H rows and the three consumed contracts to the plan, re-run the dependency check and swap each fake for the real contract in the same iteration. |
| RWB-ITG-E2014-ITG, RWB-PLT-N001-APP, RWB-PLT-N001-CON, RWB-P3-E2014-APP, RWB-P4-E2014-APP, RWB-P6-E2014-APP, RWB-P7-E2014-APP, RWB-P7-E2014-CON, RWB-P7-E2014-OPS | R-22495 | GAP-1269 | Register gap | Compliance and PDPA officer | No source enumerates the mask flags of the screen fields | Declare a mask flag of NONE, PARTIAL or FULL with a policy key on every field of the two panels, PARTIAL for the postal address, and confirm the policy keys with the masking owner (P4). |
| RWB-PLT-N001-APP, RWB-PLT-N001-CON, RWB-PLT-E1027-CON, RWB-PLT-E1072-CON, RWB-PLT-TE006-CON, RWB-PLT-E1071-CON, RWB-S7-E6020-APP, RWB-S7-E6020-CON | R-23236 | GAP-3031 | Register gap | Solution architect; business lead | RWB-S7-E6020-APP: the review date has no property, field ID, column or list, the legacy timer table is not S7's, R-WO-17's owner conflicts with the FSD role and the permission table, the plan's C row is empty while the step consumes four contracts, DP-04, DP-09 and DP-10 are absent, and no source publishes a rule, a message or a state for a date in the past or a second decision at DEFERRED | Keep the plan's H, C, I and X rows as they stand; carry the review date as an additive request property recorded in the decision record and the case move, with no column and no field ID until the business lead and rwb-case confirm them; set the review timer as a durable workflow timer and let rwb-case own the timer row; map R-WO-17's owner to the roles that hold right A for the act and to the write-off team for the return; declare the four consumed rows in sections 12.2 and 12.8 and record the absent DP-04, DP-09 and DP-10 rows; leave a second decision at DEFERRED and a past review date unpublished and tracked |
| RWB-PLT-N001-APP, RWB-PLT-N001-CON, RWB-PLT-E1027-CON, RWB-PLT-E1072-CON, RWB-PLT-TE006-CON, RWB-S7-E6019-APP, RWB-S7-E6019-CON | R-23240 | GAP-3029 | Register gap | Solution architect; business lead | RWB-S7-E6019-APP: the reject reason and the decision code have no field, column or list, R-WO-16's owner conflicts with the FSD role and the permission table, the plan's C row is empty while the step consumes three contracts, DP-04 and DP-09 are absent, and no published row moves a case out of RETURNED_TO_PURSUE | Keep the plan's H, C, I and X rows as they stand; record the reason and the decision code as request and record inputs with a placeholder until the business lead confirms them; map R-WO-16's owner to the four roles that hold right A in TSD S7 T6.1; declare the three consumed rows in sections 12.2 and 12.8 and record the absent DP-04 and DP-09 rows; leave the onward path of RETURNED_TO_PURSUE to the case owner and raise it in the next planning cut; keep committee_date and every other write_off column out of the reject slice |
| RWB-PLT-N001-APP, RWB-PLT-N001-CON, RWB-PLT-E1027-CON, RWB-PLT-E1072-CON, RWB-PLT-TE006-CON, RWB-S9-E6034-APP, RWB-S9-E6034-CON | R-23241 | GAP-3117 | Register gap | Solution architect; business lead; access owner in rwb-access | RWB-S9-E6034-APP: the legacy story names two read endpoints and no operation that places the account, partner_instruction carries no rule-version or decision column, S9 owns no route set so the placement rule is only expressible as the D9 rows R-WO-29 to R-WO-32, the legacy permission table gives the Partner portal right R while the issue needs C and the FSD also-uses role has no matrix row, both screens are list states with no placement form, the plan C row is empty while the case and the rule package are consumed, DP-04 and DP-09 are absent, the EV-20 consumer set and payload are not published, and no requirement row traces to FEAT-PRM-06 | Keep the plan H, C, I and X rows as they stand; issue the placement through API-S9-002 and never through a new path; record the rule version and the picked agency on the local decision record and add no column to partner_instruction; read the placement rows from rwb-decision as data and record the absent DP-04 rows; read the case on the rwb-case contract and record the absent C rows; authorise the issue on the Partner portal right C the matrix gives and record the legacy right R and the missing also-uses row as conflicts; serve the placement from the list state of SCR-35 through the composite route and carry the form as a placeholder; publish EV-20 with IDs only and record the absent DP-09 row; let the trace rest on the legacy key and the feature row until the E6 BRD and the PRD publish a requirement |
| RWB-PLT-N001-APP, RWB-PLT-N001-CON, RWB-PLT-E1027-CON, RWB-PLT-E1072-CON, RWB-S6-E6005-APP, RWB-S6-E6012-APP | R-23244 | GAP-3015 | Register gap | Solution architect with the owners of rwb-case (P3), rwb-decision (P7), rwb-access (P4) and rwb-source-data (P1), and the business owner of the debt sale cap | RWB-S6-E6012-APP: the cap slice has no plan row for the five consumed contracts, no cap parameter row, no cap route rule, no published trigger, no headroom column and no service contract baseline | Publish the five consumed operations with their fake; add C rows for rwb-case, rwb-decision, rwb-access and rwb-source-data; add the DP-04, DP-06, DP-07, DP-08 and DP-09 rows the tables need; name the cap row, its version, its basis and its owner; publish one route rule for the cap or confirm that R-DS-19 and R-DS-23 are its only test and which story owns them; publish the trigger or confirm the call from the lot build and award steps; add the cap-position and headroom fields or confirm the decision record as their only home; create the service contract baseline for this legacy key; and carry REQ-S6-001 and BR-050 in the plan |
| RWB-PLT-N001-APP, RWB-PLT-N001-CON, RWB-PLT-E1027-CON, RWB-S8-E7009-APP, RWB-S8-E7009-CON | R-23272 | GAP-3068 | Register gap | Solution architect; business lead; access owner in rwb-access | RWB-S8-E7009-APP: neither deviation nor any other owned table carries a complaint or contact reference, no published rule row expresses the match, no requirement row traces to FEAT-DVF-09, the Conduct and QA officer holds R only while the feature needs U, the plan's C row is empty while two contracts are consumed, DP-04, DP-05, DP-09 and DP-18 are absent, and no event carries the match to rwb-reporting | Keep the plan's H, C, I and X rows as they stand; carry the complaint and contact references and the match outcome as request inputs recorded on the local decision record until the business lead confirms their names, formats and value set; declare the two consumed rows in sections 12.2 and 12.8 and record the absent DP-04, DP-05, DP-09 and DP-18 rows; read the contact through rwb-source-data as the connection matrix gives it and never through EFS; authorise the match on the case-record right U the permission table gives and record the matrix row as the conflict; let the trace rest on the legacy key and the feature row until the E7 BRD and the PRD publish a requirement; leave the conduct measure on the decision-record ledger until an event exists |

## 4. Not applied (the value is not in the source documents)

| Story | Ruling | Item | Section | Title | Reason |
|---|---|---|---|---|---|
| RWB-PLT-N001-APP | R-18737 | DOR-RWB-PLT-N001-APP-4 | 8 | Definition of Ready item 4 Business rules: Partial | Sections 7 and 16 are not in this chunk, so no AC or TC row can be anchored. Supply those parts to map BR1 to BR10. |

## 5. Cross-document changes (pending in the target document)


### RWB-PLT-N001-CON (21)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-14722 | RWB-PLT-N001-APP | DOR-RWB-PLT-N001-APP-21 | Header | Complete the build so its build status is Done |
| CDC-14723 | RWB-PLT-N001-APP | DOR-RWB-PLT-N001-APP-22 |  | Publish a contract fake library version and record it |
| CDC-14724 | RWB-PLT-N001-APP | GAP-0693 |  | Publish the SCR-03 gateway-bff route with path, parallel call set, merge field map, 2 s budget split and partial-failure rule |
| CDC-14727 | RWB-PLT-N001-APP | GAP-0728 | find it | Publish the rwb-case console reads and the rwb-source-data reconciliation, key-resolution and freshness GET operations; fix the SCR-45 composite route in RWB-PLT-N001-CON. |
| CDC-14732 | RWB-PLT-N001-APP | GAP-0674 | find it | Publish the gateway-bff composite route for SCR-02 and SCR-03 with path, parallel calls, merge order, masking rules and the 2 s budget. |
| CDC-14741 | RWB-PLT-N001-APP | GAP-0629 |  | Drift step in the workflow of the v1 Schedule; segment read from run row; override figures via rwb-decision with agent-version filter and three additive elements; policy values in watch_measures; migration V10_007; range limits as configuration; login 'the rwb-agent login (DP-02)'; route registered under RWB-PLT-N001-CON. |
| CDC-14746 | RWB-PLT-N001-APP | GAP-0386 |  | Integration lead agrees the harness repository, SIT and UAT environments, seeded values, evidence format, retention and pass or fail gate; the platform edge story publishes the gateway-bff case-record route path and merge order in RWB-PLT-N001-CON. |
| CDC-14747 | RWB-PLT-N001-APP | GAP-0773 |  | Publish the SCR-03 composite route: path, the two parallel calls, live-wins merge rule with MSG-P2-008 fallback, masking rule and 2 s budget split. |
| CDC-14763 | RWB-PLT-N001-APP | GAP-0401 |  | Publish gateway-bff composite route for SCR-14 and SCR-30 document set; agree wave 2 harness pack, data seeding, evidence format and pass/fail gate with QA. |
| CDC-14766 | RWB-PLT-N001-APP | GAP-1903 |  | Fix the fill trigger, write key, element names and hearing uniqueness in the S4 design; the route field list and merge order go to RWB-PLT-N001-CON. |
| CDC-14788 | RWB-PLT-N001-APP | GAP-2188 |  | Fix member names and JSON spelling for ruleResult, inputs, confidence and record reference; settle types and refusal set with rwb-decision and rwb-case owners; name the route at baseline. |
| CDC-14793 | RWB-PLT-N001-APP | GAP-0094 |  | Publish the BFF composite route per screen (path, operation, merged response) as a second edge document, or state the BFF is a pure pass-through router with no composite route this release. |
| CDC-14794 | RWB-PLT-N001-APP | GAP-1393 | Not specified in the source documents (GAP-1393) | Publish the gateway-bff route document (OpenAPI and AsyncAPI) with one path per screen tab and one inbox stream path, stating the inbox push transport. Confirm the payment-tab operation with rwb-payment and the notice-tab operation with rwb-comms at the edge contract review. |
| CDC-14798 | RWB-PLT-N001-APP | GAP-0867 | Not specified in the source documents (GAP-0867) | Provide one read GET /api/recovery/access/v1/admin/home answering an AdminHome with area rows (capabilityArea, letters, scope, mayOpen) plus matrixVersion, maskingVersion, listVersion, roleClass, chain and recordedAt. Hold the cache lifetime in parameter row access.home.cache.ttl.seconds read through DP-06. |
| CDC-14852 | RWB-PLT-N001-APP | GAP-1436 |  | Confirm: dictionary served by rwb-case reference-data contract from sys_fields; rule set generated once and inherited by 19 repositories; build record carries dictionary and rule-set versions; allow-list approver is the code-owner role; release quality view is a gateway-bff composite route. |
| CDC-14862 | RWB-PLT-N001-APP | GAP-1035 | 13 | Section 13 CON row marks the SCR-30 route as Not specified in the source documents (GAP-1035) |
| CDC-14881 | RWB-PLT-N001-APP | GAP-0944 | header | Publish the composite route field lists for SCR-14 and SCR-30. Add the allowed-action decision code to the ledger decision-code list before the audit query is built. |
| CDC-14882 | RWB-PLT-N001-APP | GAP-0951 | header | State the field app's route: capture sync as a composed call beside the rwb-document call, and the SCR-30 panel as a parallel read. |
| CDC-14903 | RWB-PLT-N001-APP | GAP-1730 | find it | Record the owning service and the gateway-bff composite route for SCR-17 over this service and the case contract in the edge catalogue. |
| CDC-14904 | RWB-PLT-N001-APP | GAP-2832 | find it | Add a deferred reading to SCR-20 showing the reason, the review date and the rule version; field list and merge order to be set in the screen model. |
| CDC-14906 | RWB-PLT-N001-APP | GAP-2952 | find it | Show the LOV-HOLDING state with the case state beside it; read take-on as the ASSET_ON_BOOKS and ASSET_HELD pair; keep legacy wording as the business description. |

### 11 Delivery and operations/Recovery Workbench Dependency Map v5.xlsx (7)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-14764 | RWB-PLT-N001-APP | GAP-2354 |  | Record the six platform CONs as wave-0 prerequisites of wave-1 services and add RWB-P3-E1043-CON to the DP-07 story contract rows. |
| CDC-14773 | RWB-PLT-N001-APP | GAP-2869 |  | Add DP-10 and RWB-PLT-E1071-CON for the Schedule, add the C and I rows, and trace both slices to REQ-S5-003. |
| CDC-14818 | RWB-PLT-N001-APP | GAP-2797 |  | Consume the LITIGATION package from rwb-decision as a non-blocking contract with its fake at the version in force. The embedded runtime stays a service-template capability. Neither story declares a rule row, package or rule version. If a C row is later required, change only the Dependency Map and metadata rows. |
| CDC-14838 | RWB-PLT-N001-APP | GAP-1963 |  | Build on Day 1 against the published rwb-decision, rwb-access and rwb-case documents and their fakes; keep the metadata rows as the plan states them; ask the plan owner to add the five C rows and the rwb-decision queue dependency to the dependency map. |
| CDC-14870 | RWB-PLT-N001-APP | GAP-1335 |  | Carry RWB-PLT-E1027-CON, RWB-PLT-E1042-CON, C RWB-P3-E1042-CON, RWB-PLT-E1043-CON, C RWB-P3-E1043-CON, RWB-PLT-TE006-CON, RWB-PLT-E1071-CON and RWB-PLT-N001-CON in the dependency map. Keep the metadata rows as they are. |
| CDC-14872 | RWB-PLT-N001-APP | GAP-1337 |  | Carry the platform contracts (RWB-PLT-E1027-CON, RWB-PLT-E1072-CON, RWB-PLT-E1042-CON, RWB-PLT-E1043-CON, RWB-PLT-TE006-CON, RWB-PLT-E1071-CON, RWB-PLT-E1044-CON, RWB-PLT-N001-CON) and the rwb-case contracts (C RWB-P7-E1073-CON, C RWB-P3-E1042-CON, C RWB-P3-E1043-CON) in the dependency map. Keep the metadata rows. |
| CDC-14891 | RWB-PLT-N001-APP | GAP-1308 | Header | Add the eight platform H and three published C dependencies as DP-added in the dependency map; keep Ready to start = Day 1. |

### 05 Technical architecture/Recovery Workbench Service Contract Catalog v1.md (3)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-14729 | RWB-PLT-N001-APP | GAP-0673 | find it | Mark the FSD A1.5 and TSD T1/T5.1 INT-03 lines superseded for legacy key RWB-E4-046; load one versioned ALS interface_config row per environment. |
| CDC-14866 | RWB-PLT-N001-APP | GAP-2455 |  | Confirm that rwb-decision appends every DecisionRecorded fact to decision_log_entry, that the producer's local record is the working record and the ledger entry is the record of record, and that RWB-PLT-E1027-CON, RWB-PLT-TE006-CON, RWB-PLT-E1044-CON and RWB-PLT-N001-CON are wave-0/wave-1 baseline outside the H row. |
| CDC-14871 | RWB-PLT-N001-APP | GAP-0909 |  | Publish the SCR-03 composite route with its field list, hop list, merge order and field-level masking rule (DP-19); fix the rwb-access per-service login in the platform DB story. |

### RWB-P7-E2014-CON (3)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-14758 | RWB-PLT-N001-APP | GAP-1258 |  | Publish field list and mask flags of the two approval panels (SCR-11, SCR-18) as working read; confirm with route owner and three consumer sign-offs; correct by new contract version. |
| CDC-14759 | RWB-PLT-N001-APP | GAP-1259 |  | Carry GET /api/recovery/approvals/{approvalId} as working read and register it with the route owner at first version freeze. |
| CDC-14761 | RWB-PLT-N001-APP | GAP-1270 |  | Register approval route with 2 s budget per downstream and 1.2 s composition budget as the case screen; record measured p95 on dashboard. |

### 09 Testing and quality/Recovery Workbench Requirements Traceability Matrix v7.xlsx (2)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-14726 | RWB-PLT-N001-APP | DOR-RWB-PLT-N001-APP-12 | 16, 18 | Section 16 test case rows TC-PLT-N001-APP-01 to 10 added |
| CDC-14855 | RWB-PLT-N001-APP | CG-ALL-1277 | 18 | In the next RTM version, align REQ-OCC-007 test list to section 18 of RWB-PLT-N001-APP (TC-PLT-N001-APP-03, TC-PLT-N001-APP-07). |

### RWB-P10-TE013-CON (2)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-14789 | RWB-PLT-N001-APP | GAP-2419 |  | Treat seven platform contracts and RWB-P3-E1043-CON as wave 0 build dependencies and fakes; take authorise answer from platform guard; replace agent fake with RWB-P10-TE013-CON when it lands. |
| CDC-14792 | RWB-PLT-N001-APP | GAP-0072 |  | Build tool gateway inside rwb-agent as one outbound client holding workload identity, calling owner REST contracts with one hop and 2 s, writing each call to the run row. |

### RWB-P4-E8017-CON (2)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-14800 | RWB-PLT-N001-APP | GAP-0879 | Not specified in the source documents (GAP-0879) | Fix four operations on /api/recovery/access/v1/admin/incidents, the OPEN and CLOSED states, the five step names, the step record code and shape, and the report fields. Enter the incident reference and detection time as data; no feed from the observability platform. |
| CDC-14801 | RWB-PLT-N001-APP | GAP-2301 | Not specified in the source documents (GAP-2301) | Record the incident as two entries of the rwb-access decision-record chain per incident, not as a table. Fix three paths on the access base, the five step names, the OPEN and CLOSED states, held-area lists on LOV-CAPABILITY and letters on LOV-SCOPE. Read the right per the proposed fix. |

### RWB-P6-E4035-CON (2)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-14802 | RWB-PLT-N001-APP | GAP-2363 | Not specified in the source documents (GAP-2363) | Keep the two notice endpoints and their Litigation rights with RWB-P6-E1052-APP and RWB-P6-E2021-APP, and SCR-33 with the template stories. Serve the FEAT-COM-01 offer view to LINE OA and HOME.SCB via gateway-bff from two RWB-P6-E4035-CON operations. Fix channel screens in RWB-PLT-N001-CON. |
| CDC-14803 | RWB-PLT-N001-APP | GAP-2367 | Not specified in the source documents (GAP-2367) | Confirm the capability area and right of the two offer-view operations with the rwb-access owner at the RWB-P6-E4035-CON baseline review. Keep scope applied on the case. Add customer-channel screens and masking to RWB-PLT-N001-CON. |

### RWB-S6-E5026-APP (2)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-14833 | RWB-PLT-N001-APP | GAP-2977 |  | Keep plan H, C, I and X rows. Record rwb-document, rwb-partner and rwb-case as class C dependencies with fakes. Record the partner channel as an edge dependency. Write no lot status of the opening. |
| CDC-14834 | RWB-PLT-N001-APP | GAP-1958 |  | Declare rwb-document, rwb-partner and rwb-case as class C consumed rows of the story, build against their published documents and fakes on Day 1, keep the C row as the plan states it, and trace REQ-S6-003. |

### API:(service not named) (2)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-14853 | RWB-PLT-N001-APP | GAP-2602 |  | Declare the outlier element as an additive optional element of Approval under a draft name, with typed and nullable elements, and publish its shape in the S1 API file. |
| CDC-14895 | RWB-PLT-N001-APP | GAP-0141 |  | Rewrite every operation under /api/recovery/<short>/v1 behind gateway-bff, keeping the operation-to-service assignment of the Ownership Map v1. |

### Epic design record (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-14721 | RWB-PLT-N001-APP | DOR-RWB-PLT-N001-APP-14 |  | Record the signed epic design sign-off for RWB-PLT-EDGE |

### 02 Business architecture and process/Recovery Workbench Users Roles and Permissions v5.xlsx (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-14725 | RWB-PLT-N001-APP | DOR-RWB-PLT-N001-APP-1 | 1 | Add a role code and name for 'Recovery officer opening a case in the workbench'. Section 1 keeps its placeholder until that role exists. |

### OTHER:Legacy RWB-DM-013 and the rwb-payment contract with the Data Migration Approach (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-14728 | RWB-PLT-N001-APP | GAP-2533 | find it | Publish the handover file, a named load command with run record, the provenance column and the DP-15 split-plan record for the payment cutover. |

### RWB-S5-E1011-APP (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-14730 | RWB-PLT-N001-APP | GAP-1946 | find it | Record the nine platform and rwb-case CONs as wave-0 prerequisites with fakes; read quality from the quality-results and quality-runs GETs; declare the slice design. |

### RWB-P6-E1011-APP; 11 Delivery and operations/Recovery Workbench Dependency Map v5.xlsx (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-14731 | RWB-PLT-N001-APP | GAP-1167 | find it | Record the seven platform CONs as wave-0 platform prerequisites; keep H empty and the depth of lane L-P6-C unchanged. |

### RWB-S8-E1021-APP (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-14733 | RWB-PLT-N001-APP | GAP-3075 | find it | Platform owner confirms the eight platform contracts and two rwb-case rows before release; assembler corrects the plan metadata if reissued. |

### RWB-P7-E2032-APP (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-14734 | RWB-PLT-N001-APP | GAP-2404 |  | Set H to None plus RWB-PLT-E1027-CON, RWB-PLT-E1042-CON, RWB-PLT-E1043-CON, RWB-PLT-TE006-CON and RWB-PLT-N001-CON; set C to RWB-P10-E2032-CON plus RWB-P3-E1042-CON, RWB-P3-E1043-CON and the P4 authorise contract (ID not specified in the source documents (GAP-2404)); keep Day 1. |

### OTHER:Story record named in GAP-2448 (key not given in the item) and its section 13 (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-14735 | RWB-PLT-N001-APP | GAP-2448 |  | Keep Depends on (build) none and C RWB-P5-E1032-CON as fixed; record the DP-table platform, P3 and P4 authorise contracts in section 13, built against fakes on Day 1. |

### RWB-P6-E1032-APP; 11 Delivery and operations/Recovery Workbench Dependency Map v5.xlsx (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-14736 | RWB-PLT-N001-APP | GAP-1198 |  | Add H RWB-PLT-E1027-CON, H RWB-PLT-E1042-CON, C RWB-P3-E1042-CON, H RWB-PLT-E1043-CON, C RWB-P3-E1043-CON, H RWB-PLT-TE006-CON, H RWB-PLT-E1071-CON, H RWB-PLT-E1044-CON and H RWB-PLT-N001-CON, or record them in the platform release train. |

### RWB-P7-E2041-APP (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-14737 | RWB-PLT-N001-APP | GAP-2414 |  | Set H to None plus RWB-PLT-E1027-CON, RWB-PLT-E1072-CON, RWB-PLT-E1042-CON, RWB-PLT-E1043-CON, RWB-PLT-E1037-CON, RWB-PLT-E1047-CON, RWB-PLT-E1044-CON and RWB-PLT-N001-CON; set C to RWB-P3-E2041-CON plus RWB-P7-E1073-CON, RWB-P3-E1042-CON, RWB-P3-E1043-CON and RWB-P4-E1037-CON; treat RWB-P7-E2042-APP as the registry operation set; keep Day 1. |

### OTHER:The rwb-integration composed case-list story and the P3 and P4 contract stories named in GAP-0660 (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-14738 | RWB-PLT-N001-APP | GAP-0660 |  | Keep GET /cases and GET /cases/export with rwb-case and serve SCR-02 from the owner through gateway-bff; add the composed read and export on the integration base as a read-only composition, reading case, queue and ageing data through rwb-case contracts and access data through the rwb-access contract, one hop each with a 2 s budget. |

### OTHER:FSD P7 v3 and TSD P7 (P7 slice of RWB-E1-046, rwb_de table and columns) (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-14739 | RWB-PLT-N001-APP | GAP-2453 |  | Keep the template catalogue single with P6; make the P7 copy a template_use record row per accepted answer holding template code, language, version, catalogue version, merge codes, notice type, product group, approver reference, valid from and business date; publish the reads in RWB-P6-E1046-CON and fake them until then; treat the three platform H rows as wave-0 prerequisites; fix the table, columns and migration file. |

### RWB-P5-E1049-CON; 11 Delivery and operations/Recovery Workbench Dependency Map v5.xlsx; OTHER:RWB-P6-E1032) (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-14740 | RWB-PLT-N001-APP | GAP-1206 |  | Build H rows: RWB-PLT-E1042-CON, RWB-PLT-E1043-CON, RWB-PLT-TE006-CON, RWB-PLT-E1071-CON, RWB-PLT-E1044-CON, RWB-PLT-N001-CON. Contract C rows: RWB-P3-E1042-CON, RWB-P3-E1043-CON, and the third rwb-case contract (Not specified in the source documents (GAP-1206)). |

### RWB-P10-E1063-CON; OTHER:FSD P4 REQ-ACA-006 and NFR-042; OTHER:TSD P4 v3 T6.1 next version (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-14742 | RWB-PLT-N001-APP | GAP-2333 |  | Keep both rights; record Reporting letters for other roles in matrix load; replace lake-copy access rule with served-read access entry; correct REQ-ACA-006 and NFR-042; add five platform H and two rwb-case C rows in the owning plan rows. |

### RWB-P2-E1073-APP; RWB-P7-E1073-CON; 05 Technical architecture/Recovery Workbench Service Contract Catalog v1.md (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-14743 | RWB-PLT-N001-APP | GAP-0672 |  | Record eight DP H rows as wave-0 platform prerequisites; publish model fetch in RWB-P7-E1073-CON; ALLOCATION set as synthetic test fixture until the reference data names the package; fix local copy table and migration in rwb_integration DB story. |

### RWB-P7-E1073-APP (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-14744 | RWB-PLT-N001-APP | GAP-1328 |  | Complete the metadata rows from the DP table, or state in R5.5 that platform H and self-referential C rows are held by the platform and contract stories and are not repeated on the APP line. |

### OTHER:Story Build Order (lane and Day-1 allocation of the patterned story) (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-14745 | RWB-PLT-N001-APP | GAP-2261 | Header | Add the platform CON dependencies DP-03, DP-06, DP-07, DP-09, DP-10 and DP-19 to the lane and Day-1 allocation; keep the metadata row as delivered by the WP. |

### RWB-P7-E2002-APP (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-14748 | RWB-PLT-N001-APP | GAP-2470 |  | Complete the metadata rows from the DP table and state in R5.5 that platform H and self-referential C rows are held by the platform and contract stories, or keep the plan rows as they are. |

### OTHER:P1; OTHER:P3 and P4 contract stories and TSD P2 Integration v3 (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-14749 | RWB-PLT-N001-APP | GAP-0662 |  | Keep P2 on /api/recovery/integration/v1; read holding and freshness via rwb-source-data, parties via rwb-case, authorise and masking via rwb-access, PII event via ACE Common; fix contract field names in the contract stories. |

### RWB-PLT-N001-CON; 06 Data/Recovery Workbench Logical Data Model and Data Dictionary v9.xlsx (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-14750 | RWB-PLT-N001-APP | GAP-0390 |  | Integration lead agrees the harness, environments, seeded data, evidence format and gate; platform edge story publishes the gateway-bff composite route in RWB-PLT-N001-CON; data dictionary owner publishes the field IDs in the next LDM version. |

### RWB-P7-E2004-APP (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-14751 | RWB-PLT-N001-APP | GAP-2475 |  | State in R5.5 that platform H and self-referential C rows are held by the platform and contract stories and not repeated on secondary APP lines, or complete the metadata rows. |

### RWB-P7-E2006-APP; 11 Delivery and operations/Recovery Workbench Dependency Map v5.xlsx (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-14752 | RWB-PLT-N001-APP | GAP-1343 |  | Publish the six DP-added dependencies with RWB-P7-E2006-APP as consumer; confirm RWB-P4-E1037-CON as a contract dependency in the wave 2 contract review. |

### RWB-S8-E2009-APP (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-14753 | RWB-PLT-N001-APP | GAP-3087 |  | Keep the plan's service, lane, C row and empty H row; record the slice as secondary serving of the steering data set; publish the seven consumed operation names with owners before tagging the contract. |

### RWB-P3-E2012-CON; 11 Delivery and operations/Recovery Workbench Dependency Map v5.xlsx (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-14754 | RWB-PLT-N001-APP | GAP-2501 |  | Record as non-blocking: H RWB-PLT-E1027-CON, RWB-PLT-E1072-CON, RWB-PLT-E1043-CON, RWB-PLT-TE006-CON, RWB-PLT-E1071-CON, RWB-PLT-E1047-CON, RWB-PLT-E1044-CON, RWB-PLT-N001-CON; C RWB-P7-E1073-CON, RWB-P3-E1043-CON. |

### RWB-P7-E2013-CON; RWB-PLT-N001-CON (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-14755 | RWB-PLT-N001-APP | GAP-0732 |  | Fix approval event fields, task fields (approval and preparer refs), escalation representation, approval-to-case status mapping, composite route field list and rwb-case login name; record outcome in case DB story. |

### RWB-P6-E2013-APP (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-14756 | RWB-PLT-N001-APP | GAP-1223 |  | H: None plus DP platform contracts. C: RWB-P7-E2013-CON plus RWB-P3-E1042-CON, RWB-P3-E1043-CON, RWB-P4-E1037-CON. Story stays Day 1. |

### RWB-P7-E2014-APP (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-14757 | RWB-PLT-N001-APP | GAP-1265 |  | Add C rows RWB-P1-E1015-CON and RWB-P3-E1018-CON, or record both reads as route-level composites of RWB-PLT-N001-CON. |

### OTHER:SCR-11 and SCR-18 state tables of RWB-E2-014 (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-14760 | RWB-PLT-N001-APP | GAP-1267 |  | Keep READY, STALE_INPUT, DECIDED and GENERATED, APPROVED, HELD as panel states; treat loading, temporarily unavailable and session expired as route overlay states. |

### 22 Microservice Realignment/Recovery Workbench Microservice Ownership Map v1.xlsx; OTHER:Context pack S4; OTHER:TSD S4 v2 (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-14762 | RWB-PLT-N001-APP | GAP-2742 |  | Record notice and template rows as P6 ownership or correct S4 row; name P6 generate-and-send operation and rwb-case stage answer in their contract stories; add REQ-S4-001 to key trace. |

### RWB-PLT-N001-CON; RWB-P4-E1037-CON (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-14765 | RWB-PLT-N001-APP | GAP-0955 |  | Publish the SCR-03 and SCR-04 composite field list in RWB-PLT-N001-CON, and the authorise, me-permissions and masking-policies shapes in RWB-P4-E1037-CON. |

### RWB-S4-E2025-APP (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-14767 | RWB-PLT-N001-APP | GAP-1898 |  | Add the five H rows and two C rows to the plan when the platform stories and rwb-case contracts publish; build against fakes until then. |

### RWB-P8-E2027-APP; 11 Delivery and operations/Recovery Workbench Dependency Map v5.xlsx (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-14768 | RWB-PLT-N001-APP | GAP-1291 |  | Record the DP-added H and C contracts as non-blocking platform and published contracts built against their fakes. |

### RWB-P7-E2028-APP; 11 Delivery and operations/Recovery Workbench Dependency Map v5.xlsx (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-14769 | RWB-PLT-N001-APP | GAP-1295 |  | Read H as None plus the six platform contracts and C as RWB-P10-E2028-CON plus RWB-P3-E1043-CON and the published P3 and P4 contracts. |

### RWB-P10-E1063-CON; RWB-PLT-N001-CON (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-14770 | RWB-PLT-N001-APP | GAP-0630 |  | Fix the seven added member names and four-decimal rule, declare the agent-version filter additive, name the notice path, and register the route in RWB-PLT-N001-CON. |

### RWB-P4-E2031-APP; 11 Delivery and operations/Recovery Workbench Dependency Map v5.xlsx (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-14771 | RWB-PLT-N001-APP | GAP-2317 |  | At D1, add the four platform contracts to H and RWB-P3-E1043-CON to C; keep the Work Package metadata unchanged. |

### RWB-P2-E2036-CON; RWB-PLT-E1027-CON; 07 Screens and experience/Recovery Workbench Error and Message Standard v4.docx (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-14772 | RWB-PLT-N001-APP | GAP-2412 |  | Publish the placement fact element names, the P3 case-read and P4 authorise shapes, the reference-data operation, the MSG-P7-009 text and the login name. |

### OTHER:Work package plan (contract allocation for legacy key); OTHER:TSD P8 v2 appendix T-A; 05 Technical architecture/Recovery Workbench Kafka Topic and Event Catalog v1.xlsx (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-14774 | RWB-PLT-N001-APP | GAP-2548 |  | Allocate a service contract baseline for this key or extend RWB-P8-E4043-CON, publishing rwb.payment.TreatmentBooked.v1 in BACKWARD mode, the deliverFile manifest element set with booking branch, the error envelope and fakes. Publish ALS interface row values as reference data and the data product code in TSD P8 appendix T-A. |

### RWB-S6-E6008-APP (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-14775 | RWB-PLT-N001-APP | GAP-3006 |  | Keep the H, C, I and X rows; record the four reads and the interface call as class C in fact with placeholders. Carry the posting result, item reference and rejection code in the decision record and case state, adding no column. Run posting under service identity, let RW-CREDITAD work R-DS-32, hold month-end close as a durable timer of DebtSaleWorkflow, adopt REQ-S6-008. |

### RWB-S7-E6017-APP (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-14776 | RWB-PLT-N001-APP | GAP-3025 |  | Keep the H, C, I and X rows; record rwb-case, rwb-deviation and rwb-decision as class C in fact. Record RWB-PLT-E1072-CON, RWB-P7-E1073-CON, RWB-PLT-TE006-CON and a meeting-calendar element as tracked dependencies. State that the step provides no REST operation; add a requirement row for the routing step at next revision. |

### RWB-S7-E6021-APP (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-14777 | RWB-PLT-N001-APP | GAP-3033 |  | Record the four consumed rows as class C in the Dependency Map without changing the H row; treat DP-05 as consumed on rwb-source-data's contract; keep ALS and GL crossing, re-post and provision release with RWB-ITG-E6021-ITG; read R-WO-05 as the assertion of RWB-S7-E6015-APP; add REQ-S7-002 and REQ-S7-005 at D1. |

### RWB-S7-E6025-APP (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-14778 | RWB-PLT-N001-APP | GAP-3041 |  | Keep the H, C, I and X rows; record rwb-case and rwb-decision as class C in fact; record RWB-PLT-E1072-CON, RWB-P7-E1073-CON and RWB-PLT-TE006-CON as tracked dependencies; read the scheduler marker as the workflow's durable timer; publish retention period as versioned reference data with a placeholder until Compliance sets it under DL26. |

### RWB-S7-E6028-CON; 11 Delivery and operations/Recovery Workbench Dependency Map v5.xlsx (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-14779 | RWB-PLT-N001-APP | GAP-1312 |  | Carry H RWB-PLT-E1027-CON (DP-03) and H RWB-PLT-N001-CON (DP-19) plus the four consumed contracts (P4 delegation-limit answer, P4 authorise call, P3 case read, reference-data LOV values) in the Dependency Map as non-blocking wave 0 and published P3 and P4 contracts; leave metadata rows as given; cite this row in section 13. |

### RWB-S8-E7001-APP; OTHER:TSD S8 T5.3; 22 Microservice Realignment/Recovery Workbench Microservice Ownership Map v1.xlsx (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-14780 | RWB-PLT-N001-APP | GAP-3051 |  | Keep the H, C, I and X rows; record rwb-document and rwb-source-data reads as C in fact with placeholders and fakes; adopt DeviationRaised and DeviationCleared as EV-06 and EV-07 on rwb.deviation.events.v1 with RWB-PLT-TE006-CON as the outbox library; treat the X1 complaint service level as the DL22 value; declare the stage clock pause as a signal in the stage outcome. |

### RWB-S8-E7002-APP (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-14781 | RWB-PLT-N001-APP | GAP-3053 |  | Keep the H, C, I and X rows; record the four consumed rows as class C in fact; record RWB-PLT-TE006-CON as the wave 0 library and RWB-PLT-E1072-CON with RWB-P7-E1073-CON as the evaluation kit; confirm EFS touch ownership; adopt REQ-S8-002, REQ-DVH-005 and REQ-S8-004; confirm owners of queue, assignment, timer and the four unnamed roles; confirm EV-06 and EV-07 names. |

### RWB-S8-E7003-APP; RWB-S8-E7003-CON; OTHER:connection matrix; OTHER:DeviationWorkflow ownership (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-14782 | RWB-PLT-N001-APP | GAP-3055 |  | Keep the H, C, I and X rows; record rwb-source-data, rwb-case, rwb-access and rwb-decision as class C in fact; record the rule read, RWB-PLT-TE006-CON and RWB-PLT-E1071-CON as tracked dependencies; settle the S8-to-P7 edge with the connection matrix owner; keep escalation level in the rule row. |

### RWB-S8-E7004-APP; OTHER:TSD S8 deviation state list (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-14783 | RWB-PLT-N001-APP | GAP-3057 |  | Keep the H, C, I and X rows; record the two rwb-case rows, the boundary signal and the two rwb-decision rows as class C in fact; record RWB-PLT-E1072-CON with RWB-P7-E1073-CON as the rule kit, RWB-PLT-TE006-CON as outbox and inbox library and RWB-PLT-E1037-CON with RWB-P4-E1037-CON as the access guard; publish a list of values for the deviation state before the DB story. |

### OTHER:RWB-S8 X5 deviation story and split plan (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-14784 | RWB-PLT-N001-APP | GAP-3059 |  | Keep both metadata rows as planned; carry claim deadline, SLA and Legal route as versioned placeholder rows; build against case fake Day 1; declare Case record U on both operations; trace both slices to FEAT-DVF-05. |

### RWB-S8-E7006-APP (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-14785 | RWB-PLT-N001-APP | GAP-3061 |  | Keep the plan's H, C, I and X rows; declare the four consumed rows class C with placeholders and fakes; record absent DP-05, DP-09, DP-14 and DP-20 rows in the registers. |

### RWB-S9-E7015-APP (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-14786 | RWB-PLT-N001-APP | GAP-3129 |  | Publish a contract-end operation or confirm a workflow command; define open; publish case-side re-selection command; publish partner_user field list; command workflow and read effect via GET operations until then. |

### OTHER:rwb-access panel-change publish story (RWB-E8-012 and FSD P4 v3 A2.23) (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-14787 | RWB-PLT-N001-APP | GAP-2281 |  | Provide POST and GET /api/recovery/access/v1/admin/panel-changes; hand workbook to P3 reference-load with table code partner_panel; read rule version from P7 and accept APPROVED or IN_FORCE. |

### OTHER:Wave 1 journey harness plan (QA lead) (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-14790 | RWB-PLT-N001-APP | GAP-0385 |  | Agree harness pack, seeded data, fixed business date, evidence format and retention, and all-green gate at wave entry; publish gateway-bff composite route via RWB-PLT-N001-CON; name P10 agent-run start operation. |

### OTHER:Wave 2 journey harness plan (QA lead) (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-14791 | RWB-PLT-N001-APP | GAP-0428 |  | Agree wave 2 harness pack, seeded data, fixed business date, evidence format and retention, and all-green gate; publish gateway-bff composite route via RWB-PLT-N001-CON; name rwb-deviation read operation with RWB-S8-E2015-APP. |

### 22 Microservice Realignment/Recovery Workbench Microservice Ownership Map v1.xlsx (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-14795 | RWB-PLT-N001-APP | GAP-2099 | Not specified in the source documents (GAP-2099) | Add one row each for gateway-bff, the Redis session and the App Gateway route. Assign the edge to platform epic RWB-PLT-EDGE and composite-route contract story RWB-PLT-N001-CON (DP-19) before wave 0 closes. |

### OTHER:rwb-access access model (RWB-P4 pack contract) (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-14796 | RWB-PLT-N001-APP | GAP-2288 | Not specified in the source documents (GAP-2288) | Define the pack as a candidate matrix version with PERMISSION, SCOPE and MASKING rows. Add operations POST and GET /api/recovery/access/v1/admin/pack-checks. Fix check codes PC-ENT, PC-SCP, PC-MSK, verdicts ACCEPTED and RETURNED, the decided-version 409, and parameter rows access.pack.personalAreas and access.pack.rowLimit. |

### OTHER:rwb-access access model (RWB-P4 matrix and grant) (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-14797 | RWB-PLT-N001-APP | GAP-2304 | Not specified in the source documents (GAP-2304) | Keep the matrix as permission rows stamped with a matrix version, minted and superseded by one set. Take the right from TSD P4 v3 T6.1 and API-P4-007. Treat the five system roles of T6.1 as agent roles and carry an agent reference on the grant. |

### RWB-P4-E8013-CON (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-14799 | RWB-PLT-N001-APP | GAP-0873 | Not specified in the source documents (GAP-0873) | Freeze the two QA-sample paths and three schemas. Add the P7 contract dependency to the metadata at the next revision. Fix the draw rule and reason codes as rwb-case parameter rows. Confirm the P7 rule-model read returns valid_from, valid_to and the rule_row set. |

### OTHER:The two pack-recovery stories named in GAP-2760 (not in this chunk) (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-14804 | RWB-PLT-N001-APP | GAP-2760 | 12.2 | Add three non-blocking consumed rows in the Dependency Map: P5 rwb-document checklist read and case document page, P3 rwb-case case-move answer. Name the P5 publishing stories. Leave metadata rows unchanged. |

### OTHER:The P6 and P5 stories named in GAP-1156 (not in this chunk) (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-14805 | RWB-PLT-N001-APP | GAP-1156 |  | Make document and document_custody P5 rwb_document rows. rwb-comms declares no custody table, column or cross-schema key and uses the P5 custody operation with a 2 s budget. Add the C row and fake of the P5 custody contract in step D1. |

### OTHER:The two petition-related stories named in GAP-1885 (not in this chunk) (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-14806 | RWB-PLT-N001-APP | GAP-1885 | 12.2 | Add five non-blocking rows: C RWB-P7-E2013-CON in wave 2, rwb-case and rwb-partner contracts built against fakes, C RWB-P3-E1043-CON, and the DP-08 edge and guard rule for each operation. |

### OTHER:The two stories named in GAP-2751 (not in this chunk) (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-14807 | RWB-PLT-N001-APP | GAP-2751 | 12.2 | Add non-blocking rows for API-P5-002, API-P5-008 and API-P3-002 on fakes, C of RWB-P3-E1043-CON for reference data, and the DP-08 guard rule. Name the case-state announcement and task raise in the P3 contract. |

### OTHER:The two appeal slices named in GAP-2801 (not in this chunk) (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-14808 | RWB-PLT-N001-APP | GAP-2801 | 12.2 | Add four non-blocking rows: P7 D7.4 approval as C of its wave, P3 case and partner contracts built against fakes, C RWB-P3-E1043-CON, and DP-08 edge and guard rules. |

### RWB-P4-E8015-APP; 22 Microservice Realignment/Recovery Workbench Architecture v5 Text Extract v1.md (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-14809 | RWB-PLT-N001-APP | GAP-2296 |  | Add a JOB-nn row for the daily rwb-access chain check. Add RWB-PLT-E1071-CON to the H list of RWB-P4-E8015-APP in the dependency map and plan, or state that each service verifies its own chain daily. |

### RWB-S6-E5025-APP (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-14810 | RWB-PLT-N001-APP | GAP-3014 | 12.2 | Keep the H, C, I and X rows. Carry six consumed rows in 12.2 with operation placeholders and fakes in 12.8. Treat the masking rule set and tape spec as versioned reference data. Record the PII service as unmapped. |

### RWB-S6-E6007-APP (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-14811 | RWB-PLT-N001-APP | GAP-3004 |  | Keep the H, C, I and X rows. Add the six consumed rows and the outbox dependency for AccountsTransferred. Record the transfer on the lot status and decision record. Split R-DS-25 into one saga. |

### RWB-P4-AD008-APP (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-14812 | RWB-PLT-N001-APP | GAP-0807 |  | Add RWB-PLT-E1071-CON to the build list and DP-10 to the pattern row. Set the cron as deployment configuration under the DL38 placeholder. Create the Schedule in the operations story. |

### RWB-S7-E6015-APP (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-14813 | RWB-PLT-N001-APP | GAP-3021 |  | Keep the H, C, I and X rows. Add seven consumed rows as C in fact. Add C RWB-P10-TE013-CON, RWB-PLT-TE006-CON, RWB-PLT-E1072-CON and RWB-P7-E1073-CON. Adopt REQ-S7-002. |

### RWB-S7-E6013-APP (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-14814 | RWB-PLT-N001-APP | GAP-3016 |  | Keep the H, C, I and X rows as they stand. Record rwb-case, rwb-source-data and rwb-decision as class C rows with placeholders. Record RWB-PLT-E1072-CON with RWB-P7-E1073-CON as the rule kit, RWB-PLT-TE006-CON as the outbox and inbox library and RWB-PLT-E1071-CON as the Scheduled job kit. Declare the JOB-16 Schedule and the ACE data-ready trigger in the story without registering them. Add DP-04, DP-05, DP-09 and DP-10 rows as the source sets them. Publish the write-off state list of values before the DB story. |

### RWB-S6-E5023-APP (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-14815 | RWB-PLT-N001-APP | GAP-2973 |  | Keep the H, C, I and X rows as they stand. Record rwb-case, rwb-source-data and rwb-decision as class C rows with placeholders. Record RWB-PLT-TE006-CON as the wave 0 library for topic rwb.debtsale.events.v1 and RWB-PLT-E1072-CON with RWB-P7-E1073-CON as the rule kit. Read the cap value from the package, leave the cap test and FEAT-DBS-16 with RWB-S6-E6005-APP, declare deviation_open and fraud_flag as consumed inputs with placeholders, and adopt REQ-S6-001. |

### RWB-S6-E6011-APP; 11 Delivery and operations/Recovery Workbench Dependency Map v5.xlsx (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-14816 | RWB-PLT-N001-APP | GAP-3012 |  | Keep the H, C, I and X rows unchanged. Build against the six contract fakes and the event fake on Day 1. Record the six rows as C dependencies in fact. Track the inbox library RWB-PLT-TE006-CON, the rule kit, the settlement stamp and the FEAT-DBS-12 story in the Dependency Map and Build Sequence. Keep wave 4 and the release date. Reconcile FSD and TSD module sources at module extract. |

### RWB-S7-E6016-APP (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-14817 | RWB-PLT-N001-APP | GAP-3023 |  | Keep the plan H, C, I and X rows. Add the removal operation to the write-off base with a placeholder path and element names until the solution architect confirms them. Record rwb-case and rwb-decision as class C rows with placeholders. Record RWB-PLT-TE006-CON as the wave 0 library and RWB-PLT-E1072-CON with RWB-P7-E1073-CON as the rule kit. Declare removal_reason as free text validated as present and stored in the decision record. Leave the R-WO-06 deviation hold with RWB-S7-E6017-APP. |

### OTHER:RWB-S6-E5023 story (WP B-S6-01 line) and its split plan slice (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-14819 | RWB-PLT-N001-APP | GAP-1947 |  | Keep the metadata rows exactly as the plan states them. Declare the four consumed rows in 12.2 with the operation-name placeholder and the fakes of 12.8. Read the DEBTSALE package as data on the owner's read rather than claiming a kit. Trace REQ-S6-001 from the FSD. |

### RWB-S6-E5024-APP (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-14820 | RWB-PLT-N001-APP | GAP-2975 |  | Keep the H, C, I and X rows as they stand. Record rwb-case, rwb-source-data, rwb-agent and rwb-decision as class C rows with placeholders. Record RWB-P10-TE013-CON as the agent contract and RWB-PLT-TE006-CON as the wave 0 library. Read minimum lot size, tiered terms and reserve policy from the package as rule rows with placeholders. Keep R-DS-04 criterion with RWB-S6-E6001-APP. Adopt REQ-S6-002. |

### RWB-S7-E6023-APP (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-14821 | RWB-PLT-N001-APP | GAP-3037 |  | Fix the posting product and its event on the rwb-source-data contract and publish the matching cross-reference on the same contract. Hold the three consumed rows as class C dependencies. Record no provided operation and no Schedule. Trace the step to REQ-S7-005 with a placeholder until the E6 BRD and PRDs are written (C1). |

### OTHER:FSD S2 requirements table; 05 Technical architecture/Recovery Workbench Event and Messaging Design v5.xlsx (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-14822 | RWB-PLT-N001-APP | GAP-2669 |  | Either confirm the stage report to rwb-case as the event REQ-S2-009 means and reword the requirement, or allocate rwb.treatment.PlanBroken.v1 with its payload and consumers, add DP-09 with H RWB-PLT-TE006-CON to both stories and an outbox row, and fold it into the wave 2 event catalogue. |

### RWB-S5-E3019-APP; 22 Microservice Realignment/Recovery Workbench Microservice Ownership Map v1.xlsx (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-14823 | RWB-PLT-N001-APP | GAP-2837 |  | Keep the plan H, C, I and X rows. Record rwb-source-data and rwb-case as C rows with placeholders. Record RWB-PLT-TE006-CON as the wave 0 library for rwb.asset.events.v1. Add the asset row to the Ownership Map from Architecture v5 slides 19 and 41 and TSD S5 T3.1. Adopt REQ-S5-001. State in both APP stories that only RWB-S5-E3023-APP runs the R-DIS-06 clocks. |

### OTHER:RWB-S5-E3021 story file (APP and CON) (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-14824 | RWB-PLT-N001-APP | GAP-2847 |  | Keep H, C, I and X rows as planned. Declare the consumed AuctionResult event and three REST rows as facts with Day 1 fakes. Record RWB-PLT-TE006-CON as the wave 0 outbox and inbox library. |

### OTHER:RWB-S6-E6004 story file (APP) (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-14825 | RWB-PLT-N001-APP | GAP-2988 |  | Record the five consumed rows as class C with placeholders. Record RWB-PLT-TE006-CON as the wave 0 library. Fix API-S6-005 as this key's operation. Fix one writer per rule at assembly. |

### OTHER:RWB-S7-E6018 story file (APP) (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-14826 | RWB-PLT-N001-APP | GAP-3027 |  | Record five consumed rows as class C. Read delegation_limit as reference data. Carry out of scope R-WO-13 and R-WO-14. Claim EV-24 for the approved path. Record RWB-PLT-TE006-CON. |

### OTHER:RWB-S1-E4007 story file (plan H row) (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-14827 | RWB-PLT-N001-APP | GAP-2624 |  | Service owner or delivery lead confirms whether FEAT-VAL prerequisite stories are a build dependency. If yes, H row gains RWB-S1-E4005-APP and RWB-S1-E4006-APP. |

### OTHER:WP B2-S4-008 story files (APP and CON) (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-14828 | RWB-PLT-N001-APP | GAP-2773 |  | Name the rwb-partner panel and instruction reads and the rwb-case case-move answer as consumed rows. Build against fakes on Day 1 with a 2 s budget and a breaker. |

### OTHER:The two deferral step stories named in GAP-2829 (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-14829 | RWB-PLT-N001-APP | GAP-2829 |  | Declare the three consumed owner contracts in section 12.2 as consumed and faked on Day 1. Keep metadata rows as the plan gives them. |

### RWB-S5-E3024-APP (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-14830 | RWB-PLT-N001-APP | GAP-2860 |  | Fix the figure as an asset count with book_value and holding_cost_to_date totals by holding_status. Serve it on GET /assets. Owner is role RW-NPAMGR. Record R-DIS-01 and R-DIS-02 as built by sibling stories. |

### OTHER:RWB-S5-E3019 story file (APP and CON) (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-14831 | RWB-PLT-N001-APP | GAP-1906 |  | Keep plan H, C, I and X rows. Record rwb-source-data, rwb-case and DP-09 rows as needed dependencies. Declare AssetTakenOn from the outbox. Read REQ-S5-001 with a note that the plan carries no requirement id. |

### OTHER:RWB-S6-E5024 story file (APP and CON) (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-14832 | RWB-PLT-N001-APP | GAP-1952 |  | Keep plan H, C, I and X rows. Record rwb-source-data, rwb-agent, rwb-case and rwb-decision as class C dependencies. Fake each on Day 1. Keep DP-04 and DP-09 rows in the register. |

### RWB-S6-E6002-APP; OTHER:TSD S6 and DB story for the service (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-14835 | RWB-PLT-N001-APP | GAP-2984 |  | Keep the plan H, C, I and X rows; declare rwb-partner as class C with a placeholder name and 2 s budget; declare the package as an activity on rwb-decision and the case move as the child stage outcome; record the bid as a decision record and raise the bid table for the DB story; keep wave 4 and the tentative date; adopt REQ-S6-004. |

### RWB-S6-E6003-APP (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-14836 | RWB-PLT-N001-APP | GAP-2986 |  | Keep the plan H row; build on Day 1 against six contract fakes with a 2 s budget and a breaker; declare no provided operation and run the branch behind API-S6-003 and API-S6-004; carry the three placeholders in text and contract; delegate the re-offer to R-DS-28 at RWB-S6-E6005-APP; record the wave conflict once for the service and EP06. |

### RWB-S6-E6009-APP (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-14837 | RWB-PLT-N001-APP | GAP-3008 |  | Keep the plan H, C, I and X rows and record the five consumed rows as class C with placeholders; declare no provided operation and reach the step through sibling lot and data room reads; read the claim window as a versioned parameter with a placeholder; hold realized recovery on the account selling_price and closed lot; keep wave 4; record the W-MAP conflict once for S6 and EP06; keep the four criteria. |

### OTHER:RWB-S6-E6002 story (CON and APP) (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-14839 | RWB-PLT-N001-APP | GAP-1969 |  | Keep the metadata rows as the plan states them; declare the four consumed contracts and the authorise call as class C rows in the text and registers; name REQ-S6-004 as the requirement; confirm the three operation names with their owners before baseline tag. |

### RWB-S6-E6005-APP (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-14840 | RWB-PLT-N001-APP | GAP-2990 |  | Declare the six consumed rows in 12.2 with owners, budget and placeholder; fake them for the build in 12.8; keep the metadata C row as the plan states it. |

### RWB-S6-E6010-APP (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-14841 | RWB-PLT-N001-APP | GAP-3010 |  | Keep the plan H, C, I and X rows; record rwb-case, rwb-access and rwb-decision as class C with placeholders; declare no provided operation and name API-S6-003 of RWB-S6-E6005-APP as the start signal; record the open-action set as an assumption; run the unattended step under the rwb-debtsale service identity; declare no adapter for ALS or GL. |

### RWB-S6-E6006-APP (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-14842 | RWB-PLT-N001-APP | GAP-2996 |  | Build against the plan H row and the published documents and fakes of the five owners; declare the six rows in 12.2 with placeholders and in 12.8 with fakes; ask the plan owner to add the C rows of P5, P6, P1, P3 and P7 to the key. |

### RWB-S7-E6022-APP (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-14843 | RWB-PLT-N001-APP | GAP-3035 |  | Keep the plan H, C, I and X rows and record the four reads and the feed call as class C with placeholders; declare no provided operation and name API-S7-001 and API-S7-002 for the scan and committee decision; carry feed status and tax file reference in the decision record with no new column; read the tax criteria version as reference data and hold the case with MSG-S7-001 when none is in force. |

### OTHER:Technical Specifications by Module v6 (S7 T-A.1; OTHER:T3.1; OTHER:T3.2; RWB-S7-E6024-APP (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-14844 | RWB-PLT-N001-APP | GAP-3039 |  | Add the correction operation on the write-off base with placeholder path and elements, read its vocabulary, retry count, owner and time limit from the sources the proposed fix names, carry R-WO-41 and R-WO-43, and add the SCR-27 exception state. |

### RWB-S7-E6027-APP; OTHER:T5.2; OTHER:T5.3) (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-14845 | RWB-PLT-N001-APP | GAP-3046 |  | Declare the recovery event-driven with no operation of its own; consume the P8 event on rwb.payment.events.v1 with placeholder name and payload; add fee reference, reporting gap and screen state per the proposed fix. |

### OTHER:rwb-decision rule set (UNIVERSAL), rwb-source-data, rwb-access, and FSD S8 A2.19 / TSD S8 T3 (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-14846 | RWB-PLT-N001-APP | GAP-3070 |  | Publish one UNIVERSAL rule row for a contact sent against a contact stop routed to the Conduct and QA officer; decide breach storage; publish the ledger read and SCR-08 breach read; correct the RW-CONDUCT right; settle the service level. |

### RWB-PLT-E1072-CON (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-14847 | RWB-PLT-N001-APP | GAP-0822 |  | Keep compile, checks and SIT scenario run in rwb-decision; record in the build plan that rwb-access embeds no Drools kit and carries no DP-04. |

### RWB-PLT-N006-INF (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-14848 | RWB-PLT-N001-APP | GAP-1394 |  | Fix the deployment topology and screen-model field list in the edge design review; record the officer inbox push transport with the ACE front-end team before the first integration test. |

### RWB-PLT-NF02-APP (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-14849 | RWB-PLT-N001-APP | GAP-1400 |  | Fix the helper package, registry and version label; fix the error-map path at the library resource root; read the Idempotency-Key expiry window and store timeout as chart configuration; record the stamping rule before the template pin moves. |

### OTHER:Technical Specifications by Module v6 (T0 Service section) or a PLT module file in Functional Specifications by Module (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-14850 | RWB-PLT-N001-APP | GAP-1664 |  | Write the platform functional specification and map FR-PLT-001 to FR-PLT-034 to its FSD and BRD requirement IDs. |

### 04 User stories/Recovery Workbench Service Story Catalog v1.xlsx; OTHER:Release column) (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-14851 | RWB-PLT-N001-APP | GAP-3227 |  | Assign the wave-0 platform stories RWB-PLT-N001 to N012 and their CON variants, and RWB-PLT-NF01 to NF08, to the Window 1 release E1 (30 November 2026, tentative). |

### OTHER:Delivery plan (H rows of the RWB-S6 and RWB-S9 slices) (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-14854 | RWB-PLT-N001-APP | GAP-1959 |  | Add a plan row for API-S6-004 as one Partner portal operation of rwb-debtsale, routed via the partner gateway and rwb-partner panel; keep PT-BUYER RU (own cases) and Partner portal R (staff); operation name placeholder. |

### RWB-P1-AD018-APP; RWB-P1-AD018-CON; RWB-P1-AD018-OPS (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-14856 | RWB-PLT-N001-APP | GAP-0516 |  | Assign SCR-44 gateway-bff route: APP serves the reads, CON publishes them against RWB-PLT-N001-CON, OPS registers the gateway-bff route and its alerts. |

### RWB-P1-E1001-APP (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-14857 | RWB-PLT-N001-APP | GAP-1279 |  | Name the rwb-decision login (DP-02); fix migration file and sequence at merge under D-RCV-28; declare the 7 standard column Field IDs as a build artefact; carry six platform contracts in preconditions. |

### OTHER:Work Package story line WP B2-P8-008 (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-14858 | RWB-PLT-N001-APP | GAP-2540 |  | Keep metadata H None and Ready to start Day 1; name the six platform contracts as the service baseline in preconditions and fakes. |

### RWB-P5-E1016-APP (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-14859 | RWB-PLT-N001-APP | GAP-1028 |  | Record the secondary P5 split; publish GET retention-classes endpoints with RetentionClass shape of RWB-P5-AD021-CON; add C entries for consumed P4, P3 and P1 operations at verification loop. |

### OTHER:Work Package story line and pattern table 12.2 and 12.8 of the affected secondary slice (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-14860 | RWB-PLT-N001-APP | GAP-2429 |  | Name the five H rows, the C row RWB-P3-E1043-CON and the DP-11 authorise contract in the pattern table and 12.8 fakes; step D1 decides the dependency map entry. |

### RWB-S8-E1023-APP (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-14861 | RWB-PLT-N001-APP | GAP-3082 |  | Record the slice as secondary serving of the case page with deviation block and assembly; declare the seven platform contracts as build prerequisites and fakes; keep wave 1 by R5.6, release tentative. |

### RWB-S9-E1032-APP (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-14863 | RWB-PLT-N001-APP | GAP-3140 |  | Keep H list as the work package fixes it; record the seven platform rows as the shared wave-0 baseline; revisit only if a contract is unpublished at the wave 1 entry check. |

### RWB-PLT-N001-CON; 05 Technical architecture/Recovery Workbench Service Contract Catalog v1.md (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-14864 | RWB-PLT-N001-APP | GAP-1083 |  | Record that the Litigation right and the scope test of the notice operations are enforced at the edge under RWB-PLT-N001-CON; add DP-08 and RWB-P4-E1037-CON to this story only if the check moves into the service. |

### RWB-P3-E1052-APP (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-14865 | RWB-PLT-N001-APP | GAP-0754 |  | Keep the metadata rows as the WP gives them (H empty). Name the DP-03, DP-07, DP-09, DP-15 and DP-19 platform contracts in its pattern table and preconditions. |

### RWB-P6-E1063-APP (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-14867 | RWB-PLT-N001-APP | GAP-1212 |  | Add the eight DP-added rows to its plan H and C dependency lists (H RWB-PLT-E1042-CON, C RWB-P3-E1042-CON, H RWB-PLT-E1043-CON, C RWB-P3-E1043-CON, H RWB-PLT-TE006-CON, H RWB-PLT-E1071-CON, H RWB-PLT-E1044-CON, H RWB-PLT-N001-CON), or record the ASM-B-P6-05-E1063-3 basis. |

### 05 Technical architecture/Recovery Workbench Service Template Specification v1.md (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-14868 | RWB-PLT-N001-APP | GAP-1053 |  | Record the DEV storage account and container names, the rwb-document login and the DEV read-only role; publish the SCR-30 and SCR-31 composite route with RWB-PLT-N001-CON. |

### RWB-P6-E1073-APP (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-14869 | RWB-PLT-N001-APP | GAP-1218 |  | Add the eight platform CONs (RWB-PLT-E1027-CON, RWB-PLT-E1072-CON, RWB-PLT-E1042-CON, RWB-PLT-E1043-CON, RWB-PLT-E1071-CON, RWB-PLT-E1047-CON, RWB-PLT-E1044-CON, RWB-PLT-N001-CON) to its H list, or state them as wave-0 prerequisites in the lane document. Keep Day 1. |

### OTHER:gateway-bff composite route definition (Solution architect) (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-14873 | RWB-PLT-N001-APP | GAP-0913 |  | Publish the composite route for SCR-03 and its other products panel with its field list and masking step under RWB-PLT-N001-CON. |

### RWB-P3-E2004-CON (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-14874 | RWB-PLT-N001-APP | GAP-1340 |  | Read the twelve DP-added dependencies from its section 13 during build-order and dependency-map assembly. Keep its metadata rows as the WP fixes them. |

### 04 User stories/Recovery Workbench Service Story Catalog v1.xlsx (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-14875 | RWB-PLT-N001-APP | GAP-2484 | header | Give GET /cases/{caseId}/recommendation to the P7 story that serves the decision screen. Treat the four platform H contracts as published before Day 1. Header metadata stays as the WP fixes it. |

### RWB-P2-E2007-CON (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-14876 | RWB-PLT-N001-APP | GAP-2488 |  | Keep the metadata rows as the WP fixes them. Name every added row in its pattern table and the fakes of 12.8. Let step D1 decide whether the seven H rows and four consumed contracts enter the dependency map. |

### OTHER:RWB-E2-008 story (legacy set) (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-14877 | RWB-PLT-N001-APP | GAP-1349 | header | Answer the case payment list through GET /proceeds with case scope. Name workflow matchPayments and its four step activities. Leave the SCR-28 and run-view field lists with RWB-PLT-N001-CON. |

### RWB-P8-E2008-CON (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-14878 | RWB-PLT-N001-APP | GAP-2496 |  | Keep the metadata rows as the WP fixes them. Name every added row in its pattern table and the fakes of 12.8. Let step D1 decide whether the eight H rows and four consumed contracts enter the dependency map. |

### RWB-S8-E2012-APP (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-14879 | RWB-PLT-N001-APP | GAP-3091 | header | Slice RWB-S8-E2012-APP carries H [] and one C row. Add the eight platform H rows as tracked at the next plan revision. This story keeps Depends on (build) None and Day 1. |

### RWB-P6-E2014-APP (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-14880 | RWB-PLT-N001-APP | GAP-2389 | header | Keep H empty. Add the six platform contracts and the two rwb-case contracts to the C list at the next plan revision. |

### OTHER:Work Package dependency rows of the stories that DP-03; OTHER:DP-06; OTHER:DP-07; OTHER:DP-09; OTHER:DP-15 and DP-19 apply (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-14883 | RWB-PLT-N001-APP | GAP-1282 | Header | Add the six platform H rows and three published C rows as DP-added dependencies; keep Ready to start = Day 1. |

### OTHER:Work Package dependency rows of the stories that DP-03; OTHER:DP-06; OTHER:DP-07; OTHER:DP-09; OTHER:DP-10 and DP-19 apply (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-14884 | RWB-PLT-N001-APP | GAP-1286 | Header | Add the six platform H rows and two rwb-case C rows as DP-added dependencies; keep Ready to start = Day 1. |

### OTHER:Work Package dependency rows and service baseline of the stories that DP-03; OTHER:DP-06; OTHER:DP-07; OTHER:DP-09; OTHER:DP-15 and DP-19 apply (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-14885 | RWB-PLT-N001-APP | GAP-1288 | Header | Add the six platform H rows, two rwb-case C rows, the store baseline and the rwb-access authorise contract as DP-added dependencies. |

### OTHER:Section 13 of the story named in GAP-2312 (WP B2-P4-021) (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-14886 | RWB-PLT-N001-APP | GAP-2312 | Header | State which metadata rows are not used and list the platform and rwb-case contracts as build-against dependencies; confirm the H chain at the wave 2 gate. |

### OTHER:The agent monitoring dashboard v2 story (legacy RWB-E2-031 deployment slice) (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-14887 | RWB-PLT-N001-APP | GAP-0631 | Header | Name the rwb-agent login by secret reference (DP-02); register the route under RWB-PLT-N001-CON; make thresholds and topology chart values; update the Schedule in place; verify the consume right without a consumer group. |

### RWB-P7-E2035-APP (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-14888 | RWB-PLT-N001-APP | GAP-2410 | Header | Record that the slice builds against the platform contracts and published fakes and reads the same service's wave-1 rows through its own schema. |

### RWB-P7-E2042-APP (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-14889 | RWB-PLT-N001-APP | GAP-1296 | Header | Carry the eight platform H and three C DP-added dependencies in the story as build-against items; keep metadata as written and Ready to start = Day 1. |

### OTHER:The story named in GAP-2398 (Work Package row and its sections 13 and 18) (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-14890 | RWB-PLT-N001-APP | GAP-2398 | Header | Carry the eleven added rows in the DP application of section 13 and section 18; leave the WP metadata rows as they are. |

### RWB-P6-E5002-APP (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-14892 | RWB-PLT-N001-APP | GAP-1190 | Header | When the plan is regenerated, add RWB-PLT-E1027-CON and RWB-PLT-N001-CON to this story's build list; keep the plan rows until then. |

### OTHER:Story set next version (metadata rows of the stories the DP rows apply) (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-14893 | RWB-PLT-N001-APP | GAP-1319 |  | Carry the seven platform H dependencies, the three published C dependencies and the P4 authorise answer as DP-added rows in the dependency map; keep Ready to start Day 1; correct metadata rows at the next version. |

### OTHER:Story set version 3 order (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-14894 | RWB-PLT-N001-APP | GAP-3244 |  | Show the wave 0 platform stories N001 to N012 and harness stories W1J01 to W4J01 as Day-1 work before window 1. |

### OTHER:RWB-E4-041 legacy story (notice feature) (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-14896 | RWB-PLT-N001-APP | GAP-1154 |  | Remove SCR-33 Template approval, VR-P6-020-1, the notice operations and the A2.20 notice metric from the document request key; assign the answer screen to RWB-PLT-N001-CON and the template rule to rwb-comms template stories. |

### RWB-P6-E4035-APP (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-14897 | RWB-PLT-N001-APP | GAP-2368 |  | Add the S2 and P1 contract stories to the C list and the S8 deviation event rows to the I list when planned; keep the drift test as the guard until then. |

### OTHER:Work Packages B-P4-04 and B2-P4-010, and checks/run_all.py (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-14898 | RWB-PLT-N001-APP | GAP-2278 |  | Remove RWB-AD-016 from the B-P4-04 fanout so B2-P4-010 alone owns it; number CG and ASM IDs once; add a plan-uniqueness check to checks/run_all.py. |

### RWB-S5-E4030-APP (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-14899 | RWB-PLT-N001-APP | GAP-2953 |  | Declare the inbox and outbox as platform capabilities and the package as loaded through the service template; claim no new H row in this wave; raise the platform question at the next plan revision. |

### RWB-S3-E4015-APP (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-14900 | RWB-PLT-N001-APP | GAP-2716 | find it | Add contract rows for the rwb-decision P7 rule package and the rwb-case P3 reference data to H, or declare both as template capabilities. |

### RWB-S4-E5011-CON (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-14901 | RWB-PLT-N001-APP | GAP-2790 | find it | Name the rwb-decision rule package read and the rwb-case reference-data ride on the contract rows; add DP-04, DP-06 and DP-07 dependency rows centrally if the plan is revised. |

### RWB-PLT-N001-CON; 05 Technical architecture/Recovery Workbench Service Template Specification v1.md (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-14902 | RWB-PLT-N001-APP | GAP-1430 | find it | Name the per-service module map file in the template; publish the gateway-bff composite route list in RWB-PLT-N001-CON. |

### RWB-PLT-N001-CON; 06 Data/Recovery Workbench Reference Data and Lists of Values v5.xlsx (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-14905 | RWB-PLT-N001-APP | GAP-2891 | find it | Name the eviction state of SCR-22 in the composite route specification; the reference-data owner decides whether LOV-HOLDING gains a value or the state stays an element of the asset answer. |

## 6. Register gaps linked to this service (Gap Register v2 status)

| GAP ID | Title | Owner role | Status |
|---|---|---|---|
| GAP-0072 | The tool gateway is named by the source and given no owner | P10 rwb-agent | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-0078 | The screen for a run and its gateway route have no owner row | Platform architect | Resolved (directive) |
| GAP-0094 | The gateway-bff composite screen routes are not specified in the API source | Solution architect | Resolved (directive) |
| GAP-0141 | The API Specification v4 paths are the monolith paths while the Service Catalog states the per-service base | Solution architect | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-0385 | The wave 1 journey harness environment, seeded data, evidence format and release gate are not specified | QA lead | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-0386 | ACE plan-status harness pack: environments, seeding, evidence format, gate and composite route are not specified | Integration lead | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-0390 | Customer other-products harness pack: repository, environments, seeding, evidence format, gate and composite route are not specified | Integration lead | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-0401 | The gateway-bff composite route and the harness pack for the document generation screens are not specified | Integration lead | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-0428 | The wave 2 journey harness environment, seeded data, evidence format and release gate are not specified | QA lead | Resolved (directive) |
| GAP-0516 | SCR-44 is a gateway-bff route on a P1 story that builds no screen | DevOps lead | Resolved (directive) |
| GAP-0629 | The app slice of the agent monitoring dashboard v2: the drift step's place, the segment on the run row, the decision-log filter and elements, the notice operation, the policy values, the migration number, the range limits, the login, the route path and the name of the right are not fixed by any source | Solution architect | Resolved (directive) |
| GAP-0630 | The contract slice of the agent monitoring dashboard v2: the member types of the v2 element, the paging, the names of the drift inputs, the agent-version filter, the notice operation and the route path are not fixed by any source | Tech lead of rwb-agent | Resolved (directive) |
| GAP-0631 | The deployment slice of the agent monitoring dashboard v2: the topology, alert thresholds, login, route path, the Schedule update path and the consumer group ownership are not specified | Platform administrator | Resolved (directive) |
| GAP-0660 | rwb-integration composed case-list read and export: ownership duplication, service-base paths, ageing and access-log contracts, parameters, reference data and flag switch not settled | Solution architect | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-0662 | rwb-integration customer products read: login, contract field names, ACE view owner, endpoint and route names, masking rows and flag switch not settled | Solution architect | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-0672 | rwb-integration rule copy: the H and C rows, the model-fetch surface, the assigned package, the local copy table, the event consumers and the login are not settled by any one source | Solution architect | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-0673 | rwb-integration ALS settlement booking: the interface itself, the modelling of INT-03, the field mapping, the metadata rows and the login are not settled by any one source | Solution architect | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-0674 | gateway-bff composite route for the case screens is not specified | Solution architect | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-0693 | The gateway-bff composite route specification for SCR-03 is not given | Solution architect | Resolved (directive) |
| GAP-0728 | RWB-AD-019 in rwb-case: login name, edge composite route, source-data read shape and contract placement not specified | TechX | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-0732 | The case-side approval task shape, the approval-to-case status mapping, the escalation signal, the composite route and the rwb-case login are not specified in the source documents | Solution architect | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-0754 | The platform contract dependencies of the pattern table are not carried in the metadata rows | RW-COE | Resolved (directive) |
| GAP-0773 | The gateway-bff composite route of the case record plan section is not specified | Solution architect | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-0807 | rwb-access access review list: JOB-18 is a Temporal Schedule but the story metadata carries no workflow-kit dependency and no cron | Solution architect and the platform workflow owner | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-0822 | rwb-access rule-version load: the compile, the checks and the SIT scenario run need the Drools kit RWB-PLT-E1072-CON, which is not in this story's build list | Solution architect | Resolved (directive) |
| GAP-0867 | The administration home operation, its fields, its parameter name, its entitlement rule and its record code are not in the sources | Tech lead | Resolved (directive) |
| GAP-0873 | The QA-sample operations, the missing P7 dependency, the draw rule and the reason-code set of RWB-E8-013 are not specified in any source | Tech lead | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-0879 | The incident operations, the step record code, the detection feed and the incident screen are not in the sources | Solution architect, with the platform administrator | Resolved (directive) |
| GAP-0909 | rwb-access plan status: the per-service login name and the gateway-bff composite route field list behind SCR-03 and the plan status panel are not specified | Solution architect | Resolved (directive) |
| GAP-0913 | The field list and the masking step of the gateway-bff composite route for the other-products panel are not specified | Solution architect | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-0944 | rwb-access document set: the composite route field list of SCR-14 and SCR-30, and the decision code of an allowed screen action entry, are not specified | Solution architect | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-0951 | Whether the field app reaches the authorise path through gateway-bff or directly is not specified | Solution architect, P4 with the gateway-bff route owner | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-0955 | The authorise shape for a send and the field list of the composite route are not specified | Solution architect, P4 and the gateway-bff owner | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-1028 | The secondary P5 slice of RWB-E1-016 owns no legacy AC, and the DP10 catalog composition, the retention-class operation path and answer, the consumed contracts, the login and the product code are not fixed as this slice needs them | Solution architect | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-1035 | The SCR-30 route specification in the gateway-bff composite route is not specified | Solution architect, with the gateway-bff squad | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-1053 | The DEV Blob container names, the rwb-document login name and the DEV read-only role name are not specified | Platform administrator | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-1083 | The scope and right check of the notice operations has no rwb-access dependency row | Solution architect | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-1154 | The legacy rows of RWB-E4-041 are carried over from notice generation | Business analyst | Resolved (directive) |
| GAP-1156 | document_custody is a P6 module table in the legacy story and a P5 rwb-document table in the target, and the P5 custody contract has no C row and no contract story | solution architect with the P5 rwb-document owner | Resolved (directive) |
| GAP-1161 | The dependencies DP-03, DP-07, DP-09, DP-10 and DP-19 add are absent from this story's build and contract lists, and no fake is named for the reference data or the decision record | Solution architect | Resolved (directive) |
| GAP-1167 | RWB-P6-E1011-APP: the seven platform CONs added by DP-03, DP-06, DP-07, DP-10, DP-14, DP-15 and DP-19 are missing from the story's H list | Solution architect | Resolved (directive) |
| GAP-1190 | The platform contract rows that DP-03 and DP-19 add are not in this story's build list | Tech lead | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-1198 | The DP-added platform and P3 contracts are missing from the story dependency rows | Release manager | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-1206 | The build and contract dependency lists of the plan do not carry the dependencies the DP table adds to this key | Solution architect | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-1212 | The platform and reference contracts that DP-06, DP-07, DP-09, DP-10, DP-15 and DP-19 add are missing from the plan dependency lists of this story | platform owner, P3 case owner and delivery lead | Resolved (directive) |
| GAP-1218 | RWB-P6-E1073-APP: the platform H dependencies that DP-03, DP-04, DP-06, DP-07, DP-10, DP-14, DP-15 and DP-19 add are absent from the story's H list | Tech lead | Resolved (directive) |
| GAP-1223 | The plan's H and C lists for this story name None and RWB-P7-E2013-CON, and omit the platform and published contracts that the DP table adds | Delivery lead | Resolved (directive) |
| GAP-1258 | The field-level list and the mask flags of the D7.1 approval screen are published by no source | Solution architect | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-1259 | The composite-route name and path segment of the approval screen are not specified | Solution architect | Resolved (directive) |
| GAP-1265 | Two consumed contracts carry no C row in this key | Solution architect | Resolved (directive) |
| GAP-1267 | The legacy screen states and the platform route states are two unreconciled vocabularies | Business analyst | Resolved (directive) |
| GAP-1270 | The timeout budget of a screen that composes three reads is not specified | Solution architect | Resolved (directive) |
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
| GAP-1335 | Platform and published dependencies added by the patterns but not carried in the metadata rows | Delivery lead | Resolved (directive) |
| GAP-1337 | Platform and published dependencies added by the patterns but not carried in the metadata rows | Delivery lead | Resolved (directive) |
| GAP-1340 | DP-added platform and published dependencies are not carried in the metadata rows | Solution architect | Resolved (directive) |
| GAP-1343 | The platform and published dependencies this slice adds through the decoupling patterns are not carried by the empty metadata rows | Solution architect | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-1349 | RWB-E2-008: the case payment read, the SCR-28 and run-view field lists and the activity names of JOB-07 are not fixed by any source | Solution architect | Resolved (directive) |
| GAP-1393 | gateway-bff public path table, inbox push transport and payment-tab operation are not stated by any source | Solution architect | Resolved (directive) |
| GAP-1394 | gateway-bff deployment topology, screen-model schema, inbox push transport and gateway sizing are not stated by any source | Tech lead | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-1400 | The artefact coordinates of the helper, the error-map source, the header format and the ordering with the edge are not specified for the implementation | Platform library lead with the platform architect | Resolved (directive) |
| GAP-1430 | The per-service module-map file name and the gateway-bff composite route list are not specified | Solution architect | Resolved (directive) |
| GAP-1436 | One rule set, one pinned dictionary version, its read path and the allow-list approver after the marks became reference data | Solution architect | Resolved (directive) |
| GAP-1664 | No FSD module exists for the platform, so no FSD requirement ID states a platform capability | Business analyst | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-1730 | No source fixes the screen ownership or the gateway route of SCR-17 | Solution architect | Resolved (directive) |
| GAP-1885 | Three consumed contracts and two platform reads of the petition have no dependency row, and two of the three operation names exist in no source | Solution architect, S4 rwb-litigation, with the P7 rwb-decision, P3 rwb-case and S9 rwb-partner architects and the platform team | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-1898 | The five H rows and two C rows that DP-06, DP-07, DP-09, DP-10 and DP-19 add are absent from this story's build and contract lists | Solution architect, with the platform library owners and the rwb-case owners | Resolved (directive) |
| GAP-1903 | Several values of the slice are not named by any source: the apply trigger on the patch, its write key, the request element names of the fill, the hearing natural key, the parameter operation names and the composite-route field list | Tech lead and solution architect | Resolved (directive) |
| GAP-1906 | RWB-S5-E3019: the take-on slice has no source for its dependency rows, its event, its case move, its requirement id and the duplicated R-DIS-06 criterion | Solution architect | Resolved (directive) |
| GAP-1946 | RWB-S5-E1011-APP: the asset slice of RWB-E1-011 has no source for its dependency lists, its ACE-side read, its quality objects, its rights and its run cadence, and the data-lake and Power BI target of the legacy key is removed | Solution architect | Resolved (directive) |
| GAP-1947 | RWB-S6-E5023: the eligibility slice has no C row for its four consumed rows, no DP-04 row and no requirement id | Solution architect | Resolved (directive) |
| GAP-1952 | RWB-S6-E5024: the lot build and price step needs rwb-source-data, rwb-agent, rwb-case and rwb-decision while the plan's C row is empty | Solution architect | Resolved (directive) |
| GAP-1958 | RWB-S6-E5026: the data-room slice carries an empty C row although it needs rwb-document, rwb-partner and rwb-case, and the plan holds no requirement id | Solution architect | Resolved (directive) |
| GAP-1959 | RWB-S6-E5026: the partner channel of the data-room read has no plan row and the right is stated twice with different holders | Solution architect | Resolved (directive) |
| GAP-1963 | RWB-S6-E6001: the plan gives this step an empty C row while it consumes rwb-decision, rwb-access and rwb-case, and two of the consumed operations have no published name | Solution architect | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-1969 | RWB-S6-E6002: the qualification slice has no C row, no requirement id and no case-move or authorise operation although it needs rwb-partner, rwb-case, rwb-decision and rwb-access | Solution architect | Resolved (directive) |
| GAP-1986 | gateway-bff and the partner gateway have no owner code, no wave and no service row | Platform team | Resolved (directive) |
| GAP-2099 | The shared edge has no owner row: gateway-bff, the Redis session and the App Gateway route | Platform architect | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-2188 | The client contract has no source member types, refusal detail or record reference shape | Solution architect | Resolved (directive) |
| GAP-2261 | Depends on (build) is empty while the DP table adds platform H dependencies | TechX | Resolved (directive) |
| GAP-2278 | Two Work Packages write the same two story files and the same two fragments for legacy RWB-AD-016 on rwb-access | Delivery lead | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-2281 | The panel-change operation, its fields, the table code, the record code, the compensation, the screen and two owner contracts are not in the sources | Tech lead of rwb-access | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-2288 | The pack, its three check codes, the two operations, the five schemas, the parameter rows, the decided-version rule and the record code are not in the sources | Tech lead of rwb-access | Resolved (directive) |
| GAP-2296 | The daily chain check has no job row in the Batch and Scheduling Design and the workflow kit dependency is absent from the Work Package | Solution architect with the platform workflow owner | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-2301 | The incident record, its three operations, its record code and its right are not in the sources, and the legacy permission table conflicts with the technical specification | Solution architect | Resolved (directive) |
| GAP-2304 | The access-change record code, the matrix version label, the matrix screen, the agent identity source and the grant's service event are not in the sources, and two sources disagree on the group column of a role and on the right of the path | Solution architect | Resolved (directive) |
| GAP-2312 | DP-added platform and published contracts are not in the metadata dependency rows | Solution architect, P4 | Resolved (directive) |
| GAP-2317 | The four platform contracts and the reference-data contract that the DP table adds are absent from the Work Package dependency lists | Solution architect | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-2333 | The Reporting right of the legacy story, the data-lake copy of the access rule, the event row of the service and the DP dependencies disagree with the target sources | Solution architect with the rwb-access and rwb-agent owners | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-2354 | The platform contracts and the P3 reference-data contract that the nine applied patterns add are absent from this story's build and contract rows, which the Work Package fixes as empty | Release manager | Resolved (directive) |
| GAP-2363 | The legacy screen, endpoints and rights of RWB-E4-035 serve an officer's notice screen, not a customer's offer view | Solution architect | Resolved (directive) |
| GAP-2367 | No source gives the capability area or the right of an offer-view operation, and the legacy story names the Litigation rights of another surface | Solution architect | Resolved (directive) |
| GAP-2368 | The two contracts and the contact-stop events the view depends on carry no C row and no source shape in this key's plan | Solution architect | Resolved (directive) |
| GAP-2379 | No source names a screen for the contact repository and the legacy screen is the template screen | Business analyst | Resolved (directive) |
| GAP-2389 | The plan records no build row for the platform contracts that the patterns of this slice add | Delivery lead | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-2398 | The DP table adds eight H rows and three C rows that the Work Package dependency rows do not carry | Tech lead | Resolved (directive) |
| GAP-2404 | The metadata rows name no build dependency and the agent contract only, while the DP table of the story adds five platform contracts and two rwb-case contracts and the story consumes a further authorise operation | Delivery lead | Resolved (directive) |
| GAP-2410 | A secondary registry slice carries no build dependency while the DP rows add seven platform contracts and four published contracts | Delivery lead | Resolved (directive) |
| GAP-2412 | Placement record slice: element names of the decision-record fact, the case read and the authorise call, the reference-data operation, the MSG-P7-009 text, the per-service login name and the platform contract rows are not in any source this story may read | Solution architect, rwb-decision, with the rwb-integration and rwb-case contract owners | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-2414 | The metadata rows name no build dependency and the P3 contract only, while the DP table adds eight platform contracts and four published contracts, and the registry operations this story amends sit in another lane of the same service | Delivery lead | Resolved (directive) |
| GAP-2419 | The platform build dependencies, the authorise answer and the agent contract that the patterns add are not in the metadata rows, and RWB-P10-TE013-CON is not written | Solution architect | Resolved (directive) |
| GAP-2429 | The eight patterns add five platform build dependencies, one reference-data contract and one authorise contract that the metadata rows of a secondary slice do not carry | Solution architect, with the delivery lead | Resolved (directive) |
| GAP-2448 | The metadata dependency rows name only the P5 contract, while the DP table adds platform and rwb-case and rwb-access contracts | Solution architect, P7 | Resolved (directive) |
| GAP-2453 | The P7 slice of RWB-E1-046, the row that holds the template version, the catalog read paths, the table and columns and the login are not settled by any one source | Solution architect | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-2455 | No source states which service appends the D7.1 generation record to the central ledger | TechX | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-2470 | RWB-P7-E2002-APP: the DP table adds six platform H rows, two C rows and one PLT object set that the metadata rows of the plan do not carry | Solution architect with the platform library owner and the rwb-decision service owner | Resolved (directive) |
| GAP-2475 | RWB-P7-E2004-APP: the DP table adds eight platform H rows, three C rows and a workflow-kit dependency that the metadata rows of a secondary slice do not carry | Solution architect with the platform library owner and the rwb-decision service owner | Resolved (directive) |
| GAP-2484 | The platform contracts the DP table adds are not in the metadata build row, and one provided operation has no story | P7 solution architect and the story-catalogue owner | Resolved (directive) |
| GAP-2488 | The eleven patterns add seven platform build dependencies and four consumed contracts that the metadata rows of a secondary slice do not carry | Solution architect, with the delivery lead | Resolved (directive) |
| GAP-2496 | The twelve patterns add eight platform build dependencies and four consumed contracts that the metadata rows of a secondary slice do not carry | Solution architect, with the delivery lead | Resolved (directive) |
| GAP-2501 | The DP table adds platform and published contracts that the metadata rows do not carry | Delivery lead, with the platform contract owners | Resolved (directive) |
| GAP-2533 | rwb-payment cutover load of RWB-DM-013: the handover file, the load command and its run record, a provenance column, the legacy payment_code column and the two schema-level H rows are fixed by no single source, and this slice owns no legacy criterion | Data steward and solution architect of rwb-payment, with the rwb-source-data owner, the schema baseline owner and the ACE team | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-2540 | The plan gives this story no H row, while its migration needs the schema, the login and the Flyway pipeline of the service | Solution architect | Resolved (directive) |
| GAP-2548 | No contract story is allocated to this legacy key, and the outbound manifest, the event payload, the data product code and the ALS interface values are unpublished | P8 solution architect, the P2 integration owner and the event catalogue owner | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-2602 | The outlier element of the route answer is in no published schema, and the approved answer carries only the approval elements | Solution architect of S1 with the owner of the edge contract (RWB-PLT-N001) and the API owner | Resolved (directive) |
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
| GAP-2832 | SCR-20 carries no deferred state and no source gives a screen field list for the reason and the review date | Solution architect with the edge owner and the business analyst of EP05 | Resolved (directive) |
| GAP-2837 | RWB-S5-E3019-APP: the take-on slice has no plan row for its cross-service reads, its outbox library, its requirement id or the duplicated R-DIS-06 criterion | Solution architect | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-2847 | RWB-S5-E3021: the take-on step consumes and publishes an event and reads four owner contracts, while the plan carries no C or I row and its pattern set omits DP-09 | Solution architect | Resolved (directive) |
| GAP-2860 | RWB-S5-E3024-APP: the stock balance has no figure definition, no write operation for its confirmation, no object in the TSD, no requirement id, and its two take-on rules are owned by sibling stories | Business analyst S5 with the solution architect and the rwb-access owner | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-2869 | RWB-S5-E3026: the cycle slice has no planned dependency row for its four consumed contracts or its Schedule library, and neither the plan nor the module model holds the re-appraisal record, the requirement id or the AC3 evidence | Solution architect | Resolved (directive) |
| GAP-2891 | The legacy screen list gives SCR-22 four states and names no eviction state, and no source names the state the screen shows | S5 rwb-asset service owner with the screen designer of the gateway-bff composite route | Resolved (directive) |
| GAP-2952 | The legacy screen states of SCR-22 do not match the holding lists and the states this step produces are case states | S5 rwb-asset service owner with the screen owner of RWB-PLT-N001 and the case owner of P3 | Resolved (directive) |
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
| GAP-3227 | The 23 new wave-0 platform stories have no release date | Delivery lead | Resolved (directive) |
| GAP-3244 | The new platform stories N001 to N012 and the harness stories W1J01 to W4J01 sit in no window of version 3 | Solution architect | Accepted (directive); change listed in the Cross-document Change Register v1 |

## 7. Unconfirmed assumptions (tied to a business decision)

None.

## 8. Lint findings on the staged stories

None.

# Recovery Workbench P1 decisions, batch D (RD-P1-060 to RD-P1-074)

SCB Collections and Recovery. Henka Group, 27 November 2026.
(C) Siam Commercial Bank and Henka Pte Ltd

| Item | Value |
|---|---|
| Run | D-RCV-60 P1 developer readiness (RD-P1 register), second round of rulings |
| Input | `SET\_work\p1-ready\ESCALATIONS.md` (items 1 to 63, extra stories, check lists) |
| Builds on | Recovery Workbench P1 Decision Register v1 (binding). Amendments are stated per decision under "Amends" |
| Prepared by | Chief architect (design sub-agent), Claude Opus 5.5 (claude-opus-5-5) |
| Status of every decision | Proposed – Claude Opus 5.5 (applied) |
| Precedence | D-RCV-60 and Architecture v5 (SET\22) > RD-P1 decisions > 16 Temporal and Drools (D-RCV-36) > 15 ACE DB Alignment (D-RCV-35) > 14 Story Updates > all other documents |

Abbreviations used for sources: Arch v5 = `SET\22 Microservice Realignment\Recovery Workbench Architecture v5 Text Extract v1.md`; YAML = staged `05 Technical architecture\Recovery Workbench API Specification v7\rwb-source-data.yaml` 5.1.0; PS v9 = staged `06 Data\Recovery Workbench Physical Schema v9\`; BSD v7 = staged Batch and Scheduling Design v7.xlsx; GR v3 = staged Gap Register v3.md; PCMD v4 = Party and Customer Master Data Design v4 (extract in REVIEW\_reference\06 Data); DCPI v5 = Data Classification and Personal Data Inventory v5 (extract); LDM v10 = Logical Data Model and Data Dictionary v10 (extract); DMA v4 = Data Migration Approach v4 (extract); EMS v5 = Error and Message Standard v5 (extract).

New pending items are given temporary IDs NEW-GAP-D1 to NEW-GAP-D9; the orchestrator assigns the next free GAP numbers after GAP-3282 (the last row of GR v3). Existing temp IDs raised by the editors (NEW-GAP-…) are kept and mapped by the orchestrator as usual.

## Index

| ID | Title | Escalation items |
|---|---|---|
| RD-P1-060 | Entity reads of rwb-source-data: customer, account and collateral; recipient name and postal address | 10, 16, 23, 51, 59, 61; S8 extra stories; E4045 account read |
| RD-P1-061 | `GET /payments`: one operation, two query forms, one builder | 4 |
| RD-P1-062 | Never-stamped data product: what every reader shows and does; freshness fixtures | 17, 18, 22, 62 (first part) |
| RD-P1-063 | Contract operations reported missing: verified state and the remaining additions | 25, 29, 34, 46, 47, 49, 51 (gateway codes), 54; checks |
| RD-P1-064 | Interaction ledger callers: letter dispatch and delivery entries, hand-recorded proof, permissions and entry types | 1, 26, 32, 37, 39, 40, 41, 50, 59 (failed append), 60, 62 (second part), 63; extra stories |
| RD-P1-065 | Job reads and reruns across services; readiness repeats | 12, 24, 27, 31 (rerun part), 48, 57 (first part) |
| RD-P1-066 | Event subscriptions, start rules and job owners; ACE boundary of rwb-payment | 5, 11 (start part), 13, 14, 15, 19, 20, 21, 30, 45, 53; ACE boundary E4044/E4045 |
| RD-P1-067 | EFS history: gate products, late EFS batch and the single appender | 2, 11, 26 |
| RD-P1-068 | Migration packages: decision chain, act-time snapshot fields, DM002, DM007 key, orphan checks, DP04, loader identity, local decision record table | 6, 7, 8, 9, 35, 36, 52, 57 (second part) |
| RD-P1-069 | Reconciliation breaks, orphan keys, REC-04/REC-06 and date-wide reads | 31 (break list), 33, 38 (held proof rows, REC-09), 42, 43, 44 |
| RD-P1-070 | Count-once store for failed contacts | 3 |
| RD-P1-071 | Data dictionary gate and new fields | 55 |
| RD-P1-072 | Decision records versus reads in the ledger intake; personal data seen by agents | 38 (call notes), 56 |
| RD-P1-073 | Test isolation for append-only rows and the shared sandbox | 28, 38 (sandbox) |
| RD-P1-074 | Build-chain depth and the E1066-OPS / E1067-APP cycle | 58 |

---

## RD-P1-060 · Entity reads of rwb-source-data: customer, account and collateral; recipient name and postal address

**Question.** No published operation gives rwb-comms, rwb-integration or gateway-bff the recipient name and postal address (items 23, 51, 59, 61), nor gives RWB-P3-E2006-APP the account and collateral (item 16), rwb-payment the account fee facts (E4045), or rwb-deviation the party flags that AceDataReady no longer carries (item 10). YAML says DP02 contact rows carry no value, name or address; RWB-P1-E1016-APP v3 AC returns `contact_value` clear to an unmasked role; `GET /customers/{id}` is cited by eight stories and published nowhere.

**Options considered.** (1) Widen `GET /data-products/DP02/records` to answer clear values. (2) Publish the three per-entity reads Architecture v5 names and keep the records read masked. (3) Leave Pending. Option 2 chosen: it is what Arch v5 states, and it keeps one read path per consumer need.

**Sources.** Arch v5 lines 736, 776 (case screen: gateway-bff calls rwb-source-data `GET /v1/customers/{id}` and `/v1/accounts/{id}`, "masked by policy"), 1075 and 1114 (P1 card: `GET /customers/{id}, /accounts/{id} · GET /collateral/{id}, /payments?accountId=`), 2884. PCMD v4 sheet Read paths R4 (gateway-bff, masked values only), R7 (rwb-deviation, deceased and bankruptcy flags, `GET /customers/{id}`), R8 (rwb-comms contact points for notices: GAP-0244, ASM-0334), R9 (`/accounts/{id}` with `v_ace_ca_relation`); PCMD v4 field rows R13-R22 ("Served by GET /api/recovery/source-data/v1/customers/{id}"); PCMD v3 line 74 (`contact_value` "in full, for notices and calls; contact_value_masked for display. Every read is audited"). DCPI v5 R1073 (DF-ACE-057 first_name) and R1094 (DF-ACE-078 contact_value): "Masked unless the role may see it", basis "legal obligation for statutory notices". PS v9 `recovery_views.sql` lines 191-260 (`v_ace_customer`, `v_ace_contact` columns). YAML lines 338-395 (records read, DP02 contact rule), 1764-1795 (`PartyExtFacts`, `AccountExtFacts`), 18 (GAP-3274). RWB-P1-E1016-APP v3 AC (line 282, FieldMasker unmasks `contact_value`), line 411 (`FieldMasker` of RWB-P4-E1037-CON), line 713 (out of scope: `/customers/{id}`, `/accounts/{id}`, `/collateral/{id}`, NEW-GAP-S4b-4). RWB-P1-DM002-APP v3 lines 299, 485 (the operation belongs to RWB-P1-E1069-APP; GAP-0566). RWB-PLT-N001-CON v3 lines 32, 267, 282 (composite route, NEW-GAP-F08-4).

**Precedence applied.** Arch v5 (top) fixes the three operations and the masking-by-policy rule. RD-P1-005 (wire names camelCase) and RD-P1-004 (Problem) apply. The YAML DP02 rule is kept; the E1016-APP AC that contradicts it moves to the new read.

**Ruling.**
1. **Operations added to `rwb-source-data.yaml` 5.1.0** (the staged, unreleased version of this run; `x-service.operations` 29 → 32; owner `P1`; builder **RWB-P1-E1069-APP**; contract fake `fakes/rwb-source-data/5.1.0/` gets examples per RD-P1-011):
   - `GET /customers/{personKey}` – operationId `getCustomer`; x-capability Case record R. `personKey` = ACE `person_key` (string, maxLength 255). Answer `Customer`: the `v_ace_customer` Section A columns in camelCase – `personKey`, `cifNo`, `firstName`, `lastName`, `dateOfBirth`, `deceasedDate`, `deceasedFlag`, `gender`, `nationality`, `maritalStatus`, `occupation`, `customerStatus`, `category`, `countryOfResidence`, `isStaff`, `branchCode`, `idNoMasked`, `idNoLast4` (`spouseName` and `vatNumber` likewise, personal); the Section B columns (`partyType`, `idType`, `segment`) are added when RWB-ACE-001 deploys, behind the DL43 flag (RD-P1-043); `partyFacts` = the four `PartyExtFacts` booleans of `party_ext` (`vulnerable`, `deceasedOverride`, `bankruptcy`, `fraudFlag`), null when the person has no `party_ext` row; `contacts[]` = the `v_ace_contact` rows of the person: `contactKey`, `contactType` (PHONE, EMAIL, ADDRESS), `usageCode`, `contactValue`, `contactValueMasked`, `city`, `postCode`, `country`, with `consentStatus` and `verifiedAt` of `contact_point_ext` as in `ContactPointRow`; `freshness` = `DataProductFreshness` of DP02. No freshness refusal: the answer carries the DP02 record and the caller applies its own stale rule.
   - `GET /accounts/{accountKey}` – operationId `getAccount`; Case record R. Answer `Account`: the `v_ace_account` Section A columns in camelCase, `relations[]` from `v_ace_ca_relation` (PCMD v4 R9), `accountFacts` = the `AccountExtFacts` of `account_ext` (null when no row), `freshness` = DP01. The multi-key account-page read for the case list stays Pending under GAP-3274; this is the single-account form GAP-3274 names.
   - `GET /collateral/{assetKey}` – operationId `getCollateral`; Case record R. Answer `Collateral`: the `v_ace_collateral` rows of the asset key in camelCase, plus the `v_ace_collateral_detail` columns once Section B is live (DL43 flag), `freshness` = DP06.
   - Errors (RD-P1-004): 400 MSG-GEN-001; 401 MSG-P4-001; 403 MSG-P4-002; 404 MSG-P4-003 for a key with no row or outside scope; 503 MSG-GEN-006. GET only: no Idempotency-Key. Every read is written to the access log (YAML records rule; PCMD v3 line 74).
2. **Masking.** Every field tagged `is_personal` passes through `FieldMasker.mask(dto, session)` of RWB-P4-E1037-CON for the caller's user session or workload identity; a field with no rule is masked (E1016-APP line 411). `contactValue` is answered clear only when `isUnmasked(contactValue, session)` is true; otherwise it carries the `contact_value_masked` value. The same holds for `firstName`, `lastName` and the address columns.
3. **Recipient name and postal address (item 61).** The clear name and postal address (`firstName`, `lastName`, and the ADDRESS row's `contactValue`, `city`, `postCode`, `country`, chosen by `contactKey`) are read only through `GET /customers/{personKey}`, by the rwb-comms notice workload identity (RWB-P6-E1007-APP, RWB-P6-E1032-APP, RWB-P6-E1052-APP/CON) and the rwb-integration outbound-file workload identity (RWB-P2-E1007-APP/CON, INT-14 WIN file). The masking rule rows that unmask those fields for those two identities are **Pending, owner data protection officer with the rwb-access (P4) owner**, tracked as NEW-GAP-D1 (narrows GAP-0244 / ASM-0334). **Interim build:** the FieldMasker fake carries rules unmasking `firstName`, `lastName` and `contactValue` for those two identities only; gateway-bff and every user role get masked values (PCMD v4 R4); tests assert both branches.
4. **DP02 records read keeps its rule.** `GET /data-products/DP02/records` answers contact rows with `contactKey`, `contactType`, `consentStatus`, `verifiedAt` only (YAML line 381). RWB-P1-E1016-APP's scenario "contact_value is returned clear with masked false" is re-targeted to `GET /customers/{personKey}`.
5. **Party flags (item 10).** AceDataReady carries the four fields of RD-P1-003 only. rwb-deviation reads `deceasedFlag`, `deceasedDate` and `partyFacts.deceasedOverride` / `partyFacts.bankruptcy` through `GET /customers/{personKey}` (PCMD v4 R7), one hop, 2 s; RWB-ITG-E7003-ITG and RWB-S8-E1020-APP (the one S8 story in Story Files v2 that takes the flags off AceDataReady) align.
6. **Callers named in the YAML `description` of each operation:** `getCustomer` – gateway-bff (case screen composite, RWB-PLT-N001-CON; closes NEW-GAP-F08-4), rwb-comms, rwb-integration, rwb-deviation, rwb-case (portal offer view facts through gateway-bff, item 59; RWB-P6-E4036-APP/CON), RWB-P1-DM002-APP verification; `getAccount` – gateway-bff, rwb-case, rwb-payment (RWB-P8-E4045-APP fee facts `collections_fee` DF-ACE-024), RWB-P3-E2006-APP; `getCollateral` – RWB-P3-E2006-APP, rwb-asset.

**Rationale.** Arch v5 already names the operations and their masking; publishing them removes the largest single cross-cutting blocker (five services) without widening the records read, and keeps the clear name and address behind one audited, rule-driven read.

**Affected services.** rwb-source-data (provider); gateway-bff, rwb-comms, rwb-integration, rwb-deviation, rwb-case, rwb-payment, rwb-asset, rwb-access (masking rules).

**Affected stories.** RWB-P1-E1069-APP (builds the three operations), RWB-P1-E1016-APP (AC re-target, out-of-scope line), RWB-P1-E1016-CON, RWB-P1-DM002-APP, RWB-P6-E1007-APP, RWB-P6-E1032-APP, RWB-P6-E1052-APP, RWB-P6-E1052-CON, RWB-ITG-E1052-ITG, RWB-P2-E1007-APP, RWB-P2-E1007-CON, RWB-ITG-E1007-ITG, RWB-ITG-E1065-ITG, RWB-PLT-N001-CON, RWB-P3-E2006-APP, RWB-P3-E2014-APP, RWB-P7-E2014-APP, RWB-P8-E4045-APP, RWB-ITG-E7003-ITG, RWB-S8-E1020-APP, RWB-P6-E4036-APP, RWB-P6-E4036-CON, RWB-P10-E8003-APP.

**Affected documents.** API Specification v7 `rwb-source-data.yaml` (three paths, schemas `Customer`, `Account`, `Collateral`, operation count, records description unchanged) and `index.yaml` count; Service Contract Catalog v3 (.md and .xlsx: three rows); Party and Customer Master Data Design (next version: Read paths R8 → `GET /customers/{personKey}`); Users Roles and Permissions v6 / Role to System Access Matrix v4 (masking rows Pending, NEW-GAP-D1); Gap Register v3 (GAP-0566, GAP-0549 closed; GAP-0244 narrowed; NEW-GAP-D1).

**Escalation items settled.** 10, 16, 23, 51 (first part), 59 (customer facts), 61; S8 extra story; ACE boundary of E4045 (account part). Temp gaps closed: NEW-GAP-F13-1, NEW-GAP-F02-1, NEW-GAP-F08-4, NEW-GAP-F15-4 (read published; masking rows remain as NEW-GAP-D1), NEW-GAP-S4b-4.

**GAP/ASM.** Closes GAP-0566 and GAP-0549 (response schemas); narrows GAP-0244 / ASM-0334 to NEW-GAP-D1; GAP-3274 unchanged (page form).

**Status.** Proposed – Claude Opus 5.5 (applied). Paths, callers and masking-by-policy are sourced (Arch v5, PCMD, DCPI); the path parameter names, operationIds, answer grouping (`partyFacts`, `contacts`, `relations`, `accountFacts`) and the null-when-no-row rule are Claude Opus 5.5 choices.

**Reuse note.** Any service that needs ACE party, contact, account or collateral facts of one key calls these three reads; it never asks for clear personal values elsewhere, and it never reads the DP02 records read for a contact value.

**Values chosen without a source.** operationIds `getCustomer`, `getAccount`, `getCollateral`; path parameter names `personKey`, `accountKey`, `assetKey`; group names `partyFacts`, `contacts`, `relations`, `accountFacts`; `partyFacts` / `accountFacts` null when no extension row.

---

## RD-P1-061 · `GET /payments`: one operation, two query forms, one builder

**Question (item 4).** `/payments` is used by RWB-P1-E2008-APP (`businessDate`) and RWB-P1-E1013-APP (`accountId`) with different query parameters; YAML publishes only the date form and records NEW-GAP-S10-14.

**Sources.** Arch v5 lines 1075, 1114 (`/payments?accountId=`); YAML lines 1129-1163 (`getPayments`, businessDate, PaymentsAnswer, NEW-GAP-S10-14, GAP-0601); register RD-P1-022 final ("readiness pair, `business_day_readiness`, `GET /payments`, `snapshot(page)` – RWB-P1-E1013-APP / RWB-P1-E1015-CON"); `/accounts/{accountKey}/installment-facts` (YAML line 1164) for the wire name of the ACE account key.

**Precedence applied.** Arch v5 fixes one path with an account query; RD-P1-022 fixes the builder; RD-P1-005 fixes the wire name (`accountKey`, the ACE key name used across YAML 5.1.0; Arch v5 `accountId` is the same key).

**Ruling.**
1. One operation `GET /payments` (operationId `getPayments`), builder **RWB-P1-E1013-APP** (RD-P1-022, not amended); contract published in RWB-P1-E1015-CON.
2. Query: exactly one of `businessDate` (date) or `accountKey` (string, maxLength 255). Both or neither → 400 MSG-GEN-001 with `field`.
3. `businessDate` form: unchanged from YAML 5.1.0 (one row per `paymentCode` from `v_ace_payment` for the date, ordered by `paymentCode`, `batchStatus` and `productStatus`, 409 MSG-P1-001). Its rules are those written in RWB-P1-E2008-APP, which keeps them as the acceptance criteria of that form and gains an H dependency on RWB-P1-E1013-APP; RWB-P1-E2008-APP keeps building `GET /accounts/{accountKey}/installment-facts`.
4. `accountKey` form: the `v_ace_payment` rows of the account, ordered by `paymentDate` then `paymentCode`, in the same `PaymentsAnswer` shape with `businessDate` = the DP01 stamp in use; same 409 rule.
5. Paging and row cap stay Pending (GAP-0601, NEW-GAP-S10-04, owner data architect); interim unpaged for both forms.
6. Callers: rwb-payment JOB-07 (RWB-P8-E2008-APP), RWB-P8-E4044-APP, RWB-P8-E4045-APP, RWB-P8-E4050-APP (date form); E1013 baseline measures and gateway-bff (account form). YAML `description` names both stories and the builder.

**Affected services.** rwb-source-data; rwb-payment; gateway-bff.
**Affected stories.** RWB-P1-E1013-APP, RWB-P1-E2008-APP, RWB-P1-E1015-CON, RWB-P8-E2008-APP, RWB-P8-E2008-CON, RWB-P8-E4044-APP, RWB-P8-E4045-APP, RWB-P8-E4050-APP, RWB-ITG-E2008-ITG.
**Affected documents.** `rwb-source-data.yaml` (parameter, oneOf rule, description); Service Contract Catalog v3 (row of `getPayments`); Gap Register v3 (NEW-GAP-S10-14 closed).
**Escalation items settled.** 4. **GAP/ASM.** Closes NEW-GAP-S10-14; GAP-0601 unchanged.
**Status.** Proposed – Claude Opus 5.5 (applied). **Reuse note.** One path, one handler, one builder per resource: a second caller adds a query form to the owner's operation, never a second operation.
**Values chosen without a source.** Exactly-one rule; account-form ordering.

---

## RD-P1-062 · Never-stamped data product: what every reader shows and does; freshness fixtures

**Question (items 17, 22, 62 first part, 18).** RD-P1-041 makes a never-stamped product `businessDate` null and `status` STALE. Stories ask what the data-date header, stale banner, input age, `data_as_of`, MSG-P1-001 `{date}`, notice generation and "last complete day" do then; and fixtures in five stories use dates that do not match the RD-P1-041 expected business date.

**Sources.** Register RD-P1-041 final (never stamped = businessDate null, STALE; expected date = latest bank business day before T); RD-P1-010 final (`AceBatchNotComplete` with `lastCompleteBusinessDate` null when none); YAML `DataProductFreshness` (lines 2174-2206: "null only for a never-stamped product or while the Section B flag is off", `staleSince` "null when LOADED"); EMS v5 MSG-P1-001 "{product} is from {date}. Today's load has not arrived."; RWB-P6-E1052-APP X6 and X12 (STALE with a date: generation proceeds with that date shown); RWB-P3-E2011-APP BR12 (header omitted when the answer is absent); BSD v7 JOB-02 ("No cases from a stale business date").

**Precedence applied.** RD-P1-041 (register) fixes the answer; this decision only fixes reader behaviour and does not amend it.

**Ruling.**
1. **Answer.** `businessDate` null, `status` STALE, `staleSince` null, `sourceExtractedAt` and `loadedAt` absent.
2. **Gated reads refuse.** Every gated operation and activity (`listEligibleAccounts`, `GET /efs-history`, `/booking-facts`, `/payments`, `/accounts/{accountKey}/installment-facts`, DailyCompletenessGate) refuses with 409 MSG-P1-001 (activity: non-retryable `AceBatchNotComplete`, `lastCompleteBusinessDate` null).
3. **No date, fail closed.** A reader that needs a data date treats a never-stamped product as having none: the `X-Data-As-Of` header is omitted (as for an absent answer, E2011 BR12); the stale banner shows (status STALE); `data_as_of` on a decision record, notice or report row is null; an input age is not computed (null) and every age check that uses it fails as too old.
4. **Notices (items 22, 62).** A notice whose merged products include a never-stamped product is **held** (not generated), with MSG-P1-001, and is retried in the next window after AceDataReady (the RWB-P2-E1007-APP X1 mechanism). This is the fail-closed reading of point 3; the product owner confirms it under NEW-GAP-F13-5 (kept as a confirmation, not a build blocker). A STALE product that has a `businessDate` keeps the existing rule (proceed with the date shown).
5. **"Last complete day" (RWB-P9-E2009-APP).** The `businessDate` of the stamp in use; for a never-stamped product there is none: the data set excludes the product and shows no data date for it.
6. **MSG-P1-001 `{date}`.** EMS v5 has no wording for a product with no stamp: **Pending, owner Error and Message Standard owner (UX content lead)**, NEW-GAP-D2. Interim build: Problem `messageCode` MSG-P1-001 with `{product}` filled and `{date}` left empty; tests assert the code and the product only.
7. **Fixtures (item 18).** Every freshness fixture uses the RD-P1-041 expected date: for a test day T, the expected date D is the latest bank business day before T on the sandbox calendar. Each consumer fake serves three rows: LOADED for D; STALE with `businessDate` = the business day before D and `staleSince` = D; never stamped (`businessDate` null). RWB-P3-E2011-APP, RWB-P3-E2011-CON, RWB-P3-E2014-APP, RWB-P7-E2014-APP and RWB-P7-E2014-CON change their dates accordingly.

**Affected services.** All freshness readers: rwb-case, rwb-comms, rwb-decision, rwb-reporting, rwb-agent, rwb-access, gateway-bff.
**Affected stories.** RWB-P1-DM001-APP, RWB-P1-DM002-APP, RWB-P3-E2011-APP, RWB-P3-E2011-CON, RWB-P3-E2014-APP, RWB-P7-E2014-APP, RWB-P7-E2014-CON, RWB-P6-E1052-APP, RWB-P6-E1052-CON, RWB-P6-E1007-APP, RWB-P6-E1011-APP, RWB-P6-E1032-APP, RWB-P10-E1059-APP, RWB-P10-E1059-CON, RWB-P4-E8018-APP, RWB-P9-E2009-APP.
**Affected documents.** Error and Message Standard (next version: wording Pending, NEW-GAP-D2); Gap Register v3 (NEW-GAP-L03-1, NEW-GAP-L04-01, NEW-GAP-L04-02, NEW-GAP-L04-03, NEW-GAP-S12-1, NEW-GAP-F13-2 closed; NEW-GAP-F13-5 kept as confirmation; NEW-GAP-D2 new).
**Escalation items settled.** 17, 18, 22, 62 (first part).
**Status.** Proposed – Claude Opus 5.5 (applied). **Reuse note.** A product without a stamp is treated as having no data date: refuse gated reads, omit the date, fail age checks, hold dependent outbound work.
**Values chosen without a source.** Fail-closed reading; notice held; three-row fixture.

---

## RD-P1-063 · Contract operations reported missing: verified state and the remaining additions

**Question (items 25, 29, 34, 46, 47, 49, 51 gateway codes, 54).** Editors report operations missing from published contracts.

**Sources (verified).** YAML 5.1.0 `paths` (lines 295-1376) holds `GET /proof-of-delivery`, `GET /admin/reconciliation/results` and `/{resultId}`, `GET /booking-facts`, `GET /batch-status`, `GET /payments`, `GET /accounts/{accountKey}/installment-facts`, `PUT /extension-facts/parties/{personKey}`, `PUT /extension-facts/accounts/{accountKey}`; freshness query parameter is `product` (line 307). Staged `asyncapi/rwb-source-data.asyncapi.yaml` is 5.1.0 with key "sourceSystem:businessDate (no case)" (lines 10, 24, 159). Staged `asyncapi/rwb.decision-record.v1.asyncapi.yaml` names `rwb.decision.DecisionRecorded.v1` (lines 51, 98). Staged `rwb-case.yaml` 5.1.0 has `/admin/parameters` and no `/parameters/{key}`; register RD-P1-028 (P1 reads parameters only through RWB-P3-E1042-CON `GET /api/recovery/case/v1/parameters/{key}`); Parameter Catalog v1.csv header (14 columns). Staged `rwb-access.yaml` 5.1.0 has no `/authorise`; Service Contract Catalog v3 rows at lines 225, 609, 681 (`POST /authorise (role, scope, DoA), cached in rwb-case`, `/api/recovery/access/v1`, Arch v5 slides 13-14). Staged `rwb-partner.yaml` and `rwb-writeoff.yaml` path lists. Register RD-P1-010 (region_code belongs to rwb-case), RD-P1-001, RD-P1-004.

**Ruling.**
1. **Already published (items 25, 29, P1 half of 46, 34; DecisionRecorded check).** No story drops those operations; stories cite them by path and operationId from YAML 5.1.0. The asyncapi files already carry RD-P1-003 and RD-P1-008. Editors who saw them missing worked on an earlier copy.
2. **Freshness query name (item 46).** The query parameter is `product`; RWB-P1-E1015-CON v3 text that says `productCode` for the query is corrected. `productCode` stays the path parameter of the records read and the answer field.
3. **`rwb-case.yaml`: add `GET /parameters/{key}`** (operationId `getParameter`, owner P3, builder RWB-P3-E1042-CON, RD-P1-028). Answer: the catalog row (the 14 columns of `config/parameter-catalog.csv`) and the value in force from `parameter_value` with the column names RWB-P3-E1042-CON uses. Service workload identities only. A parameter with `secret` true answers 404 MSG-P4-003. 401, 403, 503 per RD-P1-004. This closes NEW-GAP-F11-8.
4. **`recon.tolerance.pct` `used_by` (item 46).** Not extended: only the P1 reconciliation uses it, because RD-P1-069 rule 6 removes the duplicate open-case check from RWB-P3-E1011-APP; rwb-case reads reconciliation results from `GET /admin/reconciliation/results`.
5. **`rwb-access.yaml`: add `POST /authorise`** (Service Contract Catalog v3 rows 225, 609, 681; owner P4, builder RWB-P4-E1016-APP). Request and answer fields are **Pending, owner rwb-access contract owner**, NEW-GAP-F09-3 kept. Interim build for the callers (RWB-P1-E1016-APP, -CON, -DB): they send `Idempotency-Key` (UUID per call; the platform filter RWB-PLT-N009 applies to every POST), they assert only allow or deny and the Problem `messageCode` (401 MSG-P4-001, 403 MSG-P4-002, 404 MSG-P4-003), never role or scope values the provider has not published, and they test against the P4 fake.
6. **Other contracts outside P1 (item 49).** Staff read of an instruction in `rwb-partner.yaml` and read of a write-off decision in `rwb-writeoff.yaml`: Pending, owners S9 and S7 contract owners (NEW-GAP-F07-02). Whether `identity_ref` holds a person key: Pending, owner data architect (NEW-GAP-F07-01).
7. **gateway-bff codes (item 51).** RD-P1-004 applies to gateway-bff: a downstream Problem is passed through unchanged (status, `messageCode`, `traceId`); the gateway's own errors use the same envelope; the code of the edge 500 stays Pending (NEW-GAP-F08-2, owner platform edge owner).
8. **Case region and branch (item 47).** `region_code` belongs to rwb-case (RD-P1-010). The source of `branch_code` on the case record is **Pending, owner rwb-case owner with the data architect**, NEW-GAP-F11-6 kept; interim: rwb-case stores the `branchCode` of `GET /accounts/{accountKey}` (RD-P1-060) when the account view carries one, else null.
9. **Service Contract Catalog section 6.1** is aligned to Service Catalog v2 (finishing-pass item).

**Affected services.** rwb-case, rwb-access, gateway-bff, rwb-partner, rwb-writeoff, rwb-source-data.
**Affected stories.** RWB-P1-E1015-CON, RWB-P3-E1042-CON, RWB-P3-E1011-APP, RWB-P4-E1016-APP, RWB-P1-E1016-APP, RWB-P1-E1016-CON, RWB-P1-E1016-DB, RWB-PLT-N001-CON, RWB-P1-E2007-APP, RWB-P1-E2008-APP, RWB-ITG-E2007-ITG, RWB-ITG-E2008-ITG, RWB-ITG-E1055-ITG, RWB-ITG-E1011-ITG.
**Affected documents.** `rwb-case.yaml` (`/parameters/{key}`), `rwb-access.yaml` (`/authorise`), `index.yaml` counts; Service Contract Catalog v3 (.md/.xlsx; section 6.1); Parameter Catalog v1.csv (no change to `used_by`); Gap Register v3 (NEW-GAP-F11-8 closed; NEW-GAP-F09-3, NEW-GAP-F07-01, NEW-GAP-F07-02, NEW-GAP-F08-2, NEW-GAP-F11-6 kept).
**Escalation items settled.** 25, 29, 34, 46, 47, 49, 51 (second part), 54; checks "DecisionRecorded event type" and "Service Contract Catalog 6.1".
**Status.** Proposed – Claude Opus 5.5 (applied). **Reuse note.** Before reporting an operation as missing, read the staged YAML `paths`; a caller of an unpublished shape asserts only the envelope and the code.
**Values chosen without a source.** operationId `getParameter`; secret parameter answers 404; interim `branchCode` source.

---

## RD-P1-064 · Interaction ledger callers: letter dispatch and delivery entries, hand-recorded proof, permissions and entry types

**Question (items 1, 26, 32, 37, 39, 40, 41, 50, 59 failed append, 60, 62 second part, 63; extra stories).** RD-P1-007 rule 7 sets `externalRef` = `pod_key`, but the dispatch entry carries the WIN barcode, so proof and letter never pair; `podKey` is 255 characters against `externalRef` 60 and `idempotencyKey` 120; the dispatch append needs `conductCheck`; no permission lets rwb-comms append; rwb-partner's route conflicts with ASM-5391; complaints, customer answers and notice entries have no settled form.

**Sources.** Register RD-P1-007 (rules 1-8 and final), RD-P1-009 (consumed map has no partner type), RD-P1-001. YAML `InteractionRequest` (lines 1986-2064: eventCode enum without COMPLAINT; `actorType` USER, SERVICE, PARTNER; `channel` enum incl. LETTER, PORTAL; `conductCheck` PASSED, BLOCKED, NOT_APPLICABLE; `externalRef` maxLength 60; LETTER rule "conductCheck is required when deliveryStatus is SENT or absent; externalRef is required when deliveryStatus is present"); `Interaction.latestDeliveryStatus` (derived per `externalRef`); `ProofOfDeliveryRow` (`podKey` 255, `noticeRef` 60, `barcode` 40, `callbackDate`, `deliveryStatus` 15). PS v9 `v_ace_pod` (lines 615-631). AR v3 ASM-5391. EMS v5 MSG-P1-022. RWB-P2-E1007-APP (INT-14 WIN notice file).

**Precedence applied.** RD-P1-007 stands; rule 7 is amended for the reference and key only, because the published schema lengths (YAML, same run) make `pod_key` unusable as `externalRef` and the derivation of `latestDeliveryStatus` needs the dispatch and delivery entries to share a reference. **Amends RD-P1-007 rule 7** and **changes ASM-5391**.

**Ruling.**
1. **Callers.** In-process: RWB-P1-E1067-APP, RWB-P1-E2034-APP (RD-P1-007 final). REST, each under its own workload identity: rwb-case, rwb-comms, rwb-integration, rwb-document, rwb-payment, rwb-treatment, rwb-partner.
2. **Permission (item 40).** Users Roles and Permissions v6 and Role to System Access Matrix v4 add, for each REST caller of rule 1 that lacks it, a service-identity row "Case record C on rwb-source-data" (the x-capability of `POST /cases/{caseId}/interactions`). rwb-comms is the first row (NEW-GAP-F10-01 closed).
3. **Dispatch entry (rwb-comms, when the WIN file is sent; items 1, 63).** `eventCode` LETTER, `channel` LETTER, `direction` OUTBOUND, `deliveryStatus` SENT, `externalRef` = the WIN `barcode` of the notice, `conductCheck` PASSED (a letter is dispatched only after the conduct check passed), `actorType` SERVICE, `actorRef` `rwb-comms`, `sourceRef` `INT-14 WIN`, `idempotencyKey` `LETTER-<caseNo>-<yyyyMMdd of sent date>-<noticeId>`. A letter refused by the conduct check appends `conductCheck` BLOCKED with no `deliveryStatus` and no `externalRef`.
4. **Delivery entry (rwb-comms, after `GET /proof-of-delivery`; amends rule 7).** One entry per matched row: `eventCode` LETTER, `deliveryStatus` from the row, `externalRef` = `barcode`, else `noticeRef` when `barcode` is null; a row with neither is not matched (no entry; rwb-comms logs the row as unmatched). `occurredAt` = `callbackDate` at 00:00 Asia/Bangkok. `idempotencyKey` `LETTER-<caseNo>-<yyyyMMdd of callbackDate>-<u>` where `<u>` is the UUID version 5 of `podKey` in the RFC 9562 URL namespace (36 characters, so the key stays within 120 and stays the same on every re-read). The mapping of WIN `delivery_status` values to SENT, DELIVERED, READ, FAILED is **Pending, owner rwb-comms owner with the WIN interface owner**, NEW-GAP-D3; interim: the values of the RWB-P6-E1055-APP fixture.
5. **Hand-recorded proof (items 37, 60).** Yes, it writes an entry, through rwb-comms only: `eventCode` LETTER, `actorType` USER, `actorRef` the user ID, `deliveryStatus` as recorded, `externalRef` = the notice's barcode, `idempotencyKey` `LETTER-<caseNo>-<yyyyMMdd>-<id of the rwb-comms record of the hand entry>`. `<caseNo>` is read from rwb-case `GET /cases/{caseId}` (one hop) – the case number source of item 60.
6. **Single appender of delivery entries (items 32, 39).** rwb-comms only (RD-P1-007 final). RWB-P1-E2021-APP and RWB-P3-E2021-APP write no delivery entry. `GET /proof-of-delivery` stays readable by the rwb-comms workload identity only; rwb-asset (RWB-S5-E3022-APP/CON) reads delivery state from `GET /cases/{caseId}/interactions` (`latestDeliveryStatus` of the LETTER entry) or from rwb-comms `GET /notices/{noticeId}`, and RWB-P1-E1055-APP keeps rwb-comms as its one caller.
7. **EFS history appender (item 26).** The P2 rwb-integration hand-over run (RD-P1-007 rule 8; RD-P1-067). RWB-P3-E2001-APP removes its append step.
8. **Promise rows (item 32).** PROMISE when the entry records a promise to pay (EFS `isPtp`, or a Workbench contact with `promiseAmount` and `promiseDate`); CONTACT otherwise.
9. **rwb-partner (item 50).** Appends partner results over REST: `eventCode` PARTNER_RESULT, `actorType` PARTNER, `actorRef` the partner code, business key per RD-P1-007 rule 4. ASM-5391 is changed from "through the published event" to this REST append (RD-P1-009 has no partner event in its map). NEW-GAP-F08-1 closed.
10. **Customer answers (item 60).** Appended by the receiving service: `eventCode` CONTACT, `direction` INBOUND, `channel` PORTAL for an answer given on HOME.SCB, `actorType` SERVICE, `actorRef` the receiving service (`rwb-comms`); on events `ce_actor` = `SERVICE:rwb-comms`. There is no customer actor type. That HOME.SCB maps to PORTAL is **Pending confirmation, owner product owner**, NEW-GAP-F16-1 (interim PORTAL).
11. **Notices on the timeline (item 62).** Postal notices are LETTER entries (rules 3-5); SMS and LINE messages are CONTACT entries with `channel` SMS or LINE, `direction` OUTBOUND and `deliveryStatus`. Repeats: same header key with another body → 409 MSG-PLT-N009-05; new header key with an existing business key → 200 with the existing entry (RD-P1-001, RD-P1-007 rule 4).
12. **Complaints (item 41).** No ledger eventCode identifies a complaint. **Pending, owner product owner with compliance**, NEW-GAP-F10-02 kept. Interim: RWB-P10-E1062 X1 checks run without a complaint signal from the ledger; the complaint condition is marked Pending in the story.
13. **Failed append (item 59).** On 503 MSG-P1-022 the caller does not commit its action, or retries with the same header key and business key; no caller keeps an action whose entry was not written.
14. **Extra stories.** RWB-P3-E2021-APP (drop the delivery write), RWB-P3-E2016-CON (cite RD-P1-007 instead of GAP-0716), RWB-P10-E1062-APP (ledger read through `GET /cases/{caseId}/interactions`, as its CON), RWB-P6-E2021-CON (proof of delivery is the P1 `GET /proof-of-delivery` read by rwb-comms, not an INT-15 result from rwb-integration, as RWB-P6-E2021-OPS).

**Affected services.** rwb-source-data, rwb-comms, rwb-integration, rwb-case, rwb-partner, rwb-asset, rwb-agent, rwb-access (permissions).
**Affected stories.** RWB-P1-E1055-APP, RWB-P1-E2021-APP, RWB-P1-E2034-APP, RWB-P1-E1066-APP, RWB-P6-E1055-APP, RWB-P6-E1055-CON, RWB-P6-E2021-APP, RWB-P6-E2021-CON, RWB-P6-E2021-OPS, RWB-P6-E1052-APP, RWB-P3-E2021-APP, RWB-P3-E2016-CON, RWB-P3-E2001-APP, RWB-P2-E2001-APP, RWB-ITG-E2021-ITG, RWB-ITG-E2034-ITG, RWB-ITG-E1055-ITG, RWB-S5-E3022-APP, RWB-S5-E3022-CON, RWB-S9 result stories (RWB-S9 stories cited under ASM-5391), RWB-P10-E1062-APP, RWB-P10-E1062-CON, RWB-ITG-E1062-ITG, RWB-P6-E4036-APP.
**Affected documents.** `rwb-source-data.yaml` (LETTER description: externalRef rule); Users Roles and Permissions v6 (.xlsx), Role to System Access Matrix v4 (.xlsx); Assumptions Register v3 (ASM-5391 changed); Gap Register v3 (NEW-GAP-S10-16, NEW-GAP-F06-1, NEW-GAP-F10-01, NEW-GAP-F08-1, NEW-GAP-F14-1, NEW-GAP-F14-2, NEW-GAP-F13-6, NEW-GAP-F13-7, NEW-GAP-F15-2, NEW-GAP-F16-2, NEW-GAP-F16-3, NEW-GAP-F16-4 closed; NEW-GAP-F10-02 and NEW-GAP-F16-1 kept; NEW-GAP-D3 new); register RD-P1-007 (amendment line).
**Escalation items settled.** 1, 26, 32, 37, 39, 40, 41, 50, 59 (second part), 60, 62 (second part), 63; extra stories RWB-P3-E2021-APP, RWB-P3-E2016-CON, RWB-P10-E1062-APP, RWB-P6-E2021-CON.
**Status.** Proposed – Claude Opus 5.5 (applied). **Reuse note.** Pair outbound and delivery entries on the external reference the channel returns (barcode for WIN); derive bounded business keys with UUID v5 of long source keys; customer-originated entries carry the receiving service as actor.
**Values chosen without a source.** `externalRef` barcode-then-noticeRef; UUID v5 URL namespace; `sourceRef` `INT-14 WIN`; dispatch `conductCheck` PASSED; HOME.SCB → PORTAL interim; actor of customer answers.

---

## RD-P1-065 · Job reads and reruns across services; readiness repeats

**Question (items 12, 24, 27, 31 rerun part, 48, 57 first part).**

**Sources.** Register RD-P1-012 final (rerun of a FAILED run only, ALLOW_DUPLICATE_FAILED_ONLY, 409 MSG-P1-011; other services' jobs served by their owners, gateway-bff composes; MIGRATION runs not served), RD-P1-040 final (readiness 202 idempotent; admin rerun only of FAILED runs), RD-P1-041 (no second AceDataReady for a stamped date), RD-P1-020 (`business_day_readiness`, business date unique). GR v3 GAP-3271 (per-service job reads, owner solution architect), GAP-0657 resolution ("serve the rerun on the integration base for the jobs of this service's catalogue"). BSD v7 Jobs rows JOB-03, JOB-06, JOB-14.

**Ruling.**
1. **One rerun standard (items 27, 31).** The RD-P1-012 rule is the platform standard for every service's job monitor: only a FAILED run is rerun (new run, same business date, reuse policy ALLOW_DUPLICATE_FAILED_ONLY); a COMPLETE or running run answers 409 with the owner's "already complete or running" code. TE008 of JOB-14 (rwb-decision) becomes the rerun of a FAILED chain check; a completed check is re-verified by the next 02:00 run. RWB-ITG-E2010-ITG and RWB-ITG-E4050-ITG drop "rerun of a completed run". An owner who needs another rule asks for a new RD decision.
2. **Job reads of other services (item 24).** GAP-3271 is widened to name rwb-case: the job read and rerun of DailyCaseRun (JOB-02 and its JOB-03 step) and of JOB-06 are served by rwb-case. Owner solution architect with the rwb-case owner. Interim: RWB-ITG-E1020-ITG and RWB-ITG-E1030-ITG assert outcomes through rwb-case's published reads (`/queues/{queueId}/cases`, `/cases/{caseId}`) and mark their rerun steps Pending.
3. **Readiness repeat (item 48).** `POST /business-days/{date}/ready` for a date that already has a `business_day_readiness` row answers 202 with the stored state; while AceIngestCheck runs it attaches (USE_EXISTING); once the row is DONE or LATE it starts nothing. A second ReconciliationWorkflow run of a date exists only through the rerun of a FAILED run. The ITG DM stories' assumption (no second reconciliation run) is confirmed; RWB-P1-E1011-APP and RWB-P1-E1013-APP state it.
4. **Booking confirmation retry (item 12).** No second AceDataReady is published for a stamped date. A RWB-P2-E2007-APP run that the gate refuses ends FAILED with MSG-P1-001 and is rerun from the rwb-integration job monitor (rule 1; GAP-0657); there is no wait-for-a-second-event path.
5. **RWB-PLT-E1044-CON (item 57).** Removes the migration-run record and the job-view fake (RD-P1-012: MIGRATION runs are not served).

**Affected services.** All services with jobs; rwb-case, rwb-decision, rwb-integration, rwb-source-data.
**Affected stories.** RWB-P1-E1011-APP, RWB-P1-E1013-APP, RWB-P1-AD018-APP, RWB-P2-E2007-APP, RWB-P2-E2007-CON, RWB-ITG-E2007-ITG, RWB-ITG-E1020-ITG, RWB-ITG-E1030-ITG, RWB-ITG-E2010-ITG, RWB-ITG-E4050-ITG, RWB-ITG-E1011-ITG, RWB-PLT-E1044-CON, the rwb-decision JOB-14 story that holds TE008, and the ITG DM stories (RWB-ITG-DM0nn-ITG) that test readiness repeats.
**Affected documents.** Gap Register v3 (GAP-3271 widened; NEW-GAP-F04-1, NEW-GAP-F05-2 (rerun part) closed); Test Cases (TE008 row); Batch and Scheduling Design v7 (Jobs notes: rerun standard).
**Escalation items settled.** 12, 24, 27, 31 (rerun part), 48, 57 (first part); extra story RWB-PLT-E1044-CON.
**Status.** Proposed – Claude Opus 5.5 (applied). **Reuse note.** Reruns are of failed runs only, in every service; a repeated readiness call never restarts closed work.
**Values chosen without a source.** None beyond the reuse of RD-P1-012.

---

## RD-P1-066 · Event subscriptions, start rules and job owners; ACE boundary of rwb-payment

**Question (items 5, 11 start, 13, 14, 15, 19, 20, 21, 30, 45, 53; ACE boundary of RWB-P8-E4044-APP/-CON and RWB-P8-E4045-APP).**

**Sources.** Run brief rule 6 (only rwb-source-data reads `recovery.v_ace_*`). RWB-P8-E4044-APP v3 lines 9, 48, 66, 74-75; RWB-P8-E4045-APP v3 lines 9, 50, 66, 77, 153; RWB-P8-E4047-APP line 337; YAML `/batch-status` (access rwb-integration only), `/payments`. Register RD-P1-003 (one consumer group per service per topic; KTEC v2 R13), RD-P1-040 (downstream daily work starts only on ALS/COMPLETED). BSD v7 Read me rows 19-20 (JOB-08 owner P8; JOB-02 event-started), Jobs rows JOB-02, JOB-08, JOB-15, JOB-20; Schedule and event map row JOB-15 (NEW-GAP-W5-003). GR v3 GAP-0657 (Accepted (directive): "Keep JOB-08 and its activities with rwb-integration … record the rwb-payment owner row of Architecture v5 slide 44 as superseded for this job"), GAP-0146 (DailyCaseRun: event-started; slide-14 Schedule a fallback not configured), GAP-3037. RWB-S7-E6023-APP lines 8, 28, 77, 89, 109. RWB-P2-E1007-APP lines 96, 378. Parameter Catalog v1 `caselist.allocation.wait.until` 07:15. PS v9 `data_product.expected_by` 08:00 for DP01.

**Precedence applied.** The ACE rule (D-RCV-60) overrides the P8 stories. For JOB-08 the GAP-0657 directive is a D-RCV-60 acceptance that explicitly supersedes the Arch v5 slide 44 owner row; it wins over RD-P1-040's consumer list and BSD v7. **Amends RD-P1-040 and RD-P1-003 (consumer list)**.

**Ruling.**
1. **ACE boundary.** RWB-P8-E4044-APP, RWB-P8-E4044-CON and RWB-P8-E4045-APP read no `recovery.v_ace_*` view. E4044 starts on AceDataReady (`sourceSystem` ALS, `status` COMPLETED) consumed from `rwb.source-data.events.v1` and reads the receipts with `GET /payments?businessDate=` (RD-P1-061); E4045 reads `GET /accounts/{accountKey}` (RD-P1-060) and `GET /payments`; either reads `GET /batch-status` when it needs the batch row. The YAML access line of `/batch-status` adds the rwb-payment workload identity. The "Open" lines of both stories are closed.
2. **Delivery of the events (items 20, 21).** AceDataReady and AceDataLate are delivered on the topic; "through the contract" means the asyncapi contract of rwb-source-data. rwb-payment has one consumer group, working ID `rwb-payment.rwb.source-data.events.v1`, with one listener that starts the JOB-07 run (RWB-P8-E2008-APP), E4044, E4047 and E4050 by signal-with-start on their own workflow IDs. Per-story groups are withdrawn. The same rule applies to every consumer service.
3. **JOB-08 owner (item 5).** rwb-integration (GAP-0657). BSD v7 Jobs and Schedule-map rows JOB-08 and Read me row 20 change owner to P2 rwb-integration; Kafka Topic and Event Catalog v3 adds consumer group `rwb-integration.rwb.source-data.events.v1` with READ ACL; rwb-payment keeps JOB-07. RD-P1-040 and RD-P1-003 consumer lists gain rwb-integration.
4. **Monthly GL write-off reconciliation (item 19).** No new event: the starter is AceDataReady with `sourceSystem` GL and `status` COMPLETED, consumed by rwb-writeoff's one group; the branch acts when `businessDate` is on or after the audit period's cut-off date. RD-P1-040's ALS-only rule governs daily jobs and is not breached by this monthly branch (clarification, not amendment). The posting-row read stays **Pending, owner P1 contract owner with the rwb-writeoff owner**, GAP-3037; interim the S7 stories build against a fake.
5. **Held-file release (item 13).** Confirmed: AceDataReady ALS/COMPLETED triggers the release; the held request re-reads freshness before building and stays held while its products are STALE.
6. **DailyCaseRun (item 14).** An event-started workflow started by rwb-case's AceDataReady (ALS, COMPLETED) consumer, not a Temporal Schedule; the slide-14 Schedule is a fallback not configured in the target (GAP-0146; BSD v7). RWB-PLT-NF07-INF is reworded.
7. **JOB-20 (item 15).** A Temporal Schedule in rwb-decision at 00:01 (BSD v7); AceDataReady does not start it. RWB-P7-E1020-APP preconditions are corrected.
8. **JOB-15 (item 30).** **Pending, owner solution architect with the rwb-reporting owner** (NEW-GAP-W5-003). Interim: the Airflow trigger `POST /reports/{id}/run` at 01:30 is the live entry (BSD v7 Jobs row JOB-15); the 01:30 Temporal Schedule is created paused. RWB-ITG-E2009-ITG and RWB-P9-E2009-APP follow.
9. **Lateness signals (item 45).** 07:15 is `caselist.allocation.wait.until`, the allocation wait limit, not a lateness alert. The staleness signal is STALE at `data_product.expected_by` (08:00 for DP01, RD-P1-041); AceDataLate goes out at 05:30. rwb-case derives no expected date: it reads `GET /data-products/freshness`.
10. **Case entry (item 11, start part).** JOB-02 starts on ALS alone (RD-P1-040); EFS completeness is handled in RD-P1-067.
11. **Retry and dead-letter topics (item 53).** Each consumer service gets WRITE and READ on the retry topics and WRITE on the `.dlt` topic of every topic it consumes (names per RWB-PLT-E1047-CON; RD-P1-009 non-blocking retry). Kafka Topic and Event Catalog v3 adds the ACL rows. Observability and Monitoring Design v6 adds catalog rows for AceIngestCheck (workflow metrics and alerts).

**Affected services.** rwb-payment, rwb-integration, rwb-writeoff, rwb-case, rwb-decision, rwb-reporting, rwb-deviation, gateway-bff, rwb-source-data.
**Affected stories.** RWB-P8-E4044-APP, RWB-P8-E4044-CON, RWB-P8-E4045-APP, RWB-P8-E4047-APP, RWB-P8-E4050-APP, RWB-P8-E2008-APP, RWB-P8-E2008-OPS, RWB-P2-E2007-APP, RWB-P2-E2007-OPS, RWB-P7-E2007-APP, RWB-S7-E6023-APP, RWB-S7-E6023-CON, RWB-P2-E1007-APP, RWB-PLT-NF07-INF, RWB-P7-E1020-APP, RWB-P9-E2009-APP, RWB-ITG-E2009-ITG, RWB-P3-E1011-APP, RWB-P3-E2001-APP, RWB-PLT-E1047-CON.
**Affected documents.** `rwb-source-data.yaml` (`/batch-status` access); Batch and Scheduling Design v7 (.xlsx; v6 .docx twin) JOB-08 owner, JOB-15 interim; Kafka Topic and Event Catalog v3 (consumer groups, retry/DLT ACLs); Event and Messaging Design v7; Temporal Workflow and Activity Catalog v3 (JOB-08 worker queue rwb-integration); Observability and Monitoring Design v6; Microservice Ownership Map v3 (JOB-08); Gap Register v3 (GAP-0146 resolved; NEW-GAP-F08-5, NEW-GAP-F08-10, NEW-GAP-F11-2 closed; GAP-3037, NEW-GAP-W5-003 kept); register RD-P1-040 and RD-P1-003 (amendment lines).
**Escalation items settled.** 5, 11 (start), 13, 14, 15, 19, 20, 21, 30, 45, 53; ACE boundary E4044/E4045.
**Status.** Proposed – Claude Opus 5.5 (applied). **Reuse note.** One group per service per topic, one listener fanning out; non-daily consumers may filter AceDataReady on another source; no service but rwb-source-data reads an ACE view.
**Values chosen without a source.** Group working IDs (pattern of RD-P1-003); JOB-15 Schedule paused interim; GL cut-off rule.

---

## RD-P1-067 · EFS history: gate products, late EFS batch and the single appender

**Question (items 2, 11, 26).** RD-P1-010 final names DP01 as the gate of rule 8 (`GET /efs-history`), so a stale EFS (DP05) load no longer refuses and history can be partial; case entry starts on ALS alone while EFS may arrive late; the appender differs between RD-P1-007 rule 8 and staged RWB-P3-E2001-APP.

**Sources.** Register RD-P1-010 final; RD-P1-041 item 8 (gate source set = every source mapped to a DAILY product read by JOB-02, JOB-04, JOB-07 or JOB-08); BSD v7 JOB-02 ("Creates cases …; attaches history"); PS v9 seed DP05 DAILY 08:00 (EFS); YAML `/efs-history` description ("The DP01 and DP05 freshness gate must pass"); RD-P1-007 rule 8; Parameter Catalog v1 (no `handover.hold_until` row); RD-P1-040 (poll every 5 minutes).

**Precedence applied.** Within the register, RD-P1-041 item 8 already puts EFS in the gate set because JOB-02 reads DP05; this decision reconciles RD-P1-010 with it (clarification of RD-P1-010 rule 8, recorded as an amendment line).

**Ruling.**
1. **Gate (item 2).** `GET /efs-history` refuses with 409 MSG-P1-001 unless DP01 and DP05 are both complete for the business date (YAML text kept). `listEligibleAccounts` keeps the DP01 gate.
2. **Late EFS (item 11).** Case creation proceeds on ALS. The P2 hand-over run, on 409 MSG-P1-001 from `/efs-history`, waits on a durable timer and retries every 5 minutes until DP05 is stamped for the date or until `handover.hold_until`; at that limit it hands over without history and the rows are appended when DP05 arrives (the `EFS:<efsRecordKey>` business key makes the late append idempotent). The key `handover.hold_until` is not in Parameter Catalog v1: **Pending, owner rwb-integration owner with RW-COE**, NEW-GAP-D4; interim default 09:00 as in RWB-P3-E2001-APP. No separate completeness check is built.
3. **Appender (item 26).** The P2 rwb-integration hand-over run only (RD-P1-007 rule 8). RWB-P3-E2001-APP removes the append and keeps the case-side hand-over state.

**Affected stories.** RWB-P1-E2001-APP, RWB-P2-E2001-APP, RWB-P2-E2001-CON, RWB-P2-E2001-OPS, RWB-P3-E2001-APP, RWB-ITG-E2001-ITG.
**Affected documents.** Parameter Catalog v1.csv (row Pending, NEW-GAP-D4); Gap Register v3 (NEW-GAP-L03-2 closed; NEW-GAP-D4 new); register RD-P1-010 (amendment line).
**Escalation items settled.** 2, 11, 26.
**Status.** Proposed – Claude Opus 5.5 (applied). **Reuse note.** A read is gated on every product it serves; a late secondary product delays only the step that needs it, bounded by a parameter, and is caught up idempotently.
**Values chosen without a source.** Hand over without history at the limit; 5-minute retry.

---

## RD-P1-068 · Migration packages: decision chain, act-time snapshot fields, DM002, DM007 key, orphan checks, DP04, loader identity, local decision record table

**Question (items 6, 7, 8, 9, 35, 36, 52, 57 second part).**

**Sources.** Staged `asyncapi/rwb.decision-record.v1.asyncapi.yaml` (ingest-rule line 31: "chain_seq and prev_hash assigned by rwb-decision under the chain lock"; payload lines 96-113: no rule, version, model or hash fields). RWB-P1-DM012-APP v3 lines 42-60. Register RD-P1-027 (allow-list: carry only Workbench system-of-record fields plus linking ACE business keys; DM007 carries DF-LEG-001..004 and DF-LEG-014), RD-P1-020 ("no P1 table" for decision records), RD-P1-021 (contact_point_ext cutover writer RWB-P1-DM005-APP), RD-P1-022 (REC-05 scope). LDM v10 DF-DEC-006 `model_version` (COLLINS; "Read at decision time"), DF-FIN-006 `amount` and DF-FIN-007 `received_date` (core bank via COLLINS), DF-LEG-005 `lawsuit_no` (LIT; DF-ACE-233 `v_ace_lawsuit.lawsuit_no`). GR v3 GAP-2533 (Accepted (directive): "keep the recorded legacy amount and received date with their provenance and copy no ACE row"). DMA v4 lines 132, 173 (RWB-DM-002: "Nothing: out of scope"). PS v9 seed DP04 ON_CHANGE, "ACE (ingested from the core bank) for the plan". Arch v5 line 1477 ("DB Own schema: business tables + outbox + inbox + decision_record") and line 1495. PS v9: no schema file holds a `decision_record` table.

**Precedence applied.** GAP-2533 (D-RCV-60 directive) and Arch v5 line 1477 outrank RD-P1-027 and RD-P1-020. **Amends RD-P1-027** (act-time snapshot class; DM007 key; DM002 clause) and **RD-P1-020** (decision_record table).

**Ruling.**
1. **Decision chain (item 6).** rwb-decision owns `chain_seq` and `prev_hash`; RWB-P1-DM012-APP sets no chain field and drops "the first record written in this service after cutover takes the entry_hash of the last migrated entry". Carrying the legacy `prev_hash`/`entry_hash`, rule ID and rule version on DecisionRecorded is **Pending, owner rwb-decision contract owner with compliance**, NEW-GAP-S13-4 kept (blocks the publish step only). Interim: DM012 builds the extract and the local decision records; publication of migrated entries stays behind the DM012 feature switch (off) until the schema carries the fields; the cutover evidence file lists every legacy `entry_hash` and the last legacy hash.
2. **Act-time snapshot fields (item 7).** A field that records a value as it was at a past act, which ACE cannot answer later, is CARRY with reason "value at act time": DF-DEC-006 `model_version` (DM012) and DF-FIN-006 `amount`, DF-FIN-007 `received_date` of the legacy proceeds (DM013, GAP-2533), each with `migration_source` and `migrated_at`. Source to Target Mapping v7 sheet Migration packages rows change from ACE_READ to CARRY with that reason.
3. **DM002 (item 8).** Migrates nothing (DMA v4). RWB-P1-DM002-APP is a verification story that reads `GET /customers/{personKey}` (RD-P1-060) and writes no row; the RD-P1-027 clause "DM002 contact_point_ext has zero or one row per contact_key …" belongs to RWB-P1-DM005-APP.
4. **DM007 key (item 9).** DF-LEG-005 `lawsuit_no` is KEY (the linking ACE business key to `v_ace_lawsuit`); DF-LEG-006 to DF-LEG-013 stay EXCLUDE (ACE_READ).
5. **Orphans (item 35).** REC-05 scope is unchanged. The `plan_ref` (DM004) and `asset_key` (DM006) orphan checks are each DM story's own cutover check, counted in its evidence; they read the keys through rwb-source-data (`GET /accounts/{accountKey}`, `GET /collateral/{assetKey}`).
6. **DP04 (item 36).** DP04 is ON_CHANGE (seed). Its plan part has a mapped source (the core bank, RD-P1-021 `data_product_source`): a stamp row is written when that source completes, it is never set STALE by time and DP04 is not in the DAILY gate set. RWB-P1-DM004-APP corrects "no ACE source".
7. **Loader identity (item 57).** With SY-DATALOAD retired, each package is loaded by its target service under that service's workload identity and migration owner (RD-P1-021: one owner per table).
8. **Local decision record table (item 52).** `rwb_source_data` has the local `decision_record` table that every service owns (Arch v5 line 1477), created by the shared library migration of RWB-PLT-E1027-CON; DM012 and the sandbox write through it. Its DDL is in no schema file of PS v9: **Pending, owner platform lead (library owner)**, NEW-GAP-F08-7 kept; interim the library's own migration runs in the Testcontainers build. `ce_idempotencykey` = the RD-P1-007 rule 4 business key (RD-P1-009); NEW-GAP-F08-6 closed.

**Affected stories.** RWB-P1-DM002-APP, RWB-P1-DM004-APP, RWB-P1-DM005-APP, RWB-P1-DM006-APP, RWB-P1-DM007-APP, RWB-P1-DM012-APP, RWB-P1-DM013-APP, RWB-P1-E1065-APP, RWB-PLT-E1027-CON, the ITG DM stories of DM004, DM006, DM007, DM012, DM013.
**Affected documents.** Source to Target Mapping v7 (.xlsx, sheet Migration packages); Data Migration Approach v5 (.docx); Physical Schema v9 README (decision_record Pending note); Microservice Ownership Map v3 (DM002 row); Gap Register v3 (NEW-GAP-S12-2, NEW-GAP-S12-6, NEW-GAP-F06-4, NEW-GAP-F06-6, NEW-GAP-F08-6 closed; NEW-GAP-S13-4, NEW-GAP-F08-7 kept); register RD-P1-027 and RD-P1-020 (amendment lines).
**Escalation items settled.** 6, 7, 8, 9, 35, 36, 52, 57 (second part).
**Status.** Proposed – Claude Opus 5.5 (applied). **Reuse note.** Carry a value ACE cannot answer later; never carry a value ACE answers; one chain owner; every service has its local decision record table.
**Values chosen without a source.** "Act-time snapshot" class name and reason text; DM012 publish switch interim.

---

## RD-P1-069 · Reconciliation breaks, orphan keys, REC-04/REC-06 and date-wide reads

**Question (items 31 break list, 33, 38 held proof rows and REC-09, 42, 43, 44).**

**Sources.** YAML `/admin/reconciliation/results/{resultId}` (break detail store and locator Pending, GAP-1508, NEW-GAP-S2B-03), `/proof-of-delivery` (paging GAP-0577), `BatchStatusAnswer` (no checksum); PS v9 `v_ace_batch_status.checksum` varchar(64). Register RD-P1-012 (P1 checks REC-01, REC-02, REC-05), RD-P1-022 (REC-05 owner P1; key-list read GAP-3273). RWB-P8-E4050-APP lines 64-66, 88 (REC-04 is part of the rwb-payment daily reconciliation).

**Ruling.**
1. **Break and orphan detail (items 31, 43).** Store and read stay **Pending, owner P1 data architect with the P1 contract owner** (GAP-1508, NEW-GAP-S2B-03). Interim: result reads answer aggregates; RWB-P1-AD019-APP, RWB-ITG-E2010-ITG, RWB-ITG-E4050-ITG and the P3 console assert counts.
2. **REC-04 and REC-06 (item 33).** Computed by rwb-payment's daily reconciliation (RWB-P8-E4050-APP) into `rwb_payment`; P1 computes REC-01, REC-02 and REC-05 only. `BatchStatusAnswer` adds `checksum` (string, maxLength 64, nullable; `v_ace_batch_status.checksum`) for E4050.
3. **Held proof rows and REC-09 (item 38).** No published read in P1 v1; Pending under GAP-0577 and GAP-1508.
4. **Date-wide DP06 (item 42).** **Pending, owner P1 contract owner with the rwb-asset owner**, NEW-GAP-F10-03 kept. Interim (not blocking): the S5 reconciliation reads each asset of its own list through `GET /collateral/{assetKey}` (RD-P1-060).
5. **Open-case key check (item 44).** One owner: P1 REC-05 (RD-P1-022). RWB-P3-E1011-APP drops its own check and serves only the key-list read (GAP-3273).

**Affected stories.** RWB-P1-E1011-APP, RWB-P1-E1011-CON, RWB-P1-AD019-APP, RWB-P1-E2010-APP, RWB-P3-E1011-APP, RWB-S5-E1011-APP, RWB-P8-E4050-APP, RWB-ITG-E2010-ITG, RWB-ITG-E4050-ITG, RWB-ITG-E1011-ITG.
**Affected documents.** `rwb-source-data.yaml` (`BatchStatusAnswer.checksum`); Data Quality and Reconciliation Rules v5 (owner of REC-04, REC-06); Gap Register v3 (NEW-GAP-F11-4 closed; GAP-1508, NEW-GAP-S2B-03, NEW-GAP-F10-03, GAP-0577 kept).
**Escalation items settled.** 31 (break list), 33, 38 (proof rows, REC-09), 42, 43, 44.
**Status.** Proposed – Claude Opus 5.5 (applied). **Reuse note.** One owner per reconciliation check; consumers of break detail build on counts until GAP-1508 closes.
**Values chosen without a source.** None (checksum from the view).

---

## RD-P1-070 · Count-once store for failed contacts

**Question (item 3).** `POST /contact-points/{contactPointKey}/failed-contacts` must raise `failed_count` once per contact point and reference, but no store of counted references exists (NEW-GAP-S10-17).

**Sources.** YAML lines 1241-1282; PS v9 `processed_event` (consumer varchar(60), idempotency_key varchar(120), event_id uuid nullable, hit_count, uk_processed_event (consumer, idempotency_key)); register RD-P1-001 (R-UNI-40: "work key with event_id null for in-process keys").

**Ruling.** The counted references are rows of `rwb_source_data.processed_event` with `consumer` `rwb-source-data.failed-contacts`, `idempotency_key` `FC:` followed by the lowercase hex SHA-256 of `<contactPointKey>|<reference>` (67 characters), `event_id` null. The row and the `failed_count` increase are written in one transaction. A repeat finds the row: `hit_count` + 1, `failed_count` unchanged, answer 201 with `counted` false. No new table.

**Affected stories.** RWB-P1-E2022-APP, RWB-P6 SMS/LINE caller stories, RWB-ITG-E2022 stories. **Affected documents.** `rwb-source-data.yaml` (description: Pending removed); Gap Register v3 (NEW-GAP-S10-17 closed).
**Escalation items settled.** 3. **Status.** Proposed – Claude Opus 5.5 (applied). **Reuse note.** In-process count-once keys use `processed_event` with a hashed key when the natural key can exceed 120 characters.
**Values chosen without a source.** Consumer name; `FC:` prefix and hash form.

---

## RD-P1-071 · Data dictionary gate and new fields

**Question (item 55).** RWB-P4-E1064-APP refuses loads naming unknown fields, while RD-P1-025 adds fields only through a load – a deadlock.

**Sources.** EMS v5 MSG-P1-005 ("A rule version names a field not in the data dictionary"); register RD-P1-025 (later fields carry `sys_field_version` rows).

**Ruling.** The unknown-field check (MSG-P1-005) applies to rule versions, mappings and access loads that name fields. A data dictionary load is how a field becomes known: it validates its own rows (field code unique, entity present in `sys_objects`, type valid) and writes `sys_fields` and `sys_field_version` rows. When one release brings both, the dictionary load is applied first. RWB-P4-E1064-APP and RWB-P1-E1064-APP state the scope.

**Affected stories.** RWB-P4-E1064-APP, RWB-P1-E1064-APP, RWB-P1-E1064-CON, RWB-P1-E1064-OPS. **Affected documents.** Gap Register v3 (NEW-GAP-F09-5 closed).
**Escalation items settled.** 55. **Status.** Proposed – Claude Opus 5.5 (applied). **Reuse note.** Gates that check names against a catalog never apply to the load that maintains the catalog.
**Values chosen without a source.** Order dictionary first.

---

## RD-P1-072 · Decision records versus reads in the ledger intake; personal data seen by agents

**Question (items 56, 38 call notes).** RD-P1-009 row 06 turns every DecisionRecorded with a `caseId` into a DECISION_TAKEN entry; if reads were recorded as decisions, each case-record read would add a timeline entry. A screening agent may read unmasked call-note text.

**Sources.** Register RD-P1-009 row 06; DP-03 (decision records for decisions); YAML records read ("every read is written to the access log"); YAML `Interaction.summary` ("Masked unless the caller's role may see it").

**Ruling.**
1. A read is not a decision. Reads (case record, data product, customer, authorise checks) are written to the access log only and publish no DecisionRecorded. Only decisions under DP-03 (for example a delegation-of-authority approval) are decision records, and those with a `caseId` correctly become DECISION_TAKEN entries. Stories that record a read as a decision are corrected; RD-P1-009 is unchanged.
2. The screening agent reads `summary` masked; an unmasking rule for an agent identity is **Pending, owner data protection officer**, NEW-GAP-F03-2 kept; interim masked.

**Affected stories.** RWB-P4-E1016-APP, RWB-P1-E1016-APP, RWB-P1-E1067-APP, RWB-P10-E1062-APP, RWB-P10-E1062-CON, RWB-ITG-E1062-ITG. **Affected documents.** Gap Register v3 (NEW-GAP-F09-4 closed; NEW-GAP-F03-2 kept).
**Escalation items settled.** 38 (call notes), 56. **Status.** Proposed – Claude Opus 5.5 (applied). **Reuse note.** Access is logged, decisions are recorded; never both for a read.
**Values chosen without a source.** None.

---

## RD-P1-073 · Test isolation for append-only rows and the shared sandbox

**Question (items 28, 38 sandbox).** The ITG harness wants to reset append-only ledger rows (NEW-GAP-F04-2, W1J01); a failed sandbox build and the seeding of other schemas are unclear (NEW-GAP-F03-4, NEW-GAP-F03-5).

**Sources.** Register RD-P1-007 rule 1 (append only; no update or delete), RD-P1-046 (sandbox `rwb_sandbox`, shared), RD-P1-021 (role and permission seeding to RWB-P4-E1065-APP, AC12 to RWB-P3-E1065-APP).

**Ruling.**
1. No environment deletes or resets ledger rows. The ITG harness isolates by run: every test creates its own cases and uses a fresh UUID per run as `<actionId>` in business keys; assertions filter by `caseId`. The only reset is the rebuild of the sandbox from DDL between suites (RD-P1-046).
2. A failed sandbox build leaves the previous sandbox in place and fails the pipeline; each schema is seeded by its owner's E1065 story (RD-P1-021).

**Affected stories.** RWB-ITG-E2034-ITG, RWB-ITG-E1065-ITG, RWB-ITG-W1 journey stories using W1J01, RWB-P1-E1065-APP, RWB-P1-E1065-CON, RWB-P1-E1065-DB, RWB-P3-E1065-APP, RWB-P4-E1065-APP, RWB-S8-E1065-APP. **Affected documents.** Gap Register v3 (NEW-GAP-F04-2, NEW-GAP-F03-4, NEW-GAP-F03-5 closed).
**Escalation items settled.** 28, 38 (sandbox). **Status.** Proposed – Claude Opus 5.5 (applied). **Reuse note.** Isolate tests by data, never by deleting append-only rows.
**Values chosen without a source.** Keep-old-sandbox rule.

---

## RD-P1-074 · Build-chain depth and the E1066-OPS / E1067-APP cycle

**Question (item 58).** Seven rwb-source-data stories sit in build chains up to 6 deep against a limit of 4; E1066-OPS and E1067-APP depend on each other.

**Ruling.**
1. The cut of the deep chains is **Pending, owner solution architect**, NEW-GAP-D5; interim the Story Build Order v5 and Dependency Map v7 keep the chains, flagged, and the stories are READY WITH MINOR GAPS.
2. The cycle is broken: RWB-P1-E1067-APP depends on RWB-P1-E1066-APP (the writer) only; RWB-P1-E1066-OPS depends on RWB-P1-E1066-APP and not on RWB-P1-E1067-APP; the intake's deployment step is a later step with no build dependency back.
3. The W9 graph (`SET\_work\p1-ready\qa\w9-governance\graph.py`, then `apply.py` and `fix_bo.py`) is re-run after story editing ends.

**Affected stories.** RWB-P1-E1066-OPS, RWB-P1-E1067-APP, RWB-P1-E1067-CON and the seven chain stories named by W9. **Affected documents.** Story Build Order v5 (.docx), Dependency Map v7 (.xlsx); Gap Register v3 (NEW-GAP-D5).
**Escalation items settled.** 58; finishing-pass step "re-run W9". **Status.** Proposed – Claude Opus 5.5 (applied). **Reuse note.** OPS stories depend on their APP stories, never the reverse.
**Values chosen without a source.** Direction of the cycle cut.

---

## Verdicts on "Extra stories to edit"

| Entry | Verdict |
|---|---|
| RWB-PLT-E1044-CON | Agree: remove the migration-run record and the job-view fake (RD-P1-065 rule 5, RD-P1-012). |
| RWB-P3-E2021-APP | Agree: it writes no delivery entry; rwb-comms is the one appender (RD-P1-064 rule 6). |
| RWB-P3-E2016-CON | Agree: replace the GAP-0716 citation with RD-P1-007 (and RD-P1-064). |
| RWB-P10-E1062-APP | Agree: same ledger-read alignment as its CON (`GET /cases/{caseId}/interactions`); complaint signal Pending (RD-P1-064 rule 12). |
| rwb-deviation (S8) stories taking deceased/bankrupt flags off AceDataReady | Agree: the one such story in Story Files v2 is RWB-S8-E1020-APP; flags come from `GET /customers/{personKey}` (RD-P1-060 rule 5). |
| RWB-P6-E2021-CON | Agree: proof of delivery is the P1 read used by rwb-comms, not an INT-15 result from rwb-integration (RD-P1-064 rule 14). |
| RWB-P6-E4036-CON | Agree: match E4036-APP; customer facts through `GET /customers/{personKey}` masked (RD-P1-060). |
| RWB-P8-E4044-APP, -CON, RWB-P8-E4045-APP (full review) | Agree: ACE boundary fix per RD-P1-066 rule 1. |
| RWB-P3-E2006-APP (full review) | Agree: reads `GET /data-products/freshness?product=`, `GET /accounts/{accountKey}`, `GET /collateral/{assetKey}` (RD-P1-060, RD-P1-063 rule 2). |
| S2 shallow edits (E1011 APP/CON/OPS, E1013 APP) re-run as S2b | Agree (process step; apply RD-P1-061 and RD-P1-065 in the re-run). |

## Verdicts on the check lists

| Check | Verdict |
|---|---|
| Wrong GAP numbers in AD018-APP v3 and AD019-APP v3 (GAP-3280, -3272, -3276, -3275) | Agree to check; verified now: no GAP-327x or GAP-328x citation remains in staged AD018-APP, AD019-APP, E1001-APP, E2010-APP or E1017-CON (AD018-APP line 10 records the replacement). Keep in the finishing pass for other v3 stories. |
| E1065 APP/CON/DB must not rename the sandbox database | Agree; verified: the three staged stories use `rwb_sandbox` (RD-P1-046). No edit needed. |
| E1066-APP AC15 missing key → MSG-PLT-N009-03 | Agree; verified: X8 row and AC15 cite MSG-PLT-N009-03 and -05. No edit needed. |
| Decision-record asyncapi carries `rwb.decision.DecisionRecorded.v1` | Agree; verified (lines 51, 98). Done. |
| GAP-3283 cited by E1001-APP and E2010-APP | Agree; verified: no staged story cites GAP-3283 now. The E1001 subject (NEW-GAP-F12-1) still needs a register row from the orchestrator. |
| E1066-APP event code outside the list → MSG-GEN-007 | Agree; verified: line 219 answers 422 MSG-GEN-007. No edit needed. |
| E1017-CON cites GAP-3271 for holdReport | Agree; verified: the staged E1017-CON no longer cites GAP-3271. The holdReport point belongs to RD-P1-047. |
| Staged source-data AsyncAPI still 5.0.0 with key caseId (item 34) | Disagree with the premise: staged file is 5.1.0 with key `{sourceSystem}:{businessDate}` (RD-P1-063 rule 1). |
| Re-run W9 graph after story editing | Agree (RD-P1-074 rule 3). |
| Service Contract Catalog section 6.1 to match Service Catalog v2 | Agree (RD-P1-063 rule 9). |

## Register amendments to add (for the orchestrator)

- RD-P1-003: consumer list adds rwb-integration (JOB-08) – RD-P1-066 rule 3.
- RD-P1-007 rule 7: `externalRef` = barcode (else noticeRef), key `LETTER-<caseNo>-<yyyyMMdd>-<uuid5(podKey)>` – RD-P1-064 rule 4.
- RD-P1-010 rule 8: `/efs-history` gate is DP01 and DP05 – RD-P1-067 rule 1.
- RD-P1-020: `rwb_source_data` has the library `decision_record` table – RD-P1-068 rule 8.
- RD-P1-027: act-time snapshot CARRY class; DF-LEG-005 KEY; DM002 clause moves to DM005 – RD-P1-068 rules 2-4.
- RD-P1-040: JOB-08 is rwb-integration's – RD-P1-066 rule 3.

## New gap rows (temporary IDs, next free GAP numbers after GAP-3282)

| Temp ID | Subject | Owner | Decision |
|---|---|---|---|
| NEW-GAP-D1 | Masking rule rows unmasking `firstName`, `lastName`, `contactValue` (ADDRESS) for the rwb-comms notice and rwb-integration outbound-file workload identities | Data protection officer with the rwb-access owner | RD-P1-060 |
| NEW-GAP-D2 | MSG-P1-001 wording for a product never stamped | Error and Message Standard owner | RD-P1-062 |
| NEW-GAP-D3 | Mapping of WIN `delivery_status` to SENT, DELIVERED, READ, FAILED | rwb-comms owner with the WIN interface owner | RD-P1-064 |
| NEW-GAP-D4 | Parameter `handover.hold_until` (catalog row, value) | rwb-integration owner with RW-COE | RD-P1-067 |
| NEW-GAP-D5 | Cut of build chains deeper than 4 | Solution architect | RD-P1-074 |

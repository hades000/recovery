# RWB-P4-E2019-APP Partner identities through the external gateway

SCB Collections and Recovery. Henka Group, 22 November 2026.
(C) Siam Commercial Bank and Henka Pte Ltd

**Change log.** D-RCV-60, 22 November 2026: split from RWB-E2-019 for rwb-access — the app slice that resolves a partner identity presented through the external gateway to Recovery roles, a PLACED scope, the matrix and masking versions in force and an expiry, holding no partner table and no token. Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

| Item | Value |
|---|---|
| Story key | RWB-P4-E2019-APP |
| Work type | APP (App development) |
| Suggested owner | TechX (suggested; any team may pick up this story) |
| Service | rwb-access |
| Service epic | RWB-SVC-P4 |
| Wave | 2 |
| Business epic | EP02 |
| Release | 31 December 2026 (tentative) |
| Legacy key | RWB-E2-019 |
| Legacy disposition | Split (rework) |
| Build status | Not started |
| Patterns applied | DP01, DP03, DP05, DP06, DP07, DP08, DP11, DP13, DP15, DP19 |
| Parallel lane | L-P4-A |
| Ready to start | After RWB-P4-E1022-APP, RWB-P4-E1039-APP |
| Depends on (build) | RWB-P4-E2019-CON, RWB-PLT-E1027-CON, RWB-PLT-E1042-CON, RWB-PLT-E1043-CON, RWB-PLT-E1037-CON, RWB-P4-E1037-CON, RWB-PLT-E1044-CON, RWB-PLT-N001-CON, RWB-P4-E1022-APP, RWB-P4-E1039-APP |
| Contract dependencies | RWB-P3-E1042-CON, RWB-P3-E1043-CON |
| Integration dependencies | None |
| External dependencies | RWB-P4-E2019-INF |
| PRD reference | 03 Requirements and specifications/PRD/Recovery Workbench PRD P4 rwb-access v1.md (FR-P4-034) |
| Status | Draft (realignment v1) |

### 1. Story

As a **partner and agency manager (RW-AGENCYMG)** and the **rwb-access service**, I want **a partner identity that the external gateway has already authenticated to be resolved to the Recovery roles of one partner role, a PLACED scope carrying the partner id, the matrix version and the masking policy version in force and an expiry, from the claims the gateway supplies and from rwb-access's own `role`, `permission` and `masking_rule` rows**, so that **a law firm, valuer or agency works inside the same role matrix, the same masking and the same access log as a bank user, a bank identity can never use the partner route, and a firm that leaves the panel loses access on the day it leaves**.

This is the rwb-access slice of legacy key RWB-E2-019 under epic RWB-SVC-P4, and it is the identity-resolution slice of that legacy key. The legacy story made one process hold the partner user, the firm and the partner role in a single schema and read the firm's panel status from a published interface of the same module. D-RCV-60 keeps the behaviour and separates the ownership:

- **This story, rwb-access (P4), schema `rwb_access`:** the resolution of a partner identity to the internal role model — the partner role rows of `role` with class `PARTNER_USER`, their `permission` letters in the `PARTNER_PORTAL` capability area, the `role_conflict` pairs, the default scope, the `masking_rule` version and the matrix version in force — answered on the operation `POST /api/recovery/access/v1/partner-identities/resolve` that RWB-P4-E2019-CON fixes, and the PLACED scope descriptor (scope type `PLACED`, the partner id, the instruction types of the role) that the owner of the instruction applies in its own query.
- **Not this story, rwb-partner (S9):** `partner`, `partner_user` and `partner_instruction` (Ownership Map ruling ASM-0072). The firm, its panel status and contract end, the binding of a partner identity to a firm and a role, the instructions, the accept and decline, the results, the fees and the partner portal operations are RWB-S9-E2019-APP's. This story **reads no S9 table**: the partner id, the partner role code and the firm state arrive in the claims of the caller, so the resolution reads its own role model and no S9 table (ASM-1431).
- **Not this story, rwb-decision (P7):** `decision_log_entry` and `approval`. The central ledger and the `GET /decision-log` read are P7's, and the ledger copy of a partner sign-in or refusal is RWB-P7-E2019-APP's.
- **Not this story, rwb-case (P3):** `lov_value` and the reference-data and parameter contracts. `LOV-ROLE-CLASS`, `LOV-CAPABILITY` and `LOV-SCOPE` are read through the reference-data contract with the version in force (DP-07); `rwb.access.partner.instruction-types.*` is read through the parameters contract (DP-06).
- **The end-to-end proof:** the legacy acceptance criteria 1, 2, 3, 4, 5, 7 and 8 of RWB-E2-019 are carried by **RWB-ITG-E2019-ITG**; this story owns legacy AC6 and AC9 only, and section 7 copies exactly those two.
- **The record of a refusal:** the local decision record is written through the access-entry writer of RWB-P4-E1039-APP over the local decision-record library (DP-03); this story builds no record writer of its own and writes no P7 table.
- **Service naming:** base `/api/recovery/access/v1` (DP-13), schema `rwb_access`, topic `rwb.access.events.v1` (DP-14, not used here), Temporal task queue `rwb-access` in namespace `rwb-recovery` (not used here), Java package `th.co.scb.ace.workbench.recovery.access`.
- **Events:** this story publishes no event and consumes none. `rwb.access.AccessPolicyChanged.v1` belongs to the story that loads a policy version (RWB-P4-E1037-APP) and `rwb.access.DoALimitChanged.v1` to the DoA story; DP-09 is not in this pattern set.
- **No token and no session:** the partner session lives at the external gateway (Architecture v5 slide 35; ADR-010). rwb-access holds no session table, no password, no token store and no refresh token, and it answers roles and policy only.
- **Database access:** through the per-service rwb-access login of the service baseline (DP-02). No statement of this story names a table of another schema, an ACE view or a table in `public`.

### 2. Business rationale

Partners today use separate channels — the lawyer web, the agency portal, SVAF and file transfer — and the bank cannot show one record of what a firm could see. The legacy story answered with one partner identity per person, separate from bank identities, bound to one firm and one partner role, limited to cases placed with that firm, and refused when the firm is suspended, exits the panel or reaches its contract end. That answer stays, and the realignment makes it a smaller and a stronger answer by splitting it three ways and by fixing which service owns which fact.

**The division is fixed and is the same in all three stories of this legacy key.** **RWB-P4-E2019-APP**, **RWB-P4-E2019-CON** and **RWB-P4-E2019-INF** are the rwb-access slice: the identity resolution and its answer, the contract the external gateway calls, and the DMZ plumbing that carries the call. **RWB-S9-E2019-APP** is the neighbour that owns the firm, the partner user, the binding and the instruction — `partner`, `partner_user` and `partner_instruction` are S9's under the Ownership Map ruling ASM-0072, so rwb-access keeps the internal role model only and reads no S9 table. **RWB-P7-E2019-APP** is the neighbour that owns the central ledger entries a partner sign-in and a partner refusal leave behind. **RWB-ITG-E2019-ITG** is the end-to-end proof of the key: the sign-in, the role per partner, the revoked firm, the identity with no binding, the missing second factor, two partner roles and a bank screen refused are proven there, across the gateway, rwb-access and rwb-partner, and no part of those criteria is restated in this slice.

The split follows the architecture rather than a preference. Architecture v5 keeps one entry per audience: staff screens go through gateway-bff and the shared App Gateway, and partners come only through a partner gateway in the DMZ with the FAPI 2.0 profile (slides 20 and 35). rwb-access is the reference-data owner of the roles, the scope and the masking policy and it is a cached, one-hop contract for every service that authorises (slides 10, 14 and 41). rwb-partner is the owner of the panel, of the partner users and of the instructions (slides 17 and 41). Holding a partner user table in rwb-access would put the firm's binding in two schemas and would make rwb-access read a firm's panel status across a boundary; resolving a partner identity to the **role model** needs no such read, because the role rows, their letters, their default scope and the masking rules are rwb-access's own data. The values the criteria use are the legacy values unchanged — partner identities `P-5101`, `P-5103`, `P-5104`, test user `U-5105`, firms `LF-0012` and `LF-0019`, valuer `VL-0004`, instruction `INS-2027-000431`, partner roles PT-AGENCY, PT-LAWFIRM, PT-VALUER, PT-AUCTION, PT-BUYER and PT-RAMC, scope `PLACED`, and the messages MSG-P4-001, MSG-P4-002, MSG-P4-003, MSG-P4-005, MSG-P4-006 and MSG-P4-008.

The negative side is fixed as tightly as the positive one. A partner user holds exactly one partner role and never a bank role; the resolution refuses rather than guesses; a bank identity on the partner route is refused with MSG-P4-001 and one `AC-DENY` entry whose reason is `BANK_IDENTITY_ON_PARTNER_ROUTE`; an instruction of another firm is answered `404` with MSG-P4-003 and no data; personal data never enters the answer, the record or the log, and the partner identity appears as its directory reference only. The scope type `PLACED` is the legacy scope name and is not a value of `LOV-SCOPE` in TSD P4 v3 T3.2, which holds OWN, TEAM, REGION and ALL; the resolution therefore carries `PLACED` as a scope descriptor of a partner session and does not add it to the role default-scope list — Not specified in the source documents (GAP-0784; ASM-1432).

It supports REQ-ACA-012 in full, meets NFR-050 (partner accounts authenticate with multi-factor and are scoped to their own cases), and is the input to the masking and the access log that every screen and every service applies. Two source points remain open and are carried as placeholders rather than invented: the operation path, its claim names and its answer schema are named by no source (GAP-0784; ASM-1432), and the lifetime of a resolution answer beyond the gateway's token lifetime is named by no source (GAP-0784; ASM-1438).

### 3. Preconditions

- RWB-P4-E2019-CON is published (this story's contract deliverable): the operation `POST /api/recovery/access/v1/partner-identities/resolve`, its claim set, its answer (roles, scope, matrix version, masking policy version, expiry), its refusal vocabulary and its fakes. This story implements that baseline and adds no path of its own.
- RWB-P4-E1022-APP is done: the session resolution answers the roles of a signed-in caller, the matrix version and the masking version, and the guard library answers the capability area and the right of an action.
- RWB-P4-E1039-APP is done: the access-entry writer and the local decision record exist, so a resolution and a refusal are recorded with decision code `AC-SIGN` or `AC-DENY` and a reason.
- RWB-P4-E1037-CON, RWB-PLT-E1037-CON and RWB-P4-E1037-APP are in place: the authorise contract, the guard library and the role, permission, `role_conflict` and `masking_rule` rows this story reads.
- RWB-PLT-E1027-CON is published: the local decision-record library and the shared topic `rwb.decision-record.v1` (DP-03).
- RWB-PLT-E1042-CON and RWB-PLT-E1043-CON are published: the parameters client library and the reference-data client library (DP-06, DP-07); RWB-P3-E1042-CON and RWB-P3-E1043-CON publish the rwb-case contracts behind them.
- RWB-PLT-E1044-CON is published: the per-service Flyway sequence in `rwb_access` (DP-15). This story adds no table of its own and no migration beyond the rows it seeds.
- RWB-PLT-N001-CON is published: the gateway-bff composite route, so the 403 and 404 shapes of a refusal reach the screen as the route's problem detail (DP-19). A partner never calls gateway-bff; this dependency is the staff view of the same records.
- Matrix version `PM-2026.11` and masking version `MASK-SIT-01` are in force; `MASK-SIT-01` carries no unmasked rule for a partner role until Compliance supplies one (DL26).
- The partner role rows are loaded with role class `PARTNER_USER` and their Entra group names: PT-AGENCY, PT-LAWFIRM, PT-VALUER, PT-AUCTION, PT-BUYER and PT-RAMC, for example the group `RWB-SIT-PT-LAWFIRM` of the single sign-on sheet (DL40). PT-LED has no login and no role row.
- The parameters `rwb.access.partner.instruction-types.PT-LAWFIRM=FILE_SUIT,ENFORCE`, `rwb.access.partner.instruction-types.PT-VALUER=APPRAISE`, `rwb.access.partner.instruction-types.PT-AGENCY=COLLECT` and `rwb.refload.approver.partner_user=RW-SECADM` are loaded in the parameter catalog with the version in force. The PT-AGENCY row is marked assumed in the legacy story with owner RW-AGENCYMG; it is carried unchanged.
- The claim set the external gateway supplies is the one RWB-P4-E2019-CON fixes: the partner identity reference, the partner id, the partner role code or codes, the firm state and contract end, the authentication methods (`amr`), the route and the token expiry. The claim names and the operation path are Not specified in the source documents (GAP-0784; ASM-1432).
- No S9 table is reachable from this story by design: `partner`, `partner_user` and `partner_instruction` are S9's (DP-01; ASM-0072), and the partner facts above arrive as claims of the caller, not as rows.
- No build dependency blocks the contract work, and every H dependency is a CON story or an in-lane P4 story that starts earlier; the story is ready after RWB-P4-E1022-APP and RWB-P4-E1039-APP.

### 4. Flow

1. A partner user signs in at the partner portal through the external gateway. The gateway has already authenticated the identity with a second factor, resolved the partner user and the partner role against rwb-partner, and holds the firm's panel status and contract end (RWB-PLT-N007-INF; RWB-S9-E2019-APP).
2. The gateway calls `POST /api/recovery/access/v1/partner-identities/resolve` with the claims of section 11: the partner identity reference `P-5101`, the partner id `LF-0012`, the partner role code `PT-LAWFIRM`, the firm state `ACTIVE` with contract end 30 June 2027, `amr` holding `pwd` and `mfa`, the route `partner`, and the token expiry.
3. PartnerClaimValidator checks the set before any read: the route is the partner route, the identity reference is present, the token expiry is in the future, and the identity reference carries no bank role claim.
4. A claims set that names a bank identity is refused at once with status 401 and MSG-P4-001, and the refusal is passed to the access-entry writer of RWB-P4-E1039-APP with decision code `AC-DENY` and reason `BANK_IDENTITY_ON_PARTNER_ROUTE` (AC9).
5. PartnerClaimValidator checks the second factor: where `amr` holds `pwd` only, the resolution is refused with status 401 and MSG-P4-005, and no role is answered.
6. PartnerRoleResolver reads the `role` rows named by the claims at the matrix version in force: each code must exist, be class `PARTNER_USER`, and carry the `PARTNER_PORTAL` letters the caller's action needs. A code that is unknown, is class `BANK_USER`, or is a non-human actor is refused with status 401 and MSG-P4-001, so an identity with no partner role gets no role at all (ASM-1435).
7. Where the claims name two partner roles, or a partner role together with a bank role, the resolution is refused with status 403 and MSG-P4-006 naming both codes, and the refusal is passed to the access-entry writer with reason `ROLE_CONFLICT` (BR3, ASM-1434).
8. Where the claims name no partner role at all, or assert that the identity has no active binding to a firm, the resolution is refused with status 401 and MSG-P4-001, and the refusal is recorded with reason `NO_PARTNER_BINDING`.
9. The firm state is read from the claim, never from a table: `ACTIVE` or `ON_NOTICE` with a contract end of today or later resolves; `SUSPENDED`, `EXITED` or a contract end before today is refused with status 403 and MSG-P4-008, and the refusal is recorded with reason `PARTNER_NOT_ACTIVE`.
10. PartnerScopeBuilder builds the scope descriptor: scope type `PLACED`, the partner id `LF-0012`, and the instruction types of the role read through the parameters contract — `FILE_SUIT,ENFORCE` for `PT-LAWFIRM`. The descriptor names the filter; the owner of the instruction applies it in its own query (BR4).
11. PartnerMaskingVersionReader and the session answer fix the versions in force at the moment of resolution: matrix version `PM-2026.11` from `permission.matrix_version` and masking version `MASK-SIT-01` from `masking_rule.masking_version`. Both stay for the life of the answer and change only at the next resolution (ASM-1433).
12. The answer returns the roles with their class, the scope descriptor, the matrix version, the masking policy version and the expiry; the expiry is the token expiry the caller supplied and is never later than that instant (ASM-1438).
13. One decision record with decision code `AC-SIGN`, actor `P-5101`, role `PT-LAWFIRM`, partner `LF-0012` and the versions is passed to the access-entry writer of RWB-P4-E1039-APP, which writes it locally and publishes it to `rwb.decision-record.v1` (DP-03, ASM-1437).
14. The gateway forwards the partner id and the role to the partner portal call. A read of instruction `INS-2027-000431`, placed with `LF-0019`, is applied by the owner against scope `PLACED` of `LF-0012` and answers status 404 with MSG-P4-003 and no instruction data (AC6).
15. No resolution is cached across requests and no value of another service is stored: the claims are used for the one answer and discarded, and the only rows read are `role`, `permission`, `masking_rule` and `role_conflict` in `rwb_access` (ASM-1436).

### 5. Exception paths

| ID | Trigger | What happens | Message | Covered by |
|---|---|---|---|---|
| X1 | The claims name a bank identity and the route is the partner route | The resolution is refused with 401; one `AC-DENY` record carries reason `BANK_IDENTITY_ON_PARTNER_ROUTE`; no role and no scope is answered | MSG-P4-001 | AC9 |
| X2 | The signed-in partner reads an instruction placed with another firm | The scope descriptor of the answer carries `PLACED` and the partner id, the owner of the instruction applies it, and the read answers 404 with no instruction data | MSG-P4-003 | AC6 |
| X3 | `amr` holds `pwd` only | The resolution is refused with 401 and no role is answered; the refusal is recorded | MSG-P4-005 | RWB-ITG-E2019-ITG |
| X4 | The claims name no partner role, or an unknown role code, or a role of class `BANK_USER` | The resolution is refused with 401; no role is answered | MSG-P4-001 | RWB-ITG-E2019-ITG |
| X5 | The claims name two partner roles, or a partner role and a bank role | The resolution is refused with 403, both codes are named, and one record carries reason `ROLE_CONFLICT` | MSG-P4-006 | RWB-ITG-E2019-ITG |
| X6 | The firm state claim is `SUSPENDED` or `EXITED`, or the contract end is before today | The resolution is refused with 403 and one record carries reason `PARTNER_NOT_ACTIVE` | MSG-P4-008 | RWB-ITG-E2019-ITG |
| X7 | The claim asserts no active binding of the identity to a firm | The resolution is refused with 401 and one record carries reason `NO_PARTNER_BINDING` | MSG-P4-001 | RWB-ITG-E2019-ITG |
| X8 | The answer's expiry has passed when the partner calls again | The call is refused 401 with MSG-P4-001; a new resolution is needed and no stale role is served | MSG-P4-001 | AC9 |
| X9 | The token expiry claim is absent or in the past | The resolution is refused 401 with MSG-P4-001 rather than answered with an unbounded expiry | MSG-P4-001 | AC9 |
| X10 | A claim names a partner fact this service cannot check, for example a firm contract end in a shape it cannot read | The claim set is refused 400 with the field named and no role is answered; nothing is guessed | None | AC6 |
| X11 | The claim set carries a personal field, a token or a credential | The field is rejected before any read and the request is logged with the field name only, never the value | None | AC9 |

No exception path of this story changes a case, a task or an instruction: rwb-access answers roles and policy, and the case, the instruction and the partner state machines are rwb-case's and rwb-partner's.

### 6. INVEST check

| Test | Result |
|---|---|
| Independent | Builds against RWB-P4-E2019-CON, the P4 contracts of the same lane, the parameters and reference-data fakes and the decision-record library; the firm, the binding and the instruction belong to RWB-S9-E2019-APP and are not prerequisites of this build |
| Negotiable | The partner role roster, the instruction types per role, the matrix version and the masking version are data; the claim set and the answer shape are open until the contract freeze of RWB-P4-E2019-CON |
| Valuable | One controlled way for a partner identity to become a Recovery role, a PLACED scope and a masking policy, with no partner table and no token in rwb-access |
| Estimable | One resolver, one claim validator, one role resolver, one scope builder, one version reader and the refusal mapping |
| Small | Fits one sprint with its tests, as the app slice of a legacy key that three stories share |
| Testable | Each criterion below is one component or contract test against the fakes of section 12.8, plus the one-hop call of the gateway |

### 7. Acceptance criteria

```gherkin
Feature: Partner identities resolved to Recovery roles through the external gateway

  Background:
    Given the rwb-access base path is /api/recovery/access/v1 and the schema is rwb_access
    Given the rwb-partner contract mock returns partner "LF-0012" as a LAW_FIRM with panel status "ACTIVE" and contract end 30 June 2027
    Given the rwb-partner contract mock returns partner "LF-0019" as a LAW_FIRM with panel status "ACTIVE"
    Given the rwb-partner contract mock returns partner "VL-0004" as a VALUER with panel status "ACTIVE"
    Given the partner role rows "PT-LAWFIRM", "PT-VALUER" and "PT-AGENCY" are class "PARTNER_USER" at matrix version "PM-2026.11", with the letter "-" in "QUEUE_AND_ALLOCATION" and their letters in "PARTNER_PORTAL"
    Given masking version "MASK-SIT-01" is in force and carries no unmasked rule for a partner role

  Scenario: AC6 An instruction of another firm is not returned (legacy RWB-E2-019 AC6)
    Given the rwb-partner contract mock returns instruction "INS-2027-000431" placed with "LF-0019", and "P-5101" is signed in for "LF-0012"
    When "P-5101" requests instruction "INS-2027-000431" placed with "LF-0019"
    Then the call returns status 404 with message MSG-P4-003 and no instruction data

  Scenario: AC9 A bank identity cannot use the external gateway (legacy RWB-E2-019 AC9)
    Given test user "U-5105" holds RW-LITOFF with a bank identity
    When "U-5105" signs in through the external gateway
    Then the system refuses the session with message MSG-P4-001
    Then one entry with decision code "AC-DENY" and reason "BANK_IDENTITY_ON_PARTNER_ROUTE" is written
```

These are the two legacy criteria of RWB-E2-019 that this slice owns, copied word for word with the origin tag. AC6 keeps every value of the legacy criterion (`INS-2027-000431`, `LF-0019`, `LF-0012`, `P-5101`, status 404 and MSG-P4-003); its one cross-service Given, which names an instruction of rwb-partner, is replaced by the rwb-partner contract mock and the session fact of the same line. AC9 names a bank identity and the partner route, and its whole body is the legacy body unchanged. The other seven criteria of the key — AC1 partner sign-in, AC2 role per partner, AC3 revoked, AC4 an identity with no binding, AC5 no second factor, AC7 two partner roles or a bank role, AC8 a partner cannot reach bank screens — are carried by **RWB-ITG-E2019-ITG**, and no part of them is restated here.

### 8. Business rules

| ID | Rule | Source |
|---|---|---|
| BR1 | A partner user holds a partner identity separate from bank identities and is resolved only on the partner route, after multi-factor authentication | NFR-050; REQ-ACA-012; legacy RWB-E2-019 BR1 |
| BR2 | A partner identity resolves to exactly one partner role; the role is a row of `role` with class `PARTNER_USER`, never a constant in code | legacy RWB-E2-019 BR2; TSD P4 v3 T3.1 `role`; ASM-0072 |
| BR3 | Two partner roles, or a partner role held together with a bank role, refuse the resolution with MSG-P4-006 and one record whose reason is `ROLE_CONFLICT` | legacy RWB-E2-019 BR2 and AC7; FSD P4 AC-EXC-P4-001-03 |
| BR4 | A partner role sees only cases and instructions placed with its firm: the answer carries scope type `PLACED`, the partner id and the instruction types of the role, and the owner of the instruction applies the filter in its own query | legacy RWB-E2-019 BR3 and BR4; scope `Placed cases`; parameters `rwb.access.partner.instruction-types.*` |
| BR5 | Access ends when the firm's panel status is `SUSPENDED` or `EXITED`, or its contract end has passed; the state is read from the claim and refused with MSG-P4-008 | legacy RWB-E2-019 BR5; DF-PRT-005 panel_status; DF-PRT-006 contract_end; LOV-PANEL |
| BR6 | The permission matrix, the masking rules and the access log apply to a partner user exactly as to a bank user, at the same matrix and masking versions | legacy RWB-E2-019 BR6; Admin and access model, section 8.1 |
| BR7 | A bank identity is refused on the partner route with MSG-P4-001 and one record whose reason is `BANK_IDENTITY_ON_PARTNER_ROUTE` | legacy RWB-E2-019 AC9 and BR1 |
| BR8 | rwb-access holds no partner table and reads no S9 table: `partner`, `partner_user` and `partner_instruction` are rwb-partner's, and the partner facts arrive as claims | DP-01; Ownership Map ruling ASM-0072 |
| BR9 | No token, refresh token, password, client secret or private key is held, cached or logged here; the answer carries roles, scope and versions only | ADR-010; Architecture v5 slides 29 and 35; NFR-052 |
| BR10 | No personal data is read, answered, cached or logged: the partner identity is a directory reference, the partner is an id, and a field of the claim set that carries personal data is rejected | NFR-039; NFR-040; Architecture v5 slide 35 |
| BR11 | A refusal is recorded rather than silently dropped: a resolution writes `AC-SIGN`, a refusal writes `AC-DENY` with its reason, through the access-entry writer of RWB-P4-E1039-APP | legacy RWB-E2-019 AC1, AC3, AC4 and AC9; DP-03 |
| BR12 | The answer's expiry is bounded by the token expiry the gateway supplies and by nothing later; no stale role and no stale masking version is served after it | Architecture v5 slide 35 (15-minute idle timeout, short-lived token); ASM-1438 |
| BR13 | No partner reaches the Workbench in PROD until the architecture change for external access is approved, so the resolution stays behind the feature flag until DL03 closes | legacy RWB-E2-019 BR7; DL03 |

### 9. State transitions

None for a case, a task or an instruction. This story holds no case state (TSD P4 v3 T4). The states it reads are the states of a matrix version, a masking version and a firm, and the state it produces is the state of a resolution answer.

| Object | From | Event | To | Result |
|---|---|---|---|---|
| Resolution answer | (none) | The claims pass validation, the role rows resolve and the firm state is `ACTIVE` or `ON_NOTICE` with a contract end of today or later | RESOLVED | Roles, scope `PLACED`, matrix version, masking version and expiry are answered; one `AC-SIGN` record is written |
| Resolution answer | (none) | A check fails — route, identity class, second factor, role count, role class, firm state or expiry | REFUSED | The stated status and message are answered, one `AC-DENY` record carries its reason, and no role is answered |
| Resolution answer | RESOLVED | The expiry instant passes | EXPIRED | The next call needs a new resolution; no stale role is served |
| Resolution answer | RESOLVED | A new matrix or masking version comes into force | RESOLVED | The answer keeps its versions until it expires; the next resolution reads the versions then in force |
| Partner session | RESOLVED | The firm's status turns `SUSPENDED` or `EXITED`, or the binding ends | ENDED | The next resolution is refused with MSG-P4-008; ending a session is the gateway's act on the next call |

The version status vocabulary is LOV-VERSION-STATUS (LOADED, VALIDATED, APPROVED, IN_FORCE, SUPERSEDED, ROLLED_BACK, REFUSED) in TSD P4 v3 T3.2. This story reads the version in force and writes neither a version status nor a firm state.

### 10. Authority

| Who | What they may do in this story |
|---|---|
| rwb-access service identity (the per-service login, DP-02) | Resolves a partner identity to the role model, answers the scope descriptor and the versions, and passes each resolution and refusal to the access-entry writer of RWB-P4-E1039-APP |
| RW-AGENCYMG Partner and agency manager | Requests a partner user in the bank identity directory, names the firm and the partner role, and sets the firm's panel status in rwb-partner (RWB-S9-E2019-APP) |
| Role owner (bank IAM, level 2) | Approves each partner user request |
| Access administrator (bank IAM, level 3) | Creates the partner identity and adds it to the group of the partner role |
| RW-SECADM Security administrator | Maintains the partner role rows, the groups and the conflict pairs; approves the binding version of the reference data it owns; receives a conflict incident |
| RW-REFADM Reference data administrator | Loads the parameter rows of the instruction types; loads no partner row, because no partner table is rwb-access's |
| PT-LAWFIRM, PT-VALUER, PT-AGENCY, PT-AUCTION, PT-BUYER, PT-RAMC | Are answered by the resolution for their own record; each holds the `PARTNER_PORTAL` letters of its role and no bank letter |
| RW-LITOFF | Holds a bank role on the bank route; the partner route refuses it (AC9) |
| The architecture team | Approves external access before PROD (DL03); the feature flag stays off until then |
| No delegation of authority level applies | A role, a scope and a masking version are not a credit decision |

The partner role groups are maintained as data and the resolution reads them as rows; the database login is the per-service login of the service baseline (DP-02), and this story adds no grant.

### 11. Data

| BR Field ID | Table in `rwb_access` | Field | Read or write |
|---|---|---|---|
| DF-REF-034 to DF-REF-039 | `role` | id, role_code, role_name, role_class, default_scope, entra_group | Read; the partner role rows carry class `PARTNER_USER` |
| DF-REF-040 to DF-REF-044 | `permission` | id, role_id, capability_area, letters, matrix_version | Read; the letters of the `PARTNER_PORTAL` area and matrix version `PM-2026.11` |
| DF-REF-198 to DF-REF-204 | `masking_rule` | id, role_code, field_id, unmasked, masking_version, valid_from, valid_to | Read; masking version `MASK-SIT-01` and the rules in force |
| DF-REF-205 to DF-REF-211 | `role_conflict` | id, role_code, conflicts_with, reason, conflict_version, valid_from, valid_to | Read; the pairs that refuse a resolution |
| DF-DEC-001 to DF-DEC-018 | decision record (local library, DP-03) | the `AC-SIGN` and `AC-DENY` facts of a resolution | Written by the access-entry writer of RWB-P4-E1039-APP; this story writes no row of its own |
| DF-REF-027 to DF-REF-033 | `lov_value` of `rwb_case` | lov_code, value_code, label_en | Read through the reference-data contract (DP-07); never read from `rwb_access` |

Named only, and never read by any statement of this story (DP-01; Ownership Map ruling ASM-0072): DF-REF-212 to DF-REF-217 of `partner_user`, DF-PRT-001, DF-PRT-004, DF-PRT-005, DF-PRT-006 and DF-PRT-010 to DF-PRT-011 of `partner` and `partner_instruction`. They are rwb-partner's, and the partner id, the role code and the firm state of a request arrive in the claim set of section 12.1 — not from a table. The story therefore resolves a partner identity to P4 roles and scopes from the partner-supplied claims and its own `role`, `permission` and `masking_rule` data, and reads no S9 table.

The claim set of a resolution carries no personal field and no credential: the partner identity reference, the partner id, the partner role code or codes, the firm state and contract end, `amr`, the route and the token expiry. The claim names are Not specified in the source documents (GAP-0784; ASM-1432), and the lifetime of the answer beyond the token expiry is Not specified in the source documents (GAP-0784; ASM-1438). Field IDs are those in the Logical Data Model and Data Dictionary, and the legacy physical names `role`, `permission`, `masking_rule` and `role_conflict` are kept.

### 12. Contract

#### 12.1 REST operations provided

Owner rwb-access (P4); base `/api/recovery/access/v1`. The contract is RWB-P4-E2019-CON's; this story implements it.

| Method | Path | Purpose | Access | Idempotency |
|---|---|---|---|---|
| POST | `/api/recovery/access/v1/partner-identities/resolve` | Resolve a partner identity presented through the external gateway to the Recovery role model: the roles with their class, a scope descriptor of type `PLACED` with the partner id and the instruction types, the matrix version, the masking policy version and the expiry | The partner route of the external gateway, with the workload identity of RWB-P4-E2019-INF; the caller holds the `PARTNER_PORTAL` letters of its role | `Idempotency-Key` required on the POST; a replay answers the first answer and writes no second record |

Errors: 400 a claim set of the wrong shape (no message id), 401 no partner role, no binding, no second factor, a bank identity on the partner route or an expired answer (MSG-P4-001, MSG-P4-005), 403 two roles or a partner role with a bank role (MSG-P4-006) and a firm that is not active (MSG-P4-008), 503 the record cannot be written (MSG-P7-003). The 404 case of AC6 belongs to the owner of the instruction and not to this operation.

The path, its claim names and its answer schema are Not specified in the source documents (GAP-0784; ASM-1432): TSD P4 v3 appendix T-A lists API-P4-004 to API-P4-021 and none is a partner identity operation, API Specification v4 declares no `x-module: P4` partner path, and Architecture v5 slide 14 names `/authorise`, `/me/permissions`, `/doa-limits` and `/masking-policies` only. The path follows the base rule of DP-13, is fixed by RWB-P4-E2019-CON, and duplicates no path of rwb-partner.

#### 12.2 REST operations consumed

| Method and path | Owner | Use |
|---|---|---|
| GET /api/recovery/case/v1/admin/parameters | P3 rwb-case | The instruction types of a partner role (`rwb.access.partner.instruction-types.*`) and the approval role of the binding, with the version in force (DP-06) |
| GET /api/recovery/case/v1/admin/lists/{listCode} | P3 rwb-case | `LOV-ROLE-CLASS`, `LOV-CAPABILITY` and `LOV-SCOPE` at the version in force, so no class, area or scope is a constant in code (DP-07) |

Each call is one hop with a 2 s timeout and a breaker, and the references are cached no longer than the resolution itself (DP-11, ASM-1436). Neither operation is provided by rwb-access, and no operation of rwb-partner or rwb-decision is consumed here.

#### 12.3 Events published

None. rwb-access is a reference-data owner in Architecture v5 slide 14 and publishes `rwb.access.AccessPolicyChanged.v1` and `rwb.access.DoALimitChanged.v1` only, both from other stories of the service. The `AC-SIGN` and `AC-DENY` facts leave through the local decision-record library as `rwb.decision-record.DecisionRecorded.v1` on `rwb.decision-record.v1` (DP-03), which is the platform library's event and not this service's.

#### 12.4 Events consumed

None. The matrix and the masking versions are read at resolution time and refreshed at the next resolution; this story subscribes to no topic and holds no consumer group.

#### 12.5 Workflows and activities

None. The resolution is synchronous on the caller's thread: no Temporal workflow, activity, signal or task queue takes part, and the `rwb-access` queue carries only the access review Schedule of RWB-P4-AD008-APP.

#### 12.6 Schedules

None. No Schedule of this story exists. The six-monthly access review list (JOB-18) is RWB-P4-AD008-APP's, and the firm-state refresh the legacy story described is the gateway's, not a Schedule here.

#### 12.7 Tables owned

| Table | Owner | Use in this story |
|---|---|---|
| `role` | P4 (rwb_access) | The partner role rows of class `PARTNER_USER` and their default scope |
| `permission` | P4 (rwb_access) | The letters of the `PARTNER_PORTAL` area and the matrix version in force |
| `masking_rule` | P4 (rwb_access) | The masking version in force and the rules that apply to the session's roles |
| `role_conflict` | P4 (rwb_access) | The pairs that refuse a resolution |
| `outbox_event`, `processed_event`, `idempotency_key` | PLT library, created in `rwb_access` by the service's own DB story | The replay guard of the resolution POST; no event of this story uses the outbox |

**rwb-access holds no partner table and no token.** `partner`, `partner_user` and `partner_instruction` are S9 rwb-partner's (Ownership Map ruling ASM-0072), `decision_log_entry` and `approval` are P7 rwb-decision's, and `lov_value` is P3 rwb-case's. This story resolves a partner identity to P4 roles and scopes from the partner-supplied claims and its own `role`, `permission` and `masking_rule` data, and reads no S9 table (DP-01).

#### 12.8 Contract fakes

| Fake | Serves | Stubs used by this story |
|---|---|---|
| Gateway claim fake | The claim set of `POST /api/recovery/access/v1/partner-identities/resolve` | `P-5101` for `LF-0012` with `PT-LAWFIRM`, firm state `ACTIVE` and contract end 30 June 2027; `U-5105` with a bank identity and the partner route; `amr` with `pwd` only; two role codes; an unknown code (AC9, X3 to X7) |
| rwb-partner contract fake (S9) | The instruction read of AC6 and the firm facts of the Background | Instruction `INS-2027-000431` placed with `LF-0019`; firms `LF-0012`, `LF-0019` and `VL-0004` with their panel states |
| Parameters fake (P3) | `GET /api/recovery/case/v1/admin/parameters` | `rwb.access.partner.instruction-types.PT-LAWFIRM=FILE_SUIT,ENFORCE`, `PT-VALUER=APPRAISE`, `PT-AGENCY=COLLECT` at version PAR-2026.11 |
| Reference-data fake (P3) | `GET /api/recovery/case/v1/admin/lists/{listCode}` | `LOV-ROLE-CLASS` with BANK_USER, PARTNER_USER, NON_HUMAN_ACTOR; `LOV-CAPABILITY` with PARTNER_PORTAL and QUEUE_AND_ALLOCATION; `LOV-SCOPE` with OWN, TEAM, REGION, ALL |
| Decision-record fake (DP-03) | The access-entry writer of RWB-P4-E1039-APP | A recorder that captures decision code, actor, role, partner and reason, and a switch that fails the write |
| Role fixture | The `rwb_access` rows of matrix version `PM-2026.11` and masking version `MASK-SIT-01` | The partner role rows, their `PARTNER_PORTAL` letters, the `-` in `QUEUE_AND_ALLOCATION`, the conflict pairs and the masking rules |

#### 12.9 Call-type summary

| Call type | Provided | Consumed | Notes |
|---|---|---|---|
| REST | 1 | 2 | The resolution provided on the P4 base; the parameters and reference-data reads consumed, one hop, 2 s timeout with a breaker |
| Kafka | 0 | 0 | No topic produced or consumed here; the record leaves through the DP-03 library on `rwb.decision-record.v1` |
| Temporal | 0 | 0 | No workflow, activity or Schedule |
| File | 0 | 0 | No file is read or written |

### 13. Solution plan

**Package.** `th.co.scb.ace.workbench.recovery.access.partner` in the rwb-access service, with the contract types of RWB-P4-E2019-CON in `th.co.scb.ace.workbench.recovery.access.api.partner`.

**Pattern application**

| DP | Legacy marker | Microservice pattern | Dependency added |
|---|---|---|---|
| DP-01 | `recovery.<table>` or "recovery schema" | Owner's schema `rwb_<name>`; never read another service's tables. The partner, the binding and the instruction stay in `rwb_partner` and are never read here | none |
| DP-03 | DecisionLogWriter, decision log | Local decision-record library and topic `rwb.decision-record.v1`; the `AC-SIGN` and `AC-DENY` facts are written through the writer of RWB-P4-E1039-APP | H RWB-PLT-E1027-CON |
| DP-05 | AceSourceQuery, `v_ace_*`, account_ext | Read through rwb-source-data's contract or the service's own ACE views. No ACE view is read here: a partner identity is a claim, not an ACE row | none |
| DP-06 | Parameters, casewf.config | Parameters contract of rwb-case and the client library, for the instruction types and the approval role | H RWB-PLT-E1042-CON; C RWB-P3-E1042-CON |
| DP-07 | Reference data, LOV | Reference-data contract of rwb-case, for the role class, the capability areas and the scopes | H RWB-PLT-E1043-CON; C RWB-P3-E1043-CON |
| DP-08 | RecoveryAccessGuard | Authorise contract of rwb-access and the guard library; the resolution answers what the guard then checks on each call | H RWB-PLT-E1037-CON; C RWB-P4-E1037-CON |
| DP-11 | In-process call, published interface | REST contract with mock; one hop; 2 s timeout. The gateway call is one hop and the two P3 reads are one hop each | none (C from the legacy dependency) |
| DP-13 | `/api/recovery/v1` | `/api/recovery/<short>/v1`; the resolution sits on the P4 base and duplicates no S9 path | none |
| DP-15 | V0001 baseline, migration | Per-service Flyway sequence in `rwb_access`; the partner role rows and the conflict pairs arrive as dated rows of an approved matrix version | H RWB-PLT-E1044-CON |
| DP-19 | Screen, ace-web | gateway-bff composite route for the staff view of the same records; a partner never uses it | H RWB-PLT-N001-CON |

**What changes from the monolith.** The legacy `PartnerAccessService`, `PartnerSessionRevalidation` and `PartnerUserRepository` of one process are replaced by one resolver in rwb-access plus the partner facts that now arrive as claims. The `partner_user` table and its loader leave this service with the S9 ruling (ASM-0072), and the firm status call to a module interface becomes a claim asserted by the external gateway, which holds the S9 answer. No new hardware is implied: the resolver runs on the existing rwb-access pods, reads four tables of its own schema, and adds no database, topic, queue or bucket.

**Components**

| Component | Type | Responsibility |
|---|---|---|
| `PartnerIdentityController` | Controller | The one POST of section 12.1; validation, idempotency, problem responses (BR1) |
| `PartnerClaimValidator` | Service | Checks the route, the identity class, the second factor, the token expiry and the absence of personal fields before any read (BR1, BR9, BR10) |
| `PartnerRoleResolver` | Service | Resolves the claimed role codes against `role` and `permission` at the matrix version in force; refuses an unknown, bank-class or non-human role (BR2) |
| `PartnerConflictChecker` | Service | Applies `role_conflict` to the claimed roles and refuses two partner roles or a partner role with a bank role (BR3) |
| `PartnerScopeBuilder` | Service | Builds the `PLACED` scope descriptor with the partner id and the instruction types of the role from the parameters contract (BR4) |
| `PartnerVersionReader` | Service | Reads `permission.matrix_version` and `masking_rule.masking_version` in force and stamps the answer (BR6) |
| `PartnerResolutionRefusal` | Component | The refusal vocabulary of section 14 with its status and message id, and the `AC-DENY` reason of each (BR3, BR5, BR7) |
| `PartnerDecisionRecordClient` | Client | Passes each resolution and refusal to the access-entry writer of RWB-P4-E1039-APP; writes no record of its own (BR11) |
| `PartnerFixtureLoader` | Test asset | Seeds the role rows, the conflict pairs and the masking rules of the version in force, and the claims of the fakes |

**Configuration.** The feature flag `rwb.access.partner-signin` (off in PROD until DL03 closes), the parameters of the instruction types, and the 2 s client budget of the two P3 reads. The instruction types, the role codes, the scope type and the masking positions are never constants: they are rows, parameters and reference values read through their contracts.

**Build steps**

1. Publish the contract types of RWB-P4-E2019-CON and prove the resolver compiles against the baseline and the fakes (AC9).
2. Build `PartnerClaimValidator`: the route check, the identity-class check (AC9), the second factor, the token expiry and the rejection of a personal field (X3, X9, X11).
3. Build `PartnerRoleResolver` and `PartnerConflictChecker` over `role`, `permission` and `role_conflict` at matrix version `PM-2026.11` (AC9, X4, X5).
4. Build `PartnerScopeBuilder` over the parameters contract with the instruction types of each role (AC6).
5. Build `PartnerVersionReader` over `permission` and `masking_rule`, and stamp the answer with the versions in force (BR6).
6. Build `PartnerResolutionRefusal` and the reason of each refusal, and wire the access-entry writer (AC9, BR11).
7. Prove the AC6 direction against the rwb-partner contract fake: the answer names `LF-0012` and the read of `INS-2027-000431` of `LF-0019` answers 404 with MSG-P4-003 and no data.
8. Prove the 401 of AC9 with the `U-5105` claim and the `AC-DENY` record with reason `BANK_IDENTITY_ON_PARTNER_ROUTE`.
9. Put the operation behind the flag, off in PROD until DL03 closes, and run the contract tests of section 12.8.

**Feature flag.** `rwb.access.partner-signin`, read as a parameter. Off, the operation answers 404 and no partner session resolves in that environment, so a switch-off never opens an unchecked partner path.

**Done when.** The tests of section 16 pass against the fakes, AC6 answers 404 with MSG-P4-003 and no instruction data through the partner contract fake, AC9 answers MSG-P4-001 and writes one `AC-DENY` record with reason `BANK_IDENTITY_ON_PARTNER_ROUTE`, no statement names an S9 table, and the flag is off in PROD.

### 14. Validation and messages

| ID | When | Message |
|---|---|---|
| MSG-P4-001 | No partner role, no active binding, a bank identity on the partner route, or an expired answer | You have no Recovery Workbench role. Ask your team manager to request one. |
| MSG-P4-002 | An action outside the partner role's letters, refused by the guard or by the owner of the action | You cannot {action} here. Your role does not include it. |
| MSG-P4-003 | An instruction of another firm, refused by the owner of the instruction against the `PLACED` descriptor | This case is not in your scope. |
| MSG-P4-005 | `amr` holds no second factor | Sign in again with your second factor. The Workbench needs multi-factor authentication. |
| MSG-P4-006 | Two partner roles, or a partner role and a bank role | Your roles {role} and {otherRole} cannot be held together. Access is refused and the security administrator has been told. |
| MSG-P4-008 | The firm is suspended, exited or past its contract end | Your firm's access to the Recovery Workbench has ended. Contact your SCB partner manager. |

The message ids and texts are the legacy texts unchanged and their Thai text follows DL10. A 400 of a malformed claim set and a 503 where the record cannot be written carry no business message: they are one RFC 9457 problem detail with the field or the operation and the trace identifier, per Architecture v5 slide 11.

### 15. Screens and states

| Screen | State | What the person does |
|---|---|---|
| PRT-01 Partner home | Loading | Waits while the resolution and the firm's open instructions load |
| PRT-01 Partner home | List | Sees only the firm's instructions of the role's types, with due dates; the list is the owner's and the resolution only supplies the scope |
| Partner sign-in page | Refused | Sees MSG-P4-008, MSG-P4-006 or MSG-P4-001 and no data |
| Partner sign-in page | Second factor needed | Is sent back to the second factor with MSG-P4-005 |

The partner portal screens are rwb-partner's and the gateway's; this story fixes the facts behind them and renders nothing. The staff view of the same records reaches a screen only through the gateway-bff route of RWB-PLT-N001-CON (DP-19), and a partner never calls it.

### 16. Test cases

| TC ID | Covers | Level | Data |
|---|---|---|---|
| TC-E2-019-06 | AC6, BR4 | Component | Instruction `INS-2027-000431` placed with `LF-0019`, read by `P-5101` signed in for `LF-0012` through the rwb-partner contract fake; the answer carries `PLACED` and `LF-0012`; the read answers 404 with MSG-P4-003 and no data |
| TC-E2-019-09 | AC9, BR1, BR7 | Component | Bank test user `U-5105` holding RW-LITOFF on the partner route; 401 with MSG-P4-001; one `AC-DENY` record with reason `BANK_IDENTITY_ON_PARTNER_ROUTE` and no role answered |
| TC-E2-019-01 to TC-E2-019-11 | The whole legacy set of RWB-E2-019, executed here and in RWB-ITG-E2019-ITG | End to end | The eleven legacy cases of the key, of which TC-E2-019-06 and TC-E2-019-09 run here and the rest run in the end-to-end proof |
| TC-E2-019-10 | Access | Component | A role without the right is refused with MSG-P4-002 |
| TC-E2-019-11 | Principle 5 (resilience) | NFR | The decision log write forced to fail during a partner sign-in |

Every legacy case of the key is named above and none is renumbered: TC-E2-019-01, TC-E2-019-02, TC-E2-019-03, TC-E2-019-04, TC-E2-019-05, TC-E2-019-07 and TC-E2-019-08 are executed by **RWB-ITG-E2019-ITG**, and TC-E2-019-06, TC-E2-019-09, TC-E2-019-10 and TC-E2-019-11 are executed here. The full test, with its Given, When and Then, stays in the test-case workbook under the same test case ID.

### 17. Guardrails

- No business value in code: the partner role codes, the instruction types, the matrix version, the masking version, the scope type and the conflict pairs are rows, parameters or reference values read through their contracts.
- No personal data anywhere in this story: the partner identity is a directory reference, the partner is an id, and a claim that carries a personal field is rejected before any read.
- No token, refresh token, password, secret or private key is held, cached or logged; the answer carries roles, scope and versions only (ADR-010).
- No S9 table is read: `partner`, `partner_user` and `partner_instruction` stay in `rwb_partner`, and the partner facts arrive as claims (DP-01, ASM-0072).
- The owner of an object authorises the object: this story supplies the `PLACED` descriptor and never returns another firm's instruction.
- A bank identity on the partner route is refused and recorded; it is never resolved to a partner role.
- A refusal is recorded with its reason; an unrecorded refusal is a defect.
- The matrix and masking versions of an answer do not change mid-answer: one answer carries one version of each.
- The partner path stays behind the flag and off in PROD until DL03 closes.

### 18. Traceability

| Requirement ID | Requirement (short) | BRD section | Feature | L3 process | Rules | Test cases |
|---|---|---|---|---|---|---|
| REQ-ACA-012 | Partners only through the external gateway, with MFA, scoped to their own cases | Epic 2, 3.4; Program 5.4 | FEAT-OCC-13 | 12 Manage partners | BR1 to BR13 | TC-E2-019-06, TC-E2-019-09, TC-E2-019-10, TC-E2-019-11 |

| Legacy reference | Where it is kept |
|---|---|
| AC6 an instruction of another firm is not returned | Section 7 (verbatim), sections 4, 8, 12.1, 16 |
| AC9 a bank identity cannot use the external gateway | Section 7 (verbatim), sections 4, 8, 10, 12.1, 16 |
| AC1, AC2, AC3, AC4, AC5, AC7 and AC8 of RWB-E2-019 | Carried by RWB-ITG-E2019-ITG; this story states the behaviour behind them and restates none of them |
| The partner identity, the firm and the binding | RWB-S9-E2019-APP; named only here, never read (ASM-0072) |
| The central ledger entry of a partner sign-in and refusal | RWB-P7-E2019-APP; the local record is written through RWB-P4-E1039-APP |
| The external gateway, the FAPI 2.0 profile and the DMZ | RWB-PLT-N007-INF and RWB-P4-E2019-INF |
| The contract of the resolution | RWB-P4-E2019-CON |

The seven criteria of this key that this slice does not own — AC1 partner sign-in, AC2 role per partner, AC3 revoked, AC4 an identity with no binding, AC5 no second factor, AC7 two partner roles or a bank role and AC8 a partner cannot reach bank screens — are carried by **RWB-ITG-E2019-ITG** alone, and no part of them is restated in this story.

### 19. Out of scope

- The firm, the partner user, the binding and the instruction, and every partner portal operation (`rwb-partner`, S9; RWB-S9-E2019-APP).
- The contract document of the resolution, its schemas and its fakes (RWB-P4-E2019-CON).
- The partner gateway in the DMZ, its certificate handling, its mTLS hop to rwb-access, its network policy and its rate limit (RWB-P4-E2019-INF and RWB-PLT-N007-INF).
- The central decision ledger and the `GET /decision-log` read (rwb-decision, P7; RWB-P7-E2019-APP), and the local access-entry writer itself (RWB-P4-E1039-APP).
- The end-to-end journey of the key and its evidence, and the seven legacy criteria it owns (RWB-ITG-E2019-ITG).
- The partner work screens PRT-02 to PRT-06, the accept and decline, the results, the invoices, the data room and the bids (Epics 4 to 6, S9 and S6).
- Partner panel management, contracts and scorecards, and the architecture change that makes the partner portal reachable from outside the bank (DL03).
- The reference-data and parameter catalogues themselves (`rwb-case`, P3), which are consumed and faked, never defined here.
- The deployment, the Helm chart, the topic subscription, the dashboards and the runbook.

# Recovery Workbench — frontend context

**Purpose:** the frontend technology, screen inventory, design system, accessibility and interaction
rules an agent needs to specify or build a Workbench screen.
**Status:** documented from the approved design set. No live Figma file exists; the design evidence is
the screen inventory, screen specifications, design system and prototype (`CTX-GAP-019`).

## 1. Stack and architecture

| Item | Position | Source |
|---|---|---|
| Framework | React on Vite | Engineering Practices §2.3; AI Assisted Development Approach §3.1 |
| Component primitives | Radix | Engineering Practices §2.3 |
| Data and server state | TanStack Query | Engineering Practices §2.3 |
| Language and types | TypeScript; front-end types generated from the back end, never written by hand or by an AI tool | Engineering Practices §2.2 |
| Host | The ACE front end; recovery screens live in the recovery module folder | ADR-001, ADR-002, ADR-006 |
| Identity | Entra ID SSO with MFA; the access check runs on each request | RWB-E1-022; Security and Access Design v2 |
| Styling | Bank web standards; design tokens from the design system | Design System and Component Library v1 |
| Accessibility | WCAG 2.2 AA; automated scan and keyboard checks on each screen | Accessibility Standard v2; Test Strategy §1 |
| Localisation | Thai and English; Thai labels and messages are proposed, not approved (DL10) | Content and Label Standard v2; R-11 |
| Error and message standard | Every validation message returned from the message table by rule ID | Error and Message Standard v3; AGENTS.md §3 |

## 2. Screen inventory

53 screens: 47 in the Workbench and 6 in the partner portal. Every screen is in the ACE front end and
the access check runs on each request. The full inventory is
`requirement/legacy/07-screens-and-experience/recovery-workbench-screen-inventory-and-navigation-v2-xlsx.md`.

| Area | Screens | Key screens | First release |
|---|---|---|---|
| Home and cases | SCR-01 to SCR-06 | My work, case list, case record, case timeline, transfer case, raise deviation | E1 read-only case record; E2 full |
| Queues | SCR-07 to SCR-09 | Team queues, deviation queue, exception queue | E2 |
| Approvals | SCR-10 to SCR-12 | Approval queue, decision screen, committee pack | E2; E4 committee |
| Treatment | SCR-13 to SCR-17 | Route decision, treatment record, settlement offer, deed in lieu, guarantee claim | E2 record; E3 full; E4 route |
| Litigation | SCR-18 to SCR-20 | Notice approval, litigation workspace, enforcement workspace | E2 notices; E5 full |
| Assets | SCR-21 to SCR-24 | Asset list, asset record, listing and price, auction rounds | E3; E4 rounds |
| Debt sale | SCR-25 to SCR-26 | Lot builder, award | E5 data; E6 screens |
| Write-off and money | SCR-27 to SCR-29 | Write-off proposal, proceeds matching, posting | E2 skeleton; E4 full; E6 write-off |
| Documents | SCR-30 to SCR-33 | Case documents, document review queue, document custody, template approval | E1 documents; E2 custody/templates |
| Partners | SCR-34 to SCR-36 | Partner list, placement and allocation, partner scorecard | E2 identities; E6 full; E7 scoring |
| Reports | SCR-37 to SCR-38 | Steering dashboard, decision log query | E2 |
| Administration | SCR-39 to SCR-47 | Rules and parameters, reference data, delegation of authority, queues and service levels, roles and access, interface and job monitor, data quality, agent monitor, personal data | E2 monitors; E8 full |
| Partner portal | PRT-01 to PRT-06 | Partner home, instruction, court state, invoice, data room, award/transfer | E2 identities; E5/E6 full |

## 3. Navigation model

```text
Sign-in (Entra ID SSO + MFA)
└── Home
    ├── My work                     SCR-01
    ├── Cases
    │   ├── Case list               SCR-02
    │   └── Case record             SCR-03
    │       ├── Timeline            SCR-04
    │       ├── Transfer            SCR-05
    │       ├── Raise deviation     SCR-06
    │       ├── Treatment record    SCR-14
    │       ├── Route decision      SCR-13
    │       ├── Documents           SCR-30
    │       └── Decisions           SCR-38
    ├── Queues
    │   ├── Team queues             SCR-07
    │   ├── Deviation queue         SCR-08
    │   └── Exception queue         SCR-09
    ├── Approvals
    │   ├── Approval queue          SCR-10
    │   ├── Decision screen         SCR-11
    │   └── Committee pack          SCR-12
    ├── Treatment / Litigation / Assets / Debt sale / Write-off / Money
    ├── Documents
    ├── Partners
    ├── Reports
    └── Administration
```

The partner portal has a separate entry point and a separate sign-in. A partner sees only the cases
placed with their firm. The Legal Execution Department has no login; it is reached by filing and
result interfaces.

## 4. Screen behaviour and states

Every screen specification must state:

| Element | Requirement |
|---|---|
| Purpose | What the screen is for, in one sentence |
| Roles and scope | Who reaches it, with which permission letters and default scope |
| Fields | Name, type, mandatory, list of values, default, source and masking profile |
| States | Loading, empty, list, filtered, form, saved, error, read-only, on hold, at-cap warning |
| Validation | Rule ID, message ID, field-level and form-level behaviour |
| Actions | What each button does, the permission check, the confirmation and the audit entry |
| Navigation | Where the user arrives from and where each action goes |
| Data freshness | The freshness stamp shown where the decision depends on loaded data |
| Accessibility | Keyboard order, focus, labels, error announcement, contrast, target size |
| Localisation | Thai and English labels; Thai proposed until DL10 closes |
| Design evidence | The screen specification, prototype and design-system component used |

The screen specifications in `requirement/legacy/07-screens-and-experience/recovery-workbench-screen-specifications-v1.md`
are the primary source. The prototype is `Recovery Workbench Screen Prototype v1.html`.

## 5. Design system

| Area | Position | Source |
|---|---|---|
| Components | Bank web standards; Radix primitives; approved reusable components | Design System and Component Library v1 |
| Spacing and layout | Bank spacing scale; responsive breakpoints; 1280×720 is the Playwright viewport, not the design target | Design System v1; `.vscode/mcp.json` |
| Typography | Bank type scale; Thai and English font support | Design System v1 |
| Colour | Bank palette and semantic tokens; contrast checked to WCAG 2.2 AA | Design System v1; Accessibility Standard v2 |
| Icons and assets | Bank icon set; no decorative icons that carry meaning without a label | Design System v1 |
| Forms | Labels above fields; inline validation; error summary at the top of long forms | Error and Message Standard v3 |
| Tables | Server-side paging and filtering; column visibility; export where the role allows | Screen Specifications v1 |
| Empty states | Explain what the screen is for and what to do next; no blank page | Screen Specifications v1 |
| Loading states | Skeleton or progress indicator; no layout shift | Screen Specifications v1 |
| Error states | Safe message, message ID, retry where safe, support reference | Error and Message Standard v3 |

## 6. Data and API integration

- Use TanStack Query for server state; do not copy server data into local component state without a
  reason.
- Use the generated TypeScript types from the OpenAPI contract. Do not hand-write a type that the
  contract already defines.
- Every request carries the user's identity and scope; the server enforces the access check. The
  client hides what the role cannot use, but hiding is not the control.
- Mask personal fields in the client as well as the server; the server is authoritative.
- Show the freshness stamp on the case record and on any screen where a decision depends on loaded
  data.
- A failed outbound action is shown as an exception, not as a silent failure.
- Use the error message ID from the message table; do not invent wording.

## 7. Accessibility and content

- WCAG 2.2 AA: keyboard operable, visible focus, labels, error identification, contrast, target size,
  no keyboard trap, consistent navigation.
- Every screen passes an automated scan and a keyboard check in SIT; no level A or AA failure.
- Thai and English labels; the Thai term comes from the business glossary and the content standard.
- Use the business glossary names; do not introduce a synonym in a label.
- Dates and amounts follow the bank format; Thai Buddhist era where the bank standard requires it.
- Error messages state what happened, what to do and the message ID; no blame and no personal data.

## 8. Frontend testing

| Level | What | Tool / environment |
|---|---|---|
| Component and unit | Components, hooks, formatting, validation | Developer tests in the pipeline |
| API contract | Request and response against OpenAPI | Pipeline |
| Functional automation | Every UI behaviour in the spec when `UI In Scope: YES` | Playwright MCP, `output/<RUN_ID>/functional-tests/attempt-<n>/` |
| Accessibility | Automated scan and keyboard check | SIT |
| Visual check | Screenshot against the screen specification and prototype | SIT / UAT |

The Functional Automation Test agent reads `UI In Scope` from `spec.md`. A frontend story with no
design evidence is blocked until the evidence is added; the current set has local design artifacts,
so `DESIGN_EVIDENCE_STATUS: AVAILABLE` with `SOURCE: LOCAL_ARTIFACTS` is the correct status.

## 9. Gaps and constraints

| ID | Gap | Impact |
|---|---|---|
| CTX-GAP-019 | No live Figma file or link. | Use the screen inventory, screen specifications, design system and prototype as design evidence; do not claim a Figma source. |
| CTX-GAP-021 | Thai labels and messages are proposed, not approved (DL10). | English can ship first; Thai is loaded as reference data when supplied. |
| CTX-GAP-025 | Some screens are first delivered in E8 (administration), while the underlying data can be loaded by file before then. | Do not specify an E8 screen for an E1 story; use the file-load path and record the screen as later. |
| CTX-GAP-013 | The partner portal depends on external access (DL03), first needed in E5. | Partner screens cannot be tested from outside the bank until the gateway is live. |
| CTX-GAP-020 | The front-end codebase is not in this workspace. | The context describes the intended stack and patterns; implementation must verify against the ACE repository. |

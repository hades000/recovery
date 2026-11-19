# Recovery Workbench — frontend context

**Context ID:** `CTX-FRONTEND-RWB-V2`
**Version:** 2.0, 16 November 2026
**Scope:** React front end of the ACE service, recovery module folder.
**Evidence labels:** `IMPLEMENTED`, `DOCUMENTED/REQUIRED`, `RECOMMENDED`, `N/A`.

## 1. Stack and host

| Item | Value | Evidence |
|---|---|---|
| Framework | React 18+ with TypeScript, Vite | `DOCUMENTED/REQUIRED` |
| Host | ACE front end, module folder `frontend/src/modules/recovery/` | `DOCUMENTED/REQUIRED` (ADR-006, D-RCV-10) |
| Route prefix | `/recovery/*` with one "Recovery" menu group in `AceLayout` | D-RCV-22 |
| Component library | ACE design system: Radix primitives, Tailwind tokens, shared `@/components/ui/**` | D-RCV-08 |
| State / data | TanStack Query for server state; local state for screen state | `DOCUMENTED/REQUIRED` |
| API client | Generated types from the API Specification v4; `@/api/schema` | D-RCV-39 |
| Forms | React Hook Form + Zod where the ACE pattern applies | `RECOMMENDED` |
| i18n | i18next, Thai and English, default Thai | D-RCV-13 |
| Accessibility | WCAG 2.2 AA | NFR v3 |
| Testing | Vitest + Testing Library, Playwright for functional flows | D-RCV-06/23 |

**Import rule for `frontend/src/modules/recovery/**`** (D-RCV-39, ESLint `no-restricted-imports`):
allowed outside the folder are `@/components/ui/**`, `@/lib/utils`, top-level `@/utils/*` except
`cfsc*`, `@/contexts/ApiClientContext` and `@/api/schema`. Inside the folder, `@/modules/recovery/**`
and `./…` are allowed; `../…` and the rest of `@/` are forbidden. FS-1.2 is replaced by this rule for
the recovery folder.

## 2. Screen inventory

The Screen Inventory v2 and Screen Specifications v1 list 53 screens. The screens in this baseline:

| Group | Screens | Story |
|---|---|---|
| Case work | Case list, queue view, case record v1, case record v1.1, case search | E1-002, E1-031, E1-023, E1-035, E1-033 |
| Case actions | Allocation, transfer, service-level and timer panel, rebalancing board | E1-020, E1-021, E1-028, E1-030 |
| Documents | Document hub, attach and search, OCR review queue, document checklist admin | E1-026, E1-054, E1-040 |
| Communications | Notice generation, template management | E1-052, E1-034 |
| Configuration | Parameter catalog, reference data workbench, feature flags | E1-042, E1-043, E1-047 |
| Access | Sign-in/role landing, role-to-permission matrix, access log, break-glass | E1-022, E1-037, E1-039 |
| Rules | Rule package list, upload, validation report, scenario results, approval, rollback | E1-073 |
| Platform | Temporal workflow health, task-queue backlog, job monitor | E1-070/071/056 |
| Reporting | Baseline measures, steering dashboard | E1-013, E2-009 |
| AI | Intake shadow review, extraction evaluation, deviation screening review, agent dashboard | E1-059/060/062/063 |

**Not in this baseline:** the Excel/SharePoint tracker screens (removed by D-RCV-35 U5), the inbound
load monitor (removed), and Epic 3–8 route screens.

## 3. Screen patterns

### 3.1 Case list and queue

- Server-side pagination, sorting and filters (queue, owner, stage, product, ageing bucket).
- Columns: case ID, customer (masked by role), product, stage, queue, owner, DPD, ageing, next action.
- Bulk selection for transfer/reassignment, with a reason.
- Empty state: "No cases match the filters" with a clear-filters action.
- Loading: skeleton rows; error: inline retry with the message ID.

### 3.2 Case record

- Header: case ID, status, stage, product, owner, queue, entry date, DPD, flags.
- Tabs: Summary, Accounts, Parties, Documents, History, Decisions, Treatments, Legal, Notes.
- Read-only in v1; actions appear only when the story enables them.
- History timeline is append-only and shows actor, time, action and decision-log reference.
- Documents tab: upload, classification, extraction status, review queue link.

### 3.3 Document and OCR screens

- Drag-and-drop upload with type selection; virus-scan state and progress.
- Low-confidence review queue: side-by-side document preview and extracted fields; confirm/correct.
- Field extraction shows confidence and source; corrections are logged.
- Retention class and legal hold are visible but only an authorised role can change them.

### 3.4 Configuration and rules

- Parameter catalog: list, filter by environment, edit value with effective date, approval state.
- Reference data: table code, rows, valid-from/valid-to, maker-checker.
- Rule package: upload XLS, compile result, scenario pass/fail, dry-run summary, approve/rollback.
- The author cannot approve; the approve action is hidden for the author role and refused server-side.

### 3.5 Platform and reporting

- Temporal health: namespace, task queues, open workflows, failures, backlog.
- Job monitor: job name, last run, status, next run, duration, link to run book.
- Reporting: baseline measures with definition, period, value and target; export.

## 4. Component and design rules

- Use ACE design-system components and tokens; no new colour, spacing or typography scale.
- One primary action per screen; destructive actions require confirmation and a reason.
- Every form field has a label, hint and error text; errors use the message ID and exact wording.
- Tables use the shared pagination, empty, loading and error patterns.
- Dialogs are focus-trapped; Escape closes; focus returns to the trigger.
- Keyboard navigation and visible focus are mandatory; no colour-only status.
- Thai and English strings are externalised; no string literal in a component.
- Dates use the bank timezone (Asia/Bangkok); date-only vs date-time is explicit.
- Currency and amounts use the Thai baht format and the product currency.
- Personal data is masked by role at the API; the UI never unmasks client-side.

## 5. States

| State | Behaviour |
|---|---|
| Loading | Skeleton or spinner; no layout jump |
| Empty | Clear explanation and the next action |
| Error | Message ID, short text, retry; no stack trace |
| Forbidden | 403 screen with the required role and a contact |
| Session expired | Re-authenticate and return to the same route |
| Optimistic update | Revert on failure with the message |
| Long-running job | Progress, cancel where allowed, resume link |

## 6. API integration

- All calls go through `ApiClientContext`; no direct `fetch` in a component.
- Generated types from the OpenAPI schema; no hand-written duplicate types.
- Query keys are stable and include the case ID, filters and page.
- Mutations invalidate the affected query and the case history.
- Errors are normalised to `{ code, messageId, message, fieldErrors }`.
- Idempotency key on create/move commands.

## 7. Accessibility and responsive behaviour

- WCAG 2.2 AA: contrast, labels, focus order, keyboard, screen-reader names.
- Minimum target 44×44 px for touch.
- Layout works at 1280 px and 1440 px desktop; tablet 1024 px for the case list and record.
- No horizontal scroll on the primary tables at 1280 px; secondary tables may scroll in their own box.
- Zoom to 200% without loss of function.

## 8. Testing

- Unit/component: Vitest + Testing Library, 80% on `src/modules/recovery/**`.
- Functional: Playwright for the critical journeys (case list → record → document → notice).
- Accessibility: axe scan in Playwright; no serious or critical issue.
- Visual: design-system tokens; no pixel snapshot of Thai text.
- Test data: synthetic only; never production data.

## 9. Gaps and constraints

| ID | Gap | Impact |
|---|---|---|
| `CTX-FE-GAP-01` | No live Figma; design evidence is the screen inventory and specifications | Specs record `DESIGN_EVIDENCE_STATUS: USER_STORY_SCREENSHOTS`; visual values approximate |
| `CTX-FE-GAP-02` | Thai labels are proposed | English canonical until DL10 |
| `CTX-FE-GAP-03` | Some Epic 2 screens are not specified at field level | Open at Epic 2 increment |
| `CTX-FE-GAP-04` | Removed tracker screens must not be built | Retirement register |

## 10. Required guidance for frontend agents

1. Put every file under `frontend/src/modules/recovery/`; respect the D-RCV-39 import allow-list.
2. Use ACE design-system components and tokens; do not introduce a second UI library.
3. Externalise every string; Thai and English resources both required.
4. Mask personal data at the API, not in the browser.
5. Add loading, empty, error, forbidden and expired-session states to every screen.
6. Add a Vitest test for the component logic and a Playwright flow for the journey.
7. Do not build a tracker, inbound-load monitor or removed screen.
8. Record design approximations and assumptions in the plan; do not ask a question in an automated run.

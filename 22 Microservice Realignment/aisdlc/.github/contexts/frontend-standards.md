# Recovery Workbench — frontend standards

**Context ID:** `CTX-FRONTEND-STANDARDS-V2`
**Version:** 2.0, 16 November 2026
**Applies to:** `frontend/src/modules/recovery/` in the ACE front end.

## FS-1 Structure and imports

- **FS-1.1** Every recovery screen, component, hook, type and test lives under
  `frontend/src/modules/recovery/`.
- **FS-1.2** Imports outside the folder are limited to `@/components/ui/**`, `@/lib/utils`, top-level
  `@/utils/*` except `cfsc*`, `@/contexts/ApiClientContext` and `@/api/schema`. Inside the folder,
  `@/modules/recovery/**` and `./…` are allowed. `../…` and every other `@/` import are forbidden.
  ESLint `no-restricted-imports` is scoped to the folder; a fixture test proves it fires.
- **FS-1.3** Routes live under `/recovery/*` and register in one "Recovery" menu group in `AceLayout`.
  The `App.tsx` and `AceLayout.tsx` edits are shared-file changes announced to the ACE team.
- **FS-1.4** No new UI library, icon set, state manager or HTTP client.

## FS-2 Design system and visual rules

- **FS-2.1** Use ACE design-system components and tokens. The Henka screen specification gives layout,
  content, labels and behaviour; it does not override the ACE component look.
- **FS-2.2** One primary action per screen; destructive actions need a confirmation and a reason.
- **FS-2.3** Thai and English through i18next; default Thai; no string literal in a component.
- **FS-2.4** Use the bank timezone (Asia/Bangkok). Date-only and date-time are explicit.
- **FS-2.5** Amounts use the Thai baht format and the product currency; no float arithmetic in the UI.
- **FS-2.6** No pixel-perfect copy of a prototype; use tokens and the nearest design-system component.

## FS-3 Screen behaviour

- **FS-3.1** Every screen has loading, empty, error, forbidden and expired-session states.
- **FS-3.2** Tables use the shared pagination, empty, loading and error patterns; server-side paging.
- **FS-3.3** Forms validate on blur and on submit; errors use the message ID and exact wording.
- **FS-3.4** Dialogs trap focus, close on Escape and return focus to the trigger.
- **FS-3.5** Long-running work shows progress, a cancel where allowed, and a resume link.
- **FS-3.6** Optimistic updates revert on failure with the message.
- **FS-3.7** No client-side unmasking of personal data; the API masks by role.

## FS-4 API integration

- **FS-4.1** All calls go through `ApiClientContext`; no direct `fetch` in a component.
- **FS-4.2** Use generated types from `@/api/schema`; no duplicate hand-written type.
- **FS-4.3** Query keys are stable and include case ID, filters and page.
- **FS-4.4** A mutation invalidates the affected query and the case history.
- **FS-4.5** Normalise errors to `{ code, messageId, message, fieldErrors }`.
- **FS-4.6** Send an idempotency key on create/move commands.

## FS-5 Accessibility and responsiveness

- **FS-5.1** WCAG 2.2 AA: contrast, labels, focus order, keyboard, screen-reader names.
- **FS-5.2** Minimum touch target 44×44 px.
- **FS-5.3** Desktop 1280/1440 px; tablet 1024 px for case list and record.
- **FS-5.4** No horizontal scroll on primary tables at 1280 px; secondary tables scroll in their own box.
- **FS-5.5** Zoom to 200% without loss of function.
- **FS-5.6** No colour-only status; pair colour with text or an icon.

## FS-6 Testing and quality

- **FS-6.1** Vitest + Testing Library for components and hooks; 80% on `src/modules/recovery/**`.
- **FS-6.2** Playwright for the critical journeys; axe scan with no serious or critical issue.
- **FS-6.3** No snapshot of Thai text; assert the message ID and the rendered label key.
- **FS-6.4** Test data is synthetic; no production data.
- **FS-6.5** A change with no test is not complete.

## FS-7 Removed scope

- **FS-7.1** Do not build an Excel/SharePoint tracker screen, an inbound-load monitor or a removed
  data-quality screen. D-RCV-35 removed them; see `docs/retirements/story-retirement-register.md`.
- **FS-7.2** Do not build a `payment_match_rule` admin screen; payment matching is a Drools package.

## FS-8 N/A and evidence scope

- N/A — no mobile native app; the Workbench is a responsive web module.
- N/A — no live Figma; design evidence is the screen inventory and specifications.

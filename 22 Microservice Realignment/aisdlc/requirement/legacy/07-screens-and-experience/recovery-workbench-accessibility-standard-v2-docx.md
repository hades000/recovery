<!-- source: 07 Screens and experience/Recovery Workbench Accessibility Standard v2.docx -->
<!-- converted: 2026-11-16 from DOCX -->

> **Source:** `07 Screens and experience/Recovery Workbench Accessibility Standard v2.docx`  
> **Converted from:** DOCX

Recovery Workbench

Accessibility standard

SCB Collections and Recovery. Henka Group, 28 October 2026

| Item | Detail |
|---|---|
| Document | Recovery Workbench accessibility standard |
| Version | 1 |
| Date | 28 October 2026 |
| Prepared by | Henka Group |
| Structure | WCAG 2.2 level AA |

# 1. The level

Every Workbench and partner portal screen meets WCAG 2.2 level AA. The design system components meet it by construction; each screen is checked before release.

# 2. Rules that follow from it

| Area | Rule | WCAG |
|---|---|---|
| Contrast | Text 4.5 to 1 against its background; large text and controls 3 to 1. The design tokens meet this | 1.4.3, 1.4.11 |
| Color | Status shown by text and badge, never by color alone | 1.4.1 |
| Keyboard | Every action reachable and usable by keyboard, in a logical order, with no trap | 2.1.1, 2.1.2, 2.4.3 |
| Focus | A visible 2 px focus ring on every control; focus never hidden behind sticky headers | 2.4.7, 2.4.11 |
| Target size | Click targets at least 24 by 24 px | 2.5.8 |
| Labels | Every field has a visible label tied to it; required fields marked in text | 1.3.1, 3.3.2 |
| Errors | Errors named in text next to the field and summarized at the top; focus moves to the summary | 3.3.1, 3.3.3 |
| Headings | One screen title; panels use headings in order | 1.3.1, 2.4.6 |
| Tables | Header cells marked; sortable columns announce their state | 1.3.1 |
| Dialogs | Focus moves into the dialog and returns on close; Escape closes | 2.4.3 |
| Timing | Session timeout warns two minutes before and lets the user extend | 2.2.1 |
| Zoom | Usable at 200 percent zoom and at 320 px width without loss | 1.4.4, 1.4.10 |
| Language | Page language set; Thai text marked lang=th | 3.1.1, 3.1.2 |
| Status messages | Toasts and banners announced to screen readers | 4.1.3 |
| Dragging | No action needs dragging | 2.5.7 |
| Help | Help in the same place on every screen | 3.2.6 |
| Authentication | Sign-in through Entra ID with no cognitive test | 3.3.8 |

# 3. How each screen is checked

| Check | When | Who |
|---|---|---|
| Automated scan of every screen | Every pull request that changes a screen | Pipeline (RWB-TE-010) |
| Keyboard walk-through | Before SIT exit | QA engineer |
| Screen reader check of the main screens | Before the first release of each screen | QA engineer |
| Zoom and narrow width | Before SIT exit | QA engineer |

A screen with an open level A or AA failure does not pass the definition of done.

<!-- source: 07 Screens and experience/Recovery Workbench Design System and Component Library v1.html -->
<!-- converted: 2026-11-04 from HTML -->

> **Source:** `07 Screens and experience/Recovery Workbench Design System and Component Library v1.html`  
> **Converted from:** HTML

Recovery Workbench design system**Built on**React on Vite with Radix primitives in the ACE front end; these tokens and components are the recovery screens' layer**Source**The ACE component library where one exists; this set fills the gaps until the bank design system is confirmed (DL08)**Accessibility**Every component meets WCAG 2.2 AA: contrast, focus, keyboard and target size**Language**Thai and English for every label; layouts allow Thai text to run 30 percent longer

## Rules

| Rule | Detail |
|---|---|
| Color | Purple marks primary actions and active navigation only; tables have a colored header and white body rows |
| Status | Status is shown by text and a badge, never by color alone |
| Type | Five sizes: 12, 14, 16, 20, 24 px |
| Spacing | A 4 px scale; panels 16 px apart |
| Density | Tables at 14 px with 7 px row padding; work screens show 25 rows a page |
| Icons | Only with a text label, except close and expand |

**color.primary**#4E297FPrimary actions, active navigation, headings**color.primary.dark**#201135Header bar**color.primary.hover**#3E1F66Primary button hover**color.surface**#FFFFFFPage and panel background**color.surface.alt**#F6F4FAPage background behind panels**color.header**#DCD3EBTable header fill**color.ink**#1F1F1FBody text**color.muted**#595959Secondary text, helper text**color.rule**#C8C8C8Borders and table rules**color.focus**#2459A8Focus ring**color.info**#2459A8Information banners**color.success**#1E7B4DConfirmations**color.warning**#9A5200Warnings, timers near their end**color.danger**#B42318Errors, breached service levels**color.accent**#FF9900Active tab underline on dark backgrounds only

## All tokens

| Token | Value | Used for |
|---|---|---|
| color.primary | #4E297F | Primary actions, active navigation, headings |
| color.primary.dark | #201135 | Header bar |
| color.primary.hover | #3E1F66 | Primary button hover |
| color.surface | #FFFFFF | Page and panel background |
| color.surface.alt | #F6F4FA | Page background behind panels |
| color.header | #DCD3EB | Table header fill |
| color.ink | #1F1F1F | Body text |
| color.muted | #595959 | Secondary text, helper text |
| color.rule | #C8C8C8 | Borders and table rules |
| color.focus | #2459A8 | Focus ring |
| color.info | #2459A8 | Information banners |
| color.success | #1E7B4D | Confirmations |
| color.warning | #9A5200 | Warnings, timers near their end |
| color.danger | #B42318 | Errors, breached service levels |
| color.accent | #FF9900 | Active tab underline on dark backgrounds only |
| space.1 | 4px | Inside small controls |
| space.2 | 8px | Between related items |
| space.3 | 12px | Inside panels |
| space.4 | 16px | Between panels; page gutter |
| space.5 | 24px | Between sections |
| space.6 | 32px | Page top |
| radius | 4px | Controls and panels |
| font.family | Aptos, Segoe UI, Noto Sans Thai, sans-serif | All text |
| font.size.xs | 12px | Table meta, badges |
| font.size.sm | 14px | Body, tables, controls |
| font.size.md | 16px | Panel titles |
| font.size.lg | 20px | Screen titles |
| font.size.xl | 24px | Page title in the header |
| line.height | 1.45 | All text |
| control.height | 36px | Buttons, inputs, selects |
| target.min | 24px | Smallest click target (WCAG 2.2 2.5.8) |

## Buttons

One primary button per screen area. Destructive actions use the danger style and ask for a reason.

## Fields

Offer amount (THB)

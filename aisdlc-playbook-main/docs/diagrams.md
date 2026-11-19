---
id: diagrams
title: Diagrams
description: "The diagrams in this playbook are draw.io files. Shapes in them link to the pages or sections they describe, so you can click a stage, a gate or an agent and land on its explanation."
sidebar_label: Diagrams
---

The diagrams in this playbook are **draw.io** files. Shapes in them link to the pages or sections
they describe, so you can click a stage, a gate or an agent and land on its explanation.

| Diagram | Shows | Used on | Source | Rendered |
|---|---|---|---|---|
| End-to-end flow | The nine stages from Discover / Context to Operate and Learn, the human approval gate after each, and the agents that support each stage | [2.1 End-to-end flow](/overview/end-to-end-flow) | [`end-to-end-flow.drawio`](/diagrams/end-to-end-flow.drawio) | [`end-to-end-flow.svg`](/diagrams/end-to-end-flow.svg) |
| Lifecycle paths | The eleven-phase standard lifecycle with the Greenfield, Brownfield and Modernisation treatment of each phase | [2.4 Tailoring](/overview/tailoring), [3.1 Common execution rule](/paths/overview) | [`lifecycle-paths.drawio`](/diagrams/lifecycle-paths.drawio) | [`lifecycle-paths.svg`](/diagrams/lifecycle-paths.svg) |
| Agent chain | The agents grouped by lifecycle group, with the human reviewer of each | [1.3 Lifecycle](/introduction/lifecycle), [2.5 Select agents](/overview/select-agents), [Catalogue](/agents/catalogue) | [`agent-chain.drawio`](/diagrams/agent-chain.drawio) | [`agent-chain.svg`](/diagrams/agent-chain.svg) |
| How one stage runs | Squad, agent, toolkit files and gate as swimlanes for a single stage | [4. Getting started](/getting-started/overview) | [`stage-run.drawio`](/diagrams/stage-run.drawio) | [`stage-run.svg`](/diagrams/stage-run.svg) |

## Editing

1. Open `aisdlc-playbook/diagrams/<name>.drawio` in the draw.io desktop app or app.diagrams.net.
   The exported SVG under `static/diagrams/` also opens in draw.io because the diagram is embedded
   in it; the `.drawio` file is the source we keep.
2. To give a shape a link: select it, **Edit → Edit Link** (or the link icon), and enter a site path
   such as `/overview/tailoring` or `/agents/spec-clarify`. Keep paths absolute; the export makes
   them open in the page rather than in a new tab.
3. Re-export from `aisdlc-playbook/` with `npm run diagrams`. The script uses the draw.io desktop
   app when it is installed and otherwise falls back to the bundled renderer
   (`diagrams/render.mjs`), which understands the shapes used here (rounded boxes, swimlanes, text,
   straight and orthogonal connectors). It writes `static/diagrams/<name>.svg` with the diagram
   embedded and copies the `.drawio` next to it.
4. Commit both the `.drawio` and the `.svg`.

## Embedding in a page

```mdx
<object type="image/svg+xml" data="/diagrams/end-to-end-flow.svg" className="diagram" aria-label="…">
  Fallback text.
</object>
```

An `<img>` would drop the links; `<object>` keeps them. If the site is published under a sub-path,
change `baseUrl` in `docusaurus.config.js` and prefix the links in the diagrams.

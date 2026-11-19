---
title: SCBX AI-First SDLC Playbook (site)
description: "Docusaurus site for the SCBX AI-First SDLC Playbook with clickable draw.io diagrams; how to run, build and edit it"
---

The interactive playbook for product squads delivering with Agentic PDLC, built from the
*SCBx AI PDLC Product Squad Playbook* draft (sections 1 to 5 and Appendix A). The agents, rules,
templates and MCP servers it refers to live in the toolkit one folder up (`../aisdlc-toolkit`).

* **Docs** are Markdown under `docs/`; the sidebar is `sidebars.js`.
* **Diagrams** are draw.io files under `diagrams/` (the editable source). `npm run diagrams` exports
  them to `static/diagrams/*.svg` with the diagram embedded, so the SVG itself can be opened in
  draw.io, and with the hyperlinks kept. Shapes link to playbook pages and sections. Edit the
  `.drawio`, re-export, commit both.
* **Site** is Docusaurus 3.

```bash
cd ap2510-aisdlc/aisdlc-playbook
npm install
npm run build      # static site in build/
npm run diagrams   # re-export the SVGs after editing a .drawio
npm start          # http://localhost:3000
```

`npm run diagrams` uses the draw.io desktop app when it is installed and otherwise the bundled
renderer in `diagrams/render.mjs`, which covers the shapes used by these diagrams.

To publish under a sub-path, set `url` and `baseUrl` in `docusaurus.config.js` and prefix the links
in the diagrams (they are absolute site paths such as `/overview/tailoring`).

## Structure

```text
docs/
├── intro.md                 About this playbook
├── introduction/            1. What Agentic PDLC means, four changes, the lifecycle
├── overview/                2. End-to-end flow, project types, baseline, tailoring, select agents
├── paths/                   3. Greenfield, brownfield, modernisation, hybrid
├── getting-started/         4. Environment, Claude Code runtime, BRD, PRD, backlog, specify, plan, implement, API and functional tests
├── roles/                   5. Squad roles and role evolution
├── agents/                  Appendix A. Agent catalogue
├── toolkit.md               The toolkit and the standard repository structure
└── diagrams.md              How the diagrams are made and edited
diagrams/                    *.drawio sources, export.sh, render.mjs
static/diagrams/             exported *.svg and copies of the *.drawio
```

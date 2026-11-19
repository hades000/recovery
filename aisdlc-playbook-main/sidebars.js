// @ts-check
/** @type {import('@docusaurus/plugin-content-docs').SidebarsConfig} */
const sidebars = {
  playbook: [
    'intro',
    {
      type: 'category',
      label: '1. Introduction to Agentic PDLC',
      link: { type: 'doc', id: 'introduction/what-is-agentic-pdlc' },
      items: ['introduction/four-changes', 'introduction/lifecycle'],
    },
    {
      type: 'category',
      label: '2. Overview of Agentic PDLC',
      link: { type: 'doc', id: 'overview/end-to-end-flow' },
      items: ['overview/project-types', 'overview/baseline', 'overview/tailoring', 'overview/select-agents'],
    },
    {
      type: 'category',
      label: '3. Execute in different project types',
      link: { type: 'doc', id: 'paths/overview' },
      items: ['paths/greenfield', 'paths/brownfield', 'paths/modernisation', 'paths/hybrid'],
    },
    {
      type: 'category',
      label: '4. Pilot pre-initiation and getting started',
      link: { type: 'doc', id: 'getting-started/overview' },
      items: [
        'getting-started/environment',
        'getting-started/claude-code',
        'getting-started/brd',
        'getting-started/prd',
        'getting-started/backlog',
        'getting-started/specify',
        'getting-started/plan',
        'getting-started/implement',
        'getting-started/api-tests',
        'getting-started/functional-tests',
      ],
    },
    {
      type: 'category',
      label: '5. Product squad roles',
      link: { type: 'doc', id: 'roles/squad-roles' },
      items: ['roles/role-evolution'],
    },
    {
      type: 'category',
      label: 'Appendix A. Agent catalogue',
      link: { type: 'doc', id: 'agents/catalogue' },
      items: [
        'agents/context-builder',
        'agents/brd-builder',
        'agents/prd-builder',
        'agents/backlog-manager',
        'agents/spec-clarify',
        'agents/task-planner',
        'agents/task-implementor',
        'agents/api-testing',
        'agents/functional-testing',
        'agents/azure-deploy',
        'agents/supporting-agents',
      ],
    },
    'toolkit',
    'diagrams',
  ],
};
export default sidebars;

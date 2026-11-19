// @ts-check
// SCBX AI-First SDLC Playbook. Serve locally with `npm start`, build with `npm run build`.
// If the site is published under a sub-path, change `url` and `baseUrl` and re-export the diagrams
// (their links are absolute site paths: see diagrams/export.sh).

/** @type {import('@docusaurus/types').Config} */
const config = {
  title: 'SCBX AI-First SDLC Playbook',
  tagline: 'How product squads deliver with agents across the lifecycle, with people accountable at every gate',
  favicon: 'img/favicon.svg',
  url: 'https://aisdlc-playbook.scbx.internal',
  baseUrl: '/',
  onBrokenLinks: 'throw',
  onBrokenAnchors: 'throw',
  markdown: { hooks: { onBrokenMarkdownLinks: 'throw' } },
  i18n: { defaultLocale: 'en', locales: ['en'] },
  presets: [
    [
      'classic',
      /** @type {import('@docusaurus/preset-classic').Options} */
      ({
        docs: {
          routeBasePath: '/',
          sidebarPath: './sidebars.js',
          editUrl: undefined,
          showLastUpdateTime: false,
        },
        blog: false,
        theme: { customCss: './src/css/custom.css' },
      }),
    ],
  ],
  themeConfig:
    /** @type {import('@docusaurus/preset-classic').ThemeConfig} */
    ({
      colorMode: { respectPrefersColorScheme: true },
      docs: { sidebar: { hideable: true, autoCollapseCategories: false } },
      navbar: {
        title: 'SCBX AI-First SDLC Playbook',
        items: [
          { to: '/', label: 'Playbook', position: 'left' },
          { to: '/overview/end-to-end-flow', label: 'Lifecycle', position: 'left' },
          { to: '/paths/overview', label: 'Project paths', position: 'left' },
          { to: '/getting-started/overview', label: 'Getting started', position: 'left' },
          { to: '/agents/catalogue', label: 'Agent catalogue', position: 'left' },
          { to: '/toolkit', label: 'Toolkit', position: 'right' },
          { to: '/diagrams', label: 'Diagrams', position: 'right' },
        ],
      },
      footer: {
        style: 'dark',
        links: [
          {
            title: 'Playbook',
            items: [
              { label: 'Introduction', to: '/introduction/what-is-agentic-pdlc' },
              { label: 'Lifecycle overview', to: '/overview/end-to-end-flow' },
              { label: 'Roles', to: '/roles/squad-roles' },
            ],
          },
          {
            title: 'Delivery',
            items: [
              { label: 'Getting started', to: '/getting-started/overview' },
              { label: 'Agent catalogue', to: '/agents/catalogue' },
              { label: 'Toolkit', to: '/toolkit' },
            ],
          },
        ],
        copyright: `SCBX AI PDLC Product Squad Playbook. Draft, October 2026. Living document: sections 6 to 9 follow in later drafts.`,
      },
      prism: { additionalLanguages: ['bash', 'json', 'markdown'] },
      tableOfContents: { minHeadingLevel: 2, maxHeadingLevel: 4 },
    }),
};

export default config;

// Headless smoke test of the hub script: stub enough DOM to boot and render every tab.
const fs = require('fs');
const path = require('path');

function el() {
  return {
    innerHTML: '', textContent: '', scrollTop: 0, value: '', dataset: {},
    classList: { toggle() { return false; }, add() {}, remove() {}, contains() { return false; } },
    style: {}, tagName: 'DIV',
    addEventListener() {}, setAttribute() {}, getAttribute() { return null; },
    querySelector() { return el(); }, querySelectorAll() { return []; },
    closest() { return null; }, focus() {}, setSelectionRange() {}, scrollIntoView() {},
    appendChild() {}, onclick: null,
  };
}

const payload = fs.readFileSync(path.join(__dirname, 'payload.b64'), 'utf8').trim();
const nodes = {};
global.document = {
  getElementById(id) { if (!nodes[id]) nodes[id] = el(); if (id === 'payload') nodes[id].textContent = payload; return nodes[id]; },
  querySelector() { return el(); },
  querySelectorAll() { return []; },
  body: el(), documentElement: el(), addEventListener() {},
};
global.window = {};
global.matchMedia = () => ({ matches: false });
global.innerWidth = 1400;
global.CSS = { escape: s => String(s) };
global.atob = s => Buffer.from(s, 'base64').toString('binary');

const js = fs.readFileSync(path.join(__dirname, 'v15.js'), 'utf8').replace(/\nboot\(\);\s*$/, '\n');

const test = `
(async () => {
  await boot();
  console.log('boot ok: docs', M.docs.length, 'ids', Object.keys(M.ids).length, 'stories', STORIES.length, 'setfiles', M.setfiles.length);
  const out = {};
  const cases = [['bodyStart', () => bodyStart()], ['bodyPlan', () => bodyPlan()], ['bodyDocs', () => bodyDocs(M.folders[0])],
    ['bodyFiles', () => bodyFiles()], ['bodyIds', () => bodyIds()], ['bodyTerms', () => bodyTerms()],
    ['set-all', () => { sideSet(); bodySet(); }], ['set-one', () => { sideSet(M.setfolders[0]); bodySet(M.setfolders[0]); }],
    ['bodyGroup', () => bodyGroup(GROUPS[0].id)], ['sideWork', () => sideWork()],
    ['openDoc', () => openDoc(0)], ['sideDocs', () => sideDocs()], ['sideFiles', () => sideFiles()],
    ['sideIds', () => sideIds()], ['sideDec', () => sideDec()]];
  for (const [name, fn] of cases) { try { fn(); out[name] = 'ok'; } catch (e) { out[name] = 'ERR ' + e.message; } }
  console.log(out);
  const hubDoc = M.docs.findIndex(d => d.file === 'Recovery Workbench Project Hub v14.html');
  const fsd = M.docs.findIndex(d => d.file.includes('FSD P3 Case and workflow v2.md'));
  console.log('hub nf', M.docs[hubDoc].nf, '| fsd nf', M.docs[fsd].nf);
  let nf = 0; M.docs.forEach(d => { if (d.nf) nf++; });
  console.log('docs with nf', nf, 'folders', M.setfolders.length);
})();
`;
eval(js + test);

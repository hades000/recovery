const fs = require('fs');
const path = require('path');
function el() {
  return {
    innerHTML: '', textContent: '', scrollTop: 0, value: '', dataset: {},
    classList: { toggle() { return false; }, add() {}, remove() {}, contains() { return false; } },
    style: {}, tagName: 'DIV', addEventListener() {}, setAttribute() {}, getAttribute() { return null; },
    querySelector() { return el(); }, querySelectorAll() { return []; }, closest() { return null; },
    focus() {}, setSelectionRange() {}, scrollIntoView() {}, appendChild() {}, onclick: null,
  };
}
const payload = fs.readFileSync(path.join(__dirname, 'payload.b64'), 'utf8').trim();
const nodes = {};
const bodyEl = el();
global.document = {
  getElementById(id) { if (!nodes[id]) nodes[id] = el(); if (id === 'payload') nodes[id].textContent = payload; return nodes[id]; },
  querySelector(sel) { return sel === '.body' ? bodyEl : el(); },
  querySelectorAll() { return []; }, body: el(), documentElement: el(), addEventListener() {},
};
global.window = {}; global.matchMedia = () => ({ matches: false }); global.innerWidth = 1400;
global.CSS = { escape: s => String(s) }; global.atob = s => Buffer.from(s, 'base64').toString('binary');
const js = fs.readFileSync(path.join(__dirname, 'v15.js'), 'utf8').replace(/\nboot\(\);\s*$/, '\n');
const test = `
(async () => {
  await boot();
  bodyStart();
  console.log('=== bodyStart ==='); console.log(document.querySelector('.body').innerHTML.slice(0, 2200));
  bodySet();
  const h = document.querySelector('.body').innerHTML;
  console.log('=== bodySet head ==='); console.log(h.slice(0, 1400));
  console.log('=== rows ===', (h.match(/<tr>/g)||[]).length);
  openDoc(M.docs.findIndex(d => d.file === 'Recovery Workbench Error and Message Standard v3.docx'));
  console.log('=== openDoc lede ==='); console.log(document.querySelector('.body').innerHTML.slice(0, 600));
})();
`;
eval(js + test);

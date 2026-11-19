const fs = require('fs');
const vm = require('vm');
const path = process.argv[2];
const html = fs.readFileSync(path, 'utf8');
// first <script> block holding the model constants
const start = html.indexOf('<script>const TH=');
if (start < 0) throw new Error('model script not found');
const end = html.indexOf('</script>', start);
let code = html.slice(start + 8, end);
code = code.replace(/boot\(\);\s*$/, '');
code += '\n;globalThis.__out={RES,DEC,NOTES,SIMPLE,TH,TERMS};';
const sandbox = { console };
vm.createContext(sandbox);
vm.runInContext(code, sandbox, { timeout: 20000 });
const { RES, DEC, NOTES, SIMPLE, TH, TERMS } = sandbox.__out;
console.log('RES', Object.keys(RES), 'tables', Object.keys(RES.tables).length,
  'endpoints', Object.keys(RES.endpoints).length, 'concepts', Object.keys(RES.concepts).length,
  'columns', RES.columns ? Object.keys(RES.columns).length : 0);
console.log('table sample', JSON.stringify(RES.tables[Object.keys(RES.tables)[0]]).slice(0, 300));
console.log('endpoint sample', JSON.stringify(Object.entries(RES.endpoints).slice(0, 2)).slice(0, 400));
console.log('concept sample', JSON.stringify(Object.entries(RES.concepts).slice(0, 3)).slice(0, 400));
console.log('DEC', Object.keys(DEC), Object.fromEntries(Object.entries(DEC).map(([k, v]) => [k, Array.isArray(v) ? v.length : typeof v])));
console.log('DEC open', JSON.stringify(DEC.open[0]).slice(0, 400));
console.log('DEC taken', JSON.stringify((DEC.taken || [])[0]).slice(0, 300));
console.log('NOTES', Object.keys(NOTES).length, JSON.stringify(Object.entries(NOTES)[0]).slice(0, 300));
console.log('SIMPLE', Object.keys(SIMPLE).length);
console.log('TH', Object.keys(TH).length, 'TERMS', TERMS.terms.length);

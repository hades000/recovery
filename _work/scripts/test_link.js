const fs = require('fs');
const vm = require('vm');
const path = process.argv[2];
const html = fs.readFileSync(path, 'utf8');
const start = html.indexOf('const TH=');
let end = html.indexOf('</script>', start);
let code = html.slice(start, end).replace(/boot\(\);\s*$/, '');
code += "\n;M={ids:{'RW-TRIBE':{k:'RW'},'RWB-TE-001':{k:'STORY'}},docs:[]};globalThis.__link=link;";
const sandbox = { console, document: { getElementById: () => null } };
vm.createContext(sandbox);
try { vm.runInContext(code, sandbox, { timeout: 20000 }); } catch (e) { console.log('eval err', e.message); }
const link = sandbox.__link;
console.log(link('As a **recovery developer (RW-TRIBE)**, I want **the recovery module** so that **one copy**.'));
console.log(link('The boundary is enforced twice: by boundary rule BND-6 in RWB-TE-001, which fails the build.'));

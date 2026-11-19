const fs = require('fs');
const path = process.argv[3];
const html = fs.readFileSync(path, 'utf8');
function grab(name) {
  const m = html.match(new RegExp('const ' + name + '=(\\{.*\\});\\r?\\n'));
  if (!m) return null;
  return eval('(' + m[1] + ')');
}
const RES = grab('RES'), DEC = grab('DEC'), NOTES = grab('NOTES'), SIMPLE = grab('SIMPLE'), TH = grab('TH');
console.log('RES keys', Object.keys(RES));
for (const k of Object.keys(RES)) {
  const v = RES[k];
  console.log(' ', k, Array.isArray(v) ? 'array ' + v.length : typeof v === 'object' ? 'obj ' + Object.keys(v).length : typeof v);
}
console.log('table sample', JSON.stringify(RES.tables[Object.keys(RES.tables)[0]]).slice(0, 400));
console.log('endpoint sample', JSON.stringify(Object.entries(RES.endpoints).slice(0, 2)));
console.log('concept sample', JSON.stringify(Object.entries(RES.concepts).slice(0, 3)));
console.log('DEC keys', Object.keys(DEC), Object.fromEntries(Object.entries(DEC).map(([k, v]) => [k, Array.isArray(v) ? v.length : typeof v])));
console.log('DEC open sample', JSON.stringify(DEC.open.slice(0, 2)));
console.log('DEC taken sample', JSON.stringify((DEC.taken || []).slice(0, 2)));
console.log('NOTES stories', Object.keys(NOTES).length, 'sample keys', Object.keys(NOTES).slice(0, 4));
console.log('note entry', JSON.stringify(NOTES[Object.keys(NOTES)[0]]).slice(0, 500));
console.log('SIMPLE stories', Object.keys(SIMPLE).length, 'sample', JSON.stringify(SIMPLE[Object.keys(SIMPLE)[0]]).slice(0, 400));
console.log('TH keys', Object.keys(TH).length);

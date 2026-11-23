import re, json, base64, zlib
p = r'12 Project communication\Recovery Workbench Project Hub v15.html'
s = open(p, encoding='utf-8').read()
m = re.search(r'<script type="application/octet-stream" id="payload">([^<]*)</script>', s)
M = json.loads(zlib.decompress(base64.b64decode(m.group(1)), 16 + zlib.MAX_WBITS).decode('utf-8'))
folders = sorted({x['file'].rsplit('/', 1)[0] if '/' in x['file'] else '(root)' for x in M['setfiles']})
print('setfiles', len(M['setfiles']))
print('folders', len(folders))
print('nf', sum(1 for d in M['docs'] if d.get('nf')))
print('docs', len(M['docs']), 'ids', len(M['ids']), 'files', len(M['files']))
print('missing on disk in setfiles:', [x['file'] for x in M['setfiles'] if not __import__('pathlib').Path(x['file']).exists()])

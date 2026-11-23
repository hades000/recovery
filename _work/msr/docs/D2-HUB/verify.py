import re, json, base64, zlib
p = r'12 Project communication\Recovery Workbench Project Hub v15.html'
s = open(p, encoding='utf-8').read()
m = re.search(r'<script type="application/octet-stream" id="payload">([^<]*)</script>', s)
M = json.loads(zlib.decompress(base64.b64decode(m.group(1)), 16 + zlib.MAX_WBITS).decode('utf-8'))
for d in M['docs']:
    if d['file'] in ('Recovery Workbench Project Hub v14.html',
                     'Recovery Workbench Document Index v11.md',
                     'Recovery Workbench Error and Message Standard v3.docx',
                     'Recovery Workbench Functional Specifications by Module v4.zip / Recovery Workbench FSD P3 Case and workflow v2.md'):
        print(d['folder'], '|', d['file'], '->', d.get('nf'))
print('n nf', sum(1 for d in M['docs'] if d.get('nf')))
print('setfiles folders', len({x['file'].rsplit('/',1)[0] for x in M['setfiles']}))
print([x for x in M['setfiles'] if 'Project Hub' in x['file']])
for needle in ['Document set v15', 'SCB Collections and Recovery. Henka Group, 22 November 2026.', '(C) Siam Commercial Bank and Henka Pte Ltd',
               'D-RCV-60 microservice realignment, T3 Code / OpenCode / DeepSeek v4.1 Flash', 'data-t="__set"', 'function bodySet',
               'height:calc(100% - 116px)', 'top:116px']:
    print(repr(needle), s.count(needle))

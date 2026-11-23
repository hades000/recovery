import re, base64, json
p = r'12 Project communication\Recovery Workbench Project Hub v15.html'
s = open(p, encoding='utf-8').read()
m = re.search(r'<script type="application/octet-stream" id="payload">([^<]*)</script>', s)
open(r'_work\msr\docs\D2-HUB\payload.b64', 'w').write(m.group(1))
print('payload b64 written', len(m.group(1)))

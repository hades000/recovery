import re
p = r'12 Project communication\Recovery Workbench Project Hub v15.html'
s = open(p, encoding='utf-8').read()
scripts = re.findall(r'<script(?![^>]*application/octet-stream)[^>]*>(.*?)</script>', s, re.S)
print('inline scripts', len(scripts), [len(x) for x in scripts])
open(r'_work\msr\docs\D2-HUB\v15.js', 'w', encoding='utf-8').write(scripts[0])

import re
p = r'06 Data/Recovery Workbench Entity Relationship Diagram v3.html'
s = open(p, encoding='utf-8').read()
i = s.find('id="dp01"')
j = s.find('</section>', i)
seg = s[i:j]
print(len(seg))
# strip the svg
k = seg.find('</svg>')
print('--- after svg ---')
print(seg[k:k+3000])
print('--- data attrs in nav/scripts? ---')
print(s[-1200:])

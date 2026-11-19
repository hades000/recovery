import re
s = open(r'06 Data/Recovery Workbench Entity Relationship Diagram v4.html', encoding='utf-8').read()
st = re.search(r'<style>(.*?)</style>', s, re.S).group(1)
print(st[:600])
print('---- header rules ----')
for m in re.finditer(r'[^{}]*header[^{}]*\{[^}]*\}', st):
    print(m.group(0))
print('---- first 300 after body ----')
print(s[s.find('<body>'):s.find('<body>')+300])

import io, os, sys

ROOT = r'C:\Users\SahilMore\Downloads\Recovery Workbench SharePoint Set v14'
HUB = os.path.join(ROOT, '14 Story Updates', 'Recovery Workbench Project Hub v16.html')
html = io.open(HUB, encoding='utf-8').read()
js = sys.argv[1]
out = sys.argv[2]
inject = '<script>setTimeout(function(){try{%s}catch(e){document.body.innerHTML="<pre>"+e.stack+"</pre>";}},4000);</script>' % js
html = html.replace('</body>', inject + '\n</body>')
io.open(out, 'w', encoding='utf-8').write(html)
print('wrote', out)

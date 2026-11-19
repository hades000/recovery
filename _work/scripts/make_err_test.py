import io, sys

ROOT = r'C:\Users\SahilMore\Downloads\Recovery Workbench SharePoint Set v14'
src = ROOT + r'\14 Story Updates\Recovery Workbench Project Hub v16.html'
out = r'C:\Users\SahilMore\AppData\Local\Temp\opencode\test_err.html'
html = io.open(src, encoding='utf-8').read()
head = ('<script>window.__errs=[];window.onerror=function(m,s,l,c,e){window.__errs.push(String(m)+" @"+l);};'
        'setTimeout(function(){document.title="ERRS:"+window.__errs.length+(window.__errs.length?" "+window.__errs.join(" | "):"");},12000);</script>')
html = html.replace('<head>', '<head>' + head, 1)
io.open(out, 'w', encoding='utf-8').write(html)
print('wrote', out)

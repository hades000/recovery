import re, os
p = r'06 Data/Recovery Workbench Entity Relationship Diagram v4.html'
s = open(p, encoding='utf-8').read()
probe = """<script>
setTimeout(function(){
 function r(el){ if(!el) return null; var b=el.getBoundingClientRect(); var c=getComputedStyle(el);
  return [Math.round(b.top),Math.round(b.height),c.display,c.visibility,c.color,c.backgroundColor]; }
 document.title=JSON.stringify({scrollY:window.scrollY, header:r(document.querySelector('body>header')),
   h1:r(document.querySelector('header h1')), h2:r(document.querySelector('#overview h2')),
   nav:r(document.querySelector('nav')), p:r(document.querySelector('#overview p'))});
},300);
</script></body>"""
s = s.replace('</body>', probe, 1)
open(r'C:\Users\SahilMore\AppData\Local\Temp\opencode\erd_probe.html', 'w', encoding='utf-8').write(s)
print('ok')

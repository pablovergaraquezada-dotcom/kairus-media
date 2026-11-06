import json,sys
from playwright.sync_api import sync_playwright
d=open('datos.json').read(); h=open('cartelera.html').read().replace('__DATA__',d)
open('_r.html','w').write(h)
out=sys.argv[1] if len(sys.argv)>1 else 'out.png'
with sync_playwright() as p:
    b=p.chromium.launch(); pg=b.new_page(viewport={'width':1920,'height':1080})
    import os; pg.goto('file://'+os.path.abspath('_r.html')); pg.wait_for_timeout(800)
    pg.screenshot(path=out); b.close()

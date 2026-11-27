import render as R
from playwright.sync_api import sync_playwright
G=R.KM/'google'
def pieza(w,h,ty):
    im=R.night(R.fit(G/'show-sala-llena.jpg',w,h,.5,.75 if h<1500 else .6))
    return R.page(w,h,f"""
<img class=abs src="{R.uri_img(im)}" style="inset:0">
<div class=abs style="inset:0;background:linear-gradient(180deg,#0B0A0D 0,rgba(11,10,13,.92) {44 if h<1500 else 34}%,rgba(11,10,13,.2) {62 if h<1500 else 54}%,rgba(11,10,13,0) 72%,rgba(11,10,13,.85) 100%)"></div>
<img class=logo src="{R.LOGO}" style="left:64px;top:{60 if h<1500 else 90}px">
<div class=abs style="left:64px;right:64px;top:{ty}px">
 <div class=k>eventos privados · 2° piso</div>
 <div class=t style="font-size:{132 if h<1500 else 140}px;margin:16px 0 22px">¿son 50?<br>¿son 100?</div>
 <div class=s>empresas, cumpleaños y eventos,<br>con comida, barra y música.</div>
 <div style="margin-top:30px;display:flex;align-items:baseline;gap:14px"><span class=s style="opacity:.8">desde</span><span class=t style="font-size:96px;color:{R.PINK}">$20.000</span><span class=s style="opacity:.8">por persona</span></div>
</div>
<div class=abs style="left:64px;bottom:{70 if h<1500 else 130}px;display:flex;align-items:center;gap:30px"><span class=btn>cotiza por whatsapp</span><span class=foot>los robles 3668 · coronel</span></div>""")
with sync_playwright() as pw:
    b=pw.chromium.launch(executable_path='/usr/bin/google-chrome',args=['--no-sandbox'])
    for n,(w,h,ty) in {'ad_eventos_precio_feed':(1080,1350,140),'ad_eventos_precio_historia':(1080,1920,260)}.items():
        p=b.new_page(viewport={'width':w,'height':h});p.set_content(pieza(w,h,ty));p.wait_for_timeout(300)
        p.screenshot(path=f'out/{n}.jpg',type='jpeg',quality=92);p.close()
    b.close()

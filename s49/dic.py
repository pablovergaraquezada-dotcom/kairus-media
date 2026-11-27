import base64,pathlib,io
from PIL import Image,ImageFilter,ImageEnhance
from playwright.sync_api import sync_playwright
import render as R
KM=R.KM
c=Image.open(KM/'eventos/plantilla-cartelera/cut/ivan.png').convert('RGBA').crop((0,0,716,560))
c=c.resize((900,int(c.height*900/c.width)))
r,g,b,a=c.split();rgb=ImageEnhance.Brightness(Image.merge('RGB',(r,g,b))).enhance(.6);c=Image.merge('RGBA',(*rgb.split(),a))
im=Image.new('RGBA',(1080,800),(11,10,13,255));im.alpha_composite(c,(90,40));im=im.convert('RGB')
LG=R.b64(KM/'eventos/plantilla-cartelera/fonts/LeagueGothic%5Bwdth%5D.ttf')
rows=[('SÁB 5','IVÁN CABELLO','21:00'),('SÁB 12','MEXICANO QL','21:00'),('MIÉ 16','NOESTOYCREICI','19:30'),('JUE 17','BOTOTA FOX','19:30')]
rh=''.join(f'<div style="display:flex;align-items:center;border-top:1px solid rgba(255,255,255,.18);height:110px"><div class=k style="width:200px;font-size:30px">{d}</div><div style="flex:1;font-family:LG;font-size:72px;color:#F3EBDD">{a}</div><div style="font-family:\'Inter Display\';font-weight:600;font-size:30px;color:#fff">{h}</div></div>' for d,a,h in rows)
body=f"""<style>@font-face{{font-family:LG;src:url(data:font/ttf;base64,{LG})}}</style>
<img class=abs src="{R.uri_img(im)}" style="left:0;top:0">
<div class=abs style="left:0;top:380px;width:1080px;height:420px;background:linear-gradient(rgba(11,10,13,0),#0B0A0D)"></div>
<img class=logo src="{R.LOGO}" style="right:64px;top:90px;width:180px">
<div class=abs style="left:80px;right:80px;top:640px">
<div class=k style="font-size:28px">stand up en vivo</div>
<div style="font-family:'Inter Display';font-weight:700;font-size:150px;letter-spacing:-.04em;line-height:.95;color:#F3EBDD;margin-top:20px">diciembre <span style="font-family:Ins;font-style:italic;font-weight:400;color:{R.PINK}">en</span></div>
<div style="font-family:Ins;font-style:italic;font-size:160px;line-height:.95;color:{R.PINK}">kairus.</div>
<div style="margin-top:60px">{rh}<div style="border-top:1px solid rgba(255,255,255,.18)"></div></div>
<div class=s style="font-size:30px;margin-top:34px">todos los jueves: bingo 21:00 + karaoke · entradas en kairusbar.cl</div></div>
<div class=foot style="position:absolute;left:0;right:0;bottom:80px;text-align:center;letter-spacing:.3em">los robles 3668 · coronel</div>"""
html=R.page(1080,1920,body)
with sync_playwright() as pw:
    b=pw.chromium.launch(executable_path='/usr/bin/google-chrome',args=['--no-sandbox'])
    p=b.new_page(viewport={'width':1080,'height':1920});p.set_content(html);p.wait_for_timeout(300)
    p.screenshot(path='out/bar_b6_diciembre_sin_gaby.jpg',type='jpeg',quality=92);b.close()

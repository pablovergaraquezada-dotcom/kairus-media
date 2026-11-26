# s49 · Kairus Bar + Kairus Café · piezas con el estándar (26-11-2026)
# Sin promos diarias. Bar: cumpleaños, grupos, reservas, eventos. Café: línea editorial (foto manda, minúscula, etiquetas).
import base64, io, pathlib
from PIL import Image, ImageEnhance, ImageOps
from playwright.sync_api import sync_playwright

KM = pathlib.Path('/home/claude/kairus-media')
MG = pathlib.Path('/home/claude/mesaly-gestion/marketing')
NM = pathlib.Path('/home/claude/s49/node_modules/@fontsource')
OUT = pathlib.Path('/home/claude/s49/out'); OUT.mkdir(exist_ok=True)
PINK = '#FF3EA5'; WA = '+56 9 7194 6082'

def b64(p): return base64.b64encode(pathlib.Path(p).read_bytes()).decode()
def uri_img(im, q=92):
    b = io.BytesIO(); im.convert('RGB').save(b, 'JPEG', quality=q); return 'data:image/jpeg;base64,' + base64.b64encode(b.getvalue()).decode()

LOGO = 'data:image/png;base64,' + b64(KM / 'eventos/plantilla-cartelera/logo.png')
FONTS = f"""
@font-face{{font-family:Man;font-weight:700;src:url(data:font/woff2;base64,{b64(NM/'manrope/files/manrope-latin-700-normal.woff2')})}}
@font-face{{font-family:Man;font-weight:800;src:url(data:font/woff2;base64,{b64(NM/'manrope/files/manrope-latin-800-normal.woff2')})}}
@font-face{{font-family:Ins;font-style:italic;src:url(data:font/woff2;base64,{b64(NM/'instrument-serif/files/instrument-serif-latin-400-italic.woff2')})}}
"""

def fit(path, w, h, cx=.5, cy=.5, zoom=1.0):
    """recorte tipo cover con centro (cx, cy) y zoom"""
    im = Image.open(path).convert('RGB')
    s = max(w / im.width, h / im.height) * zoom
    im = im.resize((round(im.width * s), round(im.height * s)), Image.LANCZOS)
    x = min(max(round(im.width * cx - w / 2), 0), im.width - w)
    y = min(max(round(im.height * cy - h / 2), 0), im.height - h)
    return im.crop((x, y, x + w, y + h))

def warm(im, sat=1.08, con=1.06, bri=1.0):
    r, g, b = im.split()
    r = r.point(lambda v: min(255, v * 1.04)); b = b.point(lambda v: v * .94)
    im = Image.merge('RGB', (r, g, b))
    im = ImageEnhance.Color(im).enhance(sat); im = ImageEnhance.Contrast(im).enhance(con)
    return ImageEnhance.Brightness(im).enhance(bri)

def night(im, sat=1.05, con=1.08):
    im = ImageEnhance.Color(im).enhance(sat); return ImageEnhance.Contrast(im).enhance(con)

def page(w, h, body, bg='#0B0A0D', fam="'Inter Display'"):
    return f"""<!doctype html><html><head><meta charset=utf-8><style>{FONTS}
*{{margin:0;padding:0;box-sizing:border-box}}
body{{width:{w}px;height:{h}px;overflow:hidden;background:{bg};font-family:{fam};position:relative;-webkit-font-smoothing:antialiased}}
.abs{{position:absolute}} .logo{{position:absolute;width:190px}}
.k{{font-family:'Inter Display';font-weight:700;letter-spacing:.16em;text-transform:uppercase;font-size:24px;color:{PINK}}}
.t{{font-family:'Inter Display';font-weight:700;letter-spacing:-.035em;line-height:.95;color:#fff}}
.s{{font-family:'Inter Display';font-weight:500;color:#fff;font-size:34px;line-height:1.3;opacity:.92}}
.btn{{display:inline-block;background:{PINK};color:#0B0A0D;font-family:'Inter Display';font-weight:700;letter-spacing:.12em;text-transform:uppercase;font-size:24px;padding:22px 30px}}
.foot{{font-family:'Inter Display';font-weight:600;letter-spacing:.2em;text-transform:uppercase;font-size:20px;color:#fff;opacity:.75}}
/* café */
.ct{{font-family:Man;font-weight:800;letter-spacing:-.04em;line-height:.92;color:#F3EBDD}}
.ci{{font-family:Ins;font-style:italic;color:#F3EBDD}}
.cs{{font-family:Man;font-weight:700;color:#F3EBDD;font-size:28px;letter-spacing:.02em}}
.lab{{text-shadow:0 1px 8px rgba(0,0,0,.7);position:absolute;font-family:Man;font-weight:700;font-size:26px;color:#F3EBDD;letter-spacing:.02em;white-space:nowrap}}
.dot{{position:absolute;width:12px;height:12px;border-radius:50%;background:#F3EBDD;box-shadow:0 0 0 6px rgba(243,235,221,.25)}}
.ln{{position:absolute;height:2px;background:#F3EBDD;transform-origin:0 50%}}
</style></head><body>{body}</body></html>"""

def label(x, y, tx, ty, text, side='r'):
    """punto en (x,y) del ingrediente, línea fina hasta (tx,ty) y texto"""
    import math
    dx, dy = tx - x, ty - y; L = math.hypot(dx, dy); a = math.degrees(math.atan2(dy, dx))
    t = f'<div class=lab style="left:{tx+14}px;top:{ty-18}px">{text}</div>' if side == 'r' else \
        f'<div class=lab style="right:{1080-tx+14}px;top:{ty-18}px">{text}</div>'
    return (f'<div class=dot style="left:{x-6}px;top:{y-6}px"></div>'
            f'<div class=ln style="left:{x}px;top:{y-1}px;width:{L}px;transform:rotate({a}deg)"></div>' + t)

P = {}
G = KM / 'google'; HB = MG / 'kairus/fotos'; CF = MG / 'kairuscafe/fotos'

# ---------- BAR ----------
# b1 · feed 4:5 · cumpleaños
im = night(fit(G / 'show-publico-riendo.jpg', 1080, 1350, .5, .5))
P['bar_b1_feed_cumple'] = (1080, 1350, page(1080, 1350, f"""
<img class=abs src="{uri_img(im)}" style="inset:0">
<div class=abs style="inset:0;background:linear-gradient(180deg,rgba(11,10,13,.55) 0,rgba(11,10,13,0) 22%,rgba(11,10,13,0) 38%,rgba(11,10,13,.88) 62%,#0B0A0D 82%)"></div>
<img class=logo src="{LOGO}" style="left:64px;top:60px">
<div class=abs style="left:64px;bottom:96px;right:64px">
 <div class=k>cumpleaños en kairus</div>
 <div class=t style="font-size:150px;margin:18px 0 26px">tu cumple,<br>acá.</div>
 <div class=s style="max-width:820px">tú traes a la gente, nosotros ponemos la mesa, la barra y la música.</div>
 <div style="margin-top:36px;display:flex;align-items:center;gap:34px"><span class=btn>reserva por whatsapp</span><span class=foot>los robles 3668 · coronel</span></div>
</div>"""))

# b2 · historia 9:16 · grupos (díptico)
top = night(fit(G / 'show-publico-2.jpg', 1080, 780, .5, .42))
bot = night(fit(HB / 'happy/foto-08477.jpg', 1080, 620, .5, .45))
P['bar_b2_historia_grupos'] = (1080, 1920, page(1080, 1920, f"""
<img class=abs src="{uri_img(top)}" style="left:0;top:0">
<img class=abs src="{uri_img(bot)}" style="left:0;top:1110px">
<div class=abs style="left:0;top:520px;width:1080px;height:260px;background:linear-gradient(rgba(11,10,13,0),#0B0A0D)"></div>
<div class=abs style="left:0;top:1110px;width:1080px;height:160px;background:linear-gradient(#0B0A0D,rgba(11,10,13,0))"></div>
<div class=abs style="left:0;top:1560px;width:1080px;height:170px;background:linear-gradient(rgba(11,10,13,0),#0B0A0D)"></div>
<img class=logo src="{LOGO}" style="left:64px;top:90px">
<div class=abs style="left:0;right:0;top:810px;text-align:center">
 <div class=k>reservas · viernes y sábado</div>
 <div class=t style="font-size:118px;margin-top:16px">¿vienen en grupo?</div>
 <div class=s style="margin-top:22px">reserva y llega con la mesa lista.</div>
</div>
<div class=abs style="left:0;right:0;top:1760px;text-align:center"><span class=btn>whatsapp {WA}</span>
<div class=foot style="margin-top:22px">o en kairusbar.cl · los robles 3668</div></div>"""))

# b3 · historia · fin de año con la pega (sala llena, blanco y negro + acento)
im = fit(G / 'show-sala-llena.jpg', 1080, 1920, .5, .5)
im = ImageEnhance.Contrast(ImageOps.grayscale(im).convert('RGB')).enhance(1.15)
P['bar_b3_historia_pega'] = (1080, 1920, page(1080, 1920, f"""
<img class=abs src="{uri_img(im)}" style="inset:0">
<div class=abs style="inset:0;background:linear-gradient(180deg,#0B0A0D 0,rgba(11,10,13,.75) 30%,rgba(11,10,13,.1) 55%,rgba(11,10,13,.85) 88%)"></div>
<img class=logo src="{LOGO}" style="left:64px;top:90px">
<div class=abs style="left:64px;right:64px;top:300px">
 <div class=k>empresas · 2° piso</div>
 <div class=t style="font-size:132px;margin:18px 0 26px">cierra el año<br>con la pega.</div>
 <div class=s>de 50 a 100 personas, con comida,<br>barra y música. te armamos la cotización.</div>
</div>
<div class=abs style="left:64px;bottom:130px"><span class=btn>cotiza por whatsapp</span>
<div class=foot style="margin-top:26px">{WA}</div></div>"""))

# b4 · carrusel 4:5 · serie "¿con quién vienes?"
def slide(path, cx, cy, k, t, sub, n, zoom=1.0):
    im = night(fit(path, 1080, 1350, cx, cy, zoom))
    return (1080, 1350, page(1080, 1350, f"""
<img class=abs src="{uri_img(im)}" style="inset:0">
<div class=abs style="inset:0;background:linear-gradient(180deg,rgba(11,10,13,.5) 0,rgba(11,10,13,0) 20%,rgba(11,10,13,0) 52%,rgba(11,10,13,.9) 85%)"></div>
<img class=logo src="{LOGO}" style="left:64px;top:60px">
<div class=foot style="position:absolute;right:64px;top:78px">{n} / 4</div>
<div class=abs style="left:64px;right:64px;bottom:90px"><div class=k>{k}</div>
<div class=t style="font-size:128px;margin:16px 0 18px">{t}</div><div class=s>{sub}</div></div>"""))
P['bar_b4_carrusel_1'] = slide(HB / 'local/foto-08766.jpg', .5, .4, '¿con quién vienes?', 'con las<br>de siempre.', 'las que llegan a la hora y se van al cierre.', 1)
P['bar_b4_carrusel_2'] = slide(G / 'show-publico-3.jpg', .5, .5, '¿con quién vienes?', 'con los<br>de la pega.', 'el after office que se alarga.', 2)
P['bar_b4_carrusel_3'] = slide(HB / 'happy/foto-07978.jpg', .5, .45, '¿con quién vienes?', 'con el<br>cumpleañero.', 'y con todo el grupo detrás.', 3)
sala = night(fit(G / 'show-sala-llena.jpg', 952, 640, .5, .55))
P['bar_b4_carrusel_4'] = (1080, 1350, page(1080, 1350, f"""
<img class=logo src="{LOGO}" style="left:64px;top:60px"><div class=foot style="position:absolute;right:64px;top:78px">4 / 4</div>
<div class=abs style="left:64px;top:200px"><div class=k>sea quien sea</div>
<div class=t style="font-size:150px;margin-top:18px">te guardamos<br>la mesa.</div></div>
<img class=abs src="{uri_img(sala)}" style="left:64px;top:610px;width:952px;height:440px;object-fit:cover">
<div class=abs style="left:64px;right:64px;bottom:86px;display:flex;justify-content:space-between;align-items:center">
<span class=btn>whatsapp {WA}</span><span class=foot>kairusbar.cl</span></div>"""))

# ---------- CAFÉ ----------
CB = '#1C120A'
# c1 · feed 4:5 · jamón queso caliente, con etiquetas
im = warm(fit(CF / 'cafe/sesion-img_0272.jpg', 1080, 1350, .5, .56))
P['cafe_c1_feed_jamonqueso'] = (1080, 1350, page(1080, 1350, f"""
<img class=abs src="{uri_img(im)}" style="inset:0">
<div class=abs style="inset:0;background:linear-gradient(180deg,rgba(28,18,10,.88) 0,rgba(28,18,10,.35) 26%,rgba(28,18,10,0) 40%,rgba(28,18,10,0) 80%,rgba(28,18,10,.6) 100%)"></div>
<img class=logo src="{LOGO}" style="right:60px;top:64px;width:170px">
<div class=abs style="left:68px;top:96px"><div class=ct style="font-size:104px">jamón queso,</div>
<div class=ci style="font-size:112px;line-height:1;margin-top:-4px">bien caliente.</div></div>
{label(540, 640, 770, 560, 'queso fundido')}
{label(324, 821, 150, 960, 'jamón', 'l')}
{label(640, 490, 800, 430, 'pan tostado')}
<div class=cs style="position:absolute;left:68px;bottom:56px;opacity:.85">kairus café · desde las 17:00</div>"""), CB)

# c2 · historia · la tarde pide café (foto abajo, banda editorial arriba)
im = warm(fit(CF / 'cafe/sesion-img_0274.jpg', 1080, 1500, .45, .5))
P['cafe_c2_historia_tarde'] = (1080, 1920, page(1080, 1920, f"""
<img class=abs src="{uri_img(im)}" style="left:0;top:420px">
<div class=abs style="left:0;top:420px;width:1080px;height:260px;background:linear-gradient({CB},rgba(28,18,10,0))"></div>
<img class=logo src="{LOGO}" style="left:72px;top:96px;width:160px">
<div class=abs style="left:72px;top:210px"><div class=ct style="font-size:112px">la tarde</div>
<div class=ci style="font-size:124px;line-height:.95">pide café.</div></div>
{label(432, 740, 700, 660, 'crema')}
{label(440, 1140, 740, 1060, 'café con leche')}
<div class=abs style="left:0;bottom:0;width:1080px;height:300px;background:linear-gradient(rgba(28,18,10,0),rgba(28,18,10,.92))"></div>
<div class=cs style="position:absolute;left:72px;bottom:90px;opacity:.9">todos los días desde las 17:00 · los robles 3668</div>""", bg=CB))

# c3 · historia · algo helado (jugos)
im = warm(fit(CF / 'jugos/sesion-img_0432.jpg', 1080, 1920, .55, .5), sat=1.05)
P['cafe_c3_historia_jugos'] = (1080, 1920, page(1080, 1920, f"""
<img class=abs src="{uri_img(im)}" style="inset:0">
<div class=abs style="inset:0;background:linear-gradient(180deg,rgba(28,18,10,.9) 0,rgba(28,18,10,.2) 24%,rgba(28,18,10,0) 60%,rgba(28,18,10,.75) 100%)"></div>
<img class=logo src="{LOGO}" style="left:72px;top:96px;width:160px">
<div class=abs style="left:72px;top:210px"><div class=ct style="font-size:120px">algo helado</div>
<div class=ci style="font-size:124px;line-height:.95">para la tarde.</div></div>
<div class=cs style="position:absolute;left:72px;bottom:90px;opacity:.9">jugos · kairus café · desde las 17:00</div>""", bg=CB))

# c4 · feed 4:5 · panqueques (foto CK recortada sobre el plato, sin pared blanca)
im = warm(fit(CF / 'dulces/ck-43.jpg', 1080, 1350, .55, .66, zoom=1.18), sat=1.12, con=1.12, bri=.86)
P['cafe_c4_feed_panqueques'] = (1080, 1350, page(1080, 1350, f"""
<img class=abs src="{uri_img(im)}" style="inset:0">
<div class=abs style="inset:0;background:linear-gradient(180deg,rgba(28,18,10,.9) 0,rgba(28,18,10,.45) 24%,rgba(28,18,10,0) 42%,rgba(28,18,10,0) 82%,rgba(28,18,10,.55) 100%)"></div>
<img class=logo src="{LOGO}" style="right:60px;top:64px;width:170px">
<div class=abs style="left:68px;top:96px"><div class=ct style="font-size:120px">panqueques.</div>
<div class=ci style="font-size:72px;line-height:1.05;margin-top:6px">para el antojo de la tarde.</div></div>
LABELS_C4
<div class=cs style="position:absolute;left:68px;bottom:56px;opacity:.85">kairus café · desde las 17:00</div>"""), CB)

# ================= tanda 2 (mié 2 – dom 6) =================
PC = KM / 'eventos/plantilla-cartelera'
FONTS2 = f"@font-face{{font-family:LG;src:url(data:font/ttf;base64,{b64(PC/'fonts/LeagueGothic%5Bwdth%5D.ttf')})}}"
GABY = 'data:image/png;base64,' + b64(PC / 'cut/gaby.png')
def show(w, h, top_name, gy, gw):
    return page(w, h, f"""<style>{FONTS2}</style>
<div class=abs style="inset:0;background:radial-gradient(60% 45% at 50% {gy+300}px,rgba(255,62,165,.28),rgba(11,10,13,0) 70%),#0B0A0D"></div>
<img class=logo src="{LOGO}" style="left:64px;top:{60 if h<1500 else 90}px">
<div class=k style="position:absolute;right:64px;top:{78 if h<1500 else 108}px">kairus presenta</div>
<div class=abs style="left:0;right:0;top:{top_name}px;text-align:center;font-family:LG;font-size:{250 if h<1500 else 270}px;line-height:.85;color:#F3EBDD;letter-spacing:.01em;white-space:nowrap">GABY DEL RÍO</div>
<img class=abs src="{GABY}" style="left:{(w-gw)//2}px;top:{gy}px;width:{gw}px">
<div class=abs style="left:0;right:0;bottom:0;height:{520 if h<1500 else 640}px;background:linear-gradient(rgba(11,10,13,0),#0B0A0D 55%)"></div>
<div class=abs style="left:64px;right:64px;bottom:{80 if h<1500 else 130}px">
 <div class=k>stand up · comedia en vivo</div>
 <div class=t style="font-size:{92 if h<1500 else 104}px;margin:14px 0 26px">viernes 4 de diciembre<br>21:00 hrs.</div>
 <div style="display:flex;align-items:center;gap:30px"><span class=btn>entradas en kairusbar.cl</span><span class=foot>los robles 3668 · coronel</span></div>
</div>""")
P['bar_b5_gaby_feed'] = (1080, 1350, show(1080, 1350, 120, 330, 760))
P['bar_b5_gaby_historia'] = (1080, 1920, show(1080, 1920, 250, 470, 900))

# café c5 · feed · ciabatta (foto CK recortada al pan, sin pared blanca)
im = warm(fit(CF / 'ciabatta/ck-4.jpg', 1080, 1350, .5, .68, zoom=1.35), sat=1.12, con=1.12, bri=.84)
P['cafe_c5_feed_ciabatta'] = (1080, 1350, page(1080, 1350, f"""
<img class=abs src="{uri_img(im)}" style="inset:0">
<div class=abs style="inset:0;background:linear-gradient(180deg,rgba(28,18,10,.92) 0,rgba(28,18,10,.5) 25%,rgba(28,18,10,0) 42%,rgba(28,18,10,0) 80%,rgba(28,18,10,.6) 100%)"></div>
<img class=logo src="{LOGO}" style="right:60px;top:64px;width:170px">
<div class=abs style="left:68px;top:96px"><div class=ct style="font-size:120px">ciabatta.</div>
<div class=ci style="font-size:72px;line-height:1.05;margin-top:6px">pan crujiente, bien cargada.</div></div>
LABELS_C5
<div class=cs style="position:absolute;left:68px;bottom:56px;opacity:.85">kairus café · desde las 17:00</div>"""))

# café c6 · historia · café y ciabatta (foto arriba, banda abajo)
im = warm(fit(CF / 'ciabatta/ck-25.jpg', 1080, 1400, .5, .72, zoom=1.15), sat=1.1, con=1.1, bri=.86)
P['cafe_c6_historia_once'] = (1080, 1920, page(1080, 1920, f"""
<img class=abs src="{uri_img(im)}" style="left:0;top:0">
<div class=abs style="left:0;top:0;width:1080px;height:420px;background:linear-gradient(rgba(28,18,10,.9),rgba(28,18,10,0))"></div>
<div class=abs style="left:0;top:1150px;width:1080px;height:250px;background:linear-gradient(rgba(28,18,10,0),#1C120A)"></div>
<img class=logo src="{LOGO}" style="left:72px;top:96px;width:160px">
<div class=abs style="left:72px;top:1430px"><div class=ct style="font-size:112px">café y ciabatta.</div>
<div class=ci style="font-size:96px;line-height:1">la once de siempre.</div></div>
<div class=cs style="position:absolute;left:72px;bottom:90px;opacity:.9">todos los días desde las 17:00 · los robles 3668</div>""", bg='#1C120A'))

if __name__ == '__main__':
    import sys, json
    lab = json.loads(sys.argv[1]) if len(sys.argv) > 1 else {}
    ONLY = sys.argv[2].split(',') if len(sys.argv) > 2 else []
    with sync_playwright() as pw:
        br = pw.chromium.launch(executable_path='/usr/bin/google-chrome', args=['--no-sandbox'])
        for name, v in P.items():
            if ONLY and name not in ONLY: continue
            w, h, html = v[0], v[1], v[2]
            html = html.replace('LABELS_C4', lab.get('c4', '')).replace('LABELS_C5', lab.get('c5', ''))
            pg = br.new_page(viewport={'width': w, 'height': h}); pg.set_content(html); pg.wait_for_timeout(250)
            pg.screenshot(path=str(OUT / f'{name}.jpg'), type='jpeg', quality=92); pg.close()
            print('ok', name)
        br.close()


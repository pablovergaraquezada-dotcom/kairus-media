from PIL import Image, ImageDraw, ImageFont, ImageFilter, ImageEnhance
import sys
R = "/home/claude/kairus-media/"
F = R + "eventos/plantilla-cartelera/fonts/"
OUT = sys.argv[1]

def font(name, size, var=None):
    f = ImageFont.truetype(F + name, size)
    if var:
        try:
            f.set_variation_by_axes(var)
        except Exception:
            pass
    return f

GOTH = lambda s: font("LeagueGothic%5Bwdth%5D.ttf", s)
ANTON = lambda s: font("Anton-Regular.ttf", s)
SERIF_I = lambda s: font("DMSerifDisplay-Italic.ttf", s)
ARCH = lambda s, w=500: font("Archivo%5Bwdth,wght%5D.ttf", s, [100, w])

CREAM = (243, 236, 222)
LILAC = (196, 150, 255)
INK = (14, 11, 18)
MUTED = (150, 140, 160)

ROWS = [
    ("LUNES", "10:00 – 23:00"),
    ("MARTES Y MIÉRCOLES", "10:00 – 00:00"),
    ("JUEVES", "10:00 – 01:00"),
    ("VIERNES Y SÁBADO", "13:00 – 03:00"),
    ("DOMINGO", "13:00 – 23:00"),
]

def cover(img, w, h, fy=0.4):
    s = max(w / img.width, h / img.height)
    img = img.resize((round(img.width * s), round(img.height * s)), Image.LANCZOS)
    x = (img.width - w) // 2
    y = int((img.height - h) * fy)
    return img.crop((x, y, x + w, y + h))

def tracked(d, xy, text, f, fill, track=0, anchor="l"):
    x, y = xy
    widths = [d.textlength(c, font=f) for c in text]
    total = sum(widths) + track * (len(text) - 1)
    if anchor == "m":
        x -= total / 2
    elif anchor == "r":
        x -= total
    for c, w in zip(text, widths):
        d.text((x, y), c, font=f, fill=fill)
        x += w + track
    return total

def logo(color, h):
    lg = Image.open(R + "eventos/plantilla-cartelera/logo.png").convert("RGBA")
    lg = lg.resize((round(lg.width * h / lg.height), h), Image.LANCZOS)
    a = lg.split()[3]
    solid = Image.new("RGBA", lg.size, color + (255,))
    solid.putalpha(a)
    return solid

def grain(img, amt=10):
    import random
    n = Image.effect_noise(img.size, amt).convert("L")
    n = Image.merge("RGB", (n, n, n))
    return Image.blend(img, Image.composite(img, n, Image.new("L", img.size, 235)), 0.25)

def grade(img):
    img = ImageEnhance.Contrast(img).enhance(1.08)
    img = ImageEnhance.Color(img).enhance(1.05)
    return img

def schedule(d, x0, x1, y, size_day, size_hr, gap, today=None):
    fd = ARCH(size_day, 600)
    fh = GOTH(size_hr)
    for day, hr in ROWS:
        hl = today and today in day
        col = LILAC if hl else CREAM
        tracked(d, (x0, y + (size_hr - size_day) * 0.55), day, fd, col, track=size_day * 0.12)
        d.text((x1, y - size_hr * 0.08), hr, font=fh, fill=col, anchor="ra")
        ly = y + size_hr + gap * 0.45
        d.line([(x0, ly), (x1, ly)], fill=(255, 255, 255, 40), width=1)
        y += size_hr + gap
    return y

# ---------- BAR: historia 1080x1920 ----------
def bar_story(hoy=True):
    W, H = 1080, 1920
    ph = grade(Image.open(R + "google/ambiente-mural.jpg").convert("RGB"))
    ph = cover(ph, W, 1180, 0.25)
    base = Image.new("RGB", (W, H), INK)
    base.paste(ph, (0, 0))
    ov = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    od = ImageDraw.Draw(ov)
    for i in range(640):
        a = int(255 * (i / 640) ** 1.25)
        od.line([(0, 1180 - 640 + i), (W, 1180 - 640 + i)], fill=INK + (a,))
    for i in range(260):
        a = int(150 * (1 - i / 260) ** 2)
        od.line([(0, i), (W, i)], fill=(0, 0, 0, a))
    base = Image.alpha_composite(base.convert("RGBA"), ov)
    d = ImageDraw.Draw(base)
    base.alpha_composite(logo(CREAM, 46), (72, 80))
    if hoy:
        tag = "HOY ABRIMOS 13:00"
        f = ARCH(26, 700)
        tw = tracked(d, (0, -999), tag, f, CREAM, track=4)
        d.rounded_rectangle([W - 72 - tw - 44, 74, W - 72, 74 + 58], radius=29, fill=LILAC)
        tracked(d, (W - 72 - tw - 22, 88), tag, f, INK, track=4)
    y = 900
    d.text((72, y), "desde hoy", font=SERIF_I(78), fill=LILAC)
    d.text((66, y + 70), "NUEVO HORARIO", font=GOTH(232), fill=CREAM)
    y = schedule(d, 74, W - 74, 1262, 30, 72, 30, today="VIERNES" if hoy else None)
    f = ARCH(22, 500)
    tracked(d, (W / 2, 1830), "KAIRUS BAR · KAIRUS CAFÉ · LOS ROBLES 3668, CORONEL", f, MUTED, track=3, anchor="m")
    return grain(base.convert("RGB"))

# ---------- BAR: feed 1080x1350 ----------
def bar_feed():
    W, H = 1080, 1350
    base = Image.new("RGBA", (W, H), INK + (255,))
    d = ImageDraw.Draw(base)
    base.alpha_composite(logo(CREAM, 40), ((W - logo(CREAM, 40).width) // 2, 64))
    tracked(d, (W / 2, 140), "BAR · COCINA · CAFÉ", ARCH(20, 600), MUTED, track=6, anchor="m")
    ph = grade(Image.open(R + "google/ambiente-neon.jpg").convert("RGB"))
    ph = cover(ph, 440, 760, 0.3)
    px, py = 72, 230
    sh = Image.new("RGBA", (ph.width + 60, ph.height + 60), (0, 0, 0, 0))
    ImageDraw.Draw(sh).rectangle([30, 30, 30 + ph.width, 30 + ph.height], fill=(120, 60, 200, 120))
    sh = sh.filter(ImageFilter.GaussianBlur(28))
    base.alpha_composite(sh, (px - 30, py - 30))
    base.paste(ph, (px, py))
    tx = px + ph.width + 56
    d.text((tx, 236), "nuevo", font=SERIF_I(64), fill=LILAC)
    d.text((tx - 4, 290), "HORARIO", font=GOTH(196), fill=CREAM)
    fd, fh = ARCH(21, 600), GOTH(62)
    y = 520
    x1 = W - 72
    for day, hr in ROWS:
        tracked(d, (tx, y), day, fd, MUTED, track=3)
        d.text((tx, y + 30), hr, font=fh, fill=CREAM)
        y += 104
    d.line([(72, 1060), (W - 72, 1060)], fill=(255, 255, 255, 45), width=1)
    d.text((W / 2, 1120), "El momento es acá.", font=SERIF_I(58), fill=CREAM, anchor="ma")
    tracked(d, (W / 2, 1250), "LOS ROBLES 3668 · LAGUNILLAS · CORONEL", ARCH(20, 500), MUTED, track=4, anchor="m")
    return grain(base.convert("RGB"))

# ---------- CAFÉ ----------
CC = (240, 233, 220)
CINK = (40, 33, 28)
CACC = (176, 128, 72)

def cafe_piece(W, H, hoy):
    base = Image.new("RGBA", (W, H), CC + (255,))
    d = ImageDraw.Draw(base)
    d.text((64, 58), "kairus", font=ARCH(30, 500), fill=CINK)
    d.text((64 + d.textlength("kairus ", font=ARCH(30, 500)), 52), "café", font=SERIF_I(36), fill=CINK)
    top = 130 if H == 1350 else 260
    if hoy and H == 1920:
        d.text((64, 150), "hoy abrimos a las 13:00", font=SERIF_I(50), fill=CACC)
    d.text((60, top + 6), "nuevo", font=SERIF_I(128), fill=CINK)
    d.text((60, top + 118), "horario.", font=SERIF_I(128), fill=CINK)
    y = top + 300
    fd, fh = ARCH(22 if H == 1350 else 26, 600), SERIF_I(46 if H == 1350 else 58)
    step = 64 if H == 1350 else 84
    for day, hr in ROWS:
        hl = hoy and "VIERNES" in day
        tracked(d, (64, y + 16), day, fd, CACC if hl else CINK, track=3)
        d.text((W - 64, y), hr.replace(" – ", "–"), font=fh, fill=CACC if hl else CINK, anchor="ra")
        d.line([(64, y + step - 10), (W - 64, y + step - 10)], fill=(40, 33, 28, 50), width=1)
        y += step
    ph = Image.open(R + "google/desayuno.jpg").convert("RGB")
    ph = ImageEnhance.Brightness(ph).enhance(1.03)
    ph_h = H - y - 40
    ph = cover(ph, W, ph_h, 0.5)
    base.paste(ph, (0, H - ph_h))
    gr = Image.new("RGBA", (W, 220), (0, 0, 0, 0))
    gd = ImageDraw.Draw(gr)
    for i in range(220):
        gd.line([(0, i), (W, i)], fill=(20, 15, 12, int(170 * (i / 220) ** 1.5)))
    base.alpha_composite(gr, (0, H - 220))
    tracked(d, (64, H - 70), "LOS ROBLES 3668 · CORONEL", ARCH(20, 600), CC, track=4)
    return grain(base.convert("RGB"), 6)

bar_story(True).save(OUT + "/bar_historia_hoy.jpg", quality=93)
bar_story(False).save(OUT + "/destacada_horarios.jpg", quality=93)
bar_feed().save(OUT + "/bar_feed.jpg", quality=93)
cafe_piece(1080, 1920, True).save(OUT + "/cafe_historia_hoy.jpg", quality=93)
cafe_piece(1080, 1350, False).save(OUT + "/cafe_feed.jpg", quality=93)

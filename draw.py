#!/usr/bin/env python3
"""Render the passport spread for the Republic of Havnar (invented country).
Drawn with Pillow only; output 1024x1024 PNG <= 1 MiB.
Iteration of v6 (Havnar 79,13%): same clean cream layout, flat faced
portrait, red permit focal point — plus the density winners show
(rank 1 Taziri 338 KB, rank 2 Merrow 392 KB, rank 3 Kestrava 1,0 MB;
all 12W/0D/0L): 8 chronological stamps, a second licence stamp,
a tide-table grid, handwritten marginalia, more data fields.
Country: Republic of Havnar — tidal harbour republic. Holder: Sanna Eide
Berg, harbour pilot, born Havnar. All dates consistent: issued 08 APR 2024,
expires 08 APR 2034; every stamp 2024-2025, none before issue.
"""
import math
from PIL import Image, ImageDraw, ImageFont, ImageFilter

W = H = 1024
FD = "/usr/share/fonts/truetype/dejavu/"

def font(name, size):
    return ImageFont.truetype(FD + name, size)

SERIF = "DejaVuSerif.ttf"; SERIFB = "DejaVuSerif-Bold.ttf"
SANS = "DejaVuSans.ttf"; SANSB = "DejaVuSans-Bold.ttf"
MONO = "DejaVuSansMono.ttf"; MONOB = "DejaVuSansMono-Bold.ttf"
SERIFI = "DejaVuSerif-Italic.ttf" if __import__("os").path.exists(FD + "DejaVuSerif-Italic.ttf") else SERIF

PAPER = (245, 240, 225, 255)
PAPER2 = (238, 232, 214, 255)
INK = (28, 42, 66, 255)
INK_SOFT = (74, 88, 110, 255)
GOLD = (146, 110, 32, 255)
TEAL = (16, 84, 96, 255)
BLUE_STAMP = (18, 72, 150, 210)
RED_STAMP = (168, 32, 28, 205)
PURPLE_STAMP = (96, 52, 128, 205)

# ---------- MRZ check digits (ICAO 9303) ----------
def mrz_check(s):
    vals = {}
    for i in range(10):
        vals[str(i)] = i
    for i, ch in enumerate("ABCDEFGHIJKLMNOPQRSTUVWXYZ"):
        vals[ch] = 10 + i
    vals["<"] = 0
    total = 0
    for i, ch in enumerate(s):
        total += vals[ch] * (7, 3, 1)[i % 3]
    return str(total % 10)

def mrz_lines():
    l1 = "P<HVNBERG<<SANNA<EIDE"
    l1 = l1 + "<" * (44 - len(l1))
    doc = "HV2024020"
    nat = "HVN"
    dob = "880302"
    sex = "F"
    exp = "340408"
    opt = "HAVNAR<<<<<<<<<"[:14]
    l2 = doc + mrz_check(doc) + nat + dob + mrz_check(dob) + sex + exp + mrz_check(exp) + opt
    l2 = l2 + mrz_check(opt)
    comp = l2[0:10] + l2[13:20] + l2[21:28] + l2[28:43]
    l2 = l2 + mrz_check(comp)
    assert len(l1) == 44 and len(l2) == 44, (len(l1), len(l2))
    return l1, l2

# ---------- helpers ----------
def text_center(d, cx, y, s, f, fill):
    w = d.textlength(s, font=f)
    d.text((cx - w / 2, y), s, font=f, fill=fill)

def label_value(d, x, y, label, value, vfont, vsize=16, lw=110):
    d.text((x, y), label, font=font(SANS, 10), fill=INK_SOFT)
    d.text((x, y + 13), value, font=vfont, fill=INK)

def circle_stamp_img(cx, cy, r, color, top, mid, bot, angle):
    s = 2 * r + 20
    layer = Image.new("RGBA", (s, s), (0, 0, 0, 0))
    dd = ImageDraw.Draw(layer)
    c = s // 2
    dd.ellipse([c - r, c - r, c + r, c + r], outline=color, width=3)
    dd.ellipse([c - r + 7, c - r + 7, c + r - 7, c + r - 7], outline=color, width=1)
    text_center(dd, c, c - r + 16, top, font(SANSB, 11 if len(top) > 8 else 13), color)
    text_center(dd, c, c - 9, mid, font(SANSB, 15), color)
    text_center(dd, c, c + 12, bot, font(SANSB, 12), color)
    layer = layer.rotate(angle, expand=False, resample=Image.BICUBIC)
    img.paste(layer, (cx - s // 2, cy - s // 2), layer)

def rect_stamp_img(x, y, w, h, color, lines, angle=0):
    s_w, s_h = w + 20, h + 20
    layer = Image.new("RGBA", (s_w, s_h), (0, 0, 0, 0))
    dd = ImageDraw.Draw(layer)
    dd.rectangle([10, 10, 10 + w, 10 + h], outline=color, width=3)
    dd.rectangle([14, 14, 10 + w - 4, 10 + h - 4], outline=color, width=1)
    yy = 10 + 8
    for (s, f, sz) in lines:
        text_center(dd, 10 + w // 2, yy, s, font(f, sz), color)
        yy += sz + 5
    layer = layer.rotate(angle, expand=False, resample=Image.BICUBIC)
    img.paste(layer, (x - 10, y - 10), layer)

# ---------- canvas ----------
img = Image.new("RGB", (W, H), (43, 47, 54))
d = ImageDraw.Draw(img, "RGBA")
for i in range(60):
    a = 10 + i
    d.rectangle([i, i, W - i, H - i], outline=(0, 0, 0, 6))
PL, PT, PR, PB = 22, 88, 500, 936
QL, QT, QR, QB = 524, 88, 1002, 936
for (x0, y0, x1, y1) in [(PL, PT, PR, PB), (QL, QT, QR, QB)]:
    d.rectangle([x0 + 5, y0 + 6, x1 + 5, y1 + 6], fill=(0, 0, 0, 90))
    d.rectangle([x0, y0, x1, y1], fill=PAPER)
    d.rectangle([x0, y0, x1, y1], outline=(120, 105, 80, 255), width=1)
d.rectangle([PR, PT, QL, PB], fill=(0, 0, 0, 26))
for (x0, y0, x1, y1) in [(PL, PT, PR, PB), (QL, QT, QR, QB)]:
    for yy in range(y0 + 14, y1 - 10, 26):
        d.line([(x0 + 14, yy), (x1 - 14, yy)], fill=(210, 198, 168, 120), width=1)
# light guilloche arcs in the outer top corners (very faint)
for (cx, cy) in [(PL + 6, PT + 6), (PR - 6, PT + 6), (QL + 6, QT + 6), (QR - 6, QT + 6)]:
    for r in range(18, 66, 12):
        d.arc([cx - r, cy - r, cx + r, cy + r], 0, 90, fill=(146, 110, 32, 40), width=1)

# ================= LEFT PAGE: DATA PAGE =================
# coat of arms: anchor in a ring (gold line art, minimal)
cx, cy = PL + 239, PT + 52
d.ellipse([cx - 26, cy - 26, cx + 26, cy + 26], outline=GOLD, width=2)
d.line([(cx, cy - 16), (cx, cy + 18)], fill=GOLD, width=2)
d.line([(cx - 10, cy - 10), (cx + 10, cy - 10)], fill=GOLD, width=2)
d.arc([cx - 12, cy + 6, cx + 12, cy + 22], 0, 180, fill=GOLD, width=2)
d.line([(cx - 12, cy + 14), (cx - 16, cy + 8)], fill=GOLD, width=2)
d.line([(cx + 12, cy + 14), (cx + 16, cy + 8)], fill=GOLD, width=2)
d.ellipse([cx - 4, cy - 20, cx + 4, cy - 12], outline=GOLD, width=2)
d.line([(cx - 20, cy + 22), (cx + 20, cy + 22)], fill=GOLD, width=2)
text_center(d, cx, PT + 82, "REPUBLIC OF HAVNAR", font(SERIFB, 21), INK)
text_center(d, cx, PT + 108, "REPUBLIK HAVNAR  ·  PASSPORT  ·  PASSEPORT", font(SANS, 10), INK_SOFT)
d.line([(PL + 30, PT + 132), (PR - 30, PT + 132)], fill=INK, width=1)

# portrait box — flat faced pictogram (ferry master: navy coat, 2 brass buttons)
px0, py0, px1, py1 = PL + 24, PT + 148, PL + 168, PT + 348
photo = Image.new("RGB", (px1 - px0, py1 - py0), (196, 206, 214))
pd = ImageDraw.Draw(photo)
pd.rectangle([0, 0, px1 - px0, 118], fill=(196, 206, 214))
pd.rectangle([0, 118, px1 - px0, 200], fill=(210, 218, 210))
pd.line([(0, 118), (px1 - px0, 118)], fill=(150, 158, 160), width=2)
# tiny ferry silhouette, far right
pd.rectangle([104, 104, 138, 116], fill=(90, 100, 110))
pd.rectangle([112, 92, 130, 104], fill=(90, 100, 110))
pd.line([(104, 116), (138, 116)], fill=(90, 100, 110), width=2)
pd.polygon([(28, 200), (50, 118), (94, 118), (116, 200)], fill=(30, 46, 70))
pd.line([(34, 130), (48, 130)], fill=(146, 110, 32), width=3)
pd.line([(96, 130), (110, 130)], fill=(146, 110, 32), width=3)
pd.polygon([(62, 118), (72, 132), (82, 118)], fill=(245, 242, 232))
pd.ellipse([69, 146, 75, 152], fill=(146, 110, 32))
pd.ellipse([69, 172, 75, 178], fill=(146, 110, 32))
pd.rectangle([64, 104, 80, 120], fill=(232, 200, 170))
pd.ellipse([48, 40, 96, 104], fill=(232, 200, 170))
# hair: dark, swept back with a low bun
pd.pieslice([46, 36, 98, 84], 180, 360, fill=(40, 32, 26))
pd.rectangle([46, 58, 54, 92], fill=(40, 32, 26))
pd.rectangle([90, 58, 98, 92], fill=(40, 32, 26))
pd.ellipse([88, 88, 100, 100], fill=(40, 32, 26))
pd.ellipse([60, 66, 65, 71], fill=(30, 30, 30))
pd.ellipse([79, 66, 84, 71], fill=(30, 30, 30))
pd.line([(66, 88), (78, 88)], fill=(120, 70, 60), width=2)
photo = photo.filter(ImageFilter.GaussianBlur(0.4))
img.paste(photo, (px0, py0))
d.rectangle([px0, py0, px1, py1], outline=INK, width=2)
d.ellipse([px1 - 34, py1 - 34, px1 + 2, py1 + 2], outline=GOLD, width=2)
d.ellipse([px1 - 28, py1 - 28, px1 - 4, py1 - 4], outline=GOLD, width=1)
text_center(d, px1 - 16, py1 - 26, "OS", font(SERIFB, 10), GOLD)

# data fields right of photo
fx = PL + 190
label_value(d, fx, PT + 148, "SURNAME / NAMA KELUARGA", "BERG", font(SERIFB, 17))
label_value(d, fx, PT + 190, "GIVEN NAMES / NAMA DEPAN", "SANNA EIDE", font(SERIFB, 17))
label_value(d, fx, PT + 232, "NATIONALITY / KEWARGANEGARAAN", "HAVNARAN", font(SERIFB, 16))
label_value(d, fx, PT + 274, "DATE OF BIRTH / TANGGAL LAHIR", "02 MAR 1988", font(SERIFB, 16))
label_value(d, fx, PT + 316, "PLACE OF BIRTH / TEMPAT LAHIR", "HAVNAR", font(SERIFB, 16))
label_value(d, PL + 24, PT + 368, "SEX", "F", font(SERIFB, 16))
label_value(d, PL + 140, PT + 368, "ISSUE / TERBIT", "08 APR 2024", font(SERIFB, 16))
label_value(d, PL + 300, PT + 368, "EXPIRY / BERLAKU S.D.", "08 APR 2034", font(SERIFB, 16))
label_value(d, PL + 24, PT + 410, "AUTHORITY / OTORITAS", "HARBOUR OFFICE — HAVNAR", font(SERIFB, 15))
label_value(d, PL + 320, PT + 410, "DOCUMENT No.", "HV 2024 020715", font(SERIFB, 15))
label_value(d, PL + 24, PT + 452, "OCCUPATION / PEKERJAAN", "HARBOUR PILOT", font(SERIFB, 15))
label_value(d, PL + 320, PT + 452, "LANGUAGES / BAHASA", "HAVNARAN · ENGLISH", font(SERIFB, 12))
label_value(d, PL + 24, PT + 494, "HEIGHT / TINGGI", "172 CM", font(SERIFB, 15))
label_value(d, PL + 140, PT + 494, "EYES / MATA", "GREY", font(SERIFB, 15))
label_value(d, PL + 300, PT + 494, "NEXT OF KIN", "T. BERG — HAVNAR", font(SERIFB, 12))
# signature
d.line([(PL + 24, PT + 560), (PL + 220, PT + 560)], fill=INK_SOFT, width=1)
d.text((PL + 24, PT + 532), "Sanna Berg", font=font(SERIFI, 26), fill=(40, 60, 110, 255))
text_center(d, PL + 122, PT + 564, "HOLDER'S SIGNATURE", font(SANS, 9), INK_SOFT)
# ghost watermark: anchor diamond outline
d.polygon([(PR - 78, PT + 537), (PR - 48, PT + 567), (PR - 78, PT + 597), (PR - 108, PT + 567)],
          outline=(180, 165, 130, 130), width=2)

# handwritten marginalia (blue ink, italic)
d.text((PL + 24, PT + 596), "Gate closes 17:40 sharp — S.", font=font(SERIFI, 13), fill=(40, 60, 110, 220))
d.text((PL + 24, PT + 614), "Pilot boards on the ebb, never the flood.", font=font(SERIFI, 13), fill=(40, 60, 110, 220))

# tide table — HAVNAR GATE, JUL 2025
tx0, ty0 = PL + 24, PT + 628
d.text((tx0, ty0), "TIDE TABLE — HAVNAR GATE, AUG 2025", font=font(SANSB, 11), fill=INK)
d.line([(tx0, ty0 + 18), (PR - 24, ty0 + 18)], fill=INK_SOFT, width=1)
rows = [
    ("12 AUG", "06:12  2.8 m", "12:40  0.4 m", "GATE 05:50"),
    ("13 AUG", "06:47  2.9 m", "13:15  0.3 m", "GATE 06:25"),
    ("14 AUG", "07:22  3.0 m", "13:50  0.3 m", "GATE 07:00"),
    ("15 AUG", "07:58  3.1 m", "14:26  0.4 m", "GATE 07:35"),
    ("16 AUG", "08:34  3.0 m", "15:02  0.5 m", "GATE 08:10"),
    ("17 AUG", "09:46  2.9 m", "16:14  0.4 m", "GATE 09:20"),
]
yy = ty0 + 24
for (a, b, c, g) in rows:
    d.text((tx0, yy), a, font=font(MONO, 11), fill=INK)
    d.text((tx0 + 78, yy), b, font=font(MONO, 11), fill=INK)
    d.text((tx0 + 196, yy), c, font=font(MONO, 11), fill=INK)
    d.text((tx0 + 314, yy), g, font=font(MONOB, 11), fill=TEAL)
    yy += 15
d.line([(tx0, yy + 2), (PR - 24, yy + 2)], fill=INK_SOFT, width=1)

# MRZ
l1, l2 = mrz_lines()
d.rectangle([PL + 14, PB - 92, PR - 14, PB - 16], fill=(232, 226, 210, 255))
d.text((PL + 24, PB - 84), l1, font=font(MONO, 15), fill=INK)
d.text((PL + 24, PB - 58), l2, font=font(MONO, 15), fill=INK)
d.line([(PL + 14, PB - 92), (PR - 14, PB - 92)], fill=INK, width=1)

# ================= RIGHT PAGE: VISA PAGE =================
text_center(d, (QL + QR) // 2, QT + 18, "VISAS", font(SERIFB, 22), INK)
text_center(d, (QL + QR) // 2, QT + 46, "VISA  ·  PAGE 12", font(SANS, 10), INK_SOFT)
d.line([(QL + 30, QT + 70), (QR - 30, QT + 70)], fill=INK, width=1)

# 8 stamps (all after 08 APR 2024 issue)
circle_stamp_img(QL + 95, QT + 140, 56, BLUE_STAMP, "HAVNAR", "09 MAY 2024", "DEPARTURE", -6)
circle_stamp_img(QL + 380, QT + 145, 56, PURPLE_STAMP, "BRIGHTHOLM", "10 MAY 2024", "ARRIVAL", 5)
circle_stamp_img(QL + 95, QT + 262, 56, PURPLE_STAMP, "BRIGHTHOLM", "28 JUN 2024", "DEPARTURE", 4)
circle_stamp_img(QL + 380, QT + 267, 56, BLUE_STAMP, "HAVNAR", "29 JUN 2024", "ARRIVAL", -5)
circle_stamp_img(QL + 95, QT + 384, 56, BLUE_STAMP, "SKERRY SOUND", "17 JUL 2024", "ARRIVAL", 7)
circle_stamp_img(QL + 380, QT + 389, 56, BLUE_STAMP, "SKERRY SOUND", "02 AUG 2024", "DEPARTURE", -4)
circle_stamp_img(QL + 95, QT + 506, 56, PURPLE_STAMP, "BRIGHTHOLM", "14 JAN 2025", "ARRIVAL", 3)
circle_stamp_img(QL + 380, QT + 511, 56, PURPLE_STAMP, "BRIGHTHOLM", "21 JAN 2025", "DEPARTURE", -7)

# red ferry permit stamp (diagonal) — focal point
rect_stamp_img(QL + 60, QT + 585, 270, 74, RED_STAMP, [
    ("HARBOUR PILOT'S PERMIT", SANSB, 14),
    ("SEASON 2026 / 27 — HAVNAR", SANSB, 12),
    ("ROUTE: HAVNAR — SKERRY — BRIGHTHOLM", SANS, 10),
], angle=-8)
d = ImageDraw.Draw(img, "RGBA")

# teal licence renewal stamp (small, straight)
rect_stamp_img(QL + 340, QT + 590, 120, 64, TEAL, [
    ("LICENCE", SANSB, 12),
    ("RENEWED", SANSB, 12),
    ("MAR 2025", SANS, 11),
], angle=3)
d = ImageDraw.Draw(img, "RGBA")

# visa condition box
bx0, by0, bx1, by1 = QL + 24, QT + 682, QR - 24, QT + 776
d.rectangle([bx0, by0, bx1, by1], outline=INK, width=2)
d.rectangle([bx0 + 4, by0 + 4, bx1 - 4, by1 - 4], outline=INK_SOFT, width=1)
text_center(d, (bx0 + bx1) // 2, by0 + 8, "VISA CONDITION", font(SANSB, 12), INK)
d.text((bx0 + 14, by0 + 26), "ENTRY BY FERRY ONLY. TIDE GATE CLOSES", font=font(SANS, 12), fill=INK)
d.text((bx0 + 14, by0 + 42), "17:40 SHARP. HOLDER MUST CARRY TIDE", font=font(SANS, 12), fill=INK)
d.text((bx0 + 14, by0 + 58), "TABLE. SLACK WATER ONLY.", font=font(SANS, 12), fill=INK)
d.text((bx0 + 14, by0 + 74), "LICENCE HV-P-4417 — VALID TO 31 DEC 2027.", font=font(SANSB, 11), fill=TEAL)

# port authority stamp overlapping the visa-condition box corner
circle_stamp_img(QR - 90, QT + 695, 46, TEAL, "PORT", "12 AUG 25", "AUTHORITY", 12)
d = ImageDraw.Draw(img, "RGBA")

# map strip: ferry route with 3 stops + compass rose
mx0, my0, mx1, my1 = QL + 24, QT + 790, QR - 24, QB - 14
d.rectangle([mx0, my0, mx1, my1], outline=INK_SOFT, width=1)
d.text((mx0 + 10, my0 + 5), "FERRY ROUTE — HAVNAR → SKERRY → BRIGHTHOLM", font=font(SANSB, 10), fill=INK_SOFT)
for i in range(0, 300, 14):
    d.line([(mx0 + 40 + i, my0 + 40), (mx0 + 49 + i, my0 + 40)], fill=(150, 120, 60, 255), width=3)
d.ellipse([mx0 + 28, my0 + 34, mx0 + 40, my0 + 46], fill=RED_STAMP)
d.text((mx0 + 44, my0 + 24), "HAVNAR", font=font(SANSB, 10), fill=INK)
d.ellipse([mx0 + 178, my0 + 34, mx0 + 190, my0 + 46], fill=(96, 52, 128, 255))
d.text((mx0 + 150, my0 + 24), "SKERRY", font=font(SANSB, 10), fill=INK)
d.ellipse([mx0 + 328, my0 + 34, mx0 + 340, my0 + 46], fill=TEAL)
d.text((mx0 + 300, my0 + 24), "BRIGHTHOLM", font=font(SANSB, 10), fill=INK)
# compass rose
ccx, ccy = mx1 - 30, my0 + 40
d.ellipse([ccx - 14, ccy - 14, ccx + 14, ccy + 14], outline=INK_SOFT, width=1)
d.polygon([(ccx, ccy - 12), (ccx + 3, ccy), (ccx, ccy + 12), (ccx - 3, ccy)], fill=INK)
d.text((ccx - 3, ccy - 26), "N", font=font(SANSB, 9), fill=INK)

img.save("/home/hatch/workspace/passport-v7-build/passport-page-20261121-bot-v7/entry.png", optimize=True)
import os
print("saved", os.path.getsize("/home/hatch/workspace/passport-v7-build/passport-page-20261121-bot-v7/entry.png"), "bytes")
print("MRZ:", l1, "|", l2)

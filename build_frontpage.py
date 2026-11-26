#!/usr/bin/env python3
"""Build the News Image 26 Nov 2026 front page (1024x1024 PNG) with Pillow.

All text is rendered programmatically with Pillow fonts. All illustrations
(parade balloons, tanker fire, chess board, world map) are drawn with Pillow
shapes. No AI image model is used for any words.

Date discipline: every story on this page happened or was first reported on
26 November 2026 in some time zone (i.e. inside 25 Nov 12:00 UTC - 27 Nov
12:00 UTC). Stories from 24-25 Nov outside that window are excluded and
named in the DATE CHECK footer.
"""
import os
import random
from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
PAPER = (247, 242, 230)
INK = (25, 23, 20)
RED = (163, 32, 32)
OCEAN = (214, 228, 238)
LAND = (232, 220, 194)
GREY = (90, 86, 78)
LIGHTLINE = (200, 192, 172)

FD = "/usr/share/fonts/truetype/dejavu"
FL = "/usr/share/fonts/truetype/liberation"

SERIF_B = f"{FD}/DejaVuSerif-Bold.ttf"
SANS_B = f"{FD}/DejaVuSans-Bold.ttf"
SANS = f"{FD}/DejaVuSans.ttf"
LIB_SERIF = f"{FL}/LiberationSerif-Regular.ttf"
LIB_SERIF_B = f"{FL}/LiberationSerif-Bold.ttf"
LIB_SERIF_I = f"{FL}/LiberationSerif-Italic.ttf"


def font(path, size):
    return ImageFont.truetype(path, int(size))


def wrap(draw, text, fnt, max_w):
    lines = []
    for para in text.split("\n"):
        words = para.split()
        if not words:
            lines.append("")
            continue
        cur = words[0]
        for w in words[1:]:
            trial = cur + " " + w
            if draw.textlength(trial, font=fnt) <= max_w:
                cur = trial
            else:
                lines.append(cur)
                cur = w
        lines.append(cur)
    return lines


def text_block(draw, x, y, w, text, fnt, fill=INK, leading=None, align="left"):
    if leading is None:
        leading = int(fnt.size * 1.32)
    for line in wrap(draw, text, fnt, w):
        lx = x + (w - draw.textlength(line, font=fnt)) / 2 if align == "center" else x
        draw.text((lx, y), line, font=fnt, fill=fill)
        y += leading
    return y


def hline(draw, x0, x1, y, fill=INK, width=1):
    draw.line([(x0, y), (x1, y)], fill=fill, width=width)


def draw_parade(draw, x, y, w, h):
    draw.rectangle([x, y, x + w, y + h], fill=(196, 216, 232))
    draw.ellipse([x + w - 52, y + 6, x + w - 24, y + 34], fill=(246, 214, 120))
    rnd = random.Random(26)
    bx = x
    while bx < x + w - 18:
        bw = rnd.randint(20, 34)
        bh = rnd.randint(h // 3, int(h * 0.62))
        draw.rectangle([bx, y + h - bh, bx + bw, y + h], fill=(58, 62, 70))
        for wy in range(y + h - bh + 6, y + h - 6, 12):
            for wx in range(bx + 4, bx + bw - 4, 9):
                if rnd.random() < 0.5:
                    draw.rectangle([wx, wy, wx + 4, wy + 6], fill=(247, 214, 110))
        bx += bw + 3
    draw.rectangle([x, y + h - 10, x + w, y + h], fill=(120, 116, 108))
    # blue balloon
    cx, cy = x + int(w * 0.20), y + 28
    draw.ellipse([cx - 24, cy - 20, cx + 24, cy + 20], fill=(70, 120, 190), outline=INK, width=2)
    draw.line([(cx, cy + 20), (cx, y + h - 12)], fill=INK, width=1)
    # white balloon + red bow
    cx = x + int(w * 0.50)
    draw.ellipse([cx - 22, y + 14, cx + 22, y + 52], fill=(250, 250, 248), outline=INK, width=2)
    draw.polygon([(cx - 24, y + 10), (cx - 11, y + 16), (cx - 24, y + 22)], fill=RED)
    draw.polygon([(cx + 24, y + 10), (cx + 11, y + 16), (cx + 24, y + 22)], fill=RED)
    draw.line([(cx, y + 52), (cx, y + h - 12)], fill=INK, width=1)
    # gold balloon with ears
    gx, gy = x + int(w * 0.80), y + 30
    draw.ellipse([gx - 15, gy - 22, gx - 2, gy - 9], fill=(214, 164, 60), outline=INK, width=2)
    draw.ellipse([gx + 2, gy - 22, gx + 15, gy - 9], fill=(214, 164, 60), outline=INK, width=2)
    draw.ellipse([gx - 22, gy - 16, gx + 22, gy + 24], fill=(214, 164, 60), outline=INK, width=2)
    draw.line([(gx, gy + 24), (gx, y + h - 12)], fill=INK, width=1)
    cols = [(163, 32, 32), (31, 78, 121), (214, 164, 60), (60, 140, 90)]
    for _ in range(24):
        cx2 = rnd.randint(x + 4, x + w - 4)
        cy2 = rnd.randint(y + 4, y + h - 14)
        draw.ellipse([cx2, cy2, cx2 + 3, cy2 + 3], fill=rnd.choice(cols))


def draw_fire(draw, x, y, w, h):
    draw.rectangle([x, y, x + w, y + h], fill=(38, 32, 30))
    for sx, sy, r in [(0.25, 0.30, 14), (0.38, 0.20, 18), (0.55, 0.28, 12), (0.70, 0.18, 16)]:
        cx, cy = x + int(w * sx), y + int(h * sy)
        draw.ellipse([cx - r, cy - r, cx + r, cy + r], fill=(110, 104, 96))
    draw.rectangle([x + 12, y + h - 30, x + w - 12, y + h - 20], fill=(70, 64, 60))
    draw.ellipse([x + w - 38, y + h - 36, x + w - 12, y + h - 18], fill=(90, 84, 78))
    rnd = random.Random(7)
    base = y + h - 20
    for fx in range(x + 16, x + w - 16, 14):
        fh = rnd.randint(22, 44)
        col = rnd.choice([(240, 120, 20), (250, 170, 30), (220, 60, 20)])
        draw.polygon([(fx, base), (fx + 7, base - fh), (fx + 14, base)], fill=col)
    draw.line([(x, y + h - 7), (x + w, y + h - 7)], fill=(247, 214, 110), width=2)


def draw_chess(draw, x, y, s):
    cell = s // 4
    for r in range(4):
        for c in range(4):
            col = (247, 242, 230) if (r + c) % 2 == 0 else (60, 55, 48)
            draw.rectangle([x + c * cell, y + r * cell, x + (c + 1) * cell, y + (r + 1) * cell],
                           fill=col, outline=INK, width=1)
    def piece(cx, cy, label, bg, fg):
        draw.ellipse([cx - 12, cy - 12, cx + 12, cy + 12], fill=bg, outline=INK, width=2)
        f = font(SERIF_B, 15)
        tw = draw.textlength(label, font=f)
        draw.text((cx - tw / 2, cy - 8), label, font=f, fill=fg)
    piece(x + 2 * cell + cell // 2, y + 2 * cell + cell // 2, "K", (255, 255, 255), INK)
    piece(x + 3 * cell + cell // 2, y + 1 * cell + cell // 2, "Q", (25, 23, 20), (247, 242, 230))


NA = [(-168,66),(-140,70),(-125,72),(-110,73),(-95,80),(-85,80),(-75,73),(-60,62),(-55,52),(-65,45),(-70,42),(-75,35),(-80,32),(-85,30),(-90,21),(-95,19),(-105,20),(-115,28),(-125,40),(-125,49),(-140,60),(-155,58),(-165,60)]
SA = [(-80,10),(-75,10),(-70,12),(-60,8),(-50,0),(-40,-5),(-35,-8),(-40,-20),(-48,-28),(-55,-35),(-65,-40),(-70,-50),(-73,-55),(-75,-40),(-80,-20),(-80,-5)]
AF = [(-17,15),(-10,30),(0,36),(10,37),(20,32),(32,31),(35,28),(38,22),(43,12),(51,11),(48,0),(40,-10),(35,-20),(32,-28),(25,-34),(18,-35),(15,-27),(12,-18),(9,-1),(9,4),(-8,5),(-13,8),(-17,15)]
EURASIA = [(-10,36),(-9,43),(-2,48),(0,50),(5,53),(8,57),(10,59),(18,56),(21,55),(24,58),(28,60),(30,70),(40,68),(50,70),(60,70),(70,72),(80,73),(90,75),(100,77),(110,76),(120,73),(130,72),(140,72),(150,70),(160,66),(170,66),(178,65),(170,60),(160,55),(155,50),(150,45),(142,42),(135,38),(130,35),(127,35),(122,30),(120,25),(115,20),(110,15),(105,10),(100,8),(95,15),(90,22),(85,20),(80,15),(77,8),(75,12),(70,20),(65,25),(60,25),(55,26),(50,29),(45,30),(40,30),(35,30),(30,36),(30,42),(28,45),(23,40),(20,40),(15,44),(12,44),(8,44),(3,42),(0,40),(-5,36)]
AU = [(113,-22),(114,-30),(115,-35),(120,-34),(125,-32),(130,-32),(135,-35),(140,-38),(145,-38),(150,-37),(153,-32),(153,-27),(150,-22),(146,-19),(142,-11),(137,-12),(132,-12),(127,-14),(122,-17),(118,-20)]
GL = [(-45,60),(-40,64),(-30,68),(-22,70),(-25,76),(-35,78),(-50,75),(-55,70),(-58,64),(-53,60)]

MARKERS = [
    # (num, lon, lat, dx, dy) — dx/dy nudge the dot so dense clusters stay readable
    ("1", -74.0, 40.7, 0, 0),     # New York
    ("2", -77.0, 38.9, 14, 12),   # Washington
    ("3", 6.1, 46.2, -16, -8),    # Geneva
    ("4", 35.2, 31.8, -6, 14),    # Jerusalem
    ("5", 21.0, 52.2, 4, -14),    # Warsaw
    ("6", 30.5, 50.4, 18, -4),    # Kyiv
    ("7", 46.7, 24.6, 12, 12),    # Riyadh
    ("8", 51.4, 35.7, 20, 0),     # Tehran
    ("9", 31.2, 30.0, -14, 8),    # Cairo
    ("10", 77.2, 28.6, 8, -12),   # New Delhi
    ("11", 72.9, 19.1, -12, 12),  # Mumbai
    ("12", 149.1, -35.3, 0, 0),   # Canberra
]


def draw_map(draw, x, y, w, h):
    draw.rectangle([x, y, x + w, y + h], fill=OCEAN)
    for lon in range(-150, 181, 30):
        gx = x + (lon + 180) / 360 * w
        draw.line([(gx, y), (gx, y + h)], fill=(190, 208, 222), width=1)
    for lat in range(-60, 91, 30):
        gy = y + (85 - lat) / 145 * h
        draw.line([(x, gy), (x + w, gy)], fill=(190, 208, 222), width=1)

    def proj(lon, lat):
        return (x + (lon + 180) / 360 * w, y + (85 - lat) / 145 * h)

    for poly in (NA, SA, AF, EURASIA, AU, GL):
        draw.polygon([proj(lon, lat) for lon, lat in poly], fill=LAND, outline=(120, 110, 88))
    f = font(SANS_B, 9)
    for num, lon, lat, dx, dy in MARKERS:
        mx, my = proj(lon, lat)
        ox, oy = mx + dx, my + dy
        if dx or dy:
            draw.line([(mx, my), (ox, oy)], fill=(120, 110, 88), width=1)
            draw.ellipse([mx - 2, my - 2, mx + 2, my + 2], fill=RED)
        r = 7
        draw.ellipse([ox - r, oy - r, ox + r, oy + r], fill=RED, outline=(255, 255, 255), width=2)
        tw = draw.textlength(num, font=f)
        draw.text((ox - tw / 2, oy - 5), num, font=f, fill=(255, 255, 255))


def numbers_grid(draw, x, y, w, stats, gap=8):
    """Compact 3x2 grid of (number, label) pairs."""
    draw.text((x, y), "BY THE NUMBERS", font=font(SANS_B, 9), fill=RED)
    y += 13
    hline(draw, x, x + w, y, fill=LIGHTLINE, width=1)
    y += 6
    cw = w / 3
    for i, (num, lab) in enumerate(stats):
        cx = x + (i % 3) * cw
        cy = y + (i // 3) * 28
        nf = font(SERIF_B, 15)
        tw = draw.textlength(num, font=nf)
        draw.text((cx + (cw - tw) / 2, cy), num, font=nf, fill=RED)
        lf = font(SANS_B, 7)
        tw = draw.textlength(lab, font=lf)
        draw.text((cx + (cw - tw) / 2, cy + 17), lab, font=lf, fill=INK)
    return y + 56 + gap


def briefing_panel(draw, x, y, w, items, gap=8):
    """Compact 'in short' panel: bold lead + regular text per item."""
    draw.text((x, y), "BRIEFING", font=font(SANS_B, 9), fill=RED)
    y += 13
    hline(draw, x, x + w, y, fill=LIGHTLINE, width=1)
    y += 5
    bf = font(LIB_SERIF, 11)
    lf = font(SANS_B, 10)
    for lead, rest in items:
        lines = wrap(draw, lead + " " + rest, bf, w - 14)
        first_rest = lines[0][len(lead) + 1:]
        draw.text((x, y), lead, font=lf, fill=INK)
        draw.text((x + draw.textlength(lead + " ", font=lf), y), first_rest, font=bf, fill=INK)
        y += 14
        for line in lines[1:]:
            draw.text((x, y), line, font=bf, fill=INK)
            y += 14
        y += 2
    return y + gap


def panel(draw, x, y, w, kicker, headline, body, hfont, bfont, illus=None, illus_h=50, gap=8):
    draw.text((x, y), kicker, font=font(SANS_B, 9), fill=RED)
    y += 13
    y = text_block(draw, x, y, w, headline, hfont, fill=INK, leading=int(hfont.size * 1.12))
    y += 3
    hline(draw, x, x + w, y, fill=LIGHTLINE, width=1)
    y += 5
    if illus is not None:
        illus(draw, x, y, w, illus_h)
        y += illus_h + 5
    y = text_block(draw, x, y, w, body, bfont, fill=INK, leading=int(bfont.size * 1.30))
    return y + gap


def build():
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)

    # ---------- masthead ----------
    hline(d, 24, 1000, 8, fill=INK, width=3)
    nf = font(SERIF_B, 60)
    name = "THE WORLD TODAY"
    tw = d.textlength(name, font=nf)
    d.text(((W - tw) / 2, 14), name, font=nf, fill=INK)
    d.text((24, 82), "THURSDAY", font=font(SANS_B, 12), fill=INK)
    right = "ONE DAY  •  ONE PAGE  •  30 STORIES"
    d.text((1000 - d.textlength(right, font=font(SANS_B, 12)), 82), right,
           font=font(SANS_B, 12), fill=RED)
    df = font(SERIF_B, 20)
    dl = "26 NOVEMBER 2026"
    tw = d.textlength(dl, font=df)
    d.text(((W - tw) / 2, 82), dl, font=df, fill=INK)
    hline(d, 24, 1000, 106, fill=INK, width=2)
    hline(d, 24, 1000, 109, fill=INK, width=1)

    # ---------- lead headline ----------
    hf = font(SERIF_B, 30)
    head = "TANKER FIRE KILLS 31 ON CAIRO RING ROAD"
    tw = d.textlength(head, font=hf)
    d.text(((W - tw) / 2, 116), head, font=hf, fill=INK)
    deck = "Fireball engulfs 27 vehicles as a fuel tanker explodes at Al-Warraq — 21 injured, 39 ambulances at the scene"
    dif = font(LIB_SERIF_I, 13)
    d.text(((W - d.textlength(deck, font=dif)) / 2, 152), deck, font=dif, fill=GREY)
    hline(d, 24, 1000, 172, fill=INK, width=1)

    # ---------- stat strip ----------
    stats = [
        ("31", "KILLED IN GIZA FIRE"),
        ("-4%", "NASDAQ, INTRADAY"),
        ("$94.61", "BRENT CRUDE"),
        ("100", "MACY'S INFLATABLES"),
        ("43", "CHILDREN REUNITED"),
        ("77", "YEARS OF INDIA'S CONSTITUTION"),
    ]
    sw = 976 / 6
    for i, (num, lab) in enumerate(stats):
        x0 = 24 + i * sw
        if i:
            d.line([(x0, 180), (x0, 206)], fill=LIGHTLINE, width=1)
        nf2 = font(SERIF_B, 22)
        tw = d.textlength(num, font=nf2)
        d.text((x0 + (sw - tw) / 2, 178), num, font=nf2, fill=RED)
        lf = font(SANS_B, 8)
        tw = d.textlength(lab, font=lf)
        d.text((x0 + (sw - tw) / 2, 204), lab, font=lf, fill=INK)
    hline(d, 24, 1000, 216, fill=INK, width=2)

    # ---------- main columns ----------
    col_w = 312
    x1, x2, x3 = 24, 360, 696
    y0 = 226
    HB = font(SERIF_B, 16)
    HB2 = font(SERIF_B, 15)
    BB = font(LIB_SERIF, 11)

    y = y0
    y = panel(d, x1, y, col_w, "EGYPT  •  LEAD", "Fireball on the Ring Road",
              "A fuel tanker exploded on the Cairo Ring Road at Al-Warraq late on Wednesday, sending a fireball across the highway. At least 31 people were killed and 21 injured; 27 vehicles burned and 39 ambulances rushed to the scene. The road has since reopened.",
              HB, BB, illus=draw_fire)
    y = panel(d, x1, y, col_w, "ISRAEL  •  COURTS", "Judges urge dropping of Netanyahu bribery case",
              "Judges in Jerusalem recommended prosecutors drop the bribery charge in Case 4000 — the gravest of three cases against Binyamin Netanyahu — and seek a plea deal on the fraud and breach-of-trust counts. The court also asked prosecutors to reconsider Case 2000.",
              HB2, BB)
    y = panel(d, x1, y, col_w, "POLAND  •  NATO", "Poland seeks no-fly zone at the Ukraine border",
              "Poland says it intends to set up a no-fly zone near its border with Ukraine and has asked NATO allies to help intercept Russian missiles and drones over western Ukraine, after repeated airspace violations.",
              HB2, BB)
    y = briefing_panel(d, x1, y, col_w, [
        ("AUSTRALIA —", "apologised to LGBTQ veterans for past military injustices."),
        ("IRAN —", "suspended the executions of Milad Armoon and Navid Najjaran after an international outcry."),
        ("GAZA —", "health officials warned meningitis is spreading as the health crisis deepens."),
    ])
    col1_bottom = y

    y = y0
    y = panel(d, x2, y, col_w, "UNITED STATES  •  THANKSGIVING", "America gives thanks — 100th Macy's parade",
              "New York marks 100 years of the Macy's parade today: a record 100 inflatables, 18 giant balloons, 29 floats and 10 marching bands step off at 8:30 a.m. But high winds may ground the balloons — gusts above 40 mph are forecast and police decide in the morning. The NFL's traditional triple-header kicks off; Wall Street is shut for the holiday.",
              HB, BB, illus=draw_parade)
    y = panel(d, x2, y, col_w, "CHESS  •  WORLD CHAMPIONSHIP", "Game 3 today as Gukesh–Sindarov level at 1–1",
              "The youngest title match ever — both players are 20 — resumes in Geneva today. Game 2 was drawn in 20 moves. First to 7.5 points over 14 games wins the $2.5m prize fund.",
              HB2, BB)
    y = panel(d, x2, y, col_w, "UNITED STATES  •  DIPLOMACY", "Nine more children home",
              "Nine more Ukrainian and Russian children have been reunited with their families under the White House initiative led by Melania Trump — the seventh round of exchanges, bringing the total to 43.",
              HB2, BB)
    y = panel(d, x2, y, col_w, "WEATHER", "Fog in the north, rain in the south",
              "Dense fog blankets Delhi, Punjab, Haryana and Chandigarh this morning and night, the IMD says. Heavy rain and thunderstorms with gusts of 40–50 kmph are forecast for Kerala, Tamil Nadu and Puducherry. In New York, strong winds threaten the Macy's balloons.",
              HB2, BB)
    col2_bottom = y

    y = y0
    y = panel(d, x3, y, 1000 - x3, "MARKETS  •  AI ROUT", "Nasdaq plunges 4% before pulling back",
              "US stocks suffered their worst November slide since 2008 as AI shares tumbled. The Nasdaq fell as much as 4.15% before closing 0.62% lower; Nvidia lost 8.6%. The sell-off followed the White House tariff plan covering 14 trade partners — including China, Japan, India and the EU — with duties of up to 15% on some goods.",
              HB, BB)
    y = panel(d, x3, y, 1000 - x3, "GULF  •  OIL", "Houthis claim strike on Saudi refinery",
              "Yemen's Houthis claimed a strike on Ras Tanura, the giant Saudi refinery, sending Brent crude to $94.61 — up 3.5%. Saudi forces said they downed four drones. The Houthis also claimed a strike on Riyadh's financial district; two Indians were hurt and Delhi condemned the attack.",
              HB2, BB)
    y = panel(d, x3, y, 1000 - x3, "INDIA  •  CONSTITUTION DAY", "India marks 77 years of its Constitution",
              "Ceremonies across the country mark 77 years since the Constitution was adopted on 26 November 1949. The day also marks 18 years since the 26/11 Mumbai attacks: President Murmu and PM Modi led tributes to the 160-plus victims. Maharashtra held drives at 11 forts and a rally in Thane. A report says Lashkar-e-Taiba has been severely weakened since Operation Sindoor.",
              HB, BB)
    y = numbers_grid(d, x3, y, 1000 - x3, [
        ("27", "VEHICLES BURNED"),
        ("39", "AMBULANCES"),
        ("18", "GIANT BALLOONS"),
        ("29", "FLOATS"),
        ("2.5 mi", "PARADE ROUTE"),
        ("20", "MOVES · GAME 2"),
    ])
    col3_bottom = y

    map_top = max(col1_bottom, col2_bottom, col3_bottom) + 6
    print("columns bottom:", col1_bottom, col2_bottom, col3_bottom, "map_top:", map_top)

    # ---------- world map ----------
    hline(d, 24, 1000, map_top, fill=INK, width=2)
    d.text((24, map_top + 5), "WHERE IT HAPPENED", font=font(SANS_B, 11), fill=RED)
    d.text((1000 - d.textlength("12 PLACES, ONE DAY", font=font(SANS_B, 9)), map_top + 6),
           "12 PLACES, ONE DAY", font=font(SANS_B, 9), fill=GREY)
    map_y = map_top + 22
    map_h = 100
    draw_map(d, 24, map_y, 976, map_h)
    legend = "1 New York  •  2 Washington  •  3 Geneva  •  4 Jerusalem  •  5 Warsaw  •  6 Kyiv  •  7 Riyadh  •  8 Tehran  •  9 Cairo  •  10 New Delhi  •  11 Mumbai  •  12 Canberra"
    lf = font(SANS, 9)
    tw = d.textlength(legend, font=lf)
    d.text(((W - tw) / 2, map_y + map_h + 3), legend, font=lf, fill=GREY)

    # ---------- ALSO ON ----------
    also_top = map_y + map_h + 18
    hline(d, 24, 1000, also_top, fill=INK, width=1)
    d.text((24, also_top + 4), "ALSO ON…", font=font(SANS_B, 11), fill=RED)
    also_items = [
        "Giza: 39 ambulances at the scene; hospitals on alert",
        "Beige Book: modest US growth, wage gains",
        "Parade: new balloons include Bluey and Hello Kitty",
        "NFL: Detroit and Dallas host the holiday games",
        "Ukraine hits two more Russian refineries",
        "Fog in Delhi and Punjab; rain in Kerala, Tamil Nadu",
        "Parade route: 2.5 miles, Central Park West to Herald Square",
        "Putin vows retaliation after refinery strikes",
        "Ukraine: 14 refineries struck since 1 November",
        "Thanksgiving: NBC broadcasts the parade 8:30 a.m.–noon",
    ]
    af = font(SANS, 10)
    y_a = also_top + 20
    y_b = also_top + 20
    for i, item in enumerate(also_items):
        if i % 2 == 0:
            d.text((24, y_a), "•  " + item, font=af, fill=INK)
            y_a += 14
        else:
            d.text((512, y_b), "•  " + item, font=af, fill=INK)
            y_b += 14
    also_bottom = max(y_a, y_b)

    # ---------- DATE CHECK footer ----------
    foot_top = also_bottom + 6
    hline(d, 24, 1000, foot_top, fill=RED, width=2)
    d.text((24, foot_top + 5), "DATE CHECK", font=font(SANS_B, 9), fill=RED)
    dc = ("Every story above happened or was first reported on 26 November 2026 in some time zone. "
          "NOT yesterday's news — excluded with their true dates: Shenzhou-24 launch (25 Nov), Colombia supermarket "
          "rescue (25 Nov), Bangladesh garment wage (25 Nov), Russia 500,000-dead leak (25 Nov), Hera asteroid photos "
          "(25 Nov), Solomon Islands treaty (25 Nov), North Korea expels Swiss envoy (25 Nov), turkey pardon — "
          "Freedom & Feathers (24 Nov), Lukashenko offer (24 Nov), Sooryavanshi 204 (24 Nov), IPL register (25 Nov), "
          "Antarctica quake (25 Nov).  •  THE WORLD TODAY — one day, one page.")
    y = text_block(d, 24, foot_top + 18, 976, dc, font(SANS, 9), fill=INK, leading=12)
    print("footer bottom:", y, "image H:", H)
    assert y <= 1022, f"OVERFLOW: footer ends at {y}"
    return img


if __name__ == "__main__":
    out_dir = os.path.dirname(os.path.abspath(__file__))
    img = build()
    img.save(os.path.join(out_dir, "entry.png"), optimize=True)
    print("saved entry.png", os.path.getsize(os.path.join(out_dir, "entry.png")), "bytes")

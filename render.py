#!/usr/bin/env python3
"""Render the news-image entry for Tuesday 24 November 2026.

Draws one 1024x1024 newspaper front page with PIL and saves entry.png.
All text and art are drawn from the STORIES data below (researched from
Reuters, AP, AFP, Al Jazeera, The Guardian, Xinhua, DW, Daily Summary Of,
Motley Fool / Investopedia market closes, 24-25 Nov 2026).

Layout follows the winning front-page pattern: giant date masthead,
stat strip, colour-coded region bar, UTC timeline, 3 features + 10 tiles
each with a verification chip and source, a world map with numbered pins,
an ALSO list, and a DATE CHECK box naming what was left out and why.
"""
import os
from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "entry.png")

# ---------------------------------------------------------------- fonts
FD = "/usr/share/fonts/truetype/dejavu"
NOTO = "/usr/share/fonts/truetype/noto"


def font(name, size):
    for p in (os.path.join(FD, name), os.path.join(NOTO, name)):
        if os.path.exists(p):
            return ImageFont.truetype(p, size)
    return ImageFont.load_default(size)


def F_serif(size):
    return font("DejaVuSerif-Bold.ttf", size)


def F_serif_reg(size):
    return font("DejaVuSerif.ttf", size)


def F_sans(size):
    return font("DejaVuSans.ttf", size)


def F_sans_b(size):
    return font("DejaVuSans-Bold.ttf", size)


# ---------------------------------------------------------------- palette
PAPER = (247, 242, 231)
INK = (26, 26, 26)
NAVY = (22, 35, 63)
NAVY_LT = (38, 54, 92)
RED = (176, 30, 36)
RED_DK = (140, 20, 26)
GOLD = (184, 134, 11)
GREEN = (34, 110, 58)
BLUE = (31, 78, 121)
TEAL = (0, 131, 143)
PURPLE = (106, 27, 154)
BROWN = (146, 90, 16)
GREY = (85, 85, 85)
LINE = (120, 110, 95)
SEA = (214, 228, 238)
LAND = (232, 214, 178)
LAND_EDGE = (190, 168, 128)

REGION_COLORS = {
    "EUROPE": (31, 78, 121),
    "MIDDLE EAST": (180, 83, 9),
    "AMERICAS": (46, 125, 50),
    "ASIA-PACIFIC": (198, 40, 40),
    "AFRICA": (106, 27, 154),
    "OCEANIA": (0, 131, 143),
    "WORLD": (85, 85, 85),
}

CHIP_STYLE = {
    "CONFIRMED": (GREEN, "CONFIRMED"),
    "OFFICIAL": (BROWN, "OFFICIAL"),
    "REPORTED": (BLUE, "REPORTED"),
    "CLAIM": (RED, "CLAIM"),
}


# ---------------------------------------------------------------- helpers
def tw(draw, text, fnt, max_w):
    """Wrap text to fit max_w; returns list of lines."""
    words = text.split()
    lines, cur = [], ""
    for w in words:
        trial = (cur + " " + w).strip()
        if draw.textlength(trial, font=fnt) <= max_w:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines


def text_h(draw, lines, fnt, leading):
    return len(lines) * leading


def draw_chip(draw, x, y, status, fnt=None):
    """Small outlined status chip; returns its width."""
    fnt = fnt or F_sans_b(9)
    color, label = CHIP_STYLE[status]
    w = int(draw.textlength(label, font=fnt)) + 10
    h = 14
    draw.rounded_rectangle([x, y, x + w, y + h], radius=3,
                           outline=color, width=1)
    draw.text((x + 5, y + 2), label, font=fnt, fill=color)
    return w


def num_badge(draw, cx, cy, n, r=10):
    draw.ellipse([cx - r, cy - r, cx + r, cy + r], fill=NAVY)
    f = F_sans_b(11)
    t = str(n)
    draw.text((cx - draw.textlength(t, font=f) / 2, cy - 6), t,
              font=f, fill=(255, 255, 255))


def rule(draw, x0, x1, y, w=1, color=INK):
    draw.line([(x0, y), (x1, y)], fill=color, width=w)


# ---------------------------------------------------------------- stories
# Each story: (num, region, place, category, status, source, headline, deck)
FEATURES = [
    (1, "MIDDLE EAST", "STRAIT OF HORMUZ", "WAR AT SEA", "CLAIM", "IRNA · IRIB",
     "Four tankers hit mines in the strait",
     "Iran's navy says four tankers struck mines and caught fire east of "
     "Hormuz. The joint maritime centre says the claims are unconfirmed. "
     "(IRNA · IRIB)"),
    (2, "AMERICAS", "NEW YORK", "TECH · COURTS", "CONFIRMED", "Reuters · AP",
     "Huawei guilty on 10 counts",
     "A US jury convicts Huawei of trade secrets and bank fraud, "
     "but clears it of racketeering. Sentencing is set for September 2027. "
     "(Reuters · AP)"),
    (3, "MIDDLE EAST", "RIYADH", "WAR · SAUDI ARABIA", "CONFIRMED", "Reuters · AFP",
     "Riyadh tower struck again",
     "A suspected Houthi drone attack hits the PIF tower in the capital's "
     "financial district, wounding 11 — the second strike in a week. "
     "(Reuters · AFP)"),
]

TILES = [
    (4, "EUROPE", "GULF OF FINLAND · LIBYA", "WAR", "CONFIRMED", "Reuters",
     "Ukraine strikes Russian ships at sea",
     "Kyiv: drones hit the Sparta II in the Gulf of Finland and a corvette off Libya."),
    (5, "AMERICAS", "WALL STREET", "MARKETS", "CONFIRMED", "Reuters · Fool",
     "Nvidia rally fizzles in a day",
     "Shares fall 5.86% to $155.38 after Monday's 31.5% surge. Nasdaq drops 1.48%."),
    (6, "AMERICAS", "CARTAGENA, COLOMBIA", "CRIME", "CONFIRMED", "AP",
     "25 held hostage in supermarket",
     "Gunmen seize a Cartagena store, hold 25 people. Five older women are freed."),
    (7, "MIDDLE EAST", "ADEN, YEMEN", "WAR", "REPORTED", "Reuters",
     "Houthis 60 km from Aden",
     "Yemen's military: Houthi fighters are 60 km from Aden and ready to attack."),
    (8, "WORLD", "THE HAGUE", "LAW", "CONFIRMED", "Reuters · AP",
     "Myanmar guilty of genocide",
     "The world court rules 9-6: Myanmar's forces committed genocide in 2017."),
    (9, "MIDDLE EAST", "GAZA", "WAR", "CONFIRMED", "Reuters",
     "Hamas security chief killed",
     "An Israeli strike kills Hamas's internal security chief; six others die."),
    (10, "EUROPE", "ESKISEHIR, TURKIYE", "ACCIDENT", "OFFICIAL", "Anadolu",
     "Helicopter crash kills five",
     "A Turkish Air Force helicopter goes down after take-off on a training flight."),
    (11, "MIDDLE EAST", "BAGHDAD", "OIL", "OFFICIAL", "Reuters",
     "Baghdad takes the oilfields",
     "Iraq's PM orders federal control of oilfields and crossings in Kurdish areas."),
    (12, "AFRICA", "DAKAR", "FOOTBALL", "CONFIRMED", "Reuters",
     "Senegal's title restored",
     "Court reinstates Senegal as Africa Cup champions, overturning the award."),
    (13, "EUROPE", "BOLOGNA, ITALY", "TENNIS", "CONFIRMED", "ATP",
     "Davis Cup opens in Bologna",
     "Czechia beats Canada 2-0 in the first quarter-final. Italy play Wednesday."),
]

ALSO = [
    (14, "EUROPE", "London", "UK sanctions Houthis and four senior officials", "OFFICIAL"),
    (15, "MIDDLE EAST", "Lahj", "Saudi strikes on buses, trucks: 25 dead or missing", "REPORTED"),
    (16, "MIDDLE EAST", "Gaza", "Meningitis alert: 272 cases in October, 15 dead this year", "OFFICIAL"),
    (17, "AFRICA", "DR Congo", "Plane missing; rebels claim they shot it down", "CLAIM"),
    (18, "ASIA-PACIFIC", "Hanoi", "Hotpot restaurant blast kills at least six", "REPORTED"),
    (19, "ASIA-PACIFIC", "Kuala Lumpur", "Malaysia to return thousands to Myanmar", "OFFICIAL"),
    (20, "ASIA-PACIFIC", "Seoul", "Shelter alert on Ulleungdo as Russian jets approach", "OFFICIAL"),
    (21, "ASIA-PACIFIC", "Dhaka", "Hasina plans return from exile on 16 December", "REPORTED"),
    (22, "ASIA-PACIFIC", "Beijing", "China sentences official to death for spying", "REPORTED"),
    (23, "EUROPE", "Brussels", "NATO vows space defence; Tripoli questions Kyiv", "OFFICIAL"),
    (24, "AMERICAS", "Mexico City", "US drone helped catch El Chapo Isidro", "OFFICIAL"),
    (25, "AMERICAS", "San Salvador", "Bukele names 3 soldiers killed in Haiti", "OFFICIAL"),
    (26, "AMERICAS", "Washington", "Pentagon rebukes Canada on defence, F-35", "OFFICIAL"),
    (27, "AMERICAS", "Washington", "US blacklists Megaspeed in Nvidia scandal", "OFFICIAL"),
    (28, "EUROPE", "Kyiv", "Zelensky urges four-party talks with Russia, US, Europe", "REPORTED"),
    (29, "ASIA-PACIFIC", "Jakarta", "Indonesia names two candidates to replace the VP", "OFFICIAL"),
    (30, "EUROPE", "Strasbourg", "States may expel migrants in border emergencies", "OFFICIAL"),
    (31, "AMERICAS", "Villavicencio", "Car bomb outside regional offices injures 23", "REPORTED"),
    (32, "EUROPE", "Brussels", "EU imposes import quotas on hybrid vehicles", "OFFICIAL"),
    (33, "EUROPE", "Madrid", "Real Madrid 5-1 PSV in the Champions League", "CONFIRMED"),
    (34, "EUROPE", "Geneva", "Chess title match opens: Gukesh draws Sindarov", "REPORTED"),
    (35, "MIDDLE EAST", "Ankara", "Haftar visits Turkey for the first time", "REPORTED"),
    (36, "OCEANIA", "Sydney", "Australia threatens Big Tech with 5% revenue fines", "OFFICIAL"),
]

REGION_COUNTS = [
    ("EUROPE", 10), ("MIDDLE EAST", 8), ("AMERICAS", 8),
    ("ASIA-PACIFIC", 6), ("AFRICA", 2), ("OCEANIA", 1), ("WORLD", 1),
]

STATS = [
    ("4", "tankers hit mines\nin the strait"),
    ("10 of 12", "counts Huawei\nconvicted on"),
    ("-5.86%", "Nvidia's fall\nin one day"),
    ("25", "hostages held\nin Cartagena"),
    ("11", "wounded in the\nRiyadh tower hit"),
    ("5", "air crew killed\nin Turkiye crash"),
]

TIMELINE = [
    ("00:00", "4 tankers hit"),
    ("02:15", "NATO space vow"),
    ("08:14", "Ships struck"),
    ("11:40", "Hamas chief killed"),
    ("14:27", "Riyadh tower hit"),
    ("20:41", "Huawei verdict"),
]

# ------------------------------------------------------- illustrations
# Every scene draws sky, ground, a recognisable object and small people /
# vehicles / details. All coordinates are fractions of the given box so the
# same scene works at feature size (~326x112) and tile size (~195x60).

def sky_bands(draw, x, y, w, h, top, bot):
    n = max(2, int(h / 4))
    for i in range(n):
        t = i / (n - 1)
        c = tuple(int(top[k] + (bot[k] - top[k]) * t) for k in range(3))
        draw.rectangle([x, y + i * h / n, x + w, y + (i + 1) * h / n + 1],
                       fill=c)


def person(draw, x, y, s, color):
    draw.ellipse([x - 0.35 * s, y - 1.9 * s, x + 0.35 * s, y - 1.2 * s],
                 fill=color)
    draw.rectangle([x - 0.4 * s, y - 1.2 * s, x + 0.4 * s, y], fill=color)
    draw.rectangle([x - 0.35 * s, y, x - 0.05 * s, y + 0.9 * s], fill=color)
    draw.rectangle([x + 0.05 * s, y, x + 0.35 * s, y + 0.9 * s], fill=color)


def flames(draw, x, y, s):
    for dx, ds, col in ((-0.5, 0.9, (255, 140, 0)), (0.2, 1.1, (255, 90, 0)),
                        (-0.1, 0.7, (255, 200, 60))):
        draw.polygon([(x + dx * s - 0.5 * ds * s, y),
                      (x + dx * s, y - 1.6 * ds * s),
                      (x + dx * s + 0.5 * ds * s, y)], fill=col)


def smoke(draw, x, y, s, n=4, top=None):
    for i in range(n):
        r = s * (0.5 + 0.35 * i)
        x1 = x - r + i * s * 0.55
        y1 = y - i * s * 0.8 - r
        x2 = x + r + i * s * 0.55
        y2 = y - i * s * 0.8 + r
        if top is not None:
            y1 = max(y1, top)
        draw.ellipse([x1, y1, x2, y2], fill=(120, 120, 125))


def scene_hormuz(draw, x, y, w, h):
    # Dusk sky: deep blue to a warm fire-lit horizon glow above the sea.
    sky_bands(draw, x, y, w, h * 0.55, (16, 26, 54), (88, 92, 122))
    draw.rectangle([x, y + h * 0.46, x + w, y + h * 0.55],
                   fill=(214, 130, 52))
    draw.rectangle([x, y + h * 0.52, x + w, y + h * 0.55],
                   fill=(238, 170, 80))
    # stars + moon, all below the feature label bar (top 18 px)
    for sx, sy in ((0.10, 0.24), (0.24, 0.30), (0.55, 0.22),
                   (0.70, 0.28), (0.90, 0.36), (0.38, 0.36)):
        draw.ellipse([x + w * sx, y + h * sy, x + w * sx + 2,
                      y + h * sy + 2], fill=(240, 240, 220))
    mx0, my0 = x + w * 0.84, y + h * 0.26
    draw.ellipse([mx0 - 9, my0 - 9, mx0 + 9, my0 + 9],
                 fill=(210, 200, 160))
    draw.ellipse([mx0 - 5, my0 - 5, mx0 + 5, my0 + 5],
                 fill=(246, 240, 214))
    sea_y = y + h * 0.55
    draw.rectangle([x, sea_y, x + w, y + h], fill=(20, 46, 78))
    for i in range(5):
        yy = sea_y + h * 0.07 + i * h * 0.075
        draw.arc([x + w * 0.05, yy - 3, x + w * 0.35, yy + 3], 0, 180,
                 fill=(100, 140, 180))
        draw.arc([x + w * 0.60, yy - 3, x + w * 0.95, yy + 3], 0, 180,
                 fill=(100, 140, 180))
    # tiny distant ship on the horizon in the gap between the tankers
    gx0, gy0 = x + w * 0.485, sea_y - h * 0.05
    draw.rectangle([gx0, gy0, gx0 + w * 0.06, gy0 + h * 0.04],
                   fill=(36, 40, 48))
    draw.rectangle([gx0 + w * 0.035, gy0 - h * 0.03, gx0 + w * 0.05, gy0],
                   fill=(36, 40, 48))
    draw.rectangle([gx0 + w * 0.01, gy0 + h * 0.01, gx0 + w * 0.02,
                    gy0 + h * 0.03], fill=(255, 214, 120))
    draw.rectangle([gx0 + w * 0.04, gy0 + h * 0.01, gx0 + w * 0.05,
                    gy0 + h * 0.03], fill=(255, 214, 120))
    # tanker 1 (left) with fire: hull, red waterline, white superstructure
    # with lit windows, red funnel, flames + reflection on the water
    tx, ty, tw, th = x + w * 0.05, sea_y - h * 0.17, w * 0.42, h * 0.18
    draw.rectangle([tx, ty, tx + tw, ty + th], fill=(36, 36, 42))
    draw.rectangle([tx, ty + th - 3, tx + tw, ty + th], fill=(150, 30, 30))
    draw.rectangle([tx + tw * 0.62, ty - h * 0.16, tx + tw * 0.90, ty],
                   fill=(225, 225, 215))
    for i in range(3):
        draw.rectangle([tx + tw * (0.66 + i * 0.08), ty - h * 0.13,
                        tx + tw * (0.70 + i * 0.08), ty - h * 0.08],
                       fill=(255, 200, 90))
    draw.rectangle([tx + tw * 0.78, ty - h * 0.22, tx + tw * 0.88,
                    ty - h * 0.16], fill=(150, 40, 30))
    flames(draw, tx + tw * 0.35, ty, h * 0.11)
    for i in range(3):
        draw.rectangle([tx + tw * (0.28 + i * 0.06), ty + th + 2 + i * 3,
                        tx + tw * (0.40 + i * 0.06), ty + th + 5 + i * 3],
                       fill=(255, 140, 40))
    smoke(draw, tx + tw * 0.35, ty - h * 0.14, h * 0.07, top=y + 2)
    # tanker 2 (right) with lit bridge windows + fire
    tx2, ty2 = x + w * 0.55, sea_y - h * 0.13
    draw.rectangle([tx2, ty2, tx2 + tw * 0.8, ty2 + th * 0.85],
                   fill=(48, 48, 54))
    draw.rectangle([tx2 + tw * 0.10, ty2 - h * 0.12, tx2 + tw * 0.30, ty2],
                   fill=(220, 220, 210))
    for i in range(2):
        draw.rectangle([tx2 + tw * (0.13 + i * 0.07), ty2 - h * 0.09,
                        tx2 + tw * (0.17 + i * 0.07), ty2 - h * 0.05],
                       fill=(255, 200, 90))
    flames(draw, tx2 + tw * 0.45, ty2, h * 0.09)
    # patrol boat (foreground right) with lit cabin window + wake
    bx, by = x + w * 0.78, sea_y + h * 0.22
    draw.polygon([(bx, by), (bx + w * 0.16, by),
                  (bx + w * 0.13, by + h * 0.07),
                  (bx + w * 0.03, by + h * 0.07)], fill=(200, 200, 195))
    draw.rectangle([bx + w * 0.05, by - h * 0.06, bx + w * 0.11, by],
                   fill=(90, 100, 110))
    draw.rectangle([bx + w * 0.065, by - h * 0.05, bx + w * 0.095,
                    by - h * 0.02], fill=(255, 214, 120))
    draw.line([(bx, by + h * 0.07), (bx - w * 0.10, by + h * 0.10)],
              fill=(180, 200, 220), width=2)
    # spiked mine in the water: splash ring, highlight, warning buoy + flag
    mx, my, mr = x + w * 0.46, y + h * 0.84, h * 0.085
    draw.ellipse([mx - mr * 1.5, my - mr * 0.4, mx + mr * 1.5,
                  my + mr * 0.4], outline=(200, 220, 235), width=2)
    for a in range(0, 360, 45):
        import math
        dx, dy = math.cos(math.radians(a)), math.sin(math.radians(a))
        draw.line([(mx, my), (mx + dx * mr * 1.7, my + dy * mr * 1.7)],
                  fill=(15, 15, 15), width=2)
    draw.ellipse([mx - mr, my - mr, mx + mr, my + mr], fill=(18, 18, 18))
    draw.arc([mx - mr * 0.7, my - mr * 0.7, mx + mr * 0.1, my + mr * 0.1],
             200, 320, fill=(140, 140, 140), width=2)
    ux, uy = x + w * 0.62, y + h * 0.86
    draw.ellipse([ux - 5, uy - 4, ux + 5, uy + 4], fill=(220, 60, 40))
    draw.line([(ux, uy - 4), (ux, uy - h * 0.12)], fill=(40, 40, 40),
              width=2)
    draw.polygon([(ux, uy - h * 0.12), (ux + w * 0.05, uy - h * 0.09),
                  (ux, uy - h * 0.06)], fill=(220, 60, 40))
    # restricted zone dashed line
    for i in range(6):
        draw.line([(x + w * 0.04 + i * w * 0.16, y + h * 0.94),
                   (x + w * 0.04 + (i + 0.5) * w * 0.16, y + h * 0.94)],
                  fill=(255, 80, 80), width=2)


def scene_huawei(draw, x, y, w, h):
    # Light courtroom wall so the dark judge figure contrasts (old version
    # was dark brown on dark brown, so the judge vanished at small size).
    sky_bands(draw, x, y, w, h * 0.62, (233, 214, 178), (214, 190, 150))
    # wood bench + top edge
    draw.rectangle([x, y + h * 0.62, x + w, y + h], fill=(96, 62, 32))
    draw.rectangle([x, y + h * 0.58, x + w, y + h * 0.64], fill=(120, 78, 42))
    # tall windows with lit panes + white mullions (the detail that reads
    # at judge size, same lesson as the Riyadh tower's lit windows)
    for wx0, wx1 in ((0.03, 0.19), (0.81, 0.97)):
        draw.rectangle([x + w * wx0, y + h * 0.20, x + w * wx1,
                        y + h * 0.58], fill=(52, 74, 128),
                       outline=(240, 230, 210), width=2)
        draw.rectangle([x + w * wx0 + 2, y + h * 0.44, x + w * wx1 - 2,
                        y + h * 0.58], fill=(255, 196, 90))
        draw.line([(x + w * (wx0 + wx1) / 2, y + h * 0.20),
                   (x + w * (wx0 + wx1) / 2, y + h * 0.58)],
                  fill=(240, 230, 210), width=2)
        draw.line([(x + w * wx0, y + h * 0.32), (x + w * wx1, y + h * 0.32)],
                  fill=(240, 230, 210), width=2)
        draw.line([(x + w * wx0, y + h * 0.44), (x + w * wx1, y + h * 0.44)],
                  fill=(240, 230, 210), width=2)
    # document on the wall (centre-left)
    dw, dh = w * 0.13, h * 0.30
    dx, dy = x + w * 0.23, y + h * 0.22
    draw.rectangle([dx, dy, dx + dw, dy + dh], fill=(250, 248, 240),
                   outline=(60, 60, 60))
    for i in range(3):
        draw.line([(dx + dw * 0.12, dy + dh * (0.25 + i * 0.2)),
                   (dx + dw * 0.88, dy + dh * (0.25 + i * 0.2))],
                  fill=(140, 140, 140), width=1)
    # gold seal above the judge
    sx, sy, sr = x + w * 0.50, y + h * 0.26, h * 0.055
    draw.ellipse([sx - sr, sy - sr, sx + sr, sy + sr], fill=(184, 134, 11),
                 outline=(120, 85, 20), width=2)
    draw.ellipse([sx - sr * 0.55, sy - sr * 0.55, sx + sr * 0.55,
                  sy + sr * 0.55], outline=(120, 85, 20), width=1)
    # judge figure, centre: dark robe on the light wall, skin face,
    # white collar — now readable instead of dark-on-dark
    jx = x + w * 0.50
    draw.rectangle([jx - w * 0.06, y + h * 0.44, jx + w * 0.06,
                    y + h * 0.62], fill=(22, 22, 28))
    draw.polygon([(jx - w * 0.02, y + h * 0.44), (jx + w * 0.02,
                  y + h * 0.44), (jx, y + h * 0.50)], fill=(250, 250, 250))
    draw.ellipse([jx - w * 0.032, y + h * 0.33, jx + w * 0.032,
                  y + h * 0.43], fill=(222, 184, 152))
    draw.arc([jx - w * 0.032, y + h * 0.33, jx + w * 0.032, y + h * 0.40],
             180, 360, fill=(90, 80, 70), width=3)
    # lawyer standing at right, behind the bench, with a lectern
    lx = x + w * 0.70
    draw.rectangle([lx - w * 0.035, y + h * 0.50, lx + w * 0.035,
                    y + h * 0.62], fill=(38, 38, 48))
    draw.ellipse([lx - w * 0.022, y + h * 0.42, lx + w * 0.022,
                  y + h * 0.50], fill=(210, 170, 140))
    draw.rectangle([lx - w * 0.035, y + h * 0.50, lx + w * 0.035,
                    y + h * 0.53], fill=(250, 250, 250))
    draw.polygon([(lx - w * 0.05, y + h * 0.62), (lx + w * 0.05,
                  y + h * 0.62), (lx + w * 0.03, y + h * 0.56),
                  (lx - w * 0.03, y + h * 0.56)], fill=(120, 80, 45))
    # gavel on the bench (right)
    draw.rectangle([x + w * 0.80, y + h * 0.50, x + w * 0.94, y + h * 0.54],
                   fill=(150, 100, 50))
    draw.line([(x + w * 0.87, y + h * 0.54), (x + w * 0.87, y + h * 0.62)],
              fill=(150, 100, 50), width=3)
    # bench front panels
    for i in range(5):
        px = x + w * (0.08 + i * 0.18)
        draw.line([(px, y + h * 0.68), (px, y + h * 0.96)],
                  fill=(70, 45, 22), width=2)
    # GUILTY stamp, drawn last so it sits on top; paper-white backing
    # inside the outline so the red text reads on any background.
    # Both lines fit inside the rect with margins (the old 0.24h/0.34h
    # spacing put the second line on top of the bottom outline).
    draw.rectangle([x + w * 0.58, y + h * 0.20, x + w * 0.95, y + h * 0.42],
                   fill=(250, 248, 240), outline=(176, 30, 36), width=3)
    f = F_sans_b(max(10, int(h * 0.11)))
    draw.text((x + w * 0.62, y + h * 0.215), "GUILTY", font=f, fill=RED)
    f2 = F_sans_b(max(9, int(h * 0.09)))
    draw.text((x + w * 0.62, y + h * 0.315), "10 OF 12", font=f2, fill=RED)


def scene_riyadh(draw, x, y, w, h):
    sky_bands(draw, x, y, w, h * 0.7, (14, 20, 44), (58, 74, 118))
    for sx, sy in ((0.12, 0.12), (0.35, 0.06), (0.62, 0.10), (0.88, 0.05)):
        draw.ellipse([x + w * sx, y + h * sy, x + w * sx + 2, y + h * sy + 2],
                     fill=(240, 240, 220))
    base = y + h * 0.92
    # side towers
    for tx, tw, th, col in ((0.02, 0.16, 0.45, (30, 38, 64)),
                            (0.20, 0.12, 0.60, (36, 46, 76)),
                            (0.78, 0.14, 0.52, (30, 38, 64)),
                            (0.90, 0.09, 0.38, (36, 46, 76))):
        draw.rectangle([x + w * tx, base - h * th, x + w * (tx + tw), base],
                       fill=col)
    # PIF tower (centre, tallest, twisted top)
    tx, tw = x + w * 0.40, w * 0.30
    draw.polygon([(tx, base), (tx, y + h * 0.10),
                  (tx + tw * 0.75, y + h * 0.04),
                  (tx + tw, y + h * 0.10), (tx + tw, base)], fill=(52, 66, 104))
    # lit windows on the tower
    for r in range(6):
        for c in range(4):
            if (r + c) % 2 == 0:
                draw.rectangle([tx + w * 0.05 + c * w * 0.06,
                                y + h * (0.16 + r * 0.11),
                                tx + w * 0.08 + c * w * 0.06,
                                y + h * (0.20 + r * 0.11)],
                               fill=(255, 214, 120))
    # fire at the top
    flames(draw, tx + tw * 0.5, y + h * 0.24, h * 0.09)
    smoke(draw, tx + tw * 0.5, y + h * 0.16, h * 0.05, top=y + 2)
    # street
    draw.rectangle([x, base, x + w, y + h], fill=(24, 24, 30))
    for i in range(4):
        draw.ellipse([x + w * (0.1 + i * 0.25), base + h * 0.03,
                      x + w * (0.1 + i * 0.25) + 3, base + h * 0.03 + 3],
                     fill=(255, 200, 80))


def scene_ships(draw, x, y, w, h):
    sky_bands(draw, x, y, w, h * 0.5, (120, 150, 180), (200, 210, 215))
    draw.ellipse([x + w * 0.80, y + h * 0.08, x + w * 0.88, y + h * 0.16],
                 fill=(250, 240, 200))
    sea_y = y + h * 0.5
    draw.rectangle([x, sea_y, x + w, y + h], fill=(36, 74, 110))
    for i in range(4):
        yy = sea_y + h * 0.10 + i * h * 0.10
        draw.arc([x + w * 0.08, yy - 3, x + w * 0.45, yy + 3], 0, 180,
                 fill=(120, 160, 195))
    # warship silhouette
    sx, sy = x + w * 0.08, sea_y - h * 0.10
    draw.polygon([(sx, sy + h * 0.14), (sx + w * 0.55, sy + h * 0.14),
                  (sx + w * 0.50, sy + h * 0.26), (sx + w * 0.05, sy + h * 0.26)],
                 fill=(52, 58, 64))
    draw.rectangle([sx + w * 0.12, sy - h * 0.02, sx + w * 0.34, sy + h * 0.14],
                   fill=(52, 58, 64))
    draw.rectangle([sx + w * 0.20, sy - h * 0.12, sx + w * 0.24, sy - h * 0.02],
                   fill=(52, 58, 64))
    smoke(draw, sx + w * 0.22, sy - h * 0.14, h * 0.06, top=y + 2)
    # drone boat
    bx, by = x + w * 0.68, sea_y + h * 0.16
    draw.polygon([(bx, by), (bx + w * 0.22, by), (bx + w * 0.18, by + h * 0.10),
                  (bx + w * 0.04, by + h * 0.10)], fill=(30, 30, 34))
    draw.line([(bx + w * 0.11, by), (bx + w * 0.11, by - h * 0.16)],
              fill=(30, 30, 34), width=2)
    draw.ellipse([bx + w * 0.08, by - h * 0.20, bx + w * 0.14, by - h * 0.14],
                 fill=(200, 40, 40))


def scene_nvidia(draw, x, y, w, h):
    draw.rectangle([x, y, x + w, y + h], fill=(14, 22, 34))
    # grid
    for i in range(1, 5):
        draw.line([(x + w * i / 5, y), (x + w * i / 5, y + h)],
                  fill=(28, 42, 62), width=1)
    # chip
    cx, cy, cs = x + w * 0.16, y + h * 0.30, h * 0.42
    for k in range(4):
        draw.line([(cx - cs * 0.15, cy + k * cs * 0.28),
                   (cx - cs * 0.45, cy + k * cs * 0.28)], fill=(120, 200, 120),
                  width=2)
        draw.line([(cx + cs + cs * 0.15, cy + k * cs * 0.28),
                   (cx + cs + cs * 0.45, cy + k * cs * 0.28)],
                  fill=(120, 200, 120), width=2)
    draw.rectangle([cx, cy, cx + cs, cy + cs], fill=(34, 130, 70),
                   outline=(140, 220, 150), width=2)
    draw.rectangle([cx + cs * 0.28, cy + cs * 0.28, cx + cs * 0.72,
                    cy + cs * 0.72], outline=(200, 240, 200), width=2)
    # falling red chart
    pts = []
    for i in range(7):
        px = x + w * (0.42 + i * 0.09)
        py = y + h * (0.22 + i * 0.11 + (0.05 if i % 2 else 0))
        pts.append((px, py))
    draw.line(pts, fill=(255, 70, 60), width=3, joint="curve")
    draw.polygon(pts + [(pts[-1][0], y + h * 0.92), (pts[0][0], y + h * 0.92)],
                 fill=(255, 70, 60))
    f = F_sans_b(max(10, int(h * 0.16)))
    draw.text((x + w * 0.44, y + h * 0.06), "-5.86%", font=f, fill=(255, 90, 80))

def scene_cartagena(draw, x, y, w, h):
    sky_bands(draw, x, y, w, h * 0.45, (140, 170, 205), (205, 215, 225))
    # supermarket block
    draw.rectangle([x + w * 0.06, y + h * 0.30, x + w * 0.94, y + h * 0.88],
                   fill=(240, 235, 220), outline=(90, 80, 70))
    # striped awning
    for i in range(8):
        col = (176, 30, 36) if i % 2 == 0 else (250, 248, 240)
        draw.polygon([(x + w * (0.06 + i * 0.11), y + h * 0.30),
                      (x + w * (0.06 + (i + 1) * 0.11), y + h * 0.30),
                      (x + w * (0.06 + (i + 1) * 0.11), y + h * 0.44),
                      (x + w * (0.06 + i * 0.11), y + h * 0.44)], fill=col)
    # shop windows + door
    draw.rectangle([x + w * 0.12, y + h * 0.52, x + w * 0.40, y + h * 0.82],
                   fill=(90, 130, 170))
    draw.rectangle([x + w * 0.60, y + h * 0.52, x + w * 0.88, y + h * 0.82],
                   fill=(90, 130, 170))
    draw.rectangle([x + w * 0.45, y + h * 0.58, x + w * 0.55, y + h * 0.88],
                   fill=(60, 50, 44))
    # police tape
    draw.rectangle([x, y + h * 0.86, x + w, y + h * 0.96], fill=(255, 215, 0))
    for i in range(6):
        draw.polygon([(x + w * i * 0.17, y + h * 0.96),
                      (x + w * (i * 0.17 + 0.06), y + h * 0.96),
                      (x + w * (i * 0.17 + 0.10), y + h * 0.86),
                      (x + w * (i * 0.17 + 0.04), y + h * 0.86)],
                     fill=(20, 20, 20))
    # two officers
    person(draw, x + w * 0.18, y + h * 0.99, h * 0.05, (24, 32, 64))
    person(draw, x + w * 0.82, y + h * 0.99, h * 0.05, (24, 32, 64))


def scene_aden(draw, x, y, w, h):
    sky_bands(draw, x, y, w, h * 0.55, (250, 200, 120), (245, 180, 90))
    draw.ellipse([x + w * 0.78, y + h * 0.06, x + w * 0.88, y + h * 0.16],
                 fill=(255, 240, 180))
    # mountains
    draw.polygon([(x, y + h * 0.55), (x + w * 0.25, y + h * 0.28),
                  (x + w * 0.50, y + h * 0.55)], fill=(150, 110, 70))
    draw.polygon([(x + w * 0.40, y + h * 0.55), (x + w * 0.65, y + h * 0.32),
                  (x + w * 0.90, y + h * 0.55)], fill=(130, 95, 60))
    # desert ground + road
    draw.rectangle([x, y + h * 0.55, x + w, y + h], fill=(214, 178, 120))
    draw.polygon([(x + w * 0.42, y + h), (x + w * 0.48, y + h * 0.55),
                  (x + w * 0.58, y + h * 0.55), (x + w * 0.66, y + h)],
                 fill=(90, 80, 70))
    # convoy trucks
    for i, (tx, ts) in enumerate(((0.10, 1.0), (0.30, 0.85), (0.68, 0.9))):
        bx, by = x + w * tx, y + h * (0.78 - i * 0.04)
        s = h * 0.10 * ts
        draw.rectangle([bx, by - s, bx + s * 2.2, by], fill=(80, 70, 55))
        draw.rectangle([bx + s * 2.2, by - s * 0.7, bx + s * 2.9, by],
                       fill=(110, 95, 70))
        draw.ellipse([bx + s * 0.3, by - 1, bx + s * 0.7, by + 3], fill=(20, 20, 20))
        draw.ellipse([bx + s * 1.6, by - 1, bx + s * 2.0, by + 3], fill=(20, 20, 20))
        draw.ellipse([bx + s * 2.4, by - 1, bx + s * 2.7, by + 3], fill=(20, 20, 20))


def scene_icj(draw, x, y, w, h):
    sky_bands(draw, x, y, w, h * 0.6, (150, 170, 200), (210, 220, 230))
    # courthouse
    draw.rectangle([x + w * 0.08, y + h * 0.34, x + w * 0.92, y + h * 0.90],
                   fill=(235, 228, 210), outline=(120, 105, 85))
    draw.polygon([(x + w * 0.04, y + h * 0.34), (x + w * 0.50, y + h * 0.12),
                  (x + w * 0.96, y + h * 0.34)], fill=(210, 195, 165))
    for i in range(5):
        cx = x + w * (0.16 + i * 0.17)
        draw.rectangle([cx - w * 0.03, y + h * 0.38, cx + w * 0.03,
                        y + h * 0.88], fill=(250, 244, 228))
    draw.rectangle([x + w * 0.42, y + h * 0.66, x + w * 0.58, y + h * 0.90],
                   fill=(90, 70, 50))
    # scales of justice above the door pediment
    sx, sy = x + w * 0.50, y + h * 0.10
    draw.line([(sx, sy - h * 0.06), (sx, sy + h * 0.06)], fill=(140, 110, 40),
              width=2)
    draw.line([(sx - w * 0.08, sy - h * 0.02), (sx + w * 0.08, sy - h * 0.02)],
              fill=(140, 110, 40), width=2)
    draw.ellipse([sx - w * 0.10, sy + h * 0.02, sx - w * 0.05, sy + h * 0.06],
                 fill=(140, 110, 40))
    draw.ellipse([sx + w * 0.05, sy + h * 0.02, sx + w * 0.10, sy + h * 0.06],
                 fill=(140, 110, 40))
    # two flags
    for fx, col in ((0.10, (31, 78, 121)), (0.86, (198, 40, 40))):
        draw.line([(x + w * fx, y + h * 0.10), (x + w * fx, y + h * 0.34)],
                  fill=(60, 60, 60), width=2)
        draw.polygon([(x + w * fx, y + h * 0.10),
                      (x + w * (fx + 0.08), y + h * 0.14),
                      (x + w * fx, y + h * 0.18)], fill=col)


def scene_gaza(draw, x, y, w, h):
    sky_bands(draw, x, y, w, h, (22, 28, 52), (60, 70, 110))
    draw.ellipse([x + w * 0.80, y + h * 0.08, x + w * 0.88, y + h * 0.16],
                 fill=(240, 230, 200))
    # building block
    draw.rectangle([x + w * 0.10, y + h * 0.40, x + w * 0.62, y + h * 0.95],
                   fill=(48, 48, 58))
    for r in range(4):
        for c in range(4):
            col = (255, 214, 120) if (r * 4 + c) % 3 else (40, 40, 48)
            draw.rectangle([x + w * (0.15 + c * 0.12), y + h * (0.46 + r * 0.12),
                            x + w * (0.19 + c * 0.12), y + h * (0.52 + r * 0.12)],
                           fill=col)
    # damaged corner + smoke
    draw.polygon([(x + w * 0.62, y + h * 0.40), (x + w * 0.52, y + h * 0.55),
                  (x + w * 0.62, y + h * 0.62)], fill=(30, 30, 38))
    smoke(draw, x + w * 0.58, y + h * 0.42, h * 0.06)
    flames(draw, x + w * 0.56, y + h * 0.48, h * 0.06)
    # second building
    draw.rectangle([x + w * 0.68, y + h * 0.62, x + w * 0.94, y + h * 0.95],
                   fill=(38, 38, 48))
    for r in range(2):
        for c in range(2):
            draw.rectangle([x + w * (0.72 + c * 0.10), y + h * (0.68 + r * 0.12),
                            x + w * (0.76 + c * 0.10), y + h * (0.74 + r * 0.12)],
                           fill=(255, 214, 120))


def scene_heli(draw, x, y, w, h):
    sky_bands(draw, x, y, w, h * 0.7, (130, 165, 200), (205, 215, 228))
    draw.ellipse([x + w * 0.76, y + h * 0.08, x + w * 0.86, y + h * 0.18],
                 fill=(255, 245, 200))
    # mountains
    draw.polygon([(x, y + h * 0.95), (x + w * 0.30, y + h * 0.55),
                  (x + w * 0.60, y + h * 0.95)], fill=(120, 130, 120))
    draw.polygon([(x + w * 0.45, y + h * 0.95), (x + w * 0.75, y + h * 0.48),
                  (x + w, y + h * 0.95)], fill=(100, 112, 100))
    draw.polygon([(x + w * 0.68, y + h * 0.48), (x + w * 0.75, y + h * 0.58),
                  (x + w * 0.82, y + h * 0.48)], fill=(245, 245, 245))
    # helicopter silhouette
    hx, hy = x + w * 0.30, y + h * 0.30
    draw.ellipse([hx, hy, hx + w * 0.34, hy + h * 0.22], fill=(40, 44, 50))
    draw.polygon([(hx + w * 0.30, hy + h * 0.08),
                  (hx + w * 0.48, hy + h * 0.12),
                  (hx + w * 0.48, hy + h * 0.18),
                  (hx + w * 0.30, hy + h * 0.18)], fill=(40, 44, 50))
    draw.line([(hx - w * 0.16, hy + h * 0.02), (hx + w * 0.52, hy + h * 0.02)],
              fill=(40, 44, 50), width=3)
    draw.line([(hx + w * 0.16, hy - h * 0.08), (hx + w * 0.18, hy + h * 0.02)],
              fill=(40, 44, 50), width=2)
    draw.rectangle([hx + w * 0.06, hy + h * 0.06, hx + w * 0.14, hy + h * 0.14],
                   fill=(150, 190, 220))


def scene_oil(draw, x, y, w, h):
    sky_bands(draw, x, y, w, h * 0.6, (245, 190, 110), (250, 220, 150))
    draw.ellipse([x + w * 0.80, y + h * 0.06, x + w * 0.88, y + h * 0.14],
                 fill=(255, 240, 170))
    draw.rectangle([x, y + h * 0.60, x + w, y + h], fill=(205, 165, 105))
    # derrick
    dx, dy = x + w * 0.14, y + h * 0.62
    draw.polygon([(dx, dy), (dx + w * 0.10, y + h * 0.18),
                  (dx + w * 0.20, y + h * 0.18), (dx + w * 0.30, dy)],
                 outline=(60, 50, 40), width=2)
    draw.line([(dx + w * 0.05, dy - h * 0.14), (dx + w * 0.25, dy - h * 0.28)],
              fill=(60, 50, 40), width=2)
    # pumpjack
    px, py = x + w * 0.52, y + h * 0.66
    draw.polygon([(px, py), (px + w * 0.06, py - h * 0.22),
                  (px + w * 0.30, py - h * 0.28), (px + w * 0.34, py - h * 0.20),
                  (px + w * 0.10, py - h * 0.10)], fill=(40, 40, 44))
    draw.rectangle([px + w * 0.30, py - h * 0.28, px + w * 0.32, py - h * 0.06],
                   fill=(40, 40, 44))
    # barrels
    for i, bx in enumerate((0.72, 0.82)):
        draw.rectangle([x + w * bx, y + h * (0.78 - i * 0.04),
                        x + w * (bx + 0.09), y + h * 0.92], fill=(120, 40, 30))
        draw.line([(x + w * bx, y + h * (0.83 - i * 0.04)),
                   (x + w * (bx + 0.09), y + h * (0.83 - i * 0.04))],
                  fill=(90, 30, 22), width=1)


def scene_senegal(draw, x, y, w, h):
    draw.rectangle([x, y, x + w, y + h], fill=(34, 130, 70))
    for i in range(4):
        draw.line([(x, y + h * (0.25 + i * 0.25)), (x + w, y + h * (0.25 + i * 0.25))],
                  fill=(46, 150, 84), width=2)
    # trophy
    tx, ty = x + w * 0.42, y + h * 0.30
    draw.polygon([(tx, ty), (tx + w * 0.16, ty), (tx + w * 0.13, ty + h * 0.28),
                  (tx + w * 0.03, ty + h * 0.28)], fill=(255, 205, 40))
    draw.arc([tx - w * 0.05, ty + h * 0.02, tx + w * 0.02, ty + h * 0.16],
             90, 270, fill=(255, 205, 40), width=3)
    draw.arc([tx + w * 0.14, ty + h * 0.02, tx + w * 0.21, ty + h * 0.16],
             270, 90, fill=(255, 205, 40), width=3)
    draw.rectangle([tx + w * 0.05, ty + h * 0.28, tx + w * 0.11, ty + h * 0.42],
                   fill=(255, 205, 40))
    draw.rectangle([tx + w * 0.01, ty + h * 0.42, tx + w * 0.15, ty + h * 0.48],
                   fill=(255, 205, 40))
    # ball
    bx, by, br = x + w * 0.74, y + h * 0.62, h * 0.16
    draw.ellipse([bx - br, by - br, bx + br, by + br], fill=(250, 250, 250),
                 outline=(30, 30, 30))
    draw.polygon([(bx, by - br * 0.5), (bx + br * 0.5, by - br * 0.1),
                  (bx + br * 0.3, by + br * 0.5), (bx - br * 0.3, by + br * 0.5),
                  (bx - br * 0.5, by - br * 0.1)], fill=(30, 30, 30))
    # flag stripes
    for i, col in enumerate(((0, 130, 60), (255, 205, 0), (200, 40, 40))):
        draw.rectangle([x + w * (0.06 + i * 0.07), y + h * 0.78,
                        x + w * (0.11 + i * 0.07), y + h * 0.92], fill=col)


def scene_davis(draw, x, y, w, h):
    sky_bands(draw, x, y, w, h * 0.5, (120, 160, 205), (190, 205, 225))
    # stands
    draw.rectangle([x, y + h * 0.30, x + w, y + h * 0.55], fill=(60, 70, 100))
    for i in range(12):
        draw.ellipse([x + w * (0.05 + i * 0.08), y + h * 0.36,
                      x + w * (0.08 + i * 0.08), y + h * 0.40],
                     fill=(240, 220, 180))
    # court
    draw.rectangle([x, y + h * 0.55, x + w, y + h], fill=(40, 110, 180))
    draw.rectangle([x + w * 0.06, y + h * 0.62, x + w * 0.94, y + h * 0.96],
                   fill=(52, 140, 80), outline=(255, 255, 255))
    draw.line([(x + w * 0.50, y + h * 0.62), (x + w * 0.50, y + h * 0.96)],
              fill=(255, 255, 255), width=1)
    # net
    draw.rectangle([x + w * 0.06, y + h * 0.72, x + w * 0.94, y + h * 0.76],
                   fill=(20, 20, 20))
    draw.rectangle([x + w * 0.06, y + h * 0.72, x + w * 0.94, y + h * 0.74],
                   fill=(255, 255, 255))
    # ball + player
    draw.ellipse([x + w * 0.68, y + h * 0.60, x + w * 0.74, y + h * 0.66],
                 fill=(200, 230, 60), outline=(120, 150, 40))
    person(draw, x + w * 0.22, y + h * 0.94, h * 0.09, (220, 220, 220))

SCENES = {
    1: scene_hormuz, 2: scene_huawei, 3: scene_riyadh, 4: scene_ships,
    5: scene_nvidia, 6: scene_cartagena, 7: scene_aden, 8: scene_icj,
    9: scene_gaza, 10: scene_heli, 11: scene_oil, 12: scene_senegal,
    13: scene_davis,
}

# ------------------------------------------------------------- world map
# Stylised continents, equirectangular lon/lat polygons.
NA = [(-168, 66), (-140, 70), (-120, 71), (-105, 68), (-90, 66), (-80, 62),
      (-70, 58), (-60, 52), (-55, 47), (-65, 44), (-74, 40), (-76, 35),
      (-81, 31), (-81, 26), (-86, 30), (-91, 21), (-97, 16), (-92, 14),
      (-83, 9), (-79, 9), (-90, 14), (-97, 16), (-105, 20), (-110, 23),
      (-114, 29), (-121, 34), (-124, 42), (-124, 48), (-130, 55),
      (-145, 60), (-158, 58), (-165, 60)]
SA = [(-79, 9), (-77, 4), (-80, -3), (-81, -6), (-77, -12), (-70, -18),
      (-70, -23), (-62, -26), (-53, -32), (-57, -38), (-63, -41),
      (-66, -47), (-69, -52), (-70, -54), (-66, -55), (-68, -50),
      (-72, -40), (-73, -33), (-71, -22), (-76, -14), (-80, -5)]
GL = [(-58, 64), (-50, 60), (-42, 60), (-38, 65), (-30, 68), (-22, 70),
      (-20, 74), (-30, 77), (-45, 77), (-56, 74), (-60, 70)]
EU = [(-10, 36), (-9, 43), (-2, 44), (-1, 46), (-2, 48), (0, 50), (3, 53),
      (7, 56), (10, 58), (14, 56), (19, 55), (23, 57), (26, 59), (30, 62),
      (28, 66), (24, 70), (18, 69), (12, 65), (10, 62), (6, 58), (5, 60),
      (5, 57), (0, 55), (-4, 52), (-6, 50), (-9, 43)]
AF = [(-17, 15), (-16, 21), (-11, 28), (-6, 35), (0, 36), (10, 37),
      (12, 34), (19, 32), (25, 32), (30, 31), (34, 28), (37, 20),
      (40, 15), (44, 11), (51, 11), (48, 5), (41, -2), (40, -9),
      (36, -18), (32, -26), (28, -33), (20, -35), (16, -29), (13, -18),
      (12, -10), (12, -4), (9, 4), (4, 6), (-3, 5), (-8, 5), (-13, 8),
      (-17, 12)]
AS = [(30, 62), (38, 68), (50, 69), (62, 70), (74, 72), (86, 74),
      (98, 76), (110, 75), (122, 73), (134, 72), (146, 71), (158, 69),
      (170, 66), (178, 65), (170, 60), (162, 56), (156, 51), (150, 59),
      (142, 54), (140, 44), (134, 42), (128, 38), (123, 39), (120, 32),
      (116, 24), (110, 20), (106, 10), (103, 6), (100, 8), (97, 12),
      (93, 18), (90, 22), (86, 20), (81, 15), (78, 8), (75, 12),
      (71, 20), (66, 25), (61, 25), (57, 26), (52, 28), (48, 30),
      (44, 29), (40, 24), (38, 18), (35, 14), (32, 14), (30, 18),
      (28, 24), (26, 30), (24, 34), (22, 36), (27, 37), (30, 41),
      (28, 45), (33, 46), (35, 50), (32, 55)]
AU = [(113, -22), (114, -30), (115, -35), (120, -34), (125, -32),
      (129, -32), (132, -32), (135, -35), (138, -35), (141, -38),
      (146, -39), (150, -37), (153, -32), (153, -27), (150, -23),
      (146, -19), (142, -15), (142, -11), (137, -12), (135, -15),
      (132, -12), (130, -13), (126, -14), (122, -17), (118, -20),
      (114, -22)]
UK = [(-5, 50), (-3, 53), (-5, 56), (-3, 58), (-1, 57), (0, 53), (1, 51)]
JP = [(130, 31), (133, 34), (137, 35), (140, 38), (141, 41), (143, 43),
      (145, 44), (142, 42), (140, 39), (139, 35), (136, 33), (132, 33)]
ID = [(95, 5), (98, 3), (100, 0), (104, -3), (107, -7), (110, -7),
      (114, -8), (119, -9), (122, -10), (125, -9), (128, -6), (131, -3),
      (135, -2), (138, -4), (141, -8), (140, -8), (136, -6), (132, -4),
      (128, -3), (124, 0), (120, 0), (117, 2), (114, 3), (110, 1),
      (106, -2), (102, 0)]

CONTINENTS = [NA, SA, GL, EU, AF, AS, AU, UK, JP, ID]

# pin positions for stories 1-13: (lon, lat)
PINS = {
    1: (56.5, 26.5), 2: (-74.0, 40.7), 3: (46.7, 24.6), 4: (23.0, 59.8),
    5: (-122.0, 37.4), 6: (-75.5, 10.4), 7: (45.0, 12.8), 8: (4.3, 52.0),
    9: (34.5, 31.5), 10: (30.5, 39.8), 11: (44.4, 35.5), 12: (-17.4, 14.7),
    13: (11.3, 44.5),
}


def draw_map(draw, x, y, w, h):
    draw.rectangle([x, y, x + w, y + h], fill=SEA)
    lon0, lon1, lat0, lat1 = -170, 190, -58, 84

    def px(lon, lat):
        return (x + (lon - lon0) / (lon1 - lon0) * w,
                y + (lat1 - lat) / (lat1 - lat0) * h)

    for poly in CONTINENTS:
        pts = [px(lon, lat) for lon, lat in poly]
        draw.polygon(pts, fill=LAND, outline=LAND_EDGE)
    # graticule dots
    for glon in range(-150, 181, 30):
        for glat in range(-45, 76, 30):
            gx, gy = px(glon, glat)
            draw.ellipse([gx - 1, gy - 1, gx + 1, gy + 1], fill=(170, 190, 205))
    # pins
    for n, (lon, lat) in PINS.items():
        cx, cy = px(lon, lat)
        r = 8
        draw.ellipse([cx - r, cy - r, cx + r, cy + r], fill=RED,
                     outline=(255, 255, 255), width=1)
        f = F_sans_b(9)
        t = str(n)
        draw.text((cx - draw.textlength(t, font=f) / 2, cy - 5), t,
                  font=f, fill=(255, 255, 255))

# ------------------------------------------------------------- layout
M = 14
X0, X1 = M, W - M
CW = X1 - X0

FEATURE_LABELS = {1: "4 TANKERS HIT", 2: "10 OF 12 COUNTS", 3: "11 WOUNDED"}
TILE_LABELS = {4: "SPARTA II", 5: "-5.86%", 6: "25 HOSTAGES", 7: "60 KM OUT",
               8: "9-6 RULING", 9: "SECURITY CHIEF", 10: "5 KILLED",
               11: "OILFIELDS", 12: "TITLE BACK", 13: "CZECHIA 2-0"}

DATE_CHECK = (
    "Every numbered story happened, or was first reported, on Tuesday "
    "24 November 2026. Left out as other days' news: COP31's collapse "
    "(Sun 22) · Huang's return as Nvidia chief (Mon 23 — only Tuesday's "
    "-5.86% fall is shown) · the Benghazi warship strike (Sun 22 — only "
    "Tuesday's Sparta II strike and Tripoli's demand are shown) · the "
    "Dymer toll (Mon 23) · El Chapo Isidro's capture (Sat 21 — only "
    "Tuesday's drone detail is shown) · the ATP Finals (Sun 22). "
    "Tonight's count: 4 tankers hit mines, not 2 — early wires said two; "
    "the IRGC later added two more. Not yet: Taiwan's local elections "
    "(Sat 28) · the Davis Cup final (Sun 29) · Indonesia's VP vote (11 Dec)."
)


def draw_feature(draw, fx, fy, fw, story):
    n, region, place, cat, status, source, head, deck = story
    # illustration banner
    SCENES[n](draw, fx, fy, fw, 104)
    draw.rectangle([fx, fy, fx + fw, fy + 18], fill=(20, 20, 24))
    lf = F_sans_b(11)
    draw.text((fx + 8, fy + 3), FEATURE_LABELS[n], font=lf,
              fill=(255, 255, 255))
    # badge + place + chip row
    by = fy + 110
    num_badge(draw, fx + 11, by + 7, n, r=10)
    pf = F_sans_b(10)
    draw.text((fx + 26, by + 2), place, font=pf, fill=REGION_COLORS[region])
    cf = F_sans(10)
    draw.text((fx + 26 + draw.textlength(place, font=pf) + 5, by + 2),
              "· " + cat, font=cf, fill=GREY)
    draw_chip(draw, fx + fw - 74, by + 1, status)
    # headline + deck
    hf = F_serif(18)
    lines = tw(draw, head, hf, fw - 4)[:2]
    yy = by + 22
    for ln in lines:
        draw.text((fx + 2, yy), ln, font=hf, fill=INK)
        yy += 20
    df = F_sans(11)
    dlines = tw(draw, deck, df, fw - 4)[:3]
    yy = by + 64
    for ln in dlines:
        draw.text((fx + 2, yy), ln, font=df, fill=(40, 40, 40))
        yy += 13


def draw_tile(draw, tx, ty, twd, story):
    n, region, place, cat, status, source, head, deck = story
    SCENES[n](draw, tx, ty, twd, 46)
    draw.rectangle([tx, ty, tx + twd, ty + 13], fill=(20, 20, 24))
    lf = F_sans_b(8)
    draw.text((tx + 5, ty + 2), TILE_LABELS[n], font=lf,
              fill=(255, 255, 255))
    by = ty + 50
    num_badge(draw, tx + 8, by + 6, n, r=8)
    pf = F_sans_b(8)
    pw = draw.textlength(place, font=pf)
    draw.text((tx + 19, by + 1), place, font=pf, fill=REGION_COLORS[region])
    draw_chip(draw, tx + twd - 62, by, status, F_sans_b(8))
    hf = F_serif(13)
    lines = tw(draw, head, hf, twd - 2)[:2]
    yy = by + 16
    for ln in lines:
        draw.text((tx + 1, yy), ln, font=hf, fill=INK)
        yy += 15
    df = F_sans(9)
    dlines = tw(draw, deck, df, twd - 2)[:3]
    yy = by + 48
    for ln in dlines:
        draw.text((tx + 1, yy), ln, font=df, fill=(40, 40, 40))
        yy += 11


def main():
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)

    # ---- top bar
    d.rectangle([0, 0, W, 22], fill=NAVY)
    bf = F_sans_b(11)
    d.text((X0, 5), "THE WORLD IN ONE DAY", font=bf, fill=(255, 255, 255))
    rt = "36 STORIES · 7 REGIONS · ALL FROM TUESDAY 24 NOVEMBER 2026"
    d.text((X1 - d.textlength(rt, font=bf), 5), rt, font=bf,
           fill=(255, 255, 255))

    # ---- masthead
    mf = F_serif(56)
    mt = "Tuesday 24 November 2026"
    d.text(((W - d.textlength(mt, font=mf)) / 2, 26), mt, font=mf, fill=INK)

    # ---- sub-headline
    sf = F_serif_reg(16)
    st = ("Four tankers hit mines in Hormuz  ·  Huawei guilty on 10 counts  ·  "
          "Riyadh tower struck again")
    d.text(((W - d.textlength(st, font=sf)) / 2, 90), st, font=sf, fill=RED)
    rule(d, X0, X1, 110, 2)

    # ---- stat strip
    sy = 114
    cell = CW / 6
    nf = F_serif(24)
    lf = F_sans(9)
    for i, (num, lab) in enumerate(STATS):
        cx = X0 + i * cell
        if i:
            d.line([(cx, sy + 2), (cx, sy + 40)], fill=LINE, width=1)
        nw = d.textlength(num, font=nf)
        d.text((cx + (cell - nw) / 2, sy), num, font=nf, fill=INK)
        for j, ln in enumerate(lab.split("\n")):
            lw = d.textlength(ln, font=lf)
            d.text((cx + (cell - lw) / 2, sy + 27 + j * 10), ln, font=lf,
                   fill=GREY)
    rule(d, X0, X1, 162, 1, LINE)

    # ---- region bar
    ry = 166
    seg = CW / 7
    rf = F_sans_b(10)
    for i, (name, cnt) in enumerate(REGION_COUNTS):
        x = X0 + i * seg
        d.rectangle([x, ry, x + seg - 1, ry + 20], fill=REGION_COLORS[name])
        t = f"{name} {cnt}"
        d.text((x + (seg - d.textlength(t, font=rf)) / 2, ry + 4), t,
               font=rf, fill=(255, 255, 255))

    # ---- UTC timeline
    ty = 192
    d.rectangle([X0, ty, X0 + 208, ty + 16], fill=RED)
    tf = F_sans_b(9)
    d.text((X0 + 6, ty + 3), "TUESDAY 24 NOV, AS IT HAPPENED", font=tf,
           fill=(255, 255, 255))
    uf = F_sans(10)
    items = "  ·  ".join(f"{t} {s}" for t, s in TIMELINE)
    d.text((X0 + 216, ty + 2), items, font=uf, fill=INK)
    rule(d, X0, X1, 212, 2)

    # ---- features
    fw = 326
    for i, story in enumerate(FEATURES):
        draw_feature(d, X0 + i * (fw + 9), 216, fw, story)

    # ---- tiles (2 rows x 5)
    twd = 194
    gap = (CW - 5 * twd) / 4
    for row in range(2):
        for col in range(5):
            story = TILES[row * 5 + col]
            draw_tile(d, X0 + col * (twd + gap), 420 + row * 128, twd, story)

    # ---- map + ALSO
    my = 678
    d.text((X0, my), "WHERE IT HAPPENED", font=F_sans_b(11), fill=INK)
    d.text((X0 + 8, my + 1), "", font=F_sans(9), fill=GREY)
    map_x, map_y, map_w, map_h = X0, my + 18, 300, 148
    draw_map(d, map_x, map_y, map_w, map_h)
    # map legend
    ly = my + 172
    lf = F_sans(8)
    lx = X0
    for i, (name, _) in enumerate(REGION_COUNTS):
        if i == 4:
            lx = X0
            ly += 11
        d.ellipse([lx, ly + 1, lx + 7, ly + 8], fill=REGION_COLORS[name])
        d.text((lx + 10, ly), name.title(), font=lf, fill=INK)
        lx += 10 + d.textlength(name.title(), font=lf) + 10
    d.text((X0, ly + 13), "pins = stories 1-13", font=F_sans(8), fill=GREY)

    # ALSO list
    ax = X0 + 308
    d.text((ax, my), "ALSO ON TUESDAY 24 NOVEMBER 2026",
           font=F_sans_b(12), fill=RED)
    rule(d, ax, X1, my + 16, 1, RED)
    af = F_sans(10)
    abf = F_sans_b(10)
    col_w = (X1 - ax - 10) / 2
    for idx, item in enumerate(ALSO):
        n, region, place, head, status = item
        col = idx // 12
        row = idx % 12
        ix = ax + col * (col_w + 10)
        iy = my + 22 + row * 14
        num = f"{n} "
        d.text((ix, iy), num, font=abf, fill=BLUE)
        nx = ix + d.textlength(num, font=abf)
        d.text((nx, iy), f"{place}: ", font=abf, fill=INK)
        hx = nx + d.textlength(f"{place}: ", font=abf)
        d.text((hx, iy), head, font=af, fill=(40, 40, 40))
        if status == "CLAIM":
            cw = d.textlength("CLAIM", font=F_sans_b(8))
            d.text((ix + col_w - cw, iy), "CLAIM", font=F_sans_b(8),
                   fill=RED)

    # ---- DATE CHECK
    dy = 880
    d.rectangle([X0, dy, X1, dy + 78], outline=RED, width=2)
    d.rectangle([X0, dy, X0 + 108, dy + 18], fill=RED)
    d.text((X0 + 8, dy + 3), "DATE CHECK", font=F_sans_b(11),
           fill=(255, 255, 255))
    df = F_sans(10)
    lines = tw(d, DATE_CHECK, df, CW - 24)
    yy = dy + 22
    for ln in lines:
        # bold the "Tonight's count" sentence start
        if ln.startswith("Tonight's count:"):
            bold_part = "Tonight's count: 4 tankers hit mines, not 2"
            d.text((X0 + 12, yy), bold_part, font=F_sans_b(10), fill=INK)
            rest = ln[len(bold_part):]
            d.text((X0 + 12 + d.textlength(bold_part, font=F_sans_b(10)), yy),
                   rest, font=df, fill=INK)
        else:
            d.text((X0 + 12, yy), ln, font=df, fill=INK)
        yy += 13

    # ---- footer legend + sources
    fy = 966
    ff = F_sans(9)
    leg = ("CONFIRMED = 2+ outlets  ·  OFFICIAL = an authority's own word  ·  "
           "REPORTED = carried by wires or officials  ·  CLAIM = one side's "
           "account, labelled as such")
    d.text((X0, fy), leg, font=ff, fill=GREY)
    src = ("Sources: Reuters, AP, AFP, Al Jazeera, The Guardian, Xinhua, DW · "
           "Scenes are drawn illustrations of reported events, not photographs.")
    d.text((X0, fy + 12), src, font=ff, fill=GREY)

    # ---- bottom bar
    d.rectangle([0, 992, W, H], fill=NAVY)
    d.text((X0, 998), "THE WORLD IN ONE DAY", font=F_sans_b(10),
           fill=(255, 255, 255))
    bt = "TUESDAY 24 NOVEMBER 2026 · ONE PAGE"
    d.text((X1 - d.textlength(bt, font=F_sans_b(10)), 998), bt,
           font=F_sans_b(10), fill=(255, 255, 255))

    img.save(OUT, "PNG", optimize=True)
    print("saved", OUT, os.path.getsize(OUT), "bytes")


if __name__ == "__main__":
    main()

"""News-image entry: draws a one-page newspaper for Wednesday 25 November 2026.

Pure Python standard library. No network, no randomness, no timestamps.
All news data lives in this file (DATA section, written from research done
on 25 November 2026); the renderer below turns it into /output/entry.png.
"""
import os
import struct
import zlib

W = 1024
H = 1024

# ---------------------------------------------------------------- font 5x7
# Each glyph is 7 rows of 5 bits. Written from scratch for this entry.
FONT = {
    "A": ("01110", "10001", "10001", "11111", "10001", "10001", "10001"),
    "B": ("11110", "10001", "10001", "11110", "10001", "10001", "11110"),
    "C": ("01110", "10001", "10000", "10000", "10000", "10001", "01110"),
    "D": ("11110", "10001", "10001", "10001", "10001", "10001", "11110"),
    "E": ("11111", "10000", "10000", "11110", "10000", "10000", "11111"),
    "F": ("11111", "10000", "10000", "11110", "10000", "10000", "10000"),
    "G": ("01110", "10001", "10000", "10111", "10001", "10001", "01111"),
    "H": ("10001", "10001", "10001", "11111", "10001", "10001", "10001"),
    "I": ("01110", "00100", "00100", "00100", "00100", "00100", "01110"),
    "J": ("00111", "00010", "00010", "00010", "00010", "10010", "01100"),
    "K": ("10001", "10010", "10100", "11000", "10100", "10010", "10001"),
    "L": ("10000", "10000", "10000", "10000", "10000", "10000", "11111"),
    "M": ("10001", "11011", "10101", "10101", "10001", "10001", "10001"),
    "N": ("10001", "11001", "10101", "10011", "10001", "10001", "10001"),
    "O": ("01110", "10001", "10001", "10001", "10001", "10001", "01110"),
    "P": ("11110", "10001", "10001", "11110", "10000", "10000", "10000"),
    "Q": ("01110", "10001", "10001", "10001", "10101", "10010", "01101"),
    "R": ("11110", "10001", "10001", "11110", "10100", "10010", "10001"),
    "S": ("01111", "10000", "10000", "01110", "00001", "00001", "11110"),
    "T": ("11111", "00100", "00100", "00100", "00100", "00100", "00100"),
    "U": ("10001", "10001", "10001", "10001", "10001", "10001", "01110"),
    "V": ("10001", "10001", "10001", "10001", "10001", "01010", "00100"),
    "W": ("10001", "10001", "10001", "10101", "10101", "11011", "10001"),
    "X": ("10001", "10001", "01010", "00100", "01010", "10001", "10001"),
    "Y": ("10001", "10001", "01010", "00100", "00100", "00100", "00100"),
    "Z": ("11111", "00001", "00010", "00100", "01000", "10000", "11111"),
    "a": ("00000", "00000", "01110", "00001", "01111", "10001", "01111"),
    "b": ("10000", "10000", "11110", "10001", "10001", "10001", "11110"),
    "c": ("00000", "00000", "01110", "10000", "10000", "10001", "01110"),
    "d": ("00001", "00001", "01111", "10001", "10001", "10001", "01111"),
    "e": ("00000", "00000", "01110", "10001", "11111", "10000", "01110"),
    "f": ("00110", "01001", "01000", "11110", "01000", "01000", "01000"),
    "g": ("00000", "01111", "10001", "10001", "01111", "00001", "01110"),
    "h": ("10000", "10000", "11110", "10001", "10001", "10001", "10001"),
    "i": ("00100", "00000", "01100", "00100", "00100", "00100", "01110"),
    "j": ("00010", "00000", "00110", "00010", "00010", "10010", "01100"),
    "k": ("10000", "10000", "10010", "10100", "11000", "10100", "10010"),
    "l": ("01100", "00100", "00100", "00100", "00100", "00100", "01110"),
    "m": ("00000", "00000", "11010", "10101", "10101", "10101", "10101"),
    "n": ("00000", "00000", "11110", "10001", "10001", "10001", "10001"),
    "o": ("00000", "00000", "01110", "10001", "10001", "10001", "01110"),
    "p": ("00000", "11110", "10001", "10001", "11110", "10000", "10000"),
    "q": ("00000", "01111", "10001", "10001", "01111", "00001", "00001"),
    "r": ("00000", "00000", "10110", "11001", "10000", "10000", "10000"),
    "s": ("00000", "00000", "01111", "10000", "01110", "00001", "11110"),
    "t": ("01000", "01000", "11100", "01000", "01000", "01000", "00110"),
    "u": ("00000", "00000", "10001", "10001", "10001", "10011", "01101"),
    "v": ("00000", "00000", "10001", "10001", "10001", "01010", "00100"),
    "w": ("00000", "00000", "10001", "10101", "10101", "10101", "01010"),
    "x": ("00000", "00000", "10001", "01010", "00100", "01010", "10001"),
    "y": ("00000", "00000", "10001", "10001", "01111", "00001", "01110"),
    "z": ("00000", "00000", "11111", "00010", "00100", "01000", "11111"),
    "0": ("01110", "10001", "10011", "10101", "11001", "10001", "01110"),
    "1": ("00100", "01100", "00100", "00100", "00100", "00100", "01110"),
    "2": ("01110", "10001", "00001", "00110", "01000", "10000", "11111"),
    "3": ("11111", "00010", "00100", "00010", "00001", "10001", "01110"),
    "4": ("00010", "00110", "01010", "10010", "11111", "00010", "00010"),
    "5": ("11111", "10000", "11110", "00001", "00001", "10001", "01110"),
    "6": ("00110", "01000", "10000", "11110", "10001", "10001", "01110"),
    "7": ("11111", "00001", "00010", "00100", "01000", "01000", "01000"),
    "8": ("01110", "10001", "10001", "01110", "10001", "10001", "01110"),
    "9": ("01110", "10001", "10001", "01111", "00001", "00010", "01100"),
    " ": ("00000", "00000", "00000", "00000", "00000", "00000", "00000"),
    ".": ("00000", "00000", "00000", "00000", "00000", "01100", "01100"),
    ",": ("00000", "00000", "00000", "00000", "01100", "00100", "01000"),
    ":": ("00000", "01100", "01100", "00000", "01100", "01100", "00000"),
    ";": ("00000", "01100", "01100", "00000", "01100", "00100", "01000"),
    "!": ("00100", "00100", "00100", "00100", "00100", "00000", "00100"),
    "?": ("01110", "10001", "00001", "00110", "00100", "00000", "00100"),
    "'": ("00100", "00100", "01000", "00000", "00000", "00000", "00000"),
    '"': ("01010", "01010", "00000", "00000", "00000", "00000", "00000"),
    "-": ("00000", "00000", "00000", "01110", "00000", "00000", "00000"),
    "/": ("00001", "00010", "00010", "00100", "01000", "01000", "10000"),
    "%": ("11001", "11010", "00010", "00100", "01000", "01011", "10011"),
    "$": ("00100", "01111", "10100", "01110", "00101", "11110", "00100"),
    "&": ("01100", "10010", "10100", "01000", "10101", "10010", "01101"),
    "+": ("00000", "00100", "00100", "11111", "00100", "00100", "00000"),
    "=": ("00000", "00000", "11111", "00000", "11111", "00000", "00000"),
    "*": ("00000", "10101", "01110", "11111", "01110", "10101", "00000"),
    "#": ("01010", "01010", "11111", "01010", "11111", "01010", "01010"),
    "@": ("01110", "10001", "10111", "10101", "10110", "10000", "01110"),
    "_": ("00000", "00000", "00000", "00000", "00000", "00000", "11111"),
    "(": ("00010", "00100", "01000", "01000", "01000", "00100", "00010"),
    ")": ("01000", "00100", "00010", "00010", "00010", "00100", "01000"),
    "[": ("01110", "01000", "01000", "01000", "01000", "01000", "01110"),
    "]": ("01110", "00010", "00010", "00010", "00010", "00010", "01110"),
    "<": ("00010", "00100", "01000", "10000", "01000", "00100", "00010"),
    ">": ("01000", "00100", "00010", "00001", "00010", "00100", "01000"),
    "|": ("00100", "00100", "00100", "00100", "00100", "00100", "00100"),
    "\\": ("10000", "01000", "01000", "00100", "00010", "00010", "00001"),
    "{": ("00110", "01000", "01110", "01000", "01110", "01000", "00110"),
    "}": ("01100", "00010", "01110", "00010", "01110", "00010", "01100"),
    "^": ("00100", "01010", "10001", "00000", "00000", "00000", "00000"),
    "~": ("00000", "00000", "01001", "10110", "00000", "00000", "00000"),
    "`": ("01000", "00100", "00000", "00000", "00000", "00000", "00000"),
}

# ---------------------------------------------------------------- canvas
INK = (26, 26, 26)
PAPER = (250, 246, 236)
RED = (178, 34, 34)
NAVY = (24, 48, 88)
GREY = (110, 108, 100)
LIGHT = (232, 226, 212)
MAPLAND = (214, 204, 178)
MAPLINE = (120, 110, 84)
GOLD = (168, 124, 30)
TEAL = (18, 92, 86)


class Canvas:
    def __init__(self, w, h, bg):
        self.w = w
        self.h = h
        self.px = bytearray(bg * (w * h))

    def set(self, x, y, c):
        if 0 <= x < self.w and 0 <= y < self.h:
            i = (y * self.w + x) * 3
            self.px[i], self.px[i + 1], self.px[i + 2] = c

    def rect(self, x, y, w, h, c):
        for yy in range(max(0, y), min(self.h, y + h)):
            base = (yy * self.w + max(0, x)) * 3
            for xx in range(max(0, x), min(self.w, x + w)):
                i = (yy * self.w + xx) * 3
                self.px[i], self.px[i + 1], self.px[i + 2] = c

    def hline(self, x, y, w, c, t=1):
        self.rect(x, y, w, t, c)

    def vline(self, x, y, h, c, t=1):
        self.rect(x, y, t, h, c)

    def line(self, x0, y0, x1, y1, c):
        dx = abs(x1 - x0)
        dy = -abs(y1 - y0)
        sx = 1 if x0 < x1 else -1
        sy = 1 if y0 < y1 else -1
        err = dx + dy
        while True:
            self.set(x0, y0, c)
            if x0 == x1 and y0 == y1:
                break
            e2 = 2 * err
            if e2 >= dy:
                err += dy
                x0 += sx
            if e2 <= dx:
                err += dx
                y0 += sy

    def circle(self, cx, cy, r, c, fill=True):
        for yy in range(cy - r, cy + r + 1):
            for xx in range(cx - r, cx + r + 1):
                d = (xx - cx) ** 2 + (yy - cy) ** 2
                if fill and d <= r * r:
                    self.set(xx, yy, c)
                elif not fill and r * r - 2 * r <= d <= r * r:
                    self.set(xx, yy, c)

    def text(self, x, y, s, scale, c, bold=False):
        cx = x
        for ch in s:
            g = FONT.get(ch)
            if g is None:
                cx += 6 * scale
                continue
            for row in range(7):
                bits = g[row]
                for col in range(5):
                    if bits[col] == "1":
                        for dy in range(scale):
                            for dx in range(scale):
                                self.set(cx + col * scale + dx, y + row * scale + dy, c)
                                if bold:
                                    self.set(cx + col * scale + dx + 1, y + row * scale + dy, c)
            cx += 6 * scale
        return cx

    def text_w(self, s, scale):
        return len(s) * 6 * scale

    def center(self, y, s, scale, c, bold=False):
        self.text((self.w - self.text_w(s, scale)) // 2, y, s, scale, c, bold)

    def wrap(self, s, max_chars):
        words = s.split(" ")
        lines = []
        cur = ""
        for wd in words:
            if cur and len(cur) + 1 + len(wd) > max_chars:
                lines.append(cur)
                cur = wd
            elif cur:
                cur = cur + " " + wd
            else:
                cur = wd
        if cur:
            lines.append(cur)
        return lines


def chunk(tag, data):
    c = struct.pack(">I", len(data)) + tag + data
    c += struct.pack(">I", zlib.crc32(tag + data) & 0xFFFFFFFF)
    return c


def write_png(cv, path):
    raw = bytearray()
    for y in range(cv.h):
        raw.append(0)
        raw += cv.px[y * cv.w * 3:(y + 1) * cv.w * 3]
    ihdr = struct.pack(">IIBBBBB", cv.w, cv.h, 8, 2, 0, 0, 0)
    png = b"\x89PNG\r\n\x1a\n"
    png += chunk(b"IHDR", ihdr)
    png += chunk(b"IDAT", zlib.compress(bytes(raw), 9))
    png += chunk(b"IEND", b"")
    with open(path, "wb") as f:
        f.write(png)
    return len(png)

# ---------------------------------------------------------------- data
# Every story below was verified on 25 Nov 2026 against at least two
# independent outlets. Status: CONFIRMED = court / government / agency
# record; REPORTED = wire reports; OFFICIALS SAY = attributed claims.
# lat/lon are the story locations for the map. utc is the event time
# in UTC where it is known, else "".

FEATURES = [
    (1, "RAMAPHOSA WINS: COURT SCRAPS PHALA PHALA REPORT",
     "The Western Cape High Court sets aside the 2022 Section 89 panel report that said the president had a case to answer over $580,000 found at his farm. Parliament's impeachment inquiry falls away.",
     "CONFIRMED", "Sowetan, Devdiscourse, 25 Nov", "AFRICA", -33.92, 18.42, ""),
    (2, "SHENZHOU-24 LIFTS OFF WITH PAKISTAN'S FIRST ASTRONAUT",
     "China launches Shenzhou-24 at 00:18 UTC from Jiuquan; it docks with Tiangong at 03:56 UTC. Muhammad Zeeshan Ali is the first foreign astronaut aboard the station; Tang Hongbo commands.",
     "CONFIRMED", "Xinhua, China Daily, 25 Nov", "ASIA", 40.96, 100.28, "00:18"),
    (3, "AUSTRALIA AND SOLOMON ISLANDS SIGN HISTORIC TREATY",
     "Albanese and PM Matthew Wale sign in Canberra: Australia becomes the Solomons' primary security partner, no foreign military base is allowed, and Canberra funds free education and police.",
     "CONFIRMED", "PM of Australia, Guardian, 25 Nov", "PACIFIC", -35.28, 149.13, ""),
    (4, "TANKERS HIT BY MINES IN THE STRAIT OF HORMUZ",
     "Iran's Revolutionary Guards say two oil tankers under US air escort struck naval mines in the strait and caught fire, as threats spread to the Red Sea and Yemen's war widens.",
     "REPORTED", "IRGC via state media, MEF, 25 Nov", "MIDDLE EAST", 26.57, 56.25, ""),
    (5, "ALL CARTAGENA HOSTAGES FREED AS TROOPS STORM STORE",
     "Colombian special forces storm an Exito supermarket in Cartagena at about 01:00 local time, ending a siege of almost 20 hours. All hostages are freed; one gunman is killed, four are held.",
     "CONFIRMED", "Reuters / AFP, Insight Intl, 25 Nov", "AMERICAS", 10.40, -75.51, "06:00"),
    (6, "PUTIN VOWS 'INEVITABLE' RETALIATION FOR REFINERY STRIKES",
     "At a Kremlin meeting with officials and oil executives, President Putin says Ukraine keeps hitting Russian refineries despite President Trump's request to stop, and promises retaliation.",
     "OFFICIALS SAY", "Kremlin, Silk Paradox brief, 25 Nov", "EUROPE", 55.75, 37.62, ""),
    (7, "NVIDIA SLIDES AS AI DOUBTS HIT MARKETS",
     "Nvidia shares fall about 7% on Tuesday as lawmakers question President Trump's role in bringing back CEO Jensen Huang. Japan's Nikkei drops 2.76% and the S and P 500 falls 0.5%.",
     "REPORTED", "OneTurn, Deutsche Welle, 25 Nov", "AMERICAS", 37.37, -121.98, ""),
    (8, "HOUTHI DRONE ATTACK ON RIYADH TOWER WOUNDS 11",
     "A Houthi drone hits a tower in Riyadh's financial district, wounding 11, Saudi officials say. The Saudi-led coalition orders civilians out of Yemen's port of Hodeidah.",
     "REPORTED", "Saudi officials, Al Jazeera, 25 Nov", "MIDDLE EAST", 24.71, 46.68, ""),
    (9, "HUAWEI CONVICTED ON 10 OF 12 US COUNTS",
     "A Brooklyn jury convicts Huawei of bank and wire fraud, sanctions violations and conspiring to steal trade secrets over its Iran business. It acquits the firm of racketeering.",
     "CONFIRMED", "Reuters, The Register, 25 Nov", "AMERICAS", 40.71, -73.99, ""),
    (10, "SANCHEZ AND FEIJOO CLASH IN TV DEBATE BEFORE SNAP VOTE",
     "Spain's PM Pedro Sanchez faces rival Alberto Nunez Feijoo in a televised debate four days before Sunday's snap election, called after parliament rejected his housing decrees.",
     "CONFIRMED", "Reuters, 25 Nov", "EUROPE", 40.42, -3.70, ""),
]

# (number, title, detail, sources, region, lat, lon)
ALSO = [
    (11, "NORWAY PLEDGES AT LEAST $7BN TO UKRAINE IN 2027",
     "Air defence first, Kyiv says after talks in Oslo.",
     "Kyiv Independent, Reuters", "EUROPE", 59.91, 10.75),
    (12, "HUNGARY'S MAGYAR MEETS ZELENSKY FOR FIRST TIME",
     "First formal meeting, in Uzhhorod.",
     "Silk Paradox, Kyiv Independent", "EUROPE", 48.62, 22.29),
    (13, "STRIKE ON ZAPORIZHZHIA FLATS KILLS 2, WOUNDS 40+",
     "Rescuers pull survivors from the rubble.",
     "Kyiv Independent, Reuters", "EUROPE", 47.84, 35.14),
    (14, "LATVIA WEIGHS CLOSING ITS BORDER WITH RUSSIA",
     "Riga prepares a position; Moscow summons envoy.",
     "Delfi, Moscow Times", "EUROPE", 56.95, 24.11),
    (15, "KYIV CLAIMS BALTIC SHIP STRIKE; NORWAY URGES CALM",
     "Zelensky: every Russian-flagged ship is a target.",
     "Kyiv Independent, Al Jazeera", "EUROPE", 59.90, 24.00),
    (16, "UKRAINE DEFENDS LIBYA SEA STRIKE AS SELF-DEFENCE",
     "Kyiv cites Article 51 after the sinking.",
     "Kyiv Independent, Al Jazeera", "EUROPE", 32.90, 13.19),
    (17, "TRUMP: IRAN REGIME CHANGE 'PROBABLY DOABLE'",
     "He says it is not his goal.",
     "Middle East Forum, 25 Nov", "MIDDLE EAST", 38.90, -77.04),
    (18, "ABREGO GARCIA LEAVES THE US FOR SPAIN",
     "At the centre of a deportation fight, he departs.",
     "OneTurn, 25 Nov", "AMERICAS", 38.98, -76.99),
    (19, "CHINA PROBES SHANGHAI PARTY CHIEF CHEN JINING",
     "Beijing opens a probe into a most senior official.",
     "OneTurn, 25 Nov", "ASIA", 31.23, 121.47),
    (20, "IRAN FLOGS SINGER 74 TIMES OVER UNVEILED CONCERT",
     "Punishment in Qom follows an unveiled concert.",
     "OneTurn, 25 Nov", "MIDDLE EAST", 34.64, 50.88),
    (21, "DR CONGO PLANE MISSING AS REBELS CLAIM DOWNING",
     "Plane vanishes near Minembwe; rebels claim it.",
     "OneTurn, 25 Nov", "AFRICA", -3.00, 28.90),
    (22, "PENTAGON CRITICISES CANADA'S MILITARY SPENDING",
     "Washington presses Ottawa to spend more.",
     "OneTurn, 25 Nov", "AMERICAS", 45.42, -75.70),
    (23, "HONG KONG MARKS A YEAR SINCE THE TAI PO FIRE",
     "The city remembers the blaze of a year ago.",
     "OneTurn, 25 Nov", "ASIA", 22.44, 114.17),
    (24, "RESCUE RACE FOR DOZENS TRAPPED IN BOGOR GOLD MINE",
     "Floodwater fills illegal shafts in West Java.",
     "Reuters, Xinhua, 25 Nov", "ASIA", -6.60, 106.80),
    (25, "DRONE ATTACKS ON KHARTOUM DRAW CONDEMNATION",
     "Abductions are also reported in Blue Nile state.",
     "OneTurn, 25 Nov", "AFRICA", 15.60, 32.53),
    (26, "IRAQ ORDERS TROOPS TO SEIZE KURDISH OILFIELDS",
     "Federal forces move into Kurdish-run regions.",
     "Starlit Daily, DW, 25 Nov", "MIDDLE EAST", 36.19, 44.01),
    (27, "BRITAIN SANCTIONS THE HOUTHIS AND FOUR OFFICIALS",
     "London blacklists group and four top officials.",
     "Starlit Daily, 25 Nov", "EUROPE", 51.50, -0.13),
    (28, "XIAMEN AIRLINES ORDERS 50 BOEING 737-8 JETS",
     "China Southern unit agrees a big new fleet deal.",
     "Starlit Daily, 25 Nov", "ASIA", 24.48, 118.09),
    (29, "NIGERIAN EMIR SUSPENDED AFTER ASSAULT ALLEGATION",
     "Traditional ruler suspended pending investigation.",
     "Starlit Daily, 25 Nov", "AFRICA", 11.00, 7.70),
    (30, "BANGLADESH OPENS INVEST OFFICE IN GUANGZHOU",
     "Dhaka plants a trade flag in southern China.",
     "Starlit Daily, 25 Nov", "ASIA", 23.13, 113.26),
    (31, "DR CONGO REBELS PULL BACK AFTER CLASHES",
     "Rebels withdraw from areas held in the east.",
     "Starlit Daily, 25 Nov", "AFRICA", -1.66, 29.22),
    (32, "CAMEROON SEPARATIST IN NORWAY WAR-CRIMES COURT",
     "The accused faces war-crimes charges in Oslo.",
     "Starlit Daily, 25 Nov", "EUROPE", 59.91, 10.75),
    (33, "HAMAS SECURITY CHIEF KILLED IN GAZA DRONE STRIKE",
     "Israel says it killed the Hamas security chief.",
     "Middle East Forum, 25 Nov", "MIDDLE EAST", 31.50, 34.47),
    (34, "ICC JUDGES LOSE BID TO BLOCK TRUMP SANCTIONS",
     "Judges fail to stop the US sanctions against them.",
     "Middle East Forum, 25 Nov", "EUROPE", 52.08, 4.32),
    (35, "FIVE TURKISH AIRMEN KILLED IN HELICOPTER CRASH",
     "Five airmen die when their helicopter goes down.",
     "Middle East Forum, 25 Nov", "EUROPE", 39.93, 32.86),
    (36, "VENEZUELA REVEALS $237.5BN PUBLIC DEBT",
     "Caracas puts total public debt on the record.",
     "OneTurn, 25 Nov", "AMERICAS", 10.49, -66.88),
    (37, "ARGENTINA ENTERS TECHNICAL RECESSION",
     "Two quarters of contraction: recession.",
     "OneTurn, 25 Nov", "AMERICAS", -34.60, -58.38),
    (38, "TRUMP PARDONS TURKEYS FEATHERS AND FREEDOM",
     "White House keeps the Thanksgiving-eve tradition.",
     "Middle East Forum, 25 Nov", "AMERICAS", 38.90, -77.04),
    (39, "AI STAFF DOUBT UNRELEASED MODELS ARE SAFE",
     "Staff question safety, Axios reports.",
     "Axios via Daily Edition, 25 Nov", "AMERICAS", 37.77, -122.42),
    (40, "US PREPARES NEW GLOBAL TARIFFS AFTER TRADE PROBE",
     "Washington readies fresh tariffs after a probe.",
     "Daily Edition, 25 Nov", "AMERICAS", 38.90, -77.04),
]

NUMBERS = [
    ("00:18", "UTC, SHENZHOU-24 LIFTS OFF FROM JIUQUAN"),
    ("2", "OIL TANKERS HIT BY MINES IN HORMUZ"),
    ("30", "HOSTAGES FREED IN CARTAGENA"),
    ("10/12", "COUNTS HUAWEI IS CONVICTED ON"),
    ("-2.76%", "NIKKEI FALL AS AI DOUBTS SPREAD"),
    ("$7BN", "NORWAY PLEDGES TO UKRAINE FOR 2027"),
]

TIMELINE = [
    ("00:18", "SHENZHOU-24 LAUNCHES"),
    ("03:56", "DOCKS WITH TIANGONG"),
    ("06:00", "CARTAGENA SIEGE ENDS"),
    ("MORNING", "PHALA PHALA RULING"),
    ("TODAY", "SOLOMON TREATY"),
    ("EVENING", "SPAIN TV DEBATE"),
]

DATECHECK = [
    "EXCLUDED AFTER DATE CHECK: ICJ MYANMAR GENOCIDE RULING 19 NOV - COP31 TALKS COLLAPSED 22 NOV - SENEGAL AFCON TITLE RESTORED BY CAS 24 NOV -",
    "ZAMBIA TREASON COMMITTAL 23 NOV - REAL MADRID 5-1 PSV 24 NOV - PHALA PHALA BURGLARY VERDICTS 2 NOV. HUAWEI VERDICT WAS DELIVERED TUE 24 NOV IN NEW YORK,",
    "FIRST WIDELY REPORTED WED 25 NOV, SO IT IS COUNTED AS REPORTED TODAY. EVERY NUMBERED STORY ABOVE WAS CHECKED AGAINST 2+ OUTLETS FOR 25 NOV 2026.",
]

# Rough continent outlines (lon, lat) for the dotted world map.
CONTINENTS = [
    [(-168, 66), (-140, 70), (-120, 72), (-95, 80), (-75, 73), (-55, 62), (-60, 47), (-70, 42), (-75, 35), (-80, 26), (-85, 20), (-95, 16), (-105, 20), (-115, 28), (-125, 40), (-125, 49), (-145, 60), (-165, 60)],
    [(-55, 60), (-45, 60), (-30, 68), (-25, 76), (-55, 80), (-60, 74)],
    [(-80, 10), (-75, 5), (-60, 0), (-50, -5), (-35, -8), (-40, -20), (-50, -30), (-60, -38), (-70, -50), (-73, -40), (-75, -25), (-80, -15), (-80, 0)],
    [(-17, 15), (-10, 30), (0, 35), (10, 37), (20, 32), (32, 31), (35, 28), (43, 12), (51, 11), (48, 0), (40, -10), (35, -20), (28, -33), (18, -35), (12, -18), (8, 4), (-8, 5), (-17, 15)],
    [(-10, 36), (-9, 43), (-2, 48), (0, 50), (5, 53), (8, 57), (18, 56), (21, 55), (28, 59), (30, 60), (25, 65), (30, 70), (45, 68), (60, 69), (75, 73), (90, 75), (110, 76), (130, 72), (150, 70), (170, 67), (178, 65), (170, 60), (162, 56), (158, 52), (142, 50), (140, 40), (135, 35), (130, 33), (122, 30), (115, 23), (108, 18), (105, 10), (100, 8), (97, 15), (92, 21), (88, 22), (80, 13), (77, 8), (73, 20), (66, 25), (60, 25), (56, 27), (50, 29), (48, 30), (44, 29), (40, 36), (36, 36), (30, 36), (26, 38), (22, 37), (19, 40), (15, 44), (12, 44), (8, 44), (3, 43), (-2, 37), (-9, 37), (-10, 36)],
    [(-5, 50), (-3, 53), (-5, 56), (-3, 58), (-1, 57), (0, 53), (1, 51), (-3, 50)],
    [(130, 31), (133, 34), (137, 35), (140, 38), (141, 42), (143, 44), (141, 45), (139, 41), (137, 37), (133, 34)],
    [(113, -22), (114, -30), (115, -35), (124, -33), (130, -32), (137, -35), (140, -38), (145, -38), (150, -37), (153, -32), (153, -27), (150, -22), (146, -19), (142, -15), (142, -11), (137, -12), (135, -15), (132, -12), (130, -13), (126, -14), (122, -17), (118, -20), (113, -22)],
    [(167, -45), (170, -42), (174, -40), (177, -38), (175, -36), (173, -35), (174, -38), (171, -41), (167, -45)],
    [(109, 1), (113, 4), (117, 6), (119, 1), (117, -3), (113, -3), (110, -2)],
    [(95, 5), (100, 0), (104, -3), (106, -6), (103, -5), (99, -1)],
    [(105, -6), (110, -7), (114, -8), (114, -7), (108, -6)],
    [(131, -1), (136, -2), (141, -3), (146, -6), (150, -10), (146, -8), (141, -8), (136, -4), (131, -2)],
    [(44, -16), (47, -15), (50, -16), (49, -20), (46, -24), (44, -25), (43, -21), (44, -16)],
]

# ---------------------------------------------------------------- render

def fill_poly(cv, pts, x0, y0, sx, sy, color):
    """Scanline fill of a lon/lat polygon projected into the map box."""
    px = [(x0 + (lon + 180.0) / 360.0 * sx, y0 + (82.0 - lat) / 140.0 * sy)
          for lon, lat in pts]
    ys = [p[1] for p in px]
    for y in range(int(max(y0, min(ys))), int(min(y0 + sy, max(ys))) + 1):
        xs = []
        n = len(px)
        for i in range(n):
            x1, y1 = px[i]
            x2, y2 = px[(i + 1) % n]
            if (y1 <= y < y2) or (y2 <= y < y1):
                xs.append(x1 + (y - y1) * (x2 - x1) / (y2 - y1))
        xs.sort()
        for i in range(0, len(xs) - 1, 2):
            for x in range(int(xs[i]), int(xs[i + 1]) + 1):
                cv.set(x, y, color)


def draw_map(cv, x0, y0, w, h):
    cv.text(x0 + 4, y0, "WHERE IT HAPPENED", 1, NAVY, bold=True)
    px0, py0, pw, ph = x0 + 4, y0 + 12, 300, h - 16
    cv.rect(px0 - 1, py0 - 1, pw + 2, ph + 2, MAPLINE)
    cv.rect(px0, py0, pw, ph, (238, 234, 222))
    for k in range(1, 12):
        cv.vline(px0 + k * pw // 12, py0, ph, (226, 221, 206))
    for k in range(1, 5):
        cv.hline(px0, py0 + k * ph // 5, pw, (226, 221, 206))
    for poly in CONTINENTS:
        fill_poly(cv, poly, px0, py0, pw, ph, MAPLAND)
    for poly in CONTINENTS:
        pts = [(px0 + (lon + 180.0) / 360.0 * pw,
                py0 + (82.0 - lat) / 140.0 * ph) for lon, lat in poly]
        for i in range(len(pts)):
            x1, y1 = pts[i]
            x2, y2 = pts[(i + 1) % len(pts)]
            cv.line(int(x1), int(y1), int(x2), int(y2), MAPLINE)
    # pins, nudged apart when they would collide
    placed = []
    allstories = [(n, lat, lon, True) for (n, _t, _b, _s, _src, _r, lat, lon, _u) in FEATURES]
    allstories += [(n, lat, lon, False) for (n, _t, _d, _src, _r, lat, lon) in ALSO]
    for n, lat, lon, is_feat in allstories:
        x = int(px0 + (lon + 180.0) / 360.0 * pw)
        y = int(py0 + (82.0 - lat) / 140.0 * ph)
        for _ in range(8):
            if all(abs(x - ox) > 13 or abs(y - oy) > 13 for ox, oy in placed):
                break
            x = min(px0 + pw - 9, x + 11)
            y = min(py0 + ph - 9, y + 7)
            if x >= px0 + pw - 9 and y >= py0 + ph - 9:
                break
        placed.append((x, y))
        r = 8 if n >= 10 else 7
        cv.circle(x, y, r, RED if is_feat else NAVY, fill=True)
        cv.circle(x, y, r, PAPER, fill=False)
        s = str(n)
        cv.text(x - len(s) * 3, y - 3, s, 1, PAPER)
    # legend, right of the map
    lx = x0 + 312
    cv.text(lx, y0 + 16, "PINS ARE", 1, INK, bold=True)
    cv.text(lx, y0 + 26, "NUMBERED", 1, INK, bold=True)
    cv.text(lx, y0 + 36, "TO MATCH", 1, INK, bold=True)
    cv.text(lx, y0 + 46, "THE STORIES", 1, INK, bold=True)
    cv.circle(lx + 6, y0 + 66, 7, RED, fill=True)
    cv.text(lx + 18, y0 + 63, "1-10 TOP", 1, INK)
    cv.circle(lx + 6, y0 + 84, 7, NAVY, fill=True)
    cv.text(lx + 18, y0 + 81, "11-40 ALSO ON", 1, INK)
    cv.text(lx, y0 + 100, "DOTS: LAND", 1, GREY)


def draw_feature(cv, x, y, w, n, title, body, status, src):
    cv.rect(x, y, w, 84, PAPER)
    cv.rect(x, y, w, 1, LIGHT)
    cv.rect(x, y, 1, 84, LIGHT)
    cv.rect(x + w - 1, y, 1, 84, LIGHT)
    cv.rect(x, y + 83, w, 1, LIGHT)
    cv.circle(x + 14, y + 14, 11, RED, fill=True)
    s = str(n)
    cv.text(x + 14 - len(s) * 3, y + 11, s, 1, PAPER)
    lines = cv.wrap(title, 38)[:2]
    for i, ln in enumerate(lines):
        cv.text(x + 32, y + 5 + i * 18, ln, 2, INK, bold=True)
    blines = cv.wrap(body, 78)[:3]
    for i, ln in enumerate(blines):
        cv.text(x + 8, y + 43 + i * 9, ln, 1, (58, 56, 50))
    sc = TEAL if status == "CONFIRMED" else (RED if status == "OFFICIALS SAY" else GOLD)
    cv.text(x + 8, y + 72, status, 1, sc, bold=True)
    cv.text(x + 8 + cv.text_w(status, 1) + 6, y + 72, "- " + src, 1, GREY)


def render():
    cv = Canvas(W, H, PAPER)
    # masthead
    cv.hline(0, 0, W, RED, 4)
    cv.center(8, "THE WORLD IN ONE PAGE", 4, NAVY, bold=True)
    cv.center(44, "WEDNESDAY 25 NOVEMBER 2026", 5, INK, bold=True)
    cv.center(84, "40 VERIFIED STORIES FROM WEDNESDAY 25 NOVEMBER 2026 - EVERY STORY CHECKED AGAINST TWO OR MORE OUTLETS", 1, GREY)
    cv.hline(16, 96, W - 32, INK, 2)
    # region tabs
    cv.rect(0, 100, W, 18, NAVY)
    cv.center(105, "AFRICA 5  |  MIDDLE EAST 7  |  ASIA 6  |  EUROPE 11  |  AMERICAS 10  |  PACIFIC 1  |  TOTAL 40 STORIES", 1, PAPER, bold=True)
    # features: 2 columns x 5 rows
    for i, (n, title, body, status, src, _r, _la, _lo, _u) in enumerate(FEATURES):
        col = i % 2
        row = i // 2
        x = 16 + col * 504
        y = 122 + row * 84
        draw_feature(cv, x, y, 488, n, title, body, status, src)
    # map + numbers band
    cv.hline(16, 544, W - 32, INK, 1)
    draw_map(cv, 16, 550, 388, 132)
    cv.text(424, 550, "THE DAY IN NUMBERS", 1, NAVY, bold=True)
    for i, (big, label) in enumerate(NUMBERS):
        col = i % 3
        row = i // 3
        bx = 424 + col * 198
        by = 566 + row * 58
        cv.rect(bx, by, 192, 52, (255, 253, 247))
        cv.rect(bx, by, 192, 1, LIGHT)
        cv.rect(bx, by, 1, 52, LIGHT)
        cv.rect(bx + 191, by, 1, 52, LIGHT)
        cv.rect(bx, by + 51, 192, 1, LIGHT)
        cv.text(bx + 8, by + 5, big, 3, RED, bold=True)
        for j, ln in enumerate(cv.wrap(label, 30)[:2]):
            cv.text(bx + 8, by + 29 + j * 9, ln, 1, (58, 56, 50))
    # UTC timeline
    cv.text(16, 694, "UTC TIMELINE", 1, NAVY, bold=True)
    for i, (t, label) in enumerate(TIMELINE):
        bx = 110 + i * 146
        cv.rect(bx, 690, 140, 28, (255, 253, 247))
        cv.rect(bx, 690, 140, 1, LIGHT)
        cv.rect(bx, 690, 1, 28, LIGHT)
        cv.rect(bx + 139, 690, 1, 28, LIGHT)
        cv.rect(bx, 717, 140, 1, LIGHT)
        cv.text(bx + 6, 694, t, 1, RED, bold=True)
        cv.text(bx + 6, 705, label, 1, INK)
    # also on
    cv.text(16, 728, "ALSO ON - 30 MORE STORIES FROM THE SAME DAY", 2, NAVY, bold=True)
    cv.hline(16, 744, W - 32, INK, 1)
    for i, (n, title, detail, src, _r, _la, _lo) in enumerate(ALSO):
        col = i // 10
        row = i % 10
        x = 16 + col * 336
        y = 752 + row * 21
        cv.text(x, y, str(n) + ". " + title, 1, INK, bold=True)
        cv.text(x + 18, y + 10, detail[:50], 1, (58, 56, 50))
    # date-check audit
    cv.hline(16, 962, W - 32, INK, 1)
    cv.text(16, 968, "DATE-CHECK AUDIT - STORIES WE CHECKED AND LEFT OUT", 1, RED, bold=True)
    for i, ln in enumerate(DATECHECK):
        cv.text(16, 980 + i * 9, ln, 1, (58, 56, 50))
    # footer
    cv.hline(16, 1008, W - 32, GREY, 1)
    cv.center(1013, "THE WORLD IN ONE PAGE - 40 STORIES, ALL FROM WEDNESDAY 25 NOVEMBER 2026 - SOURCES NAMED ON EVERY STORY", 1, GREY)
    return cv


def main():
    outdir = os.environ.get("MAKEFUN_OUTPUT_DIR") or "/output"
    os.makedirs(outdir, exist_ok=True)
    cv = render()
    path = os.path.join(outdir, "entry.png")
    size = write_png(cv, path)
    print("wrote %s %d bytes" % (path, size))


if __name__ == "__main__":
    main()

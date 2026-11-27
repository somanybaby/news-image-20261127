#!/usr/bin/env python3
"""One-page newspaper image of the world news of Friday 27 November 2026.

Pure Python standard library only (os, struct, zlib). No network, no PIL.
Draws its own 5x7 bitmap font on its own canvas class and writes a
deterministic 1024x1024 PNG: running twice produces identical bytes.

Run:  python3 main.py
Writes entry.png in the current directory, or /output/entry.png when
that directory exists (the competition sandbox).
"""

import os
import struct
import zlib

W = 1024
H = 1024

CREAM = (247, 240, 220)
INK = (25, 25, 25)
RED = (169, 50, 38)
NAVY = (31, 78, 121)

# ---------------------------------------------------------------------------
# 5x7 bitmap font, drawn from scratch. Each glyph is 7 rows of 5 cells,
# "#" is ink, "." is empty. Only uppercase text is rendered.
# ---------------------------------------------------------------------------
GLYPHS = {
    "A": (".###.", "#...#", "#...#", "#####", "#...#", "#...#", "#...#"),
    "B": ("####.", "#...#", "#...#", "####.", "#...#", "#...#", "####."),
    "C": (".####", "#....", "#....", "#....", "#....", "#....", ".####"),
    "D": ("####.", "#...#", "#...#", "#...#", "#...#", "#...#", "####."),
    "E": ("#####", "#....", "#....", "####.", "#....", "#....", "#####"),
    "F": ("#####", "#....", "#....", "####.", "#....", "#....", "#...."),
    "G": (".####", "#....", "#....", "#.###", "#...#", "#...#", ".###."),
    "H": ("#...#", "#...#", "#...#", "#####", "#...#", "#...#", "#...#"),
    "I": ("#####", "..#..", "..#..", "..#..", "..#..", "..#..", "#####"),
    "J": ("..###", "...#.", "...#.", "...#.", "...#.", "#..#.", ".##.."),
    "K": ("#...#", "#..#.", "#.#..", "##...", "#.#..", "#..#.", "#...#"),
    "L": ("#....", "#....", "#....", "#....", "#....", "#....", "#####"),
    "M": ("#...#", "##.##", "#.#.#", "#.#.#", "#...#", "#...#", "#...#"),
    "N": ("#...#", "##..#", "#.#.#", "#..##", "#...#", "#...#", "#...#"),
    "O": (".###.", "#...#", "#...#", "#...#", "#...#", "#...#", ".###."),
    "P": ("####.", "#...#", "#...#", "####.", "#....", "#....", "#...."),
    "Q": (".###.", "#...#", "#...#", "#...#", "#.#.#", "#..#.", ".##.#"),
    "R": ("####.", "#...#", "#...#", "####.", "#.#..", "#..#.", "#...#"),
    "S": (".####", "#....", "#....", ".###.", "....#", "....#", "####."),
    "T": ("#####", "..#..", "..#..", "..#..", "..#..", "..#..", "..#.."),
    "U": ("#...#", "#...#", "#...#", "#...#", "#...#", "#...#", ".###."),
    "V": ("#...#", "#...#", "#...#", "#...#", "#...#", ".#.#.", "..#.."),
    "W": ("#...#", "#...#", "#...#", "#.#.#", "#.#.#", "##.##", "#...#"),
    "X": ("#...#", "#...#", ".#.#.", "..#..", ".#.#.", "#...#", "#...#"),
    "Y": ("#...#", "#...#", ".#.#.", "..#..", "..#..", "..#..", "..#.."),
    "Z": ("#####", "....#", "...#.", "..#..", ".#...", "#....", "#####"),
    "0": (".###.", "#...#", "#..##", "#.#.#", "##..#", "#...#", ".###."),
    "1": ("..#..", ".##..", "..#..", "..#..", "..#..", "..#..", ".###."),
    "2": (".###.", "#...#", "....#", "...#.", "..#..", ".#...", "#####"),
    "3": ("####.", "....#", "....#", ".###.", "....#", "....#", "####."),
    "4": ("...#.", "..##.", ".#.#.", "#..#.", "#####", "...#.", "...#."),
    "5": ("#####", "#....", "####.", "....#", "....#", "#...#", ".###."),
    "6": (".###.", "#....", "#....", "####.", "#...#", "#...#", ".###."),
    "7": ("#####", "....#", "...#.", "...#.", "..#..", "..#..", "..#.."),
    "8": (".###.", "#...#", "#...#", ".###.", "#...#", "#...#", ".###."),
    "9": (".###.", "#...#", "#...#", ".####", "....#", "....#", ".###."),
    " ": (".....", ".....", ".....", ".....", ".....", ".....", "....."),
    ".": (".....", ".....", ".....", ".....", ".....", ".##..", ".##.."),
    ",": (".....", ".....", ".....", ".....", ".....", ".##..", "##..."),
    ":": (".....", ".##..", ".##..", ".....", ".##..", ".##..", "....."),
    ";": (".....", ".##..", ".##..", ".....", ".##..", ".##..", ".#..."),
    "!": ("..#..", "..#..", "..#..", "..#..", "..#..", ".....", "..#.."),
    "?": (".###.", "#...#", "....#", "...#.", "..#..", ".....", "..#.."),
    "'": ("..#..", "..#..", ".#...", ".....", ".....", ".....", "....."),
    '"': (".#.#.", ".#.#.", ".....", ".....", ".....", ".....", "....."),
    "-": (".....", ".....", ".....", "#####", ".....", ".....", "....."),
    "(": ("...##", "..#..", ".#...", ".#...", ".#...", "..#..", "...##"),
    ")": ("##...", "..#..", "...#.", "...#.", "...#.", "..#..", "##..."),
    "/": ("....#", "....#", "...#.", "..#..", ".#...", "#....", "#...."),
    "%": ("#...#", "#..#.", "...#.", "..#..", ".#...", "#..#.", "#...#"),
    "&": (".##..", "#..#.", "#..#.", ".#...", "#.#.#", "#..#.", ".##.#"),
    "+": (".....", "..#..", "..#..", "#####", "..#..", "..#..", "....."),
    "=": (".....", ".....", "#####", ".....", "#####", ".....", "....."),
    "*": (".....", ".#.#.", "..#..", "#####", "..#..", ".#.#.", "....."),
    "$": ("..#..", ".####", "#.#..", ".###.", "..#.#", "####.", "..#.."),
    "#": (".#.#.", ".#.#.", "#####", ".#.#.", "#####", ".#.#.", ".#.#."),
    "_": (".....", ".....", ".....", ".....", ".....", ".....", "#####"),
    "[": (".###.", ".#...", ".#...", ".#...", ".#...", ".#...", ".###."),
    "]": (".###.", "...#.", "...#.", "...#.", "...#.", "...#.", ".###."),
}


class Sheet:
    """A plain RGB pixel buffer with tiny drawing helpers."""

    def __init__(self, w, h, bg):
        self.w = w
        self.h = h
        self.px = bytearray(bytes(bg) * (w * h))

    def fill(self, x, y, w, h, color):
        x0 = max(0, x)
        y0 = max(0, y)
        x1 = min(self.w, x + w)
        y1 = min(self.h, y + h)
        if x1 <= x0 or y1 <= y0:
            return
        row = bytes(color) * (x1 - x0)
        span = (x1 - x0) * 3
        for yy in range(y0, y1):
            i = (yy * self.w + x0) * 3
            self.px[i:i + span] = row

    def border(self, x, y, w, h, t, color):
        self.fill(x, y, w, t, color)
        self.fill(x, y + h - t, w, t, color)
        self.fill(x, y, t, h, color)
        self.fill(x + w - t, y, t, h, color)

    def glyph(self, x, y, ch, scale, color):
        rows = GLYPHS.get(ch, GLYPHS[" "])
        for r, line in enumerate(rows):
            for c, bit in enumerate(line):
                if bit == "#":
                    self.fill(x + c * scale, y + r * scale, scale, scale, color)

    def text(self, x, y, s, scale, color):
        cx = x
        for ch in s:
            self.glyph(cx, y, ch, scale, color)
            cx += 6 * scale
        return cx

    def text_w(self, s, scale):
        return len(s) * 6 * scale

    def wrap(self, s, scale, max_w):
        lines = []
        cur = ""
        for word in s.split(" "):
            trial = word if not cur else cur + " " + word
            if self.text_w(trial, scale) <= max_w:
                cur = trial
            else:
                if cur:
                    lines.append(cur)
                cur = word
        if cur:
            lines.append(cur)
        return lines

    def para(self, x, y, s, scale, color, max_w, leading):
        for i, line in enumerate(self.wrap(s, scale, max_w)):
            self.text(x, y + i * leading, line, scale, color)


def write_png(path, w, h, px):
    raw = bytearray()
    stride = w * 3
    for y in range(h):
        raw.append(0)
        raw += px[y * stride:(y + 1) * stride]
    data = zlib.compress(bytes(raw), 9)

    def chunk(tag, payload):
        out = struct.pack(">I", len(payload)) + tag + payload
        return out + struct.pack(">I", zlib.crc32(tag + payload) & 0xFFFFFFFF)

    png = b"\x89PNG\r\n\x1a\n"
    png += chunk(b"IHDR", struct.pack(">IIBBBBB", w, h, 8, 2, 0, 0, 0))
    png += chunk(b"IDAT", data)
    png += chunk(b"IEND", b"")
    with open(path, "wb") as f:
        f.write(png)


def centered(sheet, y, s, scale, color):
    x = (W - sheet.text_w(s, scale)) // 2
    sheet.text(x, y, s, scale, color)


def story(sheet, x, y, w, kicker, headline, body):
    """One grid story: red kicker, wrapped headline, wrapped body."""
    sheet.text(x, y, kicker, 2, RED)
    hy = y + 22
    for i, line in enumerate(sheet.wrap(headline, 3, w)):
        sheet.text(x, hy + i * 27, line, 3, INK)
    n_head = len(sheet.wrap(headline, 3, w))
    sheet.para(x, hy + n_head * 27 + 10, body, 2, INK, w, 19)


def main():
    s = Sheet(W, H, CREAM)
    s.border(18, 18, 988, 988, 5, INK)
    s.border(30, 30, 964, 964, 2, INK)

    # Masthead.
    centered(s, 52, "THE WORLD IN ONE PAGE", 5, INK)
    centered(s, 100, "FRIDAY, 27 NOVEMBER 2026", 2, NAVY)
    s.fill(60, 106, 280, 2, RED)
    s.fill(684, 106, 280, 2, RED)
    s.fill(40, 128, 944, 3, INK)

    # Top story: the Thanksgiving storm in the United States.
    centered(s, 148, "TOP STORY - UNITED STATES", 2, RED)
    centered(s, 172, "US STORM WRECKS THANKSGIVING", 4, INK)
    centered(s, 214, "400 FLIGHTS AXED, 724,000 HOMES DARK", 3, RED)
    s.para(48, 252,
           "A POWERFUL STORM SWEPT THE US EAST ON THANKSGIVING, CANCELLING "
           "MORE THAN 400 FLIGHTS AND CUTTING POWER TO 724,000 HOMES. NEW "
           "YORK'S MACY'S PARADE WAS POSTPONED FOR THE FIRST TIME IN "
           "100 YEARS.",
           2, INK, 928, 19)
    # 8px clear between the top story's last line and its rule.
    s.fill(40, 330, 944, 2, INK)

    # Row 1: Gulf escalation, then Russia-Ukraine.
    story(s, 48, 348, 440, "02 - MIDDLE EAST",
          "GULF ON EDGE AFTER STRIKES",
          "IRANIAN DRONES HIT KUWAIT, KILLING TWO ITALIAN TECHNICIANS, AND "
          "BLASTS STRUCK TANKERS IN THE STRAIT OF HORMUZ AS THE US AND "
          "IRAN BATTLE FOR THE WATERWAY.")
    story(s, 536, 348, 440, "03 - UKRAINE",
          "RUSSIA HITS UKRAINE, 5 DEAD",
          "RUSSIAN STRIKES KILLED FIVE PEOPLE AND KNOCKED OUT POWER ACROSS "
          "UKRAINE, AND ZELENSKY WARNED OF A NEW MASS STRIKE IN THE COMING "
          "DAYS.")
    s.fill(40, 542, 944, 2, INK)

    # Row 2: Ibiza tanker, then New Zealand's deadlocked election.
    story(s, 48, 560, 440, "04 - EUROPE",
          "TANKER CAPSIZES OFF IBIZA",
          "A DIESEL TANKER, THE MED EMRE, CAPSIZED OFF IBIZA WITH UP TO "
          "7,000 TONNES ABOARD. ONE CREW MEMBER DIED AND SPAIN ACTIVATED "
          "ITS LEVEL 2 POLLUTION PLAN.")
    story(s, 536, 560, 440, "05 - PACIFIC",
          "NZ VOTE DEADLOCKED",
          "NEW ZEALAND'S ELECTION ENDED IN DEADLOCK. THE CENTRIST "
          "OPPORTUNITY PARTY, WITH SEVEN SEATS, NOW HOLDS THE BALANCE OF "
          "POWER.")
    s.fill(40, 754, 944, 2, INK)

    # Last story, full width: Delhi cyber-slavery bust.
    story(s, 48, 772, 928, "06 - SOUTH ASIA",
          "DELHI BUSTS CYBER-SLAVE RING",
          "DELHI POLICE RESCUED 164 FOREIGNERS, 92 INDONESIANS AND 72 "
          "MALAYSIANS, FROM A CYBER SLAVERY RACKET THAT LURED THEM WITH "
          "FAKE JOB OFFERS.")
    s.fill(40, 892, 944, 2, INK)
    centered(s, 916, "SIX STORIES - ONE PAGE - 27 NOVEMBER 2026", 2, NAVY)

    out = "/output/entry.png" if os.path.isdir("/output") else "entry.png"
    write_png(out, W, H, s.px)
    print("wrote %s (%d bytes)" % (out, os.path.getsize(out)))


if __name__ == "__main__":
    main()

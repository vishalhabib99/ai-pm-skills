"""Render docs/demo.gif: a replay of the real /build-or-not run in
examples/snake-case-tool-names.md, trimmed for length. Nothing here is
invented; every result line comes from that recorded output.

Run: python3 docs/make_demo_gif.py   (needs Pillow; macOS Menlo font)
"""

from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

W, H = 900, 560
PAD = 28
FONT_PATH = "/System/Library/Fonts/Menlo.ttc"
FONT = ImageFont.truetype(FONT_PATH, 15)
BOLD = ImageFont.truetype(FONT_PATH, 15, index=1)
SMALL = ImageFont.truetype(FONT_PATH, 12)
LINE_H = 23

BG = (22, 24, 30)
BAR = (38, 41, 50)
FG = (220, 223, 228)
DIM = (130, 136, 150)
ACCENT = (125, 170, 255)
GREEN = (120, 200, 140)
RED = (235, 120, 110)
YELLOW = (230, 200, 110)

PROMPT = "> /ai-pm-skills:build-or-not Add a check to mcp-doctor that flags"
PROMPT2 = "  MCP servers whose tool names aren't snake_case."

# (text, color, bold) — trimmed from examples/snake-case-tool-names.md
OUTPUT = [
    ("Build or not: non-snake_case tool-name check", ACCENT, True),
    ("", FG, False),
    ("Claim   Real MCP servers define at least one non-snake_case tool name", FG, False),
    ("Sample  6 real servers, by stars from the `mcp` GitHub topic", FG, False),
    ("Bar     set before checking: build if 3+ of 6", YELLOW, False),
    ("", FG, False),
    ("  1  DeusData/codebase-memory-mcp        Miss", FG, False),
    ("  2  microsoft/playwright-mcp            Miss", FG, False),
    ("  3  github/github-mcp-server            Miss", FG, False),
    ("  4  idosal/git-mcp                      Miss  (replaced mcp-toolbox: N/A)", FG, False),
    ("  5  GLips/Figma-Context-MCP             Miss", FG, False),
    ("  6  wonderwhy-er/DesktopCommanderMCP    Miss", FG, False),
    ("", FG, False),
    ("Result    0 of 6 reachable hits", FG, True),
    ("Decision  DON'T BUILD", RED, True),
    ("Reopen if servers whose tool names come from user config", GREEN, False),
    ("          commonly produce non-snake_case names", GREEN, False),
]

CAPTION = "Replay of a real run (Claude Sonnet, 2026-09-22), trimmed. Full output: examples/snake-case-tool-names.md"


def frame(typed1: str, typed2: str, n_out: int, cursor: bool) -> Image.Image:
    img = Image.new("RGB", (W, H), BG)
    d = ImageDraw.Draw(img)
    d.rectangle([0, 0, W, 30], fill=BAR)
    for i, c in enumerate([(237, 106, 94), (245, 191, 79), (98, 197, 84)]):
        d.ellipse([14 + i * 20, 10, 26 + i * 20, 22], fill=c)
    d.text((W // 2, 15), "claude", font=SMALL, fill=DIM, anchor="mm")

    y = 46
    d.text((PAD, y), typed1, font=FONT, fill=FG)
    if typed2:
        y += LINE_H
        d.text((PAD, y), typed2, font=FONT, fill=FG)
    if cursor and n_out == 0:
        line = typed2 if typed2 else typed1
        x = PAD + d.textlength(line, font=FONT)
        d.rectangle([x + 2, y + 2, x + 10, y + 18], fill=FG)

    y += LINE_H + 12
    for text, color, bold in OUTPUT[:n_out]:
        d.text((PAD, y), text, font=BOLD if bold else FONT, fill=color)
        y += LINE_H

    d.text((W // 2, H - 16), CAPTION, font=SMALL, fill=DIM, anchor="mm")
    return img


def main() -> None:
    frames, durations = [], []

    def add(img, ms):
        frames.append(img)
        durations.append(ms)

    add(frame("> ", "", 0, True), 600)
    for i in range(4, len(PROMPT) + 1, 4):
        add(frame(PROMPT[:i], "", 0, True), 45)
    for i in range(4, len(PROMPT2) + 1, 4):
        add(frame(PROMPT, PROMPT2[:i], 0, True), 45)
    add(frame(PROMPT, PROMPT2, 0, False), 900)
    for n in range(1, len(OUTPUT) + 1):
        add(frame(PROMPT, PROMPT2, n, False), 380 if OUTPUT[n - 1][0] else 120)
    durations[-1] = 5000

    pal = [f.convert("P", palette=Image.Palette.ADAPTIVE, colors=32) for f in frames]
    out = Path(__file__).with_name("demo.gif")
    pal[0].save(out, save_all=True, append_images=pal[1:], duration=durations, loop=0, optimize=True)
    print(f"wrote {out} ({out.stat().st_size // 1024} KB, {len(frames)} frames, {sum(durations) / 1000:.1f}s)")


if __name__ == "__main__":
    main()

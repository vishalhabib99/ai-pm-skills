"""Render docs/social-preview.png (1280x640), the image GitHub shows when
the repo link is shared. Upload it in the repo's Settings > Social preview.

Run: python3 docs/make_social_preview.py   (needs Pillow; macOS fonts)
"""

from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

W, H = 1280, 640
MONO = "/System/Library/Fonts/Menlo.ttc"
SANS = "/System/Library/Fonts/HelveticaNeue.ttc"

BG = (22, 24, 30)
PANEL = (32, 35, 44)
FG = (236, 238, 242)
DIM = (150, 156, 170)
ACCENT = (125, 170, 255)
GREEN = (120, 200, 140)


def font(path, size, index=0):
    return ImageFont.truetype(path, size, index=index)


def main() -> None:
    img = Image.new("RGB", (W, H), BG)
    d = ImageDraw.Draw(img)

    d.text((80, 70), "ai-pm-skills", font=font(MONO, 30), fill=ACCENT)
    d.text((80, 118), "Claude Code skills for", font=font(SANS, 58, 1), fill=FG)
    d.text((80, 186), "AI product managers", font=font(SANS, 58, 1), fill=FG)

    skills = [
        ("/build-or-not", "Check a feature idea against real examples before building it"),
        ("/eval-plan", "Set launch gates before any results exist"),
        ("/agent-trust-review", "Covered, declined on purpose, or genuinely missing"),
    ]
    y = 290
    for name, desc in skills:
        d.rounded_rectangle([80, y, W - 80, y + 72], radius=14, fill=PANEL)
        d.text((110, y + 20), name, font=font(MONO, 28), fill=GREEN)
        d.text((480, y + 24), desc, font=font(SANS, 24), fill=DIM)
        y += 88

    d.text((80, H - 62), "Each tested with evals whose gates were set before the first run, failures included.",
           font=font(SANS, 22), fill=DIM)

    out = Path(__file__).with_name("social-preview.png")
    img.save(out, optimize=True)
    print(f"wrote {out} ({out.stat().st_size // 1024} KB)")


if __name__ == "__main__":
    main()

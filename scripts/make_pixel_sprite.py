#!/usr/bin/env python3
"""
Turn a portrait photo into a pastel PIXEL-ART character, framed as a retro
KHUSHI.OS window, and export it as a looping GIF (bob + blink).

Pipeline
  1. rembg (u2netp model) cuts the subject out of the background
  2. the cutout is box-downsampled to a small pixel grid (COLS wide)
  3. colours are quantized to a small palette, then lifted toward cream so the
     result reads pastel instead of muddy
  4. a 1px deep-plum outline is drawn around the silhouette
  5. each grid cell is blown up to a crisp square (nearest neighbour)
  6. frames are composed into a window: lavender title bar, peach/mint panel

GitHub renders GIFs natively in README <img> tags, so the loop works without JS.

Usage
    python scripts/make_pixel_sprite.py <photo.png> [out.gif]
    python scripts/make_pixel_sprite.py --from-cutout <cutout.png> [out.gif]
    STATIC=1 python scripts/make_pixel_sprite.py ...   # single frame, for preview

Assets go to assets/ by default. The source photo is never written to the repo.
"""
import os
import sys

import numpy as np
from PIL import Image, ImageDraw, ImageEnhance, ImageFilter, ImageFont

HERE = os.path.dirname(os.path.abspath(__file__))
ASSETS = os.path.join(HERE, "..", "assets")

# ---- pixel grid -----------------------------------------------------------
COLS = 96              # pixel columns for the subject (higher = more detail)
PALETTE_K = 28         # colours kept from the photo before pastel lift
CROP_BOTTOM = 0.86     # keep this fraction of the subject height (head + shoulders)
SCALE = 4              # on-screen size of each pixel cell (screen px)

# ---- KHUSHI.OS palette ----------------------------------------------------
CREAM = np.array([255, 249, 238], np.float32)
PLUM = (56, 47, 74)                 # #382F4A outline
LAVENDER = (220, 206, 255)          # #DCCEFF
MINT = (191, 232, 213)              # #BFE8D5
BUTTER = (255, 240, 168)            # #FFF0A8
PEACH = (255, 214, 194)             # #FFD6C2
PLUM_SOFT = (120, 106, 145)         # #786A91
LIFT = 0.12                         # how far colours move toward cream (keep darks dark)

# ---- window chrome --------------------------------------------------------
TITLE_H = 40
PAD = 22
FOOT_H = 40
PANEL = PEACH

# ---- blink region (filled in once the portrait is inspected, see EYE_ROW) --
# Coordinates are in pixel-grid units. The blink copies the skin row just above
# the eyes down over them.
EYE_ROW = None         # set automatically below from the grid when None
EYE_COLS = None


def _rembg_cutout(path):
    from rembg import new_session, remove

    session = new_session("u2netp")
    return remove(Image.open(path).convert("RGBA"), session=session)


def _grid_from_cutout(cut):
    """Return (rgb_grid, alpha_grid) as PIL images sized COLS x ROWS."""
    bbox = cut.split()[-1].getbbox()
    if bbox:
        x0, y0, x1, y1 = bbox
        y1 = y0 + int((y1 - y0) * CROP_BOTTOM)
        cut = cut.crop((x0, y0, x1, y1))
    w, h = cut.size
    rows = max(1, round(COLS * h / w))
    rgb = cut.convert("RGB")
    # keep the subject crisp: paint background first so box-filter edges don't
    # bleed grey into the palette
    alpha = cut.split()[-1]
    bg = Image.new("RGB", cut.size, (255, 255, 255))
    bg.paste(rgb, mask=alpha)
    small = bg.resize((COLS, rows), Image.BOX)
    a_small = alpha.resize((COLS, rows), Image.BOX)
    return small, a_small, rows


def _quantize(rgb_img, alpha_img):
    """Quantize subject pixels to a small palette, then lift toward cream."""
    arr = np.array(rgb_img)
    mask = np.array(alpha_img) > 127
    base = Image.fromarray(arr)
    base = ImageEnhance.Contrast(base).enhance(1.12)
    q = base.quantize(colors=PALETTE_K, method=Image.Quantize.MEDIANCUT)
    pal = np.array(q.getpalette()[: PALETTE_K * 3], np.float32).reshape(-1, 3)
    idx = np.array(q)
    lifted = pal * (1 - LIFT) + CREAM * LIFT
    out = lifted[idx].clip(0, 255).astype(np.uint8)
    return Image.fromarray(out), Image.fromarray((mask * 255).astype(np.uint8))


def _outline(rgb_img, mask_img):
    """Add a 1px plum outline around the silhouette, with 1px padding."""
    w, h = rgb_img.size
    pw, ph = w + 2, h + 2
    canvas = Image.new("RGB", (pw, ph), (255, 255, 255))
    canvas.paste(rgb_img, (1, 1))
    m = Image.new("L", (pw, ph), 0)
    m.paste(mask_img, (1, 1))
    m = m.point(lambda v: 255 if v > 127 else 0)
    dilated = m.filter(ImageFilter.MaxFilter(3))
    outline = np.array(dilated) > 0
    inside = np.array(m) > 0
    ring = outline & ~inside
    arr = np.array(canvas)
    arr[ring] = PLUM
    arr[~outline] = (0, 0, 0)  # transparent marker, handled by alpha below
    alpha = np.where(outline, 255, 0).astype(np.uint8)
    rgba = np.dstack([arr, alpha])
    return Image.fromarray(rgba.astype(np.uint8), "RGBA")


def _auto_eye_rows(sprite):
    """Locate the eye band: the darkest pair of columns in the upper face."""
    arr = np.array(sprite.convert("L")).astype(np.float32)
    h, w = arr.shape
    top = int(h * 0.22)
    bot = int(h * 0.36)
    band = arr[top:bot, int(w * 0.30): int(w * 0.70)]
    row_dark = band.mean(axis=1)
    y = top + int(np.argmin(row_dark))
    return y


def _blink(sprite, eye_y):
    """Copy the skin row just above the eyes down over the eye band (a blink)."""
    arr = np.array(sprite).copy()
    src = arr[eye_y - 3]
    for dy in (-1, 0, 1):
        arr[eye_y + dy] = src
    return Image.fromarray(arr, "RGBA")


def _bob(sprite, dy):
    """Shift the sprite vertically by dy grid rows (transparent fill)."""
    w, h = sprite.size
    out = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    out.paste(sprite, (0, dy), sprite)
    return out


def _upscale(sprite):
    w, h = sprite.size
    return sprite.resize((w * SCALE, h * SCALE), Image.NEAREST)


def _frame(sprite_big, caption_title, caption_foot):
    """Compose one window frame. sprite_big is already upscaled RGBA."""
    sw, sh = sprite_big.size
    W = max(sw + PAD * 2, 360)
    H = TITLE_H + sh + PAD * 2 + FOOT_H
    img = Image.new("RGB", (W, H), BUTTER)
    d = ImageDraw.Draw(img)

    # window body: soft mint panel with a deep plum border
    d.rectangle([0, 0, W - 1, H - 1], fill=MINT, outline=PLUM, width=3)
    # title bar
    d.rectangle([0, 0, W - 1, TITLE_H], fill=LAVENDER, outline=PLUM, width=3)
    for i, c in enumerate([PEACH, BUTTER, MINT]):
        x = 16 + i * 18
        d.rectangle([x, 14, x + 10, 24], fill=c, outline=PLUM, width=2)

    # sprite stage
    sx = (W - sw) // 2
    sy = TITLE_H + PAD
    d.rectangle([sx - 10, sy - 10, sx + sw + 10, sy + sh + 10], fill=CREAM_HEX, outline=PLUM, width=2)
    stage = img.copy()
    stage.paste(sprite_big, (sx, sy), sprite_big)
    img = stage

    d = ImageDraw.Draw(img)
    font = _font(15)
    small = _font(12)
    d.text((96, 11), caption_title, fill=PLUM, font=font)
    d.text((PAD, H - FOOT_H + 12), caption_foot, fill=PLUM, font=small)
    return img


CREAM_HEX = (255, 249, 238)


def _font(size):
    for cand in [
        "/usr/share/fonts/truetype/dejavu/DejaVuSansMono-Bold.ttf",
        "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf",
    ]:
        if os.path.exists(cand):
            return ImageFont.truetype(cand, size)
    return ImageFont.load_default()


def build(src_cut):
    rgb, alpha, rows = _grid_from_cutout(src_cut)
    rgb_q, mask = _quantize(rgb, alpha)
    sprite = _outline(rgb_q, mask)
    global EYE_ROW
    eye_y = EYE_ROW if EYE_ROW is not None else _auto_eye_rows(sprite) + 1
    return sprite, eye_y


def main(argv):
    args = [a for a in argv[1:] if not a.startswith("--")]
    from_cutout = "--from-cutout" in argv
    if not args:
        print(__doc__)
        return 1
    src = args[0]
    out = args[1] if len(args) > 1 else os.path.join(ASSETS, "pixel-sprite.gif")
    os.makedirs(os.path.dirname(out) or ".", exist_ok=True)

    cut = Image.open(src).convert("RGBA") if from_cutout else _rembg_cutout(src)
    sprite, eye_y = build(cut)
    print("grid", sprite.size, "eye row", eye_y)

    big = _upscale(sprite)
    base = _frame(big, "khushi.exe", "KHUSHI.OS · character sprite")
    if os.environ.get("STATIC"):
        base.save(out)
        print("wrote", out, base.size)
        return 0

    # bob: sprite shifts up one grid row for a beat
    bob_big = _upscale(_bob(sprite, -1))
    bob_frame = _frame(bob_big, "khushi.exe", "KHUSHI.OS · character sprite")
    blink_big = _upscale(_blink(sprite, eye_y))
    blink_frame = _frame(blink_big, "khushi.exe", "KHUSHI.OS · character sprite")

    frames = [base, bob_frame, base, blink_frame]
    durations = [1100, 220, 1100, 130]
    frames = [f.convert("P", palette=Image.ADAPTIVE, colors=64) for f in frames]
    frames[0].save(
        out,
        save_all=True,
        append_images=frames[1:],
        duration=durations,
        loop=0,
        optimize=True,
        disposal=2,
    )
    print("wrote", out, os.path.getsize(out) // 1024, "KB", base.size)
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))

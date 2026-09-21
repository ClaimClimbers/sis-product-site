#!/usr/bin/env python3
"""Recolor public raster thumbs from Soft Clinic / Campaign Ink to Slate & Garnet."""
from __future__ import annotations

import os
import shutil
import subprocess
import sys
from pathlib import Path

import numpy as np
from PIL import Image

ROOT = Path(__file__).resolve().parents[1]
IMAGES = ROOT / "images"

GARNET = np.array([155, 42, 53], dtype=np.uint8)
GARNET_DARK = np.array([127, 31, 41], dtype=np.uint8)
SLATE = np.array([31, 45, 61], dtype=np.uint8)
STONE = np.array([244, 244, 242], dtype=np.uint8)

ANCHORS = [
    ([242, 247, 244], STONE, 35),
    ([58, 125, 106], SLATE, 50),
    ([15, 107, 92], SLATE, 50),
    ([7, 9, 13], SLATE, 28),
    ([199, 147, 52], GARNET, 58),
    ([201, 146, 15], GARNET, 58),
    ([199, 146, 48], GARNET, 58),
    ([200, 146, 48], GARNET, 58),
]

BANNED_EXACT = [
    (0xf2, 0xf7, 0xf4),
    (0x3a, 0x7d, 0x6a),
    (0xc7, 0x93, 0x34),
    (0xc9, 0x92, 0x0f),
    (0x07, 0x09, 0x0d),
    (0x0f, 0x6b, 0x5c),
]

SKIP = {
    IMAGES / "sis-how-it-works-steps.png",
}

# Brand rasters regenerated from SVG (already Slate & Garnet), then passed
# through the fixed remap. OG share card is not in this set.
BRAND_THUMBS = {
    IMAGES / "brand" / "sis-favicon-16.png",
    IMAGES / "brand" / "sis-favicon-32.png",
    IMAGES / "brand" / "sis-lockup-horizontal-1000.png",
    ROOT / "apple-touch-icon.png",
}


def _anchor_remap(rgb: np.ndarray) -> np.ndarray:
    """Recolor near-anchor pixels.

    Squared channel deltas use int32 and are clipped back to 0–255.
    int16 wraps (255**2 does not fit), which false-hits distant pixels
    and flattens garnet marks to slate.
    """
    flat = np.ascontiguousarray(rgb).reshape(-1, 3).astype(np.int32)
    for src, dst, tol in ANCHORS:
        src_a = np.asarray(src, dtype=np.int32)
        delta = flat - src_a
        dist2 = np.sum(delta * delta, axis=1)
        hit = dist2 <= int(tol) * int(tol)
        if np.any(hit):
            flat[hit] = np.asarray(dst, dtype=np.int32)
    return np.clip(flat, 0, 255).astype(np.uint8).reshape(rgb.shape)


def _hsv_remap(rgb: np.ndarray) -> np.ndarray:
    out = rgb.astype(np.float32) / 255.0
    r, g, b = out[..., 0], out[..., 1], out[..., 2]
    maxc = np.maximum(np.maximum(r, g), b)
    minc = np.minimum(np.minimum(r, g), b)
    v = maxc
    delt = maxc - minc
    s = np.where(maxc > 0, delt / maxc, 0.0)

    h = np.zeros_like(v)
    mask = delt > 1e-6
    rm, gm, bm = mask & (maxc == r), mask & (maxc == g), mask & (maxc == b)
    h[rm] = ((g[rm] - b[rm]) / delt[rm]) % 6
    h[gm] = (b[gm] - r[gm]) / delt[gm] + 2
    h[bm] = (r[bm] - g[bm]) / delt[bm] + 4
    h = h / 6.0
    hd = h * 360.0

    px = rgb.copy()
    dark = (v < 0.08) & (s < 0.5)
    px[dark] = SLATE

    ochre = (hd > 15) & (hd < 70) & (s > 0.35) & (v > 0.2)
    px[ochre & (v < 0.45)] = GARNET_DARK
    px[ochre & (v >= 0.45)] = GARNET

    sage_hi = (hd > 80) & (hd < 165) & (s > 0.12) & (v > 0.75)
    px[sage_hi] = STONE

    sage_mid = (hd > 80) & (hd < 170) & (s > 0.25) & (v > 0.25) & (v < 0.75)
    px[sage_mid] = SLATE

    return px


def remint_image(path: Path) -> None:
    img = Image.open(path)
    has_alpha = img.mode in ("RGBA", "LA") or (img.mode == "P" and "transparency" in img.info)
    if has_alpha:
        img = img.convert("RGBA")
        rgb = np.array(img)[..., :3]
        alpha = np.array(img)[..., 3]
        rgb = _hsv_remap(_anchor_remap(rgb))
        out = np.dstack([rgb, alpha])
        img = Image.fromarray(out, "RGBA")
    else:
        rgb = np.array(img.convert("RGB"))
        rgb = _hsv_remap(_anchor_remap(rgb))
        img = Image.fromarray(rgb, "RGB")

    if path.suffix.lower() in {".jpg", ".jpeg"}:
        img = img.convert("RGB")
        img.save(path, quality=90, optimize=True)
    elif path.suffix.lower() == ".webp":
        img.save(path, quality=90, method=6)
    else:
        img.save(path, optimize=True)


def count_banned(path: Path) -> int:
    im = np.array(Image.open(path).convert("RGB"))
    total = 0
    for rgb in BANNED_EXACT:
        r, g, b = rgb
        total += int(((im[:, :, 0] == r) & (im[:, :, 1] == g) & (im[:, :, 2] == b)).sum())
    return total


def iter_rasters() -> list[Path]:
    paths: list[Path] = []
    for dirpath, _, files in os.walk(IMAGES):
        for name in files:
            if name.lower().endswith((".png", ".jpg", ".jpeg", ".webp")):
                paths.append(Path(dirpath) / name)
    paths.append(ROOT / "apple-touch-icon.png")
    return sorted(set(paths))


def _raster_svg(svg: Path, width: int, height: int, out: Path, background: tuple[int, int, int] | None) -> None:
    rsvg = shutil.which("rsvg-convert")
    if rsvg is None:
        raise RuntimeError("rsvg-convert is not available")
    out.parent.mkdir(parents=True, exist_ok=True)
    subprocess.check_call(
        [rsvg, "-w", str(width), "-h", str(height), str(svg), "-o", str(out)],
    )
    if background is None:
        return
    img = Image.open(out).convert("RGBA")
    canvas = Image.new("RGB", img.size, background)
    canvas.paste(img, mask=img.getchannel("A"))
    canvas.save(out, optimize=True)


def render_apple_touch_icon() -> None:
    out = ROOT / "apple-touch-icon.png"
    svg = IMAGES / "brand" / "sis-favicon.svg"
    stone = tuple(int(x) for x in STONE)
    try:
        _raster_svg(svg, 180, 180, out, stone)
    except (RuntimeError, subprocess.CalledProcessError, OSError) as exc:
        print("apple-touch svg raster skipped:", exc, file=sys.stderr)
        _draw_mark(180).save(out, optimize=True)


def _draw_mark(size: int) -> Image.Image:
    canvas = Image.new("RGB", (size, size), tuple(int(x) for x in STONE))
    px = canvas.load()
    scale = size / 64.0

    def fill_rect(x, y, w, h, color):
        x2, y2 = int(x * scale), int(y * scale)
        w2, h2 = int(w * scale), int(h * scale)
        for yy in range(y2, min(size, y2 + h2)):
            for xx in range(x2, min(size, x2 + w2)):
                px[xx, yy] = color

    fill_rect(24, 2, 36, 44, tuple(SLATE.tolist()))
    fill_rect(4, 14, 40, 48, tuple(GARNET.tolist()))
    fill_rect(13, 30, 22, 6, (255, 255, 255))
    fill_rect(13, 43, 14, 6, (255, 255, 255))
    return canvas


def render_favicon_pngs() -> None:
    svg = IMAGES / "brand" / "sis-favicon.svg"
    for dim, name in ((16, "sis-favicon-16.png"), (32, "sis-favicon-32.png")):
        dest = IMAGES / "brand" / name
        try:
            _raster_svg(svg, dim, dim, dest, None)
        except (RuntimeError, subprocess.CalledProcessError, OSError) as exc:
            print(f"favicon svg raster skipped ({name}):", exc, file=sys.stderr)
            _draw_mark(dim).save(dest, optimize=True)


def render_lockup_1000() -> None:
    dest = IMAGES / "brand" / "sis-lockup-horizontal-1000.png"
    svg = IMAGES / "brand" / "sis-lockup-horizontal.svg"
    _raster_svg(svg, 1000, 132, dest, None)


def regenerate_brand_thumbs() -> int:
    """Rebuild favicon, apple-touch, and lockup-1000, then remap with fixed math."""
    render_apple_touch_icon()
    render_favicon_pngs()
    render_lockup_1000()
    for path in sorted(BRAND_THUMBS):
        if not path.exists():
            print("missing brand thumb", path, file=sys.stderr)
            return 1
        before = count_banned(path)
        remint_image(path)
        after = count_banned(path)
        print(f"brand {path.relative_to(ROOT)} banned {before} -> {after}")
        if after:
            return 1
    return 0


def main() -> int:
    brand_resolved = {p.resolve() for p in BRAND_THUMBS}
    skip_resolved = {p.resolve() for p in SKIP}
    for path in iter_rasters():
        if not path.exists():
            continue
        resolved = path.resolve()
        if resolved in skip_resolved or resolved in brand_resolved:
            print("skip (rendered after remap)", path.relative_to(ROOT))
            continue
        before = count_banned(path)
        remint_image(path)
        after = count_banned(path)
        print(f"remint {path.relative_to(ROOT)} banned {before} -> {after}")
        if after:
            return 1
    return regenerate_brand_thumbs()


if __name__ == "__main__":
    raise SystemExit(main())

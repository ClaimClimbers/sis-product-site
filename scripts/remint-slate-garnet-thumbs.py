#!/usr/bin/env python3
"""Recolor public raster thumbs from Soft Clinic / Campaign Ink to Slate & Garnet."""
from __future__ import annotations

import colorsys
import os
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


def _anchor_remap(rgb: np.ndarray) -> np.ndarray:
    out = rgb.copy()
    flat = out.reshape(-1, 3).astype(np.int16)
    for src, dst, tol in ANCHORS:
        src_a = np.array(src, dtype=np.int16)
        d = np.sum((flat - src_a) ** 2, axis=1)
        hit = d <= tol * tol
        if hit.any():
            flat[hit] = dst
    out[:] = flat.reshape(rgb.shape).astype(np.uint8)
    return out


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


def render_apple_touch_icon() -> None:
    out = ROOT / "apple-touch-icon.png"
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
    for dim, name in ((16, "sis-favicon-16.png"), (32, "sis-favicon-32.png")):
        _draw_mark(dim).save(ROOT / "images" / "brand" / name, optimize=True)


def main() -> int:
    render_apple_touch_icon()
    try:
        render_favicon_pngs()
    except Exception as exc:  # noqa: BLE001
        print("favicon png render skipped:", exc, file=sys.stderr)

    for path in iter_rasters():
        if not path.exists():
            continue
        if path.resolve() in {p.resolve() for p in SKIP}:
            print("skip (already reminted)", path.relative_to(ROOT))
            continue
        before = count_banned(path)
        remint_image(path)
        after = count_banned(path)
        print(f"remint {path.relative_to(ROOT)} banned {before} -> {after}")
        if after:
            return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

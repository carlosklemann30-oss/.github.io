#!/usr/bin/env python3
"""Generate responsive and placeholder images.

This script takes one or more source images and creates resized
variants for common responsive breakpoints as well as a very small
blurred placeholder. The goal is to prepare images for the `<picture>`
setup used in the site.

Examples:
    python optimize_images.py images/hero-bg.jpg images/projeto1.jpg
    python optimize_images.py images/

If a directory is provided, all `.jpg` and `.png` images inside are
processed.
"""
import argparse
import pathlib
from PIL import Image, ImageFilter

BREAKPOINTS = {
    "sm": 576,
    "md": 768,
    "lg": 992,
    "xl": 1200,
    "xxl": 1400,
}

def generate_variants(img_path: pathlib.Path) -> None:
    img = Image.open(img_path)
    stem, ext = img_path.stem, img_path.suffix

    for label, width in BREAKPOINTS.items():
        resized = img.copy()
        resized.thumbnail((width, width * img.height / img.width))
        resized.save(img_path.with_name(f"{stem}-{label}{ext}"), quality=85)

    blur = img.copy()
    blur.thumbnail((20, 20))
    blur = blur.filter(ImageFilter.GaussianBlur(10))
    blur.save(img_path.with_name(f"{stem}-blur{ext}"), quality=20)


def collect_images(paths):
    for p in paths:
        path = pathlib.Path(p)
        if path.is_dir():
            yield from path.glob("*.jpg")
            yield from path.glob("*.png")
        elif path.suffix.lower() in {".jpg", ".jpeg", ".png"}:
            yield path


def main():
    parser = argparse.ArgumentParser(description="Create responsive image variants")
    parser.add_argument("paths", nargs="+", help="Image files or directories to process")
    args = parser.parse_args()

    for img_path in collect_images(args.paths):
        generate_variants(img_path)
        print(f"Processed {img_path}")


if __name__ == "__main__":
    main()

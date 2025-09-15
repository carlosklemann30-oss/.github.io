#!/usr/bin/env python3
"""Generate responsive and placeholder images.

This script takes one or more source images and creates resized
variants for common responsive breakpoints as well as a very small
blurred placeholder. The goal is to prepare images for the `<picture>`
setup used in the site.

Examples:
    python optimize_images.py original_images/hero-bg.jpg original_images/projeto1.jpg
    python optimize_images.py original_images/
    python optimize_images.py --output images original_images/

If a directory is provided, all `.jpg` and `.png` images inside are
processed. Output images are saved to images/ by default.
"""
import argparse
import pathlib
import shutil
from PIL import Image, ImageFilter

BREAKPOINTS = {
    "sm": 576,
    "md": 768,
    "lg": 992,
    "xl": 1200,
    "xxl": 1400,
}

def generate_variants(img_path: pathlib.Path, output_dir: pathlib.Path) -> None:
    img = Image.open(img_path)
    stem, ext = img_path.stem, img_path.suffix

    # Ensure output directory exists
    output_dir.mkdir(parents=True, exist_ok=True)

    for label, width in BREAKPOINTS.items():
        resized = img.copy()
        resized.thumbnail((width, width * img.height / img.width))
        output_path = output_dir / f"{stem}-{label}{ext}"
        resized.save(output_path, quality=85)

    # Create ultra-light blur placeholder that preserves original content
    blur = img.copy()
    # First resize to a reasonable size that maintains aspect ratio and content
    blur.thumbnail((100, 100))  # Larger size to preserve content details
    # Apply moderate blur to create placeholder effect while keeping content recognizable
    blur = blur.filter(ImageFilter.GaussianBlur(2))
    blur_output_path = output_dir / f"{stem}-blur{ext}"
    # Use very low quality and optimize for smallest file size
    blur.save(blur_output_path, quality=10, optimize=True)


def collect_images(paths):
    for p in paths:
        path = pathlib.Path(p)
        if path.is_dir():
            yield from path.glob("*.jpg")
            yield from path.glob("*.png")
        elif path.suffix.lower() in {".jpg", ".jpeg", ".png"}:
            yield path


def clean_output_directory(output_dir: pathlib.Path) -> None:
    """Remove all files from the output directory."""
    if output_dir.exists():
        shutil.rmtree(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)


def main():
    parser = argparse.ArgumentParser(description="Create responsive image variants")
    parser.add_argument("paths", nargs="*", default=["original_images/"],
                       help="Image files or directories to process (default: original_images/)")
    parser.add_argument("--output", "-o", default="images",
                       help="Output directory for processed images (default: images)")
    args = parser.parse_args()

    output_dir = pathlib.Path(args.output)

    # Clean output directory before processing
    print(f"Cleaning output directory: {output_dir}")
    clean_output_directory(output_dir)

    for img_path in collect_images(args.paths):
        generate_variants(img_path, output_dir)
        print(f"Processed {img_path} -> {output_dir}")


if __name__ == "__main__":
    main()

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
import base64
import io
import pathlib
import re
import shutil
from PIL import Image, ImageFilter

BREAKPOINTS = {
    "sm": 576,
    "md": 768,
    "lg": 992,
    "xl": 1200,
    "xxl": 1400,
}

# No longer needed since we always use WebP for base64 blur placeholders

def generate_variants(img_path: pathlib.Path, output_dir: pathlib.Path) -> str:
    img = Image.open(img_path)
    stem, ext = img_path.stem, img_path.suffix

    # Ensure output directory exists
    output_dir.mkdir(parents=True, exist_ok=True)

    for label, width in BREAKPOINTS.items():
        resized = img.copy()
        resized.thumbnail((width, width * img.height / img.width))

        # Save original format
        output_path = output_dir / f"{stem}-{label}{ext}"
        resized.save(output_path, quality=80, optimize=True)

        # Save WebP format for better compression
        webp_output_path = output_dir / f"{stem}-{label}.webp"
        resized.save(webp_output_path, format='WEBP', quality=90, optimize=True)

        # Save AVIF format for even better compression
        avif_output_path = output_dir / f"{stem}-{label}.avif"
        resized.save(avif_output_path, format='AVIF', quality=50, optimize=True)

    # Create ultra-light blur placeholder that preserves original content
    blur = img.copy()
    # First resize to a reasonable size that maintains aspect ratio and content
    blur.thumbnail((150, 150))  # Larger size to preserve content details
    # Apply moderate blur to create placeholder effect while keeping content recognizable
    blur = blur.filter(ImageFilter.GaussianBlur(2))

    # Note: Blur placeholder files are no longer saved as separate files
    # since they are embedded as base64 data URLs in the HTML

    # Generate base64 data URL for the blur placeholder
    # Always use WebP format for better compression in base64
    buffer = io.BytesIO()
    blur.save(buffer, format='WEBP', quality=15, optimize=True)
    buffer.seek(0)
    base64_data = base64.b64encode(buffer.getvalue()).decode('utf-8')
    base64_url = f"data:image/webp;base64,{base64_data}"

    return base64_url


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


def update_html_with_base64(html_file: pathlib.Path, base64_mapping: dict) -> None:
    """Update HTML file with base64 data URLs for blur placeholders."""
    if not html_file.exists():
        print(f"HTML file not found: {html_file}")
        return

    content = html_file.read_text(encoding='utf-8')

    for image_stem, base64_url in base64_mapping.items():
        # Pattern to match img src attributes that reference this specific image
        # This works for both file paths and existing base64 data URLs

        # First, try to match file paths like "images/hero-bg-blur.webp"
        file_pattern = rf'src="[^"]*{re.escape(image_stem)}-blur\.[^"]*"'

        # Second, try to match within the context of the specific image's picture element
        # Look for the pattern: srcset with the image name, followed by img tag
        picture_context_pattern = rf'(<picture[^>]*>.*?srcset="[^"]*{re.escape(image_stem)}-[^"]*".*?<img[^>]*src=")[^"]*(".*?</picture>)'

        # Try file path replacement first
        if re.search(file_pattern, content):
            content = re.sub(file_pattern, f'src="{base64_url}"', content)
            print(f"Updated {image_stem} blur image file path with base64 data URL")
        # Try picture context replacement for existing base64
        elif re.search(picture_context_pattern, content, re.DOTALL):
            content = re.sub(picture_context_pattern, rf'\1{base64_url}\2', content, flags=re.DOTALL)
            print(f"Updated {image_stem} base64 data URL within picture context")
        else:
            print(f"Info: {image_stem} not found in HTML (may not be used on this page)")

    html_file.write_text(content, encoding='utf-8')
    print(f"Updated HTML file: {html_file}")


def main():
    parser = argparse.ArgumentParser(description="Create responsive image variants")
    parser.add_argument("paths", nargs="*", default=["original_images/"],
                       help="Image files or directories to process (default: original_images/)")
    parser.add_argument("--output", "-o", default="images",
                       help="Output directory for processed images (default: images)")
    parser.add_argument("--html", default="index.html",
                       help="HTML file to update with base64 data URLs (default: index.html)")
    args = parser.parse_args()

    output_dir = pathlib.Path(args.output)
    html_file = pathlib.Path(args.html)

    # Clean output directory before processing
    print(f"Cleaning output directory: {output_dir}")
    clean_output_directory(output_dir)

    # Collect base64 data URLs for blur placeholders
    base64_mapping = {}

    for img_path in collect_images(args.paths):
        base64_url = generate_variants(img_path, output_dir)
        base64_mapping[img_path.stem] = base64_url
        print(f"Processed {img_path} -> {output_dir}")

    # Update HTML file with base64 data URLs
    if base64_mapping:
        print("\nUpdating HTML file with base64 blur placeholders...")
        update_html_with_base64(html_file, base64_mapping)


if __name__ == "__main__":
    main()

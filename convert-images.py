"""
Convert JPG/PNG images to WebP for web optimization.
Usage: python3 convert-images.py [folder]
Default folder: images/
"""

import os
import sys
from PIL import Image

QUALITY = 82
SUPPORTED = {".jpg", ".jpeg", ".png"}
FOLDER = sys.argv[1] if len(sys.argv) > 1 else "images"


def convert(src_path):
    dst_path = os.path.splitext(src_path)[0] + ".webp"
    if os.path.exists(dst_path):
        print(f"  skip  {os.path.basename(src_path)} (webp already exists)")
        return
    with Image.open(src_path) as img:
        img.save(dst_path, "WEBP", quality=QUALITY, method=6)
    src_kb = os.path.getsize(src_path) // 1024
    dst_kb = os.path.getsize(dst_path) // 1024
    saving = (1 - dst_kb / src_kb) * 100 if src_kb else 0
    print(f"  done  {os.path.basename(src_path)} → {os.path.basename(dst_path)}  {src_kb}KB → {dst_kb}KB  ({saving:.1f}% smaller)")


if not os.path.isdir(FOLDER):
    print(f"Folder not found: {FOLDER}")
    sys.exit(1)

print(f"Converting images in '{FOLDER}/' (quality={QUALITY})\n")
count = 0
for fname in sorted(os.listdir(FOLDER)):
    if os.path.splitext(fname)[1].lower() in SUPPORTED:
        convert(os.path.join(FOLDER, fname))
        count += 1

if count == 0:
    print("No JPG/PNG files found.")
else:
    print(f"\nDone. {count} file(s) processed.")

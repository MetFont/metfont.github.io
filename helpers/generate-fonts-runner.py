#!/usr/bin/env python3
"""
Generate MetFont using nanoemoji.

Usage:
    python3 helpers/generate-fonts-runner.py <build_dir> <version>

This script runs inside the repo directory (no Docker required for local dev).
"""
import glob
import os
import shutil
import subprocess
import sys
from concurrent.futures import ProcessPoolExecutor, as_completed

BUILD_DIR = sys.argv[1] if len(sys.argv) > 1 else "build"
VERSION = sys.argv[2] if len(sys.argv) > 2 else "dev"

METHODS = ["glyf", "glyf_colr_1", "cff_colr_1", "cff2_colr_1", "picosvg", "picosvgz"]

os.makedirs(BUILD_DIR, exist_ok=True)
script_dir = os.path.dirname(os.path.abspath(__file__))
repo_dir = os.path.dirname(script_dir)
color_dir = os.path.join(repo_dir, "color", "svg")
fonts_dir = os.path.join(BUILD_DIR, "fonts")

# Collect all SVG files
svg_files = sorted(glob.glob(os.path.join(color_dir, "*.svg")))
if not svg_files:
    print(f"ERROR: No SVG files found in {color_dir}")
    sys.exit(1)

print(f"Found {len(svg_files)} SVG files in {color_dir}")

# Build formats in parallel (2 at a time to avoid resource exhaustion)
# Running all 6 in parallel causes "glyph names need to be stable" errors
# due to nanoemoji's glyph reuse cache being overwhelmed.
MAX_PARALLEL = 2

def build_one_method(args):
    """Build a single font format in its own subprocess."""
    method, build_dir, svg_files = args
    method_build_dir = os.path.join(build_dir, method)
    os.makedirs(method_build_dir, exist_ok=True)
    ext = ".otf" if method in ("cff_colr_1", "cff2_colr_1", "picosvg", "picosvgz") else ".ttf"
    output_file = os.path.join(method_build_dir, f"MetFont-{method}{ext}")
    cmd = [
        "nanoemoji",
        "--build_dir", method_build_dir,
        "--color_format", method,
        "--family", "MetFont",
        "--ascender", "1045",
        "--descender", "-275",
        "--width", "1024",
        "--output_file", output_file,
        "--ignore_reuse_error",
    ] + svg_files
    result = subprocess.run(cmd, capture_output=True, text=True)
    return (method, result.returncode == 0, result.stdout, result.stderr)

results = {}
with ProcessPoolExecutor(max_workers=MAX_PARALLEL) as executor:
    args_list = [(m, BUILD_DIR, svg_files) for m in METHODS]
    futures = {executor.submit(build_one_method, args): args[0] for args in args_list}
    for future in as_completed(futures):
        method, ok, stdout, stderr = future.result()
        results[method] = (ok, stdout, stderr)
        status = "OK" if ok else "FAILED"
        print(f"  {method}: {status}")
        if not ok:
            print(f"    ERROR: {stderr[:500]}")

# Post-process sequentially (TTX injection + woff2 compression)
for method in METHODS:
    ok, stdout, stderr = results.get(method, (False, None, None))
    if not ok:
        print(f"\n=== Skipping {method} (build failed) ===")
        continue
    print(f"\n=== Post-processing {method} ===")
    ext = ".otf" if method in ("cff_colr_1", "cff2_colr_1", "picosvg", "picosvgz") else ".ttf"
    method_build_dir = os.path.join(BUILD_DIR, method)
    font_in = os.path.join(method_build_dir, f"MetFont-{method}{ext}")
    method_dir = os.path.join(fonts_dir, f"MetFont-{method}")
    os.makedirs(method_dir, exist_ok=True)
    font_out = os.path.join(method_dir, f"MetFont-{method}{ext}")
    ttx_path = os.path.join(repo_dir, "data", "MetFont.ttx")
    if os.path.exists(ttx_path):
        result = subprocess.run(
            ["ttx", "-m", font_in, "-o", font_out, ttx_path],
            capture_output=True, text=True,
        )
        if result.returncode != 0:
            print(f"  WARNING: TTX injection failed: {result.stderr}")
            shutil.copy2(font_in, font_out)
        else:
            print(f"  TTX injection OK")
    else:
        shutil.copy2(font_in, font_out)
    try:
        result = subprocess.run(
            ["woff2_compress", font_out],
            capture_output=True, text=True,
        )
        if result.returncode == 0:
            print(f"  WOFF2 compression OK")
        else:
            print(f"  WARNING: woff2_compress failed: {result.stderr}")
    except FileNotFoundError:
        print(f"  WARNING: woff2_compress not found, skipping WOFF2")
    print(f"  Output: {method_dir}/")

# Copy fonts to font/ directory
font_dest = os.path.join(repo_dir, "font")
if os.path.exists(fonts_dir):
    os.makedirs(font_dest, exist_ok=True)
    for item in os.listdir(fonts_dir):
        src = os.path.join(fonts_dir, item)
        dst = os.path.join(font_dest, item)
        if os.path.isdir(src):
            if os.path.exists(dst):
                shutil.rmtree(dst)
            shutil.copytree(src, dst)
        else:
            shutil.copy2(src, dst)
    print(f"\nFonts copied to {font_dest}/")

print("\nDone!")

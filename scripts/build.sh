#!/bin/bash
# =============================================================================
# Build script for galaga.edouard.nz
# =============================================================================
# Builds a single-page marimo WASM runtime that dynamically loads notebooks
# from ./notebooks/ via URL parameter.
#
# Architecture:
#   - One copy of the marimo WASM runtime (assets/)
#   - One index.html that reads ?nb=<name> and fetches notebooks/<name>.py
#   - Raw .py notebook files served statically
#
# Usage:
#   ./scripts/build.sh
# =============================================================================
set -e

DIST_DIR="dist"
NOTEBOOKS_DIR="notebooks"
TEMPLATE_NB="notebooks/hello.py"  # Any notebook works as template source

# Clean previous build
rm -rf "$DIST_DIR"
mkdir -p "$DIST_DIR"

# Check for notebooks
if [ ! -d "$NOTEBOOKS_DIR" ] || [ -z "$(ls -A "$NOTEBOOKS_DIR"/*.py 2>/dev/null)" ]; then
  echo "No notebooks found in $NOTEBOOKS_DIR/"
  exit 1
fi

# Step 1: Export one notebook to get the runtime assets
echo "Exporting runtime assets..."
uv run marimo export html-wasm "$TEMPLATE_NB" -o "$DIST_DIR/_tmp" --mode edit --no-sandbox

# Step 2: Move assets to top level, discard the template HTML
mv "$DIST_DIR/_tmp/assets" "$DIST_DIR/assets"
# Copy favicon etc
cp "$DIST_DIR/_tmp/favicon.ico" "$DIST_DIR/" 2>/dev/null || true
cp "$DIST_DIR/_tmp/favicon-32x32.png" "$DIST_DIR/" 2>/dev/null || true
cp "$DIST_DIR/_tmp/favicon-16x16.png" "$DIST_DIR/" 2>/dev/null || true
cp "$DIST_DIR/_tmp/apple-touch-icon.png" "$DIST_DIR/" 2>/dev/null || true
cp "$DIST_DIR/_tmp/logo.png" "$DIST_DIR/" 2>/dev/null || true
cp "$DIST_DIR/_tmp/manifest.json" "$DIST_DIR/" 2>/dev/null || true
cp "$DIST_DIR/_tmp/site.webmanifest" "$DIST_DIR/" 2>/dev/null || true
rm -rf "$DIST_DIR/_tmp"

# Copy font files to root as well (runtime requests them without assets/ prefix)
cp "$DIST_DIR"/assets/*.woff2 "$DIST_DIR/" 2>/dev/null || true
cp "$DIST_DIR"/assets/*.woff "$DIST_DIR/" 2>/dev/null || true
cp "$DIST_DIR"/assets/*.ttf "$DIST_DIR/" 2>/dev/null || true
rm -rf "$DIST_DIR/_tmp"

# Step 3: Copy notebook .py files
echo "Copying notebooks..."
mkdir -p "$DIST_DIR/notebooks"
cp "$NOTEBOOKS_DIR"/*.py "$DIST_DIR/notebooks/"

# Step 4: Generate the dynamic index.html
echo "Generating dynamic loader..."
python3 scripts/generate_index.py "$DIST_DIR"

echo "Build complete: $DIST_DIR/"
echo ""
echo "Notebooks available:"
for nb in "$NOTEBOOKS_DIR"/*.py; do
  name=$(basename "$nb" .py)
  echo "  http://localhost:9191/?nb=$name"
done

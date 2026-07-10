#!/bin/bash
# =============================================================================
# Build script for galaga.edouard.nz
# =============================================================================
# Architecture (matching marimo.app):
#   /e/          — standard marimo WASM export (static, code blanked)
#   /notebooks/  — raw .py notebook files
#   /index.html  — landing page + iframe loader
#
# Usage:
#   ./scripts/build.sh
# =============================================================================
set -e

DIST_DIR="dist"
NOTEBOOKS_DIR="notebooks"
TEMPLATE_NB="notebooks/hello.py"  # Any notebook to generate the runtime

# Clean previous build
rm -rf "$DIST_DIR"
mkdir -p "$DIST_DIR"

# Check for notebooks
if [ ! -d "$NOTEBOOKS_DIR" ] || [ -z "$(ls -A "$NOTEBOOKS_DIR"/*.py 2>/dev/null)" ]; then
  echo "No notebooks found in $NOTEBOOKS_DIR/"
  exit 1
fi

# Step 1: Export one notebook to /e/ (the WASM runtime)
echo "Exporting marimo runtime to /e/..."
uv run marimo export html-wasm "$TEMPLATE_NB" -o "$DIST_DIR/e" --mode edit --no-sandbox

# Step 2: Copy notebook .py files
echo "Copying notebooks..."
mkdir -p "$DIST_DIR/notebooks"
cp "$NOTEBOOKS_DIR"/*.py "$DIST_DIR/notebooks/"

# Step 3: Generate index.html and patch /e/index.html
echo "Generating site..."
uv run python scripts/generate_index.py "$DIST_DIR"

echo ""
echo "Build complete: $DIST_DIR/"
echo ""
echo "Notebooks available:"
for nb in "$NOTEBOOKS_DIR"/*.py; do
  name=$(basename "$nb" .py)
  echo "  http://localhost:9191/?nb=$name"
done

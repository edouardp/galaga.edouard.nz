#!/bin/bash
# =============================================================================
# Build script for galaga.edouard.nz
# =============================================================================
# Produces dist/ with:
#   /e/          — marimo WASM runtime (exported from a template notebook)
#   /notebooks/  — raw .py notebook files (loaded by Lambda@Edge at request time)
#   /index.html  — landing page listing available notebooks
#
# In production, Lambda@Edge intercepts /?nb=<name> requests, fetches the
# notebook from S3, injects it into the /e/ runtime template, and returns
# the assembled HTML. The static index.html is only served when no ?nb= param
# is present.
#
# Usage:
#   ./scripts/build.sh
# =============================================================================
set -e

DIST_DIR="dist"
NOTEBOOKS_DIR="notebooks"
TEMPLATE_NB="notebooks/hello.py"  # Any notebook — used to generate the WASM runtime

# Clean previous build
rm -rf "$DIST_DIR"
mkdir -p "$DIST_DIR"

# Check for notebooks
if [ ! -d "$NOTEBOOKS_DIR" ] || [ -z "$(ls -A "$NOTEBOOKS_DIR"/*.py 2>/dev/null)" ]; then
  echo "No notebooks found in $NOTEBOOKS_DIR/"
  exit 1
fi

# Step 1: Export one notebook to get the WASM runtime at /e/
echo "Exporting marimo runtime to /e/..."
uv run marimo export html-wasm "$TEMPLATE_NB" -o "$DIST_DIR/e" --mode edit --no-sandbox

# Step 2: Copy raw notebook .py files (Lambda@Edge reads these from S3)
echo "Copying notebooks..."
mkdir -p "$DIST_DIR/notebooks"
cp "$NOTEBOOKS_DIR"/*.py "$DIST_DIR/notebooks/"

# Step 3: Generate landing page and patch /e/index.html (blank embedded code)
echo "Generating site..."
uv run python scripts/generate_index.py "$DIST_DIR"

echo ""
echo "Build complete: $DIST_DIR/"
echo ""
echo "Notebooks available:"
for nb in "$NOTEBOOKS_DIR"/*.py; do
  name=$(basename "$nb" .py)
  echo "  https://galaga.edouard.nz/?nb=$name"
done

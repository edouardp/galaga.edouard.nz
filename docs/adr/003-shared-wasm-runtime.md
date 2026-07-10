# ADR-003: Shared WASM Runtime

## Status

Accepted

## Context

Marimo's `html-wasm` export bundles the entire Pyodide runtime, Python standard library, and marimo frontend into each exported notebook — roughly 50MB of assets per export. With multiple notebooks, this means either:

1. **Per-notebook exports** — duplicate assets across notebooks, wasting S3 storage and invalidating browser caches when the user navigates between notebooks.

2. **Shared runtime** — export once to produce the runtime at `/e/`, then share it across all notebooks by injecting different notebook code into the same template.

## Decision

Export the WASM runtime exactly once (from an arbitrary template notebook) to `/e/`. All notebooks share this single copy of the runtime assets.

The build script uses `hello.py` as the template notebook (any notebook works — the embedded code is blanked out post-export). The `/e/assets/` directory contains hashed filenames that are cache-immutable.

## Consequences

- S3 stores one copy of the ~50MB runtime, not one per notebook
- Browser caches runtime assets once; navigating between notebooks reuses them
- All notebooks run the same marimo/Pyodide version (no version drift)
- Upgrading marimo requires a single re-export and redeploy of `/e/`
- The runtime template must be generic enough for any notebook (it is — marimo's export format supports this)

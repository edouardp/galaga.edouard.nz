# Architecture

## Overview

galaga.edouard.nz serves interactive marimo notebooks that execute entirely client-side via WebAssembly (Pyodide). The infrastructure handles content delivery; all computation happens in the visitor's browser.

## Request Flow

```text
Browser → CloudFront → Lambda@Edge (origin-request) → S3
```

1. User visits `https://galaga.edouard.nz/?nb=paraboloid`
2. CloudFront receives the request, cache key includes the `nb` query param
3. On cache miss, Lambda@Edge intercepts the origin-request:
   - Fetches the WASM runtime template from `s3://galaga.edouard.nz/e/index.html`
   - Fetches the notebook source from `s3://galaga.edouard.nz/notebooks/paraboloid.py`
   - Injects the notebook code into the runtime template
   - Rewrites relative asset paths (`./assets/` → `./e/assets/`)
   - Returns the assembled HTML directly (no S3 fetch for the final response)
4. CloudFront caches the assembled page (keyed on `?nb=` value)
5. Browser loads the page, Pyodide boots, notebook executes client-side

When no `?nb=` parameter is present, the request falls through to S3 and serves the static landing page (`index.html`), which lists available notebooks.

## S3 Bucket Layout

```text
galaga.edouard.nz/
├── e/                  # Marimo WASM runtime (exported once from a template notebook)
│   ├── index.html      # Runtime template (notebookCode blanked out)
│   ├── assets/         # JS/CSS/WASM bundles (hashed filenames, immutable cache)
│   └── ...
├── notebooks/          # Raw .py notebook files
│   ├── hello.py
│   ├── galaga_demo.py
│   └── paraboloid.py
└── index.html          # Landing page (notebook listing)
```

## Infrastructure Components

| Component | Purpose |
| --- | --- |
| S3 Bucket | Origin store for runtime, notebooks, and landing page |
| CloudFront | CDN with COOP/COEP headers (required for SharedArrayBuffer/Pyodide) |
| Lambda@Edge | Assembles notebook HTML at origin-request time |
| ACM Certificate | TLS for galaga.edouard.nz |
| Route 53 | DNS alias to CloudFront |
| Origin Access Control | S3 is private; only CloudFront can read it |

## Cross-Origin Isolation

Pyodide requires `SharedArrayBuffer`, which needs cross-origin isolation headers:

- `Cross-Origin-Opener-Policy: same-origin`
- `Cross-Origin-Embedder-Policy: require-corp`

These are set via a CloudFront Response Headers Policy on all responses, and also explicitly in Lambda@Edge responses.

## Caching Strategy

| Path | Cache TTL | Rationale |
| --- | --- | --- |
| `/e/assets/*` | 1 year, immutable | Hashed filenames — new builds get new URLs |
| `/e/index.html` | 1 year | Rarely changes (only on marimo version bumps) |
| `/notebooks/*` | 60 seconds | Notebook updates should propagate quickly |
| `/index.html` | 60 seconds | Landing page reflects notebook additions |
| `/?nb=<name>` | 60 seconds | Lambda@Edge response cached by CloudFront |

Deploy invalidates `/index.html` and `/notebooks/*` to force immediate propagation.

## Build Process

```text
scripts/build.sh
├── marimo export html-wasm → dist/e/     (WASM runtime from template notebook)
├── cp notebooks/*.py → dist/notebooks/   (raw notebook files)
└── scripts/generate_index.py → dist/     (landing page + patch /e/index.html)
```

The generate_index.py script:
1. Blanks out the embedded notebook code in `/e/index.html` (Lambda@Edge injects the real code)
2. Generates the landing page with links to each notebook

## Local Development

`make serve` builds and serves `dist/` with Python's HTTP server. Locally, the landing page uses an iframe + URL hash approach as a client-side fallback (no Lambda@Edge locally). The iframe loads `/e/index.html#code/<url-encoded-notebook>`, which marimo's WASM runtime picks up.

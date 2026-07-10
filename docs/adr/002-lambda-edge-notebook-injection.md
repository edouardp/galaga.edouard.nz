# ADR-002: Lambda@Edge Notebook Injection

## Status

Accepted

## Context

Each marimo WASM notebook needs to be served as a standalone HTML page with the notebook code embedded. Two approaches were considered:

1. **Static HTML per notebook** — run `marimo export html-wasm` for each notebook at build time, producing separate HTML files. Simple, but slow builds (each export takes 10-20s and duplicates ~50MB of WASM runtime assets).

2. **Lambda@Edge injection** — export the runtime once (with blank notebook code), then inject the actual notebook at request time using Lambda@Edge on the CloudFront origin-request event.

## Decision

Use Lambda@Edge to inject notebook code into a shared runtime template at request time.

The Lambda function:
- Intercepts requests with a `?nb=<name>` query parameter
- Fetches the runtime template (`/e/index.html`) and notebook source (`/notebooks/<name>.py`) from S3
- Injects the notebook code into the template
- Rewrites relative asset paths to point to `/e/`
- Returns the assembled HTML with appropriate caching headers

## Consequences

- Build time is constant regardless of notebook count (export once, copy notebooks)
- Adding a notebook is just copying a `.py` file to S3 — no rebuild needed
- Single runtime version across all notebooks (no drift between per-notebook exports)
- Introduces Lambda@Edge complexity and a small cold-start latency on cache misses (~200ms)
- CloudFront caches assembled pages, so most requests don't hit Lambda
- Lambda@Edge must be deployed in us-east-1 (CloudFront constraint)
- Landing page still works without Lambda (served as static index.html from S3)

# ADR-005: S3 + CloudFront Hosting

## Status

Accepted

## Context

The site serves static assets (HTML, JS, WASM bundles) with no server-side computation beyond notebook injection (handled by Lambda@Edge). Hosting options considered:

1. **GitHub Pages / Netlify / Vercel** — simple, but no Lambda@Edge equivalent for dynamic injection. Would require per-notebook static exports (see ADR-002 for why that's undesirable). Also limited control over response headers (COOP/COEP needed for SharedArrayBuffer).

2. **S3 + CloudFront** — full control over headers, caching, Lambda@Edge, and custom domains. Already using AWS for other edouard.nz services.

3. **EC2/ECS/Lambda function URL** — overkill for serving static content. Adds operational complexity and cost for no benefit.

## Decision

Host on S3 (origin) with CloudFront (CDN), using:
- Origin Access Control (OAC) — S3 bucket is private, only CloudFront can read it
- CloudFront Response Headers Policy — sets COOP/COEP on all responses
- ACM certificate — TLS for the custom domain
- Route 53 — DNS alias record pointing to the CloudFront distribution
- Lambda@Edge — notebook injection (origin-request event)

Infrastructure is defined in `infrastructure.yaml` (CloudFormation) and deployed via `scripts/infra.sh`.

## Consequences

- Full control over caching strategy (immutable assets vs short-lived notebook content)
- Cross-origin isolation headers applied globally (required for Pyodide/SharedArrayBuffer)
- Low cost — S3 storage is minimal, CloudFront pricing is per-request with generous free tier
- Infrastructure is code-defined and reproducible
- Requires AWS account and credentials for deployment
- Lambda@Edge must be in us-east-1 (CloudFront global requirement)
- One-time infra setup, then `make deploy` for content updates

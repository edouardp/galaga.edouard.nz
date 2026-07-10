#!/bin/bash
# =============================================================================
# Deploy script for galaga.edouard.nz
# =============================================================================
# Builds marimo WASM notebooks and deploys to S3/CloudFront.
#
# S3 layout:
#   /e/          — WASM runtime (long cache, immutable assets)
#   /notebooks/  — raw .py files (short cache, read by Lambda@Edge)
#   /index.html  — landing page (short cache, served when no ?nb= param)
#
# Usage:
#   ./scripts/deploy.sh              # Build and deploy
#   ./scripts/deploy.sh --skip-build # Deploy without rebuilding
# =============================================================================
set -e

SKIP_BUILD=false
while [[ $# -gt 0 ]]; do
  case $1 in
    --skip-build)
      SKIP_BUILD=true
      shift
      ;;
    *)
      echo "Unknown option: $1"
      exit 1
      ;;
  esac
done

# Build notebooks unless skipped
if [ "$SKIP_BUILD" = false ]; then
  echo "Building notebooks..."
  ./scripts/build.sh
fi

# Get infrastructure outputs
STACK_NAME="galaga-edouard-nz"
REGION="us-east-1"
BUCKET=$(aws cloudformation describe-stacks \
  --stack-name "$STACK_NAME" \
  --region "$REGION" \
  --query 'Stacks[0].Outputs[?OutputKey==`BucketName`].OutputValue' \
  --output text)
DISTRIBUTION_ID=$(aws cloudformation describe-stacks \
  --stack-name "$STACK_NAME" \
  --region "$REGION" \
  --query 'Stacks[0].Outputs[?OutputKey==`DistributionId`].OutputValue' \
  --output text)

echo "Syncing to S3 bucket: $BUCKET"

# Sync /e/ (runtime assets) — long cache, immutable hashed filenames
aws s3 sync dist/e/ "s3://$BUCKET/e/" \
  --cache-control "public, max-age=31536000, immutable" \
  --size-only

# Sync notebooks — short cache so updates propagate quickly
aws s3 sync dist/notebooks/ "s3://$BUCKET/notebooks/" \
  --cache-control "public, max-age=60" \
  --delete

# Sync landing page — short cache
aws s3 cp dist/index.html "s3://$BUCKET/index.html" \
  --cache-control "public, max-age=60"

echo "Invalidating CloudFront cache..."
aws cloudfront create-invalidation \
  --distribution-id "$DISTRIBUTION_ID" \
  --paths "/index.html" "/notebooks/*"

echo "Deployment complete! Site: https://galaga.edouard.nz"

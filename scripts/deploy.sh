#!/bin/bash
# =============================================================================
# Deploy script for galaga.edouard.nz
# =============================================================================
# Builds marimo WASM notebooks and deploys to S3/CloudFront.
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

# Sync assets with long cache (filenames are content-hashed)
aws s3 sync dist/assets/ "s3://$BUCKET/assets/" \
  --cache-control "public, max-age=31536000, immutable" \
  --size-only

# Sync notebooks (short cache so updates propagate quickly)
aws s3 sync dist/notebooks/ "s3://$BUCKET/notebooks/" \
  --cache-control "public, max-age=60" \
  --delete

# Sync root files (index.html, favicons) with short cache
aws s3 sync dist/ "s3://$BUCKET/" \
  --exclude "assets/*" \
  --exclude "notebooks/*" \
  --cache-control "public, max-age=60" \
  --delete

echo "Invalidating CloudFront cache..."
aws cloudfront create-invalidation \
  --distribution-id "$DISTRIBUTION_ID" \
  --paths "/*"

echo "Deployment complete! Site: https://galaga.edouard.nz"

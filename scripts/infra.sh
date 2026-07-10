#!/bin/bash
# =============================================================================
# Infrastructure deployment for galaga.edouard.nz
# =============================================================================
# Deploys the CloudFormation stack (S3 + CloudFront + ACM + DNS).
# Run this once to set up the hosting infrastructure.
#
# Prerequisites:
#   - AWS credentials configured (aws sso login)
#   - The EdouardNzHostedZone stack must already exist
#
# Usage:
#   ./scripts/infra.sh
# =============================================================================
set -e

STACK_NAME="galaga-edouard-nz"
REGION="us-east-1"
TEMPLATE="infrastructure.yaml"

# Get the hosted zone ID from the existing stack
HOSTED_ZONE_ID=$(aws cloudformation describe-stacks \
  --stack-name EdouardNzHostedZone \
  --region ap-southeast-2 \
  --query 'Stacks[0].Outputs[?OutputKey==`HostedZoneId`].OutputValue' \
  --output text)

if [ -z "$HOSTED_ZONE_ID" ] || [ "$HOSTED_ZONE_ID" = "None" ]; then
  echo "ERROR: Could not find HostedZoneId from EdouardNzHostedZone stack"
  exit 1
fi

echo "Deploying infrastructure stack: $STACK_NAME"
echo "  Region: $REGION"
echo "  Hosted Zone ID: $HOSTED_ZONE_ID"

aws cloudformation deploy \
  --template-file "$TEMPLATE" \
  --stack-name "$STACK_NAME" \
  --region "$REGION" \
  --parameter-overrides "HostedZoneId=$HOSTED_ZONE_ID" \
  --capabilities CAPABILITY_IAM \
  --no-fail-on-empty-changeset

echo "Infrastructure deployment complete!"
aws cloudformation describe-stacks \
  --stack-name "$STACK_NAME" \
  --region "$REGION" \
  --query 'Stacks[0].Outputs' \
  --output table

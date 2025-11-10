#!/bin/bash
# Script to create feature branch for issue #252

set -e

echo "=== Creating feature branch for issue #252 ==="
echo ""

# Get current branch
CURRENT_BRANCH=$(git branch --show-current 2>/dev/null || git rev-parse --abbrev-ref HEAD)
echo "Current branch: $CURRENT_BRANCH"
echo ""

# Switch to master/main/development
if git show-ref --verify --quiet refs/heads/master; then
    echo "Switching to master..."
    git checkout master
elif git show-ref --verify --quiet refs/heads/main; then
    echo "Switching to main..."
    git checkout main
elif git show-ref --verify --quiet refs/heads/development; then
    echo "Switching to development..."
    git checkout development
else
    echo "ERROR: No base branch found (master/main/development)"
    exit 1
fi

# Pull latest changes
echo "Pulling latest changes from origin..."
git pull origin $(git branch --show-current) || echo "Warning: Could not pull from origin (continuing anyway)"
echo ""

# Create new feature branch
BRANCH_NAME="feature/252-reset-detection-swd-jtag"
echo "Creating branch: $BRANCH_NAME"
git checkout -b "$BRANCH_NAME"
echo ""

# Verify
echo "=== Branch created successfully ==="
echo "Current branch: $(git branch --show-current)"
echo ""
echo "You can now start implementing the feature request #252"
echo "GitHub Issue: https://github.com/square/pylink/issues/252"


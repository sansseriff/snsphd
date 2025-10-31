#!/usr/bin/env bash
set -euo pipefail

# Bump version in pyproject.toml and __init__.py, commit, tag, and push.
# Usage: ./publish_new.sh [major|minor|patch]
# Default bump: patch

BUMP_TYPE=${1:-patch}

function die() { echo "Error: $*" >&2; exit 1; }

ROOT_DIR=$(cd "$(dirname "$0")" && pwd)
cd "$ROOT_DIR"

PYPROJECT=pyproject.toml
INIT_FILE=src/snsphd/__init__.py

[[ -f $PYPROJECT ]] || die "Cannot find $PYPROJECT"
[[ -f $INIT_FILE ]] || die "Cannot find $INIT_FILE"

# Extract current version from pyproject.toml
CURRENT_VERSION=$(grep -E '^version\s*=\s*"[0-9]+\.[0-9]+\.[0-9]+"' "$PYPROJECT" | head -n1 | sed -E 's/.*"([0-9]+\.[0-9]+\.[0-9]+)".*/\1/')
[[ -n ${CURRENT_VERSION:-} ]] || die "Could not read current version from $PYPROJECT"

IFS='.' read -r MAJOR MINOR PATCH <<<"$CURRENT_VERSION"
case "$BUMP_TYPE" in
  major) NEW_VERSION="$((MAJOR+1)).0.0" ;;
  minor) NEW_VERSION="$MAJOR.$((MINOR+1)).0" ;;
  patch) NEW_VERSION="$MAJOR.$MINOR.$((PATCH+1))" ;;
  *) die "Unknown bump type: $BUMP_TYPE (use major|minor|patch)" ;;
esac

TAG="v$NEW_VERSION"

echo "Current version: $CURRENT_VERSION"
echo "New version:     $NEW_VERSION"
echo "Tag:              $TAG"

# Update pyproject.toml
# macOS/BSD sed requires a backup suffix for -i; use '' for none
sed -i '' -E "s/^version\s*=\s*\"[0-9]+\.[0-9]+\.[0-9]+\"/version = \"$NEW_VERSION\"/" "$PYPROJECT"

# Update __init__.py __version__
sed -i '' -E "s/^__version__\s*=\s*\"[0-9]+\.[0-9]+\.[0-9]+\"/__version__ = \"$NEW_VERSION\"/" "$INIT_FILE"

# Show changes
echo "\nChanged files:"
git --no-pager diff -- $PYPROJECT $INIT_FILE | sed -n '1,200p'

# Commit, tag, and push
git add "$PYPROJECT" "$INIT_FILE"
if git diff --cached --quiet; then
  echo "No changes to commit. Creating tag only..."
else
  git commit -m "chore: release $TAG"
fi

git tag -a "$TAG" -m "Release $TAG"

echo "\nPushing commits and tags..."
git push origin HEAD
git push origin "$TAG"

echo "\nDone. GitHub Actions will build and publish to PyPI for tag $TAG."

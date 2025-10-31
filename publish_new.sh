#!/usr/bin/env bash
set -euo pipefail

# Bump version in pyproject.toml and __init__.py, commit, tag, and push.
# Usage: ./publish_new.sh [major|minor|patch|current|set X.Y.Z]
#   major/minor/patch: bumps the version accordingly (default: patch)
#   current: tags and publishes the current version without changing files
#   set X.Y.Z: sets version to the explicit value, commits, tags, and pushes

BUMP_TYPE=${1:-patch}
EXPLICIT_VERSION=${2:-}

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

NEW_VERSION=""
case "$BUMP_TYPE" in
  major|minor|patch)
    IFS='.' read -r MAJOR MINOR PATCH <<<"$CURRENT_VERSION"
    case "$BUMP_TYPE" in
      major) NEW_VERSION="$((MAJOR+1)).0.0" ;;
      minor) NEW_VERSION="$MAJOR.$((MINOR+1)).0" ;;
      patch) NEW_VERSION="$MAJOR.$MINOR.$((PATCH+1))" ;;
    esac
    ;;
  current)
    NEW_VERSION="$CURRENT_VERSION"
    ;;
  set)
    [[ -n "$EXPLICIT_VERSION" ]] || die "Usage: ./publish_new.sh set X.Y.Z"
    [[ "$EXPLICIT_VERSION" =~ ^[0-9]+\.[0-9]+\.[0-9]+$ ]] || die "Version must be X.Y.Z"
    NEW_VERSION="$EXPLICIT_VERSION"
    ;;
  *) die "Unknown mode: $BUMP_TYPE (use major|minor|patch|current|set X.Y.Z)" ;;
esac

TAG="v$NEW_VERSION"

echo "Current version: $CURRENT_VERSION"
echo "New version:     $NEW_VERSION"
echo "Tag:              $TAG"

# Update files only if version changed; otherwise sync __init__ to pyproject
if [[ "$NEW_VERSION" != "$CURRENT_VERSION" ]]; then
  # Update pyproject.toml (robust cross-platform)
  python3 - "$PYPROJECT" "$NEW_VERSION" <<'PY'
import sys, re
path, ver = sys.argv[1], sys.argv[2]
txt = open(path, 'r', encoding='utf-8').read()
new = re.sub(r'^version\s*=\s*"[0-9]+\.[0-9]+\.[0-9]+"', f'version = "{ver}"', txt, flags=re.M)
if txt == new:
    print(f"WARNING: did not update {path}; pattern not found", file=sys.stderr)
open(path, 'w', encoding='utf-8').write(new)
PY

  # Update __init__.py __version__
  python3 - "$INIT_FILE" "$NEW_VERSION" <<'PY'
import sys, re
path, ver = sys.argv[1], sys.argv[2]
txt = open(path, 'r', encoding='utf-8').read()
new = re.sub(r'^__version__\s*=\s*"[0-9]+\.[0-9]+\.[0-9]+"', f'__version__ = "{ver}"', txt, flags=re.M)
if txt == new:
    print(f"WARNING: did not update {path}; pattern not found", file=sys.stderr)
open(path, 'w', encoding='utf-8').write(new)
PY
else
  # Sync __init__ to current version if needed
  python3 - "$INIT_FILE" "$CURRENT_VERSION" <<'PY'
import sys, re
path, ver = sys.argv[1], sys.argv[2]
txt = open(path, 'r', encoding='utf-8').read()
new = re.sub(r'^__version__\s*=\s*"[0-9]+\.[0-9]+\.[0-9]+"', f'__version__ = "{ver}"', txt, flags=re.M)
open(path, 'w', encoding='utf-8').write(new)
PY
fi

# Show changes
printf "\nChanged files:\n"
git --no-pager diff -- $PYPROJECT $INIT_FILE | sed -n '1,200p'

# Commit, tag, and push
git add "$PYPROJECT" "$INIT_FILE"
if git diff --cached --quiet; then
  echo "No changes to commit. Creating tag only..."
else
  git commit -m "chore: release $TAG"
fi

# Prevent tagging an already existing version
if git rev-parse "$TAG" >/dev/null 2>&1; then
  die "Tag $TAG already exists. Aborting."
fi

git tag -a "$TAG" -m "Release $TAG"

echo "\nPushing commits and tags..."
git push origin HEAD
git push origin "$TAG"

echo "\nDone. GitHub Actions will build and publish to PyPI for tag $TAG."

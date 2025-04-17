#!/bin/bash
# Script to automate releasing a new version of culturekit

set -e  # Exit on error

# Check if version is provided
if [ "$#" -ne 1 ]; then
    echo "Usage: $0 <version>"
    echo "Example: $0 0.1.0"
    exit 1
fi

VERSION=$1

# Validate version format
if ! [[ $VERSION =~ ^[0-9]+\.[0-9]+\.[0-9]+$ ]]; then
    echo "Error: Version must be in format x.y.z"
    exit 1
fi

echo "Preparing release v$VERSION..."

# Update version in pyproject.toml
echo "Updating version in pyproject.toml..."
poetry version $VERSION

# Update version in __init__.py
echo "Updating version in __init__.py..."
sed -i '' "s/__version__ = \".*\"/__version__ = \"$VERSION\"/" src/culturekit/__init__.py

# Build the package
echo "Building package..."
poetry build

# Run tests
echo "Running tests..."
pytest

# Commit changes
echo "Committing changes..."
git add pyproject.toml src/culturekit/__init__.py
git commit -m "Bump version to $VERSION"

# Create tag
echo "Creating git tag v$VERSION..."
git tag -a "v$VERSION" -m "Version $VERSION"

echo "Version v$VERSION prepared!"
echo 
echo "Next steps:"
echo "1. Push changes:        git push"
echo "2. Push tags:           git push --tags"
echo "3. Create GitHub release: https://github.com/decisions-lab/culturekit/releases/new"
echo "   (This will trigger the PyPI publish workflow)"
echo 
echo "Alternatively, publish manually:"
echo "4. Upload to PyPI:      poetry publish" 
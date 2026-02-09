#!/bin/bash

# Exit on error
set -e

# Ensure we are in the project root
cd "$(dirname "$0")/.."

# Function to check if a command exists
command_exists() {
  command -v "$1" >/dev/null 2>&1
}

# Check dependencies
echo "Checking dependencies..."
if ! command_exists pyinstaller; then
  echo "Error: PyInstaller not found. Please install it with 'pip install pyinstaller'."
  exit 1
fi

if ! command_exists gh; then
  echo "Error: GitHub CLI (gh) not found. Please install it."
  exit 1
fi
echo "Dependencies detected."

# Get release details
# Get release details
version="$1"
if [ -z "$version" ]; then
  read -p "Enter release version (e.g., v1.1.0): " version
fi

if [ -z "$version" ]; then
  echo "Version is required."
  exit 1
fi

read -p "Enter release title (default: $version): " title
title=${title:-$version}

read -p "Preparing to release $version - $title. Continue? (y/n): " confirm
if [[ $confirm != "y" ]]; then
  echo "Aborted."
  exit 0
fi

# Build executable
# Build executables
echo "Building executables..."
./scripts/build.sh

# Collect artifacts
ARTIFACTS=()
for f in dist/ctkRouletteOverlay dist/ctkRouletteOverlay.exe; do
    if [ -f "$f" ]; then
        ARTIFACTS+=("$f")
    fi
done

if [ ${#ARTIFACTS[@]} -eq 0 ]; then
    echo "Error: No artifacts found in dist/"
    exit 1
fi

echo "Found artifacts: ${ARTIFACTS[*]}"

# Publish release
# Publish release
echo "Publishing release $version..."
notes_file="RELEASE.md"

if [ ! -f "$notes_file" ]; then
    echo "Warning: Release notes file '$notes_file' not found. Checking for release_notes.md..."
    if [ -f "release_notes.md" ]; then
        notes_file="release_notes.md"
    else
        echo "Warning: No release notes found. Creating empty RELEASE.md."
        touch "RELEASE.md"
    fi
fi

# Check if tag exists locally and delete it to prevent "tag exists" error
if git rev-parse "$version" >/dev/null 2>&1; then
    echo "Deleting existing local tag $version..."
    git tag -d "$version"
fi

gh release create "$version" "${ARTIFACTS[@]}" --title "$title" --notes-file "$notes_file"

echo "Release $version published successfully!"

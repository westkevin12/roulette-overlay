#!/bin/bash

# Exit on error
set -e

# Ensure we are in the project root
cd "$(dirname "$0")/.."

# Clean artifacts
rm -rf build dist RouletteOverlay.spec

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
echo "Dependencies detected."

# Build Windows executable if powershell.exe is available (WSL/Windows)
if command_exists powershell.exe; then
    echo "WSL/Windows environment detected. Building Windows executable..."
    powershell.exe -ExecutionPolicy Bypass -File "scripts/build.ps1"
else
    echo "powershell.exe not found. Skipping Windows build."
fi

# Build Linux executable
echo "Building Linux executable..."
# Clean only if we didn't just build windows, or be careful not to delete dist/RouletteOverlay.exe
# Actually, pyinstaller cleans build/ by default, but we should be careful about dist/
# build.ps1 clears dist/, so if we run it first, we are good.
# If we run linux build next, we should NOT clear dist/ if it contains the .exe

# Determine separator for --add-data (Linux uses :)
ADD_DATA="icons:icons"

pyinstaller --noconfirm --onefile --windowed --icon "icons/icon128X128.ico" --add-data "$ADD_DATA" --hidden-import=tkinter --collect-all=customtkinter ctkRouletteOverlay.py

echo "Build complete."
echo "Artifacts located in dist/:"
ls -l dist/

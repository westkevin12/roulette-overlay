$ErrorActionPreference = "Stop"

# Ensure we are in the project root
Set-Location -Path $PSScriptRoot/..

# Check PyInstaller module
if (-not (python -m PyInstaller --version 2>$null)) {
    Write-Host "Error: PyInstaller module not found. Please install it with 'pip install pyinstaller'." -ForegroundColor Red
    exit 1
}

Write-Host "Dependencies detected." -ForegroundColor Green

# Build executable
Write-Host "Building executable..." -ForegroundColor Cyan

if (Test-Path "build") { Remove-Item "build" -Recurse -Force }
if (Test-Path "RouletteOverlay.spec") { Remove-Item "RouletteOverlay.spec" -Force }

# Windows uses ; separator for add-data
$AddData = "icons;icons"

python -m PyInstaller --noconfirm --onefile --windowed --icon "icons/icon128X128.ico" --add-data "$AddData" --hidden-import=tkinter --collect-all=customtkinter ctkRouletteOverlay.py

if ($LASTEXITCODE -eq 0) {
    Write-Host "Build complete." -ForegroundColor Green
    Write-Host "Artifact located at dist\ctkRouletteOverlay.exe" -ForegroundColor Green
} else {
    Write-Host "Build failed." -ForegroundColor Red
    exit 1
}

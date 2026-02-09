$ErrorActionPreference = "Stop"

# Ensure we are in the project root
Set-Location -Path $PSScriptRoot/..

# Check dependencies
Write-Host "Checking dependencies..." -ForegroundColor Cyan
if (-not (python -m PyInstaller --version 2>$null)) {
    Write-Host "Error: PyInstaller module not found. Please install it with 'pip install pyinstaller'." -ForegroundColor Red
    exit 1
}

if (-not (Get-Command "gh" -ErrorAction SilentlyContinue)) {
    Write-Host "Error: GitHub CLI (gh) not found. Please install it." -ForegroundColor Red
    exit 1
}
Write-Host "Dependencies detected." -ForegroundColor Green

# Get release details
$version = Read-Host "Enter release version (e.g., v1.1.0)"
if ([string]::IsNullOrWhiteSpace($version)) {
    Write-Host "Version is required." -ForegroundColor Red
    exit 1
}

$title = Read-Host "Enter release title (default: $version)"
if ([string]::IsNullOrWhiteSpace($title)) {
    $title = $version
}

$confirm = Read-Host "Preparing to release $version - $title. Continue? (y/n)"
if ($confirm -ne "y") {
    Write-Host "Aborted." -ForegroundColor Yellow
    exit 0
}

# Build executable
Write-Host "Building executable..." -ForegroundColor Cyan

if (Test-Path "build") { Remove-Item "build" -Recurse -Force }
if (Test-Path "dist") { Remove-Item "dist" -Recurse -Force }
if (Test-Path "RouletteOverlay.spec") { Remove-Item "RouletteOverlay.spec" -Force }

$AddData = "icons;icons"

python -m PyInstaller --noconfirm --onefile --windowed --icon "icons/icon128X128.ico" --add-data "$AddData" --hidden-import=tkinter --collect-all=customtkinter ctkRouletteOverlay.py

if ($LASTEXITCODE -ne 0) {
    Write-Host "Build failed." -ForegroundColor Red
    exit 1
}

Write-Host "Build complete." -ForegroundColor Green

# Check for artifact
$Artifact = "dist\ctkRouletteOverlay.exe"
if (-not (Test-Path $Artifact)) {
    Write-Host "Error: Artifact not found at $Artifact" -ForegroundColor Red
    exit 1
}

# Publish release
Write-Host "Publishing release $version..." -ForegroundColor Cyan
$NotesFile = "RELEASE.md"

if (-not (Test-Path $NotesFile)) {
    Write-Host "Warning: Release notes file '$NotesFile' not found. Checking for release_notes.md..." -ForegroundColor Yellow
    if (Test-Path "release_notes.md") {
        $NotesFile = "release_notes.md"
    } else {
        Write-Host "Warning: No release notes found. Creating empty RELEASE.md." -ForegroundColor Yellow
        New-Item -ItemType File -Path "RELEASE.md" | Out-Null
    }
}

gh release create "$version" "$Artifact" --title "$title" --notes-file "$NotesFile"

if ($LASTEXITCODE -eq 0) {
    Write-Host "Release $version published successfully!" -ForegroundColor Green
} else {
    Write-Host "Release failed." -ForegroundColor Red
    exit 1
}

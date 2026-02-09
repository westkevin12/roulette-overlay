# Roulette Overlay

An overlay tool that helps you track your roulette betting streaks, calculates how often to raise and by how much based on your balance.

## Features
- Tracks bets in 3 currency types: whole numbers (e.g., RSGP), currency ($0,000.00), and crypto (16 decimal places).
- Includes an "Always on Top" overlay window.
- Customizable bet settings.

## Installation

### Executable (Windows)
Download the latest `RouletteOverlay.exe` from the [Releases](../../releases) page.
> **Note:** Ensure the `icons` folder is in the same directory as the executable if not bundled.

### Source (Python)
1. Clone the repository.
2. Install `customtkinter` if using the modern UI version:
   ```bash
   pip install customtkinter
   ```
3. Run the application:
   ```bash
   python RouletteOverlay.py
   # or for the modern UI version
   python ctkRouletteOverlay.py
   ```

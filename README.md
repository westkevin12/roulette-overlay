# Roulette Overlay

A lightweight, "Always on Top" betting tracker and strategy tool for Roulette.

This tool helps you track your betting streaks, automatically calculates how often to raise stake and by how much based on your balance, and provides real-time profit analysis.

## Features

- **Automated Stake Calculation**: Intelligent betting strategy adjustments.
- **Multi-Currency Support**:
  - **GP**: Whole numbers (e.g., RuneScape Gold).
  - **Fiat**: Standard currency formatting ($0,000.00).
  - **Crypto**: High-precision decimal formatting (16 decimal places).
- **Streak Tracking**: Keep track of wins/losses and set progressions.
- **Profit Analysis**: Real-time view of total cost, current bet, and net profit.
- **Modern Overlay UI**: Built with `CustomTkinter` for a sleek, dark-themed interface that stays on top of your game window.
- **Legacy Support**: Includes a standard `tkinter` version (`RouletteOverlay.py`) for older systems.

## Installation & Usage

### Recommended: Using `uv`

This project is optimized for `uv`, a fast Python package installer and resolver.

1.  **Install `uv`** (if not already installed):
    - **macOS/Linux**: `curl -LsSf https://astral.sh/uv/install.sh | sh`
    - **Windows**: `powershell -c "irm https://astral.sh/uv/install.ps1 | iex"`

2.  **Run the Application**:
    You can run the application directly from the source without manual environment setup:
    ```bash
    uv run ctkRouletteOverlay.py
    ```
    _Note: The first run will automatically install necessary dependencies (`customtkinter`, `pillow`)._

### Alternative: Standard Python (pip)

1.  Clone the repository.
2.  Install dependencies:
    ```bash
    pip install customtkinter pillow
    ```
3.  Run the application:
    ```bash
    python ctkRouletteOverlay.py
    ```

### Windows Executable

If you prefer a standalone executable:

1.  Download the latest `RouletteOverlay.exe` from the [Releases](../../releases) page.
2.  Ensure the `icons` folder is in the same directory as the executable.
3.  Run `RouletteOverlay.exe`.

## Requirements

- Python 3.13+ (for source execution)
- `customtkinter`
- `pillow` (for Linux icon support)

## License

Copyright (C) 2023 eXtremeVisionGaming
Distributed under the GNU General Public License v3. See `LICENSE` for more information.

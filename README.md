# AFX Gaming Mode

A Windows gaming launcher focused on safe performance improvements, live system monitoring, and automatic restoration after your game closes.

> **No fake FPS promises.** AFX Gaming Mode improves the environment around your game by managing process priority, power mode, and visibility into heavy background apps.

## Features

- Add/select any Windows game `.exe`
- One-click **Gaming Mode Launch**
- Raise game process priority safely
- Optional Windows **High Performance** power plan
- Automatically restore **Balanced** power mode after the game exits
- Live CPU and RAM usage
- Heavy background-process detector
- Game session timer
- Performance profile selector
- Save favorite game path
- Open Windows Game Mode settings
- Open Task Manager
- Diagnostic CLI mode
- Unit tests
- GitHub Actions workflow

## What it does

AFX Gaming Mode focuses on changes that are easy to understand and restore:

- launches the selected game
- optionally switches Windows power mode
- raises the game's process priority
- monitors system load during play
- identifies resource-heavy background processes
- restores the Windows power plan when the session ends

## What it does NOT do

It does not:

- disable Windows Security
- modify critical registry settings
- delete system files
- kill random processes automatically
- claim guaranteed FPS gains
- bypass anti-cheat software
- inject code into games

## Requirements

- Windows 10 or Windows 11
- Python 3.10+
- Install dependencies:

```bash
pip install -r requirements.txt
```

## Run

```bash
python main.py
```

Or double-click:

```text
scripts/run_windows.bat
```

## Diagnostics

```bash
python main.py --diagnose
```

## Repository structure

```text
AFX-Gaming-Mode/
├── README.md
├── main.py
├── requirements.txt
├── LICENSE
├── CHANGELOG.md
├── CONTRIBUTING.md
├── .gitignore
├── app/
│   ├── __init__.py
│   ├── ui.py
│   ├── launcher.py
│   ├── monitor.py
│   ├── profiles.py
│   ├── settings.py
│   └── windows_tools.py
├── config/
│   └── settings.json
├── docs/
│   └── GAMING_PERFORMANCE_GUIDE.md
├── scripts/
│   └── run_windows.bat
├── tests/
│   ├── test_profiles.py
│   └── test_settings.py
└── .github/
    └── workflows/
        └── python-tests.yml
```

## Performance profiles

### Eco
For lower-end systems where keeping background load low matters most.

### Balanced
Best default for most PCs.

### Competitive
Uses higher process priority and is intended for gaming systems with enough cooling and available resources.

## Important

Game performance depends on CPU, GPU, RAM, thermals, drivers, game settings, display refresh rate, and the game engine itself.

## License

MIT

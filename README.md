# Writer

Auto Writer - Automated keyboard typing script with Windows service support.

## Features

- 🎯 Automated keyboard input simulation
- ⚡ Randomized typing speed for natural appearance
- 🌍 Support for non-ASCII characters (åäö, etc.)
- 🖥️ **Windows Service mode** - Run as background service
- 🔄 Auto-restart capability
- ⚙️ Configurable delays and behavior

## Quick Start

### Basic Usage

```bash
# Install dependencies
pip install pyautogui pyperclip

# Run with default text
python write.py

# Run with custom text
python write.py --text "Your text here"

# Run from file
python write.py --file mytext.txt

# Customize timing
python write.py --delay 3 --min-interval 0.05 --max-interval 0.15
```

### Windows Service Mode 🪟

Run as a persistent background service that cannot be easily closed:

```batch
# Install dependencies
pip install -r requirements.txt

# Install service (requires Administrator)
install_service.bat

# Follow prompts to install and start
```

**See [SERVICE_SETUP.md](SERVICE_SETUP.md) for complete service documentation.**

## Files

- `write.py` - Main typing script
- `write_service.py` - Windows service wrapper
- `install_service.bat` - Service installer/manager
- `service_config.txt` - Service configuration
- `text.txt` - Default text to type
- `SERVICE_SETUP.md` - Complete service setup guide

## Requirements

- Python 3.7+
- pyautogui
- pyperclip (optional, for clipboard support)
- pywin32 (for Windows service mode)

## License

Use responsibly and ensure you have proper authorization for automated keyboard input.
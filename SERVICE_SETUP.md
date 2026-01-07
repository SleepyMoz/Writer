# Auto Writer Windows Service Setup Guide

This guide explains how to run the Auto Writer script as a Windows background service that cannot be easily closed by other programs.

## Prerequisites

1. **Python 3.7 or higher** installed on Windows
2. **Administrator privileges** to install and manage Windows services
3. **Active user session** (GUI automation requires an active desktop)

## Installation Steps

### Step 1: Install Required Dependencies

Open Command Prompt or PowerShell as Administrator and navigate to the Writer directory:

```batch
cd C:\path\to\Writer
pip install -r requirements.txt
```

This will install:
- `pyautogui` - For keyboard automation
- `pywin32` - For Windows service functionality
- `pyperclip` - For clipboard operations

### Step 2: Install the Service

Run the installer batch file as Administrator:

```batch
install_service.bat
```

Select option **1** to install the service.

Alternatively, you can install manually:

```batch
python write_service.py install
```

### Step 3: Configure the Service (Optional)

Edit `service_config.txt` to customize behavior:

```ini
delay=5.0                      # Wait 5 seconds before starting to type
min_interval=0.02              # Minimum delay between keystrokes
max_interval=0.12              # Maximum delay between keystrokes
randomize=true                 # Randomize typing speed
restart_on_completion=true     # Auto-restart after finishing
restart_delay=10.0             # Wait 10 seconds before restarting
```

Edit `text.txt` to set the text that will be typed:

```text
Your text here...
Multiple lines supported.
Special characters work: åäö
```

### Step 4: Start the Service

Using the installer:

```batch
install_service.bat
```

Select option **2** to start the service.

Or manually:

```batch
net start AutoWriterService
```

Or via Windows Services Manager:
1. Press `Win + R`, type `services.msc`, press Enter
2. Find "Auto Writer Background Service"
3. Right-click → Start

## Service Management

### Check Service Status

```batch
sc query AutoWriterService
```

Or use the installer (option 6).

### Stop the Service

```batch
net stop AutoWriterService
```

Or use the installer (option 3).

### Restart the Service

```batch
install_service.bat
```

Select option **4**, or manually:

```batch
net stop AutoWriterService
net start AutoWriterService
```

### Uninstall the Service

```batch
install_service.bat
```

Select option **5**, or manually:

```batch
net stop AutoWriterService
python write_service.py remove
```

## Service Features

### 1. **Automatic Restart on Failure**
The service is configured to automatically restart if it crashes or encounters an error.

### 2. **Protected from Normal Process Termination**
- Cannot be closed via Task Manager without Administrator privileges
- Requires stopping the service through proper channels
- Survives application crashes

### 3. **Configurable Behavior**
Edit `service_config.txt` and `text.txt` without reinstalling the service. Stop and start the service to apply changes.

### 4. **Event Logging**
Service events are logged to Windows Event Viewer:
1. Press `Win + R`, type `eventvwr.msc`, press Enter
2. Navigate to: Windows Logs → Application
3. Look for events from "AutoWriterService"

## Important Notes

### Security Considerations

⚠️ **This service performs automated keyboard input. Important points:**

- Ensure you have authorization to run this on your system
- The service runs with the privileges of the SYSTEM account or the user you configure
- Some security software may flag keyboard automation as suspicious
- Always use responsibly and legally

### Technical Limitations

1. **Requires Active User Session**: The service needs an active desktop session to perform GUI automation. It won't work when:
   - No user is logged in
   - The desktop is locked
   - Running via Remote Desktop without proper configuration

2. **Display Required**: GUI automation requires `DISPLAY` access (user must be logged in graphically).

3. **Administrator Can Always Stop**: System administrators with proper privileges can always stop or disable the service.

### Troubleshooting

**Service won't start:**
- Check that all dependencies are installed: `pip install -r requirements.txt`
- Verify Python is in system PATH
- Check Event Viewer for error messages
- Ensure `text.txt` exists and is not empty

**Typing doesn't work:**
- Verify an active user session is present
- Check that `pyautogui` can access the keyboard
- Disable any conflicting keyboard software
- Try running `write.py` manually first to test

**Service installs but doesn't type:**
- Check `service_config.txt` configuration
- Verify `text.txt` contains text to type
- Check Windows Event Viewer for service logs
- Ensure no screen saver or lock screen is active

**Can't uninstall:**
- Stop the service first: `net stop AutoWriterService`
- Wait a few seconds, then run uninstall
- If still stuck, restart Windows and try again

## Manual Service Control Commands

```batch
# Install service
python write_service.py install

# Start service
net start AutoWriterService

# Stop service
net stop AutoWriterService

# Remove service
python write_service.py remove

# Update service (reinstall)
python write_service.py update

# Debug mode (run in console, not as service)
python write_service.py debug
```

## Configuration Reference

### service_config.txt Options

| Option | Type | Default | Description |
|--------|------|---------|-------------|
| `delay` | float | 5.0 | Initial delay before typing starts (seconds) |
| `min_interval` | float | 0.02 | Minimum delay between characters |
| `max_interval` | float | 0.12 | Maximum delay between characters |
| `randomize` | boolean | true | Randomize delays for natural typing |
| `restart_on_completion` | boolean | true | Auto-restart after finishing text |
| `restart_delay` | float | 10.0 | Delay before restarting (seconds) |
| `text_file` | path | text.txt | Path to file containing text to type |

## Advanced: Running on System Startup

The service can be configured to start automatically when Windows boots:

```batch
sc config AutoWriterService start=auto
```

To disable automatic startup:

```batch
sc config AutoWriterService start=demand
```

## Support

For issues or questions:
- Check Windows Event Viewer for service logs
- Verify all prerequisites are met
- Test `write.py` manually first
- Review this documentation carefully

## License and Disclaimer

This tool is provided as-is. Users are responsible for ensuring they have proper authorization to run automated keyboard input on their systems. Always comply with applicable laws and organizational policies.

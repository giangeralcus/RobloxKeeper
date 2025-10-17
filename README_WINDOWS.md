# 🎮 Anime Vanguards Keeper - Windows Edition

**Professional AFK automation system for Anime Vanguards on Roblox with GUI controls.**

## ✨ Features

### 🖥️ **Windows GUI Application**
- ✅ **Start/Pause/Stop** controls with visual feedback
- ✅ **Real-time statistics dashboard** showing:
  - Uptime tracking
  - Total clicks and screenshots
  - Crash count
  - Error dialogs dismissed
  - Last activity timestamps
- ✅ **Live activity log viewer** with timestamps
- ✅ **Professional dark-themed interface**

### 🤖 **Automation Features**
- ✅ **Auto-click system** - Clicks every 18 minutes to prevent AFK timeout
- ✅ **Screenshot monitoring** - Captures full screenshots every hour
- ✅ **Crash detection** - Monitors if Roblox closes unexpectedly
- ✅ **Auto-relaunch** - Automatically relaunches Roblox and rejoins Anime Vanguards
- ✅ **Error dialog dismissal** - Auto-clicks "OK" on error dialogs every 15 seconds
- ✅ **Game finder** - Uses color detection to find and click play button

### 🔧 **Advanced Capabilities**
- ✅ **Configurable settings** via `config/config.json`
- ✅ **Comprehensive logging** - Activity logs, stats logs, and JSON status
- ✅ **Windows-optimized** - Uses pygetwindow, mss, and psutil

---

## 🚀 Quick Start

### Step 1: Install Dependencies

**Double-click `install.bat`** or run in terminal:

```bash
install.bat
```

This will install all required packages:
- pyautogui (mouse/keyboard automation)
- pygetwindow (window detection)
- Pillow (image processing)
- mss (fast screenshots)
- pytesseract (OCR - optional)
- opencv-python (image analysis)
- numpy (array processing)
- psutil (process monitoring)

### Step 2: Configure Settings (Optional)

Edit `config/config.json` to customize:

```json
{
  "game_name": "Anime Vanguards",
  "click_interval_minutes": 18,
  "screenshot_interval_seconds": 3600,
  "auto_relaunch": true
}
```

### Step 3: Start the Application

1. **Start Roblox** and enter Anime Vanguards
2. **Double-click `START_KEEPER.bat`**
3. **Click the START button** in the GUI

---

## 🖱️ GUI Controls

| Button | Function |
|--------|----------|
| **▶️ START** | Start monitoring (Roblox must be running) |
| **⏸️ PAUSE** | Pause/Resume monitoring |
| **⏹️ STOP** | Stop monitoring completely |
| **🗑️ CLEAR LOG** | Clear the activity log viewer |

---

## 📊 Statistics Dashboard

The GUI displays real-time statistics:

- **Status**: Current keeper state (Running/Paused/Stopped)
- **Uptime**: How long the keeper has been running
- **Total Clicks**: Number of AFK-prevention clicks
- **Screenshots**: Number of screenshots captured
- **Crashes**: Times Roblox crashed and relaunched
- **Errors Dismissed**: Error dialogs automatically closed
- **Last Click**: Timestamp of last activity click
- **Last Screenshot**: Timestamp of last screenshot

---

## 📁 Project Structure

```
RobloxKeeper/
├── START_KEEPER.bat       ← Double-click to launch
├── install.bat            ← Double-click to install
├── requirements.txt       ← Python dependencies
├── README_WINDOWS.md      ← This file
├── config/
│   └── config.json        ← Settings
├── src/
│   ├── gui_app.py         ← GUI application
│   └── keeper_engine.py   ← Core automation engine
├── logs/
│   ├── keeper.log         ← Main activity log
│   ├── stats.log          ← Stats events
│   └── status.json        ← Current status (JSON)
└── screenshots/
    └── roblox_*.png       ← Hourly screenshots
```

---

## 🔍 How It Works

### Monitoring Intervals

| Task | Interval | Description |
|------|----------|-------------|
| **Error Check** | 15 seconds | Detects and dismisses error dialogs |
| **Status Check** | 30 seconds | Monitors if Roblox is running |
| **AFK Click** | 18 minutes | Clicks to prevent timeout |
| **Screenshot** | 1 hour | Captures game state |

### Auto-Relaunch Sequence

When Roblox crashes, the keeper automatically:

1. **Detects** Roblox process has stopped
2. **Logs** the crash event
3. **Launches** Roblox via Windows protocol
4. **Waits** 15 seconds for Roblox to load
5. **Searches** for Anime Vanguards game card
6. **Clicks** the game to open details
7. **Finds** the blue play button using color detection
8. **Clicks** the play button to rejoin
9. **Resumes** monitoring

---

## ⚙️ Configuration Options

Edit `config/config.json`:

```json
{
  "game_name": "Anime Vanguards",
  "click_interval_minutes": 18,
  "screenshot_interval_seconds": 3600,
  "error_check_interval_seconds": 15,
  "status_check_interval_seconds": 30,
  "dashboard_update_interval_seconds": 300,
  "roblox_process_name": "RobloxPlayerBeta.exe",
  "auto_relaunch": true,
  "game_load_wait_seconds": 15,
  "play_button_color": {
    "r": 52,
    "g": 152,
    "b": 219,
    "tolerance": 30
  }
}
```

---

## 🐛 Troubleshooting

### Application won't start

**Error**: "Python is not installed"
- Install Python 3.8+ from https://www.python.org/
- Make sure to check "Add Python to PATH" during installation

**Error**: "No module named 'pyautogui'"
- Run `install.bat` to install dependencies
- Or manually: `pip install -r requirements.txt`

### Keeper shows "Roblox Not Running"

**Solution**: Start Roblox first, then click START in the GUI

### Auto-relaunch doesn't work

**Possible causes**:
- Roblox not in default location
- Screen resolution too high/low
- Game card position changed

**Solutions**:
1. Check logs for error messages
2. Verify `config.json` settings
3. Manually adjust play button color detection

### Screenshots are blank

**Solution**:
- Grant Python permission to capture screen
- Check Windows Privacy Settings → Screen Capture

---

## 📝 Logs

### keeper.log
Main activity log with all events:
```
[2025-10-17 12:30:45] [INFO] ✓ Double-clicked at center: (1064, 533)
[2025-10-17 13:00:00] [INFO] 📸 Screenshot saved: screenshots/roblox_20251017_130000.png
[2025-10-17 13:15:30] [INFO] 🆗 Attempted to dismiss error dialogs
```

### stats.log
Statistics events only:
```
[2025-10-17 12:30:45] CLICK: Position: (1064, 533), Total: 42
[2025-10-17 13:00:00] SCREENSHOT: File: roblox_20251017_130000.png, Total: 13
```

### status.json
Current status in JSON format:
```json
{
  "start_time": "2025-10-17 12:00:00",
  "total_clicks": 42,
  "total_screenshots": 13,
  "roblox_crashes": 0,
  "error_dialogs_dismissed": 8,
  "status": "running"
}
```

---

## 🔐 Safety & Privacy

- ✅ **Runs locally** - No data sent anywhere
- ✅ **No account access** - Only simulates mouse clicks
- ✅ **No game modifications** - Just automation, no hacks
- ✅ **Safe clicking** - Avoids UI buttons, clicks center only
- ✅ **Open source** - You can review all code

---

## 📞 Support

If the keeper isn't working:

1. Check `logs/keeper.log` for errors
2. Verify Roblox is running
3. Ensure all dependencies are installed
4. Check configuration in `config/config.json`
5. Try restarting both Roblox and the keeper

---

## 🎯 Tips for Best Results

1. **Position your AFK chamber** in the center of the screen
2. **Minimize other windows** to prevent accidental clicks
3. **Check screenshots** to verify game state
4. **Review logs** to track keeper activity
5. **Adjust click interval** based on your needs

---

## 📄 License

For personal use only. Use responsibly and in accordance with Roblox Terms of Service.

---

## 🎉 Changelog

### Version 3.0 - Windows GUI Edition
- ✅ Full Windows GUI application
- ✅ Start/Pause/Stop/Clear Log buttons
- ✅ Real-time statistics dashboard
- ✅ Live activity log viewer
- ✅ Color-based play button detection
- ✅ Configurable JSON settings
- ✅ Enhanced auto-relaunch for Anime Vanguards
- ✅ Professional dark-themed interface

---

Created: October 17, 2025
Version: 3.0 Windows GUI Edition
Game: Anime Vanguards on Roblox

# 🎮 Roblox AFK Keeper

Advanced monitoring system for keeping your Roblox game active with intelligent crash detection, server load monitoring, and detailed statistics tracking.

## 📋 Features

✅ **Auto-Click System**
- Clicks Roblox every 18 minutes to prevent AFK timeout
- Smart center-clicking to avoid UI buttons
- Automatic window detection and activation

✅ **Screenshot Monitoring**
- Captures full screenshots every hour
- Saves to organized folders with timestamps
- Detects server loading/moving

✅ **Crash Detection & Auto-Relaunch**
- Monitors if Roblox closes unexpectedly
- Automatically relaunches Roblox on crash
- Rejoins Vanguard game automatically
- Logs crash events with timestamps

✅ **Status Dashboard**
- Real-time uptime tracking
- Total clicks and screenshots counter
- Server loads and crashes detected
- Live countdown timers

✅ **Error Dialog Dismissal**
- Automatically detects error dialogs (e.g., "Teleport Failed")
- Clicks OK buttons to dismiss errors
- Checks every 15 seconds
- Prevents getting stuck on error screens

✅ **Comprehensive Logging**
- Main activity log (keeper.log)
- Stats log (stats.log)
- JSON status file for programmatic access
- Screenshot archive with timestamps

## 📁 Folder Structure

```
RobloxKeeper/
├── launch.sh               → Main launcher script
├── README.md               → This file
├── scripts/
│   ├── keeper.py           → Main monitoring script
│   └── view_status.py      → Status viewer utility
├── logs/
│   ├── keeper.log          → Main activity log
│   ├── stats.log           → Stats events log
│   ├── status.json         → Current status (JSON)
│   └── keeper.pid          → Process ID file
└── screenshots/
    └── roblox_*.png        → Hourly screenshots
```

## 🚀 Quick Start

### 1. Make launcher executable
```bash
chmod +x launch.sh
```

### 2. Start Roblox game first
Open Roblox and enter your AFK chamber

### 3. Start the keeper
```bash
./launch.sh start
```

## 📖 Commands

| Command | Description |
|---------|-------------|
| `./launch.sh start` | Start the keeper |
| `./launch.sh stop` | Stop the keeper |
| `./launch.sh restart` | Restart the keeper |
| `./launch.sh status` | Show current status |
| `./launch.sh logs` | Show recent logs |
| `./launch.sh help` | Show help |

## 📊 Monitoring Dashboard

The keeper displays a real-time dashboard showing:

```
╔══════════════════════════════════════════════════════════════════╗
║                    🎮 ROBLOX KEEPER STATUS                       ║
╠══════════════════════════════════════════════════════════════════╣
║ Status:           active                                         ║
║ Uptime:           2d 5h 30m                                      ║
║ Total Clicks:     167                                            ║
║ Total Screenshots: 51                                            ║
║ Server Loads:     3                                              ║
║ Crashes Detected: 0                                              ║
║ Errors Dismissed: 12                                             ║
║ Last Click:       2025-10-17 12:30:45                            ║
║ Last Screenshot:  2025-10-17 12:00:00                            ║
║ Last Error Fixed: 2025-10-17 11:45:30                            ║
╚══════════════════════════════════════════════════════════════════╝
```

## 📸 Screenshots

Screenshots are saved with timestamp format:
- `roblox_YYYYMMDD_HHMMSS.png`

Example: `roblox_20251017_005311.png`

Review screenshots to track your:
- AFK Chamber rewards
- Event Currencies
- Total Gems
- Game progress

## 🔍 What Gets Monitored

### Every 15 seconds:
- ✅ Check for error dialogs
- ✅ Automatically dismiss error messages
- ✅ Keep game running smoothly

### Every 30 seconds:
- ✅ Is Roblox still running?
- ✅ Process health check
- ✅ Auto-relaunch if crashed (relaunches Roblox and rejoins Vanguard)

### Every 18 minutes:
- ✅ Double-click in game center
- ✅ Log click position and time

### Every hour:
- ✅ Capture full screenshot
- ✅ Check for loading screens
- ✅ Save with timestamp

### Every 5 minutes:
- ✅ Refresh dashboard display
- ✅ Update status.json

## 📝 Log Files

### keeper.log
Main activity log with all events:
```
[2025-10-17 00:53:09] [INFO] 🚀 Enhanced Roblox Keeper Started
[2025-10-17 00:53:10] [INFO] ✓ Double-clicked at center: (1064, 533)
[2025-10-17 00:53:11] [INFO] 📸 Screenshot saved: ...
[2025-10-17 01:00:00] [WARN] ⚠️ Server loading detected!
```

### stats.log
Statistics events only:
```
[2025-10-17 00:53:10] CLICK: Position: (1064, 533), Total: 1
[2025-10-17 00:53:11] SCREENSHOT: File: roblox_..., Total: 1
[2025-10-17 01:15:30] SERVER_LOADING: Screenshot: roblox_...
```

### status.json
Current status in JSON format for programmatic access:
```json
{
  "start_time": "2025-10-17 00:53:09",
  "total_clicks": 167,
  "total_screenshots": 51,
  "roblox_crashes": 0,
  "server_loads_detected": 3,
  "error_dialogs_dismissed": 12,
  "last_click": "2025-10-17 12:30:45",
  "last_screenshot": "2025-10-17 12:00:00",
  "last_error_dismissed": "2025-10-17 11:45:30",
  "status": "active"
}
```

## ⚙️ Configuration

Edit `scripts/keeper.py` to customize:

```python
CLICK_INTERVAL_MINUTES = 18          # Click every 18 minutes
SCREENSHOT_INTERVAL_SECONDS = 3600   # Screenshot every hour
```

## ⚠️ Troubleshooting

### Keeper won't start
- Make sure Roblox is running first
- Check permissions: `chmod +x launch.sh`
- View error logs: `./launch.sh logs`

### No screenshots
- Grant Screen Recording permission:
  - System Settings → Privacy & Security → Screen Recording
  - Enable for Terminal

### Roblox crashes
- Keeper will detect and log the crash
- **Auto-relaunch** will activate automatically:
  - Launches Roblox
  - Waits for it to load
  - Attempts to find and click Vanguard game
  - Clicks play button
- If auto-relaunch fails, restart manually
- Keeper will resume monitoring automatically

## 🔐 Safety Features

- **Safe clicking**: Only clicks in center, avoids UI buttons
- **No account access**: Script runs locally, no data sent anywhere
- **No game modifications**: Only simulates mouse clicks
- **Crash detection**: Alerts you if Roblox closes

## 🚧 Future Improvements

Potential enhancements:
- OCR text recognition for auto-logging stats
- Telegram/Discord notifications
- Web dashboard for remote monitoring
- Multiple game profiles
- Custom click patterns
- Audio alerts for crashes

## 📞 Support

If the keeper isn't working:
1. Check `./launch.sh logs`
2. Verify Roblox is running
3. Check `logs/keeper.log` for errors
4. Ensure screen recording permissions are enabled

## 📄 License

For personal use only. Use responsibly and in accordance with Roblox Terms of Service.

---

Created: October 17, 2025
Version: 3.0 Auto-Relaunch Edition

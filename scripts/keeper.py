#!/usr/bin/env python3
"""
Roblox AFK Keeper - Enhanced Version
Advanced monitoring with crash detection and server loading detection
"""

import time
import pyautogui
import subprocess
from datetime import datetime
import os
import json

# Configuration
BASE_DIR = "/Users/giangeralcus/Desktop/RobloxKeeper"
CLICK_INTERVAL_MINUTES = 18
CLICK_INTERVAL_SECONDS = CLICK_INTERVAL_MINUTES * 60
SCREENSHOT_INTERVAL_SECONDS = 3600  # 1 hour
LOG_FILE = f"{BASE_DIR}/logs/keeper.log"
STATUS_FILE = f"{BASE_DIR}/logs/status.json"
SCREENSHOT_DIR = f"{BASE_DIR}/screenshots"
STATS_LOG = f"{BASE_DIR}/logs/stats.log"

# Tracking
stats = {
    'start_time': None,
    'total_clicks': 0,
    'total_screenshots': 0,
    'roblox_crashes': 0,
    'server_loads_detected': 0,
    'error_dialogs_dismissed': 0,
    'last_click': None,
    'last_screenshot': None,
    'last_error_dismissed': None,
    'status': 'running'
}

def log_message(message, level="INFO"):
    """Log message to file and console"""
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    log_entry = f"[{timestamp}] [{level}] {message}"
    print(log_entry)

    with open(LOG_FILE, 'a') as f:
        f.write(log_entry + "\n")

def save_stats():
    """Save current stats to JSON"""
    try:
        with open(STATUS_FILE, 'w') as f:
            json.dump(stats, f, indent=2)
    except Exception as e:
        log_message(f"Failed to save stats: {e}", "ERROR")

def log_stats(event_type, details=""):
    """Log stats events"""
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    entry = f"[{timestamp}] {event_type}: {details}\n"
    with open(STATS_LOG, 'a') as f:
        f.write(entry)

def is_roblox_running():
    """Check if Roblox is running"""
    try:
        result = subprocess.run(
            ['pgrep', '-i', 'roblox'],
            capture_output=True,
            text=True
        )
        return result.returncode == 0
    except Exception as e:
        log_message(f"Error checking Roblox status: {e}", "ERROR")
        return False

def get_roblox_window_info():
    """Get Roblox window position and size"""
    try:
        script = '''
        tell application "System Events"
            set robloxApp to first application process whose name contains "Roblox"
            tell robloxApp
                set windowPos to position of window 1
                set windowSize to size of window 1
                return {item 1 of windowPos, item 2 of windowPos, item 1 of windowSize, item 2 of windowSize}
            end tell
        end tell
        '''

        result = subprocess.run(['osascript', '-e', script],
                              capture_output=True,
                              text=True,
                              timeout=5)

        if result.returncode == 0:
            values = result.stdout.strip().split(', ')
            x, y, width, height = map(int, values)
            return {'x': x, 'y': y, 'width': width, 'height': height}
        return None
    except Exception as e:
        log_message(f"Error getting window info: {e}", "WARN")
        return None

def activate_roblox():
    """Bring Roblox to front"""
    try:
        script = '''
        tell application "System Events"
            set robloxApp to first application process whose name contains "Roblox"
            set frontmost of robloxApp to true
        end tell
        '''
        subprocess.run(['osascript', '-e', script],
                      capture_output=True,
                      timeout=5)
        time.sleep(0.5)
        return True
    except Exception as e:
        log_message(f"Error activating Roblox: {e}", "ERROR")
        return False

def dismiss_error_dialogs():
    """Detect and dismiss Roblox error dialogs like 'Teleport Failed'"""
    try:
        window_info = get_roblox_window_info()
        if not window_info:
            return False

        # Activate Roblox first
        activate_roblox()
        time.sleep(0.2)

        # Error dialogs in Roblox typically appear in the center
        # The OK button is usually in the lower-center area of the dialog
        center_x = window_info['x'] + (window_info['width'] // 2)
        center_y = window_info['y'] + (window_info['height'] // 2)

        # Try clicking in potential OK button locations
        # Roblox error dialogs usually have the OK button slightly below center
        ok_button_locations = [
            (center_x, center_y + 50),   # Below center
            (center_x, center_y + 70),   # A bit more below
            (center_x, center_y + 90),   # Even more below
            (center_x - 50, center_y + 60),  # Left of center, below
            (center_x + 50, center_y + 60),  # Right of center, below
        ]

        # Try clicking each potential location
        for x, y in ok_button_locations:
            pyautogui.click(x, y)
            time.sleep(0.1)

        stats['error_dialogs_dismissed'] += 1
        stats['last_error_dismissed'] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        log_message("🆗 Attempted to dismiss error dialogs", "INFO")
        log_stats("ERROR_DIALOG_DISMISSED", f"Total dismissed: {stats['error_dialogs_dismissed']}")
        save_stats()

        return True
    except Exception as e:
        log_message(f"Error dismissing dialogs: {e}", "WARN")
        return False

def check_for_loading_screen(screenshot_path):
    """Check if Roblox is showing a loading screen"""
    try:
        # Simple check: if screenshot is very small or uniform, might be loading
        # This is a placeholder - you can enhance with actual image analysis
        file_size = os.path.getsize(screenshot_path)
        # If file is suspiciously small (< 100KB), might be loading/blank screen
        if file_size < 100000:
            return True
        return False
    except:
        return False

def safe_click_roblox():
    """Click safely in the center area of Roblox window"""
    window_info = get_roblox_window_info()
    if not window_info:
        log_message("Could not get window info for clicking", "WARN")
        stats['status'] = 'warning'
        return False

    # Click in the center of the window (safe area)
    center_x = window_info['x'] + (window_info['width'] // 2)
    center_y = window_info['y'] + (window_info['height'] // 2)

    # Activate window first
    if not activate_roblox():
        stats['status'] = 'warning'
        return False

    # Double-click in center
    pyautogui.doubleClick(center_x, center_y)

    stats['total_clicks'] += 1
    stats['last_click'] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    stats['status'] = 'active'

    log_message(f"✓ Double-clicked at center: ({center_x}, {center_y})")
    log_stats("CLICK", f"Position: ({center_x}, {center_y}), Total: {stats['total_clicks']}")
    save_stats()

    return True

def take_screenshot():
    """Take a full screenshot for manual review"""
    try:
        # Activate Roblox first
        activate_roblox()
        time.sleep(0.3)

        # Take full screenshot
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"{SCREENSHOT_DIR}/roblox_{timestamp}.png"

        # Use screencapture command (macOS native)
        subprocess.run(['screencapture', '-x', filename], check=True)

        # Check if it's a loading screen
        is_loading = check_for_loading_screen(filename)

        stats['total_screenshots'] += 1
        stats['last_screenshot'] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        if is_loading:
            stats['server_loads_detected'] += 1
            log_message(f"⚠️  Server loading detected! Screenshot: {filename}", "WARN")
            log_stats("SERVER_LOADING", f"Screenshot: {filename}")
        else:
            log_message(f"📸 Screenshot saved: {filename}")
            log_stats("SCREENSHOT", f"File: {filename}, Total: {stats['total_screenshots']}")

        save_stats()
        return True
    except Exception as e:
        log_message(f"Screenshot failed: {e}", "ERROR")
        stats['status'] = 'error'
        save_stats()
        return False

def monitor_roblox_status():
    """Monitor if Roblox is still running"""
    if not is_roblox_running():
        stats['roblox_crashes'] += 1
        stats['status'] = 'crashed'
        log_message("❌ ALERT: Roblox is not running! Please restart the game.", "CRITICAL")
        log_stats("CRASH", f"Total crashes: {stats['roblox_crashes']}")
        save_stats()
        return False
    return True

def print_dashboard():
    """Print a status dashboard"""
    uptime = ""
    if stats['start_time']:
        start = datetime.strptime(stats['start_time'], "%Y-%m-%d %H:%M:%S")
        delta = datetime.now() - start
        hours = delta.seconds // 3600
        minutes = (delta.seconds % 3600) // 60
        uptime = f"{delta.days}d {hours}h {minutes}m"

    last_error = stats.get('last_error_dismissed') or 'Never'

    dashboard = f"""
╔══════════════════════════════════════════════════════════════════╗
║                    🎮 ROBLOX KEEPER STATUS                       ║
╠══════════════════════════════════════════════════════════════════╣
║ Status:           {stats['status']:40s}  ║
║ Uptime:           {uptime:40s}  ║
║ Total Clicks:     {stats['total_clicks']:40d}  ║
║ Total Screenshots: {stats['total_screenshots']:39d}  ║
║ Server Loads:     {stats['server_loads_detected']:40d}  ║
║ Crashes Detected: {stats['roblox_crashes']:40d}  ║
║ Errors Dismissed: {stats['error_dialogs_dismissed']:40d}  ║
║ Last Click:       {stats.get('last_click', 'Never'):40s}  ║
║ Last Screenshot:  {stats.get('last_screenshot') or 'Never':40s}  ║
║ Last Error Fixed: {last_error:40s}  ║
╚══════════════════════════════════════════════════════════════════╝
"""
    print(dashboard)

# Main
print("=" * 70)
print("🎮 ROBLOX AFK KEEPER - ENHANCED MONITORING")
print("=" * 70)
print(f"📁 Base folder: {BASE_DIR}")
print(f"🖱  Click interval: Every {CLICK_INTERVAL_MINUTES} minutes")
print(f"📸 Screenshot interval: Every hour")
print(f"🆗 Error dialog check: Every 15 seconds")
print(f"🔍 Monitoring: Crashes, Server Loading, Activity, Error Dialogs")
print(f"📝 Logs: {LOG_FILE}")
print(f"📊 Stats: {STATUS_FILE}")
print("=" * 70)
print()

# Initialize stats
stats['start_time'] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
log_message("🚀 Enhanced Roblox Keeper Started")

# Initial check
if not is_roblox_running():
    log_message("❌ Roblox is not running! Please start the game first.", "CRITICAL")
    print("\n❌ ERROR: Roblox is not running!")
    print("Please start Roblox and run this script again.")
    exit(1)

log_message("✓ Roblox is running")

# Initial actions
log_message("Performing initial click and screenshot...")
safe_click_roblox()
take_screenshot()

print_dashboard()

try:
    last_click_time = time.time()
    last_screenshot_time = time.time()
    last_status_check = time.time()
    last_dashboard_update = time.time()
    last_error_check = time.time()

    while True:
        current_time = time.time()

        # Check for error dialogs every 15 seconds
        if current_time - last_error_check >= 15:
            dismiss_error_dialogs()
            last_error_check = current_time

        # Check Roblox status every 30 seconds
        if current_time - last_status_check >= 30:
            if not monitor_roblox_status():
                # Roblox crashed, wait for user to restart
                print("\n⚠️  Waiting for Roblox to restart...")
                time.sleep(10)
                continue
            last_status_check = current_time

        # Check if it's time for screenshot (every hour)
        if current_time - last_screenshot_time >= SCREENSHOT_INTERVAL_SECONDS:
            log_message("📊 Hourly screenshot time!")
            take_screenshot()
            last_screenshot_time = current_time

        # Check if it's time to click (every 18 minutes)
        if current_time - last_click_time >= CLICK_INTERVAL_SECONDS:
            log_message("⏰ Time to keep active!")
            safe_click_roblox()
            last_click_time = current_time

        # Update dashboard every 5 minutes
        if current_time - last_dashboard_update >= 300:
            print("\033[2J\033[H")  # Clear screen
            print_dashboard()
            last_dashboard_update = current_time

        # Show countdown
        next_screenshot_in = int(SCREENSHOT_INTERVAL_SECONDS - (current_time - last_screenshot_time))
        next_click_in = int(CLICK_INTERVAL_SECONDS - (current_time - last_click_time))

        hrs_shot = next_screenshot_in // 3600
        mins_shot = (next_screenshot_in % 3600) // 60
        secs_shot = next_screenshot_in % 60

        mins_click = next_click_in // 60
        secs_click = next_click_in % 60

        print(f"\r⏳ Next screenshot: {hrs_shot}h {mins_shot}m {secs_shot}s | Next click: {mins_click}m {secs_click}s | Status: {stats['status']:10s}   ", end='', flush=True)

        time.sleep(1)

except KeyboardInterrupt:
    log_message("🛑 Keeper stopped by user")
    print("\n" + "=" * 70)
    print_dashboard()
    print("=" * 70)
    print(f"✓ Check logs: {LOG_FILE}")
    print(f"✓ Check stats: {STATUS_FILE}")
    print(f"✓ Check screenshots: {SCREENSHOT_DIR}")
    print("=" * 70)

except Exception as e:
    log_message(f"❌ Fatal error: {e}", "CRITICAL")
    stats['status'] = 'crashed'
    save_stats()
    print(f"\n❌ Fatal error: {e}")

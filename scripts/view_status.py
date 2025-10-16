#!/usr/bin/env python3
"""
View current status of Roblox Keeper
"""

import json
import os
from datetime import datetime

BASE_DIR = "/Users/giangeralcus/Desktop/RobloxKeeper"
STATUS_FILE = f"{BASE_DIR}/logs/status.json"

def view_status():
    if not os.path.exists(STATUS_FILE):
        print("❌ No status file found. Is the keeper running?")
        return

    with open(STATUS_FILE, 'r') as f:
        stats = json.load(f)

    uptime = ""
    if stats.get('start_time'):
        start = datetime.strptime(stats['start_time'], "%Y-%m-%d %H:%M:%S")
        delta = datetime.now() - start
        hours = delta.seconds // 3600
        minutes = (delta.seconds % 3600) // 60
        uptime = f"{delta.days}d {hours}h {minutes}m"

    print("""
╔══════════════════════════════════════════════════════════════════╗
║                    🎮 ROBLOX KEEPER STATUS                       ║
╠══════════════════════════════════════════════════════════════════╣""")
    print(f"║ Status:           {stats.get('status', 'unknown'):40s}  ║")
    print(f"║ Uptime:           {uptime:40s}  ║")
    print(f"║ Total Clicks:     {stats.get('total_clicks', 0):40d}  ║")
    print(f"║ Total Screenshots: {stats.get('total_screenshots', 0):39d}  ║")
    print(f"║ Server Loads:     {stats.get('server_loads_detected', 0):40d}  ║")
    print(f"║ Crashes Detected: {stats.get('roblox_crashes', 0):40d}  ║")
    print(f"║ Last Click:       {stats.get('last_click', 'Never'):40s}  ║")
    print(f"║ Last Screenshot:  {stats.get('last_screenshot', 'Never'):40s}  ║")
    print("╚══════════════════════════════════════════════════════════════════╝")

if __name__ == "__main__":
    view_status()

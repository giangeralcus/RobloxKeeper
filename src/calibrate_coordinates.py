#!/usr/bin/env python3
"""
Coordinate Calibration Tool
Click on screen to get exact coordinates for config
"""

import pyautogui
import pygetwindow as gw
import json
import os
from PIL import Image
import mss

def get_roblox_window():
    """Get Roblox window"""
    windows = gw.getWindowsWithTitle('Roblox')
    if windows:
        return windows[0]
    return None

def resize_roblox():
    """Resize Roblox to standard size"""
    window = get_roblox_window()
    if window:
        window.moveTo(100, 100)
        window.resizeTo(1280, 720)
        print(f"✓ Resized Roblox to 1280x720 at (100, 100)")
        return True
    print("❌ Roblox window not found!")
    return False

def take_screenshot():
    """Take screenshot of Roblox"""
    window = get_roblox_window()
    if not window:
        return None

    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    screenshot_path = os.path.join(base_dir, "screenshots", "calibration.png")

    with mss.mss() as sct:
        monitor = {
            "left": window.left,
            "top": window.top,
            "width": window.width,
            "height": window.height
        }
        screenshot = sct.grab(monitor)
        img = Image.frombytes('RGB', screenshot.size, screenshot.rgb)
        img.save(screenshot_path)

    print(f"📸 Screenshot saved: {screenshot_path}")
    return screenshot_path, window

def calibrate():
    """Interactive calibration"""
    print("=" * 70)
    print("🎯 COORDINATE CALIBRATION TOOL")
    print("=" * 70)
    print()

    # Step 1: Check Roblox
    print("Step 1: Checking for Roblox window...")
    if not resize_roblox():
        print("\nPlease start Roblox first!")
        return

    input("\nPress ENTER when Roblox home page is loaded...")

    # Step 2: Take screenshot
    print("\nStep 2: Taking screenshot...")
    result = take_screenshot()
    if not result:
        print("Failed to take screenshot!")
        return

    screenshot_path, window = result

    print("\n" + "=" * 70)
    print("CALIBRATION INSTRUCTIONS:")
    print("=" * 70)
    print()
    print("You will click 3 positions:")
    print("  1. Anime Vanguards game card")
    print("  2. Blue play button (after clicking game)")
    print("  3. Safe AFK position (center of game)")
    print()
    print("For each position:")
    print("  - Position your mouse over the target")
    print("  - Press ENTER")
    print("  - DON'T MOVE MOUSE until coordinates are captured")
    print()
    print("=" * 70)

    # Calibrate game card
    input("\n1. Position mouse over ANIME VANGUARDS game card, then press ENTER...")
    pos1 = pyautogui.position()
    game_x = pos1.x - window.left
    game_y = pos1.y - window.top
    print(f"   ✓ Game card: ({game_x}, {game_y})")

    # Calibrate play button
    print("\n   Now click the game card manually...")
    input("2. Position mouse over BLUE PLAY BUTTON, then press ENTER...")
    pos2 = pyautogui.position()
    play_x = pos2.x - window.left
    play_y = pos2.y - window.top
    print(f"   ✓ Play button: ({play_x}, {play_y})")

    # Calibrate AFK position
    print("\n   Close the game details page manually...")
    input("3. Position mouse at CENTER of screen (for AFK clicks), then press ENTER...")
    pos3 = pyautogui.position()
    afk_x = pos3.x - window.left
    afk_y = pos3.y - window.top
    print(f"   ✓ AFK position: ({afk_x}, {afk_y})")

    # Save coordinates
    config_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "config", "config.json")

    try:
        with open(config_path, 'r') as f:
            config = json.load(f)
    except:
        config = {}

    config['fixed_coordinates'] = {
        "game_card_click": {
            "x": game_x,
            "y": game_y,
            "description": "Anime Vanguards game card"
        },
        "play_button_click": {
            "x": play_x,
            "y": play_y,
            "description": "Blue play button"
        },
        "safe_afk_click": {
            "x": afk_x,
            "y": afk_y,
            "description": "Center for AFK prevention"
        }
    }

    with open(config_path, 'w') as f:
        json.dump(config, f, indent=2)

    print("\n" + "=" * 70)
    print("✅ CALIBRATION COMPLETE!")
    print("=" * 70)
    print()
    print("Saved coordinates:")
    print(f"  Game Card:   ({game_x}, {game_y})")
    print(f"  Play Button: ({play_x}, {play_y})")
    print(f"  AFK Position: ({afk_x}, {afk_y})")
    print()
    print(f"Config saved to: {config_path}")
    print()
    print("You can now use START_KEEPER.bat with these coordinates!")
    print("=" * 70)

if __name__ == "__main__":
    try:
        calibrate()
    except KeyboardInterrupt:
        print("\n\nCalibration cancelled.")
    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()

#!/usr/bin/env python3
"""
Test Script for Keeper Engine V2
Tests all 4 click methods individually

Run this with Roblox open to verify which methods work!
"""

import sys
import os
import time

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from keeper_engine_v2 import AnimeVanguardsKeeperV2, ClickMethod


def print_banner(text):
    """Print formatted banner"""
    print("\n" + "=" * 60)
    print(f"  {text}")
    print("=" * 60)


def test_method(keeper, method_name, method_func):
    """Test a single click method"""
    print(f"\n🧪 Testing: {method_name.upper()}")
    print("-" * 60)

    # Get window info
    window_rect = keeper.get_window_rect()
    if not window_rect:
        print("❌ Cannot get window info")
        return False

    # Center coordinates
    x = window_rect['width'] // 2
    y = window_rect['height'] // 2

    print(f"   Target: ({x}, {y}) - center of window")
    print(f"   Method: {method_name}")

    # Try the click
    try:
        start_time = time.time()
        success = method_func(x, y, double=True)
        elapsed = (time.time() - start_time) * 1000

        if success:
            print(f"✅ SUCCESS - {method_name} worked!")
            print(f"   Time: {elapsed:.1f}ms")
            print(f"   Watch Roblox - did you see the click?")
            return True
        else:
            print(f"❌ FAILED - {method_name} returned False")
            return False

    except Exception as e:
        print(f"❌ EXCEPTION - {method_name} crashed: {e}")
        return False


def main():
    print_banner("🎮 KEEPER ENGINE V2 - METHOD TESTER")

    print("\nThis script will test all 4 click methods:")
    print("  1. PostMessage (fastest, async)")
    print("  2. SendMessage (reliable, sync)")
    print("  3. DirectInput (game-compatible)")
    print("  4. PyAutoGUI (fallback)")
    print("\n⚠️  Make sure Roblox is RUNNING and you're in-game!")

    input("\nPress ENTER to start testing...")

    # Initialize keeper
    base_dir = os.path.dirname(os.path.abspath(__file__))
    config_path = os.path.join(base_dir, "config", "config_v2.json")

    print("\n📋 Initializing Keeper V2...")
    keeper = AnimeVanguardsKeeperV2(base_dir, config_path)

    # Check if Roblox is running
    if not keeper.is_roblox_running():
        print("\n❌ ERROR: Roblox is not running!")
        print("   Please start Roblox and try again.")
        input("\nPress ENTER to exit...")
        return

    print("✅ Roblox is running")

    # Get window info
    window_rect = keeper.get_window_rect()
    if window_rect:
        print(f"✅ Window found: {window_rect['width']}x{window_rect['height']}")
    else:
        print("❌ Cannot find Roblox window")
        input("\nPress ENTER to exit...")
        return

    # Test each method
    results = {}

    print_banner("TEST 1/4: PostMessage")
    results['postmessage'] = test_method(keeper, 'postmessage', keeper._click_postmessage)
    time.sleep(2)

    print_banner("TEST 2/4: SendMessage")
    results['sendmessage'] = test_method(keeper, 'sendmessage', keeper._click_sendmessage)
    time.sleep(2)

    print_banner("TEST 3/4: DirectInput")
    results['directinput'] = test_method(keeper, 'directinput', keeper._click_directinput)
    time.sleep(2)

    print_banner("TEST 4/4: PyAutoGUI")
    results['pyautogui'] = test_method(keeper, 'pyautogui', keeper._click_pyautogui)
    time.sleep(2)

    # Summary
    print_banner("📊 TEST RESULTS SUMMARY")

    print("\nMethod Results:")
    for method, success in results.items():
        status = "✅ WORKS" if success else "❌ FAILED"
        print(f"  {method:15s}: {status}")

    # Recommendations
    print("\n💡 Recommendations:")

    working_methods = [m for m, s in results.items() if s]

    if results.get('postmessage'):
        print("  🥇 Use PostMessage (fastest, true background)")
    elif results.get('sendmessage'):
        print("  🥈 Use SendMessage (reliable, true background)")
    elif results.get('directinput'):
        print("  🥉 Use DirectInput (game-compatible)")
    elif results.get('pyautogui'):
        print("  ⚠️  Only PyAutoGUI works (requires window activation)")
    else:
        print("  ❌ No methods worked! Check Roblox is responsive.")

    if working_methods:
        print(f"\n✅ {len(working_methods)}/4 methods work!")
        print(f"   Your config will use: {working_methods}")
    else:
        print("\n❌ No methods worked!")
        print("   Troubleshooting:")
        print("   1. Make sure you're IN the game (not menu)")
        print("   2. Try clicking manually to verify Roblox responds")
        print("   3. Check Windows permissions")

    # Test unified method
    print_banner("🎯 TESTING UNIFIED CLICK SYSTEM")

    print("\nThe unified system tries all methods in order until one works.")
    print("This is what the actual keeper uses.\n")

    input("Press ENTER to test unified click system...")

    success = keeper.safe_click_roblox()

    if success:
        print("\n✅ UNIFIED SYSTEM WORKS!")
        print("   The keeper will work correctly.")
        print(f"\n   Method used: {list(keeper.stats['method_stats'].keys())[0]}")
        print(f"   Statistics: {keeper.stats['method_stats']}")
    else:
        print("\n❌ UNIFIED SYSTEM FAILED!")
        print("   All methods failed. Check the logs above.")

    print_banner("TEST COMPLETE")

    print("\n📁 Files to check:")
    print(f"   Config: {config_path}")
    print("   Engine: src/keeper_engine_v2.py")

    print("\n🚀 Next steps:")
    if working_methods:
        print("   1. Update config.json with your preferred method")
        print("   2. Run START_KEEPER_V2.bat")
        print("   3. Enjoy true background mode!")
    else:
        print("   1. Check Roblox is running and responsive")
        print("   2. Try running as Administrator")
        print("   3. Check Windows security settings")

    input("\nPress ENTER to exit...")


if __name__ == "__main__":
    main()

#!/usr/bin/env python3
"""
Anime Vanguards Keeper Engine V2 - Industry-Grade Edition

Based on research from:
- MyBot-MBR background mode analysis
- Game automation best practices (2024)
- PyDirectInput for game compatibility
- Windows API optimization

Key Improvements:
1. Multi-method click system (4 fallback methods)
2. PyDirectInput for better game recognition
3. PostMessage for faster async clicks
4. Humanization layer to avoid detection
5. Enhanced error handling and logging
"""

import os
import json
import time
import random
import psutil
import threading
from datetime import datetime
from typing import Optional, Tuple, Callable
import ctypes
from ctypes import wintypes

# Standard imports
try:
    import pygetwindow as gw
except ImportError:
    gw = None

try:
    import pyautogui
except ImportError:
    pyautogui = None

try:
    import PyDirectInput
except ImportError:
    PyDirectInput = None

try:
    import win32gui
    import win32ui
    import win32con
    from PIL import Image
except ImportError:
    win32gui = None


class ClickMethod:
    """Enumeration of available click methods"""
    POST_MESSAGE = "postmessage"      # Fastest, async
    SEND_MESSAGE = "sendmessage"      # Reliable, sync
    DIRECT_INPUT = "directinput"      # Game-compatible
    PYAUTOGUI = "pyautogui"           # Fallback, requires activation


class AnimeVanguardsKeeperV2:
    """
    Industry-grade AFK keeper with multi-method fallback system
    """

    def __init__(self, base_dir: str, config_path: str, log_callback: Optional[Callable] = None):
        """Initialize keeper with configuration"""
        self.base_dir = base_dir
        self.config_path = config_path
        self.log_callback = log_callback

        # Load configuration
        self.config = self.load_config()

        # Statistics
        self.stats = {
            'status': 'stopped',
            'total_clicks': 0,
            'method_stats': {
                'postmessage': 0,
                'sendmessage': 0,
                'directinput': 0,
                'pyautogui': 0
            },
            'method_failures': {
                'postmessage': 0,
                'sendmessage': 0,
                'directinput': 0,
                'pyautogui': 0
            },
            'last_click': 'Never',
            'start_time': None,
            'roblox_crashes': 0
        }

        # Threading
        self.running = False
        self.paused = False
        self.keeper_thread = None

        # Windows API setup
        self.user32 = ctypes.windll.user32
        self.WM_LBUTTONDOWN = 0x0201
        self.WM_LBUTTONUP = 0x0202
        self.WM_LBUTTONDBLCLK = 0x0203

        # Click method priority order
        self.click_methods = self._get_click_method_priority()

        # Humanization settings
        self.humanization = self.config.get('humanization', {})
        self.position_variance = self.humanization.get('position_variance', 10)
        self.timing_variance = self.humanization.get('timing_variance', 0.05)
        self.double_click_chance = self.humanization.get('double_click_chance', 0.3)

        self.log_message("=" * 80)
        self.log_message("🎮 ANIME VANGUARDS KEEPER V2 - INDUSTRY GRADE")
        self.log_message("=" * 80)
        self.log_message(f"Available click methods: {', '.join([m for m, _ in self.click_methods])}")
        self.log_message(f"Primary method: {self.click_methods[0][0]}")
        self.log_message(f"Humanization: {'Enabled' if self.config.get('humanization_enabled', True) else 'Disabled'}")

    def _get_click_method_priority(self) -> list:
        """
        Get click method priority based on configuration and availability
        Returns list of (method_name, method_function) tuples
        """
        methods = []
        user_preference = self.config.get('click_method_priority', [])

        # Default priority if not configured
        default_priority = [
            ClickMethod.POST_MESSAGE,   # Fastest
            ClickMethod.SEND_MESSAGE,   # Reliable
            ClickMethod.DIRECT_INPUT,   # Game-compatible
            ClickMethod.PYAUTOGUI       # Always works
        ]

        priority = user_preference if user_preference else default_priority

        # Build available methods list
        for method in priority:
            if method == ClickMethod.POST_MESSAGE:
                methods.append((ClickMethod.POST_MESSAGE, self._click_postmessage))
            elif method == ClickMethod.SEND_MESSAGE:
                methods.append((ClickMethod.SEND_MESSAGE, self._click_sendmessage))
            elif method == ClickMethod.DIRECT_INPUT and PyDirectInput:
                methods.append((ClickMethod.DIRECT_INPUT, self._click_directinput))
            elif method == ClickMethod.PYAUTOGUI and pyautogui:
                methods.append((ClickMethod.PYAUTOGUI, self._click_pyautogui))

        return methods

    def load_config(self) -> dict:
        """Load configuration from JSON file"""
        try:
            with open(self.config_path, 'r') as f:
                return json.load(f)
        except FileNotFoundError:
            self.log_message(f"Config not found: {self.config_path}", "ERROR")
            return {}
        except json.JSONDecodeError as e:
            self.log_message(f"Invalid JSON in config: {e}", "ERROR")
            return {}

    def log_message(self, message: str, level: str = "INFO"):
        """Log message to callback"""
        if self.log_callback:
            self.log_callback(message)
        else:
            timestamp = datetime.now().strftime("%H:%M:%S")
            print(f"[{timestamp}] [{level}] {message}")

    def is_roblox_running(self) -> bool:
        """Check if Roblox process is running"""
        process_name = self.config.get('roblox_process_name', 'RobloxPlayerBeta.exe')
        for proc in psutil.process_iter(['name']):
            try:
                if proc.info['name'] == process_name:
                    return True
            except (psutil.NoSuchProcess, psutil.AccessDenied):
                pass
        return False

    def get_window_handle(self) -> Optional[int]:
        """Get Roblox window handle"""
        if not win32gui:
            return None

        def enum_callback(hwnd, results):
            if win32gui.IsWindowVisible(hwnd):
                title = win32gui.GetWindowText(hwnd)
                if "Roblox" in title:
                    results.append(hwnd)

        handles = []
        win32gui.EnumWindows(enum_callback, handles)
        return handles[0] if handles else None

    def get_window_rect(self) -> Optional[dict]:
        """Get Roblox window dimensions"""
        if not win32gui:
            return None

        hwnd = self.get_window_handle()
        if not hwnd:
            return None

        try:
            rect = win32gui.GetClientRect(hwnd)
            pos = win32gui.ClientToScreen(hwnd, (0, 0))
            return {
                'x': pos[0],
                'y': pos[1],
                'width': rect[2],
                'height': rect[3]
            }
        except Exception as e:
            self.log_message(f"Failed to get window rect: {e}", "ERROR")
            return None

    def apply_humanization(self, x: int, y: int) -> Tuple[int, int, float]:
        """
        Apply human-like randomness to click position and timing

        Returns: (adjusted_x, adjusted_y, delay)
        """
        if not self.config.get('humanization_enabled', True):
            return x, y, 0.05

        # Random position variance
        variance = self.position_variance
        x_adjusted = x + random.randint(-variance, variance)
        y_adjusted = y + random.randint(-variance, variance)

        # Random timing variance
        base_delay = 0.05
        delay = base_delay + random.uniform(-self.timing_variance, self.timing_variance)
        delay = max(0.01, delay)  # Ensure positive

        return x_adjusted, y_adjusted, delay

    def should_double_click(self) -> bool:
        """Randomly decide if should double-click (humanization)"""
        if not self.config.get('humanization_enabled', True):
            return True  # Default behavior

        return random.random() < self.double_click_chance

    # ========================================
    # CLICK METHOD 1: PostMessage (Fastest)
    # ========================================

    def _click_postmessage(self, x: int, y: int, double: bool = False) -> bool:
        """
        Click using PostMessage - Async, fastest method
        Works in background without activation
        """
        hwnd = self.get_window_handle()
        if not hwnd:
            return False

        try:
            lParam = (y << 16) | (x & 0xFFFF)

            if double:
                # Double-click sequence
                self.user32.PostMessageW(hwnd, self.WM_LBUTTONDBLCLK, 0x0001, lParam)
                time.sleep(0.05)
                self.user32.PostMessageW(hwnd, self.WM_LBUTTONUP, 0x0000, lParam)
            else:
                # Single click
                self.user32.PostMessageW(hwnd, self.WM_LBUTTONDOWN, 0x0001, lParam)
                time.sleep(0.05)
                self.user32.PostMessageW(hwnd, self.WM_LBUTTONUP, 0x0000, lParam)

            return True

        except Exception as e:
            self.log_message(f"PostMessage click failed: {e}", "WARN")
            return False

    # ========================================
    # CLICK METHOD 2: SendMessage (Reliable)
    # ========================================

    def _click_sendmessage(self, x: int, y: int, double: bool = False) -> bool:
        """
        Click using SendMessage - Synchronous, reliable method
        Works in background without activation
        """
        hwnd = self.get_window_handle()
        if not hwnd:
            return False

        try:
            lParam = (y << 16) | (x & 0xFFFF)

            if double:
                # Double-click sequence
                self.user32.SendMessageW(hwnd, self.WM_LBUTTONDBLCLK, 0x0001, lParam)
                time.sleep(0.05)
                self.user32.SendMessageW(hwnd, self.WM_LBUTTONUP, 0x0000, lParam)
            else:
                # Single click
                self.user32.SendMessageW(hwnd, self.WM_LBUTTONDOWN, 0x0001, lParam)
                time.sleep(0.05)
                self.user32.SendMessageW(hwnd, self.WM_LBUTTONUP, 0x0000, lParam)

            return True

        except Exception as e:
            self.log_message(f"SendMessage click failed: {e}", "WARN")
            return False

    # ========================================
    # CLICK METHOD 3: DirectInput (Game-Compatible)
    # ========================================

    def _click_directinput(self, x: int, y: int, double: bool = False) -> bool:
        """
        Click using PyDirectInput - Better game recognition
        May require brief activation
        """
        if not PyDirectInput:
            return False

        try:
            # Get absolute screen coordinates
            window_rect = self.get_window_rect()
            if not window_rect:
                return False

            abs_x = window_rect['x'] + x
            abs_y = window_rect['y'] + y

            # Move and click using DirectInput
            PyDirectInput.moveTo(abs_x, abs_y)
            time.sleep(0.05)

            if double:
                PyDirectInput.click(abs_x, abs_y)
                time.sleep(0.05)
                PyDirectInput.click(abs_x, abs_y)
            else:
                PyDirectInput.click(abs_x, abs_y)

            return True

        except Exception as e:
            self.log_message(f"DirectInput click failed: {e}", "WARN")
            return False

    # ========================================
    # CLICK METHOD 4: PyAutoGUI (Fallback)
    # ========================================

    def _click_pyautogui(self, x: int, y: int, double: bool = False) -> bool:
        """
        Click using PyAutoGUI - Requires window activation
        This is the current method (fallback only)
        """
        if not pyautogui or not gw:
            return False

        try:
            # Save current window
            current_window = None
            try:
                current_window = gw.getActiveWindow()
            except:
                pass

            # Activate Roblox
            windows = gw.getWindowsWithTitle("Roblox")
            if not windows:
                return False

            roblox_window = windows[0]
            roblox_window.activate()
            time.sleep(0.3)

            # Get absolute coordinates
            window_rect = self.get_window_rect()
            if not window_rect:
                return False

            abs_x = window_rect['x'] + x
            abs_y = window_rect['y'] + y

            # Click
            if double:
                pyautogui.doubleClick(abs_x, abs_y)
            else:
                pyautogui.click(abs_x, abs_y)

            # Restore previous window
            time.sleep(0.2)
            if current_window:
                try:
                    current_window.activate()
                except:
                    pass

            return True

        except Exception as e:
            self.log_message(f"PyAutoGUI click failed: {e}", "WARN")
            return False

    # ========================================
    # UNIFIED CLICK INTERFACE
    # ========================================

    def safe_click_roblox(self) -> bool:
        """
        Unified click method with multi-method fallback system
        Tries all available methods in priority order
        """
        # Get click coordinates
        use_fixed = self.config.get('use_fixed_coordinates', True)
        window_rect = self.get_window_rect()

        if not window_rect:
            self.log_message("Could not get window info", "WARN")
            return False

        # Get base coordinates
        if use_fixed:
            fixed_coords = self.config.get('fixed_coordinates', {})
            afk_click = fixed_coords.get('safe_afk_click', {})
            x = afk_click.get('x', window_rect['width'] // 2)
            y = afk_click.get('y', window_rect['height'] // 2)
        else:
            x = window_rect['width'] // 2
            y = window_rect['height'] // 2

        # Apply humanization
        x, y, delay = self.apply_humanization(x, y)
        double_click = self.should_double_click()

        self.log_message(f"🎯 Attempting click at ({x}, {y}), double={double_click}")
        self.log_message(f"   Humanization: ±{self.position_variance}px, delay={delay:.3f}s")

        # Try each method in priority order
        for method_name, method_func in self.click_methods:
            try:
                start_time = time.time()
                success = method_func(x, y, double_click)
                elapsed = (time.time() - start_time) * 1000  # ms

                if success:
                    # Update statistics
                    self.stats['total_clicks'] += 1
                    self.stats['method_stats'][method_name] += 1
                    self.stats['last_click'] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                    self.stats['status'] = 'active'

                    self.log_message(f"✅ Click SUCCESS using {method_name.upper()}")
                    self.log_message(f"   Position: ({x}, {y}), Time: {elapsed:.1f}ms")
                    self.log_message(f"   Total clicks: {self.stats['total_clicks']}")
                    self.log_message(f"   Method stats: {self.stats['method_stats']}")

                    # Save stats
                    self.save_stats()

                    return True
                else:
                    # Method failed, try next
                    self.stats['method_failures'][method_name] += 1
                    self.log_message(f"⚠️  {method_name.upper()} failed, trying next method...")

            except Exception as e:
                self.stats['method_failures'][method_name] += 1
                self.log_message(f"❌ {method_name.upper()} exception: {e}", "ERROR")
                continue

        # All methods failed
        self.log_message("❌ ALL CLICK METHODS FAILED!", "ERROR")
        self.log_message(f"   Failures: {self.stats['method_failures']}")
        return False

    def save_stats(self):
        """Save statistics to file"""
        stats_file = os.path.join(self.base_dir, "stats", "keeper_stats.json")
        os.makedirs(os.path.dirname(stats_file), exist_ok=True)

        try:
            with open(stats_file, 'w') as f:
                json.dump(self.stats, f, indent=2)
        except Exception as e:
            self.log_message(f"Failed to save stats: {e}", "ERROR")

    def get_stats(self) -> dict:
        """Get current statistics"""
        return self.stats.copy()

    # ========================================
    # KEEPER MAIN LOOP
    # ========================================

    def keeper_loop(self):
        """Main keeper loop"""
        self.log_message("🚀 Keeper loop started")
        self.stats['status'] = 'running'
        self.stats['start_time'] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        click_interval = self.config.get('click_interval_minutes', 18) * 60  # Convert to seconds

        while self.running:
            try:
                # Check if paused
                if self.paused:
                    time.sleep(1)
                    continue

                # Check if Roblox is still running
                if not self.is_roblox_running():
                    self.log_message("⚠️  Roblox not running!", "WARN")
                    self.stats['status'] = 'warning'
                    time.sleep(5)
                    continue

                # Perform AFK prevention click
                self.log_message(f"⏰ Click interval reached ({click_interval}s)")
                success = self.safe_click_roblox()

                if success:
                    self.log_message(f"✅ AFK prevention successful")
                else:
                    self.log_message(f"❌ AFK prevention failed", "ERROR")

                # Wait for next interval
                self.log_message(f"⏳ Next click in {click_interval} seconds ({click_interval/60:.1f} minutes)")
                time.sleep(click_interval)

            except Exception as e:
                self.log_message(f"Error in keeper loop: {e}", "ERROR")
                time.sleep(10)

        self.log_message("🛑 Keeper loop stopped")
        self.stats['status'] = 'stopped'

    def start(self) -> bool:
        """Start the keeper"""
        if self.running:
            self.log_message("Keeper already running", "WARN")
            return False

        if not self.is_roblox_running():
            self.log_message("Roblox is not running!", "ERROR")
            return False

        self.running = True
        self.keeper_thread = threading.Thread(target=self.keeper_loop, daemon=True)
        self.keeper_thread.start()

        return True

    def pause(self) -> bool:
        """Toggle pause state"""
        self.paused = not self.paused
        self.stats['status'] = 'paused' if self.paused else 'running'
        return self.paused

    def stop(self) -> bool:
        """Stop the keeper"""
        if not self.running:
            return False

        self.running = False
        if self.keeper_thread:
            self.keeper_thread.join(timeout=5)

        self.stats['status'] = 'stopped'
        return True

#!/usr/bin/env python3
"""
Anime Vanguards Keeper - Windows Edition
Advanced monitoring with GUI, crash detection, and auto-relaunch
"""

import time
import pyautogui
import psutil
from datetime import datetime
import os
import json
import threading
import mss
import cv2
import numpy as np
from PIL import Image
import pygetwindow as gw

class AnimeVanguardsKeeper:
    def __init__(self, base_dir, config_path, log_callback=None):
        self.base_dir = base_dir
        self.config = self.load_config(config_path)
        self.log_callback = log_callback

        # Paths
        self.log_file = os.path.join(base_dir, "logs", "keeper.log")
        self.status_file = os.path.join(base_dir, "logs", "status.json")
        self.screenshot_dir = os.path.join(base_dir, "screenshots")
        self.stats_log = os.path.join(base_dir, "logs", "stats.log")

        # State
        self.running = False
        self.paused = False
        self.monitor_thread = None

        # Stats
        self.stats = {
            'start_time': None,
            'total_clicks': 0,
            'total_screenshots': 0,
            'roblox_crashes': 0,
            'server_loads_detected': 0,
            'error_dialogs_dismissed': 0,
            'last_click': None,
            'last_screenshot': None,
            'last_error_dismissed': None,
            'status': 'stopped'
        }

        # Ensure directories exist
        os.makedirs(os.path.dirname(self.log_file), exist_ok=True)
        os.makedirs(self.screenshot_dir, exist_ok=True)

    def load_config(self, config_path):
        """Load configuration from JSON file"""
        try:
            with open(config_path, 'r') as f:
                return json.load(f)
        except Exception as e:
            print(f"Error loading config: {e}")
            return self.get_default_config()

    def get_default_config(self):
        """Return default configuration"""
        return {
            "game_name": "Anime Vanguards",
            "click_interval_minutes": 18,
            "screenshot_interval_seconds": 3600,
            "error_check_interval_seconds": 15,
            "status_check_interval_seconds": 30,
            "roblox_process_name": "RobloxPlayerBeta.exe",
            "auto_relaunch": True,
            "game_load_wait_seconds": 15
        }

    def log_message(self, message, level="INFO"):
        """Log message to file and callback"""
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        log_entry = f"[{timestamp}] [{level}] {message}"

        # Write to file
        try:
            with open(self.log_file, 'a', encoding='utf-8') as f:
                f.write(log_entry + "\n")
        except Exception as e:
            print(f"Error writing to log: {e}")

        # Send to GUI callback
        if self.log_callback:
            self.log_callback(log_entry)

    def save_stats(self):
        """Save current stats to JSON"""
        try:
            with open(self.status_file, 'w') as f:
                json.dump(self.stats, f, indent=2)
        except Exception as e:
            self.log_message(f"Failed to save stats: {e}", "ERROR")

    def log_stats(self, event_type, details=""):
        """Log stats events"""
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        entry = f"[{timestamp}] {event_type}: {details}\n"
        try:
            with open(self.stats_log, 'a', encoding='utf-8') as f:
                f.write(entry)
        except Exception as e:
            print(f"Error writing stats: {e}")

    def is_roblox_running(self):
        """Check if Roblox is running on Windows"""
        try:
            process_name = self.config.get('roblox_process_name', 'RobloxPlayerBeta.exe')
            for proc in psutil.process_iter(['name']):
                if proc.info['name'] == process_name:
                    return True
            return False
        except Exception as e:
            self.log_message(f"Error checking Roblox status: {e}", "ERROR")
            return False

    def get_roblox_window(self):
        """Get Roblox window using pygetwindow"""
        try:
            windows = gw.getWindowsWithTitle('Roblox')
            if windows:
                return windows[0]
            return None
        except Exception as e:
            self.log_message(f"Error getting Roblox window: {e}", "WARN")
            return None

    def activate_roblox(self):
        """Bring Roblox window to front"""
        try:
            window = self.get_roblox_window()
            if window:
                if window.isMinimized:
                    window.restore()
                window.activate()
                time.sleep(0.5)
                return True
            return False
        except Exception as e:
            self.log_message(f"Error activating Roblox: {e}", "ERROR")
            return False

    def get_window_rect(self):
        """Get Roblox window position and size"""
        try:
            window = self.get_roblox_window()
            if window:
                return {
                    'x': window.left,
                    'y': window.top,
                    'width': window.width,
                    'height': window.height
                }
            return None
        except Exception as e:
            self.log_message(f"Error getting window rect: {e}", "WARN")
            return None

    def safe_click_roblox(self):
        """Click safely in the center area of Roblox window"""
        window_info = self.get_window_rect()
        if not window_info:
            self.log_message("Could not get window info for clicking", "WARN")
            self.stats['status'] = 'warning'
            return False

        # Click in the center of the window (safe area)
        center_x = window_info['x'] + (window_info['width'] // 2)
        center_y = window_info['y'] + (window_info['height'] // 2)

        # Activate window first
        if not self.activate_roblox():
            self.stats['status'] = 'warning'
            return False

        # Double-click in center
        pyautogui.doubleClick(center_x, center_y)

        self.stats['total_clicks'] += 1
        self.stats['last_click'] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.stats['status'] = 'active'

        self.log_message(f"✓ Double-clicked at center: ({center_x}, {center_y})")
        self.log_stats("CLICK", f"Position: ({center_x}, {center_y}), Total: {self.stats['total_clicks']}")
        self.save_stats()

        return True

    def take_screenshot(self):
        """Take a screenshot using mss"""
        try:
            # Activate Roblox first
            self.activate_roblox()
            time.sleep(0.3)

            # Get window info
            window_info = self.get_window_rect()
            if not window_info:
                self.log_message("Could not get window for screenshot", "WARN")
                return False

            # Take screenshot
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = os.path.join(self.screenshot_dir, f"roblox_{timestamp}.png")

            with mss.mss() as sct:
                monitor = {
                    "left": window_info['x'],
                    "top": window_info['y'],
                    "width": window_info['width'],
                    "height": window_info['height']
                }
                screenshot = sct.grab(monitor)
                mss.tools.to_png(screenshot.rgb, screenshot.size, output=filename)

            self.stats['total_screenshots'] += 1
            self.stats['last_screenshot'] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

            self.log_message(f"📸 Screenshot saved: {filename}")
            self.log_stats("SCREENSHOT", f"File: {filename}, Total: {self.stats['total_screenshots']}")
            self.save_stats()

            return True
        except Exception as e:
            self.log_message(f"Screenshot failed: {e}", "ERROR")
            self.stats['status'] = 'error'
            self.save_stats()
            return False

    def dismiss_error_dialogs(self):
        """Detect and dismiss Roblox error dialogs"""
        try:
            window_info = self.get_window_rect()
            if not window_info:
                return False

            self.activate_roblox()
            time.sleep(0.2)

            center_x = window_info['x'] + (window_info['width'] // 2)
            center_y = window_info['y'] + (window_info['height'] // 2)

            # Try clicking potential OK button locations
            ok_button_locations = [
                (center_x, center_y + 50),
                (center_x, center_y + 70),
                (center_x, center_y + 90),
                (center_x - 50, center_y + 60),
                (center_x + 50, center_y + 60),
            ]

            for x, y in ok_button_locations:
                pyautogui.click(x, y)
                time.sleep(0.1)

            self.stats['error_dialogs_dismissed'] += 1
            self.stats['last_error_dismissed'] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

            self.log_message("🆗 Attempted to dismiss error dialogs", "INFO")
            self.log_stats("ERROR_DIALOG_DISMISSED", f"Total dismissed: {self.stats['error_dialogs_dismissed']}")
            self.save_stats()

            return True
        except Exception as e:
            self.log_message(f"Error dismissing dialogs: {e}", "WARN")
            return False

    def launch_roblox(self):
        """Launch Roblox application on Windows"""
        try:
            self.log_message("🚀 Launching Roblox...", "INFO")
            # Try to launch from Start Menu or default location
            import subprocess
            subprocess.Popen('start roblox:', shell=True)
            return True
        except Exception as e:
            self.log_message(f"Failed to launch Roblox: {e}", "ERROR")
            return False

    def find_and_click_game(self, game_name):
        """Find and click game using OCR text recognition"""
        try:
            self.log_message(f"🔍 Searching for '{game_name}' using OCR...", "INFO")

            # Wait for Roblox to load
            wait_time = self.config.get('game_load_wait_seconds', 15)
            for i in range(wait_time, 0, -1):
                time.sleep(1)
                if self.log_callback:
                    self.log_callback(f"⏳ Waiting for Roblox to load... {i}s")

            # Activate Roblox
            self.activate_roblox()
            time.sleep(1)

            window_info = self.get_window_rect()
            if not window_info:
                self.log_message("Could not get Roblox window info", "ERROR")
                return False

            # Take screenshot for OCR analysis
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            screenshot_path = os.path.join(self.screenshot_dir, f"game_search_{timestamp}.png")

            with mss.mss() as sct:
                monitor = {
                    "left": window_info['x'],
                    "top": window_info['y'],
                    "width": window_info['width'],
                    "height": window_info['height']
                }
                screenshot = sct.grab(monitor)
                img = Image.frombytes('RGB', screenshot.size, screenshot.rgb)
                img.save(screenshot_path)

            self.log_message(f"📸 Captured search screen: {screenshot_path}", "INFO")

            # Try OCR to find game text
            game_location = self.find_text_in_image(screenshot_path, game_name, window_info)

            if game_location:
                click_x, click_y = game_location
                self.log_message(f"✓ Found '{game_name}' at: ({click_x}, {click_y})", "INFO")
                pyautogui.click(click_x, click_y)
                time.sleep(1.5)

                # Now find and click the blue play button
                return self.click_play_button(window_info)
            else:
                self.log_message(f"⚠️  Could not find '{game_name}' via OCR, trying pattern matching...", "WARN")

                # Fallback: Try to find by looking for game card pattern
                return self.find_game_by_pattern(screenshot_path, window_info)

        except Exception as e:
            self.log_message(f"Error finding/clicking game: {e}", "ERROR")
            return False

    def find_text_in_image(self, image_path, search_text, window_info):
        """Use multiple detection methods to find the game with voting system"""
        try:
            img = cv2.imread(image_path)

            detection_votes = []

            # Method 1: Look for star rating pattern (⭐ 8.5)
            star_location = self.detect_star_rating(img)
            if star_location:
                detection_votes.append(('star_rating', star_location))
                self.log_message(f"✅ Method 1: Found star rating at {star_location}", "INFO")

            # Method 2: Detect purple/blue gradient text (ANIME VANGUARDS title)
            gradient_location = self.detect_gradient_text(img)
            if gradient_location:
                detection_votes.append(('gradient_text', gradient_location))
                self.log_message(f"✅ Method 2: Found gradient text at {gradient_location}", "INFO")

            # Method 3: Green dragon artwork detection (improved)
            dragon_location = self.detect_green_dragon(img)
            if dragon_location:
                detection_votes.append(('green_dragon', dragon_location))
                self.log_message(f"✅ Method 3: Found green dragon at {dragon_location}", "INFO")

            # Method 4: Try OCR if available
            try:
                import pytesseract
                ocr_location = self.detect_with_ocr(img, search_text)
                if ocr_location:
                    detection_votes.append(('ocr', ocr_location))
                    self.log_message(f"✅ Method 4: OCR found text at {ocr_location}", "INFO")
            except:
                pass

            # Voting: Use the most common location
            if detection_votes:
                # Average all detected locations
                avg_x = sum(loc[0] for _, loc in detection_votes) // len(detection_votes)
                avg_y = sum(loc[1] for _, loc in detection_votes) // len(detection_votes)

                final_x = window_info['x'] + avg_x
                final_y = window_info['y'] + avg_y

                self.log_message(f"🎯 VOTING RESULT: {len(detection_votes)} methods agree!", "INFO")
                self.log_message(f"📍 Final location: ({final_x}, {final_y})", "INFO")

                return (final_x, final_y)

            return None

        except Exception as e:
            self.log_message(f"Multi-detection error: {e}", "WARN")
            return None

    def detect_star_rating(self, img):
        """Detect the ⭐ 8.5 rating badge"""
        try:
            # Convert to HSV
            hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

            # Yellow color range for star
            lower_yellow = np.array([20, 100, 100])
            upper_yellow = np.array([30, 255, 255])

            mask = cv2.inRange(hsv, lower_yellow, upper_yellow)

            contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

            if contours:
                # Find star-shaped contours (small area in top-left of game card)
                for contour in contours:
                    area = cv2.contourArea(contour)
                    if 50 < area < 500:  # Star is small
                        M = cv2.moments(contour)
                        if M["m00"] != 0:
                            cx = int(M["m10"] / M["m00"])
                            cy = int(M["m01"] / M["m00"])
                            # Game card is below and to the right of star
                            return (cx + 50, cy + 80)

            return None
        except:
            return None

    def detect_gradient_text(self, img):
        """Detect purple/blue gradient text (ANIME VANGUARDS title)"""
        try:
            hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

            # Purple/blue color range
            lower_purple = np.array([120, 50, 50])
            upper_purple = np.array([150, 255, 255])

            mask = cv2.inRange(hsv, lower_purple, upper_purple)

            # Find large text areas
            contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

            if contours:
                # Find largest purple area (title text)
                large_contours = [c for c in contours if cv2.contourArea(c) > 200]

                if large_contours:
                    largest = max(large_contours, key=cv2.contourArea)
                    M = cv2.moments(largest)
                    if M["m00"] != 0:
                        cx = int(M["m10"] / M["m00"])
                        cy = int(M["m01"] / M["m00"])
                        return (cx, cy + 30)  # Click slightly below text

            return None
        except:
            return None

    def detect_green_dragon(self, img):
        """Enhanced green dragon artwork detection"""
        try:
            hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

            # Multiple green ranges for better detection
            masks = []

            # Bright green
            lower_green1 = np.array([35, 80, 80])
            upper_green1 = np.array([85, 255, 255])
            masks.append(cv2.inRange(hsv, lower_green1, upper_green1))

            # Dark green
            lower_green2 = np.array([35, 40, 40])
            upper_green2 = np.array([85, 255, 150])
            masks.append(cv2.inRange(hsv, lower_green2, upper_green2))

            # Combine masks
            combined_mask = masks[0]
            for mask in masks[1:]:
                combined_mask = cv2.bitwise_or(combined_mask, mask)

            # Find large green areas (dragon artwork)
            contours, _ = cv2.findContours(combined_mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

            if contours:
                # Find largest green area
                large_contours = [c for c in contours if cv2.contourArea(c) > 1000]

                if large_contours:
                    largest = max(large_contours, key=cv2.contourArea)
                    M = cv2.moments(largest)
                    if M["m00"] != 0:
                        cx = int(M["m10"] / M["m00"])
                        cy = int(M["m01"] / M["m00"])
                        return (cx, cy)

            return None
        except:
            return None

    def detect_with_ocr(self, img, search_text):
        """OCR detection if pytesseract is available"""
        try:
            import pytesseract

            gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

            # Enhance contrast for better OCR
            gray = cv2.equalizeHist(gray)

            data = pytesseract.image_to_data(gray, output_type=pytesseract.Output.DICT)

            search_words = search_text.upper().split()

            for i, text in enumerate(data['text']):
                if text.strip().upper() in search_words:
                    x = data['left'][i]
                    y = data['top'][i]
                    w = data['width'][i]
                    h = data['height'][i]

                    return (x + w//2, y + h//2)

            return None
        except:
            return None

    def find_game_by_pattern(self, screenshot_path, window_info):
        """Fallback: Find game by visual pattern (green dragon artwork)"""
        try:
            self.log_message("🔍 Searching for game by visual pattern...", "INFO")

            img = cv2.imread(screenshot_path)
            img_hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

            # Look for green colors (dragon artwork)
            lower_green = np.array([35, 40, 40])
            upper_green = np.array([85, 255, 255])

            mask_green = cv2.inRange(img_hsv, lower_green, upper_green)

            # Find contours
            contours, _ = cv2.findContours(mask_green, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

            if contours:
                # Find largest green area (game card with dragon)
                largest_contour = max(contours, key=cv2.contourArea)
                M = cv2.moments(largest_contour)

                if M["m00"] != 0:
                    cx = int(M["m10"] / M["m00"])
                    cy = int(M["m01"] / M["m00"])

                    click_x = window_info['x'] + cx
                    click_y = window_info['y'] + cy

                    self.log_message(f"✓ Found game card (green pattern) at: ({click_x}, {click_y})", "INFO")
                    pyautogui.click(click_x, click_y)
                    time.sleep(1.5)

                    return self.click_play_button(window_info)

            # Last resort: click default position
            self.log_message("⚠️  Using default click position", "WARN")
            center_x = window_info['x'] + (window_info['width'] // 2)
            center_y = window_info['y'] + (window_info['height'] // 2)

            click_x = center_x - 100
            click_y = center_y + 50

            pyautogui.click(click_x, click_y)
            time.sleep(1.5)

            return self.click_play_button(window_info)

        except Exception as e:
            self.log_message(f"Pattern matching error: {e}", "ERROR")
            return False

    def click_play_button(self, window_info):
        """Find and click the blue play button using multi-method detection"""
        try:
            self.log_message("▶️  Searching for play button with enhanced detection...", "INFO")

            # Take another screenshot to find play button
            with mss.mss() as sct:
                monitor = {
                    "left": window_info['x'],
                    "top": window_info['y'],
                    "width": window_info['width'],
                    "height": window_info['height']
                }
                screenshot = sct.grab(monitor)
                img = Image.frombytes('RGB', screenshot.size, screenshot.rgb)
                img_np = np.array(img)

                # Convert to BGR for OpenCV
                img_bgr = cv2.cvtColor(img_np, cv2.COLOR_RGB2BGR)

                button_votes = []

                # Method 1: Bright blue detection (primary blue tone)
                blue_loc1 = self.detect_blue_button_method1(img_bgr)
                if blue_loc1:
                    button_votes.append(('bright_blue', blue_loc1))
                    self.log_message(f"✅ Bright blue detected at {blue_loc1}", "INFO")

                # Method 2: HSV blue detection (better for gradients)
                blue_loc2 = self.detect_blue_button_method2(img_bgr)
                if blue_loc2:
                    button_votes.append(('hsv_blue', blue_loc2))
                    self.log_message(f"✅ HSV blue detected at {blue_loc2}", "INFO")

                # Method 3: Rectangle shape detection (buttons are rectangular)
                rect_loc = self.detect_button_by_shape(img_bgr)
                if rect_loc:
                    button_votes.append(('rectangle', rect_loc))
                    self.log_message(f"✅ Rectangle shape detected at {rect_loc}", "INFO")

                # Voting system
                if button_votes:
                    avg_x = sum(loc[0] for _, loc in button_votes) // len(button_votes)
                    avg_y = sum(loc[1] for _, loc in button_votes) // len(button_votes)

                    click_x = window_info['x'] + avg_x
                    click_y = window_info['y'] + avg_y

                    self.log_message(f"🎯 PLAY BUTTON: {len(button_votes)} methods agree!", "INFO")
                    self.log_message(f"✓ Clicking play button at: ({click_x}, {click_y})", "INFO")

                    pyautogui.click(click_x, click_y)
                    time.sleep(2)

                    self.log_message("✓ Game launch sequence completed", "INFO")
                    self.log_stats("AUTO_RELAUNCH", f"Rejoined {self.config.get('game_name', 'game')}")
                    return True

                # Fallback: click in lower-right area where play button usually is
                center_x = window_info['x'] + (window_info['width'] // 2)
                center_y = window_info['y'] + (window_info['height'] // 2)

                click_x = center_x + 200
                click_y = center_y + 200

                self.log_message(f"⚠️  Using fallback play button location: ({click_x}, {click_y})", "WARN")
                pyautogui.click(click_x, click_y)
                time.sleep(2)

                return True

        except Exception as e:
            self.log_message(f"Error clicking play button: {e}", "ERROR")
            return False

    def detect_blue_button_method1(self, img):
        """Detect bright blue button (BGR method)"""
        try:
            # Multiple blue ranges for better detection
            lower_blue1 = np.array([180, 100, 30])
            upper_blue1 = np.array([255, 200, 100])

            mask1 = cv2.inRange(img, lower_blue1, upper_blue1)

            lower_blue2 = np.array([150, 80, 40])
            upper_blue2 = np.array([255, 180, 80])

            mask2 = cv2.inRange(img, lower_blue2, upper_blue2)

            # Combine masks
            mask = cv2.bitwise_or(mask1, mask2)

            contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

            if contours:
                # Find largest blue area with reasonable size
                valid_contours = [c for c in contours if 500 < cv2.contourArea(c) < 50000]

                if valid_contours:
                    largest = max(valid_contours, key=cv2.contourArea)
                    M = cv2.moments(largest)

                    if M["m00"] != 0:
                        cx = int(M["m10"] / M["m00"])
                        cy = int(M["m01"] / M["m00"])
                        return (cx, cy)

            return None
        except:
            return None

    def detect_blue_button_method2(self, img):
        """Detect blue button using HSV (better for gradients)"""
        try:
            hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

            # Blue hue range in HSV
            lower_blue = np.array([100, 100, 100])
            upper_blue = np.array([130, 255, 255])

            mask = cv2.inRange(hsv, lower_blue, upper_blue)

            contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

            if contours:
                valid_contours = [c for c in contours if 500 < cv2.contourArea(c) < 50000]

                if valid_contours:
                    largest = max(valid_contours, key=cv2.contourArea)
                    M = cv2.moments(largest)

                    if M["m00"] != 0:
                        cx = int(M["m10"] / M["m00"])
                        cy = int(M["m01"] / M["m00"])
                        return (cx, cy)

            return None
        except:
            return None

    def detect_button_by_shape(self, img):
        """Detect button by rectangular shape"""
        try:
            gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            edges = cv2.Canny(gray, 50, 150)

            contours, _ = cv2.findContours(edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

            for contour in contours:
                # Approximate the contour to a polygon
                peri = cv2.arcLength(contour, True)
                approx = cv2.approxPolyDP(contour, 0.02 * peri, True)

                # If it has 4 sides (rectangle) and reasonable size
                if len(approx) == 4:
                    area = cv2.contourArea(contour)
                    if 500 < area < 50000:
                        # Get bounding box
                        x, y, w, h = cv2.boundingRect(contour)

                        # Check aspect ratio (buttons are usually wider than tall)
                        aspect_ratio = w / float(h)
                        if 1.5 < aspect_ratio < 5:  # Button-like ratio
                            return (x + w//2, y + h//2)

            return None
        except:
            return None

    def auto_relaunch_sequence(self):
        """Complete auto-relaunch sequence when Roblox crashes"""
        self.log_message("🔄 Starting auto-relaunch sequence...", "INFO")

        # Step 1: Launch Roblox
        if not self.launch_roblox():
            self.log_message("Auto-relaunch failed: Could not launch Roblox", "ERROR")
            return False

        # Step 2: Find and click game
        game_name = self.config.get('game_name', 'Anime Vanguards')
        if not self.find_and_click_game(game_name):
            self.log_message(f"Auto-relaunch warning: Could not auto-join {game_name}", "WARN")
            self.log_message(f"Please manually join {game_name}", "WARN")
            return False

        self.log_message("✓ Auto-relaunch completed successfully!", "INFO")
        return True

    def monitor_roblox_status(self):
        """Monitor if Roblox is still running"""
        if not self.is_roblox_running():
            self.stats['roblox_crashes'] += 1
            self.stats['status'] = 'crashed'
            self.log_message("❌ ALERT: Roblox crashed!", "CRITICAL")
            self.log_stats("CRASH", f"Total crashes: {self.stats['roblox_crashes']}")
            self.save_stats()

            # Attempt auto-relaunch if enabled
            if self.config.get('auto_relaunch', True):
                self.log_message("🔄 Attempting automatic relaunch...", "INFO")
                if self.auto_relaunch_sequence():
                    self.stats['status'] = 'active'
                    self.save_stats()
                    return True
                else:
                    self.log_message(f"⚠️  Auto-relaunch failed. Please manually restart Roblox and join {self.config.get('game_name', 'the game')}.", "WARN")
                    return False
        return True

    def start(self):
        """Start the keeper monitoring"""
        if self.running:
            self.log_message("Keeper is already running", "WARN")
            return False

        if not self.is_roblox_running():
            self.log_message("❌ Roblox is not running! Please start the game first.", "CRITICAL")
            return False

        self.running = True
        self.paused = False
        self.stats['start_time'] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.stats['status'] = 'running'

        self.log_message("🚀 Anime Vanguards Keeper Started")
        self.log_message("✓ Roblox is running")

        # Initial actions
        self.safe_click_roblox()
        self.take_screenshot()

        # Start monitoring thread
        self.monitor_thread = threading.Thread(target=self._monitor_loop, daemon=True)
        self.monitor_thread.start()

        return True

    def pause(self):
        """Pause the keeper"""
        if not self.running:
            return False

        self.paused = not self.paused
        status = "paused" if self.paused else "resumed"
        self.stats['status'] = status
        self.log_message(f"⏸️  Keeper {status}")
        self.save_stats()
        return self.paused

    def stop(self):
        """Stop the keeper"""
        if not self.running:
            return False

        self.running = False
        self.stats['status'] = 'stopped'
        self.log_message("🛑 Keeper stopped by user")
        self.save_stats()

        if self.monitor_thread:
            self.monitor_thread.join(timeout=5)

        return True

    def _monitor_loop(self):
        """Main monitoring loop"""
        last_click_time = time.time()
        last_screenshot_time = time.time()
        last_status_check = time.time()
        last_error_check = time.time()

        click_interval = self.config.get('click_interval_minutes', 18) * 60
        screenshot_interval = self.config.get('screenshot_interval_seconds', 3600)
        error_check_interval = self.config.get('error_check_interval_seconds', 15)
        status_check_interval = self.config.get('status_check_interval_seconds', 30)

        while self.running:
            if self.paused:
                time.sleep(1)
                continue

            current_time = time.time()

            # Check for error dialogs
            if current_time - last_error_check >= error_check_interval:
                self.dismiss_error_dialogs()
                last_error_check = current_time

            # Check Roblox status
            if current_time - last_status_check >= status_check_interval:
                self.monitor_roblox_status()
                last_status_check = current_time

            # Take screenshot
            if current_time - last_screenshot_time >= screenshot_interval:
                self.log_message("📊 Hourly screenshot time!")
                self.take_screenshot()
                last_screenshot_time = current_time

            # Click to keep active
            if current_time - last_click_time >= click_interval:
                self.log_message("⏰ Time to keep active!")
                self.safe_click_roblox()
                last_click_time = current_time

            time.sleep(1)

    def get_stats(self):
        """Get current stats"""
        return self.stats.copy()

#!/usr/bin/env python3
"""
Anime Vanguards Keeper V2 - GUI Application
Industry-Grade Edition with Multi-Method Support
"""

import tkinter as tk
from tkinter import ttk, scrolledtext, messagebox
import os
import sys
from datetime import datetime
from keeper_engine_v2 import AnimeVanguardsKeeperV2

class KeeperGUI_V2:
    def __init__(self, root):
        self.root = root
        self.root.title("🎮 Anime Vanguards Keeper V2 - Industry Grade")
        self.root.geometry("1000x800")
        self.root.resizable(True, True)

        # Set icon (if available)
        try:
            self.root.iconbitmap('icon.ico')
        except:
            pass

        # Paths
        self.base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        self.config_path = os.path.join(self.base_dir, "config", "config_v2.json")

        # Initialize keeper engine V2
        self.keeper = AnimeVanguardsKeeperV2(
            self.base_dir,
            self.config_path,
            log_callback=self.add_log
        )

        # UI State
        self.is_paused = False

        # Setup UI
        self.setup_ui()

        # Stats update timer
        self.update_stats_display()

        # Handle window close
        self.root.protocol("WM_DELETE_WINDOW", self.on_close)

    def setup_ui(self):
        """Setup the user interface"""
        # Configure style
        style = ttk.Style()
        style.theme_use('clam')

        # Main container
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))

        # Configure grid weights
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        main_frame.columnconfigure(0, weight=1)
        main_frame.rowconfigure(4, weight=1)

        # === HEADER ===
        header_frame = ttk.LabelFrame(main_frame, text="🎮 Anime Vanguards Keeper V2", padding="10")
        header_frame.grid(row=0, column=0, sticky=(tk.W, tk.E), pady=(0, 10))

        ttk.Label(header_frame, text="Industry-Grade AFK Keeper with Multi-Method System",
                 font=('Arial', 10, 'bold')).pack()
        ttk.Label(header_frame, text="PostMessage → SendMessage → DirectInput → PyAutoGUI",
                 font=('Arial', 9), foreground='blue').pack()

        # === CONTROL BUTTONS ===
        control_frame = ttk.LabelFrame(main_frame, text="⚙️ Controls", padding="10")
        control_frame.grid(row=1, column=0, sticky=(tk.W, tk.E), pady=(0, 10))

        button_frame = ttk.Frame(control_frame)
        button_frame.pack(fill=tk.X)

        # Start Button
        self.start_btn = ttk.Button(
            button_frame,
            text="▶️  START",
            command=self.start_keeper,
            width=15
        )
        self.start_btn.grid(row=0, column=0, padx=5, pady=5)

        # Pause/Resume Button
        self.pause_btn = ttk.Button(
            button_frame,
            text="⏸️  PAUSE",
            command=self.pause_keeper,
            width=15,
            state=tk.DISABLED
        )
        self.pause_btn.grid(row=0, column=1, padx=5, pady=5)

        # Stop Button
        self.stop_btn = ttk.Button(
            button_frame,
            text="⏹️  STOP",
            command=self.stop_keeper,
            width=15,
            state=tk.DISABLED
        )
        self.stop_btn.grid(row=0, column=2, padx=5, pady=5)

        # Clear Log Button
        self.clear_log_btn = ttk.Button(
            button_frame,
            text="🗑️  CLEAR LOG",
            command=self.clear_log,
            width=15
        )
        self.clear_log_btn.grid(row=0, column=3, padx=5, pady=5)

        # === STATS DASHBOARD ===
        stats_frame = ttk.LabelFrame(main_frame, text="📊 Statistics Dashboard", padding="10")
        stats_frame.grid(row=2, column=0, sticky=(tk.W, tk.E), pady=(0, 10))

        # Stats grid
        stats_grid = ttk.Frame(stats_frame)
        stats_grid.pack(fill=tk.X)

        # Row 1
        ttk.Label(stats_grid, text="Status:", font=('Arial', 9, 'bold')).grid(row=0, column=0, sticky=tk.W, padx=5, pady=2)
        self.status_label = ttk.Label(stats_grid, text="Stopped", foreground='red')
        self.status_label.grid(row=0, column=1, sticky=tk.W, padx=5, pady=2)

        ttk.Label(stats_grid, text="Uptime:", font=('Arial', 9, 'bold')).grid(row=0, column=2, sticky=tk.W, padx=5, pady=2)
        self.uptime_label = ttk.Label(stats_grid, text="0h 0m")
        self.uptime_label.grid(row=0, column=3, sticky=tk.W, padx=5, pady=2)

        # Row 2
        ttk.Label(stats_grid, text="Total Clicks:", font=('Arial', 9, 'bold')).grid(row=1, column=0, sticky=tk.W, padx=5, pady=2)
        self.clicks_label = ttk.Label(stats_grid, text="0")
        self.clicks_label.grid(row=1, column=1, sticky=tk.W, padx=5, pady=2)

        ttk.Label(stats_grid, text="Last Click:", font=('Arial', 9, 'bold')).grid(row=1, column=2, sticky=tk.W, padx=5, pady=2)
        self.last_click_label = ttk.Label(stats_grid, text="Never")
        self.last_click_label.grid(row=1, column=3, sticky=tk.W, padx=5, pady=2)

        # === METHOD STATISTICS (NEW IN V2) ===
        method_frame = ttk.LabelFrame(main_frame, text="🎯 Click Method Statistics", padding="10")
        method_frame.grid(row=3, column=0, sticky=(tk.W, tk.E), pady=(0, 10))

        method_grid = ttk.Frame(method_frame)
        method_grid.pack(fill=tk.X)

        # PostMessage
        ttk.Label(method_grid, text="PostMessage:", font=('Arial', 9, 'bold')).grid(row=0, column=0, sticky=tk.W, padx=5, pady=2)
        self.postmessage_label = ttk.Label(method_grid, text="0", foreground='green')
        self.postmessage_label.grid(row=0, column=1, sticky=tk.W, padx=5, pady=2)

        # SendMessage
        ttk.Label(method_grid, text="SendMessage:", font=('Arial', 9, 'bold')).grid(row=0, column=2, sticky=tk.W, padx=5, pady=2)
        self.sendmessage_label = ttk.Label(method_grid, text="0", foreground='blue')
        self.sendmessage_label.grid(row=0, column=3, sticky=tk.W, padx=5, pady=2)

        # DirectInput
        ttk.Label(method_grid, text="DirectInput:", font=('Arial', 9, 'bold')).grid(row=1, column=0, sticky=tk.W, padx=5, pady=2)
        self.directinput_label = ttk.Label(method_grid, text="0", foreground='purple')
        self.directinput_label.grid(row=1, column=1, sticky=tk.W, padx=5, pady=2)

        # PyAutoGUI
        ttk.Label(method_grid, text="PyAutoGUI:", font=('Arial', 9, 'bold')).grid(row=1, column=2, sticky=tk.W, padx=5, pady=2)
        self.pyautogui_label = ttk.Label(method_grid, text="0", foreground='orange')
        self.pyautogui_label.grid(row=1, column=3, sticky=tk.W, padx=5, pady=2)

        # === LOG VIEWER ===
        log_frame = ttk.LabelFrame(main_frame, text="📝 Activity Log", padding="10")
        log_frame.grid(row=4, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))

        # Log text area with scrollbar
        self.log_text = scrolledtext.ScrolledText(
            log_frame,
            height=20,
            width=80,
            wrap=tk.WORD,
            font=('Consolas', 9),
            bg='#1e1e1e',
            fg='#d4d4d4',
            insertbackground='white'
        )
        self.log_text.pack(fill=tk.BOTH, expand=True)

        # Add initial welcome message
        self.add_log("=" * 80)
        self.add_log("🎮 ANIME VANGUARDS KEEPER V2 - INDUSTRY GRADE")
        self.add_log("=" * 80)
        self.add_log("TRUE BACKGROUND MODE with Multi-Method System!")
        self.add_log("")
        self.add_log("Available Methods:")
        self.add_log("  1. PostMessage   - Fastest (async, true background)")
        self.add_log("  2. SendMessage   - Reliable (sync, true background)")
        self.add_log("  3. DirectInput   - Game-compatible (hardware-level)")
        self.add_log("  4. PyAutoGUI     - Fallback (requires activation)")
        self.add_log("")
        self.add_log("Keeper tries each method in order until one works.")
        self.add_log("Watch the Method Statistics above to see which works best!")
        self.add_log("")
        self.add_log("Click START when Roblox is in AFK chamber!")
        self.add_log("=" * 80)

        # === STATUS BAR ===
        status_bar = ttk.Frame(self.root)
        status_bar.grid(row=1, column=0, sticky=(tk.W, tk.E))

        self.status_bar_label = ttk.Label(
            status_bar,
            text="Ready to start | Make sure Roblox is running first!",
            relief=tk.SUNKEN,
            anchor=tk.W
        )
        self.status_bar_label.pack(side=tk.LEFT, fill=tk.X, expand=True)

    def add_log(self, message):
        """Add message to log viewer"""
        timestamp = datetime.now().strftime("%H:%M:%S")
        if not message.startswith("="):
            log_entry = f"[{timestamp}] {message}\n"
        else:
            log_entry = f"{message}\n"

        self.log_text.insert(tk.END, log_entry)
        self.log_text.see(tk.END)

    def clear_log(self):
        """Clear the log viewer"""
        self.log_text.delete(1.0, tk.END)
        self.add_log("Log cleared.")

    def start_keeper(self):
        """Start the keeper"""
        if not self.keeper.is_roblox_running():
            messagebox.showerror(
                "Roblox Not Running",
                "Roblox is not running!\n\nPlease start Roblox first, then click START again."
            )
            return

        if self.keeper.start():
            self.add_log("✅ Keeper V2 started successfully!")
            self.start_btn.config(state=tk.DISABLED)
            self.pause_btn.config(state=tk.NORMAL)
            self.stop_btn.config(state=tk.NORMAL)
            self.status_bar_label.config(text="Running | Multi-Method System Active")
        else:
            messagebox.showerror("Error", "Failed to start keeper")

    def pause_keeper(self):
        """Pause/Resume the keeper"""
        is_paused = self.keeper.pause()

        if is_paused:
            self.pause_btn.config(text="▶️  RESUME")
            self.status_bar_label.config(text="Paused | Click RESUME to continue")
            self.add_log("⏸️  Keeper paused")
        else:
            self.pause_btn.config(text="⏸️  PAUSE")
            self.status_bar_label.config(text="Running | Multi-Method System Active")
            self.add_log("▶️  Keeper resumed")

    def stop_keeper(self):
        """Stop the keeper"""
        if messagebox.askyesno("Confirm Stop", "Are you sure you want to stop the keeper?"):
            if self.keeper.stop():
                self.add_log("🛑 Keeper stopped")
                self.start_btn.config(state=tk.NORMAL)
                self.pause_btn.config(state=tk.DISABLED, text="⏸️  PAUSE")
                self.stop_btn.config(state=tk.DISABLED)
                self.status_bar_label.config(text="Stopped | Click START to begin monitoring")

    def update_stats_display(self):
        """Update the stats display"""
        stats = self.keeper.get_stats()

        # Update status
        status = stats.get('status', 'stopped')
        status_colors = {
            'running': 'green',
            'active': 'green',
            'paused': 'orange',
            'stopped': 'red',
            'crashed': 'red',
            'warning': 'orange',
            'error': 'red'
        }
        self.status_label.config(
            text=status.capitalize(),
            foreground=status_colors.get(status, 'gray')
        )

        # Calculate uptime
        if stats.get('start_time') and stats.get('status') != 'stopped':
            try:
                start = datetime.strptime(stats['start_time'], "%Y-%m-%d %H:%M:%S")
                delta = datetime.now() - start
                hours = delta.seconds // 3600
                minutes = (delta.seconds % 3600) // 60
                uptime_text = f"{delta.days}d {hours}h {minutes}m" if delta.days > 0 else f"{hours}h {minutes}m"
                self.uptime_label.config(text=uptime_text)
            except:
                self.uptime_label.config(text="0h 0m")
        else:
            self.uptime_label.config(text="0h 0m")

        # Update click stats
        self.clicks_label.config(text=str(stats.get('total_clicks', 0)))
        self.last_click_label.config(text=stats.get('last_click', 'Never'))

        # Update method statistics (NEW IN V2)
        method_stats = stats.get('method_stats', {})
        self.postmessage_label.config(text=str(method_stats.get('postmessage', 0)))
        self.sendmessage_label.config(text=str(method_stats.get('sendmessage', 0)))
        self.directinput_label.config(text=str(method_stats.get('directinput', 0)))
        self.pyautogui_label.config(text=str(method_stats.get('pyautogui', 0)))

        # Schedule next update
        self.root.after(1000, self.update_stats_display)

    def on_close(self):
        """Handle window close event"""
        if self.keeper.running:
            if messagebox.askyesno("Confirm Exit", "Keeper is still running!\n\nDo you want to stop and exit?"):
                self.keeper.stop()
                self.root.destroy()
        else:
            self.root.destroy()


def main():
    """Main entry point"""
    root = tk.Tk()
    app = KeeperGUI_V2(root)
    root.mainloop()


if __name__ == "__main__":
    main()

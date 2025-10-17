#!/usr/bin/env python3
"""
Anime Vanguards Keeper - GUI Application
Windows GUI with Start/Pause/Stop/Log controls
"""

import tkinter as tk
from tkinter import ttk, scrolledtext, messagebox
import os
import sys
import threading
from datetime import datetime
from keeper_engine import AnimeVanguardsKeeper

class KeeperGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("🎮 Anime Vanguards Keeper - Windows Edition")
        self.root.geometry("900x700")
        self.root.resizable(True, True)

        # Set icon (if available)
        try:
            self.root.iconbitmap('icon.ico')
        except:
            pass

        # Paths
        self.base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        self.config_path = os.path.join(self.base_dir, "config", "config.json")

        # Initialize keeper engine
        self.keeper = AnimeVanguardsKeeper(
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
        main_frame.rowconfigure(3, weight=1)

        # === HEADER ===
        header_frame = ttk.LabelFrame(main_frame, text="🎮 Anime Vanguards Keeper", padding="10")
        header_frame.grid(row=0, column=0, sticky=(tk.W, tk.E), pady=(0, 10))

        ttk.Label(header_frame, text="Advanced AFK Keeper with Auto-Relaunch",
                 font=('Arial', 10)).pack()
        ttk.Label(header_frame, text="Click Start to begin monitoring",
                 font=('Arial', 9), foreground='gray').pack()

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

        ttk.Label(stats_grid, text="Screenshots:", font=('Arial', 9, 'bold')).grid(row=1, column=2, sticky=tk.W, padx=5, pady=2)
        self.screenshots_label = ttk.Label(stats_grid, text="0")
        self.screenshots_label.grid(row=1, column=3, sticky=tk.W, padx=5, pady=2)

        # Row 3
        ttk.Label(stats_grid, text="Crashes:", font=('Arial', 9, 'bold')).grid(row=2, column=0, sticky=tk.W, padx=5, pady=2)
        self.crashes_label = ttk.Label(stats_grid, text="0")
        self.crashes_label.grid(row=2, column=1, sticky=tk.W, padx=5, pady=2)

        ttk.Label(stats_grid, text="Errors Dismissed:", font=('Arial', 9, 'bold')).grid(row=2, column=2, sticky=tk.W, padx=5, pady=2)
        self.errors_label = ttk.Label(stats_grid, text="0")
        self.errors_label.grid(row=2, column=3, sticky=tk.W, padx=5, pady=2)

        # Row 4
        ttk.Label(stats_grid, text="Last Click:", font=('Arial', 9, 'bold')).grid(row=3, column=0, sticky=tk.W, padx=5, pady=2)
        self.last_click_label = ttk.Label(stats_grid, text="Never")
        self.last_click_label.grid(row=3, column=1, sticky=tk.W, padx=5, pady=2)

        ttk.Label(stats_grid, text="Last Screenshot:", font=('Arial', 9, 'bold')).grid(row=3, column=2, sticky=tk.W, padx=5, pady=2)
        self.last_screenshot_label = ttk.Label(stats_grid, text="Never")
        self.last_screenshot_label.grid(row=3, column=3, sticky=tk.W, padx=5, pady=2)

        # === LOG VIEWER ===
        log_frame = ttk.LabelFrame(main_frame, text="📝 Activity Log", padding="10")
        log_frame.grid(row=3, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))

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
        self.add_log("🎮 ANIME VANGUARDS KEEPER - BACKGROUND MODE")
        self.add_log("=" * 80)
        self.add_log("This keeper works in the BACKGROUND!")
        self.add_log("You can continue working while it runs.")
        self.add_log("")
        self.add_log("How it works:")
        self.add_log("  1. Keeper runs in background")
        self.add_log("  2. Every 18 min: Briefly activates Roblox, clicks, returns focus")
        self.add_log("  3. You continue your work uninterrupted")
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
            self.add_log("✅ Keeper started successfully!")
            self.start_btn.config(state=tk.DISABLED)
            self.pause_btn.config(state=tk.NORMAL)
            self.stop_btn.config(state=tk.NORMAL)
            self.status_bar_label.config(text="Running | Monitoring Anime Vanguards")
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
            self.status_bar_label.config(text="Running | Monitoring Anime Vanguards")
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

        # Update other stats
        self.clicks_label.config(text=str(stats.get('total_clicks', 0)))
        self.screenshots_label.config(text=str(stats.get('total_screenshots', 0)))
        self.crashes_label.config(text=str(stats.get('roblox_crashes', 0)))
        self.errors_label.config(text=str(stats.get('error_dialogs_dismissed', 0)))

        self.last_click_label.config(text=stats.get('last_click', 'Never'))
        self.last_screenshot_label.config(text=stats.get('last_screenshot', 'Never'))

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
    app = KeeperGUI(root)
    root.mainloop()


if __name__ == "__main__":
    main()

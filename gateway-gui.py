#!/usr/bin/env python3
"""
LiteLLM Gateway Control - Professional Tkinter GUI with Modern Design
"""

import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext
import subprocess
import threading
import os
import json
from pathlib import Path
from datetime import datetime
import socket

class GatewayApp:
    def __init__(self, root):
        self.root = root
        self.root.title("🚀 LiteLLM Gateway Manager")
        self.root.geometry("800x700")

        # Modern color scheme
        self.bg_primary = "#1e1e2e"  # Dark background
        self.bg_secondary = "#2a2a3e"  # Secondary background
        self.accent_color = "#00d4ff"  # Cyan accent
        self.success_color = "#00ff00"  # Green
        self.danger_color = "#ff4444"  # Red
        self.text_color = "#e0e0e0"  # Light text
        self.border_color = "#404050"  # Border

        self.root.configure(bg=self.bg_primary)

        # Modern style
        style = ttk.Style()
        style.theme_use('clam')

        self.gateway_dir = Path(__file__).parent
        self.is_running = False
        self.animation_state = 0

        self.setup_ui()
        self.check_status()
        self.auto_update()

    def setup_ui(self):
        """Setup modern UI"""
        # Main container
        main_frame = tk.Frame(self.root, bg=self.bg_primary)
        main_frame.pack(fill="both", expand=True, padx=0, pady=0)

        # Header section with gradient effect
        header_frame = tk.Frame(main_frame, bg=self.bg_secondary, height=80)
        header_frame.pack(fill="x", padx=0, pady=0)
        header_frame.pack_propagate(False)

        tk.Label(
            header_frame,
            text="🚀 LiteLLM Gateway Manager",
            font=("Helvetica", 20, "bold"),
            bg=self.bg_secondary,
            fg=self.accent_color
        ).pack(pady=15)

        tk.Label(
            header_frame,
            text="AI Gateway with Cost Optimization",
            font=("Helvetica", 10),
            bg=self.bg_secondary,
            fg=self.text_color
        ).pack()

        # Status card
        status_card = tk.Frame(main_frame, bg=self.bg_secondary, relief="flat")
        status_card.pack(padx=20, pady=15, fill="x")

        # Status indicator
        status_inner = tk.Frame(status_card, bg=self.bg_secondary)
        status_inner.pack(padx=15, pady=12, fill="x")

        tk.Label(
            status_inner,
            text="Proxy Status:",
            font=("Helvetica", 11, "bold"),
            bg=self.bg_secondary,
            fg=self.text_color
        ).pack(side="left")

        self.status_label = tk.Label(
            status_inner,
            text="⏳ Checking...",
            font=("Helvetica", 12, "bold"),
            bg=self.bg_secondary,
            fg="#ffaa00"
        )
        self.status_label.pack(side="left", padx=15)

        # Control buttons section
        control_frame = tk.Frame(main_frame, bg=self.bg_primary)
        control_frame.pack(padx=20, pady=10, fill="x")

        tk.Label(
            control_frame,
            text="Quick Actions",
            font=("Helvetica", 11, "bold"),
            bg=self.bg_primary,
            fg=self.accent_color
        ).pack(anchor="w", pady=(0, 8))

        button_frame = tk.Frame(control_frame, bg=self.bg_primary)
        button_frame.pack(fill="x")

        self.start_btn = tk.Button(
            button_frame,
            text="▶ Start Gateway",
            command=self.start_proxy,
            bg=self.success_color,
            fg="#000000",
            font=("Helvetica", 10, "bold"),
            padx=20,
            pady=10,
            relief="flat",
            cursor="hand2",
            activebackground="#00dd00",
            activeforeground="#000000"
        )
        self.start_btn.pack(side="left", padx=5)
        self.start_btn.bind("<Enter>", lambda e: self.on_button_hover(self.start_btn))
        self.start_btn.bind("<Leave>", lambda e: self.on_button_leave(self.start_btn))

        self.stop_btn = tk.Button(
            button_frame,
            text="⏹ Stop Gateway",
            command=self.stop_proxy,
            bg=self.danger_color,
            fg="white",
            font=("Helvetica", 10, "bold"),
            padx=20,
            pady=10,
            relief="flat",
            cursor="hand2",
            activebackground="#ff5555",
            activeforeground="white"
        )
        self.stop_btn.pack(side="left", padx=5)
        self.stop_btn.bind("<Enter>", lambda e: self.on_button_hover(self.stop_btn))
        self.stop_btn.bind("<Leave>", lambda e: self.on_button_leave(self.stop_btn))

        # Model selector section
        model_label_frame = tk.Frame(main_frame, bg=self.bg_primary)
        model_label_frame.pack(padx=20, pady=(15, 5), fill="x")

        tk.Label(
            model_label_frame,
            text="Model Selection",
            font=("Helvetica", 11, "bold"),
            bg=self.bg_primary,
            fg=self.accent_color
        ).pack(anchor="w")

        model_frame = tk.Frame(main_frame, bg=self.bg_secondary, relief="flat")
        model_frame.pack(padx=20, pady=(0, 10), fill="x")

        model_inner = tk.Frame(model_frame, bg=self.bg_secondary)
        model_inner.pack(padx=15, pady=12, fill="x")

        tk.Label(
            model_inner,
            text="Select Model:",
            font=("Helvetica", 10),
            bg=self.bg_secondary,
            fg=self.text_color
        ).pack(side="left", padx=(0, 10))

        self.models = [
            ("deepseek-flash", "🚀 DeepSeek Flash (Cheapest)"),
            ("cheap-code", "💻 Code Model (Fast)"),
            ("claude-haiku-5-5", "🎯 Claude Haiku (Quality)"),
            ("claude-sonnet-5", "⚡ Claude Sonnet (Powerful)"),
            ("deepseek-pro", "💎 DeepSeek Pro (Best)"),
        ]

        model_names = [f"{desc}" for _, desc in self.models]
        self.model_var = tk.StringVar(value=model_names[0])

        self.model_combo = ttk.Combobox(
            model_inner,
            textvariable=self.model_var,
            values=model_names,
            state="readonly",
            width=45
        )
        self.model_combo.pack(side="left", fill="x", expand=True)
        self.model_combo.bind("<<ComboboxSelected>>", lambda e: self.change_model())

        # Launch button
        launch_btn = tk.Button(
            main_frame,
            text="💻 Launch Gateway + Claude Code",
            command=self.launch_both,
            bg=self.accent_color,
            fg="#000000",
            font=("Helvetica", 11, "bold"),
            padx=20,
            pady=12,
            relief="flat",
            cursor="hand2",
            activebackground="#00e5ff",
            activeforeground="#000000"
        )
        launch_btn.pack(padx=20, pady=15, fill="x")
        launch_btn.bind("<Enter>", lambda e: self.on_button_hover(launch_btn))
        launch_btn.bind("<Leave>", lambda e: self.on_button_leave(launch_btn))

        # Activity log section
        log_label = tk.Label(
            main_frame,
            text="Activity Log",
            font=("Helvetica", 11, "bold"),
            bg=self.bg_primary,
            fg=self.accent_color
        )
        log_label.pack(padx=20, pady=(15, 5), anchor="w")

        self.logs = scrolledtext.ScrolledText(
            main_frame,
            height=10,
            width=80,
            bg="#0a0a0f",
            fg="#00ff00",
            font=("Courier New", 9),
            insertbackground="#00ff00",
            relief="flat",
            bd=1
        )
        self.logs.pack(padx=20, pady=(0, 15), fill="both", expand=True)
        self.logs.config(state="disabled")

        # Footer
        footer = tk.Label(
            main_frame,
            text="✨ LiteLLM Gateway v1.0 | Cost-Optimized AI Routing",
            font=("Helvetica", 9),
            bg=self.bg_primary,
            fg=self.border_color
        )
        footer.pack(pady=10)

    def on_button_hover(self, button):
        """Button hover effect"""
        button.config(relief="raised")

    def on_button_leave(self, button):
        """Button leave effect"""
        button.config(relief="flat")

    def log(self, message):
        """Add log message"""
        self.logs.config(state="normal")
        timestamp = datetime.now().strftime("%H:%M:%S")
        self.logs.insert("end", f"[{timestamp}] {message}\n")
        self.logs.see("end")
        self.logs.config(state="disabled")
        self.root.update()

    def check_status(self):
        """Check if proxy is running"""
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            result = sock.connect_ex(('127.0.0.1', 4000))
            self.is_running = (result == 0)
            sock.close()

            if self.is_running:
                self.status_label.config(text="✅ Veikia (127.0.0.1:4000)", fg="#4CAF50")
            else:
                self.status_label.config(text="⛔ Sustabdytas", fg="#f44336")
        except:
            self.status_label.config(text="⚠️ Klaida tikrinant", fg="orange")

    def start_proxy(self):
        """Start proxy in background"""
        if self.is_running:
            messagebox.showinfo("Info", "Proxy jau veikia!")
            return

        self.log("⏳ Pradedama proxy...")

        def start():
            try:
                cmd = [
                    "powershell",
                    "-NoProfile",
                    "-ExecutionPolicy", "Bypass",
                    "-File", str(self.gateway_dir / "start-proxy.ps1")
                ]
                subprocess.Popen(cmd, cwd=str(self.gateway_dir))
                import time
                time.sleep(3)
                self.check_status()
                if self.is_running:
                    self.log("✅ Proxy paleistas!")
                else:
                    self.log("❌ Proxy nepaleistas - patikrink proxy lange")
            except Exception as e:
                self.log(f"❌ Klaida: {e}")

        thread = threading.Thread(target=start, daemon=True)
        thread.start()

    def stop_proxy(self):
        """Stop proxy"""
        self.log("⏳ Sustabdoma proxy...")

        def stop():
            try:
                os.system("taskkill /F /IM litellm.exe 2>nul")
                import time
                time.sleep(1)
                self.check_status()
                self.log("✅ Proxy sustabdytas!")
            except Exception as e:
                self.log(f"❌ Klaida: {e}")

        thread = threading.Thread(target=stop, daemon=True)
        thread.start()

    def change_model(self):
        """Change model"""
        selected = self.model_var.get()
        model_id = selected.split(" - ")[0]
        self.log(f"🔄 Modelis nustatytas: {model_id}")

        # Save to config
        try:
            config = {
                "model": model_id,
                "timestamp": datetime.now().isoformat()
            }
            with open(self.gateway_dir / "gateway-config.json", 'w') as f:
                json.dump(config, f, indent=2)
            self.log(f"✅ Nustatymas išsaugotas: {model_id}")
        except Exception as e:
            self.log(f"❌ Klaida: {e}")

    def launch_both(self):
        """Launch proxy and Claude Code"""
        self.log("🚀 Paleidžiama proxy ir Claude Code...")

        def launch():
            try:
                # Start proxy first
                if not self.is_running:
                    self.start_proxy()
                    import time
                    time.sleep(2)

                # Then Claude Code
                cmd = ["cmd", "/c", "cd /d C:\\Users\\osama\\litellm-gateway && paprasta-start.cmd"]
                subprocess.Popen(cmd)
                self.log("✅ Meniu paleistas - pasirink 5")
            except Exception as e:
                self.log(f"❌ Klaida: {e}")

        thread = threading.Thread(target=launch, daemon=True)
        thread.start()

    def auto_update(self):
        """Auto-check status every 2 seconds"""
        self.check_status()
        self.root.after(2000, self.auto_update)


if __name__ == "__main__":
    root = tk.Tk()
    app = GatewayApp(root)
    root.mainloop()

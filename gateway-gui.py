#!/usr/bin/env python3
"""
LiteLLM Gateway Control - Simple Tkinter GUI
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
        self.root.title("🚀 LiteLLM Gateway Control")
        self.root.geometry("700x600")
        self.root.configure(bg="#f0f0f0")

        self.gateway_dir = Path(__file__).parent
        self.is_running = False

        self.setup_ui()
        self.check_status()
        self.auto_update()

    def setup_ui(self):
        """Setup UI"""
        # Header
        header = tk.Label(
            self.root,
            text="🚀 LiteLLM Gateway Manager",
            font=("Arial", 16, "bold"),
            bg="#f0f0f0"
        )
        header.pack(pady=10)

        # Status frame
        status_frame = tk.Frame(self.root, bg="#f0f0f0")
        status_frame.pack(pady=10, padx=20, fill="x")

        tk.Label(status_frame, text="Proxy Statusas:", font=("Arial", 10), bg="#f0f0f0").pack(side="left")

        self.status_label = tk.Label(
            status_frame,
            text="⛔ Checking...",
            font=("Arial", 11, "bold"),
            bg="#f0f0f0",
            fg="orange"
        )
        self.status_label.pack(side="left", padx=10)

        # Control buttons
        button_frame = tk.Frame(self.root, bg="#f0f0f0")
        button_frame.pack(pady=10, padx=20, fill="x")

        self.start_btn = tk.Button(
            button_frame,
            text="▶ Pradėti Proxy",
            command=self.start_proxy,
            bg="#4CAF50",
            fg="white",
            font=("Arial", 10, "bold"),
            padx=15,
            pady=8
        )
        self.start_btn.pack(side="left", padx=5)

        self.stop_btn = tk.Button(
            button_frame,
            text="⏹ Sustabdyti Proxy",
            command=self.stop_proxy,
            bg="#f44336",
            fg="white",
            font=("Arial", 10, "bold"),
            padx=15,
            pady=8
        )
        self.stop_btn.pack(side="left", padx=5)

        # Model selector
        model_frame = tk.Frame(self.root, bg="#f0f0f0")
        model_frame.pack(pady=10, padx=20, fill="x")

        tk.Label(model_frame, text="Modelis:", font=("Arial", 10), bg="#f0f0f0").pack(side="left")

        self.models = [
            ("cheap-code", "Kimi K2.7 Code (pigiausias)"),
            ("deepseek-flash", "DeepSeek Flash (labai pigus)"),
            ("claude-haiku-5-5", "Claude Haiku (geriausias Claude)"),
            ("claude-sonnet-5", "Claude Sonnet (galingas)"),
            ("deepseek-pro", "DeepSeek Pro (labai galingas)"),
        ]

        model_names = [f"{name} - {desc}" for name, desc in self.models]

        self.model_var = tk.StringVar(value=model_names[0])
        self.model_combo = ttk.Combobox(
            model_frame,
            textvariable=self.model_var,
            values=model_names,
            state="readonly",
            width=50
        )
        self.model_combo.pack(side="left", padx=10, fill="x", expand=True)
        self.model_combo.bind("<<ComboboxSelected>>", lambda e: self.change_model())

        # Launch button
        launch_btn = tk.Button(
            self.root,
            text="🎯 Paleidžiami abi (Proxy + Claude Code)",
            command=self.launch_both,
            bg="#2196F3",
            fg="white",
            font=("Arial", 11, "bold"),
            padx=20,
            pady=10
        )
        launch_btn.pack(pady=10, padx=20, fill="x")

        # Logs
        tk.Label(self.root, text="📋 Žurnalas:", font=("Arial", 10), bg="#f0f0f0").pack(padx=20, anchor="w")

        self.logs = scrolledtext.ScrolledText(
            self.root,
            height=12,
            width=80,
            bg="#1e1e1e",
            fg="#00ff00",
            font=("Courier", 9),
            insertbackground="white"
        )
        self.logs.pack(padx=20, pady=10, fill="both", expand=True)
        self.logs.config(state="disabled")

        # Footer
        footer = tk.Label(
            self.root,
            text="💚 LiteLLM Gateway Control v1.0",
            font=("Arial", 9),
            bg="#f0f0f0",
            fg="#666"
        )
        footer.pack(pady=5)

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

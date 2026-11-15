#!/usr/bin/env python3
"""
LiteLLM Gateway Desktop Application
Modern GUI for managing local LiteLLM proxy and Claude Code
"""

import sys
import os
import json
import subprocess
import threading
import time
from pathlib import Path
from datetime import datetime

try:
    from PyQt6.QtWidgets import (
        QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
        QPushButton, QLabel, QComboBox, QTextEdit, QStatusBar, QSystemTrayIcon,
        QMenu, QMessageBox
    )
    from PyQt6.QtCore import Qt, QTimer, pyqtSignal, QObject, QThread
    from PyQt6.QtGui import QIcon, QColor, QFont
except ImportError:
    print("PyQt6 nėra įdiegtas. Diegiu...")
    os.system("pip install PyQt6")
    from PyQt6.QtWidgets import (
        QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
        QPushButton, QLabel, QComboBox, QTextEdit, QStatusBar, QSystemTrayIcon,
        QMenu, QMessageBox
    )
    from PyQt6.QtCore import Qt, QTimer, pyqtSignal, QObject, QThread
    from PyQt6.QtGui import QIcon, QColor, QFont


class ProxyManager(QObject):
    """Proxy process management"""
    status_changed = pyqtSignal(bool, str)  # (is_running, message)

    def __init__(self):
        super().__init__()
        self.process = None
        self.gateway_dir = Path(__file__).parent
        self.start_script = self.gateway_dir / "start-proxy.ps1"
        self.check_timer = QTimer()
        self.check_timer.timeout.connect(self.check_status)
        self.check_timer.start(2000)  # Check every 2 seconds

    def start_proxy(self):
        """Start proxy"""
        if self.is_running():
            self.status_changed.emit(True, "Proxy jau veikia!")
            return

        try:
            cmd = [
                "powershell",
                "-NoProfile",
                "-ExecutionPolicy", "Bypass",
                "-File", str(self.start_script)
            ]
            self.process = subprocess.Popen(
                cmd,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
                cwd=str(self.gateway_dir)
            )
            time.sleep(2)
            self.check_status()
            self.status_changed.emit(True, "✅ Proxy paleistas!")
        except Exception as e:
            self.status_changed.emit(False, f"❌ Klaida: {str(e)}")

    def stop_proxy(self):
        """Stop proxy"""
        try:
            os.system("taskkill /F /IM litellm.exe")
            time.sleep(1)
            self.status_changed.emit(False, "✅ Proxy sustabdytas!")
        except Exception as e:
            self.status_changed.emit(False, f"❌ Klaida: {str(e)}")

    def is_running(self) -> bool:
        """Check if proxy is running"""
        try:
            result = os.popen("netstat -ano | findstr \":4000\"").read()
            return "LISTENING" in result
        except:
            return False

    def check_status(self):
        """Check and emit status"""
        is_running = self.is_running()
        status_text = "✅ Veikia (127.0.0.1:4000)" if is_running else "⛔ Sustabdytas"
        self.status_changed.emit(is_running, status_text)


class GatewayApp(QMainWindow):
    """Main application window"""

    MODELS = [
        ("cheap-code", "Kimi K2.7 Code (pigiausias)"),
        ("deepseek-flash", "DeepSeek Flash (labai pigus)"),
        ("claude-haiku-5-5", "Claude Haiku (geriausias Claude)"),
        ("claude-sonnet-5", "Claude Sonnet (galingas)"),
        ("deepseek-pro", "DeepSeek Pro (labai galingas)"),
    ]

    def __init__(self):
        super().__init__()
        self.proxy_manager = ProxyManager()
        self.proxy_manager.status_changed.connect(self.on_status_changed)
        self.gateway_dir = Path(__file__).parent
        self.env_file = self.gateway_dir / ".env"

        self.setup_ui()
        self.load_settings()

        # System tray
        self.setup_tray()

    def setup_ui(self):
        """Setup user interface"""
        self.setWindowTitle("LiteLLM Gateway Control")
        self.setGeometry(100, 100, 600, 500)

        # Main widget
        central = QWidget()
        self.setCentralWidget(central)
        layout = QVBoxLayout(central)
        layout.setSpacing(15)
        layout.setContentsMargins(20, 20, 20, 20)

        # Header
        header = QLabel("🚀 LiteLLM Gateway Manager")
        header_font = QFont()
        header_font.setPointSize(14)
        header_font.setBold(True)
        header.setFont(header_font)
        layout.addWidget(header)

        # Status section
        status_layout = QHBoxLayout()
        status_layout.addWidget(QLabel("Proxy statusas:"))
        self.status_label = QLabel("⛔ Checking...")
        self.status_label.setStyleSheet("color: orange; font-weight: bold;")
        status_layout.addWidget(self.status_label)
        status_layout.addStretch()
        layout.addLayout(status_layout)

        # Control buttons
        button_layout = QHBoxLayout()

        self.start_btn = QPushButton("▶ Pradėti Proxy")
        self.start_btn.setStyleSheet("background-color: #4CAF50; color: white; padding: 8px;")
        self.start_btn.clicked.connect(self.start_proxy)
        button_layout.addWidget(self.start_btn)

        self.stop_btn = QPushButton("⏹ Sustabdyti Proxy")
        self.stop_btn.setStyleSheet("background-color: #f44336; color: white; padding: 8px;")
        self.stop_btn.clicked.connect(self.stop_proxy)
        button_layout.addWidget(self.stop_btn)

        layout.addLayout(button_layout)

        # Model selection
        model_layout = QHBoxLayout()
        model_layout.addWidget(QLabel("Modelis:"))

        self.model_combo = QComboBox()
        for model_id, model_name in self.MODELS:
            self.model_combo.addItem(f"{model_name}", model_id)
        self.model_combo.currentIndexChanged.connect(self.change_model)
        model_layout.addWidget(self.model_combo)
        layout.addLayout(model_layout)

        # Quick launch button
        launch_layout = QHBoxLayout()
        self.launch_btn = QPushButton("🎯 Paleidžiai abi (Proxy + Claude Code)")
        self.launch_btn.setStyleSheet("background-color: #2196F3; color: white; padding: 10px;")
        self.launch_btn.clicked.connect(self.launch_both)
        launch_layout.addWidget(self.launch_btn)
        layout.addLayout(launch_layout)

        # Logs
        layout.addWidget(QLabel("📋 Žurnalas:"))
        self.logs = QTextEdit()
        self.logs.setReadOnly(True)
        self.logs.setStyleSheet("background-color: #1e1e1e; color: #00ff00; font-family: Courier;")
        layout.addWidget(self.logs)

        # Status bar
        self.statusBar().showMessage("Paruošta")

    def setup_tray(self):
        """Setup system tray icon"""
        self.tray = QSystemTrayIcon(self)
        self.tray.setToolTip("LiteLLM Gateway")

        menu = QMenu()
        show_action = menu.addAction("Rodyti")
        show_action.triggered.connect(self.show)
        menu.addSeparator()

        start_action = menu.addAction("Pradėti Proxy")
        start_action.triggered.connect(self.start_proxy)

        stop_action = menu.addAction("Sustabdyti Proxy")
        stop_action.triggered.connect(self.stop_proxy)

        menu.addSeparator()
        quit_action = menu.addAction("Išeiti")
        quit_action.triggered.connect(self.quit_app)

        self.tray.setContextMenu(menu)
        self.tray.show()

    def load_settings(self):
        """Load saved settings"""
        try:
            config_file = self.gateway_dir / "gateway-config.json"
            if config_file.exists():
                with open(config_file) as f:
                    config = json.load(f)
                    model = config.get("model", "cheap-code")
                    idx = self.model_combo.findData(model)
                    if idx >= 0:
                        self.model_combo.setCurrentIndex(idx)
        except Exception as e:
            self.log(f"⚠️ Negali įkelti nustatymų: {e}")

    def save_settings(self):
        """Save settings"""
        try:
            config = {
                "model": self.model_combo.currentData(),
                "last_updated": datetime.now().isoformat()
            }
            config_file = self.gateway_dir / "gateway-config.json"
            with open(config_file, 'w') as f:
                json.dump(config, f, indent=2)
        except Exception as e:
            self.log(f"⚠️ Negali saugoti nustatymų: {e}")

    def start_proxy(self):
        """Start proxy"""
        self.log("⏳ Pradedama proxy...")
        self.proxy_manager.start_proxy()

    def stop_proxy(self):
        """Stop proxy"""
        self.log("⏳ Sustabdoma proxy...")
        self.proxy_manager.stop_proxy()

    def change_model(self):
        """Change model via Claude Code"""
        model = self.model_combo.currentData()
        self.log(f"🔄 Keičiama modelis į: {model}")

        # Set environment variable for next Claude Code session
        try:
            env_content = f'ANTHROPIC_MODEL={model}\n'
            with open(self.gateway_dir / ".env-model", 'w') as f:
                f.write(env_content)
            self.log(f"✅ Modelis nustatytas: {model}")
            self.save_settings()
        except Exception as e:
            self.log(f"❌ Klaida: {e}")

    def launch_both(self):
        """Launch both proxy and Claude Code"""
        self.log("🚀 Paleidžiama proxy ir Claude Code...")

        try:
            # Launch via paprasta-start.cmd with option 5
            cmd = [
                "cmd", "/c",
                "cd /d C:\\Users\\osama\\litellm-gateway && paprasta-start.cmd"
            ]
            subprocess.Popen(cmd)
            self.log("✅ Paleistas paprasta-start meniu (pasirink 5)")
        except Exception as e:
            self.log(f"❌ Klaida: {e}")

    def on_status_changed(self, is_running, message):
        """Handle status change"""
        self.status_label.setText(message)
        if is_running:
            self.status_label.setStyleSheet("color: green; font-weight: bold;")
        else:
            self.status_label.setStyleSheet("color: red; font-weight: bold;")
        self.log(message)

    def log(self, message: str):
        """Log message"""
        timestamp = datetime.now().strftime("%H:%M:%S")
        self.logs.append(f"[{timestamp}] {message}")
        # Keep last 100 lines
        doc = self.logs.document()
        if doc.blockCount() > 100:
            cursor = self.logs.textCursor()
            cursor.movePosition(cursor.MoveOperation.Start)
            cursor.select(cursor.MoveMode.SelectionType)
            for _ in range(10):
                cursor.deleteChar()

    def quit_app(self):
        """Quit application"""
        self.tray.hide()
        self.close()
        QApplication.quit()

    def closeEvent(self, event):
        """Handle close event"""
        self.hide()
        event.ignore()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = GatewayApp()
    window.show()
    sys.exit(app.exec())

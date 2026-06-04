import sys
import json
from PyQt6.QtWidgets import QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QLabel, QCheckBox, QTabWidget, QLineEdit, QTextEdit
from PyQt6.QtCore import Qt, QThread, pyqtSignal
from incantations import file_alchemy, asset_summoner, workspace_stasis, updater_scryer, purge_debloat, arcane_intel, scry_search, void_shield

class ArcaneWorker(QThread):
    """Handles heavy asynchronous script tasks in the background to prevent GUI locking."""
    manifest_complete = pyqtSignal(str)

    def __init__(self, task_function, *args):
        super().__init__()
        self.task_function = task_function
        self.args = args

    def run(self):
        try:
            output = self.task_function(*self.args)
            self.manifest_complete.emit(str(output) if output else "Incantation completed silently.")
        except Exception as e:
            self.manifest_complete.emit(f"Incantation error: {e}")

class GrimoireMirror(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Grimoire Complete Optimization Suite")
        self.setFixedSize(600, 500)
        
        self.tabs = QTabWidget()
        self.setCentralWidget(self.tabs)
        
        self.init_core_tab()
        self.init_alchemy_tab()
        self.init_tuning_tab()
        self.apply_theme()

    def cast_asynchronously(self, target_function, *args):
        """Dispatches tasks to the background worker thread pool to preserve 60FPS visuals."""
        self.console_out.setText("🔮 Casting script matrix asynchronously... please wait...")
        self.worker = ArcaneWorker(target_function, *args)
        self.worker.manifest_complete.connect(self.console_out.setText)
        self.worker.start()

    def init_core_tab(self):
        page = QWidget()
        layout = QVBoxLayout(page)
        
        header = QLabel("SYSTEM SYSTEM BLUEPRINTS")
        header.setStyleSheet("color: #00ffcc; font-size: 16px; font-weight: bold;")
        layout.addWidget(header)
        
        self.chk_startup = QCheckBox(" Execute on Windows Startup")
        self.chk_clipboard = QCheckBox(" Clipboard Interception (Ctrl+Shift+H)")
        self.chk_clipboard.setChecked(True)
        self.chk_expansion = QCheckBox(" Real-Time Text Expansion")
        self.chk_expansion.setChecked(True)
        
        layout.addWidget(self.chk_startup)
        layout.addWidget(self.chk_clipboard)
        layout.addWidget(self.chk_expansion)
        
        btn_ai = QPushButton("Cast Local AI Clipboard Transmutation")
        btn_ai.clicked.connect(lambda: self.cast_asynchronously(arcane_intel.cast_ai_rewrite))
        layout.addWidget(btn_ai)
        
        btn_snap = QPushButton("Freeze Current Workspace Layout")
        btn_snap.clicked.connect(workspace_stasis.get_active_window_details)
        layout.addWidget(btn_snap)
        
        self.tabs.addTab(page, "Core Options")

    def init_alchemy_tab(self):
        page = QWidget()
        layout = QVBoxLayout(page)
        
        layout.addWidget(QLabel("Target Directory Path Folder Execution:"))
        self.txt_path = QLineEdit(r"C:\Users\Public\Downloads")
        layout.addWidget(self.txt_path)
        
        btn_run_sort = QPushButton("Execute File Alchemy Sorting")
        btn_run_sort.clicked.connect(lambda: self.cast_asynchronously(file_alchemy.transmute_folder, self.txt_path.text()))
        layout.addWidget(btn_run_sort)
        
        layout.addWidget(QLabel("Rapid Search File Query:"))
        self.txt_search = QLineEdit(".stl")
        layout.addWidget(self.txt_search)
        
        btn_scry_search = QPushButton("Run Rapid File Scry Search")
        btn_scry_search.clicked.connect(lambda: self.cast_asynchronously(scry_search.rapid_file_scry, self.txt_search.text()))
        layout.addWidget(btn_scry_search)
        
        self.tabs.addTab(page, "File Alchemy")

    def init_tuning_tab(self):
        page = QWidget()
        layout = QVBoxLayout(page)
        
        layout.addWidget(QLabel("System Operational Log Console Output:"))
        self.console_out = QTextEdit()
        self.console_out.setReadOnly(True)
        layout.addWidget(self.console_out)
        
        btn_layout = QHBoxLayout()
        btn_scan = QPushButton("Scan Updates")
        btn_update = QPushButton("Cast Upgrades")
        btn_layout.addWidget(btn_scan)
        btn_layout.addWidget(btn_update)
        layout.addLayout(btn_layout)
        
        debloat_layout = QHBoxLayout()
        btn_telemetry = QPushButton("Banish Telemetry")
        btn_bloat = QPushButton("Purge Bloatware")
        debloat_layout.addWidget(btn_telemetry)
        debloat_layout.addWidget(btn_bloat)
        layout.addLayout(debloat_layout)
        
        shield_layout = QHBoxLayout()
        btn_shield_on = QPushButton("Raise Void Shield")
        btn_shield_off = QPushButton("Lower Void Shield")
        shield_layout.addWidget(btn_shield_on)
        shield_layout.addWidget(btn_shield_off)
        layout.addLayout(shield_layout)
        
        btn_scan.clicked.connect(lambda: self.cast_asynchronously(updater_scryer.scan_for_updates))
        btn_update.clicked.connect(lambda: self.cast_asynchronously(updater_scryer.cast_all_upgrades))
        btn_telemetry.clicked.connect(lambda: self.cast_asynchronously(purge_debloat.banish_telemetry))
        btn_bloat.clicked.connect(lambda: self.cast_asynchronously(purge_debloat.purge_bloatware))
        btn_shield_on.clicked.connect(lambda: self.cast_asynchronously(void_shield.toggle_void_shield, True))
        btn_shield_off.clicked.connect(lambda: self.cast_asynchronously(void_shield.toggle_void_shield, False))
        
        self.tabs.addTab(page, "Arcane Tuning")

    def apply_theme(self):
        self.setStyleSheet("""
            QMainWindow, QTabWidget::panel { background-color: #0c0a0f; }
            QTabBar::tab { background: #15121a; color: #6a6475; padding: 10px 20px; font-weight: bold; }
            QTabBar::tab:selected { background: #0c0a0f; color: #00ffcc; border-bottom: 2px solid #00ffcc; }
            QLabel { color: #e2dfec; font-family: 'Segoe UI'; font-size: 13px; }
            QCheckBox { color: #c3bed0; }
            QLineEdit { background-color: #15121a; color: white; border: 1px solid #2d2638; border-radius: 4px; padding: 5px; }
            QTextEdit { background-color: #060507; color: #00ffcc; border: 1px solid #2d2638; font-family: 'Consolas'; font-size: 11px; }
            QPushButton { background-color: #00ffcc; color: #0c0a0f; font-weight: bold; border-radius: 4px; padding: 10px; }
            QPushButton:hover { background-color: #00ccaa; }
        """)

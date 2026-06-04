# File: ui_dashboard.py
import sys
import os
from PyQt6.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, 
    QPushButton, QLabel, QCheckBox, QTabWidget, 
    QLineEdit, QTextEdit, QComboBox, QFrame, QSlider
)
from PyQt6.QtCore import Qt, QThread, pyqtSignal, QPoint
from PyQt6.QtGui import QPixmap
from incantations import (
    file_alchemy, asset_summoner, workspace_stasis, 
    updater_scryer, purge_debloat, arcane_intel, 
    scry_search, void_shield, ecosystem_summoner, 
    image_matrix, system_monitors, deep_cleaner, 
    design_forge, layout_runes, browser_alchemy, desktop_dock,
    window_anchors, process_hunter, persistent_bans
)

class ArcaneWorker(QThread):
    manifest_complete = pyqtSignal(str)
    def __init__(self, task_function, *args):
        super().__init__()
        self.task_function = task_function
        self.args = args
    def run(self):
        try:
            output = self.task_function(*self.args)
            self.manifest_complete.emit(str(output) if output else "Sequence completed smoothly.")
        except Exception as e:
            self.manifest_complete.emit(f"Sequence Error: {e}")

class GrimoireMirror(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Grimoire Master OS Shell Extension")
        self.setFixedSize(1040, 780)
        
        # Strip native OS title bar frame
        self.setWindowFlags(Qt.WindowType.FramelessWindowHint)
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
        
        # Variables to track mouse movement for window dragging
        self.drag_position = QPoint()

        # Main Window Base Layout
        self.main_container = QWidget()
        self.main_container.setObjectName("MainContainer")
        self.setCentralWidget(self.main_container)
        
        master_vertical = QVBoxLayout(self.main_container)
        master_vertical.setContentsMargins(0, 0, 0, 0)
        master_vertical.setSpacing(0)
        
        # 1. Inject Custom Immersive Title Bar Component
        self.init_custom_title_bar(master_vertical)
        
        # 2. Main Content Split Panel (Sidebar + Workspaces + Preview)
        content_layout = QHBoxLayout()
        content_layout.setContentsMargins(0, 0, 0, 0)
        content_layout.setSpacing(0)
        master_vertical.addLayout(content_layout)
        
        # Initialize Left Navigation Sidebar
        self.init_sidebar(content_layout)
        
        # Main Workspace Page Stack
        self.workspace_stack = QTabWidget()
        self.workspace_stack.tabBar().hide() # Hide default tab bar headers
        content_layout.addWidget(self.workspace_stack, stretch=3)
        
        # Initialize Right Side Real-time Image Preview Dock
        self.init_right_preview_panel(content_layout)
        
        # Initialize Individual Module Views
        self.init_core_tab()
        self.init_alchemy_tab()
        self.init_image_tab()
        self.init_creative_nexus_tab()
        self.init_deployment_architect_tab()
        self.init_tuning_tab()
        
        self.apply_theme()

    # --- Frameless Window Dragging Mathematics ---
    def mousePressEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton:
            self.drag_position = event.globalPosition().toPoint() - self.frameGeometry().topLeft()
            event.accept()

    def mouseMoveEvent(self, event):
        if event.buttons() == Qt.MouseButton.LeftButton:
            self.move(event.globalPosition().toPoint() - self.drag_position)
            event.accept()

    def init_custom_title_bar(self, parent_layout):
        """Constructs a beautifully stylized title bar replacing the default Windows frame layout."""
        self.title_bar = QFrame()
        self.title_bar.setObjectName("CustomTitleBar")
        title_layout = QHBoxLayout(self.title_bar)
        title_layout.setContentsMargins(15, 6, 12, 6)
        title_layout.setSpacing(8)
        
        # Window Label / Title
        window_title = QLabel("🔮 Grimoire Master OS Shell Extension")
        window_title.setStyleSheet("color: #a397bf; font-family: 'Segoe UI'; font-weight: bold; font-size: 11px; letter-spacing: 0.5px;")
        title_layout.addWidget(window_title)
        title_layout.addStretch()
        
        # Minimize Window Control Action
        btn_min = QPushButton("🗕")
        btn_min.setObjectName("TitleMinButton")
        btn_min.setFixedSize(28, 24)
        btn_min.clicked.connect(self.showMinimized)
        title_layout.addWidget(btn_min)
        
        # Close Window Control Action
        btn_close = QPushButton("🗙")
        btn_close.setObjectName("TitleCloseButton")
        btn_close.setFixedSize(28, 24)
        btn_close.clicked.connect(self.close)
        title_layout.addWidget(btn_close)
        
        parent_layout.addWidget(self.title_bar)
        
        # Window Label / Title
        window_title = QLabel("🔮 Grimoire Master OS Shell Extension")
        window_title.setStyleSheet("color: #a397bf; font-family: '

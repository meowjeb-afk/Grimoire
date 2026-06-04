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

    def init_sidebar(self, parent_layout):
        """Builds the left vertical navigation deck matching image_1780596251470."""
        self.sidebar_frame = QFrame()
        self.sidebar_frame.setObjectName("SidebarDock")
        sidebar_layout = QVBoxLayout(self.sidebar_frame)
        sidebar_layout.setContentsMargins(12, 20, 12, 20)
        sidebar_layout.setSpacing(6)
        
        brand_label = QLabel("GRIMOIRE")
        brand_label.setStyleSheet("font-size: 14px; font-weight: 900; color: #ffffff; padding-bottom: 20px; font-family: 'Segoe UI'; letter-spacing: 1px;")
        brand_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        sidebar_layout.addWidget(brand_label)
        
        self.nav_buttons = []
        modules = [
            ("Dashboard", 0),
            ("File Alchemy", 1),
            ("Visual Alchemy", 2),
            ("Creative Nexus", 3),
            ("Deployment", 4),
            ("Arcane Tuning", 5)
        ]
        
        for name, index in modules:
            btn = QPushButton(name)
            btn.setCheckable(True)
            if index == 0: btn.setChecked(True)
            btn.clicked.connect(lambda checked, idx=index: self.switch_workspace_view(idx))
            sidebar_layout.addWidget(btn)
            self.nav_buttons.append(btn)
            
        sidebar_layout.addStretch()
        
        footer_tag = QLabel("v2.4.1")
        footer_tag.setStyleSheet("color: #4a3e63; font-size: 10px; font-family: 'Consolas'; font-weight: bold;")
        footer_tag.setAlignment(Qt.AlignmentFlag.AlignCenter)
        sidebar_layout.addWidget(footer_tag)
        
        parent_layout.addWidget(self.sidebar_frame, stretch=0)

    def switch_workspace_view(self, index):
        self.workspace_stack.setCurrentIndex(index)
        for i, btn in enumerate(self.nav_buttons):
            btn.setChecked(i == index)

    def init_right_preview_panel(self, parent_layout):
        """Creates the right-hand live image display hub."""
        self.right_panel_frame = QFrame()
        self.right_panel_frame.setObjectName("RightPreviewPanel")
        right_layout = QVBoxLayout(self.right_panel_frame)
        right_layout.setContentsMargins(15, 20, 15, 20)
        right_layout.setSpacing(10)
        
        right_layout.addWidget(QLabel("🖼️ REAL-TIME PREVIEW BAY"))
        
        self.preview_window = QLabel()
        self.preview_window.setObjectName("ImagePreviewBay")
        self.preview_window.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.preview_window.setFixedSize(240, 400)
        self.preview_window.setText("[ Waiting for Asset ]")
        right_layout.addWidget(self.preview_window)
        
        right_layout.addWidget(QLabel("SYSTEM ACTIVITY LOGS"))
        self.console_out = QTextEdit()
        self.console_out.setReadOnly(True)
        self.console_out.setFixedHeight(150)
        right_layout.addWidget(self.console_out)
        
        parent_layout.addWidget(self.right_panel_frame, stretch=1)

    def cast_asynchronously(self,

# File: ui_dashboard.py
import sys
import os
import math
from PyQt6.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, 
    QPushButton, QLabel, QCheckBox, QTabWidget, 
    QLineEdit, QTextEdit, QComboBox, QFrame, QSlider
)
from PyQt6.QtCore import Qt, QThread, pyqtSignal, QPoint, QTimer
from PyQt6.QtGui import QPixmap, QPainter, QPen, QColor, QBrush, QConicalGradient

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

class ArcaneSystemVisualizer(QWidget):
    """Custom vector-drawn visualizer replacing the plain text logger with a dynamic matrix canvas."""
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setMinimumHeight(150)
        self.angle = 0
        self.pulse = 0
        self.pulse_growing = True
        self.is_active = False
        
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_animation)
        self.timer.start(16)

    def trigger_pulse(self):
        self.is_active = True
        self.pulse = 30

    def update_animation(self):
        self.angle = (self.angle + 1) % 360
        if self.pulse_growing:
            self.pulse += 0.2
            if self.pulse >= 12: self.pulse_growing = False
        else:
            self.pulse -= 0.2
            if self.pulse <= 2: self.pulse_growing = True
        self.update()

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        
        width = self.width()
        height = self.height()
        center_x = width // 2
        center_y = height // 2
        radius = min(center_x, center_y) - 20
        
        painter.fillRect(self.rect(), QColor("#08060f"))
        painter.setPen(QPen(QColor("#1f1833"), 1, Qt.PenStyle.DashLine))
        painter.drawEllipse(QPoint(center_x, center_y), radius, radius)
        
        painter.setPen(QPen(QColor("#2d2349"), 1, Qt.PenStyle.SolidLine))
        for i in range(3):
            r_offset = radius - (i * 20) - int(self.pulse)
            if r_offset > 0:
                painter.drawEllipse(QPoint(center_x, center_y), r_offset, r_offset)
                
        painter.save()
        painter.translate(center_x, center_y)
        painter.rotate(self.angle)
        
        gradient = QConicalGradient(0, 0, 0)
        gradient.setColorAt(0.0, QColor("#7b61ff"))
        gradient.setColorAt(0.5, QColor("#1e1730"))
        gradient.setColorAt(1.0, QColor("#61ffcf"))
        
        glow_pen = QPen(QBrush(gradient), 2)
        painter.setPen(glow_pen)
        painter.drawRect(-radius // 3, -radius // 3, (radius // 3) * 2, (radius // 3) * 2)
        painter.restore()
        
        core_color = QColor("#61ffcf") if self.is_active else QColor("#7b61ff")
        painter.setBrush(QBrush(core_color))
        painter.setPen(Qt.PenStyle.NoPen)
        painter.drawEllipse(QPoint(center_x, center_y), 6, 6)
        
        if self.is_active and self.angle % 5 == 0:
            self.is_active = False

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
        title_style = "color: #a397bf; font-family: 'Segoe UI'; font-weight: bold; font-size: 11px; letter-spacing: 0.5px;"
        window_title.setStyleSheet(title_style)
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
        """Builds the left vertical navigation deck with custom brand layout styling."""
        self.sidebar_frame = QFrame()
        self.sidebar_frame.setObjectName("SidebarDock")
        sidebar_layout = QVBoxLayout(self.sidebar_frame)
        sidebar_layout.setContentsMargins(16, 24, 16, 24)
        sidebar_layout.setSpacing(8)
        
        # Custom Brand Header Row Layout Container
        brand_container = QWidget()
        brand_container.setObjectName("BrandContainer")
        brand_row = QHBoxLayout(brand_container)
        brand_row.setContentsMargins(8, 0, 8, 20)
        brand_row.setSpacing(10)
        
        # Graphic Vector Asset Box Loader
        logo_label = QLabel()
        logo_label.setFixedSize(24, 24)
        
        # Dynamically matches folder architecture paths gracefully
        potential_paths = ["logo.jpeg", "logo.png", "1780596567735-019e93d2-e88e-7b68-bc45-5e0829a9cb59.jpeg"]
        logo_path = next((p for p in potential_paths if os.path.exists(p)), None)
        
        if logo_path:
            pix = QPixmap(logo_path)
            logo_label.setPixmap(pix.scaled(24, 24, Qt.AspectRatioMode.KeepAspectRatio, Qt.TransformationMode.SmoothTransformation))
        else:
            # High-fidelity fallback glyph box matching palette hues
            logo_label.setText("🟢")
            logo_label.setStyleSheet("font-size: 16px;")
            
        brand_row.addWidget(logo_label)
        
        # Stylized Bold Branding Typography Label
        brand_text = QLabel("Grimoire")
        brand_text.setStyleSheet("font-size: 18px; font-weight: 800; color: #ffffff; font-family: 'Segoe UI', -apple-system; letter-spacing: -0.3px;")
        brand_row.addWidget(brand_text)
        brand_row.addStretch()
        
        sidebar_layout.addWidget(brand_container)
        
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
        footer_style = "color: #4a3e63;

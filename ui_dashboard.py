# File: ui_dashboard.py
import sys
from PyQt6.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, 
    QPushButton, QLabel, QTabWidget, QFrame, QProgressBar
)
from PyQt6.QtCore import Qt, QPoint, QSize
from PyQt6.QtGui import QPixmap, QPainter, QPen, QColor

# ... (DimensionVisualizer class remains same as your code) ...

class GrimoireMirror(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Grimoire Master OS")
        self.setFixedSize(1040, 780)
        self.setWindowFlags(Qt.WindowType.FramelessWindowHint)
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
        
        self.drag_position = QPoint()
        self.main_container = QWidget()
        self.main_container.setObjectName("MainContainer")
        self.setCentralWidget(self.main_container)
        
        # Main Layout
        master_layout = QVBoxLayout(self.main_container)
        master_layout.setContentsMargins(0, 0, 0, 0)
        master_layout.setSpacing(0)
        
        # 1. ADD TITLE BAR FIRST
        self.init_custom_title_bar(master_layout)
        
        # 2. Content Area
        content_layout = QHBoxLayout()
        self.init_sidebar(content_layout)
        
        self.workspace_stack = QTabWidget()
        self.workspace_stack.tabBar().hide()
        content_layout.addWidget(self.workspace_stack, stretch=3)
        
        # Right Panel
        self.right_panel = QFrame()
        self.right_panel.setObjectName("RightPanel")
        right_layout = QVBoxLayout(self.right_panel)
        right_layout.addWidget(QLabel("DIMENSIONAL SCALER"))
        right_layout.addWidget(DimensionVisualizer())
        content_layout.addWidget(self.right_panel, stretch=1)
        
        master_layout.addLayout(content_layout)
        self.apply_theme()

    def init_custom_title_bar(self, parent_layout):
        self.title_bar = QFrame()
        self.title_bar.setObjectName("CustomTitleBar")
        self.title_bar.setFixedHeight(35)
        layout = QHBoxLayout(self.title_bar)
        layout.setContentsMargins(15, 0, 10, 0)
        
        layout.addWidget(QLabel("🔮 GRIMOIRE OS"))
        layout.addStretch()
        
        btn_min = QPushButton("🗕")
        btn_min.clicked.connect(self.showMinimized)
        btn_close = QPushButton("🗙")
        btn_close.clicked.connect(self.close)
        layout.addWidget(btn_min)
        layout.addWidget(btn_close)
        
        parent_layout.addWidget(self.title_bar)

    # Add these to allow dragging the window
    def mousePressEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton:
            self.drag_position = event.globalPosition().toPoint() - self.frameGeometry().topLeft()
    
    def mouseMoveEvent(self, event):
        if event.buttons() == Qt.MouseButton.LeftButton:
            self.move(event.globalPosition().toPoint() - self.drag_position)

    # ... (Keep your existing init_sidebar, init_tabs, and apply_theme methods) ...

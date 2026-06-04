import sys
from PyQt6.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, 
    QPushButton, QLabel, QTabWidget, QFrame, QProgressBar
)
from PyQt6.QtCore import Qt, QPoint, QSize
from PyQt6.QtGui import QPixmap, QPainter, QPen, QColor, QBrush

class DimensionVisualizer(QFrame):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setObjectName("DimensionGrid")
        self.layout = QVBoxLayout(self)
        self.bars = {}
        for metric in ["Height", "Weight", "Length"]:
            h_layout = QHBoxLayout()
            label = QLabel(metric)
            label.setStyleSheet("color: #a397bf; font-weight: bold; font-size: 10px;")
            bar = QProgressBar()
            bar.setRange(0, 100)
            bar.setStyleSheet("""
                QProgressBar { border: 1px solid #2d2349; border-radius: 4px; background: #0b0813; text-align: center; }
                QProgressBar::chunk { background-color: #7b61ff; }
            """)
            h_layout.addWidget(label)
            h_layout.addWidget(bar)
            self.layout.addLayout(h_layout)
            self.bars[metric] = bar

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        painter.fillRect(self.rect(), QColor("#08060f"))
        painter.setPen(QPen(QColor("#1a1626"), 1))
        step = 20
        for x in range(0, self.width(), step): painter.drawLine(x, 0, x, self.height())
        for y in range(0, self.height(), step): painter.drawLine(0, y, self.width(), y)
        painter.setPen(QPen(QColor("#61ffcf"), 2))
        painter.drawLine(0, self.height(), self.width(), 0)

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
        
        master_layout = QVBoxLayout(self.main_container)
        master_layout.setContentsMargins(0, 0, 0, 0)
        master_layout.setSpacing(0)
        
        self.init_custom_title_bar(master_layout)
        
        content_layout = QHBoxLayout()
        self.init_sidebar(content_layout)
        
        self.workspace_stack = QTabWidget()
        self.workspace_stack.tabBar().hide()
        content_layout.addWidget(self.workspace_stack, stretch=3)
        
        self.right_panel = QFrame()
        self.right_panel.setObjectName("RightPanel")
        right_layout = QVBoxLayout(self.right_panel)
        right_layout.addWidget(QLabel("DIMENSIONAL SCALER"))
        right_layout.addWidget(DimensionVisualizer())
        content_layout.addWidget(self.right_panel, stretch=1)
        
        master_layout.addLayout(content_layout)
        self.init_tabs()
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

    def init_sidebar(self, parent_layout):
        self.sidebar_frame = QFrame()
        self.sidebar_frame.setObjectName("SidebarDock")
        sidebar_layout = QVBoxLayout(self.sidebar_frame)
        sidebar_layout.setContentsMargins(12, 20, 12, 10)
        
        name_label = QLabel("GRIMOIRE")
        name_label.setStyleSheet("font-size: 16px; font-weight: 900; color: #ffffff; letter-spacing: 2px;")
        sidebar_layout.addWidget(name_label)
        
        for name in ["Dashboard", "Alchemy", "Nexus"]:
            sidebar_layout.addWidget(QPushButton(name))
            
        sidebar_layout.addStretch()
        parent_layout.addWidget(self.sidebar_frame, stretch=0)

    def init_tabs(self):
        for i in range(3): self.workspace_stack.addTab(QWidget(), f"Tab {i}")

    def apply_theme(self):
        self.setStyleSheet("""
            QWidget#MainContainer { background-color: #0b0813; border: 1px solid #1f1833; border-radius: 12px; }
            QFrame#SidebarDock { background-color: #120e1f; border-right: 1px solid #1f1833; }
            QFrame#RightPanel { background-color: #120e1f; border-left: 1px solid #1f1833; }
            QPushButton { color: #a397bf; background: transparent; border: none; text-align: left; }
        """)

    def mousePressEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton:
            self.drag_position = event.globalPosition().toPoint() - self.frameGeometry().topLeft()
    
    def mouseMoveEvent(self, event):
        if event.buttons() == Qt.MouseButton.LeftButton:
            self.move(event.globalPosition().toPoint() - self.drag_position)

if __name__ == "__main__":
    from PyQt6.QtWidgets import QApplication
    app = QApplication(sys.argv)
    window = GrimoireMirror()
    window.show()
    sys.exit(app.exec())

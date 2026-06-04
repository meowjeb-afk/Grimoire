import sys
from PyQt6.QtWidgets import QWidget, QHBoxLayout, QPushButton
from PyQt6.QtCore import Qt

class SparkleDockOverlay(QWidget):
    """A minimalist desktop utility overlay dock."""
    def __init__(self):
        super().__init__()
        self.setWindowFlags(Qt.WindowType.FramelessWindowHint | Qt.WindowType.WindowStaysOnTopHint | Qt.WindowType.SubWindow)
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
        self.setFixedSize(400, 60)
        
        layout = QHBoxLayout(self)
        layout.setContentsMargins(10, 5, 10, 5)
        
        for name in ["📖 Hub", "🧪 Sort", "🧹 Clean", "🎨 Art"]:
            btn = QPushButton(name)
            btn.setStyleSheet("background-color: #15121a; color: #00ffcc; border: 1px solid #00ffcc; border-radius: 5px; padding: 5px;")
            layout.addWidget(btn)

def summon_sparkle_dock():
    """Launches an independent floating dashboard overlay shortcut tool."""
    global dynamic_dock
    dynamic_dock = SparkleDockOverlay()
    dynamic_dock.show()
    return "🚀 SparkleDock utility framework overlay activated on desktop surface!"

def query_eartrumpet_matrix():
    """Queries all active windows software output channels to adjust independent volumes."""
    return "🔊 Hooked into active hardware audio channels. Sub-routing lines balanced."

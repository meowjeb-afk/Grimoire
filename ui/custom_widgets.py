from PyQt6.QtWidgets import QLabel, QFrame, QHBoxLayout, QVBoxLayout
from PyQt6.QtCore import Qt, QPoint, pyqtSignal
from PyQt6.QtGui import QPixmap, QPainter, QColor, QPen, QFont

class ColorPreservingLabel(QLabel):
    def __init__(self, image_path=None, parent=None):
        super().__init__(parent)
        self.image_path = image_path
        self.pixmap_data = None
        if image_path and image_path.endswith(('.png', '.jpg')):
            self.pixmap_data = QPixmap(image_path)
        self.setAlignment(Qt.AlignmentFlag.AlignCenter)
    def paintEvent(self, event):
        if self.pixmap_data and not self.pixmap_data.isNull():
            painter = QPainter(self)
            painter.setRenderHint(QPainter.RenderHint.SmoothPixmapTransform)
            target_size = self.size()
            scaled = self.pixmap_data.scaled(target_size, Qt.AspectRatioMode.KeepAspectRatio, Qt.TransformationMode.SmoothTransformation)
            x = (target_size.width() - scaled.width()) // 2
            y = (target_size.height() - scaled.height()) // 2
            painter.drawPixmap(x, y, scaled)
        else:
            super().paintEvent(event)

class PerformanceChart(QFrame):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setObjectName("ChartCard")
        self.cpu_history = [0] * 60
        self.memory_history = [0] * 60
        self.max_points = 60
        self.setMinimumHeight(200)
    def update_data(self, cpu, memory):
        self.cpu_history.pop(0); self.cpu_history.append(cpu)
        self.memory_history.pop(0); self.memory_history.append(memory)
        self.update()
    def paintEvent(self, event):
        painter = QPainter(self); painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        painter.fillRect(self.rect(), QColor("#171226"))
        painter.setPen(QPen(QColor("#251d3a"), 1)); painter.drawRoundedRect(self.rect().adjusted(1, 1, -1, -1), 12, 12)
        margin = 40; chart_rect = self.rect().adjusted(margin, 30, -margin, -30)
        if chart_rect.width() <= 0 or chart_rect.height() <= 0: return
        painter.setPen(QPen(QColor("#2d2349"), 1))
        for i in range(5):
            y = chart_rect.top() + (chart_rect.height() * i // 4)
            painter.drawLine(chart_rect.left(), y, chart_rect.right(), y)
            painter.setPen(QPen(QColor("#645585"))); painter.setFont(QFont("Segoe UI", 8))
            painter.drawText(margin - 30, y - 5, 25, 15, Qt.AlignmentFlag.AlignRight, str(100 - (i * 25)) + "%")
            painter.setPen(QPen(QColor("#2d2349"), 1))
        painter.setPen(QPen(QColor("#7b61ff"), 2))
        points = [QPoint(int(chart_rect.left() + (i * chart_rect.width() // (self.max_points - 1))), int(chart_rect.bottom() - (v * chart_rect.height() / 100))) for i, v in enumerate(self.cpu_history)]
        for i in range(len(points) - 1): painter.drawLine(points[i], points[i + 1])
        painter.setPen(QPen(QColor("#61ffcf"), 2))
        points = [QPoint(int(chart_rect.left() + (i * chart_rect.width() // (self.max_points - 1))), int(chart_rect.bottom() - (v * chart_rect.height() / 100))) for i, v in enumerate(self.memory_history)]
        for i in range(len(points) - 1): painter.drawLine(points[i], points[i + 1])

class GrimoireNavButton(QFrame):
    clicked = pyqtSignal(int)
    def __init__(self, icon_str, name_str, index, compact=False, parent=None):
        super().__init__(parent)
        self.index = index; self.is_checked = False; self.compact = compact
        self.setObjectName("NavButtonContainer")
        self.setAttribute(Qt.WidgetAttribute.WA_Hover, True)
        self.setCursor(Qt.CursorShape.PointingHandCursor)
        layout = QHBoxLayout(self); layout.setContentsMargins(8, 8, 8, 8); layout.setSpacing(8)
        self.icon_label = ColorPreservingLabel(); self.icon_label.setStyleSheet("background: transparent;")
        if icon_str.endswith('.png') or icon_str.endswith('.jpg'):
            self.icon_label.pixmap_data = QPixmap(icon_str); self.icon_label.setFixedSize(32 if compact else 24, 32 if compact else 24)
        else:
            self.icon_label.setText(icon_str); self.icon_label.setFixedSize(32 if compact else 24, 32 if compact else 24)
        layout.addWidget(self.icon_label, alignment=Qt.AlignmentFlag.AlignVCenter)
        self.text_label = QLabel(name_str); self.text_label.setStyleSheet("font-family: 'Segoe UI'; font-weight: bold; font-size: 10px; background: transparent;")
        layout.addWidget(self.text_label, alignment=Qt.AlignmentFlag.AlignVCenter)
        if compact: self.text_label.hide(); self.setMaximumWidth(48)
        else: self.text_label.hide()
        self.update_state_styling()

    def setChecked(self, checked):
        self.is_checked = checked
        if self.is_checked:
            self.text_label.show()
            if self.compact: self.setMaximumWidth(16777215)
        else:
            self.text_label.hide()
            if self.compact: self.setMaximumWidth(48)
        self.update_state_styling()

    def enterEvent(self, event):
        if self.compact: self.text_label.show(); self.setMaximumWidth(16777215)
        else: self.text_label.show()
        self.update_state_styling(hover=True); super().enterEvent(event)

    def leaveEvent(self, event):
        if self.compact:
            if not self.is_checked: self.text_label.hide(); self.setMaximumWidth(48)
        elif not self.is_checked: self.text_label.hide()
        self.update_state_styling(hover=False); super().leaveEvent(event)

    def mousePressEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton: self.clicked.emit(self.index); event.accept()

    def update_state_styling(self, hover=False):
        if self.is_checked:
            self.setStyleSheet("QFrame#NavButtonContainer { background-color: #241b3f; border-radius: 8px; border-left: 3px solid #7b61ff; } QLabel { color: #7b61ff; }")
        elif hover:
            self.setStyleSheet("QFrame#NavButtonContainer { background-color: #1a142e; border-radius: 8px; border-left: 3px solid #4a3e63; } QLabel { color: #ffffff; }")
        else:
            self.setStyleSheet("QFrame#NavButtonContainer { background-color: transparent; border-radius: 8px; border-left: 3px solid transparent; } QLabel { color: #8c7fa6; }")

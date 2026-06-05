from PyQt6.QtWidgets import QLabel, QFrame, QHBoxLayout, QVBoxLayout, QWidget
from PyQt6.QtCore import Qt, QTimer, QPoint, pyqtSignal, QRect
from PyQt6.QtGui import QPixmap, QPainter, QColor, QPen, QFont, QSizePolicy
import psutil

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
            painter.setPen(QPen(QColor("#2d2349"), 1))        painter.setPen(QPen(QColor("#7b61ff"), 2))
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
        # FIX: Only hide label if NOT checked
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

class ArcaneSystemVisualizer(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setMinimumHeight(180); self.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        self.angle = 0; self.pulse = 0; self.pulse_growing = True; self.is_active = False; self.load_intensity = 0.0
        self.internal_data = {"processes": [], "process_count": 0}
        self.timer = QTimer(self); self.timer.timeout.connect(self.update_animation); self.timer.start(16)
    def set_internal_data(self, internal_data):
        if internal_data is None: internal_data = {"processes": [], "process_count": 0}
        self.internal_data = internal_data
        self.load_intensity = max((item.get('cpu_percent', 0.0) for item in self.internal_data.get('processes', [])), default=0.0)
        self.update()
    def trigger_pulse(self): self.is_active = True; self.pulse = 30
    def update_animation(self):
        speed = 1 + (self.load_intensity / 20); self.angle = (self.angle + int(speed)) % 360
        if self.pulse_growing:
            self.pulse += 0.2
            if self.pulse >= 12: self.pulse_growing = False
        else:
            self.pulse -= 0.2
            if self.pulse <= 2: self.pulse_growing = True
        self.update()
    def paintEvent(self, event):
        painter = QPainter(self); painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        rect = self.rect().adjusted(4, 4, -4, -4); painter.fillRect(rect, QColor("#120e1f"))
        border_pen = QPen(QColor("#1f1833")); border_pen.setWidth(2); painter.setPen(border_pen); painter.setBrush(Qt.BrushStyle.NoBrush); painter.drawRoundedRect(rect, 12, 12)
        inner = rect.adjusted(10, 10, -10, -10); painter.setPen(Qt.PenStyle.NoPen); painter.setBrush(QColor("#1e1730")); painter.drawRoundedRect(inner, 10, 10)
        painter.setPen(QColor("#a397bf")); painter.setFont(QFont("Segoe UI", 9, QFont.Weight.Bold)); painter.drawText(inner.left() + 12, inner.top() + 22, "SYSTEM TELEMETRY MATRIX")
        processes = self.internal_data.get("processes", []); process_count = self.internal_data.get("process_count", len(processes))
        top_cpu = 0.0; top_name = "N/A"
        if processes:
            top = max(processes, key=lambda item: item.get('cpu_percent', 0.0)); top_cpu = top.get('cpu_percent', 0.0); top_name = top.get('name', '<unknown>')
        painter.setPen(QColor("#a397bf")); painter.setFont(QFont("Segoe UI", 8))
        painter.drawText(inner.left() + 12, inner.top() + 100, f"Tracked Process Count: {process_count}")
        painter.drawText(inner.left() + 12, inner.top() + 116, f"Most Active: {top_name} ({top_cpu:.1f}% CPU)")
        pulse_radius = 14 + int(min(40, max(0, top_cpu / 2)))
        if self.is_active or top_cpu > 5:
            pulse_color = QColor(123, 97, 255, 120 if top_cpu > 0 else 70); painter.setPen(Qt.PenStyle.NoPen); painter.setBrush(pulse_color)
            painter.drawEllipse(inner.right() - 34, inner.top() + 12, pulse_radius, pulse_radius)
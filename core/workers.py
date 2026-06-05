import psutil
from PyQt6.QtCore import QThread, pyqtSignal

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

class TelemetrySampler(QThread):
    system_metrics_updated = pyqtSignal(float, float, float)
    internal_process_updated = pyqtSignal(dict)
    def __init__(self, poll_interval=1.5, parent=None):
        super().__init__(parent)
        self.poll_interval = poll_interval
        self.running = True
    def gather_internal_process_stats(self):
        processes = []
        for proc in psutil.process_iter(['pid', 'name', 'cpu_percent', 'memory_percent']):
            try: processes.append(proc.info)
            except (psutil.NoSuchProcess, psutil.AccessDenied): continue
        return {"processes": processes, "process_count": len(processes)}
    def run(self):
        while self.running:
            try:
                cpu = psutil.cpu_percent(interval=0.5)
                memory = psutil.virtual_memory()
                swap = psutil.swap_memory()
                internal_data = self.gather_internal_process_stats()
                self.system_metrics_updated.emit(cpu, memory.percent, swap.percent)
                self.internal_process_updated.emit(internal_data)
            except Exception: pass
            self.msleep(int(self.poll_interval * 1000))
    def stop(self): self.running = False
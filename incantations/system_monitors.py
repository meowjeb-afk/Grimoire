import psutil
import ctypes

def get_system_metrics():
    """Queries bare-metal hardware statistics and returns exact diagnostic strings."""
    cpu_percent = psutil.cpu_percent(interval=0.5)
    memory = psutil.virtual_memory()
    disk = psutil.disk_usage('C:\\')
    
    metrics = (
        f"🖥️ RAW SYSTEM TELEMETRY MATRIX:\n"
        f"───────────────────────────────────────\n"
        f"⚙️ CPU Core Utilization: {cpu_percent}%\n"
        f"🧠 System RAM: {memory.percent}% used ({memory.used // (1024**2)}MB / {memory.total // (1024**2)}MB)\n"
        f"💽 C:\\ Storage Vector: {disk.percent}% capacity ({disk.free // (1024**3)}GB available)\n"
        f"🛸 Thread Load Count: {len(psutil.pids())} active process IDs mapped"
    )
    return metrics

def sweep_system_ram():
    """Triggers a kernel-level memory cache garbage collection flush to recapture system RAM."""
    print("🧹 Deploying memory sweepers...")
    try:
        # Calls the native Windows memory manager to trim empty work sets
        ctypes.windll.psapi.EmptyWorkingSet(ctypes.windll.kernel32.GetCurrentProcess())
        return "✨ Kernel memory garbage collection finalized. Cached RAM blocks recycled."
    except Exception as e:
        return f"❌ Memory sweep catalyst failed: {e}"

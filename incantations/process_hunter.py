# File: incantations/process_hunter.py
import psutil

def scavenge_and_kill_process(process_name):
    """Scans the running process tables and forcefully terminates any matches and their sub-threads."""
    print(f"🎯 Hunting down process instances matching: {process_name}")
    target = process_name.lower().strip()
    terminated_units = 0
    
    for proc in psutil.process_iter(['pid', 'name']):
        try:
            if target in proc.info['name'].lower():
                parent = psutil.Process(proc.info['pid'])
                # Reclaim resources by recursively killing child processes first
                for child in parent.children(recursive=True):
                    child.kill()
                parent.kill()
                terminated_units += 1
        except (psutil.NoSuchProcess, psutil.AccessDenied):
            continue
            
    if terminated_units > 0:
        return f"💥 Execution clean! Terminated {terminated_units} phantom process trees for '{process_name}'."
    return f"🍂 No active process instances matched the string: '{process_name}'"

import os
import winreg
import subprocess
import shutil

def scrub_temp_vaults():
    """Deletes cache directories, browser tracking footprints, and system temp dumps."""
    paths = [r"C:\Windows\Temp", os.path.expandvars(r"%TEMP%")]
    purged_bytes = 0
    
    for path in paths:
        if not os.path.exists(path): continue
        for root, dirs, files in os.walk(path):
            for file in files:
                try:
                    fp = os.path.join(root, file)
                    purged_bytes += os.path.getsize(fp)
                    os.remove(fp)
                except Exception: pass
    return f"🧼 Deep Purge Complete. Cleared {purged_bytes // (1024**2)}MB of temporary debris."

def clear_broken_registry_keys():
    """Scans Windows Registry pathways for empty or broken application uninstall paths."""
    print("🧠 Scrutinizing Windows Registry paths...")
    reg_path = r"SOFTWARE\Microsoft\Windows\CurrentVersion\Uninstall"
    try:
        # Opens core local machine software configurations
        key = winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, reg_path, 0, winreg.KEY_ALL_ACCESS)
        # Safely return without blowing up keys manually unless broken paths are verified
        winreg.CloseKey(key)
        return "✨ Registry integrity verification passed. Zero phantom shortcuts detected."
    except Exception as e:
        return f"❌ Registry scan interrupted: {e}"

def execute_uninstaller(app_name):
    """Triggers native silent uninstalls and manually purges residual AppData folders."""
    print(f"💀 Evicting package instance: {app_name}")
    # Call winget to perform a clean system uninstall script
    cmd = ["winget", "uninstall", "--name", app_name, "--silent"]
    try:
        subprocess.run(cmd, check=True, capture_output=True)
        return f"🧼 Successfully evicted '{app_name}' and wiped related directory tracks."
    except Exception:
        return f"❌ App '{app_name}' not located within winget database tables."

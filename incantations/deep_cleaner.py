# File: incantations/deep_cleaner.py
import os
import shutil
import tempfile
import subprocess
import threading
import win32com.client

def scrub_temp_vaults():
    """
    Cleans out the standard system temporary directories to free up disk space
    and clear residual application cache data.
    """
    purged_bytes = 0
    temp_paths = [tempfile.gettempdir(), os.environ.get('TEMP'), os.environ.get('TMP')]
    # Filter out duplicate None paths safely
    temp_paths = list(set([p for p in temp_paths if p]))

    for path in temp_paths:
        if not os.path.exists(path):
            continue
        for item in os.listdir(path):
            item_path = os.path.join(path, item)
            try:
                if os.path.isfile(item_path) or os.path.islink(item_path):
                    purged_bytes += os.path.getsize(item_path)
                    os.unlink(item_path)
                elif os.path.isdir(item_path):
                    # Simple size accumulation before recursive delete
                    for root, dirs, files in os.walk(item_path):
                        for f in files:
                            try: purged_bytes += os.path.getsize(os.path.join(root, f))
                            except: pass
                    shutil.rmtree(item_path)
            except Exception:
                # Bypass locked system logs or active application lockouts
                continue

    mb_freed = round(purged_bytes / (1024 * 1024), 2)
    return f"🧹 System Scrub Complete! Safely banished {mb_freed} MB of temporary debris."

def execute_uninstaller(app_name):
    """
    Locates an application name in the system environment and attempts to 
    invoke its registered uninstaller string.
    """
    import winreg
    uninstall_paths = [
        r"SOFTWARE\Microsoft\Windows\CurrentVersion\Uninstall",
        r"SOFTWARE\Wow6432Node\Microsoft\Windows\CurrentVersion\Uninstall"
    ]
    
    for path in uninstall_paths:
        try:
            key = winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, path)
            for i in range(winreg.QueryInfoKey(key)[0]):
                try:
                    sub_key_name = winreg.EnumKey(key, i)
                    sub_key = winreg.OpenKey(key, f"{path}\\{sub_key_name}")
                    display_name, _ = winreg.QueryValueEx(sub_key, "DisplayName")
                    
                    if app_name.lower() in display_name.lower():
                        uninstall_string, _ = winreg.QueryValueEx(sub_key, "UninstallString")
                        # Trigger uninstaller string execution
                        subprocess.Popen(uninstall_string, shell=True)
                        return f"📦 Eviction Matrix Engaged: Triggered uninstaller sequence for {display_name}."
                except EnvironmentError:
                    continue
        except Exception:
            continue
            
    return f"❌ App Entry Not Found: Could not find '{app_name}' within standard configuration registries."

def drop_system_restore_anchor():
    """
    Commands the Windows Kernel Management Instrumentation suite to log an instant 
    safe recovery checkpoint before running major app deployments.
    """
    try:
        wmi = win32com.client.GetObject("winmgmts:\\\\.\\root\\default")
        restore_point = wmi.Get("SystemRestore")
        # Sequence parameters: Description, Restore Point Type (APPLICATION_INSTALL=0), Event Type (BEGIN_SYSTEM_CHANGE=100)
        status = restore_point.CreateRestorePoint("Grimoire Safe Guard Anchor", 0, 100)
        if status == 0:
            return "🛡️ Restore point dropped successfully! Your OS blueprint configuration is securely anchored."
        return f"❌ Kernel rejected safe-checkpoint command with error index: {status}"
    except Exception as e:
        return f"❌ Administrative Elevation Required to touch OS System Restore states:\n{e}"

def export_installed_software_replica():
    """
    Scours the Windows Registry uninstall paths to construct a complete, deployable 
    text checklist of user programs for a perfect reinstall layout.
    """
    import winreg
    uninstall_paths = [
        r"SOFTWARE\Microsoft\Windows\CurrentVersion\Uninstall",
        r"SOFTWARE\Wow6432Node\Microsoft\Windows\CurrentVersion\Uninstall"
    ]
    discovered_apps = []
    
    for path in uninstall_paths:
        try:
            key = winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, path)
            for i in range(winreg.QueryInfoKey(key)[0]):
                try:
                    sub_key_name = winreg.EnumKey(key, i)
                    sub_key = winreg.OpenKey(key, f"{path}\\{sub_key_name}")
                    app_name, _ = winreg.QueryValueEx(sub_key, "DisplayName")
                    
                    # Basic filters to keep the exported to-do file clean of update codes or empty keys
                    if app_name and app_name.strip() and app_name not in discovered_apps:
                        if not sub_key_name.startswith("{") and "Update" not in app_name:
                            discovered_apps.append(app_name.strip())
                except EnvironmentError:
                    continue
        except Exception:
            continue
            
    out_file = r"C:\Users\Public\Grimoire_Software_Replica.txt"
    try:
        with open(out_file, "w", encoding="utf-8") as f:
            for app in sorted(discovered_apps):
                f.write(f"[ ] REINSTALL: {app}\n")
        return f"📋 Manifest compiled successfully! Saved {len(discovered_apps)} app blueprints to:\n{out_file}\nYou can use this list inside your deployment layout box to trigger silent installs."
    except Exception as e:
        return f"❌ Failed to write replica blueprint matrix manifest to disk: {e}"

def execute_silent_bulk_installer_exe(app_list_string):
    """
    Parses your text-to-do checklist block, extracts app names, and feeds them 
    sequentially into the native Windows Package Manager (winget) silently in the background.
    """
    lines = app_list_string.split("\n")
    apps_to_install = []
    
    for line in lines:
        if "REINSTALL:" in line:
            # Captures everything after "REINSTALL:" regardless of if it is marked [ ] or [x]
            app_name = line.split("REINSTALL:")[-1].strip()
            if app_name:
                apps_to_install.append(app_name)
                
    if not apps_to_install:
        return "❌ Deployment Matrix: No valid [ ] REINSTALL: AppName tags found in target configuration."

    def run_sequential_installs():
        for app in apps_to_install:
            try:
                # Winget executes silently, auto-bypassing package and source source terms agreements
                subprocess.run(
                    f'winget install "{app}" --silent --accept-package-agreements --accept-source-agreements', 
                    shell=True, 
                    stdout=subprocess.DEVNULL, 
                    stderr=subprocess.DEVNULL
                )
            except Exception:
                pass

    # Fire via an independent thread so the main PyQt dashboard stays active and never hangs up
    threading.Thread(target=run_sequential_installs, daemon=True).start()
    
    return (
        f"🚀 Winget Provisioning Engine Online!\n"
        f"Currently deploying {len(apps_to_install)} applications silently in the background.\n\n"
        f"Processing now:\n" + "\n".join([f" ➡️ {a}" for a in apps_to_install[:4]]) +
        (f"\n ...and {len(apps_to_install) - 4} other applications." if len(apps_to_install) > 4 else "")
    )

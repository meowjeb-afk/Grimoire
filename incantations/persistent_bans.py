# File: incantations/persistent_bans.py
import winreg
import os
import shutil

def freeze_windows_bloatware_policies():
    """Injects core Windows Explorer restriction policies to prevent blacklisted apps from running."""
    print("🔒 Solidifying anti-bloatware registry policy shields...")
    policy_path = r"Software\Microsoft\Windows\CurrentVersion\Policies\Explorer\DisallowRun"
    try:
        # Create or open the registry restriction pathway natively
        key = winreg.CreateKey(winreg.HKEY_CURRENT_USER, policy_path)
        # Set strict execution bans for standard Windows app intruders
        winreg.SetValueEx(key, "1", 0, winreg.REG_SZ, "CandyCrush.exe")
        winreg.SetValueEx(key, "2", 0, winreg.REG_SZ, "TikTok.exe")
        winreg.SetValueEx(key, "3", 0, winreg.REG_SZ, "BingNews.exe")
        winreg.CloseKey(key)
        return "🛡️ Policies locked! Injected persistent registry blocks against tracking executables."
    except Exception as e:
        return f"❌ Registry lock expansion rejected: {e}"

def backup_user_manifests(source_dir, backup_target="C:\\Users\\Public\\Grimoire_Backups"):
    """Creates copies of vital application profiles or structural layout text paths."""
    if not os.path.exists(source_dir):
        return "❌ Targeted configuration source profile path does not exist."
    try:
        os.makedirs(backup_target, exist_ok=True)
        folder_name = os.path.basename(os.path.normpath(source_dir))
        shutil.copytree(source_dir, os.path.join(backup_target, folder_name), dirs_exist_ok=True)
        return f"💾 Secure backup successfully stored inside: {backup_target}\\{folder_name}"
    except Exception as e:
        return f"❌ Critical backup sequence failed: {e}"

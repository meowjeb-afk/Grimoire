# File: incantations/ecosystem_summoner.py
import subprocess
import json
import os

def summon_bundle(progress_callback=None):
    """
    Reads the designated application manifest from runes.json and 
    installs everything silently via native Windows winget.
    """
    # Locate database relative to this portable script
    app_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    runes_path = os.path.join(app_root, "database", "runes.json")
    
    try:
        with open(runes_path, "r") as f:
            data = json.load(f)
        apps_to_install = data.get("ecosystem_bundle", [])
    except Exception as e:
        return f"❌ Failed to read manifest matrix: {e}"

    if not apps_to_install:
        return "🍂 Your ecosystem bundle manifest is empty. Add App IDs to your runes.json first."

    log_output = ["🚀 Starting fresh deployment protocol...\n"]
    
    for app_id in apps_to_install:
        msg = f"📦 Summoning {app_id}... "
        if progress_callback:
            progress_callback(msg)
            
        # --silent forces it to install without opening wizards
        # --accept-package-agreements & --accept-source-agreements skip prompt blockers
        cmd = [
            "winget", "install", "--id", app_id, 
            "--silent", "--accept-package-agreements", "--accept-source-agreements"
        ]
        
        try:
            result = subprocess.run(cmd, capture_output=True, text=True, check=True)
            log_output.append(f"✓ Successfully installed: {app_id}")
        except subprocess.CalledProcessError as e:
            log_output.append(f"⚠️ Failed or already present: {app_id} (Code: {e.returncode})")
            
    return "\n".join(log_output)

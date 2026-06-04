import subprocess

def scan_for_updates():
    """Scans the local machine for any apps that have pending updates available."""
    print("🔮 Scrying for outdated application matrices...")
    try:
        # Run 'winget upgrade' in the background to fetch the list
        result = subprocess.run(
            ["winget", "upgrade"], 
            capture_output=True, 
            text=True, 
            creationflags=subprocess.CREATE_NO_WINDOW
        )
        
        if "No available upgrade found" in result.stdout:
            return "✨ All local software applications are fully up to date."
        
        # Extract the relevant lines showing what needs updating
        lines = result.stdout.split('\n')
        updates_found = []
        for line in lines:
            if any(x in line for x in ["Version", "Available", "---"]):
                continue
            if line.strip():
                updates_found.append(line.split('   ')[0].strip())
                
        if not updates_found:
            return "✨ No urgent updates detected."
            
        return "\n".join(updates_found[:10]) # Return top 10 outdated apps
    except Exception as e:
        return f"❌ Failed to query winget updater engine: {e}"

def cast_all_upgrades():
    """Executes a global upgrade command for all outdated applications."""
    print("⚡ Activating mass upgrade sequence...")
    try:
        # '--all' updates everything, '--silent' hides installer wizard windows
        subprocess.Popen(
            ["winget", "upgrade", "--all", "--silent"],
            creationflags=subprocess.CREATE_NO_WINDOW
        )
        return "⚡ Mass upgrade running silently in the background!"
    except Exception as e:
        return f"❌ Upgrade catalyst failed: {e}"

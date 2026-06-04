import os

HOSTS_PATH = r"C:\Windows\System32\drivers\etc\hosts"
BLOCKLIST_DOMAINS = [
    "vortex.data.microsoft.com", "settings-win.data.microsoft.com",
    "telemetry.microsoft.com", "diagnostics.support.microsoft.com"
]

def toggle_void_shield(activate=True):
    """Appends or clears telemetry tracking bans directly in the system hosts layer."""
    if not os.path.exists(HOSTS_PATH):
        return "❌ Critical OS error: System hosts configuration matrix absent."
        
    try:
        with open(HOSTS_PATH, "r") as f:
            lines = f.readlines()
            
        # Clean current blocklist lines out first
        new_lines = [line for line in lines if not any(domain in line for domain in BLOCKLIST_DOMAINS)]
        
        if activate:
            new_lines.append("\n# Grimoire Void Shield Active\n")
            for domain in BLOCKLIST_DOMAINS:
                new_lines.append(f"127.0.0.1    {domain}\n")
            status = "🛡️ Void Shield raised! Windows tracking domains locked into routing loops."
        else:
            status = "🔓 Void Shield lowered. Network tracking boundary parameters restored."
            
        with open(HOSTS_PATH, "w") as f:
            f.writelines(new_lines)
        return status
    except PermissionError:
        return "❌ Administrative authentication failure. Execute Grimoire as Administrator."

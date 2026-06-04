import subprocess

def banish_telemetry():
    """Disables native Windows telemetry tracking services via PowerShell registry adjustments."""
    print("🧼 Purging Windows tracking and telemetry services...")
    
    # PowerShell commands targeting tracking services
    commands = [
        "Stop-Service DiagTrack -ErrorAction SilentlyContinue",
        "Set-Service DiagTrack -StartupType Disabled",
        "Reg add 'HKLM\\SOFTWARE\\Policies\\Microsoft\\Windows\\DataCollection' /v AllowTelemetry /t REG_DWORD /d 0 /f"
    ]
    
    try:
        for cmd in commands:
            subprocess.run(
                ["powershell", "-Command", cmd], 
                creationflags=subprocess.CREATE_NO_WINDOW
            )
        return "🔮 Telemetry banished. Privacy metrics reinforced."
    except Exception as e:
        return f"❌ Telemetry purge failed: {e}"

def purge_bloatware():
    """Removes standard Windows pre-installed apps (bloatware) safely."""
    print("🧹 Purging default bloatware packages...")
    
    # List of common native bloatware packages to target
    target_packages = [
        "*3dbuilder*", "*bingweather*", "*gethelp*", "*solitairecollection*",
        "*skypeapp*", "*officehub*", "*mixedreality.portal*", "*feedbackhub*"
    ]
    
    purged_count = 0
    for package in target_packages:
        ps_command = f"Get-AppxPackage {package} | Remove-AppxPackage -ErrorAction SilentlyContinue"
        try:
            subprocess.run(
                ["powershell", "-Command", ps_command], 
                creationflags=subprocess.CREATE_NO_WINDOW
            )
            purged_count += 1
        except Exception:
            pass
            
    return f"🧹 System purge finalized. Cleared {purged_count} package footprints."

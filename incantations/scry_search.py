import os
from pathlib import Path

def rapid_file_scry(search_term, root_dir="C:\\"):
    """Quickly scans directories matching specific filenames or extensions."""
    print(f"🔍 Scrying filesystem structures for: {search_term}...")
    matches = []
    search_term = search_term.lower()
    
    try:
        # Loop through files, skipping common protected system folders
        for root, dirs, files in os.walk(root_dir):
            # Prune directories in place to prevent deep loops into system data
            dirs[:] = [d for d in dirs if d not in ["AppData", "Windows", "ProgramData"]]
            
            for file in files:
                if search_term in file.lower():
                    full_path = os.path.join(root, file)
                    matches.append(full_path)
                    if len(matches) >= 15: # Cap at top 15 results for performance
                        break
            if len(matches) >= 15:
                break
    except Exception as e:
        return f"Scan scan breakdown: {e}"
        
    if not matches:
        return "🍂 No file configurations matched your query criteria."
        
    return "\n".join(matches)

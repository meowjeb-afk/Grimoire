import os
import requests
from pathlib import Path

def summon_assets(keyword, save_directory="C:\\Users\\Public\\Downloads"):
    """Queries public domain endpoints to auto-harvest design assets."""
    print(f"📡 Summoning creative assets for tag: {keyword}...")
    url = f"https://openverse.org/api/v1/images/?q={keyword}"
    
    try:
        response = requests.get(url, headers={"User-Agent": "GrimoireHub/1.0"}, timeout=10)
        if response.status_code != 200:
            return
            
        data = response.json()
        results = data.get("results", [])
        
        target_path = Path(save_directory) / "Summoned_Assets"
        target_path.mkdir(parents=True, exist_ok=True)
        
        for idx, item in enumerate(results[:5], start=1): # Limit to 5 files per cast
            img_url = item.get("url")
            if img_url and img_url.startswith("http"):
                img_data = requests.get(img_url, timeout=10).content
                file_name = f"summoned_{keyword}_{idx}.jpg"
                
                with open(target_path / file_name, "wb") as f:
                    f.write(img_data)
                print(f"📥 Manifested asset: {file_name}")
                
    except Exception as e:
        print(f"❌ Asset summoning interrupted: {e}")

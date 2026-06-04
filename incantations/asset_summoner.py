# File: incantations/asset_summoner.py
import os
import requests
from pathlib import Path

def summon_clean_assets(keyword, save_directory="C:\\Users\\Public\\Downloads"):
    """
    Queries open-access repositories, strictly filtering for 
    Public Domain / CC0 assets to ensure immaculate, unwatermarked data entry.
    """
    print(f"📡 Summoning verified public domain assets for: {keyword}...")
    
    # 'license_type=CC0' filters exclusively for Public Domain Dedication files
    url = f"https://openverse.org/api/v1/images/?q={keyword}&license_type=CC0"
    
    try:
        response = requests.get(url, headers={"User-Agent": "GrimoireSuite/2.0"}, timeout=10)
        if response.status_code != 200:
            return f"❌ Library connection bottleneck. Status code: {response.status_code}"
            
        data = response.json()
        results = data.get("results", [])
        
        if not results:
            return "🍂 No public domain configurations matched this specific tag."
        
        target_path = Path(save_directory) / "Summoned_Assets"
        target_path.mkdir(parents=True, exist_ok=True)
        
        downloaded_count = 0
        for idx, item in enumerate(results[:5], start=1):  # Cap at 5 clean assets per cast
            img_url = item.get("url")
            if img_url and img_url.startswith("http"):
                try:
                    img_data = requests.get(img_url, timeout=10).content
                    # Keep track of file formats dynamically based on the source extension
                    ext = Path(img_url).suffix if Path(img_url).suffix in ['.jpg', '.png', '.jpeg'] else '.jpg'
                    file_name = f"clean_{keyword}_{idx}{ext}"
                    
                    with open(target_path / file_name, "wb") as f:
                        f.write(img_data)
                    downloaded_count += 1
                except Exception:
                    continue  # Skip broken URLs gracefully
                    
        return f"📥 Harvest finalized. Manifested {downloaded_count} pristine, high-fidelity assets inside /Summoned_Assets."
                
    except Exception as e:
        return f"❌ Asset summoning interrupted: {e}"

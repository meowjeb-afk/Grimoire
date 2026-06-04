import os
import shutil
from pathlib import Path

FILE_CATEGORIES = {
    "3D_Models": [".stl", ".obj", ".fbx", ".blend"],
    "Images": [".png", ".jpg", ".jpeg", ".gif", ".webp"],
    "Documents": [".pdf", ".docx", ".txt", ".md"],
    "Zips_and_Mods": [".zip", ".rar", ".7z"]
}

def transmute_folder(target_dir):
    """Sorts files into designated category folders."""
    target_path = Path(target_dir)
    if not target_path.exists():
        return f"Path generic error: {target_dir} not found."

    moved = 0
    for item in target_path.iterdir():
        if item.is_file():
            file_ext = item.suffix.lower()
            dest_folder = "Uncategorized"
            
            for category, extensions in FILE_CATEGORIES.items():
                if file_ext in extensions:
                    dest_folder = category
                    break
            
            category_path = target_path / dest_folder
            category_path.mkdir(exist_ok=True)
            
            if not (category_path / item.name).exists():
                shutil.move(str(item), str(category_path / item.name))
                moved += 1
    return f"Success! Organized {moved} files."

def bulk_rename(folder_path, prefix):
    """Sequentially renames files to Prefix_001, Prefix_002, etc."""
    target_path = Path(folder_path)
    if not target_path.exists():
        return
    
    files = [f for f in target_path.iterdir() if f.is_file()]
    files.sort()
    
    for index, file_path in enumerate(files, start=1):
        new_name = f"{prefix}_{index:03d}{file_path.suffix}"
        file_path.rename(file_path.parent / new_name)

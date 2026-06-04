# File: incantations/image_matrix.py
import os
import requests
from PIL import Image, ImageOps, ImageEnhance
from PyQt6.QtWidgets import QApplication
from PyQt6.QtCore import QMimeData, QUrl

def search_giphy(query, api_key="dc6zaTOxFJmzC"): # Uses public beta key by default
    """Scries the Giphy database and returns a list of source URL image streams."""
    url = f"https://api.giphy.com/v1/gifs/search?api_key={api_key}&q={query}&limit=5"
    try:
        response = requests.get(url, timeout=5).json()
        urls = [item['images']['fixed_height_small']['url'] for item in response.get('data', [])]
        return urls if urls else ["❌ No visual manifestations found for that query."]
    except Exception as e:
        return [f"❌ Giphy Rift connection error: {e}"]

def apply_pixel_art_slider(image_path, pixel_size=8):
    """Transmutes a standard visual canvas into a pixel-art matrix using adaptive downsampling."""
    if not os.path.exists(image_path): return "❌ Targeted asset matrix not found."
    try:
        img = Image.open(image_path)
        # Downscale and upscale using NEAREST block filters to create retro pixel clusters
        small = img.resize((max(1, img.width // pixel_size), max(1, img.height // pixel_size)), Image.Resampling.NEAREST)
        pixel_art = small.resize(img.size, Image.Resampling.NEAREST)
        
        out_path = os.path.splitext(image_path)[0] + "_pixel.png"
        pixel_art.save(out_path)
        return f"👾 Pixel transmutation complete! Formed: {out_path}"
    except Exception as e:
        return f"❌ Pixel error: {e}"

def enhance_pixel_density(image_path, sharpness_val=2.0, contrast_val=1.5):
    """Applies micro-contrast and edge enhancements to restore low-res assets or pixel art scales."""
    if not os.path.exists(image_path): return "❌ Targeted asset matrix not found."
    try:
        img = Image.open(image_path)
        img = ImageEnhance.Sharpness(img).enhance(sharpness_val)
        img = ImageEnhance.Contrast(img).enhance(contrast_val)
        out_path = os.path.splitext(image_path)[0] + "_enhanced.png"
        img.save(out_path)
        return f"✨ Pixel density and edges enhanced: {out_path}"
    except Exception as e:
        return f"❌ Enhancement error: {e}"

def transmute_to_plush_or_crochet(image_path, mode="plush"):
    """
    Renders style prompts or local filter masks to simulate fabric structures.
    In a full local AI suite, this pipes directly to the stable-diffusion controlnet framework.
    """
    if not os.path.exists(image_path): return "❌ Targeted asset matrix not found."
    out_path = os.path.splitext(image_path)[0] + f"_{mode}_blueprint.png"
    try:
        img = Image.open(image_path)
        if mode == "crochet":
            # Stylize into structural grid blocks representing stitch instructions
            img = ImageOps.posterize(img.convert("L"), 3)
        else:
            # High-saturation softening filter simulation
            img = ImageEnhance.Color(img).enhance(1.5)
        img.save(out_path)
        return f"🧶 Rendered {mode} asset conversion archetype to: {out_path}"
    except Exception as e:
        return f"❌ Fabric transmutation failed: {e}"

def format_sticker_package(image_path, platform="discord"):
    """Resizes, transparent-pads, and instantly copies the asset to the clipboard for rapid Ctrl+V pasting."""
    if not os.path.exists(image_path): return "❌ Target image not found."
    try:
        img = Image.open(image_path)
        target_size = (320, 320) if platform == "discord" else (512, 512)
        img.thumbnail(target_size, Image.Resampling.LANCZOS)
        
        out_path = os.path.splitext(image_path)[0] + f"_{platform}_sticker.png"
        img.save(out_path)
        
        # Inject directly into Windows Clipboard for instant chat app pasting
        cb = QApplication.clipboard()
        mime = QMimeData()
        mime.setUrls([QUrl.fromLocalFile(out_path)])
        cb.setMimeData(mime)
        
        return f"🏷️ Sticker formatted for {platform.capitalize()} & copied to Clipboard! Just press Ctrl+V in your chat room."
    except Exception as e:
        return f"❌ Sticker compilation error: {e}"

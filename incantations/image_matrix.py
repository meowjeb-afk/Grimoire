import os
from pathlib import Path
from PIL import Image, ImageFilter, ImageEnhance
from rembg import remove

def erase_background(image_path):
    """Leverages a local U2Net model to cleanly strip image backgrounds entirely offline."""
    print("🔮 Banishing visual backgrounds from canvas...")
    path = Path(image_path)
    if not path.exists():
        return "❌ Source asset image file path is invalid."
        
    try:
        output_path = path.parent / f"{path.stem}_no_bg.png"
        with open(path, 'rb') as i_file:
            input_data = i_file.read()
            # rembg processes the raw bytes locally and cuts out the alpha channel
            output_data = remove(input_data)
        with open(output_path, 'wb') as o_file:
            o_file.write(output_data)
        return f"✨ Background severed successfully!\nSaved to: {output_path.name}"
    except Exception as e:
        return f"❌ Background extraction failed: {e}"

def remaster_and_upscale(image_path, scale_factor=2):
    """Applies structural sharpening, color remastering, and high-fidelity sampling."""
    print(f"🚀 Initializing asset remaster and {scale_factor}x scale matrix...")
    path = Path(image_path)
    if not path.exists():
        return "❌ Target image file not found."

    try:
        with Image.open(path) as img:
            # 1. High-Fidelity Lanczos Sampling Reconstruction
            new_size = (int(img.width * scale_factor), int(img.height * scale_factor))
            upscaled_img = img.resize(new_size, resample=Image.Resampling.LANCZOS)
            
            # 2. Visual Remastering Layer (Enhancing local detail matrices)
            # Denoise/Smooth micro-grain via Unsharp Masking
            sharper = upscaled_img.filter(ImageFilter.UnsharpMask(radius=2, percent=150, threshold=3))
            
            # Boost color saturation and contrast for a vivid, rich asset finish
            color_engine = ImageEnhance.Color(sharper)
            vivid = color_engine.enhance(1.15)
            contrast_engine = ImageEnhance.Contrast(vivid)
            remastered_final = contrast_engine.enhance(1.05)
            
            output_path = path.parent / f"{path.stem}_remastered.png"
            remastered_final.save(output_path, "PNG")
            return f"✨ Remaster complete!\nDimensions scaled to {new_size[0]}x{new_size[1]}.\nFile: {output_path.name}"
    except Exception as e:
        return f"❌ Remaster execution failed: {e}"

def convert_format(image_path, target_format):
    """Transmutes image configurations between formats (PNG, JPG, WEBP, ICO)."""
    print(f"✨ Transmuting image asset format to {target_format.upper()}...")
    path = Path(image_path)
    if not path.exists():
        return "❌ Source file undetected."
        
    target_format = target_format.strip().lower()
    valid_formats = ["png", "jpeg", "webp", "ico"]
    if target_format not in valid_formats:
        return f"❌ Unsupported output format. Select: {', '.join(valid_formats).upper()}"

    try:
        with Image.open(path) as img:
            # Handle alpha channel conversions if saving down to standard JPEG formats
            if target_format in ["jpeg", "jpg"] and img.mode in ('RGBA', 'LA'):
                background = Image.new('RGB', img.size, (255, 255, 255))
                background.paste(img, mask=img.split()[3])
                img = background
            
            ext = "jpg" if target_format == "jpeg" else target_format
            output_path = path.parent / f"{path.stem}_converted.{ext}"
            
            # Set structural adjustments if building true Windows app icon sets
            if target_format == "ico":
                icon_sizes = [(16, 16), (32, 32), (48, 48), (64, 64), (128, 128), (256, 256)]
                img.save(output_path, format="ICO", sizes=icon_sizes)
            else:
                img.save(output_path, format=target_format.upper(), quality=95)
                
            return f"✨ Conversion successful!\nSaved file: {output_path.name}"
    except Exception as e:
        return f"❌ Transmutation sequence failed: {e}"

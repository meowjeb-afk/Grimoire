# File: incantations/layout_runes.py
from PIL import Image, ImageDraw, ImageFont

def draw_procedural_logo(text="GRIMOIRE", radius_size=20, border_thickness=4):
    """Generates a high-fidelity vector-style logo bounding layout based on image_249083.png aesthetics."""
    # Build canvas asset frame
    img = Image.new("RGBA", (500, 150), (22, 19, 28, 255))
    draw = ImageDraw.Draw(img)
    
    # Draw rounded pill bounding frame container layout
    draw.rounded_rectangle(
        [10, 10, 490, 140], 
        radius=radius_size, 
        fill=(12, 10, 15, 255), 
        outline=(0, 255, 204, 255), 
        width=border_thickness
    )
    
    # Render fallback graphical typography
    draw.text((250, 75), text, fill=(255, 255, 255, 255), anchor="mm", font=None)
    
    out_path = r"C:\Users\Public\Grimoire_Procedural_Logo.png"
    img.save(out_path)
    return f"🎨 Logo template vector canvas constructed at: {out_path}"

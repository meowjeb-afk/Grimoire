import random
from PIL import Image, ImageDraw

def generate_palette(base_hex="#00ffcc"):
    """Generates five complementary dark fantasy or gothic-cute theme color codes."""
    print(f"🎨 Forging visual palette around: {base_hex}")
    # Fallback mock colors for fast palette rendering
    palettes = [base_hex, "#15121a", "#6a6475", "#0c0a0f", "#ff007f"]
    return " ✨ Generated Palette Matrix:\n " + " | ".join(palettes)

def craft_procedural_texture(filename="texture.png"):
    """Generates a seamless 256x256 mossy/noise canvas background texture."""
    img = Image.new("RGB", (256, 256), color=(21, 18, 26))
    draw = ImageDraw.Draw(img)
    for _ in range(3000):
        x, y = random.randint(0, 255), random.randint(0, 255)
        draw.point((x, y), fill=(random.randint(10, 40), random.randint(120, 200), 150))
    img.save(filename)
    return f"✨ Procedural texture map saved as: {filename}"

def build_favicon(source_img_path):
    """Converts any creative artwork file into a multi-layer production web icon."""
    try:
        with Image.open(source_img_path) as img:
            out_path = os.path.splitext(source_img_path)[0] + "_favicon.ico"
            img.save(out_path, format="ICO", sizes=[(16,16), (32,32), (48,48)])
            return f"✨ Favicon generated: {os.path.basename(out_path)}"
    except Exception as e:
        return f"❌ Favicon conversion broke: {e}"

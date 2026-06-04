# File: incantations/asset_summoner.py
import requests
import json

def local_offline_ai_forge(prompt, negative_prompt="", steps=20, cfg_scale=7.0, width=512, height=512, sketch_path=None):
    """
    Connects to a local offline Stable Diffusion instance via the standard WebUI API port 7860.
    Operates completely offline with zero limits, constraints, or filtering.
    """
    # Fallback simulation if the local background server isn't actively running yet
    url = "http://127.0.0.1:7860/sdapi/v1/txt2img" if not sketch_path else "http://127.0.0.1:7860/sdapi/v1/img2img"
    
    payload = {
        "prompt": prompt,
        "negative_prompt": negative_prompt,
        "steps": int(steps),
        "cfg_scale": float(cfg_scale),
        "width": int(width),
        "height": int(height)
    }
    
    try:
        # Intentional 2-second timeout check to see if local WebUI engine is awake
        response = requests.post(url, json=payload, timeout=2)
        if response.status_code == 200:
            return "🎨 Visual asset synthesized offline successfully by local GPU array!"
    except Exception:
        pass
        
    return f"🔮 Offline AI Matrix Standby:\nEngine path generated with no restrictions.\n[PROMPT]: {prompt}\n[CFG Scale]: {cfg_scale}\n(To render, verify your local WebUI backend is listening on port 7860)."

def architect_game_asset_prompt(base_idea, style="Pixel Art"):
    """Transforms a simple concept into a hyper-detailed layout prompt optimized for game developer assets."""
    modifiers = {
        "Pixel Art": "isometric 16-bit pixel art sprite, clean lines, vibrant retro colors, video game asset, transparent background",
        "3D Model/Slicer": "low poly 3D model style render, game engine asset, highly detailed textures, orthographic projection",
        "Gothic Cute": "creepy-cute gothic cottagecore style asset, highly detailed ink linework, muted pastel colors, clean sticker border"
    }
    selected_mod = modifiers.get(style, "highly detailed vector sprite asset, transparent background")
    return f"{base_idea}, {selected_mod} --v 6.0"

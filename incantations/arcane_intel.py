import requests
import pyperclip

def cast_ai_rewrite():
    """Intercepts clipboard text, passes it to the local LLM, and replaces it with the output."""
    input_text = pyperclip.paste()
    if not input_text:
        return "Clipboard is completely empty. Place an ink string inside first."
        
    print(f"🧠 Consulting local Arcane Intelligence matrix...")
    url = "http://localhost:11434/api/generate"
    payload = {
        "model": "llama3",
        "prompt": f"Clean up, proofread, and optimize the following text or code. Maintain its core intent but elevate its structure:\n\n{input_text}",
        "stream": False
    }
    
    try:
        response = requests.post(url, json=payload, timeout=30)
        if response.status_code == 200:
            ai_output = response.json().get("response", "").strip()
            pyperclip.copy(ai_output)
            return "✨ AI Transmutation complete! Output injected into your clipboard."
        return f"❌ AI Engine responded with status error code: {response.status_code}"
    except Exception as e:
        return "❌ Local AI Core offline. Ensure the Ollama engine service is active on your machine."

import keyboard
import pyperclip

def wrap_clipboard_incantation():
    """Grabs clipboard text and wraps it cleanly in markdown code blocks."""
    original_text = pyperclip.paste()
    if not original_text:
        return
        
    # Wrap text in clear code block format
    transformed_text = f"```text\n{original_text}\n```"
    pyperclip.copy(transformed_text)
    print("🔮 Spell Cast: Clipboard wrapped successfully.")

def summon_keyboard_listener():
    """Starts listening for global hotkeys."""
    keyboard.add_hotkey('ctrl+shift+h', wrap_clipboard_incantation)
    keyboard.wait()

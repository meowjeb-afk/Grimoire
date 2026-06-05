"""
Clipboard Grimoire Module
Handles clipboard history tracking and snippet management.
"""
import json
import os
from PyQt6.QtCore import QObject, pyqtSignal

class ClipboardGrimoire(QObject):
    history_updated = pyqtSignal(list)

    def __init__(self, clipboard):
        """
        Initializes the Clipboard Grimoire engine.
        Connects to the system clipboard to track changes.
        """
        super().__init__()
        self.clipboard = clipboard
        self.history = []
        self.max_history = 50  # Keep last 50 items
        
        self.snippets_file = os.path.join(os.path.dirname(__file__), "snippets.json")
        self.snippets = self.load_snippets()
        
        # Connect to clipboard change signal
        self.clipboard.dataChanged.connect(self._on_clipboard_change)
        print("[ClipboardGrimoire] Engine initialized.")

    def _on_clipboard_change(self):
        """
        Callback triggered when the system clipboard changes.
        Adds the new text to the history list.
        """
        text = self.clipboard.text()
        if text and (not self.history or self.history[0] != text):
            self.history.insert(0, text)
            # Trim history to max size
            self.history = self.history[:self.max_history]
            self.history_updated.emit(self.history)

    def load_snippets(self):
        """
        Loads saved snippets from the JSON config file.
        """
        if os.path.exists(self.snippets_file):
            try:
                with open(self.snippets_file, 'r') as f:
                    return json.load(f)
            except Exception as e:
                print(f"[Warning] Failed to load snippets: {e}")
        return {}

    def save_snippets(self):
        """
        Saves snippets to the JSON config file.
        """
        try:
            with open(self.snippets_file, 'w') as f:
                json.dump(self.snippets, f, indent=4)
        except Exception as e:
            print(f"[Error] Failed to save snippets: {e}")

    def add_snippet(self, key, value):
        """
        Adds a new snippet to the library.
        """
        self.snippets[key] = value
        self.save_snippets()
        print(f"[Success] Added snippet: {key}")

    def remove_snippet(self, key):
        """
        Removes a snippet from the library.
        """
        if key in self.snippets:
            del self.snippets[key]
            self.save_snippets()
            print(f"[Success] Removed snippet: {key}")

    def get_history(self):
        """
        Returns the current clipboard history.
        """
        return self.history

    def clear_history(self):
        """
        Clears the clipboard history.
        """
        self.history = []
        self.history_updated.emit(self.history)
        print("[Success] Clipboard history cleared.")

"""
Automation Weaver Module
Handles idle time detection and task scheduling triggers.
"""
import ctypes
import json
import os

class AutomationWeaver:
    def __init__(self):
        """
        Initializes the Automation Weaver engine.
        Loads existing spells from the JSON config file.
        """
        self.spells_file = os.path.join(os.path.dirname(__file__), "weaver_spells.json")
        self.spells = self.load_spells()
        print("[AutomationWeaver] Engine initialized.")

    def get_idle_time(self):
        """
        Returns the system idle time in seconds (Windows only).
        Uses the Win32 API GetLastInputInfo function.
        """
        class LASTINPUTINFO(ctypes.Structure):
            _fields_ = [("cbSize", ctypes.c_uint), ("dwTime", ctypes.c_uint)]
        
        lii = LASTINPUTINFO()
        lii.cbSize = ctypes.sizeof(LASTINPUTINFO)
        
        if ctypes.windll.user32.GetLastInputInfo(ctypes.byref(lii)):
            millis = ctypes.windll.kernel32.GetTickCount() - lii.dwTime
            return millis / 1000.0
        return 0.0

    def load_spells(self):
        """
        Loads automation spells from the JSON config file.
        """
        if os.path.exists(self.spells_file):
            try:
                with open(self.spells_file, 'r') as f:
                    return json.load(f)
            except Exception as e:
                print(f"[Warning] Failed to load spells: {e}")
        return []

    def save_spells(self):
        """
        Saves automation spells to the JSON config file.
        """
        try:
            with open(self.spells_file, 'w') as f:
                json.dump(self.spells, f, indent=4)
        except Exception as e:
            print(f"[Error] Failed to save spells: {e}")

    def add_spell(self, name, trigger_type, target_module):
        """
        Adds a new automation spell to the list.
        """
        spell = {
            "name": name, 
            "trigger": trigger_type, 
            "target": target_module, 
            "active": True
        }
        self.spells.append(spell)
        self.save_spells()
        print(f"[Success] Added spell: {name}")
        return spell

    def remove_spell(self, index):
        """
        Removes a spell by index.
        """
        if 0 <= index < len(self.spells):
            removed = self.spells.pop(index)
            self.save_spells()
            print(f"[Success] Removed spell: {removed['name']}")
            return removed
        return None

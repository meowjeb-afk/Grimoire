import tkinter as tk
from tkinter import font

def scry_installed_fonts():
    """Queries the OS engine to catalog every accessible font family name."""
    root = tk.Tk()
    root.withdraw()
    system_fonts = sorted(list(font.families()))
    root.destroy()
    return "\n".join(system_fonts[:20]) + f"\n...and {len(system_fonts)-20} more fonts cataloged."

def get_paper_spec(size_name):
    """Returns the precise physical blueprint dimensions for manufacturing layouts."""
    specs = {
        "A4": "210 x 297 mm | 8.3 x 11.7 inches (Standard Print)",
        "A3": "297 x 420 mm | 11.7 x 16.5 inches (Poster Matrix)",
        "A5": "148 x 210 mm | 5.8 x 8.3 inches (Booklet/Zine Manual)",
        "Letter": "215.9 x 279.4 mm | 8.5 x 11.0 inches (Legacy Document)"
    }
    return specs.get(size_name.strip(), "🍂 Unknown layout size definition.")

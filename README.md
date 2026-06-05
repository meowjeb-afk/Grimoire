# Grimoire 📖✨

Grimoire is an open-source, portable, administrative optimization suite and custom Windows shell utility powered by Python and PyQt6. Designed for creators, developers, and power users, Grimoire acts as an automated "book of spells"—running natively in the Windows system tray to execute heavy OS automation, privacy hardening, system debloating, and local machine learning tasks.

By decoupling the high-performance system automation backend from the graphical user interface via asynchronous thread pools, Grimoire maintains a fluid, low-overhead system footprint without sacrificing multi-layered operational stability.

---

## 🔮 Active Incantations (Core Modules)

Grimoire organizes its core system hooks into specialized sub-modules:

* **Arcane Intelligence (`arcane_intel.py`):** Integrates directly with local, offline LLM model matrices (via Ollama) to execute hardware-accelerated text refactoring and code optimizations directly within the Windows clipboard.
* **Void Shield (`void_shield.py`):** A boundary-layer privacy filter that programmatically intercepts and disables Windows telemetry, data collection routes, and background tracking servers at the OS hosts configuration layer.
* **File Alchemy & Scrying (`file_alchemy.py` & `scry_search.py`):** Features automated extensions sorting, bulk asset indexing routines, and a low-level MFT-style rapid filesystem search engine that bypasses standard Windows Explorer delays.
* **Purge Engine (`purge_debloat.py`):** Leverages administrative PowerShell subprocess wrappers to cleanly strip pre-installed system bloatware packages and telemetry services.
* **Workspace Stasis (`workspace_stasis.py`):** Captures multi-monitor win32 process handles and pixel geometry coordinates to snapshot and freeze custom application grid layouts.
* **Text & Keyboard Alchemy (`text_expansion.py` & `clipboard_magic.py`):** Drives system-wide asynchronous hotkey listeners to intercept and format text buffers or dynamically substitute custom typed abbreviations on the fly.

---

## 📐 Project Architecture

The architecture maintains strict decoupling between the graphical rendering engine and background thread executors:

```

Grimoire_OS/  <-- (Your Root Folder)
│
├── main.py                 <-- (The new entry point. You run this!)
├── ui_dashboard_OLD.py     <-- (Your old monolithic file. Renamed so it doesn't interfere)
│
── assets/                 <-- (Your images and icons. Untouched)
│   ├── grimoire_logo.png
│   ├── grimoire_text.png
│   ├── 0.png
│   └── ...
│
├── incantations/           <-- (Your existing backend logic. Untouched)
│   ├── __init__.py
│   ├── file_alchemy.py
│   ├── image_matrix.py
│   ├── deep_cleaner.py
│   └── ...
│
├── core/                   <-- (NEW: The AI engines we just added)
│   ├── __init__.py
│   ├── ai_suite.py         <-- (DesignSuite & AdvancedDesignExtensions)
│   └── workers.py          <-- (Background threading)
│
└── ui/                     <-- (NEW: The modularized PyQt6 interface)
    ├── __init__.py
    ├── custom_widgets.py   <-- (Nav buttons, charts, visualizer)
    ├── main_window.py      <-- (The main GrimoireMirror class)
    └── tabs.py             <-- (Dashboard, Visual Alchemy, Task Viewer, etc.)

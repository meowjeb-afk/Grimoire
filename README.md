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

Grimoire/
├── main.py                  # Auto-elevated master bootloader & system tray layer
├── ui_dashboard.py          # Asynchronous, multi-tab PyQt6 UI Control panel
├── database/
│   └── runes.json           # Local relative configuration data matrix
├── incantations/            # Discrete, dynamic automation modules
│   ├── __init__.py          
│   ├── arcane_intel.py      # Local LLM integration (Ollama)
│   ├── asset_summoner.py    # Automated design asset API harvester
│   ├── clipboard_magic.py   # Global clipboard interception tools
│   ├── file_alchemy.py      # Extension-based directory organization
│   ├── purge_debloat.py     # Native Windows package purging
│   ├── scry_search.py       # High-performance filesystem scanning
│   ├── text_expansion.py    # Real-time keyboard shorthand expands
│   ├── updater_scryer.py    # Winget application scanner
│   ├── void_shield.py       # Hosts-layer telemetry firewall
│   └── workspace_stasis.py  # Win32 window coordinate snapshots
└── assets/                  # Custom visual themes, UI profiles, and icons

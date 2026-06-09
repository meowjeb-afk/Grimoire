
---

# 🔮 #  Grimoire

[![Python 3.10+](https://img.shields.io/badge/Python-3.10+-blue.svg)](https://www.python.org/downloads/)
[![UI PyQt6](https://img.shields.io/badge/UI-PyQt6-green.svg)](https://www.riverbankcomputing.com/software/pyqt/)
[![License MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Status Production Ready](https://img.shields.io/badge/Status-Production_Ready-brightgreen)]()

**The Ultimate Arcane Power-User Utility Suite.**

A comprehensive, non-blocking, and cryptographically secure desktop application for system maintenance, privacy warding, network diagnostics, and workflow automation. Built with a dark, gothic aesthetic for developers, power users, and digital artisans.

---

## 📜 About The Grimoire

Grimoire is not just another system utility; it is a unified command center. Built with a modular, multithreaded architecture in Python and PyQt6, it ensures that heavy operations (like bulk software installation, image processing, or system scanning) never freeze the user interface.

From securely shredding sensitive files to blocking telemetry at the DNS level and managing encrypted secrets, the Grimoire provides a sleek interface to wield total control over your digital environment.

---

## ✨ Core Incantations (Features)

### 🏠 Core & Telemetry
*   **The Altar (Dashboard):** A 5-column read-only status screen monitoring system health, storage, temperatures, and startup impact.
*   **Arcane Scratchpad:** Persistent markdown notepad saved locally between sessions.
*   **Task Viewer:** Live process manager with sorting, filtering, and termination capabilities.

### 🧹 Cleanse
*   **Essence Siphon:** The master system cleaner.
    *   *Dust & Cobwebs:* Clears temp files, thumbnails, browser caches, and the Recycle Bin.
    *   *Shadow Purge:* Identifies registry orphans and clears the Windows Update cache.
    *   *Deep Artifacts:* Excavates Memory Dumps, Windows Error Reporting (WER), and old logs.
    *   *Weightless Ritual:* Flushes inactive RAM working-sets and stops high-RAM background services.

### ⚡ Optimize & Deploy
*   **Transmutation Array (Tuning):** RAM sweeping, workspace layout stasis (capture/restore), and window anchoring (opacity/pinning).
*   **Binding Rites (Deployment):** 
    *   *Bloatware Remover:* Ninite-style checklist for removing pre-installed junk via Winget.
    *   *Software Vault:* Bulk installer for verified open-source/freeware applications.
    *   *Update Scryer:* Scans and upgrades outdated applications.
*   **Automation Weaver:** Global text expansion listener and HTML System Scribe report generator.

### 🛡️ Security & Privacy
*   **Privacy & Warding:** Consolidated anti-telemetry and forensic cleaning.
    *   *Telemetry & Tracking:* Disables DiagTrack, WAP Push, and Advertising ID via Services/Registry.
    *   *Casting Circles (Hosts):* Appends a massive blocklist to the system `hosts` file to block tracking domains at the DNS level (with backup/restore).
    *   *Network Cleansing:* Flushes DNS, resets Winsock, and releases/renews IP.
    *   *Forensic Clean:* Wipes Event Logs, Recent Files, and Run Dialog history.
*   **Warding Sigils:** Windows Firewall control, active TCP connection monitoring (Sentry's Eye), IP blocking, and a "Network Panic Kill" switch to instantly disable all adapters.
*   **Arcane Cipher:** Text/File encryption (AES-256), hashing (SHA-256/512, MD5), and encoding (Base64, ROT13, URL).

### ️ Tools & Intel
*   **Visual Alchemy:** Comprehensive image editor with dimensional scaling, live filters (Blur, Sharpen, Gamma), pixelation, color grading, palette extraction, and sticker creation.
*   **File Alchemy:** Secure file shredding (DoD-style overwrites) and rapid filesystem scrying (search).
*   **Ethereal Postmaster:** Gmail inbox intelligence—scan, bulk trash, and block senders via OAuth.
*   **Optical Scrying:** Full-screen capture and OCR text extraction using Tesseract.
*   **Browser Alchemy:** Scans and clears cache, cookies, history, and passwords across Chrome, Firefox, Edge, Brave, and Opera.
*   **Design Forge:** Advanced image processing for seamless textures, normal maps, and alpha compositing.

---

## ⚠️ Prerequisites

Before summoning the Grimoire, ensure your system meets these requirements:

1.  **Python 3.10 or higher** installed.
2.  **Tesseract OCR** (Required for Optical Scrying):
    *   *Windows:* Download from [UB-Mannheim Tesseract](https://github.com/UB-Mannheim/tesseract/wiki) and add to PATH during installation.
3.  **Administrator Privileges:** Features like Global Text Expansion, Audio Control, Registry/Hosts modification, and Service management require the application to be run as Administrator.

---

## ️ Installation & Setup

1.  **Clone the Repository:**
    ```bash
    git clone https://github.com/[Your-Username]/grimoire-mirror.git
    cd grimoire-mirror
    ```

2.  **Create and Activate a Virtual Environment (Recommended):**
    ```bash
    # Windows
    python -m venv venv
    venv\Scripts\activate

    # macOS / Linux
    python3 -m venv venv
    source venv/bin/activate
    ```

3.  **Install Dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

4.  **Launch the Grimoire:**
    ```bash
    python main.py
    ```
    *(On Windows, right-click your terminal and select "Run as Administrator" for full feature access).*

---

## 📦 Building for Deployment (Windows `.exe`)

To compile the Grimoire into a standalone, portable executable:

1.  Ensure `pyinstaller` is installed (included in `requirements.txt`).
2.  Run the build command:
    ```bash
    pyinstaller grimoire.spec --clean --noconfirm
    ```
3.  Your standalone application will be located in the `dist/GrimoireMirror/` directory.

---

## 🏗️ Architecture Overview

The codebase is strictly modular, separating UI logic from backend processing to ensure a buttery-smooth interface.

```text
grimoire-mirror/
├── main.py                  # Application entry point
├── requirements.txt         # Python dependencies
├── core/
│   └── workers.py           # Multithreaded QThread/QRunnable management
├── incantations/            # Backend logic modules (No UI code here)
│   ├── essence_siphon.py    # System cleaning logic
│   ├── arcane_cipher.py     # Encryption/Hashing logic
│   └── ...                  # (Specialized backend modules)
└── ui/
    ├── main_window.py       # Main window orchestration and sidebar
    ├── tabs/                # Individual Mixin classes for each tab
    │   ├── dashboard.py
    │   ├── privacy_warding.py
    │   └── ...
    └── custom_widgets.py    # Optimized, custom-painted PyQt components

    ⚖️ Disclaimer
With great power comes great responsibility.
Grimoire Mirror includes tools that make permanent, low-level changes to your operating system (e.g., Secure Shredder, Hosts File modification, Registry editing). 

    The Secure Shredder permanently destroys data. It cannot be undone.
    The Privacy & Warding tab modifies your system's hosts file and disables core Windows services.

Always review the actions you are taking, and ensure you have backups of critical data before running system-wide automation or cleaning scripts.
📜 License
This project is licensed under the MIT License. See the LICENSE
 file for details.
Built with 🔮 and ☕ by Pixl
May your system always run optimally, and your frames remain high.

 **Happy deploying!** 🚀🔮

# Grimoire 📖✨

(Work in Progress)

**Grimoire** is an open-source, portable, administrative optimization suite and custom Windows shell utility powered by Python and PyQt6. Designed for creators, developers, and power users, Grimoire acts as an automated "book of spells"—running natively in the Windows system tray to execute heavy OS automation, privacy hardening, system debloating, and local machine learning tasks.

By decoupling the high-performance system automation backend from the graphical user interface via asynchronous thread pools, Grimoire maintains a fluid, low-overhead system footprint without sacrificing multi-layered operational stability.

## 🔮 Active Incantations (Core Modules)

Grimoire organizes its core system hooks into specialized sub-modules:

- **Arcane Intelligence** (`arcane_intel.py`): Integrates directly with local, offline LLM model matrices (via Ollama) to execute hardware-accelerated text refactoring and code optimizations directly within the Windows clipboard.
- **Void Shield** (`void_shield.py`): A boundary-layer privacy filter that programmatically intercepts and disables Windows telemetry, data collection routes, and background tracking servers at the OS hosts configuration layer.
- **File Alchemy & Scrying** (`file_alchemy.py` & `scry_search.py`): Features automated extensions sorting, bulk asset indexing routines, and a low-level MFT-style rapid filesystem search engine that bypasses standard Windows Explorer delays.
- **Purge Engine** (`purge_debloat.py`): Leverages administrative PowerShell subprocess wrappers to cleanly strip pre-installed system bloatware packages and telemetry services.
- **Workspace Stasis** (`workspace_stasis.py`): Captures multi-monitor win32 process handles and pixel geometry coordinates to snapshot and freeze custom application grid layouts.
- **Text & Keyboard Alchemy** (`text_expansion.py` & `clipboard_magic.py`): Drives system-wide asynchronous hotkey listeners to intercept and format text buffers or dynamically substitute custom typed abbreviations on the fly.

## 🎨 Visual Alchemy & AI Design Suite

Grimoire now includes a comprehensive **Visual Alchemy** workspace with integrated AI-powered design tools:

### Design Suite Features:
- **🖼️ Subject Isolator**: AI-powered background removal with flawless alpha channel extraction
- **⬆️ Super Resolution Upscaler**: OpenCV-based lossless image enhancement (2x-4x scaling)
- **🎨 Style Transfer**: Neural style remapping using Stable Diffusion XL Refiner
- **🔄 Seamless Texture Tiler**: Automatic generation of tileable patterns from any image
- **🌈 Palette Harmonizer**: Extracts dominant color schemes for brand consistency
- **🖌️ Context-Aware Inpainting**: AI-powered image modification using neural networks

### Advanced Production Extensions:
- **🗺️ PBR Map Generator**: Creates normal maps and displacement maps from diffuse textures
- **📐 Layer Composer**: Professional alpha-channel compositing for multi-layer workflows

*Optimized for NVIDIA GPUs (RTX 3060 Ti and above recommended for AI features)*

## 📐 Project Architecture

The architecture maintains strict decoupling between the graphical rendering engine and background thread executors:
Grimoire_OS/
│
├── main.py                     # Application entry point
├── requirements.txt            # Python dependencies
│
├── assets/                     # UI assets and icons
│   ├── grimoire_logo.png
│   ├── grimoire_text.png
│   └── ...
│
├── incantations/               # Backend automation modules
│   ├── init.py
│   ├── file_alchemy.py
│   ├── image_matrix.py
│   ├── deep_cleaner.py
│   └── ...
│
├── core/                       # AI engines and workers
│   ├── init.py
│   ├── ai_suite.py            # DesignSuite & AdvancedDesignExtensions
│   └── workers.py             # Async thread pools
│
└── ui/                         # PyQt6 interface (modular)
    ├── init.py
    ├── custom_widgets.py      # Custom UI components
    ├── main_window.py         # Main application window
    └── tabs.py                # Workspace tabs (Dashboard, Visual Alchemy, etc.)
    
## 🚀 Installation

### Prerequisites
- **Python 3.10+**
- **Windows 10/11** (Administrator privileges recommended)
- **NVIDIA GPU** (Optional but recommended for AI features - RTX 2060 or better)

### Basic Installation

(```bash)
# Clone the repository
git clone https://github.com/yourusername/Grimoire.git
cd Grimoire

# Install core dependencies
pip install -r requirements.txt

AI Design Suite Installation (Optional)
For full AI-powered visual features:

# Install PyTorch with CUDA support (for NVIDIA GPUs)
pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu121

# Install AI dependencies
pip install opencv-python diffusers rembg transformers accelerate safetensors pillow numpy

Note: The AI suite requires ~3-5GB disk space for model weights on first run.
🎯 Usage

# Launch Grimoire
python main.py

The application will appear in your system tray. Right-click the tray icon to access quick actions, or click to open the full dashboard.
First-Time Setup

    AI Models: On first launch with AI features enabled, Grimoire will automatically download required models (~2-3GB)
    Administrator Rights: Some system optimization features require elevated privileges
    GPU Detection: AI features automatically detect and utilize available CUDA hardware

📂 Key Features
🖥️ Dashboard

    Real-time system telemetry (CPU, RAM, Storage, Processes)
    Performance charts and historical data
    Quick system statistics

🧪 File Alchemy

    Automated file organization by type/date/size
    Batch rename engine with pattern matching
    Duplicate file finder

👁️ Visual Alchemy

    Professional image editing tools (PIL-based)
    AI-powered background removal and upscaling
    Style transfer and neural inpainting
    Color palette extraction
    PBR map generation for 3D workflows
    Save/export in multiple formats (PNG, JPEG, BMP)

🚀 Deployment Architect

    System restore checkpoint creation
    Silent bulk software installer
    Automated deployment loops

🧠 Task Viewer

    Real-time process monitoring
    CPU/Memory usage tracking
    Process termination controls

⚙️ Arcane Tuning

    Windows telemetry disable
    UI animation controls
    Performance optimization presets
    Registry policy guards

🔧 Configuration
Grimoire uses a modular configuration system. Edit settings in the incantations/ directory to customize:

    Automation schedules
    Telemetry blocklists
    File sorting rules
    AI model parameters

🛡️ Privacy & Security

    Offline-First: Core features work without internet connectivity
    No Telemetry: Grimoire does not collect user data
    Open Source: All code is auditable and community-reviewed
    Local Processing: AI features run locally on your hardware (no cloud APIs)

📝 Requirements
Core Dependencies

    PyQt6 - GUI framework
    psutil - System monitoring
    Pillow - Image processing

AI Dependencies (Optional)

    torch - PyTorch for neural networks
    opencv-python - Computer vision
    diffusers - Stable Diffusion pipelines
    rembg - Background removal
    transformers - Hugging Face models

🤝 Contributing
Contributions are welcome! Please read our contributing guidelines before submitting PRs.

    Fork the repository
    Create your feature branch (git checkout -b feature/AmazingFeature)
    Commit your changes (git commit -m 'Add some AmazingFeature')
    Push to the branch (git push origin feature/AmazingFeature)
    Open a Pull Request

📄 License
This project is licensed under the MIT License - see the LICENSE
 file for details.
🙏 Acknowledgments

    PyQt6 for the excellent GUI framework
    Hugging Face for the Transformers and Diffusers libraries
    OpenCV for computer vision capabilities
    The Community for feedback and testing

📧 Support
For issues, questions, or suggestions:

    Open an issue on GitHub
    Check the Wiki
     for documentation
    Join our community discussions

Made with ❤️ for the Windows power user community

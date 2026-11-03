# RecordiaILIA 🎥📸

[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Git Flow](https://img.shields.io/badge/Git%20Flow-Feature%20Branches-green.svg)](docs/GIT_WORKFLOW_LOG.md)

**RecordiaILIA** is an advanced desktop utility designed for automated **Problem Steps Recording (PSR)**, instant screenshot capturing, screen recording, and automated local project organization. Developed as a collaborative academic project demonstrating **Git Flow, Kanban Issue Tracking, and GitHub Collaborative Workflows**.

---

## 👥 Authors & Roles

- **Hachem Squalli** (`hachemite`): Architecture, UI initial prototype, Core Capture/Recording Logic.
- **Yassine Ouali** (`Ysn-Ir`): Modular Architecture, Global Hotkeys (`pynput`), Storage & Settings Management, OpenCV Video Recording Engine, Automated Steps Recorder with Window Inspection & HTML Reporting, and Comprehensive Test Suite.

---

## ✨ Features

- 📑 **Project-Based Steps Recorder**:
  - Automatically isolates each capture session into its own dedicated project folder (`captures/Projects/<Project_Name>_<Timestamp>/`).
  - Automatically detects the foreground **Application Name** (e.g. `chrome.exe`, `Code.exe`) and **Window Title** via Windows APIs (`ctypes` + `psutil`).
  - Records exact timestamps and user action annotations for every single step.
  - Automatically exports a self-contained, responsive **HTML Report** (`report.html`) and Markdown summary (`REPORT.md`) containing all step screenshots, app badges, timestamps, and step descriptions.
- 🖥️ **Interactive Desktop GUI**: Built with Tkinter, featuring project name configuration, real-time step counter, one-click HTML report export, capture controls, directory opening, and modal preferences.
- ⚡ **Global Hotkeys**: Background keyboard listener using `pynput` supporting system-wide shortcuts even when minimized:
  - **Capture Step**: `Ctrl + Shift + S`
  - **Toggle Screen Video**: `Ctrl + Shift + R`
- 🎥 **Smooth Screen Recording**: Multi-threaded video recording engine using OpenCV (`cv2.VideoWriter` with `mp4v` codec) capturing frames in the background without UI lag.
- ⚙️ **Persistent Preferences & Storage**: Automated hierarchical directory organization (`Projects/`, `Screenshots/`, and `Recordings/`), configurable storage folder, customizable screenshot format (`PNG`/`JPG`), and selectable framerate (`15`, `30`, `60` FPS).
- 🧪 **Complete Test Suite**: 16 automated unit and integration tests covering window inspection, session management, settings, storage, hotkeys, screenshot, and video recording modules.

---

## 🏗️ Project Architecture

```text
recordia-ilia/
├── docs/
│   └── GIT_WORKFLOW_LOG.md       # Comprehensive log of all Git commands and outputs
├── src/
│   ├── main.py                   # Application orchestrator and entry point
│   ├── capture/                  # Screen capture and video engines
│   │   ├── __init__.py
│   │   ├── base.py               # Abstract base classes (BaseScreenshotEngine, BaseRecordingEngine)
│   │   ├── screenshot.py         # Pillow + mss screenshot capture implementation
│   │   └── recorder.py           # Multi-threaded OpenCV screen recording engine
│   ├── config/                   # Settings and configuration management
│   │   ├── __init__.py
│   │   └── settings.py           # JSON settings persistence (paths, hotkeys, fps)
│   ├── core/                     # Core system utilities
│   │   ├── __init__.py
│   │   ├── hotkeys.py            # Global Hotkey manager via pynput GlobalHotKeys
│   │   └── window_info.py        # Active foreground window and process detection
│   ├── storage/                  # File persistence and session management
│   │   ├── __init__.py
│   │   ├── file_manager.py       # Timestamped naming and explorer launcher
│   │   └── session_manager.py    # Project-based step session manager & HTML report exporter
│   └── ui/                       # Desktop user interface (Tkinter)
│       ├── __init__.py
│       ├── main_window.py        # Main control window with step recorder controls
│       ├── settings_window.py    # Configuration modal dialog
│       └── step_dialog.py        # Step annotation and quick-mode dialog
├── tests/                        # Comprehensive test suite (16 tests)
│   ├── __init__.py
│   ├── test_file_manager.py
│   ├── test_hotkeys.py
│   ├── test_recorder.py
│   ├── test_screenshot.py
│   ├── test_session_manager.py
│   ├── test_settings.py
│   └── test_window_info.py
├── .gitignore                    # Ignored artifacts, virtual environments, captures
├── requirements.txt              # Project dependencies
└── README.md                     # Documentation and setup guide
```

---

## 🚀 Getting Started

### 1. Prerequisites
- Python 3.10 or later installed.
- Git.

### 2. Installation
Clone the repository and install the dependencies:
```bash
git clone https://github.com/hachemite/recordia-ilia.git
cd recordia-ilia
pip install -r requirements.txt
```

### 3. Running the Application
Launch RecordiaILIA directly with Python:
```bash
python src/main.py
```

### 4. Running the Tests
Execute the automated test suite (16 tests):
```bash
python -m unittest discover -s tests -v
```

---

## ⌨️ Hotkeys Reference

| Action | Global Shortcut | Description |
|---|---|---|
| **Capture Step** | `Ctrl + Shift + S` | Captures step with active window info and saves to active project session |
| **Start/Stop Video** | `Ctrl + Shift + R` | Toggles screen video recording saved to `Recordings/` |

---

## 📈 Git & GitHub Collaborative Workflow

This repository strictly demonstrates professional software engineering Git practices:
1. **Feature Branching**: Each feature was developed on an isolated branch (`feature/<name>`).
2. **Issue Linking**: Commits and merge pull requests link GitHub issues using keywords (`Fixes #X`, `Closes #X`).
3. **Topology Preservation**: Merges into `main` use `--no-ff` to maintain a transparent, traceable commit tree graph.
4. **Audit Trail**: Every command, branch lifecycle, test run, and API status change is documented in [`docs/GIT_WORKFLOW_LOG.md`](docs/GIT_WORKFLOW_LOG.md).

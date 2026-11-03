# RecordiaILIA

[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Git Flow](https://img.shields.io/badge/Git%20Flow-Feature%20Branches-green.svg)](docs/GIT_WORKFLOW_LOG.md)

**RecordiaILIA** is an advanced desktop utility designed for automated **Problem Steps Recording (PSR)**, custom hotkeys, flexible event-driven step capturing (manual, on mouse click, or periodic timer), post-session step description editing, screen recording, and automated local project organization. Developed as a collaborative academic project demonstrating **Git Flow, Kanban Issue Tracking, and GitHub Collaborative Workflows**.

---

## Authors & Roles

- **Yassine Ouali** (`Ysn-Ir`): Project Architecture, Core Capture & Video Recording Engines (Pillow/mss + OpenCV), Global Hotkeys (`pynput`), Storage & Settings Management, Automated Event-Driven Steps Recorder (On-Click & Periodic Timer), Step Review/Editor, and Comprehensive Test Suite.
- **Hachem Squalli** (`hachemite`): UI Design & Initial Tkinter Prototype, Documentation & Academic Reports, Git/GitHub Workflow Orchestration, and Project Coordination.

---

## Features

- **Automated Steps Recorder (User's Choice of Trigger)**:
  - **Manual Trigger**: Capture steps on demand via UI button or custom global hotkey (default `Ctrl + Shift + S`, fully configurable in Settings).
  - **Auto on Mouse Click**: Automatically captures a step on every mouse click across the desktop with click coordinates `(x, y)` and active button.
  - **Auto Periodic Timer**: Automatically captures steps at a configurable interval (e.g. every 1s, 2s, 5s).
  - **Active Window Inspection**: Automatically detects the foreground **Application Name** (e.g. `chrome.exe`, `Code.exe`) and **Window Title** via Windows APIs (`ctypes` + `psutil`).
  - **Isolated Project Folders**: Creates dedicated timestamped directories for every session (`captures/Projects/<Project_Name>_<Timestamp>/`).
  - **Review & Edit Step Descriptions**: Review all captured steps at any point during or after a session and update individual descriptions before generating reports.
  - **Interactive HTML & Markdown Reports**: Automatically exports clean, professional **HTML Reports** (`report.html`) with embedded screenshots, app badges, timestamps, and step descriptions, and opens it directly in the browser upon finishing a session.
- **Customizable Global Hotkeys**:
  - Configure your preferred hotkey combinations in the Settings dialog (e.g. `<f9>`, `<f10>`, `<ctrl>+<alt>+s`, etc.) with instant live re-binding.
- **Smooth Screen Recording**: Multi-threaded video recording engine using OpenCV (`cv2.VideoWriter` with `mp4v` codec) capturing frames in the background without UI lag.
- **Persistent Preferences & Storage**: Automated hierarchical directory organization (`Projects/`, `Screenshots/`, and `Recordings/`), configurable storage folder, customizable screenshot format (`PNG`/`JPG`), and selectable framerate (`15`, `30`, `60` FPS).
- **Clean Interface**: Professional, clean typography without emoji stickers.
- **Complete Test Suite**: 20 automated unit and integration tests covering auto-steppers, window inspection, session management, settings, storage, hotkeys, screenshot, and video recording modules.

---

## Project Architecture

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
│   │   ├── auto_stepper.py       # Event-driven triggers: Manual, On-Click & Periodic Timer
│   │   ├── hotkeys.py            # Global Hotkey manager via pynput GlobalHotKeys
│   │   └── window_info.py        # Active foreground window and process detection
│   ├── storage/                  # File persistence and session management
│   │   ├── __init__.py
│   │   ├── file_manager.py       # Timestamped naming and explorer launcher
│   │   └── session_manager.py    # Project-based step session manager & HTML report exporter
│   └── ui/                       # Desktop user interface (Tkinter)
│       ├── __init__.py
│       ├── main_window.py        # Main control window with mode selectors and counters
│       ├── settings_window.py    # Configuration modal dialog (paths, custom hotkeys, FPS)
│       ├── step_dialog.py        # Step annotation dialog
│       └── step_editor_window.py # Review and edit step descriptions dialog
├── tests/                        # Comprehensive test suite (20 tests)
│   ├── __init__.py
│   ├── test_auto_stepper.py
│   ├── test_file_manager.py
│   ├── test_hotkeys.py
│   ├── test_recorder.py
│   ├── test_screenshot.py
│   ├── test_session_manager.py
│   ├── test_settings.py
│   └── test_window_info.py
├── .gitignore                    # Ignored artifacts, virtual environments, captures
├── LICENSE                       # MIT license
├── requirements.txt              # Project dependencies
└── README.md                     # Documentation and setup guide
```

---

## Getting Started

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
Execute the automated test suite (20 tests):
```bash
python -m unittest discover -s tests -v
```

---

## Hotkeys Reference

| Action | Default Shortcut | Customization |
|---|---|---|
| **Capture Step** | `Ctrl + Shift + S` | Configurable in Settings (e.g. `<f9>`) |
| **Start/Stop Video** | `Ctrl + Shift + R` | Configurable in Settings (e.g. `<f10>`) |

---

## Git & GitHub Collaborative Workflow

This repository strictly demonstrates professional software engineering Git practices:
1. **Feature Branching**: Each feature was developed on an isolated branch (`feature/<name>`).
2. **Issue Linking**: Commits and merge pull requests link GitHub issues using keywords (`Fixes #X`, `Closes #X`).
3. **Topology Preservation**: Merges into `main` use `--no-ff` to maintain a transparent, traceable commit tree graph.
4. **Audit Trail**: Every command, branch lifecycle, test run, and API status change is documented in [`docs/GIT_WORKFLOW_LOG.md`](docs/GIT_WORKFLOW_LOG.md).

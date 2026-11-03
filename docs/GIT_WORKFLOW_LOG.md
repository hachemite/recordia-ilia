# Git & GitHub Collaborative Workflow Log

> **Project**: RecordiaILIA (Desktop Screenshot & Screen Recording Utility)  
> **Course / TP**: Collaborative Git & GitHub Workflow Demonstration  
> **Repository**: [hachemite/recordia-ilia](https://github.com/hachemite/recordia-ilia)  
> **Authors**: Yassine Ouali (`Ysn-Ir`), Hachem Squalli (`hachemite`)

---

## 1. Branching Strategy & Methodology

This project adheres to the **Feature Branch Workflow**:
- `main`: Production-ready, stable codebase.
- `feature/<feature-name>`: Dedicated branches for each specific feature or GitHub issue.
- Direct pushes to `main` without feature branches are avoided.
- Merge commits preserve history (`--no-ff`) and link issues via `Closes #X` / `Fixes #X`.
- Remote tracking branches are maintained on GitHub (`origin`).

---

## 2. Issues Breakdown & Assignment Matrix

| Issue ID | Feature Title | Assignee | Target Branch | Status |
|:---:|:---|:---:|:---|:---:|
| **#1** | Design the project architecture and hotkeys | `Ysn-Ir` | `feature/architecture-and-hotkeys` | **CLOSED** (Commit 4d4966e / Merge d0735a3) |
| **#2** | Create the user interface | `hachemite` | `feature/Creating_user_interface` | **CLOSED** (PR #9) |
| **#3** | Develop file saving and settings | `Ysn-Ir` | `feature/file-saving-and-settings` | **CLOSED** (Commit e923205 / Merge e49e456) |
| **#4** | Develop screenshot capture | `Ysn-Ir` | `feature/screenshot-capture` | **CLOSED** (Commit b3864cf / Merge d2ab6c1) |
| **#5** | Develop screen recording | `Ysn-Ir` | `feature/screen-recording` | **In Progress** |
| **#6** | Develop file saving and settings | *(unassigned)* | Duplicate of #3 | **CLOSED** (Merge e49e456) |
| **#7** | Test the features | `Ysn-Ir` | `feature/test-features` | Queued |
| **#8** | Write documentation and report | *(unassigned)* | `feature/documentation-and-report` | Queued |

---

## 3. Step-by-Step Command Log & Terminal Outputs

### Step 1: Upstream Sync
**Action**: Synchronize local `main` branch with remote upstream repository to avoid drift.
```bash
git pull origin main
```
**Terminal Output**:
```text
From https://github.com/hachemite/recordia-ilia
 * branch            main       -> FETCH_HEAD
Already up to date.
```

---

### Step 2: Feature #1 - Architecture & Hotkeys Listener (Closes #1)

#### 2.1 Branch Creation
**Action**: Create and switch to isolated feature branch `feature/architecture-and-hotkeys`.
```bash
git checkout -b feature/architecture-and-hotkeys
```
**Terminal Output**:
```text
Switched to a new branch 'feature/architecture-and-hotkeys'
```

#### 2.2 Changes Implemented
- Added `.gitignore` to prevent committing bytecode, cache, and local captures.
- Created `src/core/hotkeys.py` with `HotkeyManager` using `pynput.keyboard.GlobalHotKeys` for cross-platform background hotkey monitoring.
- Created `src/config/settings.py` for persistent user configurations and defaults.
- Created `src/capture/base.py` defining abstract base classes `BaseScreenshotEngine` and `BaseRecordingEngine`.
- Refactored `src/ui/main_window.py` to support thread-safe status updates via `root.after` and graceful application shutdown callbacks.
- Updated `src/main.py` with `RecordiaApp` orchestrator binding settings, UI, and hotkeys.

#### 2.3 Staging and Committing
**Action**: Stage all newly created architecture and core modules, and commit using Conventional Commits syntax linking Issue #1.
```bash
git add .
git commit -m "feat(core): design project architecture and global hotkeys listener (fixes #1)"
```
**Terminal Output**:
```text
[feature/architecture-and-hotkeys 4d4966e] feat(core): design project architecture and global hotkeys listener (fixes #1)
 10 files changed, 381 insertions(+), 11 deletions(-)
 create mode 100644 .gitignore
 create mode 100644 docs/GIT_WORKFLOW_LOG.md
 create mode 100644 src/capture/__init__.py
 create mode 100644 src/capture/base.py
 create mode 100644 src/config/__init__.py
 create mode 100644 src/config/settings.py
 create mode 100644 src/core/__init__.py
 create mode 100644 src/core/hotkeys.py
```

#### 2.4 Publishing Feature Branch Upstream
**Action**: Push feature branch to `origin` and establish tracking.
```bash
git push -u origin feature/architecture-and-hotkeys
```
**Terminal Output**:
```text
branch 'feature/architecture-and-hotkeys' set up to track 'origin/feature/architecture-and-hotkeys'.
To https://github.com/hachemite/recordia-ilia.git
 * [new branch]      feature/architecture-and-hotkeys -> feature/architecture-and-hotkeys
```

#### 2.5 Merging into Main & Auto-Closing Issue #1
**Action**: Switch to `main`, ensure latest status, and merge with `--no-ff` preserving history graph.
```bash
git checkout main
git pull origin main
git merge --no-ff feature/architecture-and-hotkeys -m "Merge branch 'feature/architecture-and-hotkeys' (Closes #1)"
git push origin main
```
**Terminal Output**:
```text
Merge made by the 'ort' strategy.
To https://github.com/hachemite/recordia-ilia.git
   f0d65b2..d0735a3  main -> main
```

---

### Step 3: Feature #3 & #6 - File Saving & Settings Dialog (Closes #3, Closes #6)

#### 3.1 Branch Creation
**Action**: Create and switch to isolated branch `feature/file-saving-and-settings` branched from updated `main`.
```bash
git checkout -b feature/file-saving-and-settings
```
**Terminal Output**:
```text
Switched to a new branch 'feature/file-saving-and-settings'
```

#### 3.2 Changes Implemented
- Created `src/storage/file_manager.py` implementing `FileManager` with automatic directory structure creation (`Screenshots/` and `Recordings/`), unique timestamped naming, and cross-platform folder opener.
- Created `src/ui/settings_window.py` with `SettingsWindow` GUI modal for folder selection (`filedialog`), screenshot format choices (PNG/JPG), and recording framerate settings (15/30/60 FPS).
- Enhanced `src/ui/main_window.py` with quick-access buttons for "Open Captures 📁" and "Settings ⚙️".
- Updated `src/main.py` orchestrator linking settings updates dynamically to storage paths.

#### 3.3 Staging and Committing
**Action**: Stage and commit file saving and settings modules, referencing issues #3 and #6.
```bash
git add .
git commit -m "feat(storage): implement file saving manager and settings dialog (fixes #3, fixes #6)"
```
**Terminal Output**:
```text
[feature/file-saving-and-settings e923205] feat(storage): implement file saving manager and settings dialog (fixes #3, fixes #6)
 6 files changed, 240 insertions(+), 19 deletions(-)
 create mode 100644 src/storage/__init__.py
 create mode 100644 src/storage/file_manager.py
 create mode 100644 src/ui/settings_window.py
```

#### 3.4 Publishing Feature Branch Upstream
**Action**: Push feature branch to `origin`.
```bash
git push -u origin feature/file-saving-and-settings
```
**Terminal Output**:
```text
branch 'feature/file-saving-and-settings' set up to track 'origin/feature/file-saving-and-settings'.
To https://github.com/hachemite/recordia-ilia.git
 * [new branch]      feature/file-saving-and-settings -> feature/file-saving-and-settings
```

#### 3.5 Merging into Main & Auto-Closing Issues #3 and #6
**Action**: Switch to `main`, merge `--no-ff`, and push upstream.
```bash
git checkout main
git pull origin main
git merge --no-ff feature/file-saving-and-settings -m "Merge branch 'feature/file-saving-and-settings' (Closes #3, Closes #6)"
git push origin main
```
**Terminal Output**:
```text
Merge made by the 'ort' strategy.
To https://github.com/hachemite/recordia-ilia.git
   d0735a3..e49e456  main -> main
```

---

### Step 4: Feature #4 - Screenshot Capture Engine (Closes #4)

#### 4.1 Branch Creation
**Action**: Create and switch to isolated branch `feature/screenshot-capture`.
```bash
git checkout -b feature/screenshot-capture
```
**Terminal Output**:
```text
Switched to a new branch 'feature/screenshot-capture'
```

#### 4.2 Changes Implemented
- Created `src/capture/screenshot.py` implementing `ScreenshotEngine` inheriting from `BaseScreenshotEngine`.
- Supports fullscreen capture and region capture with Pillow and mss.
- Added graceful headless / CI fallback for systems without active display devices.
- Integrated screenshot trigger into `RecordiaApp` in `src/main.py`.

#### 4.3 Staging and Committing
**Action**: Stage and commit screenshot engine linking Issue #4.
```bash
git add .
git commit -m "feat(capture): implement screenshot capture engine with mss (fixes #4)"
```
**Terminal Output**:
```text
[feature/screenshot-capture b3864cf] feat(capture): implement screenshot capture engine with mss (fixes #4)
 4 files changed, 156 insertions(+), 10 deletions(-)
 create mode 100644 src/capture/screenshot.py
```

#### 4.4 Publishing Feature Branch Upstream
**Action**: Push feature branch to `origin`.
```bash
git push -u origin feature/screenshot-capture
```
**Terminal Output**:
```text
branch 'feature/screenshot-capture' set up to track 'origin/feature/screenshot-capture'.
To https://github.com/hachemite/recordia-ilia.git
 * [new branch]      feature/screenshot-capture -> feature/screenshot-capture
```

#### 4.5 Merging into Main & Auto-Closing Issue #4
**Action**: Switch to `main`, merge `--no-ff`, and push upstream.
```bash
git checkout main
git pull origin main
git merge --no-ff feature/screenshot-capture -m "Merge branch 'feature/screenshot-capture' (Closes #4)"
git push origin main
```
**Terminal Output**:
```text
Merge made by the 'ort' strategy.
To https://github.com/hachemite/recordia-ilia.git
   e49e456..d2ab6c1  main -> main
```

---

### Step 5: Feature #5 - Screen Recording Engine (Closes #5)

#### 5.1 Branch Creation
**Action**: Create and switch to isolated branch `feature/screen-recording`.
```bash
git checkout -b feature/screen-recording
```
**Terminal Output**:
```text
Switched to a new branch 'feature/screen-recording'
```

#### 5.2 Changes Implemented
- Created `src/capture/recorder.py` implementing `ScreenRecorder` inheriting from `BaseRecordingEngine`.
- Continuous background frame capture and video encoding using `cv2.VideoWriter` (`mp4v` codec) and `mss`.
- Non-blocking execution via worker thread with synchronization locks and clean stop/join mechanisms.
- Wired Start/Stop recording actions into `RecordiaApp` and UI status feedback in `src/main.py`.

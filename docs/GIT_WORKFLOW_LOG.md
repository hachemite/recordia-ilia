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
| **#1** | Design the project architecture and hotkeys | `Ysn-Ir` | `feature/architecture-and-hotkeys` | **CLOSED** (Commit `4d4966e` / Merge `d0735a3`) |
| **#2** | Create the user interface | `hachemite` | `feature/Creating_user_interface` | **CLOSED** (PR #9) |
| **#3** | Develop file saving and settings | `Ysn-Ir` | `feature/file-saving-and-settings` | **CLOSED** (Commit `e923205` / Merge `e49e456`) |
| **#4** | Develop screenshot capture | `Ysn-Ir` | `feature/screenshot-capture` | **CLOSED** (Commit `b3864cf` / Merge `d2ab6c1`) |
| **#5** | Develop screen recording | `Ysn-Ir` | `feature/screen-recording` | **CLOSED** (Commit `ee15286` / Merge `1b0f505`) |
| **#6** | Develop file saving and settings | *(unassigned)* | Duplicate of #3 | **CLOSED** (Merge `e49e456`) |
| **#7** | Test the features | `Ysn-Ir` | `feature/test-features` | **CLOSED** (Commit `93805f8` / Merge `798cf8a`) |
| **#8** | Write documentation and report | *(unassigned)* | `feature/documentation-and-report` | **CLOSED** (Commit `60a428d` / Merge `9f431ab`) |
| **Bonus** | Automated Steps Recorder & HTML Reporting | `Ysn-Ir` | `feature/steps-recorder` | **In Progress** |

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

#### 2.3 Staging, Committing, Pushing & Merging
```bash
git add .
git commit -m "feat(core): design project architecture and global hotkeys listener (fixes #1)"
git push -u origin feature/architecture-and-hotkeys
git checkout main
git pull origin main
git merge --no-ff feature/architecture-and-hotkeys -m "Merge branch 'feature/architecture-and-hotkeys' (Closes #1)"
git push origin main
```
**Terminal Output**:
```text
[feature/architecture-and-hotkeys 4d4966e] feat(core): design project architecture and global hotkeys listener (fixes #1)
To https://github.com/hachemite/recordia-ilia.git
   f0d65b2..d0735a3  main -> main
```

---

### Step 3: Feature #3 & #6 - File Saving & Settings Dialog (Closes #3, Closes #6)

#### 3.1 Branch Creation, Changes & Staging
```bash
git checkout -b feature/file-saving-and-settings
git add .
git commit -m "feat(storage): implement file saving manager and settings dialog (fixes #3, fixes #6)"
git push -u origin feature/file-saving-and-settings
git checkout main
git pull origin main
git merge --no-ff feature/file-saving-and-settings -m "Merge branch 'feature/file-saving-and-settings' (Closes #3, Closes #6)"
git push origin main
```
**Terminal Output**:
```text
[feature/file-saving-and-settings e923205] feat(storage): implement file saving manager and settings dialog (fixes #3, fixes #6)
To https://github.com/hachemite/recordia-ilia.git
   d0735a3..e49e456  main -> main
```

---

### Step 4: Feature #4 - Screenshot Capture Engine (Closes #4)

#### 4.1 Branch Creation, Changes & Staging
```bash
git checkout -b feature/screenshot-capture
git add .
git commit -m "feat(capture): implement screenshot capture engine with mss (fixes #4)"
git push -u origin feature/screenshot-capture
git checkout main
git pull origin main
git merge --no-ff feature/screenshot-capture -m "Merge branch 'feature/screenshot-capture' (Closes #4)"
git push origin main
```
**Terminal Output**:
```text
[feature/screenshot-capture b3864cf] feat(capture): implement screenshot capture engine with mss (fixes #4)
To https://github.com/hachemite/recordia-ilia.git
   e49e456..d2ab6c1  main -> main
```

---

### Step 5: Feature #5 - Screen Recording Engine (Closes #5)

#### 5.1 Branch Creation, Changes & Staging
```bash
git checkout -b feature/screen-recording
git add .
git commit -m "feat(recorder): implement threaded screen recording engine with OpenCV (fixes #5)"
git push -u origin feature/screen-recording
git checkout main
git pull origin main
git merge --no-ff feature/screen-recording -m "Merge branch 'feature/screen-recording' (Closes #5)"
git push origin main
```
**Terminal Output**:
```text
[feature/screen-recording ee15286] feat(recorder): implement threaded screen recording engine with OpenCV (fixes #5)
To https://github.com/hachemite/recordia-ilia.git
   d2ab6c1..1b0f505  main -> main
```

---

### Step 6: Feature #7 - Comprehensive Test Suite (Closes #7)

#### 6.1 Branch Creation, Changes & Test Run
```bash
git checkout -b feature/test-features
python -m unittest discover -s tests -v
git add .
git commit -m "test(core): implement comprehensive unit and integration test suite (fixes #7)"
git push -u origin feature/test-features
git checkout main
git pull origin main
git merge --no-ff feature/test-features -m "Merge branch 'feature/test-features' (Closes #7)"
git push origin main
```
**Terminal Output**:
```text
Ran 12 tests in 0.976s - OK
[feature/test-features 93805f8] test(core): implement comprehensive unit and integration test suite (fixes #7)
To https://github.com/hachemite/recordia-ilia.git
   1b0f505..798cf8a  main -> main
```

---

### Step 7: Feature #8 - Documentation, Setup Guide & Report (Closes #8)

#### 7.1 Branch Creation, Changes & Staging
```bash
git checkout -b feature/documentation-and-report
git add .
git commit -m "docs: complete user documentation, setup guide, and Git workflow report (fixes #8)"
git push -u origin feature/documentation-and-report
git checkout main
git pull origin main
git merge --no-ff feature/documentation-and-report -m "Merge branch 'feature/documentation-and-report' (Closes #8)"
git push origin main
```
**Terminal Output**:
```text
[feature/documentation-and-report 60a428d] docs: complete user documentation, setup guide, and Git workflow report (fixes #8)
To https://github.com/hachemite/recordia-ilia.git
   798cf8a..9f431ab  main -> main
```

---

### Step 8: Feature - Automated Steps Recorder & HTML Reporting

#### 8.1 Branch Creation
```bash
git checkout -b feature/steps-recorder
```
**Terminal Output**:
```text
Switched to a new branch 'feature/steps-recorder'
```

#### 8.2 Changes Implemented
- Created `src/core/window_info.py`: Cross-platform foreground window inspector using Windows APIs (`ctypes` + `psutil`) to automatically capture application name (e.g. `chrome.exe`, `Code.exe`) and window caption.
- Created `src/storage/session_manager.py`: `SessionManager` and `StepRecord` data model. Organizes captures into dedicated project folders (`captures/Projects/<Project_Name>_<Timestamp>/`), saving individual step screenshots, JSON session metadata, and generating responsive **HTML Reports** (`report.html`) and Markdown reports (`REPORT.md`).
- Created `src/ui/step_dialog.py`: Annotation dialog presenting detected app name, window title, and description prompt with optional quick-mode.
- Refactored `src/ui/main_window.py` to support project naming, dynamic step counter badge, and one-click HTML report generation.
- Updated `src/main.py` orchestrator linking step recording, hotkeys, and automatic browser report launching.
- Added comprehensive unit tests in `tests/test_session_manager.py` and `tests/test_window_info.py` bringing total test suite count to 16 passing tests.

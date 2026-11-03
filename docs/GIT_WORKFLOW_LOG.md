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
| **Bonus 1** | Automated Steps Recorder & HTML Reporting | `Ysn-Ir` | `feature/steps-recorder` | **CLOSED** (Commit `aae535f` / Merge `bbece0a`) |
| **Bonus 2** | Event-Driven Auto Step Triggers (Click & Timer) | `Ysn-Ir` | `feature/auto-step-triggers` | **CLOSED** (Commit `f106f05` / Merge `2ed5baa`) |
| **Bonus 3** | Custom Hotkey Re-binding & Step Description Editor | `Ysn-Ir` | `feature/hotkey-config-and-step-editor` | **In Progress** |

---

## 3. Step-by-Step Command Log & Terminal Outputs

### Step 1: Upstream Sync
```bash
git pull origin main
```
**Terminal Output**:
```text
Already up to date.
```

---

### Step 2: Feature #1 - Architecture & Hotkeys Listener (Closes #1)
- Branch: `feature/architecture-and-hotkeys`
- Commit: `4d4966e` / Merge: `d0735a3`

---

### Step 3: Feature #3 & #6 - File Saving & Settings Dialog (Closes #3, Closes #6)
- Branch: `feature/file-saving-and-settings`
- Commit: `e923205` / Merge: `e49e456`

---

### Step 4: Feature #4 - Screenshot Capture Engine (Closes #4)
- Branch: `feature/screenshot-capture`
- Commit: `b3864cf` / Merge: `d2ab6c1`

---

### Step 5: Feature #5 - Screen Recording Engine (Closes #5)
- Branch: `feature/screen-recording`
- Commit: `ee15286` / Merge: `1b0f505`

---

### Step 6: Feature #7 - Comprehensive Test Suite (Closes #7)
- Branch: `feature/test-features`
- Commit: `93805f8` / Merge: `798cf8a`

---

### Step 7: Feature #8 - Documentation, Setup Guide & Report (Closes #8)
- Branch: `feature/documentation-and-report`
- Commit: `60a428d` / Merge: `9f431ab`

---

### Step 8: Feature - Automated Steps Recorder & HTML Reporting
- Branch: `feature/steps-recorder`
- Commit: `aae535f` / Merge: `bbece0a`

---

### Step 9: Feature - Event-Driven Auto Step Triggers (Click & Timer)
- Branch: `feature/auto-step-triggers`
- Commit: `f106f05` / Merge: `2ed5baa`

---

### Step 10: Feature - Custom Hotkey Re-binding, Step Review/Editor & Clean UI

#### 10.1 Branch Creation
```bash
git checkout -b feature/hotkey-config-and-step-editor
```
**Terminal Output**:
```text
Switched to a new branch 'feature/hotkey-config-and-step-editor'
```

#### 10.2 Changes Implemented
- Updated `src/ui/settings_window.py` with custom hotkey configuration fields for step capture (e.g. `<f9>`) and video recording with instant live re-binding.
- Created `src/ui/step_editor_window.py`: Dedicated interactive step review and description editor allowing users to inspect all captured steps in a Treeview list, edit descriptions, and save updates back to `session_metadata.json`.
- Updated `src/storage/session_manager.py` with `update_step_description()` and `get_steps()` methods.
- Removed emoji stickers across the UI and HTML report templates for a clean, minimal appearance.
- Updated `src/main.py` orchestrator with live hotkey re-registration and step editor wiring.
- Added unit test `test_update_step_description` in `tests/test_session_manager.py`, bringing total passing test suite count to 20 tests.

#### 10.3 Test Suite Execution
```bash
python -m unittest discover -s tests -v
```
**Terminal Output**:
```text
Ran 20 tests in 2.598s

OK
```

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
| **Bonus 2** | Event-Driven Auto Step Triggers (Click & Timer) | `Ysn-Ir` | `feature/auto-step-triggers` | **In Progress** |

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
- Commit: `feat(core): design project architecture and global hotkeys listener (fixes #1)` (`4d4966e`)
- Merged into `main` (`d0735a3`) and pushed upstream.

---

### Step 3: Feature #3 & #6 - File Saving & Settings Dialog (Closes #3, Closes #6)
- Branch: `feature/file-saving-and-settings`
- Commit: `feat(storage): implement file saving manager and settings dialog (fixes #3, fixes #6)` (`e923205`)
- Merged into `main` (`e49e456`) and pushed upstream.

---

### Step 4: Feature #4 - Screenshot Capture Engine (Closes #4)
- Branch: `feature/screenshot-capture`
- Commit: `feat(capture): implement screenshot capture engine with mss (fixes #4)` (`b3864cf`)
- Merged into `main` (`d2ab6c1`) and pushed upstream.

---

### Step 5: Feature #5 - Screen Recording Engine (Closes #5)
- Branch: `feature/screen-recording`
- Commit: `feat(recorder): implement threaded screen recording engine with OpenCV (fixes #5)` (`ee15286`)
- Merged into `main` (`1b0f505`) and pushed upstream.

---

### Step 6: Feature #7 - Comprehensive Test Suite (Closes #7)
- Branch: `feature/test-features`
- Commit: `test(core): implement comprehensive unit and integration test suite (fixes #7)` (`93805f8`)
- Merged into `main` (`798cf8a`) and pushed upstream.

---

### Step 7: Feature #8 - Documentation, Setup Guide & Report (Closes #8)
- Branch: `feature/documentation-and-report`
- Commit: `docs: complete user documentation, setup guide, and Git workflow report (fixes #8)` (`60a428d`)
- Merged into `main` (`9f431ab`) and pushed upstream.

---

### Step 8: Feature - Automated Steps Recorder & HTML Reporting
- Branch: `feature/steps-recorder`
- Commit: `feat(steps): implement automated steps recorder with window inspection and HTML reports` (`aae535f`)
- Merged into `main` (`bbece0a`) and pushed upstream.

---

### Step 9: Feature - Event-Driven Auto Step Triggers (User's Choice: Manual, Click, Timer)

#### 9.1 Branch Creation
```bash
git checkout -b feature/auto-step-triggers
```
**Terminal Output**:
```text
Switched to a new branch 'feature/auto-step-triggers'
```

#### 9.2 Changes Implemented
- Created `src/core/auto_stepper.py` with `AutoStepper` supporting:
  - `TriggerMode.MANUAL`: on-demand user captures.
  - `TriggerMode.ON_CLICK`: global `pynput.mouse.Listener` capturing steps automatically on every desktop mouse click with coordinates `(x, y)` and button name, debounced against rapid clicks.
  - `TriggerMode.PERIODIC`: background daemon timer capturing steps automatically every $N$ seconds.
- Enhanced `src/ui/main_window.py` with:
  - User trigger mode selector (Manual, Auto on Click, Auto Periodic Timer).
  - Interval spinbox/entry for tuning timer seconds.
  - Dynamic Start/Stop toggle button for auto-capturing.
- Updated `src/main.py` orchestrator linking `AutoStepper` background triggers to `SessionManager`.
- Created `tests/test_auto_stepper.py` unit tests bringing total test suite to 19 passing tests.

#### 9.3 Test Suite Execution
```bash
python -m unittest discover -s tests -v
```
**Terminal Output**:
```text
Ran 19 tests in 2.556s

OK
```

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
- Direct pushes to `main` are restricted in favor of **Pull Requests** (or documented fast-forward/rebase merges) referencing issue numbers (`Closes #X`, `Fixes #X`).
- Explicit tracking of all git operations (pull, branch, add, commit, push, merge, prune).

---

## 2. Issues Breakdown & Assignment Matrix

| Issue ID | Feature Title | Assignee | Target Branch | Status |
|:---:|:---|:---:|:---|:---:|
| **#1** | Design the project architecture and hotkeys | `Ysn-Ir` | `feature/architecture-and-hotkeys` | **In Progress** |
| **#2** | Create the user interface | `hachemite` | `feature/Creating_user_interface` | **Closed** (PR #9) |
| **#3** | Develop file saving and settings | `Ysn-Ir` | `feature/file-saving-and-settings` | Queued |
| **#4** | Develop screenshot capture | `Ysn-Ir` | `feature/screenshot-capture` | Queued |
| **#5** | Develop screen recording | `Ysn-Ir` | `feature/screen-recording` | Queued |
| **#6** | Develop file saving and settings | *(unassigned)* | Duplicate of #3 | Queued |
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


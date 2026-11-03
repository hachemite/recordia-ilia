"""
Step recording session manager for RecordiaILIA.
Organizes captures into dedicated project folders with metadata, timestamps,
application names, descriptions, and automated HTML/Markdown report generation.
"""

import json
import os
import re
from dataclasses import dataclass, asdict
from datetime import datetime
from pathlib import Path
from typing import List, Optional, Dict, Any
from PIL import Image

from core.window_info import get_active_window_info


@dataclass
class StepRecord:
    """Represents an individual captured step."""
    step_number: int
    timestamp: str
    app_name: str
    window_title: str
    description: str
    image_filename: str
    image_path: str

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)


class SessionManager:
    """Manages project-based step recording sessions and reports."""

    def __init__(self, base_directory: Optional[str] = None):
        if base_directory:
            self.base_dir = Path(base_directory)
        else:
            self.base_dir = Path.home() / "Pictures" / "RecordiaCaptures"
        
        self.projects_dir = self.base_dir / "Projects"
        self.projects_dir.mkdir(parents=True, exist_ok=True)

        self.current_project_name: Optional[str] = None
        self.current_session_dir: Optional[Path] = None
        self.screenshots_dir: Optional[Path] = None
        self.steps: List[StepRecord] = []
        self._is_active: bool = False

    @property
    def is_active(self) -> bool:
        return self._is_active

    @property
    def step_count(self) -> int:
        return len(self.steps)

    def start_session(self, project_name: str = "Project") -> Path:
        """
        Initializes a dedicated folder for the project session.
        """
        clean_name = re.sub(r'[\\/*?:"<>| ]', '_', project_name.strip()) or "Project"
        timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        folder_name = f"{clean_name}_{timestamp}"

        self.current_project_name = project_name
        self.current_session_dir = self.projects_dir / folder_name
        self.screenshots_dir = self.current_session_dir / "screenshots"
        self.screenshots_dir.mkdir(parents=True, exist_ok=True)

        self.steps = []
        self._is_active = True

        self._save_metadata()
        return self.current_session_dir

    def record_step(
        self,
        image: Image.Image,
        description: str = "",
        window_info: Optional[Dict[str, Any]] = None
    ) -> StepRecord:
        """
        Records a step with screenshot, timestamp, app name, and description.
        """
        if not self._is_active or not self.screenshots_dir:
            self.start_session("Default_Project")

        step_num = len(self.steps) + 1
        ts = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        info = window_info or get_active_window_info()
        app_name = info.get("app_name", "Desktop")
        win_title = info.get("window_title", "Active Screen")

        desc = description.strip() if description else f"Step performed in {app_name}"

        filename = f"step_{step_num:02d}.png"
        file_path = self.screenshots_dir / filename
        image.save(file_path)

        step = StepRecord(
            step_number=step_num,
            timestamp=ts,
            app_name=app_name,
            window_title=win_title,
            description=desc,
            image_filename=filename,
            image_path=str(file_path)
        )
        self.steps.append(step)
        self._save_metadata()
        return step

    def _save_metadata(self) -> Path:
        """Persists the session metadata JSON file."""
        meta_file = self.current_session_dir / "session_metadata.json"
        data = {
            "project_name": self.current_project_name,
            "session_directory": str(self.current_session_dir),
            "step_count": len(self.steps),
            "created_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "steps": [s.to_dict() for s in self.steps]
        }
        with open(meta_file, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=4)
        return meta_file

    def export_html_report(self) -> Path:
        """
        Generates a responsive HTML report with screenshots and annotations.
        """
        if not self.current_session_dir:
            raise ValueError("No active or completed session to export.")

        html_file = self.current_session_dir / "report.html"
        steps_html = []

        for step in self.steps:
            steps_html.append(f"""
            <div class="step-card">
                <div class="step-header">
                    <span class="step-badge">Step {step.step_number}</span>
                    <span class="step-time">⏱️ {step.timestamp}</span>
                    <span class="app-badge">💻 {step.app_name}</span>
                </div>
                <div class="step-body">
                    <h4 class="window-title">{step.window_title}</h4>
                    <p class="description">{step.description}</p>
                    <div class="image-wrapper">
                        <img src="screenshots/{step.image_filename}" alt="Step {step.step_number}" loading="lazy"/>
                    </div>
                </div>
            </div>
            """)

        full_html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>RecordiaILIA Steps Report - {self.current_project_name}</title>
    <style>
        :root {{
            --primary: #2563eb;
            --bg: #f8fafc;
            --card-bg: #ffffff;
            --text: #1e293b;
            --text-muted: #64748b;
            --border: #e2e8f0;
        }}
        body {{
            font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
            background-color: var(--bg);
            color: var(--text);
            margin: 0;
            padding: 30px 20px;
        }}
        .container {{
            max-width: 960px;
            margin: 0 auto;
        }}
        header {{
            background: var(--card-bg);
            padding: 24px;
            border-radius: 12px;
            border: 1px solid var(--border);
            margin-bottom: 24px;
            box-shadow: 0 1px 3px rgba(0,0,0,0.05);
        }}
        header h1 {{
            margin: 0 0 8px 0;
            color: var(--primary);
        }}
        .meta-bar {{
            display: flex;
            gap: 20px;
            font-size: 0.9em;
            color: var(--text-muted);
        }}
        .step-card {{
            background: var(--card-bg);
            border-radius: 12px;
            border: 1px solid var(--border);
            margin-bottom: 24px;
            overflow: hidden;
            box-shadow: 0 2px 4px rgba(0,0,0,0.04);
        }}
        .step-header {{
            background: #f1f5f9;
            padding: 12px 18px;
            display: flex;
            align-items: center;
            gap: 12px;
            border-bottom: 1px solid var(--border);
        }}
        .step-badge {{
            background: var(--primary);
            color: white;
            font-weight: bold;
            padding: 4px 10px;
            border-radius: 20px;
            font-size: 0.85em;
        }}
        .app-badge {{
            background: #e0e7ff;
            color: #3730a3;
            padding: 4px 10px;
            border-radius: 20px;
            font-size: 0.85em;
            font-weight: 500;
        }}
        .step-time {{
            color: var(--text-muted);
            font-size: 0.85em;
        }}
        .step-body {{
            padding: 18px;
        }}
        .window-title {{
            margin: 0 0 8px 0;
            font-size: 1.1em;
            color: #0f172a;
        }}
        .description {{
            font-size: 1em;
            margin: 0 0 16px 0;
            color: #334155;
            background: #f8fafc;
            padding: 10px 14px;
            border-left: 4px solid var(--primary);
            border-radius: 4px;
        }}
        .image-wrapper {{
            border-radius: 8px;
            overflow: hidden;
            border: 1px solid var(--border);
        }}
        .image-wrapper img {{
            width: 100%;
            height: auto;
            display: block;
        }}
        footer {{
            text-align: center;
            color: var(--text-muted);
            font-size: 0.85em;
            margin-top: 40px;
        }}
    </style>
</head>
<body>
    <div class="container">
        <header>
            <h1>RecordiaILIA Steps Report</h1>
            <div class="meta-bar">
                <span>📁 <strong>Project:</strong> {self.current_project_name}</span>
                <span>🔢 <strong>Steps Captured:</strong> {len(self.steps)}</span>
                <span>📅 <strong>Generated:</strong> {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</span>
            </div>
        </header>

        <div class="steps-list">
            {''.join(steps_html) if steps_html else '<p>No steps recorded.</p>'}
        </div>

        <footer>
            Generated automatically by <strong>RecordiaILIA Steps Recorder</strong>
        </footer>
    </div>
</body>
</html>
"""
        with open(html_file, "w", encoding="utf-8") as f:
            f.write(full_html)
        return html_file

    def export_markdown_report(self) -> Path:
        """
        Generates a Markdown report summary for the project session.
        """
        if not self.current_session_dir:
            raise ValueError("No active or completed session to export.")

        md_file = self.current_session_dir / "REPORT.md"
        lines = [
            f"# Steps Recording Report: {self.current_project_name}",
            "",
            f"- **Date Generated**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
            f"- **Total Steps**: {len(self.steps)}",
            f"- **Session Directory**: `{self.current_session_dir}`",
            "",
            "---",
            "",
            "## Recorded Steps",
            ""
        ]

        for s in self.steps:
            lines.extend([
                f"### Step {s.step_number}: {s.app_name}",
                f"- **Window Title**: {s.window_title}",
                f"- **Timestamp**: {s.timestamp}",
                f"- **Description**: {s.description}",
                f"",
                f"![Step {s.step_number}](screenshots/{s.image_filename})",
                "",
                "---",
                ""
            ])

        with open(md_file, "w", encoding="utf-8") as f:
            f.write("\n".join(lines))
        return md_file

    def finish_session(self) -> Dict[str, Any]:
        """
        Finalizes active recording session and exports all reports.
        """
        if not self.current_session_dir:
            return {"status": "no_active_session"}

        meta_path = self._save_metadata()
        html_path = self.export_html_report()
        md_path = self.export_markdown_report()
        session_path = str(self.current_session_dir)

        count = len(self.steps)
        self._is_active = False

        return {
            "project_name": self.current_project_name,
            "session_directory": session_path,
            "step_count": count,
            "metadata_file": str(meta_path),
            "html_report": str(html_path),
            "markdown_report": str(md_path)
        }

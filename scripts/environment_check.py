#!/usr/bin/env python3
"""Read-only environment feature report; no downloads or configuration changes."""
import importlib.util
import json
import platform
import shutil
import sys

def diagnose():
    commands = ("python3", "python", "git", "node", "npm", "codex")
    modules = ("openpyxl", "pandas", "numpy", "pytest", "reportlab", "docx", "matplotlib")
    return {
        "platform": platform.platform(),
        "python": platform.python_version(),
        "commands": {name: bool(shutil.which(name)) for name in commands},
        "optional_modules": {name: importlib.util.find_spec(name) is not None for name in modules},
        "notes": ["읽기 전용 검사. 다운로드·설치·설정 변경 없음.",
                  "설치 여부는 실행 권한이나 실제 정상 작동을 증명하지 않습니다."],
    }

if __name__ == "__main__":
    print(json.dumps(diagnose(), ensure_ascii=False, indent=2))

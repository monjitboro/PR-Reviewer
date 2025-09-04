import subprocess
import json
from typing import List, Dict


def run_ruff(paths: List[str]) -> List[Dict]:
    if not paths:
        return []
    cmd = ["ruff", "check", "--format", "json"] + paths
    try:
        out = subprocess.check_output(cmd, text=True, stderr=subprocess.STDOUT)
        issues = json.loads(out) if out.strip() else []
        return _format_ruff(issues)
    except subprocess.CalledProcessError as e:
# Ruff exits non-zero when issues found; still parse output
        try:
            issues = json.loads(e.output) if e.output else []
            return _format_ruff(issues)
        except Exception:
            return []




def _format_ruff(issues_json) -> List[Dict]:
    comments: List[Dict] = []
    for it in issues_json:
        comments.append({
        "file": it.get("filename"),
        "line": it.get("location", {}).get("row", 1),
        "body": f"[Ruff {it.get('code')}] {it.get('message')}",
    })
    return comments
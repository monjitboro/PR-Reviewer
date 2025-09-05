import re
from typing import List, Dict

def style_checks(filename: str, patch: str) -> List[Dict]:
    findings = []
    if filename.endswith(".py"):
        if re.search(r"\bprint\(", patch):
            findings.append({
                "type":"style",
                "name":"print used in library code",
                "severity":"low",
                "why":"Consider logging instead of print for libraries/services.",
                "file": filename
            })
        if re.search(r"def\s+\w+\(.*\):\n(\s+.*\n){50,}", patch, re.MULTILINE):
            findings.append({
                "type":"style",
                "name":"Very long function",
                "severity":"medium",
                "why":"Consider splitting long functions for readability.",
                "file": filename
            })
    return findings

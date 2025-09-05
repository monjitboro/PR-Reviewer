import re
from typing import List, Dict

_PATTERNS = [
    {"name":"eval() usage", "regex": r"\beval\s*\(", "severity":"high", "why":"Arbitrary code execution risk."},
    {"name":"exec() usage", "regex": r"\bexec\s*\(", "severity":"high", "why":"Arbitrary code execution risk."},
    {"name":"subprocess with shell=True", "regex": r"subprocess\.\w+\(.*shell\s*=\s*True", "severity":"high", "why":"Shell injection risk."},
    {"name":"Hardcoded AWS key", "regex": r"AKIA[0-9A-Z]{16}", "severity":"critical", "why":"Leaked cloud credentials."},
    {"name":"Hardcoded password", "regex": r"password\s*=\s*['\"]\w+['\"]", "severity":"high", "why":"Credential leakage."},
]

def security_checks(filename: str, patch: str) -> List[Dict]:
    findings = []
    for pat in _PATTERNS:
        if re.search(pat["regex"], patch):
            findings.append({
                "type": "security",
                "name": pat["name"],
                "severity": pat["severity"],
                "why": pat["why"],
                "file": filename
            })
    return findings

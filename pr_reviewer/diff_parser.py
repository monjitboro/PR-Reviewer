import requests, math
from typing import List, Dict, Any

API = "https://api.github.com"

def fetch_pr_files(owner: str, repo: str, pr: int, token: str, max_total_files: int = 20) -> list:
    url = f"{API}/repos/{owner}/{repo}/pulls/{pr}/files?per_page=100"
    headers = {
        "Authorization": f"Bearer {token}",
        "Accept": "application/vnd.github+json",
    } if token else {"Accept": "application/vnd.github+json"}

    files = []
    page = 1
    while True:
        r = requests.get(url + f"&page={page}", headers=headers, timeout=30)
        if r.status_code != 200:
            break
        chunk = r.json()
        files.extend(chunk)
        if len(chunk) < 100 or len(files) >= max_total_files:
            break
        page += 1

    return files[:max_total_files]

def chunk_patch(patch: str, max_lines: int = 300) -> List[str]:
    lines = patch.splitlines()
    chunks = []
    for i in range(0, len(lines), max_lines):
        part = "\n".join(lines[i:i+max_lines])
        chunks.append(part)
    return chunks

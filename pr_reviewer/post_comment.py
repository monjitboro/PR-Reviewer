import requests

def post_issue_comment(owner: str, repo: str, pr_number: int, body: str, token: str) -> bool:
    url = f"https://api.github.com/repos/{owner}/{repo}/issues/{pr_number}/comments"
    headers = {
        "Authorization": f"Bearer {token}",
        "Accept": "application/vnd.github+json",
    } if token else {"Accept": "application/vnd.github+json"}
    r = requests.post(url, headers=headers, json={"body": body}, timeout=30)
    return r.status_code == 201

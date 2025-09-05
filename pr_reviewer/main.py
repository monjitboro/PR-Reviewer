import argparse, os, json, sys, textwrap
from typing import List, Dict, Any, Tuple

from .llm import LLMClient
from .diff_parser import fetch_pr_files, chunk_patch
from .reviewers.security import security_checks
from .reviewers.style import style_checks
from .formatters.github import build_comment_markdown
from .post_comment import post_issue_comment
from .util import load_config

def run(repo: str, pr: int, token: str, event_path: str = None, dry_run: bool = False) -> int:
    cfg = load_config()
    model = cfg.get("model", "gpt-4o-mini")
    max_file_bytes = int(cfg.get("max_file_bytes", 20000))
    max_total_files = int(cfg.get("max_total_files", 20))

    if event_path:
        with open(event_path, "r", encoding="utf-8") as f:
            ev = json.load(f)
        # override if present
        if "pull_request" in ev:
            pr = ev["pull_request"]["number"]
            repo_full = ev["repository"]["full_name"]
            repo = repo_full

    owner, name = repo.split("/", 1)

    files = fetch_pr_files(owner, name, pr, token, max_total_files=max_total_files)
    if not files:
        print("No changed files detected or API error.", file=sys.stderr)
        return 0

    # Build review content
    llm = LLMClient(model=model)
    all_sections = []
    severe_findings = []

    for f in files:
        filename = f.get("filename")
        patch = f.get("patch") or ""
        if not patch:
            continue
        if len(patch.encode("utf-8")) > max_file_bytes:
            patch = patch[:max_file_bytes] + "\n... [truncated]\n"

        # Static checks
        sec = security_checks(filename, patch)
        sty = style_checks(filename, patch)

        if any(it.get("severity") == "critical" for it in sec):
            severe_findings.extend([it for it in sec if it.get("severity") == "critical"])

        # LLM suggestions (chunking if long)
        chunks = chunk_patch(patch, max_lines=300)
        suggestions = []
        for idx, ch in enumerate(chunks, 1):
            resp = llm.review_diff(filename, ch)
            suggestions.append({"chunk": idx, "text": resp})

        section = {
            "filename": filename,
            "security": sec,
            "style": sty,
            "llm": suggestions
        }
        all_sections.append(section)

    body = build_comment_markdown(all_sections, title=cfg.get("comment_title", "🤖 LLM PR Review"))

    if dry_run:
        print(body)
    else:
        ok = post_issue_comment(owner, name, pr, body, token or os.getenv("GITHUB_TOKEN"))
        if not ok:
            print("Failed to post comment.", file=sys.stderr)
            return 1

    if cfg.get("fail_on_severe_findings") and severe_findings:
        print("Severe findings detected. Failing as per config.")
        return 2

    return 0

def cli():
    p = argparse.ArgumentParser(description="LLM-powered PR reviewer")
    p.add_argument("--repo", help="owner/repo (e.g., octocat/hello-world)")
    p.add_argument("--pr", type=int, help="PR number")
    p.add_argument("--token", help="GitHub token (or set GITHUB_TOKEN)")
    p.add_argument("--event-path", help="Path to GitHub event JSON")
    p.add_argument("--dry-run", action="store_true", help="Print review instead of posting")
    args = p.parse_args()

    repo = args.repo
    pr = args.pr
    token = args.token or os.getenv("GITHUB_TOKEN", "")

    if not args.event_path and (not repo or not pr):
        p.error("Either --event-path or both --repo and --pr are required.")

    code = run(repo, pr, token, event_path=args.event_path, dry_run=args.dry_run)
    sys.exit(code)

if __name__ == "__main__":
    cli()

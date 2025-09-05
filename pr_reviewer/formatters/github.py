from typing import List, Dict

def _badge(sev: str) -> str:
    mapping = {
        "critical":"🛑",
        "high":"⚠️",
        "medium":"🟠",
        "low":"🟢",
    }
    return mapping.get(sev, "•")

def build_comment_markdown(sections: List[Dict], title: str = "🤖 LLM PR Review") -> str:
    lines = [f"## {title}", "", "_Automated suggestions. Please use your judgment before applying changes._", ""]

    for s in sections:
        lines.append(f"### `{s['filename']}`")
        sec = s.get("security", [])
        sty = s.get("style", [])
        llm = s.get("llm", [])

        if sec:
            lines.append("**Security checks:**")
            for it in sec:
                lines.append(f"- {_badge(it.get('severity',''))} **{it['name']}** — {it['why']}")
            lines.append("")

        if sty:
            lines.append("**Style checks:**")
            for it in sty:
                lines.append(f"- {_badge(it.get('severity',''))} **{it['name']}** — {it['why']}")
            lines.append("")

        if llm:
            lines.append("**LLM suggestions:**")
            for sug in llm:
                lines.append(sug["text"])
                if not sug["text"].endswith("\n"):
                    lines.append("")
        lines.append("---\n")

    return "\n".join(lines)

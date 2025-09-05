import os, textwrap
from typing import Optional
from openai import OpenAI

_SYSTEM = """You are an expert code reviewer. Provide concise, actionable feedback.
- Focus on *changes in the diff*
- Prioritize: correctness, security, performance, readability
- If suggesting code, provide minimal, targeted patches in fenced blocks.
- Avoid speculative advice if the diff doesn't support it.
- Do not include private chain-of-thought; only final suggestions.
"""

USER_TMPL = """Filename: {filename}

Diff (unified):
```
{diff}
```

Provide:
1) 2-6 succinct suggestions with rationale.
2) If needed, a small code patch using ```diff fences.
3) Key risks or follow-ups, if any.
"""

class LLMClient:
    def __init__(self, model: str = "gpt-4o-mini"):
        self.model = model
        # OPENAI_API_KEY must be set in env
        self.client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

    def review_diff(self, filename: str, diff_text: str) -> str:
        user = USER_TMPL.format(filename=filename, diff=diff_text)
        resp = self.client.chat.completions.create(
            model=self.model,
            messages=[
                {"role":"system","content":_SYSTEM},
                {"role":"user","content":user},
            ],
            temperature=0.2,
        )
        return resp.choices[0].message.content.strip()

from transformers import pipeline


_MODEL_ID = "Salesforce/codet5-small"


_PROMPT = (
    "You are a senior engineer performing a code review.\n"
    "Given this unified diff hunk, write 1-3 concise, actionable review comments.\n"
    "Each comment should reference a line number if possible and be specific.\n\n"
    "Diff:\n{diff}\n\nComments:\n"
)




class LLMSuggester:
    def __init__(self):
        # text2text works well for instruction-style prompts
        self.generator = pipeline("text2text-generation", model=_MODEL_ID)


    def suggest_for_hunk(self, hunk_text: str, max_new_tokens: int = 128) -> list[str]:
        # Keep prompt bounded to avoid CI timeouts
        prompt = _PROMPT.format(diff=hunk_text[:2000])
        out = self.generator(prompt, max_new_tokens=max_new_tokens, do_sample=False)
        text = out[0]["generated_text"].strip()
        # Split into lines; filter short noise; cap at 3 suggestions
        lines = [l.strip("-•* ").strip() for l in text.splitlines() if l.strip()]
        return [l for l in lines if len(l) > 5][:3]
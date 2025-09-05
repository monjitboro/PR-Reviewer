import os, yaml

def load_config(path: str = "pr_reviewer.yaml") -> dict:
    if os.path.exists(path):
        with open(path, "r", encoding="utf-8") as f:
            return yaml.safe_load(f) or {}
    # Try default shipped config
    default_path = os.path.join(os.path.dirname(__file__), "..", "pr_reviewer.yaml")
    if os.path.exists(default_path):
        with open(default_path, "r", encoding="utf-8") as f:
            return yaml.safe_load(f) or {}
    return {}

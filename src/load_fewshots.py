import os
import yaml
from difflib import get_close_matches

def load_fewshots(path="src/response_fewshots.yaml"):
    if not os.path.exists(path):
        return {}
    with open(path, "r") as f:
        return yaml.safe_load(f) or {}

def find_answer_from_yaml(tool: str, query: str, fewshots: dict) -> str:
    if tool not in fewshots:
        return None

    examples = fewshots[tool]
    queries = [ex["input"] for ex in examples if "input" in ex]
    match = get_close_matches(query, queries, n=1, cutoff=0.85)
    
    if match:
        for ex in examples:
            if ex["input"] == match[0]:
                return ex.get("answer")
    return None
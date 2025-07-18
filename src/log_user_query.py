import json
import os
from datetime import datetime

MEMORY_PATH = "logs/user_query_memory.jsonl"
os.makedirs("logs", exist_ok=True)

def log_user_interaction(query, tool, response):
    entry = {
        "timestamp": datetime.now().isoformat(),
        "query": query,
        "tool": tool,
        "response": response
    }
    with open(MEMORY_PATH, "a") as f:
        f.write(json.dumps(entry) + "\n")

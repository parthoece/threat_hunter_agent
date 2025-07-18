import os
import json
import yaml
from datetime import datetime
from langchain_community.llms import Ollama
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain

# File paths
FEWSHOT_PATH = "src/response_fewshots.yaml"
MEMORY_PATH = "logs/user_query_memory.jsonl"

# Load few-shot examples from YAML
def load_fewshot_examples(path=FEWSHOT_PATH):
    if not os.path.exists(path):
        return []
    with open(path, "r", encoding="utf-8") as f:
        data = yaml.safe_load(f)
    return data.get("ResponderPlanner", [])

# Load past user queries from memory
def load_past_user_queries(memory_path=MEMORY_PATH):
    if not os.path.exists(memory_path):
        return []
    with open(memory_path, "r") as f:
        return [json.loads(line) for line in f if "ResponderPlanner" in line]

# Combine few-shot and memory examples to build prompt context
def build_context_examples():
    fewshots = load_fewshot_examples()
    memory = load_past_user_queries()
    examples = [f"Q: {ex['input']}\nA: (LLM will fill this in)" for ex in fewshots]
    examples += [f"Q: {m['query']}\nA: {m['response']}" for m in memory if m.get("response")]
    return examples[:6]  # Limit to 6 for prompt size

# Initialize LLM
llm = Ollama(model="mistral")

# Adaptive responder function

def adaptive_plan_response(query: str) -> str:
    examples = build_context_examples()
    fewshot_prompt = "\n\n".join(examples)

    prompt = PromptTemplate(
        input_variables=["query"],
        template=(
            "You are an ICS incident responder. Given user queries about cyber threats in ICS systems, provide actionable and realistic incident response steps."
            "\n\nHere are a few examples:\n"
            f"{fewshot_prompt}\n\n"
            "Now respond to the new query below.\n"
            "Q: {{query}}\nA:"
        )
    )

    chain = LLMChain(llm=llm, prompt=prompt)
    response = chain.run(query=query)

    # Optionally log this response for future adaptation
    os.makedirs("logs", exist_ok=True)
    log_entry = {
        "timestamp": datetime.now().isoformat(),
        "query": query,
        "tool": "ResponderPlanner",
        "response": response.strip()
    }
    with open(MEMORY_PATH, "a") as f:
        f.write(json.dumps(log_entry) + "\n")

    return response.strip()

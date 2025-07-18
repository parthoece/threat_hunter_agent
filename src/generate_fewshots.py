import os
import yaml
import random

def generate_fewshot_examples_from_vcdb(ics_data, max_per_tool=3):
    search_incident_examples = []
    summarizer_examples = []
    responder_examples = []

    for entry in ics_data:
        desc = entry.get("summary") or entry.get("incident", "")
        if not desc or len(desc) < 40:
            continue

        # SearchIncidents example
        if len(search_incident_examples) < max_per_tool:
            actor = entry.get("actor", {}).get("external", {}).get("name", "unknown actor")
            query = f"What happened during the {actor} ICS breach?"
            search_incident_examples.append((query, "SearchIncidents"))

        # Summarizer example
        if len(summarizer_examples) < max_per_tool:
            victim = entry.get("victim", {}).get("name", "an ICS company")
            query = f"Summarize the ICS incident involving {victim}."
            summarizer_examples.append((query, "Summarizer"))

        # ResponderPlanner example
        if len(responder_examples) < max_per_tool and "malware" in desc.lower():
            query = "What steps should I take after detecting malware in ICS systems?"
            responder_examples.append((query, "ResponderPlanner"))

        if all(len(lst) >= max_per_tool for lst in [search_incident_examples, summarizer_examples, responder_examples]):
            break

    return search_incident_examples + summarizer_examples + responder_examples

def save_fewshots_to_yaml(examples, path="src/response_fewshots.yaml"):
    grouped = {"SearchIncidents": [], "Summarizer": [], "ResponderPlanner": []}
    for q, tool in examples:
        if tool in grouped:
            grouped[tool].append({"input": q})

    os.makedirs(os.path.dirname(path), exist_ok=True)

    with open(path, "w", encoding="utf-8") as f:
        yaml.dump(grouped, f, sort_keys=False, allow_unicode=True)

    print(f"Few-shot examples saved to {path}")

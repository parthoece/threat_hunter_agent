---
title: ICS Incident Response Assistant
emoji: 🛡️
colorFrom: gray
colorTo: blue
sdk: gradio
sdk_version: 3.36.1
app_file: app_agent.py
pinned: false
license: mit
---

# ICS Incident Response Assistant (Agentic, Offline, Local LLM)

A lightweight, fully offline, agent-based AI assistant for ICS threat hunting and incident response. This system runs entirely on local CPU hardware, leverages Mistral via Ollama for LLM reasoning, and supports modular planning and search workflows using real-world ICS incident datasets.

## Problem

Industrial Control Systems (ICS) are a prime target for cyberattacks, yet incident response in this domain remains highly manual, data-siloed, and reactive. Security analysts often struggle to navigate past ICS incidents, identify common threats, and suggest appropriate mitigations due to:

- Fragmented or unstructured incident data
- Lack of integrated threat modeling tools
- No access to cloud-based AI in air-gapped ICS environments

## Solution

This project introduces a fully local, CPU-compatible, agent-based assistant that:

- Extracts ICS-related incidents from Verizon's VCDB dataset
- Enables semantic search and Q&A using a local LLM (Mistral via Ollama)
- Suggests incident response steps using rule-based planning with YAML logic
- Runs entirely offline with no paid API or internet access required

The system is built with LangChain's agent framework and served through a Gradio interface.

### How the Solution Works (System Overview)

The architecture processes user input through a tool-using agent pipeline. It includes:

1. Input via Gradio UI with tool selection (`SearchIncidents`, `ResponderPlanner`, `Summarizer`)
2. Incident extraction and preprocessing from VCDB JSON data
3. Tool execution using FAISS for RAG, YAML for rule logic, and LLMs for reasoning
4. Local LLM inference using Mistral via Ollama
5. Optional few-shot example injection and logging

Example query:
- "Summarize a boundary logic tampering incident in ICS"

## Features

- Search past ICS incidents using a semantic retriever
- Suggest response plans using a rule-based planner
- Summarize threat patterns (experimental)
- Completely offline and API-free

## Example Prompts

- Show ICS incidents involving ransomware
- Plan a response for boundary logic tampering
- Summarize kill chain for Triton malware

## Tools

- SearchIncidents: Semantic QA over VCDB with FAISS + LLM
- ResponderPlanner: YAML + few-shot-based IR suggestions
- Summarizer: Summarizes kill chains (prototype)

## Quickstart

Make sure you have Ollama running locally:

```bash
ollama run mistral
```

Then launch the app:

```bash
python app_agent.py
```

You may optionally add VCDB JSON files in `data/vcdb/`.

## License

MIT License

## Author

Partho Adhikari  
Email: parthoece23@gmail.com

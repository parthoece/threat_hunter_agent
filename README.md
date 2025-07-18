# 🛡️ ICS Incident Response Assistant (Agentic, Local LLM – Mistral via Ollama)

A lightweight, fully offline, agent-based AI assistant for ICS threat hunting and incident response. This system runs entirely on local CPU hardware, leverages Mistral via Ollama for LLM reasoning, and supports modular planning and search workflows using real-world ICS incident datasets.

**Sections:**
- [Problem](#problem)
- [Solution](#solution)
- [Quickstart](#quickstart)
- [Kubernetes + EC2 Deployment](#kubernetes--ec2-deployment)
- [Tools](#tools)
- [Project Structure & Versioning](#project-structure--versioning)

---

## Problem

Industrial Control Systems (ICS) are a prime target for cyberattacks, yet incident response in this domain remains highly manual, data-siloed, and reactive. Security analysts often struggle to navigate past ICS incidents, identify common threats, and suggest appropriate mitigations due to:

- Fragmented or unstructured incident data
- Lack of integrated threat modeling tools
- No access to cloud-based AI in air-gapped ICS environments

---

## Solution

This project introduces a fully local, CPU-compatible, agent-based assistant that:

- Extracts ICS-related incidents from Verizon's VCDB dataset
- Enables semantic search and Q&A using a local LLM (Mistral via Ollama)
- Suggests incident response steps using rule-based planning with YAML logic
- Runs entirely offline with no paid API or internet access required

Built using LangChain's agent framework and served through a lightweight Gradio UI, this system enables:

- Rapid threat identification from historical attacks
- Scenario-based response planning
- Summarization of attacker behavior

### Solution Architecture


---

###  How the Solution Works (System Overview)

The diagram below shows the internal architecture of the ICS Incident Response Assistant and how it processes queries using an agentic LLM pipeline.

![Agentic Workflow](assets/system.jpg)

#### Workflow Breakdown:

1. **Input & Agent Interaction**  
   Users interact via a simple Gradio UI, selecting a tool (e.g., `SearchIncidents`, `ResponderPlanner`, or `Summarizer`) and entering a query, such as:
   > _"Summarize a boundary logic tampering incident in ICS."_  

2. **ICS Incident Corpus**  
   The assistant extracts ICS-relevant entries from the VCDB (Verizon Data Breach DB), preprocesses them, and converts them into LangChain-compatible document objects.

3. **Tool Execution**  
   - **SearchIncidents**: Uses semantic retrieval (via FAISS) + Mistral to answer incident-specific questions.  
   - **ResponderPlanner**: Applies rule-based logic (YAML + few-shot examples) to propose incident mitigation steps.  
   - **Summarizer**: (Experimental) Produces concise summaries of killchains and attack patterns using LLM.

4. **LLM Reasoning Engine**  
   Mistral (accessed locally via Ollama) is used as the backend for reasoning. It runs in zero-shot reactive mode with tool context prompts.

5. **Few-Shot Memory + Logs**  
   Tool responses are enriched with example-driven answers (loaded from YAML), and all user interactions are logged for future audit and improvement.

This design supports real-time, offline ICS incident assistance—emulating a security analyst while ensuring reproducibility, explainability, and air-gapped safety.


---

## Quickstart

To set up locally:

```bash
# Step 1: Clone Repository and Setup Environment
python3 -m venv icsenv
source icsenv/bin/activate
git clone https://github.com/parthoece/threat_hunter_agent.git
cd threat_hunter_agent

# Step 2: Install Dependencies
pip install --upgrade pip
pip install -r requirements.txt

# Step 3: Install Ollama and Pull Mistral Model
curl -fsSL https://ollama.com/install.sh | sh  # For Linux
# brew install ollama                          # For Mac
ollama pull mistral
ollama run mistral
```

```bash
# Step 4: Add VCDB JSON data
python download_vcdb.py
mkdir -p data/vcdb/
cp your_files.json data/vcdb/

# Step 5: Launch
python app_agent.py
```

Visit `http://localhost:7860`

# Test & Push to Git
```bash
python tests/test_app.py


# Now start pushing to git
git init
git remote add origin https://github.com/YOUR_USERNAME/threat_hunter_agent.git
git add .
git commit -m "Initial commit with CI"
git pull origin main --rebase
git push -u origin main

# Avoid large files, put them in gitignore
touch .gitignore #open in editor
 icsenv/ # add this line in gitignore file
git rm -r --cached icsenv/ #Remove Already Tracked Virtual Environment
git commit -m "Remove virtual environment from version control"
git pull origin main --rebase
git push -u origin main

---

## Kubernetes + EC2 Deployment

### Option A: EC2 + Docker

```bash
docker build -t ics-agent .
docker run -p 7860:7860 ics-agent
```

Expose using EC2 Public IP or with:

```bash
ngrok http 7860
```

### Option B: Kubernetes (Minikube or EKS)

```bash
docker build -t your-repo/ics-agent:latest .
docker push your-repo/ics-agent:latest
```

Create `deployment.yaml`:

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: ics-agent
spec:
  replicas: 1
  selector:
    matchLabels:
      app: ics-agent
  template:
    metadata:
      labels:
        app: ics-agent
    spec:
      containers:
      - name: app
        image: your-repo/ics-agent:latest
        ports:
        - containerPort: 7860
```

Then run:

```bash
kubectl apply -f deployment.yaml
kubectl expose deployment ics-agent --type=LoadBalancer --port=7860
```

---

## Tools

| Tool Name         | Description                                     |
| ----------------- | ----------------------------------------------- |
| Search Incidents  | RAG-based semantic retrieval from VCDB corpus   |
| Responder Planner | Suggests mitigation via rule-based YAML logic   |
| Summarizer        | (Experimental) Summarizes threat chains locally |

Example prompts:

- "Show ICS incidents involving ransomware."
- "Plan a response for boundary logic tampering."
- "Summarize kill chain for Triton malware."

### LLM Output

**1. Search Interface**  
![Search View](assets/search_incident.jpg)

**2. Response Planner Output**  
![Response Planner](assets/responder_plan.jpg)

**3. Summary Example (Triton ICS)**  
![Summarizer](assets/summarizer_view.jpg)

---

## Project Structure & Versioning

```
ics-incident-assistant/
├── data/vcdb/               # Place VCDB JSON files here
├── notebooks/               # Optional exploratory notebooks
├── src/                     # All core modules
│   ├── extract_ics.py       # Extract ICS incidents
│   ├── preprocess.py        # Convert to LangChain docs
│   ├── vector_store.py      # FAISS vector DB
│   ├── qa_chain.py          # LLM + retriever chain
│   ├── responder_planner.py # Rule-based response planner
│   └── run.py               # CLI version
├── app_agent.py             # Gradio agent UI (Ollama-powered)
├── requirements.txt         # Python dependencies
└── README.md                # You are here
```

### Versioning

- Python ≥ 3.8
- LangChain ≥ 0.1.0
- Ollama (latest)
- Mistral 7B-Instruct (via `ollama pull mistral`)

---

### License

MIT License

---

### Author

Built by **Partho Adhikari**  
📧 [parthoece23@gmail.com](mailto:parthoece23@gmail.com)

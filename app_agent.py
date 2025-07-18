import os
import traceback
import gradio as gr
import logging

from langchain_community.llms import Ollama
from langchain.agents import initialize_agent, Tool

from src.extract_ics import extract_ics_incidents
from src.preprocess import preprocess_for_langchain
from src.vector_store import create_vectorstore
from src.qa_chain import build_qa_chain
from src.responder_planner import adaptive_plan_response as plan_response
from src.log_user_query import log_user_interaction  #  NEW: log queries/responses
from src.load_fewshots import load_fewshots, find_answer_from_yaml

# Create logs folder
os.makedirs("logs", exist_ok=True)

# Configure logging
logging.basicConfig(
    filename="logs/app_agent.log",
    level=logging.ERROR,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

# Step 1: Load ICS data
vcdb_path = "data/vcdb"
if not os.path.exists(vcdb_path) or not os.listdir(vcdb_path):
    raise FileNotFoundError(
        "No VCDB files found in data/vcdb. Please download JSON files from https://github.com/vz-risk/VCDB/tree/master/data/json"
    )

print("Extracting ICS-related incidents from VCDB...")
ics_data = extract_ics_incidents(vcdb_path)
if not ics_data:
    print("No ICS-related incidents found. Using all incidents for demo/testing.")
    ics_data = extract_ics_incidents(vcdb_path, fallback_if_empty=True)
print("Number of ICS incidents loaded:", len(ics_data))

# Step 2: Vectorstore & Chain
docs = preprocess_for_langchain(ics_data)
vectorstore = create_vectorstore(docs)
retriever = vectorstore.as_retriever()
qa_chain = build_qa_chain(retriever)

# Step 3: Summarizer
def summarize_example(query):
    return "Summary: This is a placeholder summary for: " + query

# Step 4: LLM
llm = Ollama(model="mistral")

# Step 5: Toolset
toolset = {
    "SearchIncidents": Tool(
        name="SearchIncidents",
        func=lambda q: qa_chain.invoke({"query": q})["result"],
        description="Use to answer ICS-related questions from historical incidents."
    ),
    "Summarizer": Tool(
        name="Summarizer",
        func=summarize_example,
        description="Use to summarize user queries."
    ),
    "ResponderPlanner": Tool(
        name="ResponderPlanner",
        func=plan_response,  #  Now uses adaptive responder logic with few-shot + memory
        description="Use to suggest incident response actions based on attack type."
    )
}

# Step 6: Agent logic
# Load few-shot YAML data once globally
fewshot_data = load_fewshots("src/response_fewshots.yaml")

def run_agentic_tool(query, selected_tool):
    try:
        if not selected_tool or selected_tool not in toolset:
            return (
                "The selected tool is unavailable. Please select a valid option: "
                "SearchIncidents, ResponderPlanner, or Summarizer."
            )

        #  First try to find a close match from YAML
        fewshot_response = find_answer_from_yaml(selected_tool, query, fewshot_data)
        if fewshot_response:
            log_user_interaction(query=query, tool=selected_tool, response=fewshot_response)
            return fewshot_response

        # Otherwise use the tool agent
        tool = toolset[selected_tool]
        agent = initialize_agent(
            tools=[tool],
            llm=llm,
            agent="zero-shot-react-description",
            handle_parsing_errors=True,
            verbose=False
        )

        if len(query.strip()) < 10:
            query += " (Note: Please provide more context if possible — e.g., attack type, ICS layer, or impact.)"

        system_prompt = (
            f"You are a cybersecurity assistant trained on ICS incident reports. "
            f"Your task is to use the tool '{selected_tool}' to assist the user. "
            f"Respond clearly. If the input is vague, make safe assumptions or ask for clarification."
        )

        full_prompt = f"{system_prompt}\nUser query: {query}"
        response = agent.run(full_prompt)

        log_user_interaction(query=query, tool=selected_tool, response=response)
        return response or "The assistant could not generate a response. Try asking with more context."

    except Exception as e:
        traceback.print_exc()
        logging.error("Agent execution failed", exc_info=True)
        return "An error occurred while processing your request. Please try again later."

# Step 7: UI with Gradio
iface = gr.Interface(
    fn=run_agentic_tool,
    inputs=[
        gr.Textbox(label="Enter your query", lines=3, placeholder="Example: What to do during a ransomware attack?"),
        gr.Dropdown(
            choices=list(toolset.keys()),
            label="Select Tool",
            info="Select one of the available tools"
        )
    ],
    outputs=gr.Textbox(label="Assistant Response"),
    title="ICS Incident Response Assistant",
    description="Ask about ICS cyberattacks, response actions, or request summaries.",
    examples=[
    #  Protocol-based threat hunting (SearchIncidents)
    ["Have there been any ICS incidents involving abnormal Modbus function codes or command injection over TCP port 502?", "SearchIncidents"],
    ["Are there any documented attacks that altered boundary function logic in PLCs or bypassed safety interlocks in ICS?", "SearchIncidents"],

    #  Response with MALCOLM (ResponderPlanner)
    ["How can I use MALCOLM to detect abnormal Modbus write commands targeting PLCs?", "ResponderPlanner"],
    ["What steps should I follow in MALCOLM to investigate suspicious boundary function changes during ICS compromise?", "ResponderPlanner"],

    #  Technical summaries (Summarizer)
    ["Summarize a real ICS incident where attackers used unauthorized Modbus writes or DNP3 protocol abuse.", "Summarizer"],
    ["Summarize a kill chain scenario where boundary logic in a chemical plant PLC was manipulated via protocol abuse.", "Summarizer"]
]

)

if __name__ == "__main__":
    print("Launching ICS Assistant UI at http://127.0.0.1:7860")
    iface.launch(server_port=7860, share=False, inbrowser=True)

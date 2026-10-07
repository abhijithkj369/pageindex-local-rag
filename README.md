# PageIndex Local Open-Source RAG

A simple, fully open-source demonstration of **PageIndex**—a vectorless, reasoning-based RAG framework. This project runs entirely locally, replacing traditional vector databases and chunking with a hierarchical document tree searched agentically by a local LLM.

## Tech Stack
- **Framework:** [PageIndex](https://github.com/VectifyAI/PageIndex) (Agentic Tree RAG)
- **Local LLM Server:** [Ollama](https://ollama.com/)
- **Model:** Llama 3.1 (8B)
- **Dataset:** "Attention Is All You Need" (Open Access Research Paper)

## How It Works
Unlike traditional RAG that relies on semantic similarity (which often retrieves similar but irrelevant chunks), PageIndex extracts the document layout into a hierarchical tree structure. An LLM then reasons through this tree to find the exact context needed, mimicking how a human expert reads a long report.

## Setup Instructions

1. **Install Ollama and pull the model:**
   Ensure Ollama is running locally, then download the model:

bash
ollama run llama3.1


2. **Install Python dependencies:**
bash
pip install -r requirements.txt


3. **Get the Dataset:**
Download the sample document into the root folder:
bash
curl -o attention_is_all_you_need.pdf https://arxiv.org/pdf/1706.03762.pdf


4. **Run the application:**
bash
python app.py

## 🔍 Inspecting the Tree (Under the Hood)
Run `python inspect_tree.py` to generate `document_tree.json`. 

## 🕵️ Inspecting the Agent Trace

When building Agentic RAG with local models (like Llama 3.1 8B), you will often encounter **Tool Hallucinations**—where the LLM understands what to do, but generates the wrong JSON schema for the tool.

We built an internal trace inspector in `app.py` to watch the agent's internal reasoning, tool calls, and tool errors in real time. 

### Prompt-Based Schema Enforcement
To fix tool schema hallucinations in smaller models without fine-tuning, we use the `instructions` parameter to strictly enforce the schema rules at runtime:

bash
python
stream = client.chat(
question,
doc_id=doc_id,
stream=True,
instructions=(
"When using get_page_content, you MUST provide the required "
"pages argument. Never use page_range, start_index, or end_index."
)
)

Running `python app.py` will now output a color-coded trace showing the exact API calls the agent makes to the document tree, making it incredibly easy to debug and optimize local LLM behavior.

**Why this matters:**
Traditional RAG cuts documents into meaningless 1,000-character chunks. PageIndex builds a hierarchical tree (Chapters -> Sections -> Paragraphs). During a query, the LLM agent actively reads the node summaries and navigates down the most relevant branches—simulating how a human uses a Table of Contents to find an answer without reading the whole book.


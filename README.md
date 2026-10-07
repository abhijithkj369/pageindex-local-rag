<div align="center">
  <h1>🌲 PageIndex Local: Agentic RAG from Scratch</h1>
  <p>
    <b>A fully open-source, local implementation of vectorless, reasoning-based RAG.</b>
  </p>
  
  [![Python](https://img.shields.io/badge/Python-3.10+-blue.svg)](https://www.python.org)
  [![Framework](https://img.shields.io/badge/Framework-PageIndex-orange.svg)](https://github.com/VectifyAI/PageIndex)
  [![LLM](https://img.shields.io/badge/Local_LLM-Ollama_%7C_Llama_3.1-black.svg)](https://ollama.com/)
  [![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

  <p>
    <a href="#-architecture--how-it-works">Architecture</a> •
    <a href="#%EF%B8%8F-prerequisites">Prerequisites</a> •
    <a href="#-quickstart">Quickstart</a> •
    <a href="#-under-the-hood-inspecting-the-tree">Under the Hood</a>
  </p>
</div>

---

## 📖 Overview

Traditional RAG systems rely on chopping documents into meaningless chunks and retrieving them via mathematical vector similarity—often returning data that is mathematically similar but contextually irrelevant. 

This repository demonstrates **Agentic Tree RAG** using [PageIndex](https://github.com/VectifyAI/PageIndex). It runs entirely locally, bypassing vector databases completely. Instead, it extracts the document's natural layout into a hierarchical tree, and allows an agentic LLM (Llama 3.1) to dynamically navigate and read it exactly like a human expert would.

## 🧠 Architecture & How It Works

GitHub supports dynamic flowcharts. The diagram below illustrates the fundamental difference between our Agentic RAG approach and standard Vector RAG:

```mermaid
graph TD
    subgraph Traditional Vector RAG
        A1[Document] -->|Blind Chunking| B1[Random Text Chunks]
        B1 -->|Embedding| C1[(Vector Database)]
        D1[User Query] -->|Semantic Search| C1
        C1 -.->|Out of Context| E1[LLM Generation]
    end
    
    subgraph PageIndex Agentic RAG
        A2[Document] -->|Layout Parsing| B2[Hierarchical Tree]
        B2 -->|Summarization| C2[Root > Chapter > Section]
        D2[User Query] --> E2[Agentic LLM]
        E2 <-->|Active Reasoning & Tool Calls| C2
        C2 -.->|Exact Context Block| E2
    end
    
    style E2 fill:#4caf50,stroke:#388e3c,stroke-width:2px,color:#fff


⚙️ Prerequisites
To run this pipeline efficiently without external API costs, you need a machine capable of running local open-weights models.

OS: Linux or Windows via WSL2 (Ubuntu 24.04 recommended)

Compute: A dedicated GPU for fast local inference. This project has been tested and optimized on an NVIDIA RTX 6000 Ada Generation GPU (48 GB VRAM) with 128 GB RAM for lightning-fast tree indexing.

Dependencies: Python 3.10+ and Ollama.

🚀 Quickstart
Follow these steps to spin up the agentic engine on your machine.

1. Initialize the Local LLM Server
Ensure Ollama is installed and running, then pull the Llama 3.1 model:

Bash
ollama run llama3.1
Leave the Ollama server running in the background.

2. Environment Setup
Clone this repository and install the required Python packages:

Bash
git clone [https://github.com/](https://github.com/)<your-username>/pageindex-local-rag.git
cd pageindex-local-rag

python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
3. Fetch the Sample Dataset
We use the foundational AI paper "Attention Is All You Need" as our test corpus. Download the PDF directly into your workspace:

Bash
curl -o attention_is_all_you_need.pdf [https://arxiv.org/pdf/1706.03762.pdf](https://arxiv.org/pdf/1706.03762.pdf)
4. Execute the RAG Pipeline
Run the main application. This will override the standard OpenAI endpoints, point PageIndex to your local Ollama instance, build the tree, and execute a reasoning query.

Bash
python app.py
🔍 Under the Hood: Inspecting the Tree
What does a "Vectorless Document Tree" actually look like?

Run the inspector script to dump the LLM's internal representation of the document:

Bash
python inspect_tree.py
JSON
{
  "node_id": "root",
  "title": "Attention Is All You Need",
  "summary": "A research paper proposing the Transformer architecture...",
  "children": [
    {
      "node_id": "section_1",
      "title": "1. Introduction",
      "summary": "Discusses the limitations of recurrent neural networks...",
      "children": []
    },
    {
      "node_id": "section_3",
      "title": "3. Model Architecture",
      "summary": "Explains the encoder-decoder structure and self-attention...",
      "children": [
        {
          "node_id": "paragraph_3.1",
          "text": "The Transformer follows this overall architecture using stacked self-attention..."
        }
      ]
    }
  ]
}
During retrieval, the LLM evaluates the summary of each node. If a branch is irrelevant, it ignores it. If a branch is highly relevant (like section_3), it actively calls a tool to drill down into the children until it reaches the ground-truth text block.

🤝 Contributing
Contributions, issues, and feature requests are welcome! Feel free to check the issues page.

📄 License
This project is open-source and available under the MIT License.

If you found this implementation helpful, please consider giving the repository a ⭐!
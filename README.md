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
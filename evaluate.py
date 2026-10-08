import os
import json
import requests
from pageindex import PageIndexClient

# Configuration
OLLAMA_URL = "http://localhost:11434/api/generate"
DOC_PATH = "attention_is_all_you_need.pdf"
CACHE_FILE = ".cached_doc_id.txt"

# We use Llama 3.1 for both RAG and Evaluation. 
# (If you downloaded qwen2.5:32b, change EVAL_MODEL to that for a smarter judge!)
RAG_MODEL = "llama3.1"
EVAL_MODEL = "llama3.1"

# Setup PageIndex Client
os.environ["OPENAI_BASE_URL"] = "http://localhost:11434/v1"
os.environ["OPENAI_API_KEY"] = "ollama"
client = PageIndexClient(index=RAG_MODEL, chat=RAG_MODEL)

def get_doc_id():
    with open(CACHE_FILE, "r") as f:
        return f.read().strip()

def run_rag(question, doc_id):
    """Runs the agent and extracts the retrieved context and final answer."""
    stream = client.chat(
        question, 
        doc_id=doc_id, 
        stream=True,
        instructions="Strictly answer using only the retrieved document content."
    )
    
    retrieved_context = ""
    final_answer = ""
    
    for event in stream.events:
        event_type = event.get("type")
        if event_type == "tool_result":
            retrieved_context += str(event.get("output", "")) + "\n"
        elif event_type == "answer":
            final_answer += event.get("delta", "")
            
    return retrieved_context, final_answer

def llm_judge(question, context, answer):
        """Uses Ollama to score the RAG output based on Faithfulness and Relevance."""
        prompt = f"""You are an expert AI evaluator.
        
        QUESTION: {question}
        RETRIEVED CONTEXT: {context[:2000]}...
        AGENT ANSWER: {answer}

        Evaluate the Agent's Answer based on two metrics:
        1. Faithfulness (1-5): Is the answer strictly derived from the context? (5 = 100% grounded, 1 = severe hallucination)
        2. Relevance (1-5): Does it directly answer the user's question? (5 = perfectly relevant, 1 = entirely off-topic)

        You MUST output ONLY a JSON object exactly matching this format, with no other text:
        {{
            "faithfulness": <int>,
            "relevance": <int>,
            "reasoning": "<a short one-sentence explanation for the scores>"
        }}
        """
        
        payload = {
            "model": EVAL_MODEL,
            "prompt": prompt,
            "stream": False,
            "format": "json" 
        }
        
        response = requests.post(OLLAMA_URL, json=payload)
        
        try:
            return json.loads(response.json()["response"])
        except Exception as e:
            return {"faithfulness": 0, "relevance": 0, "reasoning": f"Parse error: {e}"}

def main():
    print("="*60)
    print("PAGEINDEX RAG EVALUATION BENCHMARK")
    print("="*60)
    
    doc_id = get_doc_id()
    
    test_questions = [
        "What is the primary mechanism proposed in this paper?",
        "How does multi-head attention work?",
        "What optimizer was used to train the Transformer?",
        "What are the advantages of self-attention over recurrent layers?",
        "What is the capital of France?" # Guardrail/Hallucination test!
    ]

    for i, q in enumerate(test_questions, 1):
        print(f"\n[Test {i}/5] Question: {q}")
        print("Running Agentic Retrieval...")
        
        context, answer = run_rag(q, doc_id)
        
        print("Running LLM Judge Evaluation...")
        scores = llm_judge(q, context, answer)
        
        print(f"Answer: {answer[:150]}...")
        print(f"📊 Faithfulness Score: {scores.get('faithfulness', 'N/A')}/5")
        print(f"🎯 Relevance Score: {scores.get('relevance', 'N/A')}/5")
        print(f"💡 Judge Reasoning: {scores.get('reasoning', 'N/A')}")
        print("-" * 60)

if __name__ == "__main__":
    main()
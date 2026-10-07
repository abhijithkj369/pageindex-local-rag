import os
from pageindex import PageIndexClient

# 1. Point PageIndex to the local Ollama server
os.environ["OPENAI_BASE_URL"] = "http://localhost:11434/v1"
os.environ["OPENAI_API_KEY"] = "ollama"  # Required by the client, but ignored by Ollama

def main():
    print("Initializing PageIndex with local Llama 3.1...")
    
    # 2. Configure the client to use our open-source model 
    # for both the tree indexing and the retrieval reasoning.
    client = PageIndexClient(
        index="llama3.1", 
        chat="llama3.1",  
    )

    doc_path = "attention_is_all_you_need.pdf"
    
    print(f"\nProcessing: {doc_path}")
    print("Building the hierarchical tree index (Vectorless RAG)...")
    
    # 3. Submit the document. PageIndex runs 'flash indexing' locally.
    result = client.submit_document(doc_path)
    doc_id = result["doc_id"]
    
    print(f"Index built successfully! Document ID: {doc_id}")
    
    # 4. Agentic reasoning over the document tree
    question = "What is the primary mechanism proposed in this paper?"
    print(f"\nQuery: {question}")
    
    answer = client.chat(question, doc_id=doc_id)
    
    print("\n--- Answer ---")
    print(answer)

if __name__ == "__main__":
    main()
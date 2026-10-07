import os
import json
from pageindex import PageIndexClient

# Point to the local Ollama server
os.environ["OPENAI_BASE_URL"] = "http://localhost:11434/v1"
os.environ["OPENAI_API_KEY"] = "ollama"

DOC_PATH = "attention_is_all_you_need.pdf"
CACHE_FILE = ".cached_doc_id.txt"

def get_or_create_document(client):
    # 1. Prevent duplicate document indexing by caching the doc_id locally
    if os.path.exists(CACHE_FILE):
        with open(CACHE_FILE, "r") as f:
            doc_id = f.read().strip()
            print(f"Loaded existing document ID from cache: {doc_id}")
            return doc_id
    
    print(f"Indexing '{DOC_PATH}' for the first time...")
    result = client.submit_document(DOC_PATH)
    doc_id = result["doc_id"]
    
    with open(CACHE_FILE, "w") as f:
        f.write(doc_id)
        
    print(f"Indexing complete. Saved ID to cache.")
    return doc_id

def main():
    # Using Llama 3.1 to observe its schema adherence behavior
    client = PageIndexClient(index="llama3.1", chat="llama3.1")

    print("="*50)
    print("PAGEINDEX AGENTIC RAG - TRACE INSPECTION")
    print("="*50)
    
    doc_id = get_or_create_document(client)
    question = "How does multi-head attention work?"
    
    print(f"\nDocument: {DOC_PATH}")
    print(f"Question: {question}\n")

    # Enable the trace stream
    stream = client.chat(
        question,
        doc_id=doc_id,
        stream=True,
        instructions=(
            "When using get_page_content, you MUST provide the required "
            "`pages` argument. The value must be a page specification such "
            "as `3`, `3-5`, or `1-3,7,9-12`. "
            "Never use `page_range`, `start_index`, or `end_index`."
        ),
    )

    for event in stream.events:
        event_type = event.get("type")

        if event_type == "thinking":
            delta = event.get("delta", "")
            if delta:
                print(f"\033[90m{delta}\033[0m", end="", flush=True)

        elif event_type == "tool_call":
            print("\n\n" + "-"*50)
            print("🛠️ TOOL CALL")
            print("-" * 50)
            print(f"Tool: {event.get('name')}")
            
            # Safely format the arguments
            args = event.get("arguments", {})
            if isinstance(args, str):
                try:
                    args = json.loads(args)
                except json.JSONDecodeError:
                    pass
            print(f"Arguments:\n{json.dumps(args, indent=2)}")

        elif event_type == "tool_result":
                output_data = event.get("output", "")
                output_str = str(output_data)
                
                is_error = False
                # PageIndex wraps output in {'type': 'text', 'text': '{json...}'}
                if isinstance(output_data, dict) and "text" in output_data:
                    try:
                        parsed_out = json.loads(output_data["text"])
                        if isinstance(parsed_out, dict) and "error" in parsed_out:
                            is_error = True
                    except:
                        pass

                print("\n" + "-"*50)
                if is_error:
                    print("❌ TOOL ERROR")
                else:
                    print("📄 TOOL RESULT")
                print("-" * 50)
                
                if len(output_str) > 800:
                    print(f"{output_str[:800]}...\n\n[...Content truncated for display...]")
                else:
                    print(output_str)

        elif event_type == "answer":
            if not hasattr(stream, "_printed_answer_header"):
                print("\n\n" + "-"*50)
                print("🤖 MODEL OUTPUT")
                print("-"*50)
                stream._printed_answer_header = True
                
            print(event.get("delta", ""), end="", flush=True)

    print("\n\n" + "="*50)

if __name__ == "__main__":
    main()
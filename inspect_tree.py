import os
import json
from pageindex import PageIndexClient

# Point to local Ollama
os.environ["OPENAI_BASE_URL"] = "http://localhost:11434/v1"
os.environ["OPENAI_API_KEY"] = "ollama"

client = PageIndexClient(index="llama3.1", chat="llama3.1")

# Replace with the document ID from your previous run!
doc_id = "pi-ecfa131288be432e92c1da24a3c14608" 

print("Fetching the hierarchical document tree...")

# 1. Pull the raw tree structure
tree = client.get_document_structure(doc_id)

# 2. Save it to a JSON file so we can inspect the hierarchy
output_file = "document_tree.json"
with open(output_file, "w") as f:
    json.dump(tree, f, indent=2)

print(f"Success! Saved the underlying tree to {output_file}.")
print("Open this file in VS Code to see how PageIndex views the document.")
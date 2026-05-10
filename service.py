import os
import json
from langchain_ollama import OllamaEmbeddings
from langchain_chroma import Chroma
from langchain_core.documents import Document

# 1. Path Configurations
JSON_FILE_PATH = "test.json"
DB_LOCATION = "./chrome_langchain_db"

# 2. Initialize your local embedding model
embeddings = OllamaEmbeddings(model="mxbai-embed-large")

# 3. Check if the database already exists to avoid redundant embeddings
add_documents = not os.path.exists(DB_LOCATION)

documents = []
ids = []

if add_documents:
    print("📂 Loading test cases from JSON...")
    
    # Read and parse the JSON file
    with open(JSON_FILE_PATH, "r") as file:
        test_cases = json.load(file)
        
    for item in test_cases:
        # Build semantic text representation for search
        # Combining title and description gives the embedding model plenty of context
        page_content = f"Title: {item['title']}\nDescription: {item['description']}"
        
        # We store metadata to filter searches or retrieve tags/services later
        metadata = {
            "title": item["title"],
            "service": item["service"],
            # Chroma metadata fields must be simple types (strings, ints, floats, or bools).
            # Because tags are a list, we join them into a comma-separated string.
            "tags": ", ".join(item["tags"]) 
        }
        
        # Use the JSON test-case ID (e.g., 'TC-AUTH-001') directly as the document ID
        doc_id = item["id"]
        
        document = Document(
            page_content=page_content,
            metadata=metadata,
            id=doc_id
        )
        
        documents.append(document)
        ids.append(doc_id)
        
    print(f"✅ Loaded {len(documents)} test cases.")

# 4. Initialize (or load) ChromaDB
print("🤖 Initializing Chroma Vector Store...")
vector_store = Chroma(
    collection_name="test_cases_suite",
    persist_directory=DB_LOCATION,
    embedding_function=embeddings
)

# 5. Add documents only if it's a fresh database
if add_documents:
    print("🧬 Generating embeddings and writing to disk...")
    vector_store.add_documents(documents=documents, ids=ids)
    print("💾 Vector Database saved successfully!")
else:
    print("📂 Loaded existing Vector Database from disk.")

# 6. Test retriever functionality
retriever = vector_store.as_retriever(
    search_kwargs={"k": 2}
)

# Let's do a quick query validation
query = "What test should I run to check unauthorized login attempts?"
print(f"\n🔍 Testing retriever with query: '{query}'")
results = retriever.invoke(query)

for i, doc in enumerate(results, 1):
    print(f"\n--- Match {i} ---")
    print(f"ID: {doc.id}")
    print(f"Title: {doc.metadata['title']}")
    print(f"Tags: {doc.metadata['tags']}")
from pathlib import Path

import chromadb
from chromadb.utils import embedding_functions

# Step A: Read the document
doc_path = Path(__file__).resolve().parent.parent.parent / "data" / "knowledge_base" / "sip_basics.txt"
text = doc_path.read_text(encoding="utf-8")

# Step B: Split into robust, overlapping chunks
import sys
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from app.rag.chunking import chunk_text

chunks = chunk_text(text, chunk_size=300, overlap=50)

# Step C: Set up the embedding function (converts text to vectors)
embedding_fn = embedding_functions.SentenceTransformerEmbeddingFunction(
    model_name="all-MiniLM-L6-v2"
)

# Step D: Create a Chroma collection and add our chunks
client = chromadb.Client()
collection = client.create_collection(name="test_collection", embedding_function=embedding_fn)

collection.add(
    documents=chunks,
    ids=[f"chunk_{i}" for i in range(len(chunks))],
)

print("Chunks added to Chroma. Now let's search!\n")

# Step E: Ask a question and retrieve the closest chunk(s)
question = "what is the difference between old vs new tax regime in india?"
results = collection.query(query_texts=[question], n_results=2)

print(f"Question: {question}\n")
print("Top matching chunks:\n")
for chunk_text, distance in zip(results["documents"][0], results["distances"][0]):
    print(f"(distance: {distance:.4f})")
    print(chunk_text)
    print()
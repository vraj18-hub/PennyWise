import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from app.rag.loader import load_and_chunk_documents
from app.rag.vectorstore import get_collection


def run_ingestion():
    chunks = load_and_chunk_documents()

    if not chunks:
        print("No documents found in data/knowledge_base/. Nothing to ingest.")
        return

    collection = get_collection()

    collection.upsert(
        ids=[c["id"] for c in chunks],
        documents=[c["text"] for c in chunks],
        metadatas=[{"source": c["source"]} for c in chunks],
    )

    print(f"Ingested {len(chunks)} chunks from the knowledge base:")
    sources = sorted(set(c["source"] for c in chunks))
    for source in sources:
        count = sum(1 for c in chunks if c["source"] == source)
        print(f"  - {source}: {count} chunks")


if __name__ == "__main__":
    run_ingestion()